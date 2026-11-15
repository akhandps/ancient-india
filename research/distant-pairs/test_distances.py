import hashlib
import json
import sys
import unittest
from collections import defaultdict
from pathlib import Path

import networkx as nx

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analyze_distant_pairs import extremes,load_baseline,project


class DistanceTests(unittest.TestCase):
    def test_exact_extremes_on_known_path(self):
        g=nx.path_graph(5)
        r=extremes(g,defaultdict(set))
        self.assertEqual(r['maximum_finite_distance'],4)
        self.assertEqual(r['farthest_pairs'],[[0,4]])
        self.assertEqual(r['unreachable_unordered_pairs'],0)

    def test_disconnected_pairs_are_not_finite_distances(self):
        g=nx.Graph([(0,1),(1,2),(3,4)])
        r=extremes(g,defaultdict(set))
        self.assertEqual(r['maximum_finite_distance'],2)
        self.assertEqual(r['components'],2)
        self.assertEqual(r['unreachable_unordered_pairs'],6)

    def test_saved_paths_and_canonical_graph(self):
        raw,before=load_baseline()
        addition=json.loads((ROOT/'research/agastya/expansion/distance_bridges.json').read_text())
        results=json.loads((ROOT/'research/distant-pairs/results.json').read_text())
        self.assertEqual(results['baseline_sha256'],hashlib.sha256(raw).hexdigest())
        expected=project(before,before['claims']+addition['claims'])
        canonical=json.loads((ROOT/'research/agastya/graph.json').read_text())
        by_id={c['id']:c for c in canonical['claims']}
        for claim in before['claims']:
            self.assertEqual(by_id[claim['id']],claim)
        actual=project(canonical,canonical['claims'])
        self.assertEqual(set(map(frozenset,expected.edges())),set(map(frozenset,actual.edges())))
        for row in results['scenarios'].values():
            for p in row['selected_pairs']:
                if p['distance'] is None:
                    self.assertEqual(p['steps'],[])
                    continue
                self.assertEqual(len(p['steps']),p['distance'])
                for a,b in zip(p['steps'],p['steps'][1:]):self.assertEqual(a['to_id'],b['from_id'])
        for p in results['scenarios']['combined_no_nanda_comparison']['selected_pairs']:
            used={e['id'] for step in p['steps'] for e in step['evidence']}
            self.assertFalse(used.intersection({'FD002','FD004'}))


if __name__=='__main__':unittest.main()
