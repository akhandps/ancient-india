"""Exact finite graph extremes, disconnected pairs, and sourced bridge tests.

The before graph is retrieved from the immutable pre-experiment Git commit.
No source data is fetched, inferred, merged, or overwritten by this script.
"""
import hashlib
import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path

import networkx as nx
from analyze_agastya import PERSON_TYPES, edge_class, make_graph, source_family

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'research/distant-pairs'
BASELINE_REF='25c0987ee447cac76feecc74fb4884d40b494b25'
PAIR_IDS=[
    ('vp1112_satvata','vp24_sumalya'),
    ('vp24_candragupta','vp67_parashurama'),
    ('vp22_sumitra_ikshvaku','vp20_abhimanyu'),
    ('rama','vp24_ashokavardhana'),
]


def load_baseline():
    raw=subprocess.check_output(['git','show',f'{BASELINE_REF}:research/agastya/graph.json'],cwd=ROOT)
    return raw,json.loads(raw)


def project(data,claims):
    people={n['id'] for n in data['nodes'] if n['type'] in PERSON_TYPES}
    eligible=[c for c in claims if c['subject'] in people and c['object'] in people
              and c['status']!='identity_hypothesis']
    return make_graph(eligible,people)


def family(source,sources):
    title=sources[source]['title']
    if 'Rāmāyaṇa' in title:return 'Ramayana'
    if 'Bhāgavata' in title or 'Bhāgavatam' in title:return 'Bhagavata'
    if 'Viṣṇu Purāṇa' in title:return 'Vishnu Purana'
    return source_family(source)


