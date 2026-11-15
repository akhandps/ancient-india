# Maximum-weight independent sets

Input: commit `bc7f074adeb3844790af1aca99e54bddb7bfaa99`, SHA-256 `eaf34175dcf95509e2f7977c880806cb6468ee3b3ee41a08ff6634c5e59101a9`.

Each selected record is nonadjacent to every other selected record in the specified conflict graph. An independent set is not evidence of unrelated cultures, independent testimonies, or historical separation.

The solver uses binary variables and one at-most-one constraint per edge. It maximizes positive integer weights by minimizing their negative sum. A zero requested relative MIP gap is used. A time-limited feasible solution would be labeled nonoptimal. See [SciPy MILP documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html).

| Model | Candidates | Conflicts | Size cap | Selected | Weight | Optimal | Gap |
|---|---:|---:|---:|---:|---:|---|---:|
| uniform | 3238 | 3752 | None | 2455 | 2455 | True | 0.0 |
| degree | 3238 | 3752 | None | 2433 | 5852 | True | 0.0 |
| source_diversity | 3238 | 3752 | None | 2455 | 4894 | True | 0.0 |
| bridge | 3238 | 3752 | None | 1591 | 40454 | True | 0.0 |
| hubs_distance_1 | 193 | 262 | None | 110 | 18097 | True | 0.0 |
| hubs_distance_2 | 193 | 1165 | None | 54 | 10085 | True | 0.0 |
| hubs_distance_2_budget_10 | 193 | 1165 | 10 | 10 | 7748 | True | 0.0 |

## Weights

- uniform: `1`
- degree: `1 + original degree`
- source_diversity: `1 + number of incident passage-checked source families`
- bridge: `1 + round(10000 * exact normalized original-graph betweenness)`

## How the models differ

The four full-graph models share the same person-like universe, including deities, collectives and Agastya facets. Texts, places and objects are excluded; identity hypotheses are excluded, while other explicit identity and comparison claims remain conflict edges. Multiple claims per pair collapse to one undirected edge. No source-local dossiers are merged. All positive-weight isolates are necessarily selected.

The two hub models use every original record of degree at least five. This is an explicit exploratory candidate filter, not a discovered natural threshold. Their weights are the bridge weights computed on the full original graph. `hubs_distance_1` forbids only direct adjacency. `hubs_distance_2` also forbids sharing an original-graph neighbor, including neighbors outside the candidate pool. Thus distance two is measured before restricting candidates, rather than in the induced hub subgraph.

`hubs_distance_2_budget_10` adds a cap of ten selected records to that stricter conflict graph. This is a cardinality-constrained MWIS variant for a readable research shortlist, not the unconstrained optimum. Its membership-exclusion tests retain the same cap.

Integer rounding defines the bridge objective: certified optimality applies to that integerized score, not to an unrounded real-valued centrality sum. Source families group editions of the same work and do not establish independent testimony. Claim `facet` tags are not used as source families.

Different optimal sets may tie. For each selected record in a hub model, we forbid it and resolve the same problem. A strictly lower certified optimum marks that record mandatory for every optimum under that exact model. An equal optimum marks it optional. This is conditional optimizer stability, not robustness to other weights, missing passages or identity changes.

## hubs_distance_1: selected set

