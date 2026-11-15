import hashlib
import csv
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from analyze_jambavant import rewrite


class DossierTests(unittest.TestCase):
    def setUp(self):
        self.base=json.loads((ROOT/'research/agastya/analysis/input-graph.json').read_text())
        self.s=json.loads((ROOT/'research/jambavant/records.json').read_text())

    def test_references_and_ids(self):
        nodes={n['id'] for n in self.base['nodes']+self.s['nodes']}
        sources={s['id'] for s in self.base['sources']+self.s['sources']}
        ids=[c['id'] for c in self.base['claims']+self.s['claims']]
        self.assertEqual(len(ids),len(set(ids)))
        for c in self.s['claims']:
            self.assertIn(c['subject'],nodes)
            self.assertIn(c['object'],nodes)
            self.assertIn(c['source'],sources)
        for o in self.s['observations']:self.assertIn(o['source'],sources)

    def test_variants_and_inquiry_preserved(self):
        fights=[o['value'] for o in self.s['observations'] if o['kind']=='narrated_duration']
        self.assertEqual(sorted(fights),[21,21,28])
        claims={c['id']:c for c in self.s['claims']}
        self.assertEqual(claims['JV008']['object'],'ram6_hanuman')
        self.assertEqual(claims['JV008']['addressee'],'vibhishana_epic')
        self.assertEqual(claims['JV014']['object'],'jv_krishna_sb10')
        self.assertEqual(claims['JV017']['object'],'jv_son_sb10')
        mappings=self.s['scenario_alignments']
        self.assertNotIn('jv_son_sb10',mappings['additional_named_figures'])

    def test_identity_scenario_does_not_mutate_evidence(self):
        original=[dict(id='a',subject='x',object='y')]
        changed=rewrite(original,{'x':'z'})
        self.assertEqual(original[0]['subject'],'x')
        self.assertEqual(changed[0]['subject'],'z')
        self.assertEqual(changed[0]['id'],original[0]['id'])

    def test_analysis_matches_inputs(self):
        result=json.loads((ROOT/'research/jambavant/analysis.json').read_text())
        for key,path in [('baseline_sha256',ROOT/'research/agastya/analysis/input-graph.json'),
                         ('supplement_sha256',ROOT/'research/jambavant/records.json')]:
            self.assertEqual(result[key],hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(result['supplement_counts']['claims'],len(self.s['claims']))
        self.assertEqual(len(result['scenarios']),5)

    def test_canonical_integration_and_csv_qualifiers(self):
        canonical=json.loads((ROOT/'research/agastya/graph.json').read_text())
        ids={c['id']:c for c in canonical['claims']}
        for c in self.s['claims']:
            self.assertIn(c['id'],ids)
            self.assertEqual(c['summary'],ids[c['id']]['summary'])
        self.assertEqual(ids['MBAPE128']['predicate'],'teacher_of')
        self.assertEqual(len(canonical['observations']),len(self.s['observations']))
        for c in canonical['claims']:
            if c['id'] in {'JV034','JV035'}:
                self.assertNotEqual(c['predicate'],'killed')
                self.assertNotEqual(c['predicate'],'kills')
        with (ROOT/'research/agastya/claims.csv').open() as f:
            exported={row['id']:row for row in csv.DictReader(f)}
        self.assertEqual(exported['JV008']['addressee'],'vibhishana_epic')


if __name__=='__main__':unittest.main()
