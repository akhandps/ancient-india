# Ancient Indian textual relationships

This repository traces people, places, and textual witnesses connected to Agastya and records each relationship as a source attributed claim. The graph currently contains 3,295 nodes and 4,199 claims from 105 sources. These are textual records, not a count of distinct historical people.

[Open the rendered graph](https://akhandps.github.io/ancient-india/).

## Explore

- [WebGL graph with circular nodes](research/agastya/force-graph-webgl.html)
- [Direct Three.js graph](research/agastya/force-graph-three.html)
- [Canvas 3D graph](research/agastya/force-graph-3d.html)
- [Canvas 2D graph](research/agastya/force-graph-2d.html)
- [Timeline](research/agastya/timeline.html)
- [Research notes, sources, and limitations](research/agastya/README.md)

Open the HTML files locally in a browser. The WebGL views use the bundled JavaScript in `research/agastya/vendor/` and do not require a server.

## Data and regeneration

The main graph is [graph.json](research/agastya/graph.json). Research batches and provenance notes are in `research/agastya/expansion/`. The Python scripts in the repository root merge the reviewed batches and generate the research views. See the [research README](research/agastya/README.md) for the regeneration order and evidence caveats.

The third party Mahābhārata name index transcription and generated excerpt CSVs are excluded from the repository. Their source, attribution, and local regeneration notes are in [INM-SOURCE.md](research/agastya/expansion/INM-SOURCE.md). Vendored JavaScript licenses are in `research/agastya/vendor/`.