| Record | Weight | Original degree | Source families | Membership |
|---|---:|---:|---|---|
| Arjuna · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 2318 | 136 | Mahabharata | mandatory |
| Agastya · Mahābhārata | 1031 | 14 | Mahabharata | mandatory |
| Nahuṣa · Viṣṇu Purāṇa witness | 948 | 8 | Vishnu Purana | mandatory |
| Yama · host of the assembly described in MB 2 Section VIII · Mahābhārata Sabha Parva §VIII | 932 | 125 | Bhagavata, Mahabharata | mandatory |
| Jāmbavant · linked Rāmāyaṇa, Viṣṇu Purāṇa and Bhāgavata witnesses | 904 | 13 | Bhagavata, Ramayana, Vishnu Purana | mandatory |
| Saṃvaraṇa · Ṛkṣa branch · Viṣṇu Purāṇa 4.19 witness | 665 | 5 | Bhagavata, Mahabharata, Vishnu Purana | mandatory |
| Kadrū · mother in Ādiparvan serpent genealogy | 664 | 78 | Mahabharata | mandatory |
| Vasudeva / Ānakadundubhi · Viṣṇu Purāṇa 4.14 witness | 588 | 57 | Bhagavata, Mahabharata, Vishnu Purana | mandatory |
| Dhṛtarāṣṭra · Viṣṇu Purāṇa 4.20 witness | 521 | 107 | Mahabharata, Vishnu Purana | mandatory |
| Danu · Mahābhārata Ādiparvan 1.59–1.61 witness | 430 | 55 | Bhagavata, Mahabharata | mandatory |
| Karṇa · Viṣṇu Purāṇa witness · Viṣṇu Purāṇa 4.18 witness | 410 | 11 | Mahabharata, Vishnu Purana | mandatory |
| Yadu · Viṣṇu Purāṇa witness | 372 | 6 | Vishnu Purana | mandatory |
| Dharma · deity · Viṣṇu Purāṇa 4.20 witness | 362 | 33 | Bhagavata, Mahabharata, Ramayana, Vishnu Purana | mandatory |
| Varuṇa | 342 | 51 | Bhagavata, Mahabharata, Manimekalai, Vedic | mandatory |
| Daśaratha | 340 | 6 | Mahabharata, Ramayana, Vishnu Purana | mandatory |
| Vivasvat · Āditya · Mahābhārata Ādiparvan 1.59–1.61 witness | 337 | 22 | Bhagavata, Mahabharata | mandatory |
| Ajamīḍha · Hastin branch · Viṣṇu Purāṇa 4.19 witness | 337 | 6 | Vishnu Purana | mandatory |
| Kubera / Vaiśravaṇa · host of the assembly described in MB 2 Section X | 335 | 61 | Bhagavata, Mahabharata | mandatory |
| Brahmā · host of the assembly described in MB 2 Section XI | 331 | 38 | Bhagavata, Mahabharata | mandatory |
| Sītā | 310 | 5 | Ramayana, Vishnu Purana | mandatory |
| Satrājita · son of Nighna · Viṣṇu Purāṇa 4.13 witness | 307 | 8 | Bhagavata, Vishnu Purana | mandatory |
| Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness | 289 | 34 | Bhagavata, Mahabharata | mandatory |
| Kṛpa · Satyadhṛti episode · Viṣṇu Purāṇa 4.19 witness | 273 | 6 | Mahabharata, Vishnu Purana | mandatory |
| Skanda | 272 | 22 | Mahabharata | mandatory |
| Vishnu / Nārāyaṇan · deity described in Maṇimēkalai canto 27 | 201 | 17 | Bhagavata, Manimekalai | mandatory |
| Ugrasena · Viṣṇu Purāṇa 4.14 witness | 196 | 21 | Bhagavata, Vishnu Purana | mandatory |
| Prava · Mahābhārata Ādiparvan 1.59–1.61 witness | 191 | 35 | Mahabharata | mandatory |
| Dharma · deity · Mahābhārata Ādiparvan 1.59–1.61 witness | 179 | 20 | Mahabharata | mandatory |
| Sātvata · Viṣṇu Purāṇa 4.13 witness | 165 | 8 | Vishnu Purana | mandatory |
| Śaśabindu · Kroṣṭu line | 164 | 7 | Vishnu Purana | mandatory |
| Uparicara Vasu · Kṛtaka branch · Viṣṇu Purāṇa 4.19 witness | 160 | 6 | Vishnu Purana | mandatory |
| Vasu · daughter of Dakṣa and wife of Yamarāja · Śrīmad-Bhāgavatam 6.6–6.7 witness | 157 | 11 | Bhagavata | mandatory |
| Śvaphalka · Viṣṇu Purāṇa 4.14 witness | 139 | 12 | Bhagavata, Vishnu Purana | mandatory |
| Anu · Viṣṇu Purāṇa witness | 135 | 5 | Vishnu Purana | mandatory |
| Nahuṣa · son of Āyu | 129 | 7 | Bhagavata, Mahabharata | mandatory |
| Dhṛṣṭadyumna · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 128 | 7 | Mahabharata | mandatory |
| Dhruva · son of Uttānapāda and Sunīti | 118 | 8 | Bhagavata | mandatory |
| Senajit · Viṣṇu Purāṇa 4.19 witness | 118 | 5 | Vishnu Purana | mandatory |
| Parāśara | 117 | 5 | Mahabharata | mandatory |
| Ulmuka · son of Cākṣuṣa and Naḍvalā | 104 | 9 | Bhagavata | mandatory |
| Parāvṛt · Kroṣṭu line | 104 | 6 | Vishnu Purana | mandatory |
| Agastya · Vedic witnesses | 99 | 15 | Brihaddevata, Vedic | mandatory |
| Dhanaka · Viṣṇu Purāṇa 4.11 witness | 96 | 5 | Vishnu Purana | mandatory |
| Bhīma / Bhīmasena · Pāṇḍu’s son · Viṣṇu Purāṇa 4.20 witness | 84 | 7 | Mahabharata, Vishnu Purana | mandatory |
| Pṛthā · Viṣṇu Purāṇa 4.14 witness · Vasudeva’s sister | 79 | 7 | Vishnu Purana | mandatory |
| Kārtavīrya Arjuna · son of Kṛtavīrya · Viṣṇu Purāṇa 4.11 witness | 68 | 6 | Vishnu Purana | mandatory |
| Bhavanmanyu · Viṣṇu Purāṇa 4.19 witness | 67 | 5 | Vishnu Purana | mandatory |
| Vidarbha · son of Jyāmagha and Śaibyā · Viṣṇu Purāṇa 4.12 witness | 66 | 5 | Vishnu Purana | mandatory |
| Vijitāśva / Antardhāna · eldest son of Pṛthu; source explicitly gives title Antardhāna | 65 | 11 | Bhagavata | mandatory |
| Vinatā · Mahābhārata Ādiparvan 1.59–1.61 witness | 63 | 8 | Bhagavata, Mahabharata | mandatory |
| Manu · son of Mārtaṇḍa | 61 | 11 | Mahabharata | mandatory |
| Virāṭa · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 58 | 9 | Mahabharata | mandatory |
| Raudrāśva · Puru-line witness | 55 | 11 | Vishnu Purana | mandatory |
| Uśīnara · Viṣṇu Purāṇa 4.18 witness | 51 | 6 | Vishnu Purana | mandatory |
| Udayakumaran · Maṇimēkalai witness | 49 | 8 | Manimekalai | mandatory |
| Puṣpārṇa · son of Vatsara and Svarvīthi | 47 | 10 | Bhagavata | mandatory |
| Parīkṣit · Abhimanyu’s son · Viṣṇu Purāṇa 4.20 witness | 47 | 9 | Vishnu Purana | mandatory |
| Sugrīva | 42 | 12 | Ramayana | mandatory |
| Hiraṇyakaśipu · Mahābhārata Ādiparvan 1.59–1.61 witness | 38 | 7 | Mahabharata | mandatory |
| Bhīmasena · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 36 | 13 | Mahabharata | mandatory |
| Svāyambhuva Manu · Canto 4 genealogy witness | 36 | 6 | Bhagavata | mandatory |
| Kuśa · Amāvasu branch | 36 | 5 | Vishnu Purana | mandatory |
| Anāyus · Mahābhārata Ādiparvan 1.59–1.61 witness | 35 | 5 | Mahabharata | mandatory |
| Dambha · child of Adharma and Mṛṣā | 32 | 5 | Bhagavata | mandatory |
| Māyā · child of Adharma and Mṛṣā | 32 | 5 | Bhagavata | mandatory |
| Haryaśva · Nīla branch · Viṣṇu Purāṇa 4.19 witness | 32 | 6 | Vishnu Purana | mandatory |
| Śarmiṣṭhā · daughter of Vṛṣaparvan; mother of Druhyu, Anu, and Pūru by Yayāti | 31 | 6 | Bhagavata, Mahabharata | mandatory |
| Lakshmi · Maṇimēkalai past-birth name | 29 | 5 | Manimekalai | mandatory |
| Punniyarājan · king in Maṇimēkalai | 29 | 6 | Manimekalai | mandatory |
| Bhīṣma · Gaṅgā branch · Viṣṇu Purāṇa 4.20 witness | 29 | 6 | Mahabharata, Vishnu Purana | mandatory |
| Somadatta · Bāhlīka branch · Viṣṇu Purāṇa 4.20 witness | 28 | 7 | Mahabharata, Vishnu Purana | mandatory |
| Svāhā · daughter of Dakṣa and wife of Agni | 26 | 5 | Bhagavata | mandatory |
| Urvaśī · Purūravas’s consort | 26 | 6 | Vishnu Purana | mandatory |
| Purūravas · Viṣṇu Purāṇa 4.8–9 witness | 26 | 6 | Vishnu Purana | mandatory |
| Arundhatī | 24 | 10 | Bhagavata, Mahabharata, Ramayana | mandatory |
| Nakula · Viṣṇu Purāṇa 4.20 witness | 24 | 7 | Mahabharata, Vishnu Purana | mandatory |
| Kālakā · mother of eight kings · Mahābhārata Ādiparvan 1.59–1.61 witness | 23 | 7 | Mahabharata | mandatory |
| Dīrghatamas · Viṣṇu Purāṇa 4.18 witness | 23 | 5 | Vishnu Purana | mandatory |
| Parīkṣit · Kuru branch · Viṣṇu Purāṇa 4.19 witness | 23 | 5 | Vishnu Purana | mandatory |
| Devaka · Viṣṇu Purāṇa 4.14 witness | 23 | 5 | Vishnu Purana | mandatory |
| Pīḷivaḷai · Maṇimēkalai witness | 22 | 6 | Manimekalai | mandatory |
| Marutvatī · daughter of Dakṣa and wife of Yamarāja · Śrīmad-Bhāgavatam 6.6–6.7 witness | 21 | 5 | Bhagavata | mandatory |
| Mādhavi · Maṇimēkalai witness | 21 | 7 | Manimekalai | mandatory |
| Sahadeva · Pāṇḍu’s son · Viṣṇu Purāṇa 4.20 witness | 20 | 8 | Mahabharata, Vishnu Purana | mandatory |
| Drupada / Yajñasena · king of Pāñcāla | 19 | 6 | Mahabharata | mandatory |
| Viśravā · son of Pulastya and Havirbhū | 19 | 8 | Bhagavata | mandatory |
| Lakṣmaṇa | 18 | 5 | Ramayana, Vishnu Purana | mandatory |
| Śūrpaṇakhā · Rāmāyaṇa witness | 18 | 6 | Ramayana | mandatory |
| Purūravas · child of Ilā; partner of Urvaśī | 17 | 6 | Mahabharata | mandatory |
| Durukti · Harsh Speech, sister of Kali | 12 | 5 | Bhagavata | optional |
| Urvaśī · partner of Purūravas and mother of their six sons | 11 | 5 | Mahabharata | mandatory |
| Devayānī · daughter of Śukra and wife of Yayāti | 9 | 5 | Mahabharata | mandatory |
| Nakula · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 5 | 5 | Mahabharata | mandatory |
| Sahadeva · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 5 | 5 | Mahabharata | mandatory |
| Somadatta · named attendee at Draupadī’s svayaṃvara (BORI CE Ādiparvan 1.177) | 3 | 5 | Mahabharata | mandatory |
| Brahmā · creator · Mahābhārata Ādiparvan 1.59–1.61 witness | 2 | 7 | Bhagavata, Mahabharata | mandatory |
| Sthāṇu (Śiva) · Rudra progenitor · Mahābhārata Ādiparvan 1.59–1.61 witness | 1 | 11 | Mahabharata | mandatory |
| Havirdhānī · wife of Havirdhāna | 1 | 7 | Bhagavata | mandatory |
| Śraddhā · wife of Aṅgirā; distinct from Dakṣa’s daughter of the same name | 1 | 7 | Bhagavata | optional |
| Dhiṣaṇā · Śrīmad-Bhāgavatam 6.6–6.7 witness | 1 | 5 | Bhagavata | mandatory |
| Sarūpā · Śrīmad-Bhāgavatam 6.6–6.7 witness | 1 | 12 | Bhagavata | mandatory |
| Brahma-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 8 | Bhagavata | mandatory |
| Dakṣa-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 5 | Bhagavata | mandatory |
| Deva-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 5 | Bhagavata | mandatory |
| Indra-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 9 | Bhagavata | mandatory |
| Rudra-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 7 | Bhagavata | mandatory |
| Svārociṣa Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 7 | Bhagavata | mandatory |
| Tāmasa Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 8 | Bhagavata | optional |
| Dharma · Vindhyaśakti branch · Viṣṇu Purāṇa 4.24 future-dynasty witness | 1 | 7 | Vishnu Purana | mandatory |
| Viśvāmitra · son of Satyavatī’s unnamed mother | 1 | 6 | Vishnu Purana | mandatory |

