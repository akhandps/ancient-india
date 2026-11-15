"""Reproducible exploratory analysis of textual claims, never historical meetings.

Run: python analyze_agastya.py (see research/agastya/analysis/README.md).
Source data is read-only. All generated artifacts go in analysis/.
"""
import csv
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'research/agastya/analysis'
PERSON_TYPES = {'person', 'deity', 'deity_collective', 'celestial', 'asura',
                'commentator', 'poet', 'bodhisattva', 'people_collective',
                'person_collective', 'person_or_entity', 'person_or_king',
                'person_or_prince', 'agastya_facet'}
CHECKED = {'translation_checked', 'source_text_checked'}
PARENT_FORWARD = {'father_of', 'is_father_of', 'mother_of', 'is_mother_of',
                  'is_named_mother_of', 'has_son', 'has_son_named',
                  'is_named_as_father_of', 'is_parent_of', 'gave_birth_to'}
PARENT_REVERSE = {'son_of', 'is_son_of', 'daughter_of', 'is_daughter_of',
                  'is_child_of', 'mother_is', 'is_called_son_of'}
SPOUSE = {'married', 'is_married_to', 'is_husband_of', 'husband_of',
          'is_wife_of', 'wife_of', 'spouse_of', 'is_described_as_wife_of',
          'is_consort_of', 'is_partner_of', 'conjugal_partner_of'}
TEACH_FORWARD = {'teacher_of', 'is_spiritual_teacher_of',
                 'instructed', 'instructs', 'teaches_dharma_to',
                 'teaches_buddha_dharma_to', 'traditionally_teaches'}
TEACH_REVERSE = {'is_disciple_of', 'trained_by', 'studies_veda_under', 'is_instructed_by',
                 'commentarially_identified_as_pupil_of',
                 'traditionally_learns_tamil_from', 'alternatively_learns_tamil_from'}
NARRATIVE = {'asks_about', 'speaks_about', 'narrates_deeds_of', 'recounts_deeds_of',
             'tells_story_of', 'cites_story_of', 'cites_as_precedent',
             'cited_as_precedent_by', 'mentions', 'mentions_in_attributed_hymn',
             'story_also_names', 'writes_about', 'comparison_for', 'is_compared_to'}
KILL_FORWARD = {'killed', 'kills', 'kills_in_battle', 'slayer_of', 'struck_down'}
KILL_REVERSE = {'was_slain_by', 'is_slain_by', 'killed_by'}
# These are excluded from typed motifs, not silently rewritten in the input.
NORMALIZATION_EXCLUSIONS = {
    'MBAPE128': 'Predicate says father; summary and note explicitly deny parentage and describe teaching.'}


def edge_class(p):
    if ('attend' in p or p in {'named_as_present_at_rajasuya_of', 'present_at_rajasuya_of'}):
        return 'attendance'
    if p.startswith('is_predicted_') or p == 'prophesies_birth_as':
        return 'prediction'
    if (p in PARENT_FORWARD | PARENT_REVERSE | SPOUSE or
        any(t in p for t in ['father', 'mother', 'son_of', 'daughter', 'child',
                             'offspring', 'brother', 'sister', 'sibling', 'lineage',
                             'ancestor', 'parentage', 'beget', 'begot',
                             'born_from', 'womb_of', 'adopt', 'raised_as_son'])):
        return 'kinship'
    if p in TEACH_FORWARD | TEACH_REVERSE:
        return 'teaching'
    if p in NARRATIVE:
        return 'narration_or_reference'
    return 'other'


def source_family(s):
    # Explicit source identifiers rather than claim.facet: facet is a collection
    # tag and does not reliably identify the text that supplies the passage.
    if s.startswith('mb') or s == 'inm_nahusha': return 'Mahabharata'
    if s.startswith('vp'): return 'Vishnu Purana'
    if s.startswith(('sb', 'bp', 'puranic_bp')): return 'Bhagavata'
    if s.startswith('ram'): return 'Ramayana'
    if s.startswith(('rv', 'vedic', 'ts')): return 'Vedic'
    if s.startswith('root_bc'): return 'Buddhacarita'
    if s == 'root_bd4': return 'Brihaddevata'
    if s == 'tamil_manimekalai_hart': return 'Manimekalai'
    if s == 'tamil_puram201_translation_excerpt': return 'Purananuru excerpt'
    return 'Scholarship'


