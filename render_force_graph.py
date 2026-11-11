"""Embed the current evidence graph in standalone 2D and 3D force views."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
graph = json.loads((ROOT / 'research/agastya/graph.json').read_text())
payload = json.dumps(graph, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
many_body = (ROOT / 'agastya-many-body.js').read_text()
for dimension in ('3d', '2d', 'webgl', 'three'):
    template = (ROOT / f'agastya-force-{dimension}.template.html').read_text()
    html = template.replace('__GRAPH_DATA__', payload).replace('__MANY_BODY_HELPER__', many_body)
    target = ROOT / f'research/agastya/force-graph-{dimension}.html'
    target.write_text(html)
    print(target)