## hubs_distance_2: selected set

| Record | Weight | Original degree | Source families | Membership |
|---|---:|---:|---|---|
| Yudhiṣṭhira | 2556 | 198 | Mahabharata, Vishnu Purana | mandatory |
| Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness | 980 | 59 | Bhagavata, Mahabharata | mandatory |
| Nahuṣa · Viṣṇu Purāṇa witness | 948 | 8 | Vishnu Purana | mandatory |
| Rāma | 709 | 29 | Mahabharata, Manimekalai, Ramayana, Vishnu Purana | mandatory |
| Tapatī · daughter of the Sun and wife of Saṃvaraṇa | 695 | 7 | Bhagavata, Mahabharata | mandatory |
| Kadrū · mother in Ādiparvan serpent genealogy | 664 | 78 | Mahabharata | mandatory |
| Ajamīḍha · Hastin branch · Viṣṇu Purāṇa 4.19 witness | 337 | 6 | Vishnu Purana | mandatory |
| Satrājita · son of Nighna · Viṣṇu Purāṇa 4.13 witness | 307 | 8 | Bhagavata, Vishnu Purana | mandatory |
| Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness | 289 | 34 | Bhagavata, Mahabharata | mandatory |
| Maṇimēkalai · heroine of the Tamil epic | 263 | 27 | Manimekalai | mandatory |
| Dharma · deity · Mahābhārata Ādiparvan 1.59–1.61 witness | 179 | 20 | Mahabharata | mandatory |
| Sātvata · Viṣṇu Purāṇa 4.13 witness | 165 | 8 | Vishnu Purana | mandatory |
| Śaśabindu · Kroṣṭu line | 164 | 7 | Vishnu Purana | mandatory |
| Uparicara Vasu · Kṛtaka branch · Viṣṇu Purāṇa 4.19 witness | 160 | 6 | Vishnu Purana | mandatory |
| Nahuṣa · son of Āyu | 129 | 7 | Bhagavata, Mahabharata | mandatory |
| Dhruva · son of Uttānapāda and Sunīti | 118 | 8 | Bhagavata | mandatory |
| Senajit · Viṣṇu Purāṇa 4.19 witness | 118 | 5 | Vishnu Purana | mandatory |
| Parāśara | 117 | 5 | Mahabharata | mandatory |
| Vasiṣṭha | 110 | 15 | Bhagavata, Vedic | mandatory |
| Ulmuka · son of Cākṣuṣa and Naḍvalā | 104 | 9 | Bhagavata | mandatory |
| Parāvṛt · Kroṣṭu line | 104 | 6 | Vishnu Purana | mandatory |
| Dhanaka · Viṣṇu Purāṇa 4.11 witness | 96 | 5 | Vishnu Purana | mandatory |
| Pṛthā · Viṣṇu Purāṇa 4.14 witness · Vasudeva’s sister | 79 | 7 | Vishnu Purana | mandatory |
| Upamadgu · Viṣṇu Purāṇa 4.14 witness | 68 | 13 | Vishnu Purana | mandatory |
| Bhavanmanyu · Viṣṇu Purāṇa 4.19 witness | 67 | 5 | Vishnu Purana | mandatory |
| Vijitāśva / Antardhāna · eldest son of Pṛthu; source explicitly gives title Antardhāna | 65 | 11 | Bhagavata | mandatory |
| Manu · son of Mārtaṇḍa | 61 | 11 | Mahabharata | mandatory |
| Raudrāśva · Puru-line witness | 55 | 11 | Vishnu Purana | mandatory |
| Uśīnara · Viṣṇu Purāṇa 4.18 witness | 51 | 6 | Vishnu Purana | mandatory |
| Viśvakarman · creator of Tilottamā | 39 | 5 | Bhagavata, Mahabharata | mandatory |
| Kuśa · Amāvasu branch | 36 | 5 | Vishnu Purana | mandatory |
| Dambha · child of Adharma and Mṛṣā | 32 | 5 | Bhagavata | optional |
| Haryaśva · Nīla branch · Viṣṇu Purāṇa 4.19 witness | 32 | 6 | Vishnu Purana | mandatory |
| Punniyarājan · king in Maṇimēkalai | 29 | 6 | Manimekalai | mandatory |
| Pulaha · Mahābhārata Sabha Parva §XI Brahmā-assembly roster | 23 | 5 | Bhagavata, Mahabharata | mandatory |
| Kālakā · mother of eight kings · Mahābhārata Ādiparvan 1.59–1.61 witness | 23 | 7 | Mahabharata | mandatory |
| Dīrghatamas · Viṣṇu Purāṇa 4.18 witness | 23 | 5 | Vishnu Purana | mandatory |
| Parīkṣit · Kuru branch · Viṣṇu Purāṇa 4.19 witness | 23 | 5 | Vishnu Purana | mandatory |
| Devaka · Viṣṇu Purāṇa 4.14 witness | 23 | 5 | Vishnu Purana | mandatory |
| Drupada / Yajñasena · king of Pāñcāla | 19 | 6 | Mahabharata | mandatory |
| Durukti · Harsh Speech, sister of Kali | 12 | 5 | Bhagavata | optional |
| Sthāṇu (Śiva) · Rudra progenitor · Mahābhārata Ādiparvan 1.59–1.61 witness | 1 | 11 | Mahabharata | optional |
| Śraddhā · wife of Aṅgirā; distinct from Dakṣa’s daughter of the same name | 1 | 7 | Bhagavata | optional |
| Dhiṣaṇā · Śrīmad-Bhāgavatam 6.6–6.7 witness | 1 | 5 | Bhagavata | mandatory |
| Brahma-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 8 | Bhagavata | mandatory |
| Dakṣa-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 5 | Bhagavata | mandatory |
| Deva-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 5 | Bhagavata | mandatory |
| Indra-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 9 | Bhagavata | mandatory |
| Rudra-sāvarṇi Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 7 | Bhagavata | mandatory |
| Svārociṣa Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 7 | Bhagavata | mandatory |
| Tāmasa Manu · Śrīmad-Bhāgavatam Canto 8 witness | 1 | 8 | Bhagavata | optional |
| Dharma · Vindhyaśakti branch · Viṣṇu Purāṇa 4.24 future-dynasty witness | 1 | 7 | Vishnu Purana | mandatory |
| Kaṃsa · Viṣṇu Purāṇa 4.14 witness | 1 | 7 | Vishnu Purana | mandatory |
| Viśvāmitra · son of Satyavatī’s unnamed mother | 1 | 6 | Vishnu Purana | mandatory |

