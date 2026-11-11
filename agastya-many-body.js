// Exact repulsion for small views; Barnes-Hut approximation for large views.
function repulsion(ns, particles, dimensions, fx, fy, fz, sourceWeighted) {
  const count = ns.length;
  const points = ns.map(n => particles.get(n.id));
  const add = (i, dx, dy, dz, weight) => {
    const r2 = dx * dx + dy * dy + (dimensions === 3 ? dz * dz : 0) + 1600;
    const mag = weight * Math.min(120, 12000 / r2) / Math.sqrt(r2);
    fx[i] += dx * mag;
    fy[i] += dy * mag;
    if (dimensions === 3) fz[i] += dz * mag;
  };
  if (count <= 420) {
    for (let i = 0; i < count; i++) {
      for (let j = i + 1; j < count; j++) {
        const a = points[i], b = points[j];
        const weight = sourceWeighted && (ns[i].kind === 'source' || ns[j].kind === 'source') ? .72 : 1;
        const dx = a.x - b.x, dy = a.y - b.y, dz = dimensions === 3 ? a.z - b.z : 0;
        add(i, dx, dy, dz, weight);
        add(j, -dx, -dy, -dz, weight);
      }
    }
    return;
  }

  let minX = Infinity, minY = Infinity, minZ = Infinity;
  let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;
  for (const p of points) {
    minX = Math.min(minX, p.x); maxX = Math.max(maxX, p.x);
    minY = Math.min(minY, p.y); maxY = Math.max(maxY, p.y);
    if (dimensions === 3) { minZ = Math.min(minZ, p.z); maxZ = Math.max(maxZ, p.z); }
  }
  const half = Math.max(maxX - minX, maxY - minY, dimensions === 3 ? maxZ - minZ : 0, 2) / 2 + 1;
  const make = (x, y, z, h) => ({ x, y, z, h, children: null, items: [], mass: 0, sources: 0, sx: 0, sy: 0, sz: 0 });
  const root = make((minX + maxX) / 2, (minY + maxY) / 2,
    dimensions === 3 ? (minZ + maxZ) / 2 : 0, half);
  const childIndex = (cell, p) => (p.x >= cell.x ? 1 : 0) + (p.y >= cell.y ? 2 : 0) +
    (dimensions === 3 && p.z >= cell.z ? 4 : 0);
  const child = (cell, index) => {
    if (!cell.children) cell.children = Array(1 << dimensions);
    if (!cell.children[index]) {
      const h = cell.h / 2;
      cell.children[index] = make(cell.x + (index & 1 ? h : -h),
        cell.y + (index & 2 ? h : -h),
        dimensions === 3 ? cell.z + (index & 4 ? h : -h) : 0, h);
    }
    return cell.children[index];
  };
  const insert = (cell, index, depth) => {
    const p = points[index];
    cell.mass++;
    if (ns[index].kind === 'source') cell.sources++;
    cell.sx += p.x; cell.sy += p.y; if (dimensions === 3) cell.sz += p.z;
    if (!cell.children && (cell.items.length === 0 || depth >= 24)) {
      cell.items.push(index);
      return;
    }
    if (!cell.children) {
      const old = cell.items;
      cell.items = [];
      for (const prior of old) insert(child(cell, childIndex(cell, points[prior])), prior, depth + 1);
    }
    insert(child(cell, childIndex(cell, p)), index, depth + 1);
  };
  for (let i = 0; i < count; i++) insert(root, i, 0);

  const theta2 = 1.45 * 1.45;
  for (let i = 0; i < count; i++) {
    const p = points[i], source = ns[i].kind === 'source';
    const visit = cell => {
      if (!cell || !cell.mass) return;
      if (!cell.children) {
        for (const j of cell.items) {
          if (j === i) continue;
          const q = points[j];
          const weight = sourceWeighted && (source || ns[j].kind === 'source') ? .72 : 1;
          add(i, p.x - q.x, p.y - q.y, dimensions === 3 ? p.z - q.z : 0, weight);
        }
        return;
      }
      const dx = p.x - cell.sx / cell.mass, dy = p.y - cell.sy / cell.mass;
      const dz = dimensions === 3 ? p.z - cell.sz / cell.mass : 0;
      const distance2 = dx * dx + dy * dy + dz * dz;
      const contains = Math.abs(p.x - cell.x) <= cell.h && Math.abs(p.y - cell.y) <= cell.h &&
        (dimensions !== 3 || Math.abs(p.z - cell.z) <= cell.h);
      if (!contains && 4 * cell.h * cell.h < theta2 * distance2) {
        const weight = !sourceWeighted ? cell.mass : source ? .72 * cell.mass : cell.mass - .28 * cell.sources;
        add(i, dx, dy, dz, weight);
      } else {
        for (const sub of cell.children) if (sub) visit(sub);
      }
    };
    visit(root);
  }
}
