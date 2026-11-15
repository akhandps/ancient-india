"""Compare source-local and explicitly aligned Jambavant supplement scenarios."""
import copy
import hashlib
import json
import os
from pathlib import Path

import networkx as nx
from analyze_agastya import PERSON_TYPES, edge_class, make_graph

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'research/jambavant'
FOCAL='vp4_13_jambavant'
LOCAL=['jv_ram','jv_sb8','jv_sb10',FOCAL]


def relation_class(c):
    if c['id'] in {'JV001','JV010'}: return 'kinship'
    if c['predicate'] in {'narrates_birth_and_praises_capacity_of','asks_about_survival_of',
                         'attributes_prior_lanka_campaign_to'}:return 'narration_or_reference'
    if c['predicate'].startswith('predict_'):return 'prediction'
    return edge_class(c['predicate'])


def rewrite(claims,mapping):
    return [dict(c,subject=mapping.get(c['subject'],c['subject']),
                   object=mapping.get(c['object'],c['object'])) for c in claims]


def main():
    raw=(ROOT/'research/agastya/analysis/input-graph.json').read_bytes()
    supplement_raw=(OUT/'records.json').read_bytes()
    base=json.loads(raw); supplement=json.loads(supplement_raw)
    nodes={n['id']:n for n in base['nodes']+supplement['nodes']}
    assert len(nodes)==len(base['nodes'])+len(supplement['nodes'])
    people={i for i,n in nodes.items() if n['type'] in PERSON_TYPES}
    all_claims=base['claims']+supplement['claims']
    for c in supplement['claims']:
        assert c['subject'] in nodes and c['object'] in nodes,c['id']
    roots=sorted(i for i,n in nodes.items() if n['type']=='agastya_facet')
    original=copy.deepcopy(base['claims'])
    split=copy.deepcopy(original)
    # Reverse only the existing, inspectable canonical Ramayana->VP identity
    # rewrite. Other cross-text identities stay unchanged in every scenario.
    for c in split:
        if c['source']=='ram6_yuddha_27':
            for endpoint in ['subject','object']:
                if c[endpoint]==FOCAL:c[endpoint]='jv_ram'
    enriched=split+supplement['claims']
    jmap=supplement['scenario_alignments']['jambavant_only']
    fullmap=dict(jmap,**supplement['scenario_alignments']['additional_named_figures'])
    scenarios={'original':original,'existing_jambavant_split':split,
               'enriched_source_local':enriched,
               'enriched_align_jambavant':rewrite(enriched,jmap),
               'enriched_align_named_figures':rewrite(enriched,fullmap)}
    output={'baseline_sha256':hashlib.sha256(raw).hexdigest(),
            'supplement_sha256':hashlib.sha256(supplement_raw).hexdigest(),
            'networkx':nx.__version__,
            'method':'Exact unweighted undirected betweenness on fixed union of person-like records, including isolates. Local or aligned records are graph entities, not distinct historical people.',
            'alignment_maps':supplement['scenario_alignments'],
            'supplement_counts':{'nodes':len(supplement['nodes']),'claims':len(supplement['claims']),
                                 'observations':len(supplement['observations']),'sources':len(supplement['sources'])},
            'scenarios':{}}
    for name,cc in scenarios.items():
        eligible=[c for c in cc if c['subject'] in people and c['object'] in people and c['status']!='identity_hypothesis']
        rows={}
        for view in ['all','no_attendance','no_attendance_or_kinship']:
            excluded= {'attendance'} if view=='no_attendance' else {'attendance','kinship','prediction'} if view=='no_attendance_or_kinship' else set()
            keep=[c for c in eligible if relation_class(c) not in excluded]
            g=make_graph(keep,people)
            bc=nx.betweenness_centrality(g,normalized=True,weight=None)
            ordered=sorted(g,key=lambda n:(-bc[n],n)); ranks={n:i+1 for i,n in enumerate(ordered)}
            distance=nx.multi_source_dijkstra_path_length(g,roots,weight=None)
            rows[view]={'nodes':len(g),'edges':g.number_of_edges(),
                'focal':{n:{'label':nodes[n]['label'],'degree':g.degree(n),
                     'betweenness':bc[n], 'rank':ranks[n] if bc[n]>0 else None,
                     'distance_from_any_agastya':distance.get(n),
                     'neighbors':[{'id':v,'label':nodes[v]['label'],
                       'claim_ids':g[n][v]['claim_ids']} for v in sorted(g[n])]}
                     for n in LOCAL}}
        output['scenarios'][name]=rows
        print(name,{view:(v['focal'][FOCAL]['rank'],v['focal'][FOCAL]['degree']) for view,v in rows.items()},flush=True)
    (OUT/'analysis.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    lines=['# Jāmbavant identity and enrichment experiment','',
       'Ranks use exact betweenness on a fixed union node universe. All other identity choices are held fixed.','',
       '| Scenario | VP/aligned record rank, all edges | Without attendance: rank / degree | Without attendance and broad kinship: rank / degree |',
       '|---|---:|---:|---:|']
    for name,views in output['scenarios'].items():
        focal=[views[v]['focal'][FOCAL] for v in ['all','no_attendance','no_attendance_or_kinship']]
        lines.append(f'| {name} | {focal[0]["rank"]} | {focal[1]["rank"]} / {focal[1]["degree"]} | {focal[2]["rank"]} / {focal[2]["degree"]} |')
    lines+=['','The first two enriched scenarios keep Kṛṣṇa and other new Bhāgavata figures source-local. The last scenario additionally aligns the explicitly listed named figures. Changes are conditional on those mappings and targeted corpus enrichment, not independent confirmation.','',
       'See `analysis.json` for all four focal dossiers, neighbor claim IDs, scores, and input hashes. No merged graph is written over the original dataset.']
    (OUT/'RESULTS.md').write_text('\n'.join(lines)+'\n')
    plot_durations(supplement)


def plot_durations(supplement):
    os.environ.setdefault('MPLCONFIGDIR','/private/tmp/agastya-matplotlib')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.8),layout='constrained')
    fig.suptitle('Same jewel episode. Different narrated durations.',fontsize=18,fontweight='bold')
    labels=['Vishnu Purana','Bhagavata Purana'];colors=['#387d7a','#86654a']
    for ax,vals,title,locators in [
        (axes[0],[21,28],'Fight duration (days)',['4.13.17','10.56.24']),
        (axes[1],[7.5,12],'Companions wait outside the cave (days)',['4.13.17–18','10.56.33'])]:
        ax.bar(labels,vals,color=colors,width=.55)
        for i,(v,loc) in enumerate(zip(vals,locators)):
            value='7 or 8' if ax is axes[1] and i==0 else str(int(v))
            ax.text(i,v+.5,value,ha='center',fontweight='bold',fontsize=14)
            ax.text(i,1,loc,ha='center',color='white',fontsize=10)
        ax.set_title(title,fontsize=11,pad=12)
        ax.set_ylim(0,max(vals)*1.22);ax.spines[['top','right']].set_visible(False)
        ax.set_ylabel('Narrated days')
    fig.supxlabel('Translation-level comparison; preserve separate witnesses. These are story durations, not calendar anchors.\nThe “7 or 8” bar is positioned at 7.5 only for display; the source alternatives remain separate in the data.',fontsize=9)
    fig.savefig(OUT/'duration-variants.png',dpi=180,facecolor='white');plt.close(fig)


if __name__=='__main__':main()
