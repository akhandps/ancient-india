# Computed experiment results

Input SHA-256: `f91663fa2b6fc4449de4a8fb86a0eb61f49703a7fa41f8c6d9f3daab2ee26bea`. Seed 42 unless stated otherwise.

Textual entities include deities and collectives. All structural edges are undirected; claims retain their directions in the evidence export.

| Variant | Edges | Active records | Largest component | Within 3 links of any Agastya facet |
|---|---:|---:|---:|---:|
| baseline | 3730 | 3155 | 2855 | 1247 |
| checked_only | 3708 | 3142 | 2839 | 1114 |
| no_attendance | 3014 | 2561 | 2215 | 503 |
| no_kinship | 1358 | 1314 | 1106 | 841 |
| no_attendance_or_kinship | 638 | 661 | 425 | 273 |
| no_narration | 3716 | 3150 | 2846 | 831 |
| no_secondary_identity | 3729 | 3155 | 2855 | 1239 |

## Bridge candidates by exact betweenness

Scores use the same original record universe for normalization. Compare ranks and structure as well as scores; ablation changes component sizes.

### baseline

| Record | Degree | Betweenness |
|---|---:|---:|
| Arjuna · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 136 | 0.232112 |
| Indra | 100 | 0.231654 |
| Yudhiṣṭhira | 198 | 0.227493 |
| Agastya · Mahābhārata | 14 | 0.107915 |
| Nahuṣa · Viṣṇu Purāṇa witness | 8 | 0.100313 |
| Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness | 59 | 0.099377 |
| Nahuṣa | 2 | 0.098710 |
| Pṛthu · born from Vena’s arm and husband of Arci | 22 | 0.096648 |
| Yama · host of the assembly described in MB 2 Section VIII · Mahābhārata Sabha Parva §VIII | 125 | 0.089172 |
| Draupadī · Viṣṇu Purāṇa 4.20 witness | 130 | 0.088807 |

### checked_only

| Record | Degree | Betweenness |
|---|---:|---:|
| Arjuna · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 136 | 0.225065 |
| Yudhiṣṭhira | 198 | 0.210132 |
| Indra | 100 | 0.181651 |
| Tapatī · daughter of the Sun and wife of Saṃvaraṇa | 7 | 0.111641 |
| Saṃvaraṇa · Ṛkṣa branch · Viṣṇu Purāṇa 4.19 witness | 5 | 0.111560 |
| Pṛthu · born from Vena’s arm and husband of Arci | 22 | 0.104480 |
| Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness | 59 | 0.096395 |
| Yama · host of the assembly described in MB 2 Section VIII · Mahābhārata Sabha Parva §VIII | 125 | 0.093151 |
| Vasiṣṭha · sage in the Tapatī and Kalmāṣapāda accounts | 4 | 0.090518 |
| Draupadī · Viṣṇu Purāṇa 4.20 witness | 130 | 0.089723 |

### no_attendance

| Record | Degree | Betweenness |
|---|---:|---:|
| Indra | 23 | 0.158757 |
| Agastya · Mahābhārata | 14 | 0.084204 |
| Jāmbavant · Viṣṇu Purāṇa 4.13 witness · bear king | 6 | 0.080157 |
| Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness | 58 | 0.079663 |
| Nahuṣa · Viṣṇu Purāṇa witness | 8 | 0.076447 |
| Skanda | 21 | 0.075966 |
| Yudhiṣṭhira | 36 | 0.075777 |
| Nahuṣa | 2 | 0.074673 |
| Sūrya / Āditya | 4 | 0.070272 |
| Tapatī · daughter of the Sun and wife of Saṃvaraṇa | 7 | 0.068384 |

### no_attendance_or_kinship

| Record | Degree | Betweenness |
|---|---:|---:|
| Indra | 19 | 0.009728 |
| Yudhiṣṭhira | 31 | 0.006615 |
| Agastya · Mahābhārata | 12 | 0.006242 |
| Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness | 32 | 0.003674 |
| Jāmbavant · Viṣṇu Purāṇa 4.13 witness · bear king | 3 | 0.003233 |
| Maṇimēkalai · heroine of the Tamil epic | 24 | 0.003038 |
| Kṛpa · Satyadhṛti episode · Viṣṇu Purāṇa 4.19 witness | 6 | 0.002974 |
| Śiva | 13 | 0.002809 |
| Pṛthu · born from Vena’s arm and husband of Arci | 15 | 0.002693 |
| Abhimanyu · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 31 | 0.002667 |

