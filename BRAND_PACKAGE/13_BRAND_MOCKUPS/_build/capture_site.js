#!/usr/bin/env node
/**
 * capture_site.js — screenshot the real site (16_WEBSITE_IMPLEMENTATION) at device pixel density for the device mockups.
 *   node capture_site.js --in ../../16_WEBSITE_IMPLEMENTATION/index.html --out plates/site-desktop-dark.png --width 1440 --height 900 --scale 2 [--theme light]
 * Waits for the site's own `loaded` class and fonts, freezes CSS animations, then screenshots the viewport.
 */
const { chromium } = require('playwright');
const path = require('path');
const a = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, arr) => { if (v.startsWith('--')) acc.push([v.slice(2), (arr[i+1] && !arr[i+1].startsWith('--')) ? arr[i+1] : true]); return acc; }, []));
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +a.width || 1440, height: +a.height || 900 }, deviceScaleFactor: +a.scale || 2, colorScheme: a.theme === 'light' ? 'light' : 'dark' });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(a.in), { waitUntil: 'load' });
  await page.waitForFunction(() => document.documentElement.classList.contains('loaded'), null, { timeout: 15000 }).catch(() => {});
  if (a.theme === 'light') { await page.evaluate(() => document.querySelector('.theme').click()); await page.waitForTimeout(2800); }   // the site's own toggle (index cross-fades via View Transitions)
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(+a.wait || 2500);
  await page.screenshot({ path: a.out, animations: 'disabled', timeout: 120000, caret: 'hide' });
  await browser.close();
  console.log('wrote', a.out);
})();
