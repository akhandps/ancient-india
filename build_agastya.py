"""Curated research seed; generates the evidence graph and review tables."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'research' / 'agastya'
OUT.mkdir(parents=True, exist_ok=True)
sources = {}
nodes = {}
claims = []

def source(key, title, url, kind='primary_translation', edition='', locator=''):
    sources[key] = dict(id=key, title=title, url=url, kind=kind, edition=edition, locator=locator, accessed='2026-10-27')

def node(key, label, kind):
    nodes[key] = dict(id=key, label=label, type=kind)

def claim(facet, a, rel, b, src, loc, summary, category='relationship', status='translation_checked', speaker=None, note=''):
    claims.append(dict(id=f'C{len(claims)+1:03}', facet=facet, subject=a, predicate=rel, object=b,
        source=src, locator=loc, summary=summary, category=category, status=status,
        speaker=speaker, note=note, original_language_reviewed=False))

source('rv170', 'Ṛgveda 1.170', 'https://sacred-texts.com/hin/rigveda/rv01170.htm', edition='R. T. H. Griffith translation')
source('rv179', 'Ṛgveda 1.179', 'https://sacred-texts.com/hin/rigveda/rv01179.htm', edition='Griffith; some verses rendered in Latin; speaker assignments are editorial')
source('rv180', 'Ṛgveda 1.180', 'https://sacred-texts.com/hin/rigveda/rv01180.htm', edition='Griffith translation')
source('rv733', 'Ṛgveda 7.33', 'https://sacred-texts.com/hin/rigveda/rv07033.htm', edition='Griffith translation')
source('ts', 'Taittirīya Saṃhitā 7.5.5', 'https://sacred-texts.com/hin/yv/yv07.htm', edition='A. B. Keith translation')
for s in (11,12,13):
    source(f'ram3{s}', f'Rāmāyaṇa 3.{s}', f'https://www.valmikiramayan.net/utf8/aranya/sarga{s}/aranya_{s}_prose.htm', edition='Desiraju Hanumanta Rao prose translation; site chapter numbering; commentary interspersed')
source('ram441', 'Rāmāyaṇa 4.41', 'https://www.valmikiramayan.net/utf8/kish/sarga41/kishkindha_41_prose.htm', edition='D. H. Rao prose translation; commentary interspersed')
source('ram6105', 'Rāmāyaṇa 6.105: Ādityahṛdaya', 'https://www.valmikiramayan.net/utf8/yuddha/sarga105/yuddha_105_prose.htm', edition='Site numbering; often 6.107 in other editions; no automatic equivalence to critical-edition numbering')
for s in (96,97,98,99,103,104):
    source(f'mb3{s}', f'Mahābhārata, Vana Parva, Ganguli §{s}', f'https://sacred-texts.com/hin/m03/m03{s:03}.htm', edition='K. M. Ganguli translation; section numbers are NOT BORI critical-edition chapter numbers')
source('mb517', 'Mahābhārata, Udyoga Parva, Ganguli §17', 'https://sacred-texts.com/hin/m05/m05017.htm', edition='K. M. Ganguli translation; non-critical-edition section numbering')
for k, loc in [('bp6185','6/18/5'),('bp6186','6/18/6'),('bp847','8/4/7'),('bp848','8/4/8'),('bp8410','8/4/10'),('bp91051','9/10/51')]:
    source(k, 'Bhāgavata Purāṇa '+loc.replace('/','.'), f'https://vedabase.io/en/library/sb/{loc}/', edition='Bhaktivedanta Book Trust Sanskrit and translation; distinguish translation/purport from verse')
source('zvelebil', 'Kamil Zvelebil, Pre-history of Tamil Literature', 'https://www.tamiluniversity.ac.in/english/wp-content/uploads/2018/08/paper_01-PDF.pdf', 'scholarship', '2010 excerpts from Tamil Literature (1975)', 'printed pp. 9–11, 15')
source('mahadevan', 'Iravatham Mahadevan, Meluhha and Agastya (2009)', 'https://www.harappa.com/sites/default/files/pdf/meluhha_and_agastya_2009.pdf', 'scholarship', locator='§§4.9–4.11, pp. 13–16')
source('rvdate', 'Jamison and Brereton, The Rigveda (2020)', 'https://academic.oup.com/book/33632', 'scholarship')
source('rvdating', 'Jamison and Brereton, Dating and Authorship', 'https://academic.oup.com/book/33632/chapter-abstract/288152909', 'scholarship')
source('epicdate', 'Gregory Nagy, Homeric Questions: comparison with Sanskrit epics', 'https://www-current.chs.harvard.edu/homeric-questions-2/', 'scholarship')
source('bpdate', 'Barbara Holdrege, Mystical Cognition and Canonical Authority (2000)', 'https://academic.oup.com/book/2098/chapter-abstract/142029717', 'scholarship')
source('bpearly', 'Amarnath Ray, Bhāgavata Purāna and the Kārikās of Gaudapāda (1935)', 'https://www.cambridge.org/core/journals/bulletin-of-the-school-of-oriental-and-african-studies/article/abs/bhagavata-purana-and-the-karikas-of-gaudapada/530F523DFEF6E24819E6D38249DCB079', 'scholarship')

for k,l in [('vedic','Agastya · Vedic witnesses'),('ramayana','Agastya · Rāmāyaṇa'),('mahabharata','Agastya · Mahābhārata'),('puranic','Agastya · Bhāgavata'),('tamil','Akattiyar · Tamil traditions')]: node(k,l,'agastya_facet')
for k,l in [('rv','Ṛgveda'),('ts_text','Taittirīya Saṃhitā'),('ram','Vālmīki Rāmāyaṇa'),('mb','Mahābhārata'),('bp','Bhāgavata Purāṇa'),('tol_commentary','Tolkāppiyam commentaries'),('viracoliyam','Vīracōḻiyam'),('puram201','Puṟanāṉūṟu 201'),('akattiyam','Akattiyam · attributed lost grammar')]: node(k,l,'text')
people = [('indra','Indra','deity'),('maruts','Maruts','deity_collective'),('lopamudra','Lopāmudrā','person'),('vasistha','Vasiṣṭha','person'),('mitra','Mitra','deity'),('varuna','Varuṇa','deity'),('urvasi','Urvaśī','celestial'),('asvins','Aśvins','deity_collective'),('atri','Atri','person'),('tugras_son','Tugra’s son','person'),('rama','Rāma','person'),('lakshmana','Lakṣmaṇa','person'),('sita','Sītā','person'),('dasaratha','Daśaratha','person'),('arundhati','Arundhatī','person'),('sutikshna','Sutīkṣṇa','person'),('sugriva','Sugrīva','person'),('surya','Sūrya / Āditya','deity'),('lomasa','Lomaśa','person'),('yudhisthira','Yudhiṣṭhira','person'),('salya','Śalya','person'),('nahusha','Nahuṣa','person'),('srutarvan','Śrutarvan','person'),('vradhnasva','Vṛdhnaśva','person'),('trasadasyu','Trasadasyu · epic witness','person'),('ilvala','Ilvala','asura'),('vatapi','Vātāpi','asura'),('vidarbha_king','Unnamed Vidarbha king','person'),('dridhasyu','Dṛḍhasyu / Idhmavāha · epic witness','person'),('indradyumna','Indradyumna · Bhāgavata witness','person'),('suka','Śuka','person'),('tolkappiyar','Tolkāppiyar','person'),('naccinarkkiniyar','Nacciṉārkkiṉiyar','commentator'),('peraciriyar','Pērāciriyar','commentator'),('kapilar','Kapilar','poet'),('avalokitesvara','Avalokiteśvara','bodhisattva'),('siva','Śiva','deity'),('skanda','Skanda','deity'),('velir','Vēḷir','people_collective')]
for k,l,t in people: node(k,l,t)
for k,l in [('pancavati','Pañcavaṭī'),('godavari','Godāvarī'),('dandaka','Daṇḍaka forest'),('malaya','Malaya mountain'),('gangadvara','Gaṅgādvāra'),('vidarbha','Vidarbha'),('manimati','Maṇimati'),('vindhya','Vindhya · personified mountain'),('south','Southern region'),('ocean','Ocean · unspecified'),('potiyil','Potiyil / Pothigai'),('dvaraka','Dvārakā · commentary identification'),('pandya','Pāṇḍya / Draviḍa'),('kulacala','Kulācala · translated as Malaya Hills')]: node(k,l,'place')

claim('vedic','rv','explicitly_names','vedic','rv170','1.170.3','Agastya is named in direct address.','text')
claim('vedic','indra','addresses','vedic','rv170','1.170.3','Indra questions Agastya’s withholding of an offering.','incoming',speaker='Indra',note='Speaker identification belongs to interpretation of the dialogue; naming Agastya is explicit.')
claim('vedic','vedic','addresses','indra','rv170','1.170.2, 5','The dialogue voice appeals to Indra for accommodation with the Maruts.','outgoing',speaker='Agastya, by dialogue attribution')
claim('vedic','vedic','mentions','maruts','rv170','1.170.2, 5','The appeal concerns the Maruts.','outgoing',speaker='Agastya, by dialogue attribution')
claim('vedic','rv','explicitly_names','vedic','rv179','1.179.6','The closing stanza names Agastya and his desire for offspring.','text')
claim('vedic','lopamudra','dialogue_with','vedic','rv179','1.179.1–4','Lopāmudrā and Agastya form the marital dialogue.','incoming',status='editorial_attribution',note='Names occur in verses 4 and 6; assignment of the individual speeches is editorial/traditional.')
claim('vedic','vedic','dialogue_with','lopamudra','rv179','1.179.3–4','Agastya’s response belongs to the received dialogue interpretation.','outgoing',status='editorial_attribution')
claim('vedic','rv','explicitly_names','vedic','rv733','7.33.10','Agastya appears within the Vasiṣṭha birth hymn.','text',note='Do not silently replace the distinct name Māna in verse 13 with Agastya.')
claim('vedic','vedic','associated_with_birth_of','vasistha','rv733','7.33.10–13','The hymn connects Agastya with Vasiṣṭha’s birth imagery.','relationship',note='This does not make Vasiṣṭha the identified speaker, nor establish a historical sibling relationship.')
claim('vedic','vedic','invokes','asvins','rv180','1.180.8','The verse explicitly says Agastya roused the Aśvins with praises.','outgoing')
claim('vedic','vedic','mentions_in_attributed_hymn','atri','rv180','1.180.4','The hymn recalls aid given to Atri.','outgoing',status='editorial_attribution',note='Hymn attribution is not a statement that Agastya personally met Atri.')
claim('vedic','vedic','mentions_in_attributed_hymn','tugras_son','rv180','1.180.5','Tugra’s son is invoked as a precedent.','outgoing',status='editorial_attribution',note='Retain the wording Tugra’s son; do not automatically resolve to a unique Bhujyu.')
claim('vedic','ts_text','attributes_hymn_to','vedic','ts','7.5.5','Ritual instructions identify a hymn as Agastya’s.','text',note='This is a later Vedic attribution, not a contemporary eyewitness report.')

claim('ramayana','ram','portrays','ramayana','ram312','3.12','Agastya receives the exiled party.','text')
claim('ramayana','rama','speaks_about','ramayana','ram311','3.11','Rāma recounts Agastya’s deeds en route to his hermitage.','incoming',speaker='Rāma')
claim('ramayana','sutikshna','gives_directions_to','ramayana','ram311','3.11','Sutīkṣṇa directs the party toward Agastya.','incoming',speaker='Sutīkṣṇa')
claim('ramayana','lakshmana','requests_audience_with','ramayana','ram312','3.12','Lakṣmaṇa asks Agastya’s disciple to announce their arrival.','incoming',speaker='Lakṣmaṇa',note='The request is made to a disciple; it is not direct speech to Agastya.')
claim('ramayana','rama','asks_for_residence_advice','ramayana','ram313','3.13','Rāma asks the sage where to reside.','incoming',speaker='Rāma')
claim('ramayana','ramayana','addresses','rama','ram313','3.13','Agastya advises Rāma about residence and Sītā.','outgoing',speaker='Agastya')
claim('ramayana','ramayana','addresses','lakshmana','ram313','3.13, opening greeting','Agastya greets Lakṣmaṇa.','outgoing',speaker='Agastya')
claim('ramayana','ramayana','mentions','sita','ram313','3.13','Agastya praises Sītā’s endurance and fidelity.','outgoing',speaker='Agastya')
claim('ramayana','ramayana','claims_friendship_with','dasaratha','ram313','3.13','Agastya states his friendship with Daśaratha.','outgoing',speaker='Agastya')
claim('ramayana','ramayana','compares_sita_to','arundhati','ram313','3.13','Arundhatī is the comparison for Sītā.','outgoing',speaker='Agastya')
claim('ramayana','ramayana','recommends_residence_at','pancavati','ram313','3.13','Pañcavaṭī is specified as two yojanas away.','place_direct',speaker='Agastya',note='No conversion to modern kilometres or coordinates is assumed.')
claim('ramayana','ramayana','names_river','godavari','ram313','3.13','Godāvarī is named in the recommended surroundings.','place_direct',speaker='Agastya')
claim('ramayana','sugriva','speaks_about','ramayana','ram441','4.41','Sugrīva directs the southern search party toward Agastya.','incoming',speaker='Sugrīva')
claim('ramayana','ramayana','located_on','malaya','ram441','4.41','Sugrīva locates Agastya on Malaya.','place_association',speaker='Sugrīva',note='This is Sugrīva’s geographical statement, not a place named by Agastya himself. Modern identification requires separate evidence.')
claim('ramayana','ramayana','teaches_praise_of','surya','ram6105','6.105, Ādityahṛdaya','Agastya instructs Rāma to worship the sun.','outgoing',speaker='Agastya')

claim('mahabharata','mb','recounts_deeds_of','mahabharata','mb396','Vana §96','Agastya’s past deeds frame a pilgrimage account.','text')
claim('mahabharata','yudhisthira','asks_about','mahabharata','mb396','Vana §96','Yudhiṣṭhira asks why Agastya killed Vātāpi.','incoming',speaker='Yudhiṣṭhira',note='He asks Lomaśa, not Agastya; no meeting is asserted.')
claim('mahabharata','lomasa','narrates_deeds_of','mahabharata','mb396','Vana §§96–99','Lomaśa recounts Agastya’s earlier life.','incoming',speaker='Lomaśa')
claim('mahabharata','mahabharata','requests_marriage_from','vidarbha_king','mb397','Vana §97','Agastya asks the Vidarbha ruler for Lopāmudrā.','outgoing',speaker='Agastya')
claim('mahabharata','mahabharata','speaks_to_spouse','lopamudra','mb397','Vana §97','The spouses discuss household life and wealth.','outgoing',speaker='Agastya')
claim('mahabharata','mahabharata','practises_austerities_at','gangadvara','mb397','Vana §97','The couple goes to Gaṅgādvāra.','place_association',speaker='Lomaśa')
claim('mahabharata','mahabharata','marriage_associated_with','vidarbha','mb397','Vana §97','Lopāmudrā is given by the Vidarbha king.','place_association',speaker='Lomaśa')
for p in ['srutarvan','vradhnasva','trasadasyu']:
    claim('mahabharata','mahabharata','requests_wealth_from',p,'mb398','Vana §98','Agastya requests wealth without harm to others.','outgoing',speaker='Agastya',note='Trasadasyu is called Purukutsa’s son here; cross-text identity with a Vedic king remains untested.' if p=='trasadasyu' else '')
claim('mahabharata','mahabharata','speaks_to','ilvala','mb399','Vana §99','Agastya addresses Ilvala about Vātāpi and wealth.','outgoing',speaker='Agastya')
claim('mahabharata','mahabharata','destroys','vatapi','mb399','Vana §99','The episode recounts Vātāpi’s destruction.','relationship',speaker='Lomaśa')
claim('mahabharata','mahabharata','father_of','dridhasyu','mb399','Vana §99','The son is called Dṛḍhasyu and also Idhmavāha.','relationship',note='Keep this epic identity local to its witness; later Vedic attribution indexes may differ.')
claim('mahabharata','mahabharata','speaks_to_and_crosses','vindhya','mb3104','Vana §104','Agastya asks Vindhya to remain low until his return.','place_direct',speaker='Agastya',note='The mountain is a speaking narrative agent as well as a place.')
claim('mahabharata','mahabharata','announces_journey_to','south','mb3104','Vana §104','Agastya says he will travel south.','place_direct',speaker='Agastya')
claim('mahabharata','mahabharata','approaches','ocean','mb3104','Vana §104','Agastya accompanies the gods to the sea.','place_association',speaker='Lomaśa',note='No specific sea or shoreline is identified here.')
claim('mahabharata','salya','narrates_deeds_of','mahabharata','mb517','Udyoga §17','Śalya narrates Agastya’s report to Indra.','incoming',speaker='Śalya')
claim('mahabharata','indra','addresses','mahabharata','mb517','Udyoga §17','Indra asks Agastya how Nahuṣa fell.','incoming',speaker='Indra')
claim('mahabharata','mahabharata','reports_to','indra','mb517','Udyoga §17','Agastya tells Indra about Nahuṣa’s fall.','outgoing',speaker='Agastya')
claim('mahabharata','mahabharata','curses','nahusha','mb517','Udyoga §17','Agastya recounts cursing Nahuṣa to serpent existence.','outgoing',speaker='Agastya',note='Ganguli gives ten thousand years for the curse; this is not Agastya’s age.')

claim('puranic','bp','names','puranic','bp6185','6.18.5','Agastya and Vasiṣṭha occur together.','text',speaker='Śuka')
claim('puranic','suka','narrates_genealogy_of','puranic','bp6185','6.18.5','Śuka’s genealogical account names Agastya.','incoming',speaker='Śuka')
for p in ['mitra','varuna']:
    claim('puranic','puranic','mythic_son_of',p,'bp6185','6.18.5','The verse assigns shared Mitra–Varuṇa parentage.','relationship',note='Mythic genealogy, not independently dated biological evidence.')
claim('puranic','puranic','shares_parentage_with','vasistha','bp6185','6.18.5','The two sages share the stated parentage.','relationship')
claim('puranic','puranic','birth_story_involves','urvasi','bp6186','6.18.5–6','Urvaśī appears in the jar-birth context.','relationship',note='Do not flatten this into an ordinary mother–son relationship.')
claim('puranic','puranic','curses','indradyumna','bp8410','8.4.10','Agastya curses the silent king to elephant existence.','outgoing',speaker='Agastya')
claim('puranic','indradyumna','ruler_of','pandya','bp847','8.4.7','The king is associated with Pāṇḍya and Draviḍa.','place_association',note='Indirect geography through an associated king, not Agastya’s own place statement.')
claim('puranic','indradyumna','has_hermitage_at','kulacala','bp848','8.4.8','The king’s hermitage is on Kulācala.','place_association',note='The translation identifies this as Malaya Hills; the verse has kulācala.')

claim('tamil','tol_commentary','portrays','tamil','zvelebil','pp. 9–11, 15','Medieval commentaries elaborate Akattiyar traditions.','text','scholarly_report')
claim('tamil','naccinarkkiniyar','writes_about','tamil','zvelebil','p. 15','The commentator links Tolkāppiyar to Agastya.','incoming','scholarly_report')
claim('tamil','peraciriyar','writes_about','tamil','zvelebil','pp. 10, 15','Pērāciriyar defends the pupil tradition.','incoming','scholarly_report')
claim('tamil','tamil','traditionally_teaches','tolkappiyar','zvelebil','pp. 9, 15','Tolkāppiyar is presented as Agastya’s pupil.','relationship','scholarly_report',note='A commentary tradition; not an explicit statement in the Tolkāppiyam base text.')
claim('tamil','tamil','traditionally_authors','akattiyam','mahadevan','§4.10, p. 15','A lost Tamil grammar is attributed to Agastya.','text','scholarly_report',note='No surviving complete authorial text has been verified here.')
claim('tamil','tamil','traditionally_settles_at','potiyil','mahadevan','§4.11, p. 16','The migration account ends at Potiyil.','place_association','scholarly_report')
claim('tamil','tamil','traditionally_leads_migration_from','dvaraka','mahadevan','§4.11, p. 16','The commentary account starts the migration at Tuvarāpati.','place_association','scholarly_report',note='Dvārakā is the reported identification; not a verified migration date.')
claim('tamil','tamil','traditionally_leads','velir','mahadevan','§4.11, p. 16','The Vēḷir accompany the southern migration.','relationship','scholarly_report')
claim('tamil','viracoliyam','portrays','tamil','mahadevan','§4.10, p. 15','A Buddhist Tamil-learning tradition is reported.','text','scholarly_report')
claim('tamil','tamil','traditionally_learns_tamil_from','avalokitesvara','mahadevan','§4.10, p. 15','The Buddhist tradition makes Avalokiteśvara the teacher.','relationship','scholarly_report')
claim('tamil','tamil','alternatively_learns_tamil_from','siva','mahadevan','§4.10, p. 15','Another tradition assigns the instruction to Śiva.','relationship','scholarly_report')
claim('tamil','tamil','alternatively_learns_tamil_from','skanda','mahadevan','§4.10, p. 15','Skanda is another reported teacher.','relationship','scholarly_report')
claim('tamil','puram201','possibly_alludes_to','tamil','mahadevan','§4.9, pp. 13–14','Mahadevan identifies an unnamed northern sage with Agastya.','text','identity_hypothesis',note='The poem does not name Agastya. Its 49-generation claim concerns a Vēḷir ancestor, not an Agastya lifespan.')
claim('tamil','kapilar','possibly_alludes_to','tamil','mahadevan','§4.9, pp. 13–14','The proposed identification would make Kapilar an indirect witness.','incoming','identity_hypothesis',note='Keep separate from explicit named attestations; the identification is disputed.')

chronology = [
 dict(id='T01',facet='vedic',kind='text_composition',label='Ṛgvedic textual horizon',range='Latter half of the second millennium BCE',start=-1500,end=-1000,source='rvdate',note='Broad corpus horizon from Jamison–Brereton; not a dated birth, death, or individual hymn. Oral composition complicates finer dating.'),
 dict(id='T02',facet='vedic',kind='relative_textual',label='Later Vedic reception',range='After the hymn tradition; absolute range not assigned here',start=None,end=None,source='ts',note='Taittirīya Saṃhitā 7.5.5 already treats a hymn as Agastya’s; a date for this particular layer remains to be sourced.'),
 dict(id='T03',facet='ramayana',kind='narrative_synchronism',label='Contemporary of Rāma and Daśaratha',range='Rāma’s exile; friendship with the preceding king',start=None,end=None,source='ram313',note='Internal synchronism only. Does not independently supply a BCE year.'),
 dict(id='T04',facet='ramayana',kind='cross_text_traditional_placement',label='Tretā-yuga linkage',range='Tretā-yuga, through the Rāma synchronism',start=None,end=None,source='bp91051',note='Bhāgavata 9.10.51 puts Rāma’s reign in Tretā. Linking Agastya to it combines two texts; it is not an explicit birth date for Agastya.'),
 dict(id='T05',facet='ramayana',kind='text_formation',label='Rāmāyaṇa formative period · Nagy synthesis',range='Approximately 200 BCE–200 CE',start=-200,end=200,source='epicdate',note='Broad scholarly model of epic formation; individual Agastya passages may have different histories. Earlier oral material and later growth are not excluded.'),
 dict(id='T06',facet='mahabharata',kind='narrative_order',label='Past deeds in Yudhiṣṭhira’s narrative present',range='Earlier than Lomaśa’s account to the Pāṇḍavas',start=None,end=None,source='mb396',note='The pilgrimage story establishes earlier deeds, not a meeting or a dated death. In §104 Agastya has not returned from the south as of the narrator’s present.'),
 dict(id='T07',facet='mahabharata',kind='narrative_duration',label='Nahuṣa’s curse',range='10,000 years in Ganguli’s Udyoga §17',start=None,end=None,source='mb517',note='The duration belongs to Nahuṣa’s serpent curse. It is not Agastya’s age and is not used as a calendar anchor.'),
 dict(id='T08',facet='mahabharata',kind='text_formation',label='Mahābhārata formative period · Nagy synthesis',range='Approximately 400 BCE–400 CE',start=-400,end=400,source='epicdate',note='Broad corpus formation, not the date of the war or the date of Agastya.'),
 dict(id='T09',facet='puranic',kind='text_composition',label='Bhāgavata · Holdrege’s dating',range='9th or early 10th century CE',start=800,end=950,source='bpdate',note='Numeric endpoints are visualization approximations to the source’s century wording. Applies to text, not narrated persons.'),
 dict(id='T10',facet='puranic',kind='alternative_text_dating',label='Bhāgavata · Ray’s older proposal',range='550–650 CE; published in 1935',start=550,end=650,source='bpearly',note='Historical alternative in the dating literature; not represented as equal to a current consensus or as Agastya’s lifetime.'),
 dict(id='T11',facet='tamil',kind='commentary_attestation',label='Nacciṉārkkiṉiyar commentary witness',range='14th century CE in Zvelebil’s account',start=1300,end=1400,source='zvelebil',note='Dates this witness to the disciple tradition, not the origin of every Tamil Agastya tradition and not the life of Tolkāppiyar or Agastya.'),
 dict(id='T12',facet='tamil',kind='interpretive_hypothesis',label='Indus cultural-memory hypothesis · Mahadevan',range='Post-Indus migration interpretation; no individual lifespan',start=None,end=None,source='mahadevan',note='A modern interpretation of legends and undeciphered signs; no independently read Agastya inscription or secure absolute date is established.'),
]

data = dict(schema_version='0.1', title='Agastya evidence graph', as_of='2026-10-27',
 scope='Curated first-pass seed, not an exhaustive concordance. Translation checks and scholarly reports only; original-language philological review is pending.',
 identity_policy='The five Agastya facets are source-local dossiers. Their labels organize traditions; neither one historical individual nor five separate people is asserted.',
 status_definitions=dict(translation_checked='Claim inspected in an accessible primary-text translation; does not certify historical truth.', editorial_attribution='Speaker or hymn-author identification depends on editorial/traditional interpretation.', scholarly_report='Scholarship reports the tradition; underlying primary passage has not been checked in this pass.',identity_hypothesis='Proposed identification; exclude from explicit named-attestation counts.'),
 nodes=list(nodes.values()),sources=list(sources.values()),claims=claims,chronology=chronology,
 open_work=[
 'Align all epic passages to the Sanskrit and the critical apparatus; preserve current edition-specific numbering.',
 'Audit the full Ṛgveda 1.165–191 attribution block and its named persons/places against an Anukramaṇī and a modern translation.',
 'Check Aitareya Āraṇyaka 1.2.2, Kāṭhaka Saṃhitā 10.11, Maitrāyaṇī Saṃhitā 2.1, Aitareya Brāhmaṇa 5.16, Taittirīya Brāhmaṇa 2.7.11, Pañcaviṃśa Brāhmaṇa 21.14; citations are leads, not verified graph edges.',
 'Read Tamil primary witnesses: Paripāṭal, Cilappatikāram, Maṇimēkalai, Vīracōḻiyam, Iraiyaṉār Akapporuḷ commentary, and Tolkāppiyam commentaries; source each date and variant.',
 'Expand Purāṇic coverage beyond Bhāgavata and distinguish unrelated works called Agastyasaṃhitā.',
 'Add Agastya/Canopus as a separate celestial entity after checking astronomical texts; do not infer a human lifespan from stellar visibility.',
 'Investigate whether the epic Trasadasyu is identifiable with Vedic attestations, without automatic name merging.',
 'Review manuscript witnesses, inscriptions, regional geography, Buddhist Akitti traditions, and Southeast Asian reception.'
 ])
for c in claims:
    assert c['subject'] in nodes and c['object'] in nodes and c['source'] in sources
for t in chronology: assert t['source'] in sources
(OUT/'graph.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
with (OUT/'claims.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(claims[0]));w.writeheader();w.writerows(claims)
with (OUT/'chronology.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(chronology[0]));w.writeheader();w.writerows(chronology)
print(f'{len(nodes)} nodes, {len(claims)} claims, {len(sources)} sources, {len(chronology)} chronology records')