## Claim-removal sensitivity

Number of baseline records within three links that move beyond three links or become unreachable when this single claim is removed. Parallel support can preserve an edge.

| Claim | Description | Records lost from 3-link neighborhood |
|---|---|---:|
| C030 | Yudhiṣṭhira → asks_about → Agastya · Mahābhārata | 401 |
| C068 | Akattiyar · Tamil traditions → alternatively_learns_tamil_from → Śiva | 85 |
| SB4_0072 | Agastya · Bhāgavata → is_child_of → Pulastya · Mahābhārata Sabha Parva §XI Brahmā-assembly roster | 26 |
| C069 | Akattiyar · Tamil traditions → alternatively_learns_tamil_from → Skanda | 15 |
| RFX008 | Nahuṣa → corresponds_to_puranic_witness → Nahuṣa · Viṣṇu Purāṇa witness | 8 |
| C026 | Sugrīva → speaks_about → Agastya · Rāmāyaṇa | 7 |
| C022 | Agastya · Rāmāyaṇa → claims_friendship_with → Daśaratha | 6 |
| C028 | Agastya · Rāmāyaṇa → teaches_praise_of → Sūrya / Āditya | 6 |
| TEX_007 | King Kānthan · Maṇimēkalai witness → plans_to_seek_audience_with → Akattiyar · Tamil traditions | 5 |
| C021 | Agastya · Rāmāyaṇa → mentions → Sītā | 3 |
| PSC002 | Agastya · Bhāgavata → father_of → Dṛḍhacyuta · Bhāgavata witness | 2 |
| REX002 | Udāyin · Buddhacarita witness → cites_as_precedent → Agastya · Buddhacarita reception | 2 |

## Recurring typed relations across source families

Families group editions of the same work; recurrence is not independent historical corroboration.

