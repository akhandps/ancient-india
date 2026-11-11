import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

(() => {
  'use strict';

  const data = JSON.parse(document.getElementById('graph-data').textContent);
  const stage = document.getElementById('stage');
  const detail = document.getElementById('detail');
  const error = document.getElementById('error');
  const status = document.getElementById('status');
  const tradition = document.getElementById('tradition');
  const radius = document.getElementById('radius');
  const sources = document.getElementById('sources');
  const search = document.getElementById('search');
  const results = document.getElementById('results');
  const fit = document.getElementById('fit');
  const pause = document.getElementById('pause');

  const esc = value => String(value ?? '').replace(/[&<>"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[char]);
  const facetIds = data.nodes.filter(node => node.type === 'agastya_facet').map(node => node.id);
  const displayId = id => facetIds.includes(id) ? 'agastya-hub' : id;
  const facetLabels = { vedic: 'Vedic', ramayana: 'Rāmāyaṇa', mahabharata: 'Mahābhārata', puranic: 'Bhāgavata', tamil: 'Tamil', buddhist: 'Buddhacarita' };
  for (const id of facetIds) {
    const option = document.createElement('option');
    option.value = id;
    option.textContent = facetLabels[id] || id;
    tradition.append(option);
  }

  const nodeMap = new Map(data.nodes.filter(node => node.type !== 'agastya_facet').map(node => [node.id, {
    ...node,
    kind: node.type === 'text' ? 'text' : node.type === 'place' ? 'place' : 'person'
  }]));
  nodeMap.set('agastya-hub', { id: 'agastya-hub', label: 'Agastya', kind: 'hub', type: 'navigation' });
  const sourceMap = new Map(data.sources.map(source => [source.id, source]));
  for (const source of data.sources) nodeMap.set('source:' + source.id, { id: 'source:' + source.id, label: source.title, kind: 'source', source });
  const claimEdges = data.claims.map(claim => ({ a: displayId(claim.subject), b: displayId(claim.object), kind: 'claim', claim }));
  const palette = { hub: '#ffe1a0', person: '#83c7ee', text: '#b9a9ef', place: '#87d8bc', source: '#8193ad' };
  const particles = new Map();
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#080f1d');
  const camera = new THREE.PerspectiveCamera(60, 1, 1, 50000);
  camera.position.set(0, 0, 1800);
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  } catch (cause) {
    error.textContent = 'Three.js could not start WebGL: ' + cause.message;
    error.hidden = false;
    return;
  }
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.setSize(Math.max(300, stage.clientWidth), Math.max(300, stage.clientHeight));
  stage.append(renderer.domElement);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 75;
  controls.maxDistance = 30000;

  let activeNodes = [], activeEdges = [], degree = new Map(), selected = 'agastya-hub';
  let pointCloud = null, lineCloud = null, highlightLines = null;
  let pointPositions, pointColors, pointSizes, linePositions;
  let playing = true, heat = 1, lastPhysics = 0, flight = null, searchChoices = [], searchCursor = 0;
  const raycaster = new THREE.Raycaster();
  raycaster.params.Points.threshold = 18;
  const pointer = new THREE.Vector2();

  function seed(id) {
    let hash = 2166136261;
    for (const char of id) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619);
    const angle = ((hash >>> 0) % 6283) / 1000;
    const latitude = (((hash >>> 8) % 3141) / 1000) - 1.57;
    const r = 130 + ((hash >>> 17) % 170);
    return { x: r * Math.cos(angle) * Math.cos(latitude), y: r * Math.sin(latitude), z: r * Math.sin(angle) * Math.cos(latitude), vx: 0, vy: 0, vz: 0 };
  }

  function distances(edges, limit) {
    const adjacency = new Map();
    for (const edge of edges) {
      if (!adjacency.has(edge.a)) adjacency.set(edge.a, []);
      if (!adjacency.has(edge.b)) adjacency.set(edge.b, []);
      adjacency.get(edge.a).push(edge.b);
      adjacency.get(edge.b).push(edge.a);
    }
    const seen = new Map([['agastya-hub', 0]]), queue = ['agastya-hub'];
    for (let i = 0; i < queue.length; i++) {
      const id = queue[i];
      if (seen.get(id) >= limit) continue;
      for (const neighbor of adjacency.get(id) || []) if (!seen.has(neighbor)) {
        seen.set(neighbor, seen.get(id) + 1);
        queue.push(neighbor);
      }
    }
    return seen;
  }

  function disposeGraphObjects() {
    for (const object of [pointCloud, lineCloud, highlightLines]) {
      if (!object) continue;
      scene.remove(object);
      object.geometry.dispose();
      object.material.dispose();
    }
  }

  const pointMaterial = () => new THREE.ShaderMaterial({
    transparent: true,
    depthWrite: false,
    vertexColors: false,
    vertexShader: `
      attribute vec3 aColor;
      attribute float aSize;
      varying vec3 vColor;
      void main() {
        vColor = aColor;
        vec4 view = modelViewMatrix * vec4(position, 1.0);
        gl_PointSize = clamp(aSize * 650.0 / max(1.0, -view.z), 2.0, 30.0);
        gl_Position = projectionMatrix * view;
      }
    `,
    fragmentShader: `
      varying vec3 vColor;
      void main() {
        float d = length(gl_PointCoord - vec2(0.5));
        float core = 1.0 - smoothstep(0.29, 0.45, d);
        float aura = (1.0 - smoothstep(0.35, 0.5, d)) * 0.18;
        float alpha = min(1.0, core + aura);
        if (alpha < 0.02) discard;
        gl_FragColor = vec4(vColor, alpha);
      }
    `
  });

  function buildGeometry() {
    disposeGraphObjects();
    pointPositions = new Float32Array(activeNodes.length * 3);
    pointColors = new Float32Array(activeNodes.length * 3);
    pointSizes = new Float32Array(activeNodes.length);
    const pointGeometry = new THREE.BufferGeometry();
    pointGeometry.setAttribute('position', new THREE.BufferAttribute(pointPositions, 3).setUsage(THREE.DynamicDrawUsage));
    pointGeometry.setAttribute('aColor', new THREE.BufferAttribute(pointColors, 3).setUsage(THREE.DynamicDrawUsage));
    pointGeometry.setAttribute('aSize', new THREE.BufferAttribute(pointSizes, 1).setUsage(THREE.DynamicDrawUsage));
    pointGeometry.boundingSphere = new THREE.Sphere(new THREE.Vector3(), 1e7);
    pointCloud = new THREE.Points(pointGeometry, pointMaterial());
    pointCloud.frustumCulled = false;
    scene.add(pointCloud);

    linePositions = new Float32Array(activeEdges.length * 6);
    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3).setUsage(THREE.DynamicDrawUsage));
    lineGeometry.boundingSphere = new THREE.Sphere(new THREE.Vector3(), 1e7);
    lineCloud = new THREE.LineSegments(lineGeometry, new THREE.LineBasicMaterial({ color: '#6a819b', transparent: true, opacity: 0.18, depthWrite: false }));
    lineCloud.frustumCulled = false;
    scene.add(lineCloud);
    highlightLines = new THREE.LineSegments(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: '#ffd586', transparent: true, opacity: 0.82, depthWrite: false }));
    highlightLines.frustumCulled = false;
    scene.add(highlightLines);
    updateColors();
    updatePositions();
  }

  function updateColors() {
    if (!pointCloud) return;
    for (let i = 0; i < activeNodes.length; i++) {
      const node = activeNodes[i];
      const color = new THREE.Color(node.id === selected ? '#ffe1a0' : palette[node.kind] || palette.person);
      pointColors.set([color.r, color.g, color.b], i * 3);
      pointSizes[i] = node.id === selected ? 56 : node.kind === 'hub' ? 49 : node.kind === 'source' ? 15 : node.kind === 'text' ? 27 : 19 + Math.min(19, Math.sqrt(degree.get(node.id) || 0) * 2.1);
    }
    pointCloud.geometry.attributes.aColor.needsUpdate = true;
    pointCloud.geometry.attributes.aSize.needsUpdate = true;
    updateHighlight();
  }

  function updateHighlight() {
    if (!highlightLines) return;
    highlightLines.geometry.dispose();
    const incident = activeEdges.filter(edge => edge.kind === 'claim' && (edge.a === selected || edge.b === selected));
    const positions = new Float32Array(incident.length * 6);
    for (let i = 0; i < incident.length; i++) {
      const a = particles.get(incident[i].a), b = particles.get(incident[i].b);
      positions.set([a.x, a.y, a.z, b.x, b.y, b.z], i * 6);
    }
    highlightLines.geometry = new THREE.BufferGeometry();
    highlightLines.geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3).setUsage(THREE.DynamicDrawUsage));
    highlightLines.userData.incident = incident;
  }

  function updatePositions() {
    if (!pointCloud) return;
    for (let i = 0; i < activeNodes.length; i++) {
      const p = particles.get(activeNodes[i].id);
      pointPositions.set([p.x, p.y, p.z], i * 3);
    }
    for (let i = 0; i < activeEdges.length; i++) {
      const a = particles.get(activeEdges[i].a), b = particles.get(activeEdges[i].b);
      linePositions.set([a.x, a.y, a.z, b.x, b.y, b.z], i * 6);
    }
    const highlighted = highlightLines?.geometry.attributes.position?.array;
    if (highlighted) for (let i = 0; i < highlightLines.userData.incident.length; i++) {
      const edge = highlightLines.userData.incident[i], a = particles.get(edge.a), b = particles.get(edge.b);
      highlighted.set([a.x, a.y, a.z, b.x, b.y, b.z], i * 6);
    }
    pointCloud.geometry.attributes.position.needsUpdate = true;
    lineCloud.geometry.attributes.position.needsUpdate = true;
    if (highlighted) highlightLines.geometry.attributes.position.needsUpdate = true;
  }

  function forces(dt) {
    const nodes = activeNodes, count = nodes.length;
    const fx = new Float64Array(count), fy = new Float64Array(count), fz = new Float64Array(count);
    const index = new Map(nodes.map((node, i) => [node.id, i]));
    repulsion(nodes, particles, 3, fx, fy, fz, false);
    for (const edge of activeEdges) {
      const i = index.get(edge.a), j = index.get(edge.b);
      if (i === undefined || j === undefined) continue;
      const a = particles.get(edge.a), b = particles.get(edge.b);
      const dx = b.x - a.x, dy = b.y - a.y, dz = b.z - a.z;
      const length = Math.hypot(dx, dy, dz) || 1;
      const da = degree.get(edge.a) || 0, db = degree.get(edge.b) || 0;
      const rest = edge.kind === 'claim' ? 145 - Math.min(78, 12 * Math.log1p(da * db)) : 135;
      const spring = edge.kind === 'claim' ? 0.026 : 0.007;
      const magnitude = (length - rest) * spring / length;
      fx[i] += dx * magnitude; fy[i] += dy * magnitude; fz[i] += dz * magnitude;
      fx[j] -= dx * magnitude; fy[j] -= dy * magnitude; fz[j] -= dz * magnitude;
    }
    const step = Math.min(1.35, dt / 16.67), cool = Math.max(0.035, heat);
    for (let i = 0; i < count; i++) {
      const node = nodes[i], p = particles.get(node.id);
      const center = node.kind === 'hub' ? 0.07 : 0.018;
      p.vx = Math.max(-8, Math.min(8, (p.vx + step * cool * (fx[i] - p.x * center)) * 0.68));
      p.vy = Math.max(-8, Math.min(8, (p.vy + step * cool * (fy[i] - p.y * center)) * 0.68));
      p.vz = Math.max(-8, Math.min(8, (p.vz + step * cool * (fz[i] - p.z * center)) * 0.68));
      p.x += p.vx * step; p.y += p.vy * step; p.z += p.vz * step;
    }
    heat = Math.max(0.035, heat * 0.994);
    updatePositions();
  }

  function rebuild() {
    const facet = tradition.value;
    const base = facet === 'all' ? claimEdges : claimEdges.filter(edge => edge.claim.facet === facet);
    const limit = radius.value === 'all' ? Infinity : Number(radius.value);
    const seen = distances(base, limit);
    const claims = limit === Infinity ? base : base.filter(edge => seen.has(edge.a) && seen.has(edge.b));
    const ids = new Set(['agastya-hub']);
    for (const edge of claims) { ids.add(edge.a); ids.add(edge.b); }
    if (facet === 'all' && limit === Infinity) for (const node of data.nodes) if (node.type !== 'agastya_facet') ids.add(node.id);
    const edges = claims.map(edge => ({ ...edge }));
    if (sources.checked) {
      const cited = new Set();
      for (const edge of claims) {
        const sourceId = 'source:' + edge.claim.source;
        ids.add(sourceId);
        for (const id of [edge.a, edge.b]) {
          const key = sourceId + '|' + id;
          if (!cited.has(key)) { cited.add(key); edges.push({ a: sourceId, b: id, kind: 'citation' }); }
        }
      }
      if (facet === 'all' && limit === Infinity) for (const source of data.sources) ids.add('source:' + source.id);
    }
    activeNodes = [...ids].map(id => nodeMap.get(id)).filter(Boolean);
    activeEdges = edges;
    degree = new Map(activeNodes.map(node => [node.id, 0]));
    for (const edge of claims) {
      degree.set(edge.a, (degree.get(edge.a) || 0) + 1);
      degree.set(edge.b, (degree.get(edge.b) || 0) + 1);
    }
    for (const node of activeNodes) if (!particles.has(node.id)) particles.set(node.id, seed(node.id));
    if (!ids.has(selected)) selected = 'agastya-hub';
    heat = 1;
    buildGeometry();
    renderDetail();
    status.textContent = `${activeNodes.length.toLocaleString()} nodes · ${claims.length.toLocaleString()} passage claims`;
    fitAll(false);
  }

  function bounds() {
    const box = new THREE.Box3();
    for (const node of activeNodes) {
      const p = particles.get(node.id);
      box.expandByPoint(new THREE.Vector3(p.x, p.y, p.z));
    }
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    const radius = Math.max(size.x / Math.max(0.7, camera.aspect), size.y, size.z) / 2;
    return { center, distance: Math.max(500, radius / Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * 1.55 + radius) };
  }

  function flyTo(position, target, duration = 950) {
    flight = { fromPosition: camera.position.clone(), fromTarget: controls.target.clone(), toPosition: position.clone(), toTarget: target.clone(), start: performance.now(), duration };
  }

  function fitAll(animated = true) {
    const { center, distance } = bounds();
    const destination = center.clone().add(new THREE.Vector3(0, 0, distance));
    if (animated) flyTo(destination, center);
    else { flight = null; camera.position.copy(destination); controls.target.copy(center); controls.update(); }
  }

  function focusOn(id) {
    const p = particles.get(id);
    if (!p || !activeNodes.some(node => node.id === id)) return;
    selected = id;
    renderDetail();
    updateColors();
    const target = new THREE.Vector3(p.x, p.y, p.z);
    const direction = camera.position.clone().sub(controls.target).normalize();
    const distance = 250 + Math.min(220, Math.sqrt(degree.get(id) || 0) * 20);
    flyTo(target.clone().addScaledVector(direction, distance), target, 1050);
  }

  function claimsFor(id) {
    return data.claims.filter(claim => displayId(claim.subject) === id || displayId(claim.object) === id || (id.startsWith('source:') && claim.source === id.slice(7)))
      .filter(claim => tradition.value === 'all' || claim.facet === tradition.value);
  }

  function renderDetail() {
    const node = nodeMap.get(selected), claims = claimsFor(selected), source = node?.source;
    let html = `<h2>${esc(node?.label || 'Agastya')}</h2><div class="muted small">${esc(node?.kind || 'entity')}${source ? ` · <a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">Open source</a>` : ''}</div><div class="metric"><span>${degree.get(selected) || 0} passage connections</span><span>${claims.length} claims</span></div>`;
    if (selected === 'agastya-hub') html += '<p class="small muted">Agastya groups the source-local witnesses for navigation. A passage link records a textual claim, not an established historical meeting.</p>';
    html += '<h3>Passage evidence</h3>';
    html += claims.slice(0, 50).map(claim => {
      const sourceRecord = sourceMap.get(claim.source);
      return `<div class="claim"><strong>${esc(nodeMap.get(displayId(claim.subject))?.label || claim.subject)} → ${esc(claim.predicate.replaceAll('_', ' '))} → ${esc(nodeMap.get(displayId(claim.object))?.label || claim.object)}</strong><p>${esc(claim.summary)}</p><a href="${esc(sourceRecord?.url || '#')}" target="_blank" rel="noopener noreferrer">${esc(sourceRecord?.title || claim.source)} · ${esc(claim.locator)}</a><br><small>${esc(facetLabels[claim.facet] || claim.facet)} · ${esc(claim.status.replaceAll('_', ' '))}</small></div>`;
    }).join('');
    if (claims.length > 50) html += `<p class="small muted">${claims.length - 50} more claims in graph.json.</p>`;
    detail.innerHTML = html;
  }

  const fold = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '');
  const forms = value => [...new Set([fold(value), fold(String(value).toLowerCase().replace(/[ṛṝ]/g, 'ri').replace(/[śṣ]/g, 'sh').replace(/ṅ/g, 'ng').replace(/ñ/g, 'ny'))])];
  function findMatches(raw) {
    const queries = forms(raw).filter(Boolean);
    if (!queries.length) return [];
    return [...nodeMap.values()].map(node => {
      const names = node.label.split(' · ')[0].split(/\s*\/\s*/).flatMap(forms);
      const exact = queries.some(q => names.includes(q));
      const prefix = queries.some(q => names.some(name => name.startsWith(q)));
      const inside = queries.some(q => names.some(name => name.includes(q)));
      const body = queries.some(q => forms(node.label).some(name => name.includes(q)));
      let score = exact ? 0 : prefix ? 10 : inside ? 27 : body ? 43 : queries.some(q => fold(node.id).includes(q)) ? 50 : Infinity;
      if (node.kind === 'text') score += 4;
      if (node.kind === 'source') score += 7;
      score -= Math.min(4, Math.log1p(degree.get(node.id) || 0));
      return { node, score };
    }).filter(result => Number.isFinite(result.score))
      .sort((a, b) => a.score - b.score || (degree.get(b.node.id) || 0) - (degree.get(a.node.id) || 0))
      .slice(0, 8).map(result => result.node);
  }

  function showResults() {
    const query = search.value.trim();
    results.hidden = !query;
    search.setAttribute('aria-expanded', query ? 'true' : 'false');
    if (!query) return;
    results.innerHTML = searchChoices.length ? searchChoices.map((node, i) => {
      const parts = node.label.split(' · ');
      return `<button type="button" role="option" aria-selected="${i === searchCursor}" class="result${i === searchCursor ? ' active' : ''}" data-index="${i}"><strong>${esc(parts[0])}</strong><small>${esc(parts.slice(1).join(' · ') || node.kind)}</small></button>`;
    }).join('') : '<div class="empty">No matching person or text</div>';
  }

  function chooseSearch(index, close = false) {
    const node = searchChoices[index];
    if (!node) return;
    if (!activeNodes.some(active => active.id === node.id)) {
      tradition.value = 'all'; radius.value = 'all';
      if (node.kind === 'source') sources.checked = true;
      rebuild();
    }
    focusOn(node.id);
    if (close) { results.hidden = true; search.setAttribute('aria-expanded', 'false'); }
  }

  const pick = event => {
    if (!pointCloud) return null;
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.set(((event.clientX - rect.left) / rect.width) * 2 - 1, -((event.clientY - rect.top) / rect.height) * 2 + 1);
    raycaster.setFromCamera(pointer, camera);
    const hit = raycaster.intersectObject(pointCloud, false)[0];
    return hit ? activeNodes[hit.index] : null;
  };
  let down = null;
  renderer.domElement.addEventListener('pointerdown', event => { down = { x: event.clientX, y: event.clientY }; results.hidden = true; });
  renderer.domElement.addEventListener('pointerup', event => {
    if (!down) return;
    const moved = Math.hypot(event.clientX - down.x, event.clientY - down.y);
    down = null;
    if (moved < 4) { const node = pick(event); if (node) focusOn(node.id); }
  });
  renderer.domElement.addEventListener('pointermove', event => {
    if (down) return;
    const node = pick(event);
    renderer.domElement.style.cursor = node ? 'pointer' : 'grab';
    renderer.domElement.title = node?.label || '';
  });
  renderer.domElement.addEventListener('pointercancel', () => { down = null; });
  renderer.domElement.addEventListener('pointerdown', () => { flight = null; });
  renderer.domElement.addEventListener('wheel', () => { flight = null; }, { passive: true });

  tradition.addEventListener('change', rebuild);
  radius.addEventListener('change', rebuild);
  sources.addEventListener('change', rebuild);
  search.addEventListener('input', () => {
    searchChoices = findMatches(search.value); searchCursor = 0; showResults();
    if (fold(search.value).length >= 2) chooseSearch(0);
  });
  search.addEventListener('keydown', event => {
    if (event.key === 'Escape') { results.hidden = true; search.setAttribute('aria-expanded', 'false'); return; }
    if (!searchChoices.length) return;
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      event.preventDefault();
      searchCursor = (searchCursor + (event.key === 'ArrowDown' ? 1 : -1) + searchChoices.length) % searchChoices.length;
      showResults(); chooseSearch(searchCursor);
    } else if (event.key === 'Enter') { event.preventDefault(); chooseSearch(searchCursor, true); }
  });
  results.addEventListener('click', event => {
    const option = event.target.closest('[data-index]');
    if (option) { searchCursor = Number(option.dataset.index); chooseSearch(searchCursor, true); }
  });
  fit.addEventListener('click', () => fitAll(true));
  pause.addEventListener('click', () => { playing = !playing; pause.textContent = playing ? 'Pause motion' : 'Resume motion'; });

  function resize() {
    const width = Math.max(300, stage.clientWidth), height = Math.max(300, stage.clientHeight);
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }
  new ResizeObserver(resize).observe(stage);
  resize();
  rebuild();

  function animate(now) {
    if (playing && now - lastPhysics >= 30) {
      forces(Math.min(45, now - lastPhysics || 16));
      lastPhysics = now;
    }
    if (flight) {
      const progress = Math.min(1, (now - flight.start) / flight.duration);
      const eased = progress * progress * (3 - 2 * progress);
      camera.position.lerpVectors(flight.fromPosition, flight.toPosition, eased);
      controls.target.lerpVectors(flight.fromTarget, flight.toTarget, eased);
      if (progress >= 1) flight = null;
    }
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
})();
