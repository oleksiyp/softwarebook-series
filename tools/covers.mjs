// Renders each book's front cover and spine at landing-page size from the books' own wrap.svg:
// node tools/covers.mjs  → assets/books/<key>-{front,spine}.png (then cwebp them). Run from this repo, beside the book repos.
import puppeteer from '../../resilient-systems/cover-lab/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, '../assets/books');
const BOOKS = {
  architecture: { svg: '../../arch-site/assets/cover/wrap.svg', spineW: 55 },
  products:     { svg: '../../buildproducts-book/assets/cover/wrap.svg', spineW: 75 },
  software:     { svg: '../../buildsoftware-book/assets/cover/wrap.svg', spineW: 80 },
  resilience:   { svg: '../../resilient-systems/assets/cover/wrap.svg', spineW: 75 },
  operations:   { svg: '../../prod-systems/assets/cover/wrap.svg', spineW: 70 },
};
const FRONT_PX = 800;   // ~2x the largest size the landing page shows a cover

const browser = await puppeteer.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
const page = await browser.newPage();
for (const [key, b] of Object.entries(BOOKS)) {
  const svg = fs.readFileSync(path.join(here, b.svg), 'utf8');
  const W = 12.5 + 600 + b.spineW + 600 + 12.5;
  const scale = FRONT_PX / 600;
  const H = Math.round(900 * scale);
  const shots = { spine: { x: 612.5, w: b.spineW }, front: { x: 612.5 + b.spineW, w: 600 } };
  for (const [part, r] of Object.entries(shots)) {
    const w = Math.round(r.w * scale);
    await page.setViewport({ width: w, height: H });
    await page.setContent(`<html><body style="margin:0;overflow:hidden">
      <div style="width:${w}px;height:${H}px;overflow:hidden;position:relative">
      <div style="position:absolute;left:${-r.x * scale}px;top:${-12.5 * scale}px;width:${W * scale}px;height:${925 * scale}px">
      ${svg.replace(/<\?xml[^>]*>/, '').replace('<svg ', `<svg width="${W * scale}" height="${925 * scale}" `)}
      </div></div></body></html>`);
    await page.screenshot({ path: path.join(out, `${key}-${part}.png`), clip: { x: 0, y: 0, width: w, height: H } });
  }
}
await browser.close();
console.log('covers done');
