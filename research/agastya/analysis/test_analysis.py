"""Small graph ground-truth checks and invariants for the generated research run."""
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from analyze_agastya import adjusted_rand, edge_class, make_graph, metrics


class AnalysisTests(unittest.TestCase):
    def test_parallel_claim_support_survives_removal(self):
        claims = [dict(id='a', subject='root', object='x'),
                  dict(id='b', subject='x', object='root')]
        graph = make_graph(claims, {'root','x','isolate'})
        self.assertEqual(graph.number_of_edges(),1)
        self.assertEqual(graph['root']['x']['claim_ids'],['a','b'])
        self.assertEqual(make_graph(claims[1:],set(graph)).number_of_edges(),1)
        result=metrics(graph,['root'])
        self.assertEqual(result['within_three_hops'],1)
        self.assertEqual(result['isolates'],1)

    def test_relation_class_precedence(self):
        self.assertEqual(edge_class('attended_and_honored_birth_of'),'attendance')
        self.assertEqual(edge_class('is_predicted_to_be_father_of'),'prediction')
        self.assertEqual(edge_class('is_born_from_arm_of'),'kinship')
        self.assertEqual(edge_class('is_disciple_of'),'teaching')
        self.assertEqual(edge_class('asks_about'),'narration_or_reference')

    def test_partition_agreement(self):
        a=[{1,2},{3,4}]
        self.assertEqual(adjusted_rand(a,list(reversed(a))),1)
        self.assertAlmostEqual(adjusted_rand(a,[{1,3},{2,4}]),-0.5)

    def test_generated_run_invariants(self):
        r=json.loads((ROOT/'research/agastya/analysis/results.json').read_text())
        raw=(ROOT/'research/agastya/analysis/input-graph.json').read_bytes()
        self.assertEqual(r['input_sha256'],hashlib.sha256(raw).hexdigest())
        baseline=r['variants']['baseline']
        for m in r['variants'].values():
            self.assertEqual(m['nodes'],baseline['nodes'])
            self.assertLessEqual(m['edges'],baseline['edges'])
            self.assertLessEqual(m['within_three_hops'],baseline['within_three_hops'])
        control=r['identity_sensitivity']['scenarios'][0]
        self.assertEqual(control['original_records_with_shorter_distance'],0)
        self.assertEqual(control['newly_reached_original_records'],0)
        self.assertEqual(control['original_records_within_three'],baseline['within_three_hops'])
        for motif in r['motifs']['multiple_parent_records']:
            self.assertNotIn('MBAPE128',[i for p in motif['parents'] for i in p['claim_ids']])
        non_teaching=set(r['semantic_audit']['teaching_non_edges'])
        for motif in r['motifs']['teaching_chains']:
            self.assertFalse(non_teaching.intersection(motif['claim_ids']))


if __name__=='__main__': unittest.main()
