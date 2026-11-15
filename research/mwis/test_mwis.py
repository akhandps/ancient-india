import itertools
import json
import subprocess
import sys
import unittest
from pathlib import Path

import networkx as nx

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analyze_mwis import solve_mwis,conflict_graph,INPUT_REF
from analyze_agastya import PERSON_TYPES,make_graph


class MWISTests(unittest.TestCase):
    def test_solver_matches_exhaustive_weighted_search(self):
        for g,w in [(nx.cycle_graph(5),{i:i+1 for i in range(5)}),
                    (nx.star_graph(3),{0:10,1:4,2:4,3:4})]:
            best=0
            for bits in itertools.product([0,1],repeat=len(g)):
                chosen={n for n,b in zip(g,bits) if b}
                if all(not (a in chosen and b in chosen) for a,b in g.edges()):
                    best=max(best,sum(w[n] for n in chosen))
            answer=solve_mwis(g,w)
            self.assertTrue(answer['optimal'])
            self.assertEqual(answer['objective'],best)

    def test_shared_neighbor_outside_candidate_pool(self):
        g=nx.Graph([('a','outside'),('outside','b')])
        self.assertEqual(conflict_graph(g,['a','b'],1).number_of_edges(),0)
        stronger=conflict_graph(g,['a','b'],2)
        self.assertTrue(stronger.has_edge('a','b'))
        self.assertEqual(solve_mwis(stronger,{'a':3,'b':2})['selected'],['a'])

    def test_capacity_and_forced_membership(self):
        g=nx.empty_graph(3);w={0:5,1:4,2:1}
        self.assertEqual(solve_mwis(g,w,max_size=2)['objective'],9)
        self.assertEqual(solve_mwis(g,w,max_size=2,included=[2])['objective'],6)
        self.assertEqual(solve_mwis(nx.Graph(),{})['selected'],[])

    def test_results_feasible_and_certified(self):
        r=json.loads((ROOT/'research/mwis/results.json').read_text())
        data=json.loads(subprocess.check_output(['git','show',f'{INPUT_REF}:research/agastya/graph.json'],cwd=ROOT))
        people={n['id'] for n in data['nodes'] if n['type'] in PERSON_TYPES}
        claims=[c for c in data['claims'] if c['subject'] in people and c['object'] in people and c['status']!='identity_hypothesis']
        g=make_graph(claims,people)
        for name,m in r['models'].items():
            selected=set(m['selected'])
            self.assertTrue(m['optimal'],name)
            self.assertEqual(m['gap'],0.,name)
            self.assertAlmostEqual(m['upper_bound'],m['objective'],places=5)
            self.assertEqual(g.subgraph(selected).number_of_edges(),0,name)
            if m['cardinality_limit'] is not None:self.assertLessEqual(len(selected),m['cardinality_limit'])
            if m['conflict_distance']==2:
                for n in selected:
                    near=set(nx.single_source_shortest_path_length(g,n,cutoff=2))-{n}
                    self.assertFalse(near.intersection(selected),name)


if __name__=='__main__':unittest.main()
