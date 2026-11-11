"""Reproduce a manual precision audit of Sörensen INM candidate records.

The seeded simple random sample is drawn only from the existing
likely_individual_candidate stratum. Decisions adjudicate the INM lead
entry only; they do not claim passage verification or identity resolution.
"""
import csv
import json
import math
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'inm-candidates.csv'
OUTPUT = ROOT / 'inm-review.json'
SAMPLE_CSV = ROOT / 'inm-review-sample.csv'
SEED = 20261027
SAMPLE_N = 100

# Human review of the sampled lead definitions. A failure includes a clearly
# non-individual referent or an entry that merges multiple people under one
# headword. These decisions are scoped to the definition shown, not the epic.
DECISIONS = {
    '3384': ('single_referent_indicated', 'The lead directly identifies Dhanuṣākṣa as one ṛṣi.'),
    '1686': ('single_referent_indicated', 'The numbered entry identifies Bilvaka 1 as one serpent.'),
    '2835': ('single_referent_indicated', 'The lead identifies Śunaḥśepha as the son of Ṛcīka.'),
    '3939': ('single_referent_indicated', 'The lead identifies Gālava as one ṛṣi.'),
    '12117': ('single_referent_indicated', 'The lead identifies Vipṛthu 1 as one Vṛṣṇi prince.'),
    '3884': ('single_referent_indicated', 'The patronymic Ekalavyasuta denotes one son of Ekalavya, though it is not a personal name by itself.'),
    '8732': ('single_referent_indicated', 'Pulomā 2 is identified as one female Asura.'),
    '2429': ('single_referent_indicated', 'Śānta 1 is identified as one son of the Vasu Ahas.'),
    '4756': ('single_referent_indicated', 'Jambūka is identified as one warrior of Skanda.'),
    '748': ('not_single_referent', 'Apsaras is explicitly described as mostly plural, so the headword is not one individual.'),
    '791': ('single_referent_indicated', 'Ariha 2 is identified as one son of Devātithi.'),
    '10243': ('single_referent_indicated', 'Sukratu 2 is identified as one prince.'),
    '9008': ('single_referent_indicated', 'Rathantarī is identified as one wife of Īlina.'),
    '8964': ('single_referent_indicated', 'Rāma 2 is identified as one king with a specific genealogy and spouse.'),
    '11348': ('single_referent_indicated', 'Vaidarbhī 5 is cross-referenced but the lead identifies one wife of Sagara.'),
    '1198': ('single_referent_indicated', 'Bali 2 is described as one king who rescued Dīrghatamas.'),
    '2136': ('single_referent_indicated', 'Citrasena 2 is identified as one son of the elder Parikṣit.'),
    '9174': ('single_referent_indicated', 'Ṛṣika is identified as one king.'),
    '4836': ('single_referent_indicated', 'Jaṭāyu(s) is identified as one vulture and brother of Sampāti.'),
    '10268': ('single_referent_indicated', 'Sumana is tentatively identified as one Gandharva; the question mark lowers confidence but does not indicate plurality.'),
    '4393': ('single_referent_indicated', 'Harī is identified as one daughter of Krodhavaśā.'),
    '5266': ('single_referent_indicated', 'Kāmboja 4 is identified as one ancient king.'),
    '8354': ('single_referent_indicated', 'Piṇḍasektṛ is identified as one serpent.'),
    '3728': ('single_referent_indicated', 'Dṛḍhavrata is identified as one ṛṣi.'),
    '4265': ('single_referent_indicated', 'Gṛdhrapatra is identified as one warrior of Skanda.'),
    '10186': ('single_referent_indicated', 'Sudharman 1 is identified as one Vṛṣṇi prince.'),
    '6938': ('single_referent_indicated', 'Mahodara 3 is identified as one son of Dhṛtarāṣṭra.'),
    '8726': ('single_referent_indicated', 'Pulina is tentatively identified as one Nāga; the note gives a variant identification as Yakṣa.'),
    '2837': ('single_referent_indicated', 'Śunaka 1 is identified as one ṛṣi.'),
    '5349': ('single_referent_indicated', 'Kapaṭa is identified as one Asura.'),
    '7833': ('single_referent_indicated', 'Padmaṇābha 2 is identified as one son of Dhṛtarāṣṭra.'),
    '6632': ('single_referent_indicated', 'Madhuvarna is identified as one warrior of Skanda.'),
    '2235': ('single_referent_indicated', 'Śailālaya is identified as one ancient king and grandfather of Bhagadatta.'),
    '410': ('single_referent_indicated', 'Amatsyāśin is identified as one son of Viśvāmitra.'),
    '2657': ('single_referent_indicated', 'Śitikaṇṭha 2 is identified as one serpent.'),
    '4482': ('single_referent_indicated', 'Hemavarṇa 2 is identified as one son of Rocamāna.'),
    '5456': ('single_referent_indicated', 'Karṇikā is identified as one Apsaras.'),
    '6179': ('single_referent_indicated', 'Kuṇḍika is identified as one son of Dhṛtarāṣṭra 4.'),
    '11569': ('single_referent_indicated', 'Varāṅgī is identified as one princess with parentage and spousal relationship.'),
    '11112': ('single_referent_indicated', 'Ugratejas 1 is identified as one serpent.'),
    '12632': ('single_referent_indicated', 'Yudhāmanyu is identified as one Pāñcāla and brother of Uttamaujas.'),
    '3910': ('single_referent_indicated', 'Gada is identified as one Vṛṣṇi and younger brother of Kṛṣṇa.'),
    '5640': ('single_referent_indicated', 'Kausalyā 1 is identified as one wife of Pūru.'),
    '2172': ('single_referent_indicated', 'Cyavana 1 is identified as one ṛṣi and son of Bhṛgu.'),
    '6164': ('single_referent_indicated', 'Kuṇḍadhāra 4 is identified as one ṛṣi.'),
    '3273': ('single_referent_indicated', 'Devarāta 2 is identified as one muni and son of Viśvāmitra.'),
    '10703': ('single_referent_indicated', 'Syūmaraśmi is identified as one ṛṣi.'),
    '8462': ('single_referent_indicated', 'Prādhā is identified as one daughter of Dakṣa and wife of Kaśyapa.'),
    '6788': ('single_referent_indicated', 'Mahākarṇi is identified as one minister of king Ambuvīca.'),
    '11903': ('single_referent_indicated', 'Viśvadaṃṣṭra is tentatively identified as one Asura; the question mark signals uncertainty, not plurality.'),
    '7788': ('single_referent_indicated', 'Ogharatha is identified as one son of Oghavat 2.'),
    '11928': ('single_referent_indicated', 'Viśvāmitra is identified as one ṛṣi and son of Gādhi.'),
    '2386': ('single_referent_indicated', 'Śambhu 7 is identified as one son of Kṛṣṇa and Rukmiṇī.'),
    '8350': ('single_referent_indicated', 'Piṇḍāra is identified as one serpent.'),
    '11644': ('single_referent_indicated', 'Vasātīya is glossed as one king of the Vasātis, although the entry gives a title rather than biography.'),
    '12082': ('single_referent_indicated', 'Viṃśa is identified as one son of Ikṣvāku.'),
    '6937': ('single_referent_indicated', 'Mahodara 2 is identified as one Asura, separate numbered entry from Mahodara 3.'),
    '7517': ('single_referent_indicated', 'Naiṣādi 5 is identified as one Kuru warrior by cross-reference.'),
    '9200': ('single_referent_indicated', 'Sada is identified as one son of Dhṛtarāṣṭra.'),
    '12646': ('single_referent_indicated', 'Yugapa is identified as one Gandharva.'),
    '5928': ('single_referent_indicated', 'Kṛṣṇānubhautika is identified as one ṛṣi.'),
    '12158': ('single_referent_indicated', 'Vīrasena is identified as one king, father of Nala.'),
    '3130': ('single_referent_indicated', 'Dāntā is identified as one Apsaras.'),
    '1136': ('single_referent_indicated', 'Bala 7 is identified as one son of Parikṣit and king of Ayodhyā.'),
    '5015': ('single_referent_indicated', 'Kāśya 1 is identified as one king and father of Ambā, Ambikā, and Ambālikā.'),
    '8137': ('single_referent_indicated', 'Parāvasu is identified as one brahman with named kin.'),
    '10567': ('single_referent_indicated', 'Suvāha is identified as one warrior of Skanda.'),
    '7203': ('single_referent_indicated', 'Mātaṅgī is identified as one daughter of Krodhavaśā and mother of the elephants.'),
    '6115': ('single_referent_indicated', 'Kumārī 2 is identified as one wife of Dhanañjaya.'),
    '4131': ('single_referent_indicated', 'Ghaṭotkaca is identified as one Rākṣasa with named parents.'),
    '12270': ('single_referent_indicated', 'Vṛddhakṣatra 1 is identified as one king and father of Jayadratha.'),
    '1883': ('not_single_referent', 'Caidya is an epithet/title applied in the entry to Śiśupāla and Dhṛṣṭaketu, so one record does not mean one person.'),
    '10743': ('single_referent_indicated', 'Taṃsu is identified as one ancient king.'),
    '10647': ('single_referent_indicated', 'Svarbhānu is identified as one demon and equated with Rāhu; aliasing does not make the entry plural.'),
    '12386': ('single_referent_indicated', 'Vṛtta 1 is identified as one serpent.'),
    '1936': ('single_referent_indicated', 'Cāmpeya is identified as one son of Viśvāmitra.'),
    '4651': ('single_referent_indicated', 'Indrasena 2 is identified as one son of Nala and Damayantī.'),
    '705': ('single_referent_indicated', 'Anuyāyin is identified as one son of Dhṛtarāṣṭra.'),
    '10091': ('single_referent_indicated', 'Subala 1 is identified as one ancient king.'),
    '2853': ('single_referent_indicated', 'Śūrasena 2 is identified as one Kuru warrior.'),
    '11130': ('single_referent_indicated', 'Ulūka 2 is tentatively identified as one Nāga; the note records an alternate Yakṣa identification.'),
    '2789': ('single_referent_indicated', 'Śuci 10 is identified as one son of Bhṛgu.'),
    '4987': ('single_referent_indicated', 'Kāśin is identified as one son of Kavi.'),
    '6102': ('single_referent_indicated', 'Kumāra 3 is identified as one Suparṇa and son of Garuḍa.'),
    '11820': ('not_single_referent', 'Vetrakīyagṛha is identified as the residence of a king, a place rather than an individual.'),
    '3919': ('single_referent_indicated', 'Gādhi is identified as one king with parentage and named descendants.'),
    '5454': ('single_referent_indicated', 'Karṇaveṣṭa is identified as one prince.'),
    '11757': ('single_referent_indicated', 'Vāyubala is identified as one son of Maṅkaṇaka.'),
    '4727': ('single_referent_indicated', 'Jalandhama is identified as one warrior of Skanda.'),
    '9992': ('single_referent_indicated', 'Somapa 1 is identified as one warrior of Skanda.'),
    '2183': ('single_referent_indicated', 'Śacī is identified as one queen of Indra, with parentage and child.'),
    '12076': ('single_referent_indicated', 'Vimalā is identified as one daughter of Surabhi.'),
    '11082': ('single_referent_indicated', 'Udrapāraka is identified as one serpent.'),
    '6737': ('single_referent_indicated', 'Mahāśiras 2 is identified as one Asura.'),
    '11008': ('single_referent_indicated', 'Tuhāra is identified as one warrior of Skanda.'),
    '7305': ('single_referent_indicated', 'Merusāvarṇi is identified as one ṛṣi.'),
    '8289': ('single_referent_indicated', 'Pauṣṭī is identified as one wife of Pūru.'),
    '8688': ('single_referent_indicated', 'Pṛṣadaśva is identified as one ancient king.'),
    '8689': ('single_referent_indicated', 'Pṛṣaddhra is identified as one ancient king.'),
    '7307': ('single_referent_indicated', 'Meṣa is identified as one warrior of Skanda.'),
}


