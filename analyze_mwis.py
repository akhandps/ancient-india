"""Certified MWIS experiments on textual records, with explicit weight choices."""
import csv
import hashlib
import itertools
import json
import os
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from analyze_agastya import PERSON_TYPES, CHECKED, make_graph
from analyze_distant_pairs import family

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'research/mwis'
INPUT_REF='bc7f074adeb3844790af1aca99e54bddb7bfaa99'


def solve_mwis(graph,weights,excluded=(),time_limit=45,max_size=None,included=()):
    """Return a feasible independent set and the solver's optimality certificate.

    Positive integer weights. No heuristic result is labeled optimal. The
    secondary exclusion solves retain exactly the same primary objective.
    """
    names=sorted(graph);index={n:i for i,n in enumerate(names)}
    if not names:
        return dict(selected=[],objective=0,status=0,optimal=True,gap=0.,upper_bound=0.,seconds=0.)
    assert set(weights)==set(names)
    assert all(isinstance(weights[n],int) and weights[n]>0 for n in names)
    rows=[];cols=[]
    for i,(a,b) in enumerate(graph.edges()):
        rows.extend([i,i]);cols.extend([index[a],index[b]])
    constraints=[]
    if rows:
        matrix=coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(graph.number_of_edges(),len(names))).tocsc()
        constraints.append(LinearConstraint(matrix,-np.inf,1))
    if max_size is not None:
        constraints.append(LinearConstraint(np.ones((1,len(names))),-np.inf,max_size))
    upper=np.ones(len(names))
    lower=np.zeros(len(names))
    for n in excluded:upper[index[n]]=0
    for n in included:lower[index[n]]=1
    assert not set(excluded).intersection(included)
    start=time.monotonic()
    result=milp(-np.array([weights[n] for n in names],dtype=float),
                integrality=np.ones(len(names)),bounds=Bounds(lower,upper),
                constraints=constraints,options={'time_limit':time_limit,'mip_rel_gap':0.0})
    if result.x is None:raise RuntimeError(f'No feasible solution: {result.message}')
    selected={n for n,x in zip(names,result.x) if x>.5}
    assert not any(a in selected and b in selected for a,b in graph.edges())
    assert not selected.intersection(excluded)
    assert set(included).issubset(selected)
    assert max_size is None or len(selected)<=max_size
    score=sum(weights[n] for n in selected)
    bound=getattr(result,'mip_dual_bound',None)
    gap=getattr(result,'mip_gap',None)
    return dict(selected=sorted(selected),objective=score,status=int(result.status),
                optimal=bool(result.status==0),gap=None if gap is None else float(gap),
                upper_bound=None if bound is None else float(-bound),
                solver_message=str(result.message),seconds=time.monotonic()-start)


def conflict_graph(original,candidates,distance=1):
    """Use original-graph distances; paths may pass through non-candidates."""
    if distance==1:return original.subgraph(sorted(candidates)).copy()
    result=nx.Graph();result.add_nodes_from(sorted(candidates));pool=set(candidates)
    for u in sorted(candidates):
        for v,d in nx.single_source_shortest_path_length(original,u,cutoff=distance).items():
            if u<v and v in pool and d>0:result.add_edge(u,v)
    return result


def diagnostics(original,selected,nodes):
    selected=set(selected)
    shared=set()
    common=[]
    for n in original:
        neighbors=sorted(selected.intersection(original[n]))
        if len(neighbors)>=2:
            common.append(dict(id=n,label=nodes[n]['label'],selected_neighbors=len(neighbors)))
            shared.update(itertools.combinations(neighbors,2))
    counts=Counter(original.degree(n) for n in selected)
    return dict(selected_count=len(selected),selected_isolates=counts[0],
        selected_degree_at_most_one=counts[0]+counts[1],
        original_edges_inside_set=original.subgraph(selected).number_of_edges(),
        selected_pairs_with_common_neighbor=len(shared),
        shared_neighbor_examples=sorted(common,key=lambda x:(-x['selected_neighbors'],x['id']))[:8])


