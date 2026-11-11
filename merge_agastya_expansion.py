"""Merge reviewed passage claims into the Agastya evidence graph."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'research' / 'agastya'
EXP = OUT / 'expansion'
seed = json.loads((OUT / 'seed-graph.json').read_text())
batches = {name: json.loads((EXP / f'{name}.json').read_text()) for name in ('vedic', 'epic', 'tamil', 'reception', 'vedic_three_hops', 'epic_three_hops', 'tamil_puranic_three_hops', 'epic_scale', 'puranic_scale', 'vedic_tamil_scale', 'tamil_scale_review', 'genealogy_scale', 'genealogy_scale_more', 'genealogy_scale_kuru', 'genealogy_scale_kaurava', 'genealogy_anu', 'genealogy_ayus', 'rama_descendants', 'tamil_further', 'tamil_later', 'genealogy_future_kuru', 'genealogy_vedic_solar', 'tamil_final', 'genealogy_future_dynasties', 'genealogy_solar_middle', 'genealogy_yadu_middle', 'mb_sabha_people', 'mb_adi_genealogies', 'mb_sabha_earlier', 'mb_adi_incarnations', 'mb_adi_royal_lineages', 'mb_sabha_first', 'mb_adi_next', 'mb_other_roster', 'mb_war_roster', 'mb_adi_pandava_early', 'ramayana_war_roster', 'mb_battle_new_people', 'mb_vana_roster', 'bhagavata_lineages_more', 'mb_adi_later', 'bhagavata_9_24_new', 'bhagavata_canto8_people', 'mb_adi_later_more', 'bhagavata_canto4_people')}

# Preserve collector output unchanged. These adjustments document the editorial review.
edits = {
    'EEX013': {'summary': 'Vṛdhnaśva offers wealth, but Agastya declines because the king’s income equals his expenditure; Vṛdhnaśva then joins Agastya and Śrutarvan in visiting Trasadasyu.'},
    'TEX_008': {'status': 'scholarly_report', 'note': 'Mahadevan paraphrases Puṟanāṉūṟu 201 and separately proposes identifying the unnamed sage as Agastya. The poem itself and its translation have not been independently checked here.'},
    'TEX_006': {'note': 'The Tamil prologue names Agastya’s overturned vessel and the river’s emergence. The crow occurs in Hart’s explanatory English prose, not in the cited Tamil lines.'},
    'REX006': {'note': 'Cowell’s English for the second half of 4.73 is difficult; this records co-mention only, without inferring kinship or a second event.'},
    'VEX004': {'note': '“Sons of Māna” is in 1.171.5. The identification of Māna as Agastya’s father is commentary. Do not merge him automatically with a Māna in RV 7.33.'},
    'TPH001': {'source': 'tamil_manimekalai_hart'},
    'TPH002': {'source': 'tamil_manimekalai_hart'},
    'VTE002': {'object': 'tamil_manimekalai_heroine', 'locator': 'Canto 2, lines 02-010–02-020', 'note': 'The heroine is a person node distinct from the epic text of the same name.'},
    'VTE004': {'object': 'tamil_manimekalai_heroine', 'note': 'The heroine is a person node distinct from the epic text of the same name.'},
    'GSC033': {'locator': '4.19.3'},
    'GSC034': {'locator': '4.19.3'},
    'GSC039': {'locator': '4.19.3'},
    'TF010': {'subject': 'tamil_adipathi', 'summary': 'After Brahmadarman’s warning, King Adipathi orders his people to leave and travels north with his army toward Avanthi.'},
    'TF016': {'subject': 'tamil_buddha_peedihai', 'summary': 'The Buddha Peedihai foretells the heroine’s rebirth under the name Kavera Kanni.', 'note': 'The shrine, not the goddess Maṇimēkalai, is credited with the prediction.'},
    'TF017': {'note': 'Kavera Kanni is a predicted name for the heroine in the rebirth account, not counted as a second distinct individual.'},
    'TF024': {'object': 'tamil_lakshmi_past', 'summary': 'Aṟavaṇar tells Lakshmi about the Buddha’s sacred footprints and invites her to worship them.'},
    'TF025': {'subject': 'tamil_madhavi', 'object': 'tamil_tharai', 'summary': 'The goddess says Mādhavi is the rebirth of Thārai.'},
    'TF026': {'subject': 'tamil_sudhamathi', 'object': 'tamil_veerai', 'summary': 'The goddess says Sudhamathi is the rebirth of Vīrai.'},
    'GSM011': {'subject': 'vp19_bhavanmanyu', 'predicate': 'is_son_of', 'object': 'vp19_bharadvaja', 'summary': 'Vitatha, also called Bharadvāja in this translation, is the father of Bhavanmanyu.'},
    'GSM040': {'subject': 'vp19_para_samara', 'summary': 'Pāra, son of Samara, is the father of Pṛthu in this branch.'},
    'GSK031': {'source': 'vp4_19_sanskrit', 'note': 'The verse-indexed Sanskrit witness distinguishes Saudāsa and his son Sahadeva. ANU English reads “Saudāsa Sahadeva” as one expression; retain the witness variant rather than treating both readings as one settled genealogy.'},
    'GSK032': {'source': 'vp4_19_sanskrit', 'note': 'This follows the Sanskrit witness’s Saudāsa → Sahadeva → Somaka sequence; ANU English punctuation/wording differs.'},
    'ANU18_038': {'predicate': 'receives_as_daughter', 'summary': 'The childless Aṅga-line Daśaratha receives Śāntā as a daughter from Aja’s son Daśaratha.', 'note': 'The passage says she was given to him; it does not describe a formal adoption rite.'},
    'GKA023': {'subject': 'vp20_parjanya', 'predicate': 'sends_rain_during_reign_of', 'object': 'vp19end_shantanu', 'summary': 'Parjanya sends rain during Śāṃtanu’s reign after Devāpi is deemed ineligible to rule.'},
    'GKA041': {'predicate': 'has_children_with', 'summary': 'Dhṛtarāṣṭra has sons with Gāndhārī; the passage identifies their parentage without narrating the marriage.'},
    'GKA087': {'object': 'vp20_parikshit_abhimanyu', 'summary': 'Abhimanyu is the father of the later Parīkṣit born to Uttarā.'},
    'GKA088': {'object': 'vp20_parikshit_abhimanyu'},
    'GKA090': {'object': 'vp20_parikshit_abhimanyu'},
    'GKA091': {'object': 'vp20_parikshit_abhimanyu'},
    'TL051': {'note': 'The speaking goddess image represents the previously named Kaṇṇaki; the image is a separate graph node, not a second counted person.'},
    'GFK001': {'object': 'vp21_janamejaya_parikshit', 'note': 'This is Abhimanyu’s son Parīkṣit and his future son, distinct from Kuru’s earlier Parīkṣit and Janamejaya in chapter 20.'},
    'GFK002': {'object': 'vp21_shrutasena_parikshit', 'note': 'Future son of Abhimanyu’s son Parīkṣit; distinct from the same-named son of Kuru’s earlier Parīkṣit.'},
    'GFK003': {'object': 'vp21_ugrasena_parikshit', 'note': 'Future son of Abhimanyu’s son Parīkṣit; distinct from the same-named son of Kuru’s earlier Parīkṣit.'},
    'GFK004': {'object': 'vp21_bhimasena_parikshit', 'note': 'Future son of Abhimanyu’s son Parīkṣit; distinct from the same-named son of Kuru’s earlier Parīkṣit.'},
    'TFNL001': {'predicate': 'is_named_as_vedic_authority_to', 'summary': 'The Alavaivādi names Vedaviyasar among the three sages followed by his Vaidika tradition while speaking to Maṇimēkalai.'},
    'TFNL002': {'predicate': 'is_named_as_vedic_authority_to', 'summary': 'The Alavaivādi names Kirudakoodi among the three sages followed by his Vaidika tradition while speaking to Maṇimēkalai.'},
    'TFNL003': {'predicate': 'is_named_as_vedic_authority_to', 'summary': 'The Alavaivādi names Saimini among the three sages followed by his Vaidika tradition while speaking to Maṇimēkalai.'},
    'TFNL011': {'predicate': 'is_described_to_heroine_as_creator_and_destroyer', 'summary': 'A Śaiva interlocutor describes Śiva as creator and destroyer when the heroine asks about his god.'},
    'TFNL012': {'predicate': 'is_described_to_heroine_as_creator', 'summary': 'A Brahmavādi says to the heroine that Brahmā created the worlds.'},
    'TFNL013': {'predicate': 'is_described_to_heroine_as_world_protector', 'summary': 'A Vaiṣṇava interlocutor tells the heroine that Nārāyaṇa protects the world.'},
    'MB3VANA_003': {'predicate': 'rescues', 'summary': 'Indra drives away Keśin and rescues Devasenā from him.'},
}
excluded = {'TEX_008': 'retained only as scholarly report, not as primary translation', 'tamil_cict_iraiyanar_catalogue': 'catalogue lead; no textual claim derived', 'puranic_bp1084': 'roster inspected but no distinctive new relation retained', 'TF009': 'unclear whether the shrine or Brahmadarman is speaker in the retold warning', 'TF029': 'reverses the food offering: Lakshmi offers to feed Sādhu Chakran', 'GKA020': 'unary retirement event was incorrectly encoded as an edge to Śāṃtanu', 'TL068': 'the survivors of the shipwreck, not the missing child, tell the king about the loss', 'TFNL014': 'the passage says Indra worships an unnamed Jain god; it does not say Indra is worshiped by the heroine', 'TFNL017': 'the king hosts visiting sages; the passage does not say he hosts Māsāthuvān', 'TFNL018': 'the earlier Kovalan called an ancestor of the Chera king is not established as the heroine’s father of the same name', 'TFNL029': 'the translated warning and destination are ambiguous and do not directly link Dīpathilahai to Mādhavi', 'TFNL032': 'Aravanar recounts Buddha’s teaching; the passage does not narrate Buddha directly teaching the heroine'}
excluded['MB2ROSTER_001'] = 'self-attendance of the host is not a meaningful relationship'
excluded['MB3VANA_030'] = 'self-edge does not encode the Aditi/Revatī name relationship'
excluded['MB3VANA_031'] = 'self-edge does not encode the Diti/Mukhamaṇḍikā name relationship'
excluded['SB4_0076'] = 'Dahrāgni is retained as Agastya’s next-birth name on the merged Agastya facet; a self-edge adds no relation'
id_rewrites = {'tamil_vasanthamālai': 'tamil_vasanthamalai', 'vp19_raudrashva': 'vp_raudrashva', 'vp19_bharata': 'vp_bharata', 'vp18_aja_dasaratha': 'dasaratha', 'vp20_indra_deity': 'indra', 'vp20_ashvins': 'asvins', 'vp20_yudhishthira': 'yudhisthira', 'mb2_xi_agastya': 'epic', 'mb2vii_indra': 'indra', 'mb2ix_varuna': 'varuna', 'mb2viii_rama_dasharatha': 'rama', 'mb2viii_dasaratha': 'dasaratha', 'mb2viii_rama_jamadagnya': 'vp67_parashurama',
    'mb_adi_royal_shantanu': 'vp19end_shantanu', 'mb_adi_royal_satyavati': 'vp20_satyavati',
    'mb_adi_royal_bhishma': 'vp20_bhishma', 'mb_adi_royal_chitrangada': 'vp20_chitrangada_royal',
    'mb_adi_royal_vichitravirya': 'vp20_vicitravirya', 'mb_adi_royal_ambika': 'vp20_ambika',
    'mb_adi_royal_ambalika': 'vp20_ambalika', 'mb_adi_royal_vyasa': 'vp20_krishna_dvaipayana',
    'mb_adi_royal_dhritarashtra': 'vp20_dhritarashtra', 'mb_adi_royal_pandu': 'vp20_pandu',
    'mb_adi_royal_vidura': 'vp20_vidura', 'mb_adi_royal_dharma': 'vp20_dharma_deity',
    'mb_adi_royal_kunti': 'vp20_kunti', 'mb_adi_royal_madri': 'vp20_madri',
    'mb_adi_royal_karna': 'vp18_karna', 'mb_adi_royal_gandhari': 'vp20_gandhari',
    'mb_adi_royal_ganga': 'vp20_ganga', 'mb_adi_royal_sun': 'surya',
    'mb_adi_royal_son_v2_01': 'vp20_duryodhana', 'mb_adi_royal_son_v2_03': 'vp20_dushasana',
    'mb2_sabha_yudhishthira': 'yudhisthira',
    'mb_adi_nxt_duṣyanta': 'vp_dushyanta', 'mb_adi_nxt_bharata': 'vp_bharata',
    'mb2xxx_nakula': 'vp20_nakula', 'mb2xxx_dhritarashtra': 'vp20_dhritarashtra',
    'mb2xxx_bhishma': 'vp20_bhishma', 'mb2xxx_vidura': 'vp20_vidura',
    'mb2xxx_duryodhana': 'vp20_duryodhana', 'mb2xxx_karna': 'vp18_karna',
    'mb2xxx_somadatta': 'vp20_somadatta', 'mb2xxx_ashwatthama': 'vp19end_ashvatthaman',
    'mb2xxx_kripa': 'vp19end_kripa', 'mb2xxx_drona': 'vp19end_drona',
    'mb2xxx_dussasana': 'vp20_dushasana', 'mb2xxx_sahadeva': 'vp20_sahadeva_pandava',
    'mb2xxx_krishna': 'vp20_krishna_deity', 'mb2xxx_vasudeva_father': 'vp4_14_vasudeva',
    'mb2xxx_drupada': 'vp19end_drupada', 'mb2xxx_ekalavya': 'mb_adi_inc_ekalavya',
    'mb2xxx_jamadagnya': 'vp67_parashurama', 'mb2xxx_virata': 'mb_adi_inc_virata_human_incarnation',
    'mb2xxx_sarana': 'vp4_15_sarana', 'mb2xxx_gada': 'vp4_15_gada',
    'mb2xxx_shamva': 'vp4_15_samba', 'mb2xxx_charudeshna': 'vp4_15_carudesna',
    'mb2xxx_ulmuka': 'vp4_15_ulmuka', 'mb2xxx_nishatha': 'vp4_15_nisatha',
    'mb2xxx_rukmi': 'mb_adi_inc_rukmi',
    'mb5_udyoga_bhimasena': 'vp20_bhima_pandava', 'mb5_udyoga_arjuna': 'vp20_arjuna',
    'mb5_udyoga_subhadra': 'vp20_subhadra',
    'mb_adi_early_draupadi': 'vp20_draupadi', 'mb_adi_early_samvarana': 'vp19end_samvarana',
    'ram6_jambavan': 'vp4_13_jambavant',
    'mb3_kadru': 'mb_adi_kadru', 'mb3_airavata_naga': 'mb_adi_kadru_airavata',
    'mb3_citra_naga': 'mb2ix_naga_chitra', 'mb3_parvati': 'mb2_x_parvati',
    'mb3_vishvakarman': 'mb_adi_early_vishvakarman',
    'sb6_bhava': 'mb_adi_inc_bhava', 'sb6_ajaikapat': 'mb_adi_inc_ajaikapat',
    'sb6_ahirbudhnya': 'mb_adi_inc_ahirbudhnya', 'sb6_surabhi': 'mb3_surabhi',
    'sb6_sarama': 'mb3_sarama',
    'sb4_agastya': 'puranic',
}

node_ids = {n['id'] for n in seed['nodes']}
source_ids = {s['id'] for s in seed['sources']}
claim_ids = {c['id'] for c in seed['claims']}
for batch in batches.values():
    for original_node in batch['nodes']:
        n = dict(original_node)
        n['id'] = id_rewrites.get(n['id'], n['id'])
        if n['id'] not in node_ids:
            seed['nodes'].append(n); node_ids.add(n['id'])
    for s in batch['sources']:
        if s['id'] not in source_ids and s['id'] not in {'tamil_cict_iraiyanar_catalogue', 'tamil_manimekalai_hart_canto22', 'puranic_bp1084', 'mb_ganguli_adi'}:
            seed['sources'].append(s); source_ids.add(s['id'])
    for original in batch['claims']:
        c = dict(original)
        if c['facet'] == 'bhagavata_purana':
            c['facet'] = 'puranic'
        if c['id'].startswith('MBAL') and c['status'] == 'translation_checked':
            c['status'] = 'source_text_checked'
        for end in ('subject', 'object'):
            c[end] = id_rewrites.get(c[end], c[end])
        c.update(edits.get(c['id'], {}))
        if c['id'].startswith('MBAI') and c['predicate'] == 'is_incarnated_as':
            c['predicate'] = 'is_human_incarnation_of'
        if c['id'] in {'TF009', 'TF029', 'GKA020', 'TL068', 'TFNL014', 'TFNL017', 'TFNL018', 'TFNL029', 'TFNL032', 'MB2ROSTER_001', 'MB3VANA_030', 'MB3VANA_031', 'SB4_0076'}:
            continue
        if c['id'] in claim_ids:
            raise ValueError(f'duplicate claim: {c["id"]}')
        seed['claims'].append(c); claim_ids.add(c['id'])

for n in seed['nodes']:
    if n['id'] == 'vedic_vispala':
        n['label'] = 'Viśpalā · interpreted as a mare'
        n['type'] = 'animal_or_entity'
    if n['id'] == 'tamil_brahmadarman':
        n['label'] = 'Brahmadarman · Maṇimēkalai witness'
    if n['id'] in {'tamil_goddess_manimekalai', 'tamil_kama', 'tamil_murugan', 'tamil_bhudam_pukar'}:
        n['type'] = 'deity'
    if n['id'] == 'tamil_later_nakka_saranar':
        n['label'] = 'Nakka Sāraṇar · Nāga people in Maṇimēkalai'
        n['type'] = 'people_collective'
    if n['id'] == 'tamil_later_manmuhan_cow':
        n['type'] = 'animal_or_entity'
    if n['id'] in {'mb2_x_sankha', 'mb2_x_padma'}:
        n['type'] = 'person_or_entity'
    if n['id'] in {'mb2_kubera_sabha_x', 'mb2_brahma_sabha_xi', 'mb2_x_mahadeva', 'mb2_x_parvati', 'mb2_x_lakshmi'}:
        n['type'] = 'deity'
    if n['id'] == 'mb2viii_yama':
        n['type'] = 'deity'
for s in seed['sources']:
    if s['id'] == 'vedic_jb_rv':
        s['locator'] = 'vol. I, hymns 1.117, 1.165, 1.170–172, 1.182–183; VII.33'
    if s['id'] == 'vp4_19_anu':
        s['locator'] = 'Book 4, ch. 19; claim verse locators follow the separate SanskritSahitya/Eternal Raga segmentation, not ANU’s printed stanza numbers'
        s['edition'] = 'McComas Taylor, trans., ANU Press (2021), Book 4, ch. 19; names and relationships follow this English witness unless a claim notes a Sanskrit variant'
    if s['id'] == 'mb_bori_adi_ce':
        s['locator'] = 'Ādiparvan Book 1; each claim gives its own critical-edition chapter and verse locator'

# Further passage-level links found during the review.
additional_nodes = [
    {'id': 'epic_purukutsa', 'label': 'Purukutsa · Mahābhārata witness', 'type': 'person'},
    {'id': 'tamil_sambapathi', 'label': 'Sambāpathi · Maṇimēkalai goddess', 'type': 'deity'},
    {'id': 'vedic_gotama', 'label': 'Gotama · Ṛgveda 1.183.5 witness', 'type': 'person'},
    {'id': 'vedic_purumidha', 'label': 'Purumīḍha · Ṛgveda 1.183.5 witness', 'type': 'person'},
    {'id': 'vp20_parikshit_abhimanyu', 'label': 'Parīkṣit · Abhimanyu’s son · Viṣṇu Purāṇa 4.20 witness', 'type': 'person'},
    {'id': 'vp21_janamejaya_parikshit', 'label': 'Janamejaya · later Parīkṣit’s son · Viṣṇu Purāṇa 4.21 witness', 'type': 'person'},
    {'id': 'vp21_shrutasena_parikshit', 'label': 'Śrutasena · later Parīkṣit’s son · Viṣṇu Purāṇa 4.21 witness', 'type': 'person'},
    {'id': 'vp21_ugrasena_parikshit', 'label': 'Ugrasena · later Parīkṣit’s son · Viṣṇu Purāṇa 4.21 witness', 'type': 'person'},
    {'id': 'vp21_bhimasena_parikshit', 'label': 'Bhīmasena · later Parīkṣit’s son · Viṣṇu Purāṇa 4.21 witness', 'type': 'person'},
    {'id': 'vp_text', 'label': 'Viṣṇu Purāṇa', 'type': 'text'},
]
seed['nodes'] += additional_nodes
node_ids.update(n['id'] for n in additional_nodes)
seed['claims'] += [
    {'id': 'RFX001', 'facet': 'mahabharata', 'subject': 'trasadasyu', 'predicate': 'is_called_son_of', 'object': 'epic_purukutsa', 'source': 'mb398', 'locator': 'Vana Parva, Ganguli §98', 'summary': 'Lomaśa introduces Trasadasyu as the son of Purukutsa when Agastya and the kings visit him.', 'category': 'relationship', 'status': 'translation_checked', 'speaker': 'Lomaśa', 'note': 'Name form in Ganguli: Purokutsa. This is a relationship within the narrated episode.', 'original_language_reviewed': False},
    {'id': 'RFX002', 'facet': 'tamil', 'subject': 'tamil', 'predicate': 'tells_to_worship', 'object': 'tamil_sambapathi', 'source': 'tamil_manimekalai_hart', 'locator': 'Prologue, lines 00-20–00-24', 'summary': 'Agastya tells Kāviri to venerate the goddess Sambāpathi.', 'category': 'outgoing', 'status': 'translation_checked', 'speaker': 'Agastya', 'note': 'The addressee is Kāviri, whom the prologue personifies as the river goddess.', 'original_language_reviewed': False},
    {'id': 'RFX003', 'facet': 'tamil', 'subject': 'tamil', 'predicate': 'addresses', 'object': 'tamil_kaveri', 'source': 'tamil_manimekalai_hart', 'locator': 'Prologue, lines 00-20–00-24', 'summary': 'Agastya addresses the personified Kāviri directly.', 'category': 'outgoing', 'status': 'translation_checked', 'speaker': 'Agastya', 'note': 'Kāviri is represented as both river and goddess in the poem.', 'original_language_reviewed': False},
    {'id': 'RFX004', 'facet': 'vedic', 'subject': 'vedic', 'predicate': 'mentions_as_asvin_invoker', 'object': 'vedic_gotama', 'source': 'vedic_jb_rv', 'locator': 'Ṛgveda 1.183.5; Jamison–Brereton translation, vol. I p. 386', 'summary': 'A hymn attributed to Agastya names Gotama among poets who summon the Aśvins.', 'category': 'outgoing', 'status': 'editorial_attribution', 'speaker': 'Agastya by hymn attribution', 'note': 'A named poetic predecessor or peer, not a recorded meeting. Do not merge automatically with other Gotamas.', 'original_language_reviewed': False},
    {'id': 'RFX005', 'facet': 'vedic', 'subject': 'vedic', 'predicate': 'mentions_as_asvin_invoker', 'object': 'vedic_purumidha', 'source': 'vedic_jb_rv', 'locator': 'Ṛgveda 1.183.5; Jamison–Brereton translation, vol. I p. 386', 'summary': 'A hymn attributed to Agastya names Purumīḍha among poets who summon the Aśvins.', 'category': 'outgoing', 'status': 'editorial_attribution', 'speaker': 'Agastya by hymn attribution', 'note': 'A named poetic predecessor or peer, not a recorded meeting.', 'original_language_reviewed': False},
    {'id': 'RFX006', 'facet': 'vedic', 'subject': 'vedic', 'predicate': 'mentions_as_asvin_invoker', 'object': 'atri', 'source': 'vedic_jb_rv', 'locator': 'Ṛgveda 1.183.5; Jamison–Brereton translation, vol. I p. 386', 'summary': 'A hymn attributed to Agastya names Atri with Gotama and Purumīḍha as summoners of the Aśvins.', 'category': 'outgoing', 'status': 'editorial_attribution', 'speaker': 'Agastya by hymn attribution', 'note': 'This need not be the same scene as other Atri references.', 'original_language_reviewed': False},
    {'id': 'RFX007', 'facet': 'vedic', 'subject': 'vedic', 'predicate': 'mentions', 'object': 'vedic_vispala', 'source': 'vedic_jb_rv', 'locator': 'Ṛgveda 1.182.1; Jamison–Brereton translation, vol. I p. 385', 'summary': 'The Aśvin hymn attributed to Agastya recalls the benefit the gods gave Viśpalā.', 'category': 'outgoing', 'status': 'editorial_attribution', 'speaker': 'Agastya by hymn attribution', 'note': 'Jamison–Brereton interpret Viśpalā as a mare. The verse does not describe Agastya meeting her.', 'original_language_reviewed': False},
]

# Sörensen explicitly identifies the serpent-cursed Nahuṣa as Āyus’s son
# and Yayāti’s father, linking the epic and Purāṇic witnesses as a reviewed
# cross-text identity hypothesis rather than silently collapsing their nodes.
seed['sources'].append({'id': 'inm_nahusha', 'title': 'Sörensen, Index to the Names in the Mahābhārata, Nahuṣa 2', 'url': 'https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/inm/inm.txt#L85413', 'kind': 'scholarly_index', 'edition': 'CDSL digitization of Sörensen, record 7485, p. 494 col. 2', 'locator': 'Nahuṣa 2, record 7485', 'accessed': '2026-10-27'})
source_ids.add('inm_nahusha')
seed['claims'].append({'id': 'RFX008', 'facet': 'mahabharata', 'subject': 'nahusha', 'predicate': 'corresponds_to_puranic_witness', 'object': 'vp_nahusha', 'source': 'inm_nahusha', 'locator': 'Nahuṣa 2, record 7485', 'summary': 'The index groups Āyus’s son and Yayāti’s father with the king cursed into serpent form, linking the two witness dossiers.', 'category': 'identity', 'status': 'scholarly_report', 'speaker': None, 'note': 'This is a cross-text identification based on a secondary concordance; both nodes and their source-specific claims remain visible.', 'original_language_reviewed': False})
seed['claims'] += [
    {'id': 'RFX009', 'facet': 'puranic', 'subject': 'vp67_vishvavasu_gandharva', 'predicate': 'steals_pet_sheep_from', 'object': 'vp19end_urvashi', 'source': 'vp4_6_anu', 'locator': '4.6.33–34', 'summary': 'Viśvāvasu and other gandharvas steal Urvaśī’s pet sheep to break her agreement with Purūravas.', 'category': 'relationship', 'status': 'translation_checked', 'speaker': 'Parāśara', 'note': 'The sheep are not individually named.', 'original_language_reviewed': False},
    *[{'id': f'RFX{i:03d}', 'facet': 'puranic', 'subject': subject, 'predicate': 'is_named_in', 'object': 'vp_text', 'source': 'vp4_24_anu', 'locator': locator, 'summary': summary, 'category': 'attestation', 'status': 'translation_checked', 'speaker': 'Parāśara', 'note': 'The source lists this future ruler; no relationship to another named person is asserted in this clause.', 'original_language_reviewed': False}
      for i, subject, locator, summary in [
          (10, 'vp24_pushyamitra_mekala', '4.24.14', 'Puṣyamitra is named among later kings in the future-dynasty list.'),
          (11, 'vp24_patumitra', '4.24.14', 'Paṭumitra is named among later kings in the future-dynasty list.'),
          (12, 'vp24_vishvasphatika', '4.24.15', 'Viśvasphaṭika is named as a future king in Magadha.'),
          (13, 'vp24_devarakshita', '4.24.15', 'Devarakṣita is named as protector of Kosala and other regions.'),
      ]],
    *[{'id': f'RFX{i:03d}', 'facet': 'tamil', 'subject': subject, 'predicate': 'is_named_in', 'object': 'tamil_manimekalai', 'source': 'tamil_manimekalai_hart', 'locator': locator, 'summary': summary, 'category': 'attestation', 'status': 'translation_checked', 'speaker': 'Narrator', 'note': 'The person is attested by name here without inferring another relationship.', 'original_language_reviewed': False}
      for i, subject, locator, summary in [
          (14, 'tamil_final_kudakko_ceeraladan', 'Canto 28, lines 28-105–28-120', 'Kudakko Ceeralādan is named as the Chera king in Māsāthuvān’s account.'),
          (15, 'tamil_final_deepathilahai', 'Canto 29, lines 29-035–29-040', 'Dīpathilahai is named in the account of the threatened destruction of Pukār.'),
      ]],
]
seed['sources'].append({'id': 'vp_taylor_dating', 'title': 'McComas Taylor, introduction to The Viṣṇu Purāṇa: Problems with dating', 'url': 'https://press-files.anu.edu.au/downloads/press/n8264/html/introduction.xhtml?page=5', 'kind': 'scholarly_introduction', 'edition': 'ANU Press, 2021', 'locator': 'Introduction, “Problems with dating”', 'accessed': '2026-10-27'})
source_ids.add('vp_taylor_dating')
seed['chronology'].append({'id': 'T13', 'facet': 'puranic', 'kind': 'text_formation', 'label': 'Viṣṇu Purāṇa · Taylor’s tentative dating', 'range': 'Possible present extent in 4th–5th centuries CE', 'start': 300, 'end': 500, 'source': 'vp_taylor_dating', 'note': 'Taylor calls this a reasonable guess, not an exact composition date. The genealogies are narrative attestations, not the lifespans of Nahuṣa or descendants.'})

seed['schema_version'] = '0.3'
seed['title'] = 'Agastya: passage-level evidence graph, expansion 3'
seed['scope'] += ' The expansion adds Vedic, epic, Tamil, and Buddhist reception links; it remains a sampled source review, not an exhaustive corpus census.'
seed['open_work'] += [
    'Collate Bṛhaddevatā 4.55–64 against the printed scan and Sanskrit; the online transcription is marked unproofread.',
    'Check Puṟanāṉūṟu 201 in a primary Tamil edition and translation; keep its unnamed sage separate from Agastya pending that review.',
    'Compare the Buddhacarita 4.73 Sanskrit and modern translations before interpreting the Lopāmudrā clause.',
    'Search Mahābhārata and Purāṇa recensions systematically for further named relatives and interlocutors.',
    'Verify three-hop paths in alternate editions, especially the genealogy in Rāmāyaṇa 3.14 and the collective/individual Vasiṣṭha distinction in Ṛgveda 7.33.',
    'Scale entity review with the Sörensen Mahābhārata name index as a candidate queue; do not equate an index headword with a distinct person without passage and identity checks.',
]

assert len(node_ids) == len(seed['nodes'])
assert len(source_ids) == len(seed['sources'])
assert len({c['id'] for c in seed['claims']}) == len(seed['claims'])
for c in seed['claims']:
    assert c['subject'] in node_ids and c['object'] in node_ids and c['facet'] in node_ids, c['id']
    assert c['source'] in source_ids, c['id']

(OUT / 'graph.json').write_text(json.dumps(seed, ensure_ascii=False, indent=2) + '\n')
with (OUT / 'claims.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(seed['claims'][0]))
    writer.writeheader(); writer.writerows(seed['claims'])
(EXP / 'review.json').write_text(json.dumps({'edits': edits, 'qualification': excluded, 'additional_claims': [f'RFX{i:03d}' for i in range(1, 16)]}, ensure_ascii=False, indent=2) + '\n')

print(f"{len(seed['nodes'])} nodes, {len(seed['claims'])} claims, {len(seed['sources'])} sources")
