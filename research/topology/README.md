# Topological ordering: what can come before what?

Input: graph at `1c5958bc213fece401e86af5c82a560a4996c4d4`. Reproduce with `python analyze_topology.py` in the existing graph-analysis environment. No new textual claims or identities are introduced.

## The ancestry projection can be sorted

Using the existing explicit parent-predicate allowlists, normalizing child-to-parent claims to **parent → child**, and retaining only passage-checked claims produces a directed acyclic graph:

- **1,629 active records, 1,699 directed edges.**
- **43 topological layers**, numbered 0–42.
- A longest chain contains **42 parent–child links**. It runs from the Vasiṣṭha dossier associated with Aśmaka through the Rāma line to Bṛhadbala. All steps and supporting claim IDs are in `results.json`.

Every recorded parent precedes its child in the exported ordering. Records in the same layer have no ancestry path between them in this projection. They are not thereby contemporaries. Disconnected lineages each begin at layer zero; a root means no included parent, not the first person in history. Other valid topological orders exist, and incomparable records may occur in different layers too.

This is a conservative predicate projection. It uses `PARENT_FORWARD`, `PARENT_REVERSE`, `CHECKED`, and `NORMALIZATION_EXCLUSIONS` from `analyze_agastya.py`, all recorded in the results. Predicted parentage, rebirth, grandparent links, special predicates for adoptive or dynastic relationships, and generic birth/creation predicates are not silently converted into ordinary parentage. Some included source claims can still concern divine or attributed parentage; see the individual evidence. Source-local dossiers and existing identity alignments are preserved. Absence of cycles does not establish that the genealogies are historically correct or complete.

Download [the ancestry ordering](ancestry-order.csv) or inspect [the full results and evidence IDs](results.json).

## The mixed graph cannot be sorted directly

The active person-like subject → object projection has **3,164 records and 3,850 edges**, excluding identity hypotheses. It contains **16 cyclic strongly connected components**, the largest with **227 records**. Each cyclic component and an example cycle with supporting claims is exported.

A cycle is expected when directions mean different things. Reciprocal relationships and parent/child predicates stored in opposite directions can already produce cycles. Dialogue, combat and recognition edges do not consistently mean “earlier than.” These cycles are not automatically contradictions, time loops or narrative communities.

We also computed the **condensation DAG**: each strongly connected component becomes one block, and those blocks can be topologically ordered. This preserves inter-block reachability but supplies no internal order within a cyclic block. Its direction is still subject → object, not chronological precedence. See the [NetworkX condensation documentation](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.condensation.html).

## For a narrative sequence, order events

To ask “what happens before what?”, we should build a separate **event → event** projection with source-qualified precedence claims. For example, Jāmbavant's initial misrecognition and later recognition are different moments, although both current claims connect the same two character records.

Such an event graph could distinguish explicit sequence from inferred sequence, preserve different tellings, and identify genuine precedence conflicts. A topological order of the current character relationships cannot recover that sequence by itself. The useful first export here is therefore ancestry layering, not a universal timeline.

The script verifies every ancestry edge against both the order and layer assignment, verifies the longest-chain length, and checks the condensation DAG's layer constraints. Layer construction follows [NetworkX topological generations](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.topological_generations.html).
