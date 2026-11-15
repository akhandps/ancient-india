"""Audit every shortest path behind Jambavant's three MWIS conflicts."""
import json
import subprocess
from pathlib import Path

import networkx as nx

from analyze_agastya import PERSON_TYPES, make_graph

ROOT = Path(__file__).resolve().parent
INPUT_REF = 'd966449'


def main():
    data = json.loads(subprocess.check_output(
        ['git', 'show', f'{INPUT_REF}:research/agastya/graph.json'], cwd=ROOT))
    nodes = {n['id']: n for n in data['nodes']}
    sources = {s['id']: s for s in data['sources']}
    people = {n for n in nodes if nodes[n]['type'] in PERSON_TYPES}
    claims = [c for c in data['claims'] if c['subject'] in people
              and c['object'] in people and c['status'] != 'identity_hypothesis']
    graph = make_graph(claims, people)
    mwis = json.loads((ROOT / 'research/mwis/results.json').read_text())
    probe = next(p for p in mwis['models']['hubs_distance_2_budget_10']['forced_in_probes']
                 if p['id'] == 'vp4_13_jambavant')
    audits = []
    for target in probe['conflicts_with_selected']:
        paths = []
        for path in sorted(nx.all_shortest_paths(graph, probe['id'], target['id'])):
            assert len(path) <= 3
            steps = []
            for a, b in zip(path, path[1:]):
                evidence = [dict(c, source_record=sources[c['source']]) for c in claims
                            if {c['subject'], c['object']} == {a, b}]
                assert evidence
                steps.append(dict(from_id=a, to_id=b, evidence=evidence))
            paths.append(dict(ids=path, labels=[nodes[n]['label'] for n in path], steps=steps))
        audits.append(dict(target=target, distance=len(paths[0]['steps']), paths=paths))
    result = dict(input_commit=INPUT_REF,
                  scope='Original MWIS conflicts; directions, predicates and speakers retained in evidence. '
                        'Undirected paths do not establish shared events or meetings.',
                  audited_conflicts=audits)
    (ROOT / 'research/jambavant/mwis-path-audit.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Audited', len(audits), 'conflicts:', [(a['target']['label'], a['distance']) for a in audits])


if __name__ == '__main__':
    main()
