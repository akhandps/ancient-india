"""Write a small, source-local Jambavant research supplement.

Hand-curated passage summaries, not an automatic extraction or canonical merge.
Re-running recreates the source-local dossier and canonical expansion batch.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'research/jambavant'
OUT.mkdir(parents=True, exist_ok=True)

sources = [
    ('JV_R117', 'Vālmīki Rāmāyaṇa 1.17', 'https://www.valmikiramayan.net/utf8/baala/sarga17/balasans17.htm'),
    ('JV_R465', 'Vālmīki Rāmāyaṇa 4.65', 'https://www.valmikiramayan.net/utf8/kish/sarga65/kishkindhasans65.htm'),
    ('JV_R466', 'Vālmīki Rāmāyaṇa 4.66', 'https://www.valmikiramayan.net/utf8/kish/sarga66/kishkindhasans66.htm'),
    ('JV_R674', 'Vālmīki Rāmāyaṇa 6.74', 'https://sanskritdocuments.org/sites/valmikiramayan/yuddha/sarga74/yuddharoman74.htm'),
    ('JV_SB8218', 'Bhāgavata Purāṇa 8.21.8', 'https://vedabase.io/en/library/sb/8/21/8/'),
    ('JV_SB1056', 'Bhāgavata Purāṇa 10.56', 'https://vedabase.io/en/library/sb/10/56/'),
    ('JV_SB105624', 'Bhāgavata Purāṇa 10.56.24', 'https://vedabase.io/en/library/sb/10/56/24/'),
    ('JV_SB105626', 'Bhāgavata Purāṇa 10.56.26', 'https://vedabase.io/en/library/sb/10/56/26/'),
    ('JV_SB105628', 'Bhāgavata Purāṇa 10.56.28', 'https://vedabase.io/en/library/sb/10/56/28/'),
    ('JV_SB105632', 'Bhāgavata Purāṇa 10.56.32', 'https://vedabase.io/en/library/sb/10/56/32/'),
    ('JV_SB105633', 'Bhāgavata Purāṇa 10.56.33', 'https://vedabase.io/en/library/sb/10/56/33/'),
    ('JV_SB1061', 'Bhāgavata Purāṇa 10.61.10–12', 'https://vedabase.io/en/library/sb/10/61/10-12/'),
    ('JV_SB111', 'Bhāgavata Purāṇa 11.1.13–15', 'https://vedabase.io/en/library/sb/11/1/13-15/'),
    ('JV_SB11116', 'Bhāgavata Purāṇa 11.1.16', 'https://vedabase.io/en/library/sb/11/1/16/'),
    ('JV_HV138', 'Harivaṃśa, Harivaṃśaparvan 1.38, site edition', 'https://www.dvaipayana.net/harivamsa/harivamshaparva/hv_1_38.html'),
    ('JV_R560', 'Vālmīki Rāmāyaṇa 5.60', 'https://www.valmikiramayan.net/utf8/sundara/sarga60/sundarasans60.htm'),
    ('JV_SB105616', 'Bhāgavata Purāṇa 10.56.16', 'https://vedabase.io/en/library/sb/10/56/16/'),
    ('JV_SB105635', 'Bhāgavata Purāṇa 10.56.35', 'https://vedabase.io/en/library/sb/10/56/35/'),
]
node_specs = [
    ('jv_ram', 'Jāmbavān · Rāmāyaṇa dossier', 'person'),
    ('jv_sb8', 'Jāmbavān · Bhāgavata 8.21 dossier', 'person'),
    ('jv_sb10', 'Jāmbavān · Bhāgavata 10.56 dossier', 'person'),
    ('jv_brahma_ram', 'Brahmā · Rāmāyaṇa 1.17 creation account', 'deity'),
    ('jv_trivikrama_ram', 'Trivikrama / Viṣṇu · Rāmāyaṇa 4.65', 'deity'),
    ('jv_garuda_ram', 'Garuḍa · Jāmbavān’s recollection in Rāmāyaṇa 4.66', 'celestial'),
    ('jv_vamana_sb8', 'Vāmana · Bhāgavata 8.21 victory', 'deity'),
    ('jv_krishna_sb10', 'Kṛṣṇa · Bhāgavata Syamantaka episode', 'person'),
    ('jv_jambavati_sb10', 'Jāmbavatī · Bhāgavata 10.56 / 10.61', 'person'),
    ('jv_son_sb10', 'Unnamed young son of Jāmbavān · Bhāgavata 10.56', 'person'),
    ('jv_lion_sb10', 'Unnamed lion in the Syamantaka episode · Bhāgavata', 'animal_or_entity'),
    ('jv_gem_sb10', 'Syamantaka jewel · Bhāgavata 10.56', 'object'),
    ('jv_samba_sb', 'Sāmba · Jāmbavatī’s son in Bhāgavata 10.61 / 11.1', 'person'),
    ('jv_yadu_boys_sb11', 'Young Yadu boys · Bhāgavata 11.1', 'people_collective'),
    ('jv_sages_sb11', 'Sages addressed by the Yadu boys · Bhāgavata 11.1', 'people_collective'),
    ('jv_earth_ram', 'Earth · Jāmbavān’s recollection in Rāmāyaṇa 4.66', 'place'),
    ('jv_amrita_herbs', 'Herbs gathered for nectar-churning · Rāmāyaṇa 4.66', 'object'),
    ('jv_churning', 'Nectar-churning recalled by Jāmbavān · Rāmāyaṇa 4.66', 'event'),
    ('jv_kin_vp', 'Kṛṣṇa’s kinsfolk · Viṣṇu Purāṇa Syamantaka episode', 'people_collective'),
    ('jv_funeral_rites_vp', 'Funerary offerings for the presumed-dead Kṛṣṇa · Viṣṇu Purāṇa 4.13', 'event'),
    ('jv_duel_vp', 'Jāmbavant–Kṛṣṇa duel · Viṣṇu Purāṇa 4.13', 'event'),
    ('jv_nurse_vp', 'Unnamed nurse of Jāmbavant’s child · Viṣṇu Purāṇa 4.13', 'person'),
    ('jv_dvaraka_residents_sb', 'Residents of Dvārakā · Bhāgavata 10.56.35', 'people_collective'),
    ('jv_candrabhaga_durga', 'Candrabhāgā / Durgā · Bhāgavata 10.56.35', 'deity'),
]
claims = []


def add(number, subject, predicate, obj, source, locator, summary, **qualifications):
    claims.append(dict(id=f'JV{number:03}', subject=subject, predicate=predicate,
        object=obj, source=source, locator=locator, summary=summary,
        status='translation_checked', original_language_reviewed=False,
        **qualifications))


add(1, 'jv_brahma_ram', 'creates', 'jv_ram', 'JV_R117', '1.17.7',
    'Brahmā describes Jāmbavān emerging when he yawned.', speaker='Brahmā',
    note='Narrated origin, not an ordinary biological father claim.')
add(2, 'jv_ram', 'recalls_circumambulating', 'jv_trivikrama_ram', 'JV_R465', '4.65.15',
    'Jāmbavān recalls circling Trivikrama at Bali’s sacrifice.', speaker='Jāmbavān',
    note='Verse 15 gives no count of circuits. No yuga-to-calendar conversion.')
add(3, 'jv_ram', 'argues_against_sending_leader', 'ram6_angada', 'JV_R465', '4.65.20–27',
    'He argues that Aṅgada should be protected as leader.', speaker='Jāmbavān')
add(4, 'jv_ram', 'encourages_for_ocean_crossing', 'ram6_hanuman', 'JV_R465', '4.65.34–35',
    'He turns to Hanumān to enable the mission.', speaker='Jāmbavān')
add(5, 'jv_ram', 'reports_having_seen', 'jv_garuda_ram', 'JV_R466', '4.66.4–6',
    'He recalls seeing Garuḍa and compares Hanumān’s abilities.', speaker='Jāmbavān')
add(6, 'jv_ram', 'narrates_birth_and_praises_capacity_of', 'ram6_hanuman', 'JV_R466', '4.66.8–30, 37',
    'He recounts Hanumān’s origins and urges action.', speaker='Jāmbavān',
    note='No forgetting-curse claim is extracted from the site’s commentary.')
add(7, 'jv_ram', 'recognizes_by_voice', 'vibhishana_epic', 'JV_R674', '6.74.17',
    'Wounded Jāmbavān identifies Vibhīṣaṇa by voice.', speaker='Jāmbavān')
add(8, 'jv_ram', 'asks_about_survival_of', 'ram6_hanuman', 'JV_R674', '6.74.18–23',
    'He treats Hanumān’s survival as crucial to recovery.', speaker='Jāmbavān',
    addressee='vibhishana_epic', note='An inquiry about Hanumān, not an address to him.')
add(9, 'jv_ram', 'sends_for_four_healing_herbs', 'ram6_hanuman', 'JV_R674', '6.74.26–34',
    'He directs Hanumān to fetch four restorative herbs.', speaker='Jāmbavān')
add(10, 'jv_ram', 'is_described_as_son_of', 'jv_brahma_ram', 'JV_R674', '6.74.14',
    'The battlefield account calls him Prajāpati’s son.', speaker='narrator',
    note='Linked translation identifies Prajāpati here as Brahmā; retain that qualification.')
add(11, 'jv_sb8', 'announces_victory_of', 'jv_vamana_sb8', 'JV_SB8218', '8.21.8',
    'Jāmbavān proclaims Vāmana’s victory with an instrument.', speaker='narrator',
    note='No circumambulation count is given in this verse.')
add(12, 'jv_sb10', 'fights_with', 'jv_krishna_sb10', 'JV_SB105624', '10.56.24',
    'The two fight for twenty-eight days.', speaker='Śuka')
add(13, 'jv_sb10', 'recognizes_as_vishnu', 'jv_krishna_sb10', 'JV_SB105626', '10.56.26',
    'Jāmbavān identifies his opponent as Viṣṇu.', speaker='Jāmbavān',
    note='A character’s theological recognition, not a database same-person merge.')
add(14, 'jv_sb10', 'attributes_prior_lanka_campaign_to', 'jv_krishna_sb10', 'JV_SB105628', '10.56.28',
    'He associates his addressee with the bridge and Laṅkā campaign.', speaker='Jāmbavān',
    note='Rāma is not explicitly named in the verse; the episode identification is contextual. Does not itself say the speaker personally witnessed every listed deed.')
add(15, 'jv_sb10', 'father_of', 'jv_jambavati_sb10', 'JV_SB105632', '10.56.32',
    'Jāmbavatī is identified as Jāmbavān’s daughter.', speaker='Śuka')
add(16, 'jv_sb10', 'presents_jewel_and_daughter_to', 'jv_krishna_sb10', 'JV_SB105632', '10.56.32',
    'He presents the jewel and his daughter to Kṛṣṇa.', speaker='Śuka')
add(17, 'jv_sb10', 'father_of', 'jv_son_sb10', 'JV_SB1056', '10.56.15',
    'The jewel becomes a plaything for his young son.', speaker='Śuka',
    note='The verse leaves the son unnamed. Do not automatically label him Sukumāra.')
add(18, 'jv_sb10', 'kills', 'jv_lion_sb10', 'JV_SB1056', '10.56.14',
    'Jāmbavān kills the lion that killed Prasena.', speaker='Śuka',
    note='This is not a claim that Jāmbavān killed Prasena.')
add(19, 'jv_son_sb10', 'plays_with', 'jv_gem_sb10', 'JV_SB1056', '10.56.15',
    'The child plays with the Syamantaka jewel.', speaker='Śuka')
add(20, 'jv_jambavati_sb10', 'mother_of', 'jv_samba_sb', 'JV_SB1061', '10.61.11–12',
    'Sāmba is listed among Jāmbavatī’s sons.', speaker='Śuka')
add(21, 'jv_samba_sb', 'is_son_of', 'jv_jambavati_sb10', 'JV_SB111', '11.1.14',
    'The later episode again names Sāmba’s mother.', speaker='Śuka')
add(22, 'jv_yadu_boys_sb11', 'disguise_as_pregnant_woman', 'jv_samba_sb', 'JV_SB111', '11.1.13–15',
    'The Yadu boys disguise Sāmba to test the sages.', speaker='Śuka')
add(23, 'jv_sages_sb11', 'predict_dynasty_destroying_club_to', 'jv_yadu_boys_sb11', 'JV_SB11116', '11.1.16',
    'The sages foretell a club destructive to their dynasty.', speaker='sages',
    note='A reported prediction addressed to the boys; not a causal edge from Jāmbavān.')
add(24, 'jv_ram', 'reports_circling_twenty_one_times', 'jv_earth_ram', 'JV_R466', '4.66.32',
    'He reports twenty-one circuits of the earth during Trivikrama’s time.', speaker='Jāmbavān',
    note='The object is the earth, not explicitly Trivikrama’s body. This numerical passage was omitted from the initial dossier.')
add(25, 'jv_ram', 'recalls_collecting', 'jv_amrita_herbs', 'JV_R466', '4.66.33',
    'He recalls collecting herbs under divine orders for nectar-churning.', speaker='Jāmbavān',
    note='The speaker uses a plural rendered as royal we by the linked translator. No claim that these are the later four healing herbs.')
add(26, 'jv_amrita_herbs', 'are_intended_for', 'jv_churning', 'JV_R466', '4.66.33',
    'The collected herbs belong to the recalled nectar-churning operation.', speaker='Jāmbavān')
add(27, 'jv_ram', 'counsels_considering_ramas_intent', 'ram6_angada', 'JV_R560', '5.60.5–6',
    'He urges Aṅgada to consider Rāma’s intention before acting.', speaker='Jāmbavān',
    note='This short passage does not explicitly state a ban on unauthorized rescue, despite expanded retellings.')
add(28, 'ram6_angada', 'proposes_bringing_back', 'sita', 'JV_R560', '5.60.1–4',
    'Aṅgada proposes returning with Sītā rather than only reporting.', speaker='Aṅgada',
    note='A proposed action, not a completed rescue.')
add(29, 'jv_kin_vp', 'perform_funeral_rites_for', 'vp4_15_kṛṣṇa', 'vp4_13_17_anu', '4.13.18',
    'Kṛṣṇa’s kinsfolk perform rites after receiving news of his supposed death.', speaker='Parāśara',
    note='The report is mistaken within the narrative; Kṛṣṇa is still fighting.')
add(30, 'jv_funeral_rites_vp', 'are_narrated_to_sustain', 'vp4_15_kṛṣṇa', 'vp4_13_17_anu', '4.13.18–19',
    'The offerings are narrated as sustaining Kṛṣṇa during the duel.', speaker='Parāśara',
    note='A claim within this telling, not an empirical statement about ritual efficacy.')
add(31, 'vp4_13_jambavant', 'weakens_without_food_during', 'jv_duel_vp', 'vp4_13_17_anu', '4.13.19',
    'Jāmbavant lacks food and weakens as the fight continues.', speaker='Parāśara')
add(32, 'jv_nurse_vp', 'sings_to', 'vp4_13_sukumara', 'vp4_13_17_anu', '4.13.14–15',
    'The nurse’s song recounts the jewel’s passage through the lion and bear.', speaker='Parāśara')
add(33, 'vp4_15_kṛṣṇa', 'hears_song_of', 'jv_nurse_vp', 'vp4_13_17_anu', '4.13.14–17',
    'Kṛṣṇa hears the nurse before approaching the jewel.', speaker='Parāśara',
    note='Hearing is not necessarily a reciprocal conversation.')
add(34, 'jv_kin_vp', 'suspect_killing_of_prasena_by', 'vp4_15_kṛṣṇa', 'vp4_13_17_anu', '4.13.13',
    'The Yādavas suspect Kṛṣṇa after Prasena disappears.', speaker='Parāśara',
    note='This encodes suspicion, not Kṛṣṇa killing Prasena. The subject is the collectively described Yādavas.')
add(35, 'vp4_13_satrajita', 'accuses_of_killing_prasena', 'jv_krishna_sb10', 'JV_SB105616', '10.56.16',
    'Satrājit voices the accusation that spreads through the populace.', speaker='Satrājit',
    note='An attributed accusation, contradicted by the narrated lion episode; not an actual killing edge.')
add(36, 'jv_dvaraka_residents_sb', 'pray_for_krishnas_return_to', 'jv_candrabhaga_durga', 'JV_SB105635', '10.56.35',
    'The residents seek Kṛṣṇa’s return through Candrabhāgā / Durgā.', speaker='Śuka',
    note='Compare the VP funerary-offering narrative; do not infer either practice is absent from every other witness.')

observations = [
    dict(id='JVO01', kind='narrated_duration', episode='Syamantaka fight',
         source='vp4_13_17_anu', locator='4.13.17', value=21, unit='days'),
    dict(id='JVO02', kind='narrated_duration', episode='Syamantaka fight',
         source='JV_SB105624', locator='10.56.24', value=28, unit='days'),
    dict(id='JVO03', kind='narrated_wait', episode='Companions outside cave',
         source='vp4_13_17_anu', locator='4.13.18', alternatives=[7,8], unit='days'),
    dict(id='JVO04', kind='narrated_wait', episode='Companions outside cave',
         source='JV_SB105633', locator='10.56.33', value=12, unit='days'),
    dict(id='JVO05', kind='self_reported_capacity', subject='jv_ram',
         source='JV_R465', locator='4.65.13', value=90, unit='yojana',
         note='Narrative capacity claim; no conversion to modern distance.'),
    dict(id='JVO06', kind='self_reported_capacity', subject='ram6_angada',
         source='JV_R465', locator='4.65.19', value=100, unit='yojana',
         return_capacity='uncertain', note='Jāmbavān subsequently invokes protection of the leader.'),
    dict(id='JVO07', kind='narrated_duration', episode='Syamantaka fight',
         source='JV_HV138', locator='1.38.39', value=21, unit='days',
         note='Site numbering; not asserted to equal a critical-edition locator. This is a third textual witness, not independent historical corroboration.'),
    dict(id='JVO08', kind='self_reported_circuits', subject='jv_ram', object='jv_earth_ram',
         source='JV_R466', locator='4.66.32', value=21, unit='circuits',
         note='Circuits of the earth; kept distinct from the unnumbered Trivikrama circumambulation in 4.65.15.'),
]
supplement = dict(schema_version='jambavant-supplement-1', as_of='2026-11-15',
    scope='Targeted reading of selected translations, not an exhaustive concordance or original-language audit.',
    identity_policy='Jāmbavān dossiers remain separate by textual context. Scenario maps are explicit literary alignments, not historical identifications.',
    nodes=[dict(id=i,label=l,type=t) for i,l,t in node_specs],
    sources=[dict(id=i,title=t,url=u,kind='primary_translation',accessed='2026-11-15',
                  locator='',edition='Linked online verse translation; site-specific numbering.',
                  note='Translated verse/narrative used; commentary is not promoted to primary evidence.') for i,t,u in sources],
    claims=claims, observations=observations,
    scenario_alignments={
        'jambavant_only':{'jv_ram':'vp4_13_jambavant','jv_sb8':'vp4_13_jambavant','jv_sb10':'vp4_13_jambavant'},
        'additional_named_figures':{'jv_krishna_sb10':'vp4_15_kṛṣṇa',
             'jv_jambavati_sb10':'vp4_15_jambavati','jv_samba_sb':'vp4_15_samba',
             'jv_vamana_sb8':'sb8_13_vamana','jv_trivikrama_ram':'sb8_13_vamana'}},
    rejected_name_matches=['Jambha','Jambhāsura','Jambūmāli','Vāmana the serpent'],
    open_work=['Collate Sanskrit and critical-edition numbering before philological claims.',
               'Review more Jāmbavān passages and alternative Syamantaka tellings.',
               'Retain disagreements in duration and names instead of harmonizing them.'])
(OUT/'records.json').write_text(json.dumps(supplement,ensure_ascii=False,indent=2)+'\n')
# Keep collector dossiers intact. The canonical graph continues the existing
# literary cross-text alignment, with the exact mapping recorded in the batch.
mapping=dict(supplement['scenario_alignments']['jambavant_only'],
             **supplement['scenario_alignments']['additional_named_figures'])
mapping['jv_gem_sb10']='vp4_13_syamantaka'
canonical_claims=[]
for original in claims:
    c=dict(original)
    c['facet']='ramayana' if c['source'].startswith('JV_R') else 'puranic'
    c.setdefault('category','relationship');c.setdefault('note','');c.setdefault('speaker',None)
    for key in ['subject','object','addressee']:
        if key in c:c[key]=mapping.get(c[key],c[key])
    canonical_claims.append(c)
batch=dict(nodes=[n for n in supplement['nodes'] if n['id'] not in mapping],
           sources=supplement['sources'],claims=canonical_claims,
           observations=[dict(o,**{k:mapping.get(o[k],o[k]) for k in ['subject','object'] if k in o}) for o in observations],
           identity_alignments=mapping,
           identity_note='Literary alignment of named figures in linked episodes, continuing the existing Ramayana/VP merge. Not proof of a single historical lifespan. Original dossiers remain in research/jambavant/records.json.',
           search_log=[{'scope':'Jāmbavant source review', 'result':'Translation-level checks of linked Ramayana, Bhagavata, Vishnu Purana and Harivamsa passages; narrative content kept separate from commentary.'}])
target=OUT.parent/'agastya/expansion/jambavant_deep_dive.json'
target.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n')
print(f'Wrote {len(claims)} claims, {len(observations)} observations, {len(sources)} source records.')
