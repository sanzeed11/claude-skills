#!/usr/bin/env node
/* render_batch.js — same behaviour as brand-kit/render.js, but renders a JSON list of jobs in one Chromium.
   node render_batch.js jobs.json      jobs: [{in, out, width, height, scale, full, pdf, size:"WxH", landscape, wait, selector, transparent, jpgQuality}]
   Used only to regenerate the whole folder quickly; every job can be reproduced one-by-one with render.js. */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const width = parseInt(j.width || 1440), height = parseInt(j.height || 900);
    const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: parseFloat(j.scale || 2) });
    const page = await ctx.newPage();
    page.on('pageerror', e => console.error('[pageerror]', j.in, e.message));
    page.on('requestfailed', r => console.error('[requestfailed]', j.in, r.url()));
    await page.goto('file://' + path.resolve(j.in), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(parseInt(j.wait || 300));
    if (j.pdf) {
      const [w, h] = (j.size || '210x297').split('x').map(Number);
      await page.emulateMedia({ media: 'print' });
      await page.pdf({ path: j.out, width: `${w}mm`, height: `${h}mm`, landscape: !!j.landscape, printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    } else {
      const opts = { path: j.out, omitBackground: !!j.transparent, fullPage: !!j.full, type: j.out.endsWith('.jpg') ? 'jpeg' : 'png' };
      if (opts.type === 'jpeg') opts.quality = j.jpgQuality || 88;
      if (j.selector) await page.locator(j.selector).first().screenshot(opts); else await page.screenshot(opts);
    }
    await ctx.close();
    console.log('wrote', j.out);
  }
  await browser.close();
})();