def make_graph(claims, all_people):
    g = nx.Graph()
    # Keep the identical node universe across edge-ablation experiments.
    g.add_nodes_from(sorted(all_people))
    for c in claims:
        u, v = c['subject'], c['object']
        if u == v: continue
        if not g.has_edge(u, v): g.add_edge(u, v, claim_ids=[])
        g[u][v]['claim_ids'].append(c['id'])
    return g


def metrics(g, roots):
    sizes = sorted((len(c) for c in nx.connected_components(g)), reverse=True)
    distances = nx.multi_source_dijkstra_path_length(g, roots, weight=None)
    return {'nodes': len(g), 'active_nodes': sum(d > 0 for _, d in g.degree()),
            'edges': g.number_of_edges(), 'components': len(sizes),
            'isolates': nx.number_of_isolates(g), 'largest_component': sizes[0],
            'reachable_from_any_agastya': len(distances) - len(roots),
            'within_three_hops': sum(0 < d <= 3 for d in distances.values()),
            'triangles': sum(nx.triangles(g).values()) // 3}


def write_csv(name, rows):
    if not rows: return
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    raw = (OUT / 'input-graph.json').read_bytes()
    data = json.loads(raw)
    nodes = {n['id']: n for n in data['nodes']}
    sources = {s['id']: s for s in data['sources']}
    by_id = {c['id']: c for c in data['claims']}
    people = {n['id'] for n in data['nodes'] if n['type'] in PERSON_TYPES}
    roots = sorted(n for n in people if nodes[n]['type'] == 'agastya_facet')
    claims = [c for c in data['claims'] if c['subject'] in people and
              c['object'] in people and c['status'] != 'identity_hypothesis']
    label = lambda n: nodes[n]['label']
    variants = {
        'baseline': claims,
        'checked_only': [c for c in claims if c['status'] in CHECKED],
        'no_attendance': [c for c in claims if edge_class(c['predicate']) != 'attendance'],
        'no_kinship': [c for c in claims if edge_class(c['predicate']) not in {'kinship', 'prediction'}],
        'no_attendance_or_kinship': [c for c in claims if edge_class(c['predicate']) not in {'attendance', 'kinship', 'prediction'}],
        'no_narration': [c for c in claims if edge_class(c['predicate']) != 'narration_or_reference'],
        'no_secondary_identity': [c for c in claims if c.get('category') != 'identity'],
    }
    graphs = {k: make_graph(v, people) for k, v in variants.items()}
    results = {'input_sha256': hashlib.sha256(raw).hexdigest(),
               'input_path': 'research/agastya/analysis/input-graph.json', 'seed': 42,
               'versions': {'networkx': nx.__version__},
               'counts': {'nodes': len(nodes), 'claims': len(data['claims']),
                          'person_like_nodes': len(people), 'person_like_claims': len(claims),
                          'agastya_facets': roots},
               'relationship_classes': dict(Counter(edge_class(c['predicate']) for c in claims)),
               'variants': {}, 'centrality': {}, 'communities': {}}
    centralities = {}
    print(f'Running exact betweenness and Louvain on {len(variants)} variants...', flush=True)
    community_rows = []
    for name, g in graphs.items():
        results['variants'][name] = metrics(g, roots)
        bc = nx.betweenness_centrality(g, normalized=True, weight=None)
        centralities[name] = bc
        top = sorted(bc, key=lambda n: (-bc[n], n))[:25]
        results['centrality'][name] = [dict(id=n, label=label(n),
              betweenness=bc[n], degree=g.degree(n)) for n in top]
        active = g.subgraph([n for n, d in g.degree() if d]).copy()
        communities = nx.community.louvain_communities(active, seed=42, weight=None)
        communities.sort(key=lambda c: (-len(c), min(c)))
        membership = {n: i for i, c in enumerate(communities) for n in c}
        summaries = []
        for i, comm in enumerate(communities):
            cc = [c for c in variants[name] if c['subject'] in comm and c['object'] in comm]
            summaries.append({'community': i, 'size': len(comm),
                'top_nodes': [label(n) for n in sorted(comm, key=lambda n: (-g.degree(n), n))[:6]],
                'source_families': dict(Counter(source_family(c['source']) for c in cc))})
            community_rows.extend(dict(variant=name, community=i, id=n, label=label(n)) for n in sorted(comm))
        results['communities'][name] = {'count': len(communities),
              'modularity': nx.community.modularity(active, communities, weight=None),
              'groups': summaries}
        # Participation distinguishes hubs whose neighbors occupy many communities.
        participation = {}
        for n in active:
            counts = Counter(membership[v] for v in active[n])
            participation[n] = 1 - sum((v / active.degree(n)) ** 2 for v in counts.values())
        results['communities'][name]['participation'] = [
            dict(id=n, label=label(n), participation=participation[n], degree=g.degree(n))
            for n in sorted((n for n in active if g.degree(n) >= 5),
                            key=lambda n: (-participation[n], -bc[n], n))[:20]]
        print(name, results['variants'][name], flush=True)
    write_csv('communities.csv', community_rows)
    ranks = {k: {n: i + 1 for i, n in enumerate(sorted(bc, key=lambda n: (-bc[n], n)))}
             for k, bc in centralities.items()}
    ranking_rows = []
    for n in sorted(people):
        row = {'id': n, 'label': label(n)}
        for name, g in graphs.items():
            row[name + '_degree'] = g.degree(n)
            row[name + '_betweenness'] = centralities[name][n]
            row[name + '_rank'] = ranks[name][n] if centralities[name][n] else ''
        ranking_rows.append(row)
    write_csv('centrality.csv', ranking_rows)

    # Exact articulation impact relative to the node's original component.
    g = graphs['baseline']; comp = {}
    for c in nx.connected_components(g):
        for n in c: comp[n] = c
    articulations = []
    for n in nx.articulation_points(g):
        parts = sorted((len(c) for c in nx.connected_components(g.subgraph(comp[n] - {n}))), reverse=True)
        articulations.append(dict(id=n, label=label(n), separated_from_largest_piece=sum(parts[1:]),
                                  pieces=parts, degree=g.degree(n)))
    results['articulations'] = sorted(articulations, key=lambda x: (-x['separated_from_largest_piece'], x['id']))

    # Leave one source record out. A record can be a whole book or a single hymn.
    base_dist = nx.multi_source_dijkstra_path_length(g, roots, weight=None)
    source_impacts = []
    for s in sorted({c['source'] for c in claims}):
        reduced = make_graph([c for c in claims if c['source'] != s], people)
        d = nx.multi_source_dijkstra_path_length(reduced, roots, weight=None)
        lost = sorted(set(base_dist) - set(d))
        pushed = sorted(n for n in d if 0 < base_dist[n] <= 3 < d[n])
        source_impacts.append(dict(source=s, title=sources[s]['title'],
             removed_claims=sum(c['source'] == s for c in claims),
             unreachable_count=len(lost), unreachable=lost,
             pushed_beyond_three_count=len(pushed), pushed_beyond_three=pushed))
    results['source_ablation'] = sorted(source_impacts, key=lambda x: (-x['unreachable_count'], x['source']))
    results['source_family_ablation'] = {}
    for family in sorted({source_family(c['source']) for c in claims}):
        reduced = make_graph([c for c in claims if source_family(c['source']) != family],people)
        results['source_family_ablation'][family] = metrics(reduced,roots)
    # Removing one claim may leave another claim supporting the same graph edge.
    results['individual_claim_ablation'] = []
    candidates = [c for c in claims if c['subject'] in roots or c['object'] in roots or c['id']=='RFX008']
    for c in candidates:
        reduced=make_graph([d for d in claims if d['id']!=c['id']],people)
        d=nx.multi_source_dijkstra_path_length(reduced,roots,weight=None)
        lost=[n for n in base_dist if 0<base_dist[n]<=3 and d.get(n,999)>3]
        results['individual_claim_ablation'].append(dict(claim_id=c['id'],
            baseline_three_hop_records_lost=len(lost),
            unreachable_count=len(set(base_dist)-set(d))))
    results['individual_claim_ablation'].sort(key=lambda x:(-x['baseline_three_hop_records_lost'],x['claim_id']))

    # Cross-text support uses source-family grouping to avoid counting editions
    # of one work as independent traditions. No claim of independent testimony.
    pair_claims = defaultdict(list)
    for c in claims: pair_claims[tuple(sorted((c['subject'], c['object'])))].append(c)
    cross = []
    for pair, cc in pair_claims.items():
        families = sorted({source_family(c['source']) for c in cc})
        if len(families) < 2: continue
        cross.append(dict(nodes=list(pair), labels=[label(n) for n in pair],
            families=families, family_count=len(families),
            predicates=sorted({c['predicate'] for c in cc}), claim_ids=[c['id'] for c in cc]))
    results['cross_source_pairs'] = sorted(cross, key=lambda x: (-x['family_count'], x['nodes']))

    # Parent -> child normalization only for a small explicit predicate set.
    parent = nx.DiGraph(); spouse = nx.Graph(); teaching = nx.DiGraph(); killing = nx.DiGraph()
    normalized = defaultdict(list)
    for c in claims:
        u, v, p = c['subject'], c['object'], c['predicate']
        if c['id'] in NORMALIZATION_EXCLUSIONS: continue
        kind = None
        if p in PARENT_REVERSE: u, v = v, u; kind = 'parent'
        elif p in PARENT_FORWARD: kind = 'parent'
        elif p in SPOUSE: kind = 'spouse'
        elif p in TEACH_REVERSE: u, v = v, u; kind = 'teaching'
        elif p in TEACH_FORWARD: kind = 'teaching'
        elif p in KILL_REVERSE: u, v = v, u; kind = 'killing'
        elif p in KILL_FORWARD: kind = 'killing'
        if kind:
            target = {'parent': parent, 'spouse': spouse, 'teaching': teaching, 'killing': killing}[kind]
            target.add_edge(u, v)
            normalized[kind, u, v].append(c['id'])
    motifs = {}
    # Multiple named parents are not contradictions (e.g. divine, adoptive,
    # biological, or source-local variants); this is an inspection queue.
    motifs['multiple_parent_records'] = [dict(id=n, label=label(n),
        parents=[dict(id=p, label=label(p), claim_ids=normalized['parent', p, n])
                 for p in sorted(parent.predecessors(n))])
        for n in sorted(parent) if parent.in_degree(n) >= 3]
    motifs['parent_cycles'] = [dict(nodes=sorted(c), labels=[label(n) for n in sorted(c)])
         for c in nx.strongly_connected_components(parent) if len(c) > 1]
    motifs['teaching_chains'] = [dict(nodes=[a,b,c], labels=[label(n) for n in [a,b,c]],
         claim_ids=normalized['teaching',a,b] + normalized['teaching',b,c])
         for b in sorted(teaching) for a in sorted(teaching.predecessors(b))
         for c in sorted(teaching.successors(b)) if a != c]
    motifs['parent_spouse_triangles'] = [dict(parents=[a,b], child=c,
         labels=[label(a),label(b),label(c)], claim_ids=normalized['parent',a,c] +
         normalized['parent',b,c] + normalized.get(('spouse',a,b),[]) + normalized.get(('spouse',b,a),[]))
         for c in sorted(parent) for a,b in combinations(sorted(parent.predecessors(c)),2)
         if spouse.has_edge(a,b)]
    kin = parent.to_undirected()
    kin.add_edges_from(spouse.edges())
    motifs['killing_within_two_family_steps'] = []
    for a,b in sorted(killing.edges()):
        if a not in kin or b not in kin: continue
        paths = list(nx.all_simple_paths(kin,a,b,cutoff=2))
        if paths:
            motifs['killing_within_two_family_steps'].append(dict(nodes=[a,b],
               labels=[label(a),label(b)], family_paths=paths,
               claim_ids=normalized['killing',a,b]))
    # Two-edge narration motifs retain the narrator, which generic paths erase.
    motifs['narrator_intermediaries'] = []
    for c in claims:
        if c['predicate'] != 'asks_about': continue
        about = c['object']
        for d in claims:
            if d['object'] == about and d['predicate'] in {'narrates_deeds_of','recounts_deeds_of'}:
                motifs['narrator_intermediaries'].append(dict(labels=[label(c['subject']),label(d['subject']),label(about)],
                    claim_ids=[c['id'],d['id']], note='Common subject of narration; not proof these records describe the same exchange.'))
    results['motifs'] = motifs
    results['semantic_audit'] = {'excluded_from_typed_motifs':NORMALIZATION_EXCLUSIONS,
         'teaching_non_edges': [c['id'] for c in claims if c['predicate'] in
              {'appointed_as_teacher','sought_instruction_from'}],
         'note':'Appointing a teacher and requesting instruction do not establish a teacher-student edge.'}
    signatures=defaultdict(list)
    for (kind,u,v),ids in normalized.items():
        if kind=='spouse':u,v=sorted((u,v))
        signatures[kind,u,v].extend(ids)
    recurring=[]
    for (kind,u,v),ids in signatures.items():
        families=sorted({source_family(by_id[i]['source']) for i in ids})
        if len(families)>1:
            recurring.append(dict(relation=kind,nodes=[u,v],labels=[label(u),label(v)],
                families=families,claim_ids=ids))
    results['normalized_cross_source_relations']=sorted(recurring,key=lambda x:(-len(x['families']),x['nodes']))

    # Identity stress tests are intentionally unsafe upper-bound scenarios,
    # never proposed entity resolutions and never written back to graph.json.
    identity = []
    base_groups = defaultdict(list)
    for n in sorted(people):
        base_groups[label(n).split(' · ')[0].strip()].append(n)
    collisions = {k:v for k,v in base_groups.items() if len(v)>1}
    for name, mapping in [
        ('merge_agastya_facets', {n: ('AGASTYA_HYPOTHETICAL' if n in roots else n) for n in people}),
        ('merge_exact_base_labels_UNSAFE', {n: label(n).split(' · ')[0].strip() for n in people})]:
        merged = nx.Graph()
        merged.add_nodes_from(mapping.values())
        merged.add_edges_from((mapping[u],mapping[v]) for u,v in g.edges() if mapping[u]!=mapping[v])
        mr = {mapping[n] for n in roots}
        d = nx.multi_source_dijkstra_path_length(merged,mr,weight=None)
        # Compare reachability in ORIGINAL records, not collapsed node counts.
        projected = {n:d[mapping[n]] for n in people if mapping[n] in d}
        shortcuts = sorted(n for n in projected if n in base_dist and projected[n]<base_dist[n])
        newly_reached = sorted(set(projected)-set(base_dist))
        identity.append(dict(scenario=name, collapsed_nodes=len(people)-len(merged),
            original_records_with_shorter_distance=len(shortcuts), shortcut_examples=[
              dict(id=n,label=label(n),before=base_dist[n],after=projected[n]) for n in shortcuts[:30]],
            newly_reached_original_records=len(newly_reached),
            newly_reached_examples=[dict(id=n,label=label(n)) for n in newly_reached[:15]],
            original_records_within_three=sum(projected.get(n,999)<=3 for n in people-set(roots))))
    results['identity_sensitivity'] = {'scenarios':identity,'base_label_collision_groups':collisions}

    # Shortest-path semantics: exact counts of whether a <=3-hop path EXISTS
    # after removing a class. Avoid mistaking one arbitrary BFS path for all paths.
    path_sensitivity = {}
    for name in ['no_attendance','no_kinship','no_attendance_or_kinship','no_narration','checked_only']:
        d = nx.multi_source_dijkstra_path_length(graphs[name],roots,weight=None)
        lost = sorted(n for n in base_dist if 0<base_dist[n]<=3 and d.get(n,999)>3)
        path_sensitivity[name] = {'baseline_three_hop_records_lost':len(lost),
            'examples':[dict(id=n,label=label(n)) for n in lost[:20]]}
    results['path_sensitivity'] = path_sensitivity
    results['predicate_classification'] = {p:edge_class(p) for p in sorted({c['predicate'] for c in claims})}
    results['source_family_mapping'] = {s:source_family(s) for s in sorted(sources)}
    # Louvain optimization is stochastic. Record variation rather than treating
    # one partition or its number of communities as a cultural ground truth.
    stability = {}
    for name in ['baseline','no_attendance_or_kinship']:
        gg=graphs[name]; active=gg.subgraph([n for n,d in gg.degree() if d]).copy()
        partitions=[]; runs=[]
        for seed in [7,19,42]:
            partition=nx.community.louvain_communities(active,seed=seed,weight=None)
            partitions.append(partition)
            runs.append(dict(seed=seed,communities=len(partition),
                             modularity=nx.community.modularity(active,partition,weight=None)))
        stability[name]={'runs':runs,'pairwise_adjusted_rand':[
            dict(seeds=[a,b],score=adjusted_rand(partitions[i],partitions[j]))
            for (i,a),(j,b) in combinations(list(enumerate([7,19,42])),2)]}
    results['community_stability']=stability
    results['claim_evidence'] = {c['id']:dict(c,subject_label=label(c['subject']),
         object_label=label(c['object']),source_title=sources[c['source']]['title'],
         source_url=sources[c['source']]['url']) for c in claims}
    (OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    write_csv('source_ablation.csv',[{k:v for k,v in r.items() if k not in {'unreachable','pushed_beyond_three'}} for r in results['source_ablation']])
    write_csv('predicate_classes.csv',[dict(predicate=p,classification=edge_class(p),count=n)
         for p,n in Counter(c['predicate'] for c in claims).most_common()])
    write_summary(results)
    plot_results(results)
    print('Wrote',OUT,flush=True)


def plot_results(r):
    os.environ.setdefault('MPLCONFIGDIR','/private/tmp/agastya-matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    names = list(r['variants'])[:6]
    pretty = ['All claims','Passage checked','No attendance','No kinship / predictions',
              'No attendance or kinship','No narrative references']
    fig, axes = plt.subplots(1,2,figsize=(14,5.4),layout='constrained')
    fig.suptitle('What makes Agastya’s textual network look connected?',fontsize=17,fontweight='bold')
    for ax,key,title in zip(axes,['within_three_hops','largest_component'],
                           ['Records within three links of any Agastya facet','Size of largest connected component']):
        vals=[r['variants'][n][key] for n in names]
        bars=ax.barh(pretty[::-1],vals[::-1],color=['#55a6a0']*5+['#264653'])
        ax.bar_label(bars,padding=4)
        ax.set_xlim(0,max(vals)*1.19); ax.set_title(title,fontsize=11,pad=12)
        ax.spines[['top','right','bottom']].set_visible(False)
        ax.tick_params(axis='x',bottom=False,labelbottom=False)
    fig.supxlabel('Same node universe in every experiment. Links are textual claims; distance does not imply a meeting or shared lifetime.',fontsize=9)
    fig.savefig(OUT/'connectivity.png',dpi=180,facecolor='white'); plt.close(fig)
    fig,ax=plt.subplots(figsize=(12,6.5),layout='constrained')
    fig.patch.set_facecolor('#fbfaf6'); ax.set_facecolor('#fbfaf6')
    positions={'Jambavant':(0,0),'Rama':(-2,1.05),'Indra':(2,1.05),'Krishna':(0,-1.45)}
    for target,relation,citation,color in [
        ('Rama','commands allied troops for','Ramayana 6.27.10–14','#387d7a'),
        ('Indra','aided in battle','Ramayana 6.27.12','#387d7a'),
        ('Krishna','fought with','Vishnu Purana 4.13.16–20','#86654a')]:
        x,y=positions[target]
        ax.annotate('',xy=(x*.83,y*.83),xytext=(x*.18,y*.18),
                    arrowprops=dict(arrowstyle='->',lw=2,color=color))
        tx,ty=x*.59,y*.59
        if target=='Krishna':tx+=1.15
        else:ty+=.27
        ax.text(tx,ty,relation+'\n'+citation,ha='center',va='center',fontsize=10,
                color=color,bbox=dict(facecolor='#fbfaf6',edgecolor='none',pad=4))
    for name,(x,y) in positions.items():
        ax.text(x,y,name,ha='center',va='center',fontsize=15,fontweight='bold',
                color='white' if name=='Jambavant' else '#273c43',
                bbox=dict(boxstyle='round,pad=0.8',facecolor='#273c43' if name=='Jambavant' else '#e6ece8',edgecolor='none'))
    ax.set_xlim(-3.2,3.2);ax.set_ylim(-2.1,1.9);ax.axis('off')
    fig.suptitle('Jambavant: few connections, an unusually strong bridge',fontsize=18,fontweight='bold')
    fig.supxlabel('Three remaining neighbors after attendance and broad kinship/prediction links are removed.\nThe dataset reuses one Jambavant record across these texts; this is a textual network, not evidence of a historical lifespan.',fontsize=9)
    fig.savefig(OUT/'jambavant-bridge.png',dpi=180,facecolor=fig.get_facecolor());plt.close(fig)


def adjusted_rand(a,b):
    """Adjusted Rand index from partition contingency counts, no sklearn needed."""
    aa={n:i for i,c in enumerate(a) for n in c}; bb={n:i for i,c in enumerate(b) for n in c}
    assert aa.keys()==bb.keys()
    choose2=lambda n:n*(n-1)/2
    cells=Counter((aa[n],bb[n]) for n in aa)
    observed=sum(choose2(v) for v in cells.values())
    left=sum(choose2(len(c)) for c in a); right=sum(choose2(len(c)) for c in b)
    total=choose2(len(aa))
    if not total:return 1.0
    expected=left*right/total; upper=(left+right)/2
    return (observed-expected)/(upper-expected) if upper!=expected else 1.0


def write_summary(r):
    lines=['# Computed experiment results','',
           f'Input SHA-256: `{r["input_sha256"]}`. Seed 42 unless stated otherwise.','',
           'Textual entities include deities and collectives. All structural edges are undirected; claims retain their directions in the evidence export.','',
           '| Variant | Edges | Active records | Largest component | Within 3 links of any Agastya facet |',
           '|---|---:|---:|---:|---:|']
    for name,m in r['variants'].items():
        lines.append(f'| {name} | {m["edges"]} | {m["active_nodes"]} | {m["largest_component"]} | {m["within_three_hops"]} |')
    lines+=['','## Bridge candidates by exact betweenness','',
            'Scores use the same original record universe for normalization. Compare ranks and structure as well as scores; ablation changes component sizes.','']
    for name in ['baseline','checked_only','no_attendance','no_attendance_or_kinship']:
        lines += [f'### {name}','','| Record | Degree | Betweenness |','|---|---:|---:|']
        for n in r['centrality'][name][:10]:
            lines.append(f'| {n["label"]} | {n["degree"]} | {n["betweenness"]:.6f} |')
        lines.append('')
    lines+=['## Claim-removal sensitivity','',
            'Number of baseline records within three links that move beyond three links or become unreachable when this single claim is removed. Parallel support can preserve an edge.','',
            '| Claim | Description | Records lost from 3-link neighborhood |','|---|---|---:|']
    for row in r['individual_claim_ablation'][:12]:
        c=r['claim_evidence'][row['claim_id']]
        lines.append(f'| {c["id"]} | {c["subject_label"]} → {c["predicate"]} → {c["object_label"]} | {row["baseline_three_hop_records_lost"]} |')
    lines+=['','## Recurring typed relations across source families','',
            'Families group editions of the same work; recurrence is not independent historical corroboration.','']
    for x in r['normalized_cross_source_relations']:
        lines.append(f'- {x["labels"][0]} → {x["relation"]} → {x["labels"][1]}: {", ".join(x["families"])}. Claims: {", ".join(x["claim_ids"])}.')
    lines+=['','## Motifs and audit queues','']
    for k,v in r['motifs'].items():lines.append(f'- {k}: {len(v)}')
    lines+=['','No parent cycles were found with the explicit parent predicate set; this is not a validation of every genealogical claim.','',
            '## Community stability','']
    for name, s in r['community_stability'].items():
        lines.append(f'- {name}: runs {s["runs"]}; adjusted Rand comparisons {s["pairwise_adjusted_rand"]}.')
    lines+=['','## Identity sensitivity','']
    for x in r['identity_sensitivity']['scenarios']:
        lines.append(f'- {x["scenario"]}: {x["collapsed_nodes"]} records collapsed; {x["original_records_with_shorter_distance"]} previously reachable records get shorter paths; {x["newly_reached_original_records"]} previously unreachable records become reachable; {x["original_records_within_three"]} original non-root records are within three links.')
    lines+=['','The base-label merge is an intentionally unsafe stress test. It is not an identity proposal and must not be used as a historical result.','',
            '## Semantic exclusions','']
    for k,v in NORMALIZATION_EXCLUSIONS.items():lines.append(f'- {k}: {v}')
    (OUT/'RESULTS.md').write_text('\n'.join(lines)+'\n')


if __name__ == '__main__':
    main()