def main():
    OUT.mkdir(exist_ok=True)
    raw=subprocess.check_output(['git','show',f'{INPUT_REF}:research/agastya/graph.json'],cwd=ROOT)
    data=json.loads(raw)
    nodes={n['id']:n for n in data['nodes']};sources={s['id']:s for s in data['sources']}
    people={i for i,n in nodes.items() if n['type'] in PERSON_TYPES}
    claims=[c for c in data['claims'] if c['subject'] in people and c['object'] in people and c['status']!='identity_hypothesis']
    graph=make_graph(claims,people)
    print('Computing exact betweenness...',flush=True)
    bc=nx.betweenness_centrality(graph,weight=None,normalized=True)
    families=defaultdict(set)
    for c in claims:
        if c['status'] in CHECKED:
            for n in [c['subject'],c['object']]:families[n].add(family(c['source'],sources))
    profiles={
        'uniform':{n:1 for n in graph},
        'degree':{n:1+graph.degree(n) for n in graph},
        'source_diversity':{n:1+len(families[n]) for n in graph},
        'bridge':{n:1+int(round(10000*bc[n])) for n in graph},
    }
    hubs=sorted(n for n in graph if graph.degree(n)>=5)
    experiments=[(name,graph,weights,1,None) for name,weights in profiles.items()]
    for distance in [1,2]:
        experiments.append((f'hubs_distance_{distance}',conflict_graph(graph,hubs,distance),
                            {n:profiles['bridge'][n] for n in hubs},distance,None))
    experiments.append(('hubs_distance_2_budget_10',conflict_graph(graph,hubs,2),
                         {n:profiles['bridge'][n] for n in hubs},2,10))
    output=dict(input_commit=INPUT_REF,input_sha256=hashlib.sha256(raw).hexdigest(),
        versions={'scipy':scipy.__version__,'networkx':nx.__version__,'numpy':np.__version__},
        graph={'nodes':len(graph),'edges':graph.number_of_edges(),'isolates':nx.number_of_isolates(graph),'hub_candidates':len(hubs)},
        objective='maximize sum(w_v*x_v); binary x_v; x_u+x_v<=1 for every conflict edge',
        weights={'uniform':'1','degree':'1 + original degree',
                 'source_diversity':'1 + number of incident passage-checked source families',
                 'bridge':'1 + round(10000 * exact normalized original-graph betweenness)'},
        models={})
    rows=[]
    for n in sorted(graph):
        row=dict(id=n,label=nodes[n]['label'],degree=graph.degree(n),betweenness=bc[n],
                 source_families='; '.join(sorted(families[n])))
        for name,w in profiles.items():row[name+'_weight']=w[n]
        rows.append(row)
    for name,conflicts,weights,distance,max_size in experiments:
        answer=solve_mwis(conflicts,weights,max_size=max_size)
        selected=set(answer['selected'])
        answer.update(diagnostics(graph,selected,nodes))
        answer['conflict_distance']=distance
        answer['cardinality_limit']=max_size
        answer['candidate_nodes']=len(conflicts)
        answer['conflict_edges']=conflicts.number_of_edges()
        selected_rows=[dict(id=n,label=nodes[n]['label'],weight=weights[n],
            degree=graph.degree(n),betweenness=bc[n],families=sorted(families[n]))
            for n in sorted(selected,key=lambda n:(-weights[n],n))]
        answer['top_selected']=selected_rows if name.startswith('hubs_') else selected_rows[:30]
        if name.startswith('hubs_') and answer['optimal']:
            stability=[]
            for n in sorted(selected):
                alternative=solve_mwis(conflicts,weights,excluded=[n],time_limit=15,max_size=max_size)
                classification=('mandatory' if alternative['objective']<answer['objective'] else 'optional') if alternative['optimal'] else 'undetermined'
                stability.append(dict(id=n,label=nodes[n]['label'],classification=classification,
                    optimum_without_record=alternative['objective'],alternative_optimal=alternative['optimal']))
            answer['selected_membership_stability']=stability
        if name=='hubs_distance_2_budget_10' and answer['optimal']:
            probes=[]
            for n in ['indra','mb_adi_inc_arjuna_human_incarnation','vp4_13_jambavant','vp4_15_kṛṣṇa']:
                alternative=solve_mwis(conflicts,weights,included=[n],max_size=max_size)
                probes.append(dict(id=n,label=nodes[n]['label'],
                    forced_objective=alternative['objective'],alternative_optimal=alternative['optimal'],
                    objective_loss=answer['objective']-alternative['objective'],
                    selected=alternative['selected'],
                    selected_labels=[nodes[v]['label'] for v in sorted(alternative['selected'],key=lambda v:(-weights[v],v))],
                    conflicts_with_selected=[dict(id=v,label=nodes[v]['label'],weight=weights[v])
                                             for v in sorted(selected.intersection(conflicts[n]))]))
            answer['forced_in_probes']=probes
        output['models'][name]=answer
        for row in rows:row[name+'_selected']=row['id'] in selected
        print(name,'optimal',answer['optimal'],'weight',answer['objective'],
              'size',len(selected),'shared-neighbor pairs',answer['selected_pairs_with_common_neighbor'],flush=True)
    # Pairwise overlap is descriptive: the objectives have different meanings.
    output['selection_jaccard']={}
    for a,b in itertools.combinations(output['models'],2):
        aa=set(output['models'][a]['selected']);bb=set(output['models'][b]['selected'])
        output['selection_jaccard'][a+' / '+b]=len(aa&bb)/len(aa|bb) if aa|bb else 1.
    (OUT/'results.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    with (OUT/'memberships.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    write_report(output)
    plot_panel(output)


def write_report(r):
    lines=['# Maximum-weight independent sets','',
        f'Input: commit `{r["input_commit"]}`, SHA-256 `{r["input_sha256"]}`.','',
        'Each selected record is nonadjacent to every other selected record in the specified conflict graph. An independent set is not evidence of unrelated cultures, independent testimonies, or historical separation.','',
        'The solver uses binary variables and one at-most-one constraint per edge. It maximizes positive integer weights by minimizing their negative sum. A zero requested relative MIP gap is used. A time-limited feasible solution would be labeled nonoptimal. See [SciPy MILP documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html).','',
        '| Model | Candidates | Conflicts | Size cap | Selected | Weight | Optimal | Gap |',
        '|---|---:|---:|---:|---:|---:|---|---:|']
    for name,m in r['models'].items():
        lines.append(f'| {name} | {m["candidate_nodes"]} | {m["conflict_edges"]} | {m["cardinality_limit"]} | {m["selected_count"]} | {m["objective"]} | {m["optimal"]} | {m["gap"]} |')
    lines+=['','## Weights','']
    for k,v in r['weights'].items():lines.append(f'- {k}: `{v}`')
    lines+=['','## How the models differ','',
        'The four full-graph models share the same person-like universe, including deities, collectives and Agastya facets. Texts, places and objects are excluded; identity hypotheses are excluded, while other explicit identity and comparison claims remain conflict edges. Multiple claims per pair collapse to one undirected edge. No source-local dossiers are merged. All positive-weight isolates are necessarily selected.','',
        'The two hub models use every original record of degree at least five. This is an explicit exploratory candidate filter, not a discovered natural threshold. Their weights are the bridge weights computed on the full original graph. `hubs_distance_1` forbids only direct adjacency. `hubs_distance_2` also forbids sharing an original-graph neighbor, including neighbors outside the candidate pool. Thus distance two is measured before restricting candidates, rather than in the induced hub subgraph.','',
        '`hubs_distance_2_budget_10` adds a cap of ten selected records to that stricter conflict graph. This is a cardinality-constrained MWIS variant for a readable research shortlist, not the unconstrained optimum. Its membership-exclusion tests retain the same cap.','',
        'Integer rounding defines the bridge objective: certified optimality applies to that integerized score, not to an unrounded real-valued centrality sum. Source families group editions of the same work and do not establish independent testimony. Claim `facet` tags are not used as source families.','',
        'Different optimal sets may tie. For each selected record in a hub model, we forbid it and resolve the same problem. A strictly lower certified optimum marks that record mandatory for every optimum under that exact model. An equal optimum marks it optional. This is conditional optimizer stability, not robustness to other weights, missing passages or identity changes.','']
    for name in ['hubs_distance_1','hubs_distance_2','hubs_distance_2_budget_10']:
        m=r['models'][name];stable={x['id']:x['classification'] for x in m.get('selected_membership_stability',[])}
        lines += [f'## {name}: selected set','','| Record | Weight | Original degree | Source families | Membership |','|---|---:|---:|---|---|']
        for n in m['top_selected']:
            lines.append(f'| {n["label"]} | {n["weight"]} | {n["degree"]} | {", ".join(n["families"])} | {stable.get(n["id"],"unchecked")} |')
        lines.append('')
    lines+=['## Shared-neighbor audit','',
        'No direct selected–selected edges does not prevent many selected records from sharing a parent or assembly host. This audit counts unique selected pairs with at least one common original-graph neighbor.','']
    for name,m in r['models'].items():
        lines.append(f'- **{name}**: {m["selected_degree_at_most_one"]} selected records have original degree ≤1; {m["selected_pairs_with_common_neighbor"]} selected pairs share a neighbor.')
        for x in m['shared_neighbor_examples'][:2]:lines.append(f'  - {x["label"]}: {x["selected_neighbors"]} selected neighbors.')
    lines+=['','## Forcing a prominent hub into the ten-record shortlist','',
            'These are new solves of the same capped objective, with the named record required. A positive loss measures the tradeoff under this model. Conflicts list members of the original optimum that cannot coexist with the required record.','',
            '| Required record | Best forced weight | Loss from optimum | Conflicting original members |','|---|---:|---:|---|']
    for p in r['models']['hubs_distance_2_budget_10']['forced_in_probes']:
        lines.append(f'| {p["label"]} | {p["forced_objective"]} | {p["objective_loss"]} | {"; ".join(x["label"] for x in p["conflicts_with_selected"])} |')
    lines+=['','## Reproduce','',
        'Install `requirements.txt` into the graph-analysis Python environment, then run `python analyze_mwis.py` from the repository root. The input commit must be available locally. `results.json` records all selected IDs, objectives, upper bounds, gaps and versions; `memberships.csv` includes every record’s scores and memberships.','',
        'These selections are analytical artifacts, not new textual relationships. No claims or edges are added to the canonical graph by this experiment.','']
    (OUT/'README.md').write_text('\n'.join(lines))


def plot_panel(r):
    os.environ.setdefault('MPLCONFIGDIR','/private/tmp/agastya-matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rows=r['models']['hubs_distance_2_budget_10']['top_selected']
    labels=[n['label'].split(' · ')[0] for n in rows]
    fig,ax=plt.subplots(figsize=(11,6),layout='constrained')
    bars=ax.barh(labels[::-1],[n['weight'] for n in rows][::-1],color='#387d7a')
    ax.bar_label(bars,padding=4);ax.set_xlim(0,max(n['weight'] for n in rows)*1.14)
    ax.set_xlabel('Integer bridge weight: 1 + round(10000 × betweenness)')
    ax.set_title('A ten-record MWIS research shortlist',fontsize=17,pad=14)
    ax.spines[['top','right']].set_visible(False)
    fig.supxlabel('Candidates have degree ≥5. No selected pair is adjacent or shares a neighbor in the original graph.\nThis is a size-constrained optimization over recorded textual relationships, not evidence of historical independence.',fontsize=9)
    fig.savefig(OUT/'shortlist.png',dpi=180,facecolor='white');plt.close(fig)


if __name__=='__main__':main()
