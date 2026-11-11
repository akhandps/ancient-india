"""Audit up-to-three-step person paths from source-local Agastya nodes."""
import json
from collections import deque, defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'research' / 'agastya'
graph = json.loads((OUT / 'graph.json').read_text())
nodes = {n['id']: n for n in graph['nodes']}
sources = {s['id']: s for s in graph['sources']}
claim_by_id = {c['id']: c for c in graph['claims']}
person_types = {'person', 'deity', 'deity_collective', 'celestial', 'asura', 'commentator', 'poet', 'bodhisattva', 'people_collective', 'person_collective', 'person_or_entity', 'person_or_king', 'person_or_prince', 'agastya_facet'}
roots = [n['id'] for n in graph['nodes'] if n['type'] == 'agastya_facet']
adj = defaultdict(list)
for c in graph['claims']:
    if c['status'] == 'identity_hypothesis' or nodes[c['subject']]['type'] not in person_types or nodes[c['object']]['type'] not in person_types:
        continue
    adj[c['subject']].append((c['object'], c['id']))
    adj[c['object']].append((c['subject'], c['id']))

distance = {id: 0 for id in roots}
parent = {}
queue = deque(roots)
while queue:
    u = queue.popleft()
    for v, claim_id in adj[u]:
        if v not in distance:
            distance[v] = distance[u] + 1
            parent[v] = (u, claim_id)
            queue.append(v)

paths = []
for id, depth in sorted(distance.items(), key=lambda x: (x[1], nodes[x[0]]['label'])):
    if not 1 <= depth <= 3:
        continue
    steps = []
    v = id
    while v in parent:
        u, claim_id = parent[v]
        c = claim_by_id[claim_id]
        steps.append({'from': u, 'to': v, 'claim_id': claim_id, 'predicate': c['predicate'], 'source': c['source'], 'locator': c['locator'], 'status': c['status'], 'summary': c['summary'], 'note': c.get('note', '')})
        v = u
    steps.reverse()
    paths.append({'id': id, 'label': nodes[id]['label'], 'hops': depth, 'steps': steps})

(OUT / 'three-hop-paths.json').write_text(json.dumps({'method': 'Shortest paths through person-like nodes and sourced claim endpoints. Source nodes, place nodes and text nodes do not count as person links. Direction is ignored for reachability, not for interpretation. Identity hypotheses excluded. A path does not establish meetings, contemporaneity or a single historical Agastya.', 'roots': roots, 'paths': paths}, ensure_ascii=False, indent=2) + '\n')

lines = ['# Person paths from Agastya witnesses', '', 'This is a shortest-path audit over sourced person-to-person claim edges. All six source-local Agastya facets start at distance zero. Text witnesses, places, and citations remain visible in the 3D graph but are not counted as person hops. Direction is ignored only when finding a path. A path does not show that its people met or lived at the same time.', '']
for depth in (3, 2):
    group = [p for p in paths if p['hops'] == depth]
    lines += [f'## {depth} hops · {len(group)} people', '']
    for p in group:
        names = [nodes[p['steps'][0]['from']]['label']] + [nodes[step['to']]['label'] for step in p['steps']]
        lines += [f'### {p["label"]}', '', ' → '.join(names), '']
        for step in p['steps']:
            c = claim_by_id[step['claim_id']]
            s = sources[c['source']]
            direction = f'{nodes[c["subject"]]["label"]} → {c["predicate"].replace("_", " ")} → {nodes[c["object"]]["label"]}'
            lines.append(f'- {step["claim_id"]}: {direction}. [{s["title"]}, {c["locator"]}]({s["url"]}). {c["status"]}. {c["summary"]}' + (f' {c["note"]}' if c.get('note') else ''))
        lines.append('')

lines += ['## Method and limits', '', '- `translation_checked` concerns a passage in translation, not historicity.', '- `editorial_attribution` includes assigned hymn speakers and related interpretive links.', '- Co-mention or an attributed poetic lineage is weaker than a narrated encounter; read every step of a path.', '- The path list is limited by the presently reviewed corpus and should grow with more editions and texts.', '']
(OUT / 'three-hop-paths.md').write_text('\n'.join(lines))
print(f'{len([p for p in paths if p["hops"] == 3])} people at exactly three person links')
