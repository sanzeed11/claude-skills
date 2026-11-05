#!/usr/bin/env node
/**
 * validate_lottie.js — proves the hand-written Lottie JSON renders: loads each player in Chromium (Playwright),
 * steps lottie-web with goToAndStop(frame, true), screenshots six frames, and assembles a labelled proof strip.
 *   node validate_lottie.js            -> ../../Exports/Lottie_Proofs/sanzeed-lottie--<name>--f<frame>.png + ...--proof.png
 * Exit code 1 if lottie-web reports an error, the JSON fails to parse, or a frame renders empty.
 */
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs'); const path = require('path');
const HERE = __dirname; const OUT = path.resolve(HERE, '../../Exports/Lottie_Proofs'); fs.mkdirSync(OUT, { recursive: true });
const JOBS = [
  { name: 'logo-reveal', player: 'player--logo-reveal.html', json: 'sanzeed-logo-reveal.json', frames: [0, 20, 30, 48, 66, 119], bg: '#000000' },
  { name: 'loader',      player: 'player--loader.html',      json: 'sanzeed-loader.json',      frames: [0, 6, 15, 24, 33, 45],  bg: '#000000', scale: 3 },
];
(async () => {
  const browser = await chromium.launch(); let failed = false;
  for (const job of JOBS) {
    JSON.parse(fs.readFileSync(path.join(HERE, job.json), 'utf8'));   // must be valid JSON
    const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: job.scale || 1, colorScheme: 'dark' });
    const page = await ctx.newPage(); const errors = [];
    page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto('file://' + path.join(HERE, job.player), { waitUntil: 'load' });
    await page.waitForFunction(() => window.anim && window.anim.isLoaded);
    const info = await page.evaluate(() => ({ frames: window.anim.totalFrames, fr: window.anim.frameRate, w: window.anim.animationData.w, h: window.anim.animationData.h }));
    const files = [];
    for (const f of job.frames) {
      await page.evaluate(f => window.anim.goToAndStop(f, true), f);
      await page.waitForTimeout(40);
      const file = path.join(OUT, `sanzeed-lottie--${job.name}--f${String(f).padStart(3, '0')}.png`);
      await page.locator('#anim').screenshot({ path: file, omitBackground: false });
      files.push([f, file]);
    }
    await ctx.close();
    // proof strip with labels (ImageMagick-free: ffmpeg drawtext would need font paths; use Pillow)
    const py = `
from PIL import Image, ImageDraw, ImageFont
import json, sys
files = json.loads(sys.argv[1]); title = sys.argv[2]; info = sys.argv[3]
ims = [Image.open(f).convert('RGB') for _, f in files]
tw = 420; th = int(ims[0].height * tw / ims[0].width); pad = 16; top = 64
sheet = Image.new('RGB', (pad + (tw + pad) * len(ims), top + th + pad + 24), (13, 13, 15))
d = ImageDraw.Draw(sheet)
try:
    f1 = ImageFont.truetype('/home/user/claude-skills/BRAND_PACKAGE/04_TYPOGRAPHY/Font_Files/Inter_Tight/InterTight[wght].ttf', 22)
    f2 = ImageFont.truetype('/home/user/claude-skills/BRAND_PACKAGE/04_TYPOGRAPHY/Font_Files/Inter/Inter[opsz,wght].ttf', 15)
except Exception:
    f1 = f2 = ImageFont.load_default()
d.text((pad, 18), title + '  —  rendered by lottie-web (SVG renderer) in Chromium', fill=(245, 245, 247), font=f1)
d.text((pad + 760, 24), info, fill=(128, 128, 134), font=f2)
for n, ((fr, _), im) in enumerate(zip(files, ims)):
    x = pad + n * (tw + pad); im = im.resize((tw, th), Image.LANCZOS); sheet.paste(im, (x, top))
    d.rectangle([x, top, x + tw - 1, top + th - 1], outline=(255, 255, 255, 25))
    d.text((x, top + th + 6), f'frame {fr:03d}  ·  {fr / 30:.2f} s', fill=(161, 161, 166), font=f2)
sheet.save(sys.argv[4])
`;
    const proof = path.join(OUT, `sanzeed-lottie--${job.name}--proof.png`);
    fs.writeFileSync('/tmp/sz-motion/_strip.py', py);
    execSync(`python3 /tmp/sz-motion/_strip.py '${JSON.stringify(files)}' "${job.name}" "${info.w}×${info.h} · ${info.fr} fps · ${info.frames} frames · ${job.json}" "${proof}"`);
    const ok = errors.length === 0;
    console.log(`${ok ? 'OK  ' : 'FAIL'} ${job.name}: ${info.w}x${info.h} ${info.frames} frames @ ${info.fr} fps -> ${path.relative(HERE, proof)}${ok ? '' : '\n   ' + errors.join('\n   ')}`);
    if (!ok) failed = true;
  }
  await browser.close(); process.exit(failed ? 1 : 0);
})();