## hubs_distance_2_budget_10: selected set

| Record | Weight | Original degree | Source families | Membership |
|---|---:|---:|---|---|
| Yudhiṣṭhira | 2556 | 198 | Mahabharata, Vishnu Purana | mandatory |
| Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness | 980 | 59 | Bhagavata, Mahabharata | mandatory |
| Nahuṣa · Viṣṇu Purāṇa witness | 948 | 8 | Vishnu Purana | mandatory |
| Rāma | 709 | 29 | Mahabharata, Manimekalai, Ramayana, Vishnu Purana | mandatory |
| Tapatī · daughter of the Sun and wife of Saṃvaraṇa | 695 | 7 | Bhagavata, Mahabharata | mandatory |
| Kadrū · mother in Ādiparvan serpent genealogy | 664 | 78 | Mahabharata | mandatory |
| Ajamīḍha · Hastin branch · Viṣṇu Purāṇa 4.19 witness | 337 | 6 | Vishnu Purana | mandatory |
| Satrājita · son of Nighna · Viṣṇu Purāṇa 4.13 witness | 307 | 8 | Bhagavata, Vishnu Purana | mandatory |
| Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness | 289 | 34 | Bhagavata, Mahabharata | mandatory |
| Maṇimēkalai · heroine of the Tamil epic | 263 | 27 | Manimekalai | mandatory |