with INPUT.open(newline='', encoding='utf-8') as f:
    all_rows = list(csv.DictReader(f))
stratum = [r for r in all_rows if r['classification'] == 'likely_individual_candidate']
sample = random.Random(SEED).sample(stratum, SAMPLE_N)
sample_ids = {row['record_id'] for row in sample}
if sample_ids != set(DECISIONS):
    raise ValueError(f'explicit review/sample mismatch: missing={sorted(sample_ids-set(DECISIONS))}, extra={sorted(set(DECISIONS)-sample_ids)}')
for row in sample:
    decision, reason = DECISIONS[row['record_id']]
    row['audit_decision'] = decision
    row['audit_note'] = reason

successes = sum(r['audit_decision'] == 'single_referent_indicated' for r in sample)
failures = SAMPLE_N - successes
p = successes / SAMPLE_N
z = 1.96
denom = 1 + z*z/SAMPLE_N
center = (p + z*z/(2*SAMPLE_N)) / denom
half = z * math.sqrt(p*(1-p)/SAMPLE_N + z*z/(4*SAMPLE_N*SAMPLE_N)) / denom

candidate_rows = stratum
headword_counts = Counter(r['headword_slp1'] for r in candidate_rows)
report = {
    'title': 'INM likely-individual lead-definition precision review',
    'source': 'Sörensen, Index to the Names in the Mahābhārata, CDSL digitization',
    'source_url': 'https://sanskrit-lexicon.github.io/INM/',
    'candidate_csv': 'inm-candidates.csv',
    'scope': 'Audit of whether the INM lead definition explicitly points to one individual referent. This is not primary-passage verification, distinct-person counting, or an entity-resolution audit.',
    'sampling': {
        'method': 'Simple random sample without replacement within classification=likely_individual_candidate',
        'seed': SEED,
        'sample_n': SAMPLE_N,
        'stratum_n': len(stratum),
        'reproduce': 'python3 research/agastya/expansion/inm-review.py',
    },
    'results': {
        'single_referent_indicated': successes,
        'not_single_referent': failures,
        'observed_precision': p,
        'wilson_95_percent_interval': [round(center-half, 4), round(center+half, 4)],
        'interpretation': 'Observed lead-definition precision is 97% (97/100; Wilson 95% interval 91.5%–99.0%). Treat this as a screening yield, not a verified-person yield.',
    },
    'scale_check': {
        'candidate_records': len(candidate_rows),
        'distinct_slp1_spellings_in_candidate_stratum': len(headword_counts),
        'records_beyond_first_exact_spelling': len(candidate_rows)-len(headword_counts),
        'spellings_with_multiple_candidate_records': sum(n > 1 for n in headword_counts.values()),
        'note': 'Exact spelling duplicates alone remove 494 records; they do not resolve homonyms or aliases with different spellings.',
    },
    'methodology': [
        'Use INM only to generate a candidate queue and citation locator; preserve its record id and page/column throughout review.',
        'For each candidate, open the cited Mahābhārata passage in a chosen edition (prefer the BORI Critical Edition for a stable baseline), verify the Sanskrit name-form and context, and record edition, parvan/chapter/verse, and exact name-bearing text.',
        'Decide whether the passage denotes a person or person-like character; keep animals, places, collectives, offices, events, and abstract names typed separately rather than silently counting them as people.',
        'Resolve identity using explicit kinship, title, epithet, and cross-reference evidence; keep homonyms separate unless evidence supports a merge, and keep alias records attached to a canonical entity instead of counting them again.',
        'For each person entity, retain at least one independently checked passage and an auditable decision/status; treat the target of 3000 as distinct canonical entities with passage evidence, not INM rows.',
        'Calibrate the pattern classifier on a second stratified sample from unclassified_name and alias_or_equivalence; likely_individual precision alone cannot establish how many usable people remain in those large classes.',
    ],
    'pitfalls_observed': [
        {'example': 'Apsaras', 'record_id': '748', 'issue': 'Plural collective slips through because “apsaras” is in the person-signal regex.'},
        {'example': 'Vetrakīyagṛha', 'record_id': '11820', 'issue': 'A lead that mentions a king can still name the king’s residence.'},
        {'example': 'Caidya', 'record_id': '1883', 'issue': 'Title/ethnonym points to multiple people in one index record; a single headword is not a single entity.'},
        {'example': 'same spelling, numbered entries', 'issue': 'The candidate stratum has 2,572 records but 2,078 exact SLP1 spellings; numbered homonyms such as Mahodara 2/3 show that spelling deduplication is not identity resolution.'},
        {'example': 'alias and equivalence entries', 'issue': 'The broader index is dominated by alias_or_equivalence records (5,486); these are valuable discovery links but are mostly not additional entities.'},
        {'example': 'index locator vs primary passage', 'issue': 'Sörensen summarizes and cross-references occurrences; locators may be edition-specific, include variant readings, and require checking against a declared edition.'},
    ],
    'sample': [{key: row[key] for key in ('record_id', 'page_column', 'headword_slp1', 'headword_display', 'classification', 'person_signal', 'source_line', 'source_url', 'audit_decision', 'audit_note')} for row in sample],
}
OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
with SAMPLE_CSV.open('w', newline='', encoding='utf-8') as f:
    fields = list(sample[0])
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(sample)
print(json.dumps(report['results'], ensure_ascii=False))
print(f"Wrote {OUTPUT.name} and {SAMPLE_CSV.name}")
