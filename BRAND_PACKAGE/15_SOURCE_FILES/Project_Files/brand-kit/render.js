#!/usr/bin/env node
/**
 * render.js — render an HTML file to PNG or PDF with Chromium (Playwright).
 *   node render.js --in page.html --out out.png --width 1080 --height 1080 [--scale 2] [--full] [--wait 400] [--selector ".card"] [--transparent]
 *   node render.js --in doc.html  --out out.pdf --pdf --size 210x297 [--landscape] [--wait 600]
 * Sizes for PDF are in millimetres (page.pdf uses CSS @page if present; --size is the fallback).
 * Waits for document.fonts.ready so the OFL web fonts are always rendered.
 */
const { chromium } = require('playwright');
const path = require('path');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), (arr[i+1] && !arr[i+1].startsWith('--')) ? arr[i+1] : true]); return a; }, []));
(async () => {
  if (!args.in || !args.out) { console.error('usage: --in file.html --out file.(png|pdf) [--width --height --scale --full --pdf --size WxH(mm) --landscape --wait --selector --transparent --js "code"]'); process.exit(1); }
  const browser = await chromium.launch();
  const width = parseInt(args.width || 1440), height = parseInt(args.height || 900);
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: parseFloat(args.scale || 2) });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.error('[pageerror]', e.message));
  await page.goto('file://' + path.resolve(args.in), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  if (args.js) await page.evaluate(args.js);
  await page.waitForTimeout(parseInt(args.wait || 300));
  if (args.pdf) {
    const [w, h] = (args.size || '210x297').split('x').map(Number);
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: args.out, width: `${w}mm`, height: `${h}mm`, landscape: !!args.landscape, printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  } else {
    const opts = { path: args.out, omitBackground: !!args.transparent, fullPage: !!args.full, type: args.out.endsWith('.jpg') ? 'jpeg' : 'png' };
    if (opts.type === 'jpeg') opts.quality = 92;
    if (args.selector) await page.locator(args.selector).first().screenshot(opts); else await page.screenshot(opts);
  }
  await browser.close();
  console.log('wrote', args.out);
})();