## Shared-neighbor audit

No direct selected–selected edges does not prevent many selected records from sharing a parent or assembly host. This audit counts unique selected pairs with at least one common original-graph neighbor.

- **uniform**: 1820 selected records have original degree ≤1; 56011 selected pairs share a neighbor.
  - Yudhiṣṭhira: 171 selected neighbors.
  - Yama · host of the assembly described in MB 2 Section VIII · Mahābhārata Sabha Parva §VIII: 121 selected neighbors.
- **degree**: 1678 selected records have original degree ≤1; 61585 selected pairs share a neighbor.
  - Yudhiṣṭhira: 176 selected neighbors.
  - Yama · host of the assembly described in MB 2 Section VIII · Mahābhārata Sabha Parva §VIII: 122 selected neighbors.
- **source_diversity**: 1808 selected records have original degree ≤1; 56332 selected pairs share a neighbor.
  - Yudhiṣṭhira: 173 selected neighbors.
  - Yama · host of the assembly described in MB 2 Section VIII · Mahābhārata Sabha Parva §VIII: 122 selected neighbors.
- **bridge**: 998 selected records have original degree ≤1; 22251 selected pairs share a neighbor.
  - Arjuna · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness: 127 selected neighbors.
  - Dhṛtarāṣṭra · Viṣṇu Purāṇa 4.20 witness: 86 selected neighbors.
