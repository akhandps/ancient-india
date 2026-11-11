import { CanvasTexture, Sprite, SpriteMaterial } from 'three';

const canvas = document.createElement('canvas');
canvas.width = canvas.height = 64;
const context = canvas.getContext('2d');
const glow = context.createRadialGradient(32, 32, 20, 32, 32, 31);
glow.addColorStop(0, 'rgba(255,255,255,1)');
glow.addColorStop(0.76, 'rgba(255,255,255,1)');
glow.addColorStop(0.93, 'rgba(255,255,255,0.86)');
glow.addColorStop(1, 'rgba(255,255,255,0)');
context.fillStyle = glow;
context.fillRect(0, 0, 64, 64);
const texture = new CanvasTexture(canvas);

window.agastyaCircleSprite = (node, color, degree = 0) => {
  const material = new SpriteMaterial({ map: texture, color, transparent: true, depthWrite: false });
  const sprite = new Sprite(material);
  const size = node.kind === 'hub' ? 26 : node.kind === 'source' ? 6 : node.kind === 'text' ? 16 : 10 + Math.min(10, Math.sqrt(degree) * 1.2);
  sprite.scale.set(size, size, 1);
  return sprite;
};
