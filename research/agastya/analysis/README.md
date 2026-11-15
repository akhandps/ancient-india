# Agastya graph experiments

This directory records a completed exploratory run over [input-graph.json](input-graph.json), preserved before the Jāmbavant extension was integrated into `../graph.json`. It asks what the **recorded textual relationships** imply about that particular dataset snapshot. It does not test whether narrated events happened, date people, or establish independent historical corroboration.

- [Findings and interpretation](FINDINGS.md)
- [Generated numerical results](RESULTS.md)
- [Machine-readable results and claim evidence](results.json)
- [Connectivity chart](connectivity.png)
- [Jāmbavant bridge diagram](jambavant-bridge.png)

## Reproduce

From the repository root, with Python 3.10 or later:

```sh
python3 -m venv /tmp/agastya-analysis
/tmp/agastya-analysis/bin/pip install -r research/agastya/analysis/requirements.txt
MPLCONFIGDIR=/tmp/agastya-matplotlib /tmp/agastya-analysis/bin/python analyze_agastya.py
/tmp/agastya-analysis/bin/python -m unittest discover -s research/agastya/analysis -p 'test_*.py'
```

The script reads the preserved `input-graph.json` and overwrites generated results, CSVs, and PNGs. It does not modify the canonical graph or narrative `FINDINGS.md`. Results include the input SHA-256, package version, and random seeds. These baseline results remain distinct from the expanded canonical graph.

## Completed experiments

| Experiment | Method | Outputs |
|---|---|---|
| Communities | Unweighted Louvain on each variant; repeat seeds 7, 19, 42 for baseline and the graph without attendance/kinship | Group sizes, leading nodes, within-community claim source families, modularity, adjusted Rand agreement; `communities.csv` |
| Bridges | Exact unweighted node betweenness, articulation points, cross-community participation for nodes with degree ≥5 | Full `centrality.csv`, ranked candidates and articulation component sizes |
| Typed motifs | Explicit directional parent, spouse, teaching, killing predicate sets | Parent–spouse triangles, teaching chains, multiple-parent review queue, directed parent cycles, short family paths between killer/victim records, narrator/reference motifs |
| Cross-source recurrence | Endpoint-pair overlap, then direction-normalized parent/spouse/teaching/killing overlap; group editions of the same work | Claim IDs and text families for every recurring pair/typed relationship |
| Robustness | Remove attendance, broad kinship/predictions, narration/reference, non-passage-checked claims, and secondary identity links; remove each source and each source family; remove individual root-incident claims | Graph size, component size, root reachability, three-link neighborhoods; `source_ablation.csv` |
| Identity sensitivity | Hypothetically merge six Agastya facets; separately merge exact pre-` · ` name labels as an intentionally unsafe stress test | Counts projected back onto original records, shortened paths, newly reachable records, collision groups |

## Modeling choices

**Universe:** 3,229 person-like records, including deities, collectives, and the six Agastya facets. Non-person types (texts, places, events, unresolved references, etc.) are excluded, consistently with the existing hop audit. Isolated person-like records stay in every graph, so normalization and node counts use a fixed universe. “Person-like” is a computational category, not a historical assertion.

**Edges:** Only claims whose two endpoints are person-like. Exclude `identity_hypothesis` claims. Multiple claims between the same endpoints become one undirected, unweighted edge for structural analysis; every supporting claim ID is retained. Self-links are omitted structurally. Graph direction is ignored only for connectivity and centrality, never for typed motifs. There is no chronological or causal inference from an undirected path. Exact betweenness counts all shortest paths, normalized against the fixed node universe, including unreachable pairs as zero contributions.

**Root distances:** Multi-source shortest paths from all six Agastya facets. These are alternative source-local starting dossiers, not six assertions about historical identity. Three links is a descriptive threshold, not a natural boundary. The merge-six-facets scenario is a useful control: multi-source minimum distances should not shorten. Other pairwise distances and centralities can still change under that merge.

**Predicate ablation:** `edge_class` in `analyze_agastya.py` applies an explicit, inspectable rule. `predicate_classes.csv` lists every predicate and its assigned class. Attendance is detected before kinship (so birth-attendance is not a parent link); predictions are separated before kinship. Broad kinship includes relationships concerning birth, marriage, ancestry, adoption, and kinship language, including some requests and mythic birth imagery. It is deliberately broader than biological parentage. This is a sensitivity analysis, not a definitive semantic ontology. A pair survives an ablation if another non-removed claim supports it.

**Communities:** Run on active records; components and isolates strongly affect apparent modularity. Source-family composition counts internal **claims**, not unique edges or people. Communities are optimization results, not identified cultures, periods, or independently discovered historical groups. Seed stability is not robustness to missing texts or identity decisions. Participation and community count should not be compared as if all variants had the same active universe.

**Sources:** Source records have different granularity (one hymn versus an entire electronic book), so leave-one-source counts do not rank historical importance. `source_family_mapping` groups editions and chapters for broad comparisons. A shared source family does not establish dependence; different families do not establish independence. Cross-source recurrence can only find already-linked endpoints; source-local duplicates suppress apparent overlap. The claim `facet` field is a collection tag and is not used as a substitute for source provenance.

**Identity:** Base-name merging ignores branch labels, homonyms, spelling variants, and explicit source-local distinctions. It is a deliberately damaging counterfactual, not a recommended resolution. Report reachability against original records to avoid confusing fewer merged nodes with fewer reachable entities. Newly reachable records are counted separately from previously reachable records whose paths shorten. Original non-root records mapped onto a root count as distance zero in the unsafe scenario.

**Typed motifs:** Normalize only named predicate sets. Appointment as a teacher and an unsuccessful request to study are not accepted teaching edges. Reported alternative teachers are separate claim-qualified paths, not simultaneous asserted lineages. `MBAPE128` is excluded from baseline typed motifs because its father predicate contradicts its own summary and note. It is now corrected to `teacher_of` in the canonical merge review; the original error stays visible in the experiment input snapshot. Multiple-parent motifs are an audit queue; rebirth, adoption, divine origin, duplicate records, role language, and extraction errors can all explain them. No detected motif is claimed statistically enriched: no matched null model or corpus sampling model has been fitted.

## Files

- `centrality.csv`: all original records, degrees, exact betweenness, positive-score ranks for every variant. Zero-score ranks are blank.
- `communities.csv`: active record memberships for seed 42, all variants.
- `source_ablation.csv`: per-source reachability losses.
- `predicate_classes.csv`: auditable edge-class assignment.
- `results.json`: complete experiment output, semantic exclusions, input hash, source mappings, and claim-level evidence.

## Follow-up experiments

The current results nominate questions rather than statistical discoveries. Strong follow-ups would split identity links from event relationships into separate layers, distinguish life episodes in rebirth stories, resolve candidate duplicates through passage review, add source-balanced weighted centrality, and compare motifs with degree-preserving null graphs. These would be new experiments, not checks already completed here.
