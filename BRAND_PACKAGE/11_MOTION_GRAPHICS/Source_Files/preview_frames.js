#!/usr/bin/env node
/**
 * preview_frames.js — quick look at an animation source before a full render: steps every animation to the given
 * times (same mechanism as the kit's capture_frames.js) and writes one PNG per time, plus a labelled strip.
 *   node preview_frames.js --in story-quote/index.html --width 1080 --height 1920 --times 0.8,1.4,2.2,5.9 --out /tmp/sz-motion/pv-story-quote
 * Writes <out>--t<time>.png and <out>--strip.png (frames scaled to 420 px wide).
 */
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path'); const fs = require('fs');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), (arr[i+1] && !arr[i+1].startsWith('--')) ? arr[i+1] : true]); return a; }, []));
(async () => {
  const width = parseInt(args.width || 1920), height = parseInt(args.height || 1080);
  const times = (args.times || '0,1,2,3').split(',').map(Number); const out = args.out || 'preview';
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
  const page = await ctx.newPage(); const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('file://' + path.resolve(args.in), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(200);
  await page.evaluate(() => { document.getAnimations({ subtree: true }).forEach(a => { a.pause(); a.currentTime = 0; }); });
  const n = await page.evaluate(() => document.getAnimations({ subtree: true }).length);
  const files = [];
  for (const t of times) {
    await page.evaluate(t => { document.getAnimations({ subtree: true }).forEach(a => { a.currentTime = t; }); }, t * 1000);
    const f = `${out}--t${t.toFixed(2)}s.png`; await page.screenshot({ path: f, omitBackground: !!args.transparent }); files.push([t, f]);
  }
  await browser.close();
  const py = `
from PIL import Image, ImageDraw, ImageFont
import json, sys
files = json.loads(sys.argv[1]); label = sys.argv[2]
ims = [Image.open(f).convert('RGB') for _, f in files]
tw = 420; th = int(ims[0].height * tw / ims[0].width); pad = 12; top = 40
sheet = Image.new('RGB', (pad + (tw + pad) * len(ims), top + th + pad + 22), (28, 28, 30))
d = ImageDraw.Draw(sheet); f = ImageFont.truetype('/home/user/claude-skills/BRAND_PACKAGE/04_TYPOGRAPHY/Font_Files/Inter/Inter[opsz,wght].ttf', 16)
d.text((pad, 12), label, fill=(245, 245, 247), font=f)
for i, ((t, _), im) in enumerate(zip(files, ims)):
    x = pad + i * (tw + pad); sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, top)); d.text((x, top + th + 4), f'{t:.2f} s', fill=(161, 161, 166), font=f)
sheet.save(sys.argv[3])
`;
  fs.writeFileSync('/tmp/sz-motion/_pvstrip.py', py);
  execSync(`python3 /tmp/sz-motion/_pvstrip.py '${JSON.stringify(files)}' "${path.basename(path.dirname(path.resolve(args.in)))}/${path.basename(args.in)} · ${width}×${height} · ${n} animations" "${out}--strip.png"`);
  console.log(`${n} animations; ${errors.length ? 'PAGE ERRORS: ' + errors.join(' | ') : 'no page errors'} -> ${out}--strip.png`);
})();
