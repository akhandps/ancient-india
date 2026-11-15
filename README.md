# Ancient Indian textual relationships

This repository traces people, places, and textual witnesses connected to Agastya and records each relationship as a source attributed claim. The graph currently contains 3,310 nodes and 4,244 claims from 125 sources, plus eight source-qualified observations. These are textual records, not a count of distinct historical people.

[Open the rendered graph](https://akhandps.github.io/ancient-india/).

## Explore

- [WebGL graph with circular nodes](research/agastya/force-graph-webgl.html)
- [Direct Three.js graph](research/agastya/force-graph-three.html)
- [Canvas 3D graph](research/agastya/force-graph-3d.html)
- [Canvas 2D graph](research/agastya/force-graph-2d.html)
- [Timeline](research/agastya/timeline.html)
- [Research notes, sources, and limitations](research/agastya/README.md)
- [Graph experiments and findings](research/agastya/analysis/README.md): communities, bridges, relationship motifs, source dependence, and identity sensitivity.
- [Jāmbavant deep dive](research/jambavant/README.md): new passage records, narrative connections, duration variants, and identity-sensitive bridge tests.
- [Distant-pair experiments](research/distant-pairs/FINDINGS.md): exact graph extremes, disconnected records, and source-backed connection searches.
- [Maximum-weight independent sets](research/mwis/FINDINGS.md): certified solutions under explicit weights, with shared-neighbor and shortlist controls.

Open the HTML files locally in a browser. The WebGL views use the bundled JavaScript in `research/agastya/vendor/` and do not require a server.

## Data and regeneration

The main graph is [graph.json](research/agastya/graph.json). Research batches and provenance notes are in `research/agastya/expansion/`. The Python scripts in the repository root merge the reviewed batches and generate the research views. See the [research README](research/agastya/README.md) for the regeneration order and evidence caveats.

The third party Mahābhārata name index transcription and generated excerpt CSVs are excluded from the repository. Their source, attribution, and local regeneration notes are in [INM-SOURCE.md](research/agastya/expansion/INM-SOURCE.md). Vendored JavaScript licenses are in `research/agastya/vendor/`.