- **hubs_distance_1**: 0 selected records have original degree ≤1; 296 selected pairs share a neighbor.
  - Yudhiṣṭhira: 13 selected neighbors.
  - Indra: 8 selected neighbors.
- **hubs_distance_2**: 0 selected records have original degree ≤1; 0 selected pairs share a neighbor.
- **hubs_distance_2_budget_10**: 0 selected records have original degree ≤1; 0 selected pairs share a neighbor.

## Forcing a prominent hub into the ten-record shortlist

These are new solves of the same capped objective, with the named record required. A positive loss measures the tradeoff under this model. Conflicts list members of the original optimum that cannot coexist with the required record.

| Required record | Best forced weight | Loss from optimum | Conflicting original members |
|---|---:|---:|---|
| Indra | 7078 | 670 | Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness; Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness; Rāma; Maṇimēkalai · heroine of the Tamil epic; Yudhiṣṭhira |
| Arjuna · human incarnation · Mahābhārata Ādiparvan 1.59–1.61 witness | 7086 | 662 | Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness; Dakṣa · Prajāpati · Mahābhārata Ādiparvan 1.59–1.61 witness; Kadrū · mother in Ādiparvan serpent genealogy; Yudhiṣṭhira |
| Jāmbavant · linked Rāmāyaṇa, Viṣṇu Purāṇa and Bhāgavata witnesses | 7691 | 57 | Bali · Daitya · Mahābhārata Ādiparvan 1.59–1.61 witness; Rāma; Satrājita · son of Nighna · Viṣṇu Purāṇa 4.13 witness |
| Kṛṣṇa · born to Devakī · Viṣṇu Purāṇa 4.15 witness · Kṛṣṇa’s incarnation narrative | 7086 | 662 | Rāma; Satrājita · son of Nighna · Viṣṇu Purāṇa 4.13 witness; Yudhiṣṭhira |

## Reproduce

Install `requirements.txt` into the graph-analysis Python environment, then run `python analyze_mwis.py` from the repository root. The input commit must be available locally. `results.json` records all selected IDs, objectives, upper bounds, gaps and versions; `memberships.csv` includes every record’s scores and memberships.

These selections are analytical artifacts, not new textual relationships. No claims or edges are added to the canonical graph by this experiment.
