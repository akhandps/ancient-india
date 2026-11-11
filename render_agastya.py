"""Render the curated graph as an inline fragment and a readable research file."""
import json
from pathlib import Path

root=Path(__file__).resolve().parent
out=root/'research'/'agastya'
data=json.loads((out/'graph.json').read_text())
progress=json.loads((out/'progress.json').read_text())
index_review=json.loads((out/'expansion'/'inm-review.json').read_text())
template=(root/'agastya-graph.template.html').read_text()
# The inline view follows Agastya out to three person links. The standalone
# force graphs and graph.json retain every sourced claim in the wider graph.
hop_paths = json.loads((out/'three-hop-paths.json').read_text())
near_ids = set(hop_paths['roots'])
for path in hop_paths['paths']:
    near_ids.add(path['id'])
    for step in path['steps']:
        near_ids.update((step['from'], step['to']))
view_claims = [c for c in data['claims'] if c['subject'] in hop_paths['roots'] or c['object'] in hop_paths['roots'] or (c['subject'] in near_ids and c['object'] in near_ids)]
view_node_ids = set(hop_paths['roots']) | {v for c in view_claims for v in (c['subject'], c['object'])}
view_source_ids = {c['source'] for c in view_claims} | {t['source'] for t in data['chronology']}
view_data = {
    'nodes': [{k: n[k] for k in ('id', 'label', 'type')} for n in data['nodes'] if n['id'] in view_node_ids],
    'sources': [{k: s[k] for k in ('id', 'title', 'url')} for s in data['sources'] if s['id'] in view_source_ids],
    'claims': [{k: c[k] for k in ('id', 'facet', 'subject', 'predicate', 'object', 'source', 'locator', 'summary', 'status') if k in c} for c in view_claims],
    'chronology': data['chronology'],
}
fragment=template.replace('__AGASTYA_DATA__',json.dumps(view_data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
visual=Path('/Users/akhand/.codex/visualizations/2026/10/27/01a17c4a-9f77-7af2-bb95-eea7843a9c7f/agastya-evidence.html')
visual.write_text(fragment)
(out/'graph-fragment.html').write_text(fragment)
nodes={n['id']:n for n in data['nodes']}
sources={s['id']:s for s in data['sources']}
facets=[n['id'] for n in data['nodes'] if n['type']=='agastya_facet']
lines=[f'# Agastya: evidence graph, version {data["schema_version"]}','',
f'Research snapshot: 27 October 2026. {len(data["nodes"])} nodes, {len(data["claims"])} claims, {len(data["sources"])} sources, {len(data["chronology"])} chronological records.','',
data['scope'],'',data['identity_policy'],'',
'## Coverage and identity review','',
f'{progress["passage_checked_named_records"]} named records have a checked textual passage; {progress["needs_primary_passage_review"]} more named records need primary passage review. The 3,000-record milestone is exceeded by {max(0, progress["passage_checked_named_records"] - progress["target"])} at the present review level. These are source-local textual entities, not a count of distinct historical people.','',
f'The Mahābhārata index contributes {progress["separate_index_headword_candidates"]} likely individual *candidate records* to a separate review queue; zero are counted before passage and identity review. Only {index_review["scale_check"]["distinct_slp1_spellings_in_candidate_stratum"]} exact spellings occur in this candidate stratum. See `progress.json`, `individuals.csv`, `expansion/inm-review.json`, and `expansion/INM-SOURCE.md`.','',
'## Reading the graph','',
'Arrows record passage-level claims, not established historical events. “Incoming” distinguishes a person speaking about Agastya from speaking to him. “Outgoing” includes attributed speech and is labeled where speaker assignments depend on interpretation. Geography distinguishes Agastya’s own words from descriptions by other speakers. Deities and personified places retain their entity types.','',
'Most claims are checked against translations; selected Mahābhārata claims are checked against the electronic Sanskrit critical text. No systematic Sanskrit/Tamil philological audit or manuscript collation has been completed. Prose translation pages may interleave commentary: only translated narrative statements were used for primary claims.','',
'## Principal findings','',
'- Earliest textual horizon in this seed: the Ṛgveda; this dates attestations within a corpus, not Agastya’s lifespan.','- Ṛgveda 1.170.3 explicitly addresses Agastya. The Lopāmudrā dialogue requires editorial speaker assignments. Ṛgveda 7.33 places him in Vasiṣṭha birth imagery without identifying Vasiṣṭha as the speaker.','- Rāmāyaṇa 3.13 gives direct geographical speech about Pañcavaṭī and Godāvarī, and a claimed friendship with Daśaratha. Sugrīva’s Malaya statement is a different evidence type.','- Yudhiṣṭhira asks Lomaśa about Agastya; that exchange does not establish an Agastya–Yudhiṣṭhira meeting.','- Tamil commentary traditions connect Akattiyar with Tolkāppiyar and southern geography. Their primary passages remain to be audited. The Tolkāppiyam base text must not inherit its commentators’ claims automatically.','- Puṟanāṉūṟu 201 does not explicitly name Agastya. Mahadevan’s identification of its northern sage is retained as a hypothesis.','- No independently anchored birth/death interval for a historical Agastya is established by this dataset.','',
'## Chronology','',
'Calendar dates below belong to texts or witnesses unless explicitly marked otherwise. Narrative yugas and durations have not been converted into BCE dates. Alternative scholarly datings remain separate source-attributed claims.','',
'| Claim | Type | Period | Source / qualification |','|---|---|---|---|']
for t in data['chronology']:
 s=sources[t['source']]
 lines.append(f"| {t['label']} | {t['kind']} | {t['range']} | [{s['title']}]({s['url']}). {t['note']} |")
lines+=['','## Evidence claims','', 'Locators are edition-specific. Ganguli section numbers are not BORI chapter numbers. The Rāmāyaṇa locators follow the linked site; no critical-edition concordance is claimed.','']
for facet in facets:
 lines+=['### '+nodes[facet]['label'],'','| ID | Subject → predicate → object | Evidence | Review status / qualification |','|---|---|---|---|']
 for c in data['claims']:
  if c['facet']!=facet:continue
  s=sources[c['source']]
  desc=f"{nodes[c['subject']]['label']} → {c['predicate'].replace('_',' ')} → {nodes[c['object']]['label']}"
  lines.append(f"| {c['id']} | {desc} | [{c['locator']}]({s['url']}). {c['summary']} | {c['status']}. {c['note']} |")
 lines.append('')
lines+=['## Source register','']
for s in data['sources']:
 lines.append(f"- **{s['id']}**: [{s['title']}]({s['url']}); {s['kind']}. {s['edition']} {s['locator']}")
lines+=['','## Next research work','']+['- '+x for x in data['open_work']]
lines+=['','## Files','', '- `graph.json`: expanded nodes, source records, claims, and chronology.','- `seed-graph.json`: preserved initial curated graph.','- `people.md` and `people.json`: evidence dossiers for every person-like node.','- `progress.json`, `individuals.csv`, and `identity-review.csv`: counted dossiers, review levels, and same-name identity checks.','- `three-hop-paths.md` and `.json`: audited shortest paths through person-like claim endpoints.','- `force-graph-2d.html` and `force-graph-3d.html`: standalone Canvas force graphs with text witnesses, source links, and passage details.','- `force-graph-webgl.html`: alternate true 3D view using circular sprites and the locally vendored 3d-force-graph 1.80.1 bundle; `vendor/3d-force-graph-LICENSE.txt` contains its MIT license.','- `force-graph-three.html`: direct Three.js point-cloud view with circular sprites, bundled locally from `agastya-three-app.js`; `vendor/three-0.186.1-LICENSE.txt` contains its MIT license.','- `expansion/*.json`: reviewed research batches and review manifest.','- `claims.csv`: claims in a spreadsheet-compatible form.','- `chronology.csv`: narrative and textual chronology claims.','- `graph-fragment.html`: interactive view, intended for the Codex visualization runtime.','', 'Regenerate with `python3 merge_agastya_expansion.py`, then `python3 measure_agastya_progress.py`, `python3 render_agastya_people.py`, `python3 render_agastya_hops.py`, `python3 render_agastya.py`, and `python3 render_force_graph.py`. `build_agastya.py` regenerates the original seed.','']
lines += ['To rebuild the direct Three.js bundle after editing `agastya-three-app.js`, run `npm install` and `npm run build:three` from the project root. For the WebGL library view’s circular sprites, run `npm run build:webgl-sprites`, then regenerate the standalone pages with `python3 render_force_graph.py`.', '']
(out/'README.md').write_text('\n'.join(lines))
print(visual)
