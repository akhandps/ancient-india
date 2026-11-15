"""Reproducible ancestry ordering and mixed-relation cycle audit."""
import csv
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path

import networkx as nx

from analyze_agastya import (CHECKED, NORMALIZATION_EXCLUSIONS, PERSON_TYPES,
                             PARENT_FORWARD, PARENT_REVERSE)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'research/topology'
INPUT_REF = '1c5958bc213fece401e86af5c82a560a4996c4d4'


def main():
    OUT.mkdir(exist_ok=True)
    raw = subprocess.check_output(['git', 'show', f'{INPUT_REF}:research/agastya/graph.json'], cwd=ROOT)
    data = json.loads(raw)
    nodes = {n['id']: n for n in data['nodes']}
    people = {n for n in nodes if nodes[n]['type'] in PERSON_TYPES}
    claims = [c for c in data['claims'] if c['subject'] in people and c['object'] in people
              and c['status'] != 'identity_hypothesis']
    mixed = nx.DiGraph()
    ancestry = nx.DiGraph()
    evidence = defaultdict(list)
    for c in claims:
        u, v = c['subject'], c['object']
        mixed.add_edge(u, v)
        if c['status'] not in CHECKED or c['id'] in NORMALIZATION_EXCLUSIONS:
            continue
        if c['predicate'] in PARENT_REVERSE:
            u, v = v, u
        elif c['predicate'] not in PARENT_FORWARD:
            continue
        ancestry.add_edge(u, v)
        evidence[u, v].append(c['id'])

    assert nx.is_directed_acyclic_graph(ancestry)
    layers = [sorted(g) for g in nx.topological_generations(ancestry)]
    layer_of = {n: i for i, layer in enumerate(layers) for n in layer}
    order = [n for layer in layers for n in layer]
    position = {n: i for i, n in enumerate(order)}
    assert len(position) == len(ancestry)
    assert all(layer_of[u] < layer_of[v] and position[u] < position[v] for u, v in ancestry.edges())
    longest = nx.dag_longest_path(ancestry, topo_order=order)
    assert len(longest) == len(layers)

    components = sorted((sorted(s) for s in nx.strongly_connected_components(mixed)), key=lambda s: s[0])
    condensed = nx.condensation(mixed, components)
    component_layers = [sorted(g) for g in nx.topological_generations(condensed)]
    clayer = {n: i for i, layer in enumerate(component_layers) for n in layer}
    assert nx.is_directed_acyclic_graph(condensed)
    assert all(clayer[u] < clayer[v] for u, v in condensed.edges())
    cyclic = [s for s in components if len(s) > 1 or mixed.has_edge(s[0], s[0])]
    cycles = []
    for s in sorted(cyclic, key=lambda s: (-len(s), s)):
        example = nx.find_cycle(mixed.subgraph(s), source=s[0])
        steps = [dict(from_id=u, to_id=v,
                      claims=[c for c in claims if c['subject'] == u and c['object'] == v])
                 for u, v in example]
        cycles.append(dict(size=len(s), members=s, labels=[nodes[n]['label'] for n in s],
                           example_cycle=steps))

    result = dict(input_commit=INPUT_REF, input_sha256=hashlib.sha256(raw).hexdigest(), networkx=nx.__version__,
                  parent_forward=sorted(PARENT_FORWARD), parent_reverse=sorted(PARENT_REVERSE),
                  normalization_exclusions=NORMALIZATION_EXCLUSIONS,
                  mixed=dict(active_records=len(mixed), edges=mixed.number_of_edges(),
                             is_dag=nx.is_directed_acyclic_graph(mixed), cyclic_components=cycles,
                             condensed_components=len(condensed), condensed_layers=component_layers,
                             components=components, condensed_edges=sorted(condensed.edges())),
                  ancestry=dict(active_records=len(ancestry), edges=ancestry.number_of_edges(),
                                is_dag=True, layers=layers, order=order,
                                longest_path=[dict(id=n, label=nodes[n]['label']) for n in longest],
                                longest_path_steps=[dict(parent=u, child=v, claim_ids=evidence[u, v])
                                                    for u, v in zip(longest, longest[1:])]))
    (OUT / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with (OUT / 'ancestry-order.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['position', 'layer', 'id', 'label', 'parents_in_projection'])
        writer.writerows((position[n], layer_of[n], n, nodes[n]['label'],
                          ';'.join(sorted(ancestry.predecessors(n)))) for n in order)
    print(f'Ancestry: {len(ancestry)} records, {ancestry.number_of_edges()} edges, {len(layers)} layers; '
          f'mixed: {len(cyclic)} cyclic components, largest {max(map(len, cyclic), default=0)}.')


if __name__ == '__main__':
    main()