def extremes(g,node_families):
    """Exact BFS from every vertex, including every connected component.

    Disconnected pairs do not compete with finite distances. Candidate lists
    retain at most 20 examples, while tie counts remain exact.
    """
    comps=sorted(nx.connected_components(g),key=lambda c:(-len(c),min(c)))
    finite_max=-1; far=[]; far_count=0
    cross_max=-1; cross=[]; cross_count=0
    component_rows=[]
    for comp in comps:
        diameter=0
        for u in sorted(comp):
            distances=nx.single_source_shortest_path_length(g,u)
            for v,d in distances.items():
                if u>=v:continue
                diameter=max(diameter,d)
                if d>finite_max:finite_max=d;far=[];far_count=0
                if d==finite_max:
                    far_count+=1
                    if len(far)<20:far.append([u,v])
                if node_families[u] and node_families[v] and node_families[u].isdisjoint(node_families[v]):
                    if d>cross_max:cross_max=d;cross=[];cross_count=0
                    if d==cross_max:
                        cross_count+=1
                        if len(cross)<20:cross.append([u,v])
        component_rows.append({'size':len(comp),'diameter':diameter,
            'representative_nodes':sorted(comp,key=lambda n:(-g.degree(n),n))[:6]})
    total=len(g)*(len(g)-1)//2
    connected_pairs=sum(len(c)*(len(c)-1)//2 for c in comps)
    return dict(nodes=len(g),edges=g.number_of_edges(),components=len(comps),
        isolates=nx.number_of_isolates(g),largest_component=len(comps[0]),
        unreachable_unordered_pairs=total-connected_pairs,
        maximum_finite_distance=max(0,finite_max),farthest_pair_count=far_count,
        farthest_pairs=far,cross_family_maximum=cross_max,
        cross_family_tie_count=cross_count,cross_family_examples=cross,
        component_summaries=component_rows)


def describe_path(g,a,b,claims,nodes,sources):
    if not nx.has_path(g,a,b):return {'distance':None,'steps':[]}
    path=nx.shortest_path(g,a,b)
    steps=[]
    for u,v in zip(path,path[1:]):
        evidence=[]
        for cid in g[u][v]['claim_ids']:
            c=claims[cid]
            evidence.append({k:c.get(k) for k in ['id','subject','predicate','object','source','locator','status','category','note']}
                | {'url':sources[c['source']]['url'],
                   'subject_label':nodes[c['subject']]['label'],
                   'object_label':nodes[c['object']]['label']})
        steps.append(dict(from_id=u,to_id=v,from_label=nodes[u]['label'],
                          to_label=nodes[v]['label'],evidence=evidence))
    return {'distance':len(path)-1,'nodes':path,'steps':steps}


def main():
    OUT.mkdir(exist_ok=True)
    raw,before=load_baseline()
    additions=json.loads((ROOT/'research/agastya/expansion/distance_bridges.json').read_text())
    nodes={n['id']:n for n in before['nodes']}
    sources={s['id']:s for s in before['sources']+additions['sources']}
    all_claims=before['claims']+additions['claims']
    by_id={c['id']:c for c in all_claims}
    assert len(by_id)==len(all_claims)
    for c in all_claims:
        assert c['subject'] in nodes and c['object'] in nodes and c['source'] in sources,c['id']
    families=defaultdict(set)
    for c in all_claims:
        for n in [c['subject'],c['object']]:families[n].add(family(c['source'],sources))
    identities=[c for c in additions['claims'] if c['category']=='identity']
    passages=[c for c in additions['claims'] if c['category']!='identity']
    scenarios={
        'before':before['claims'],
        'continuity_links_only':before['claims']+identities,
        'passage_links_only':before['claims']+passages,
        'combined':all_claims,
        'combined_no_attendance':[c for c in all_claims if edge_class(c['predicate'])!='attendance'],
        'combined_no_nanda_comparison':[c for c in all_claims if c['id'] not in {'FD002','FD004'}],
    }
    # One source-family classification, frozen from the before graph, is used
    # for all candidate rankings, so newly read sources do not redefine groups.
    baseline_families=defaultdict(set)
    for c in before['claims']:
        for n in [c['subject'],c['object']]:baseline_families[n].add(family(c['source'],sources))
    result=dict(baseline_commit=BASELINE_REF,input_path='research/agastya/graph.json',
        baseline_sha256=hashlib.sha256(raw).hexdigest(),networkx=nx.__version__,
        additions_sha256=hashlib.sha256((ROOT/'research/agastya/expansion/distance_bridges.json').read_bytes()).hexdigest(),
        method='Exact unweighted undirected BFS distances across every person-like component. Disconnected pairs remain undefined. No anonymous name merging or missing-edge prediction.',
        scenarios={})
    selected=list(PAIR_IDS)
    for name,cc in scenarios.items():
        g=project(before,cc)
        row=extremes(g,baseline_families)
        if name=='before':
            for pair in row['cross_family_examples'][:2]:
                if tuple(pair) not in selected:selected.append(tuple(pair))
        row['selected_pairs']=[dict(ids=[a,b],labels=[nodes[a]['label'],nodes[b]['label']],
            **describe_path(g,a,b,by_id,nodes,sources)) for a,b in selected]
        row['farthest_labels']=[[nodes[n]['label'] for n in p] for p in row['farthest_pairs']]
        result['scenarios'][name]=row
        print(name,{k:row[k] for k in ['components','largest_component','maximum_finite_distance']},
              'selected distances',[p['distance'] for p in row['selected_pairs']],flush=True)
    (OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    write_report(result,nodes,additions)
    plot(result)


def write_report(r,nodes,additions):
    lines=['# Distant-pair experiment','',
        f'Before graph: commit `{r["baseline_commit"]}`; SHA-256 `{r["baseline_sha256"]}`.','',
        'Exact maximum finite distance is computed over every component. A disconnected pair has no finite distance, so disconnected and far-apart pairs are reported separately. These are distances between textual records, not measures of historical or cultural relatedness.','',
        '| Scenario | Components | Largest component | Maximum finite distance |',
        '|---|---:|---:|---:|']
    for name,row in r['scenarios'].items():
        lines.append(f'| {name} | {row["components"]} | {row["largest_component"]} | {row["maximum_finite_distance"]} |')
    lines+=['','## Selected pairs','','| Pair | Before | Continuity only | Passage additions only | Combined |','|---|---:|---:|---:|---:|']
    for i,p in enumerate(r['scenarios']['before']['selected_pairs']):
        vals=[]
        for name in ['before','continuity_links_only','passage_links_only','combined']:
            distance=r['scenarios'][name]['selected_pairs'][i]['distance']
            vals.append('disconnected' if distance is None else str(distance))
        lines.append('| '+' ↔ '.join(p['labels'])+' | '+' | '.join(vals)+' |')
    lines+=['','## How the farthest original pair changes','']
    pair=PAIR_IDS[0]
    for name in ['before','continuity_links_only','passage_links_only','combined']:
        p=next(p for p in r['scenarios'][name]['selected_pairs'] if p['ids']==list(pair))
        lines+=[f'### {name}: {p["distance"]} links','',
                ' → '.join(nodes[n]['label'] for n in p['nodes']),'']
    lines+=['## Added evidence','',
            'Full qualifiers and locators are in `../agastya/expansion/distance_bridges.json`. No nodes are merged.','']
    for c in additions['claims']:
        lines.append(f'- **{c["id"]}**: {nodes[c["subject"]]["label"]} → `{c["predicate"]}` → {nodes[c["object"]]["label"]}. {c["status"]}; {c["source"]}, {c["locator"]}.')
    lines+=['','## Interpretation and limits','',
        '- The baseline maximum has a long genealogy at each end. Distance is dominated by sampled lineage chains, rather than an absence of thematic connections.',
        '- The Satvata and Bṛhadbala continuity links are editorial claims from chapter context; they remain separately filterable and do not collapse source-local dossiers.',
        '- The Nanda–Paraśurāma edge is a comparison, not an encounter. The final scenario removes only its two supporting claims, FD002 and FD004, to test that exact shortcut.',
        '- Kauṭilya’s action and the Maurya-to-Śuṅga transition are encoded in the source’s future-narrative register. No calendar chronology is inferred.',
        '- Different translations of the same work provide another reading check, not independent historical corroboration.',
        '- A path through an identity claim, a comparison, and a prediction cannot be interpreted as a chain of people who met.',
        '- Added links can connect formerly separate components and increase the global diameter even while shortening a selected pair. Do not equate diameter alone with improved data quality.',
        '- The comparison table isolates the two chapter-continuity links from six passage-checked claims, which produce four distinct non-identity edges.',
        '- Cross-family candidates use disjoint sets of incident source families in the original dataset. This is a coverage-based filter, not a semantic similarity model.',
        '', '## Reproduce','',
        'Use the dependencies in `../agastya/analysis/requirements.txt`, then run `python analyze_distant_pairs.py` from the repository root. The script uses `git show` to retrieve the immutable baseline commit. A shallow clone must contain that commit. All shortest-path steps, supporting claim IDs, directions and source URLs are retained in `results.json`.','']
    (OUT/'README.md').write_text('\n'.join(lines))


def plot(r):
    os.environ.setdefault('MPLCONFIGDIR','/private/tmp/agastya-matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    stages=['before','continuity_links_only','passage_links_only','combined']
    values=[r['scenarios'][s]['selected_pairs'][0]['distance'] for s in stages]
    fig,ax=plt.subplots(figsize=(10,4.5),layout='constrained')
    bars=ax.barh(['Original graph','Chapter continuity only','New passage claims only','Both additions'][::-1],values[::-1],color=['#387d7a','#6b9f98','#af9c7a','#273e48'])
    ax.bar_label(bars,padding=5);ax.set_xlim(0,max(values)*1.15)
    ax.set_xlabel('Shortest path length (undirected textual links)')
    ax.set_title('Satvata ↔ Sumalya: testing the original 93-link extreme',fontsize=15,pad=15)
    ax.spines[['top','right']].set_visible(False)
    fig.supxlabel('Continuity, comparison, and narrative action are different kinds of connection. No historical meetings are implied.',fontsize=9)
    fig.savefig(OUT/'distance-changes.png',dpi=180,facecolor='white');plt.close(fig)


if __name__=='__main__':main()
