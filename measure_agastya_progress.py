"""Audit named individuals separately from graph nodes and index candidates."""
import csv
import json
from collections import Counter
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent / 'research' / 'agastya'
graph = json.loads((ROOT / 'graph.json').read_text())
index = json.loads((ROOT / 'expansion' / 'inm-candidates-summary.json').read_text())

# These are individual entities within a textual witness, including named gods
# and nonhuman figures. Collective, place, text and uncertain entity types do
# not enter the target. This is a registry count, not a historical census.
INDIVIDUAL_TYPES = {
    'person', 'deity', 'celestial', 'asura', 'commentator', 'poet',
    'bodhisattva', 'person_or_king', 'person_or_prince',
}
UNNAMED = {
    'tugras_son', 'vidarbha_king', 'tamil_unnamed_northern_sage',
    'root_prince', 'root_student',
    'vp89_unnamed_kasi_king', 'tamil_later_cook',
    'tamil_later_peelivalai_child', 'tamil_later_peelivalai_story_king',
    'tamil_later_chola_king_23', 'tamil_later_manmuhan_cow',
    'mb2xxx_pandya',
    'mb_battle_martikavata_bhoja',
}
# A source-local node can represent a name or rebirth of a person already
# counted. Keep both graph nodes, but count the textual individual once.
SAME_INDIVIDUAL_AS = {
    'vp_nahusha': 'nahusha',
    'vp19end_urvashi': 'urvasi',
    'tamil_later_arundhati_ch18': 'arundhati',
    'tamil_later_ahalya': 'vp19end_ahalya',
    'tamil_later_goddess_kannagi': 'tamil_kannagi',
    'tamil_later_punniyarajan': 'tamil_apputhiran',
    'tamil_lakshmi_past': 'tamil_manimekalai_heroine',
    'tamil_kavera_kanni': 'tamil_manimekalai_heroine',
    'tamil_ragulan': 'tamil_udayakumaran',
    'tamil_tharai': 'tamil_madhavi',
    'tamil_veerai': 'tamil_sudhamathi',
    # Book 4.14–15 repeats explicitly anchored parents, spouses and children
    # already represented by source-local nodes in Books 4.18 and 4.20.
    'vp4_14_prtha': 'vp18_pritha',
    'vp4_14_pandu': 'vp20_pandu',
    'vp4_14_yudhisthira': 'yudhisthira',
    'vp4_14_arjuna': 'vp20_arjuna',
    'vp4_14_karna': 'vp18_karna',
    'vp4_14_madri': 'vp20_madri',
    'vp4_14_nakula': 'vp20_nakula',
    'vp4_14_sahadeva': 'vp20_sahadeva_pandava',
    'vp4_14_dharma': 'vp20_dharma_deity',
    'vp4_14_vayu': 'vp20_vayu_deity',
    'vp4_14_indra': 'indra',
    'vp4_15_ravana': 'ravana_epic',
    'vp4_15_rama': 'rama',
    'vp4_15_dasaratha': 'dasaratha',
    'vp4_15_sita': 'sita',
    'vp4_15_kṛṣṇa': 'vp20_krishna_deity',
    'vp4_15_balarama': 'puranic_balarama',
    'mb2ix_naga_vasuki': 'mb_adi_kadru_vasuki',
    'mb2ix_naga_takshaka': 'mb_adi_kadru_takshaka',
    'mb2ix_naga_airavana': 'mb_adi_kadru_airavata',
    'mb2ix_naga_karkotaka': 'mb_adi_kadru_karkotaka',
    'mb2ix_naga_dhananjaya': 'mb_adi_kadru_dhanamjaya',
}
# The Ādiparvan identifies the human figures in this roster as births of
# named earlier beings. Retain both manifestations in the graph, count once.
for claim in graph['claims']:
    if claim['predicate'] == 'is_human_incarnation_of':
        SAME_INDIVIDUAL_AS[claim['subject']] = claim['object']
PASSAGE_STATUSES = {'translation_checked', 'source_text_checked'}
claims_by_node = {n['id']: [] for n in graph['nodes']}
for claim in graph['claims']:
    for endpoint in {claim['subject'], claim['object']}:
        claims_by_node[endpoint].append(claim)

rows = []
for node in graph['nodes']:
    if node['type'] not in INDIVIDUAL_TYPES or node['id'] in UNNAMED or node['id'] in SAME_INDIVIDUAL_AS:
        continue
    claims = claims_by_node[node['id']]
    rows.append({
        'id': node['id'],
        'label': node['label'],
        'entity_type': node['type'],
        'review_level': 'passage_checked' if any(c['status'] in PASSAGE_STATUSES for c in claims) else 'needs_primary_passage_review',
        'claim_ids': ';'.join(c['id'] for c in claims),
        'source_ids': ';'.join(sorted({c['source'] for c in claims})),
    })

# All Agastya facets are one provisional identity for this *count* only. The
# graph keeps them separate because the textual traditions must stay visible.
agastya_facets = [n['id'] for n in graph['nodes'] if n['type'] == 'agastya_facet']
assert agastya_facets
assert any(any(c['status'] in PASSAGE_STATUSES for c in claims_by_node[f]) for f in agastya_facets)
rows.append({
    'id': 'agastya_counting_identity', 'label': 'Agastya / Akattiyar (provisional counting identity)',
    'entity_type': 'agastya_facet_group', 'review_level': 'passage_checked',
    'claim_ids': ';'.join(c['id'] for f in agastya_facets for c in claims_by_node[f]),
    'source_ids': ';'.join(sorted({c['source'] for f in agastya_facets for c in claims_by_node[f]})),
})

with (ROOT / 'individuals.csv').open('w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda row: row['label'].casefold()))

spellings = defaultdict(list)
for node in graph['nodes']:
    if node['type'] in INDIVIDUAL_TYPES:
        name = node['label'].split(' · ')[0].split(' / ')[0]
        spellings[name].append(node['id'])
same_name = [{'name': name, 'source_local_ids': ';'.join(ids), 'records': len(ids),
              'review': 'homonym_or_alias_to_check'}
             for name, ids in sorted(spellings.items()) if len(ids) > 1]
with (ROOT / 'identity-review.csv').open('w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=('name', 'source_local_ids', 'records', 'review'))
    writer.writeheader()
    writer.writerows(same_name)

levels = Counter(row['review_level'] for row in rows)
types = Counter(row['entity_type'] for row in rows)
report = {
    'as_of': graph['as_of'],
    'target': 3000,
    'named_source_local_individual_records': len(rows),
    'passage_checked_named_records': levels['passage_checked'],
    'needs_primary_passage_review': levels['needs_primary_passage_review'],
    'record_types': dict(sorted(types.items())),
    'source_local_alias_or_rebirth_nodes_not_counted_again': SAME_INDIVIDUAL_AS,
    'same_spelling_groups_pending_identity_review': len(same_name),
    'remaining_to_target_at_passage_checked_level': max(0, 3000 - levels['passage_checked']),
    'separate_index_headword_candidates': index['classification_counts']['likely_individual_candidate'],
    'index_candidates_counted_in_target': 0,
    'counting_policy': 'Named individual entities, including deities and named nonhuman beings. Excludes unnamed roles, collectives, places, texts, ambiguous person_or_entity nodes, and listed same-individual aliases or rebirth names. Agastya facets count as one provisional identity. A passage_checked record has at least one translation_checked or source_text_checked claim and locator. This is a count of textual dossiers; further cross-text identity and original-language audit remain open.',
}
(ROOT / 'progress.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