- Daśaratha → parent → Rāma: Mahabharata, Ramayana, Vishnu Purana. Claims: EEX003, VSG040, MB2EARLY_202.
- Tapatī · daughter of the Sun and wife of Saṃvaraṇa → spouse → Saṃvaraṇa · Ṛkṣa branch · Viṣṇu Purāṇa 4.19 witness: Bhagavata, Mahabharata. Claims: MBAPE140, SB6L207, MBALM137.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Aryamā · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI023, SB6L182.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Bhaga · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI027, SB6L186.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Dhātā · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI021, SB6L187.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Mitra · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI022, SB6L190.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Savitṛ · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI030, SB6L185.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Tvaṣṭṛ · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI031, SB6L184.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Varuṇa · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI025, SB6L189.
- Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Vivasvat · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI028, SB6L181.
- Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Aditi · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI008, SB6L106.
- Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Danu · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI010, SB6L112.
- Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Diti · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI009, SB6L109.
- Siṃhikā · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Rāhu · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI084, SB6L180.
- Vinatā · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Aruṇa · Vinatā line · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI099, SB6L105.
- Vinatā · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Garuḍa · Vinatā line · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI098, SB6L104.
- Virocana · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness: Bhagavata, Mahabharata. Claims: MBAI042, SB8P038.
- Vivasvat · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness → parent → Yama · son of Vivasvat: Bhagavata, Mahabharata. Claims: MBANI015, SB6L199.
- Nahuṣa · son of Āyu → parent → Yayāti · son of Nahuṣa; father of the five named sons: Bhagavata, Mahabharata. Claims: MBANI045, SB6L167.
- Śāṃtanu · Viṣṇu Purāṇa 4.19 witness → parent → Bhīṣma · Gaṅgā branch · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA028, MBAR006.
- Śāṃtanu · Viṣṇu Purāṇa 4.19 witness → parent → Citrāṅgada · Śāṃtanu’s son · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA030, MBAR002.
- Śāṃtanu · Viṣṇu Purāṇa 4.19 witness → parent → Vicitravīrya · Śāṃtanu’s son · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA032, MBAR004.
- Ambālikā · Viṣṇu Purāṇa 4.20 witness → spouse → Vicitravīrya · Śāṃtanu’s son · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA036, MBAR009.
- Ambikā (ANU; Sanskrit variant Ambā) · Viṣṇu Purāṇa 4.20 witness → spouse → Vicitravīrya · Śāṃtanu’s son · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA035, MBAR008.
- Dhṛtarāṣṭra · Viṣṇu Purāṇa 4.20 witness → parent → Duryodhana · Dhṛtarāṣṭra branch · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA042, MBAR028.
- Dhṛtarāṣṭra · Viṣṇu Purāṇa 4.20 witness → parent → Duḥśāsana · Dhṛtarāṣṭra branch · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA044, MBAR030.
- Gaṅgā · Viṣṇu Purāṇa 4.20 witness → parent → Bhīṣma · Gaṅgā branch · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA029, MBAR007.
- Kuntī · Viṣṇu Purāṇa 4.20 witness → spouse → Pāṇḍu · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA046, MBAR023, MBAL004.
- Mādrī · Viṣṇu Purāṇa 4.20 witness → spouse → Pāṇḍu · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA047, MBAR024, MBAL005, MBAL024.
- Satyavatī · Viṣṇu Purāṇa 4.20 witness → parent → Citrāṅgada · Śāṃtanu’s son · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA031, MBAR003.
- Satyavatī · Viṣṇu Purāṇa 4.20 witness → parent → Kṛṣṇa-Dvaipāyana · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA037, MBAR012, MBAL025.
- Satyavatī · Viṣṇu Purāṇa 4.20 witness → parent → Vicitravīrya · Śāṃtanu’s son · Viṣṇu Purāṇa 4.20 witness: Mahabharata, Vishnu Purana. Claims: GKA033, MBAR005.
- Duṣyanta · Puru-line witness → parent → Bharata · Puru-line witness: Mahabharata, Vishnu Purana. Claims: GSC034, MBANI004.

## Motifs and audit queues

- multiple_parent_records: 12
- parent_cycles: 0
- teaching_chains: 8
- parent_spouse_triangles: 198
- killing_within_two_family_steps: 0
- narrator_intermediaries: 2

No parent cycles were found with the explicit parent predicate set; this is not a validation of every genealogical claim.

## Community stability

- baseline: runs [{'seed': 7, 'communities': 88, 'modularity': 0.9031717327084936}, {'seed': 19, 'communities': 88, 'modularity': 0.9035213722516514}, {'seed': 42, 'communities': 88, 'modularity': 0.9036276405350431}]; adjusted Rand comparisons [{'seeds': [7, 19], 'score': 0.9238162878310182}, {'seeds': [7, 42], 'score': 0.8999394353577816}, {'seeds': [19, 42], 'score': 0.895274577132473}].
- no_attendance_or_kinship: runs [{'seed': 7, 'communities': 107, 'modularity': 0.8819648490089523}, {'seed': 19, 'communities': 106, 'modularity': 0.8814538477412761}, {'seed': 42, 'communities': 107, 'modularity': 0.8811320152121146}]; adjusted Rand comparisons [{'seeds': [7, 19], 'score': 0.968752374989436}, {'seeds': [7, 42], 'score': 0.9377874331047634}, {'seeds': [19, 42], 'score': 0.9076612625794229}].

## Identity sensitivity

- merge_agastya_facets: 5 records collapsed; 0 previously reachable records get shorter paths; 0 previously unreachable records become reachable; 1247 original non-root records are within three links.
- merge_exact_base_labels_UNSAFE: 854 records collapsed; 1669 previously reachable records get shorter paths; 277 previously unreachable records become reachable; 2387 original non-root records are within three links.

The base-label merge is an intentionally unsafe stress test. It is not an identity proposal and must not be used as a historical result.

## Semantic exclusions

- MBAPE128: Predicate says father; summary and note explicitly deny parentage and describe teaching.
