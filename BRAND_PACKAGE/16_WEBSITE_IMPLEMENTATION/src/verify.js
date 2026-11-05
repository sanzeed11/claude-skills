#!/usr/bin/env node
/**
 * verify.js — loads the built site (and the untouched backup as "before") in headless Chromium and checks:
 *   console/page errors, failed requests (404s), fonts resolved (document.fonts), wordmark SVG geometry,
 *   theme toggle, gallery filter + search, favicon/manifest/OG files return 200.
 * Writes screenshots/ (desktop + mobile, dark + light, before/after, header @2×) and screenshots/verify-report.json.
 *   node 16_WEBSITE_IMPLEMENTATION/src/verify.js [--before <dir>]
 */
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const http = require('http'), path = require('path'), fs = require('fs');
const SITE = path.resolve(__dirname, '..'), SHOTS = path.join(SITE, 'screenshots');
const argv = process.argv.slice(2); const bi = argv.indexOf('--before'); const BEFORE = bi >= 0 ? argv[bi + 1] : null;
fs.mkdirSync(SHOTS, { recursive: true });
const EXTERNAL = /gc\.zgo\.at|goatcounter|drive\.google|googleapis|gstatic|unpkg|cdn/;
const PAGES = [['index', '/'], ['work-prime-minister-museum', '/work/prime-minister-museum.html'], ['work-ram-katha-show', '/work/ram-katha-show.html'], ['work-buddha-park', '/work/buddha-park.html']];
const VIEWPORTS = [['desktop', 1440, 900], ['mobile', 390, 844]];

function serve(dir, port) { const p = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1'], { cwd: dir, stdio: 'ignore' }); return p; }
function ready(port) { return new Promise((res) => { const t = () => http.get({ host: '127.0.0.1', port, path: '/' }, (r) => { r.resume(); res(); }).on('error', () => setTimeout(t, 150)); t(); }); }
const jpg = (file) => ({ path: path.join(SHOTS, file), type: 'jpeg', quality: 85 });

async function scrollThrough(page) {           // trigger lazy images + reveal animations, then return to top
  await page.evaluate(async () => {
    const go = (y) => { if (window.__lenis) window.__lenis.scrollTo(y, { immediate: true }); window.scrollTo(0, y); };
    const h = () => document.documentElement.scrollHeight; const step = Math.max(600, innerHeight * .8);
    for (let y = 0; y < h(); y += step) { go(y); await new Promise(r => setTimeout(r, 90)); }
    go(h()); await new Promise(r => setTimeout(r, 500)); go(0); await new Promise(r => setTimeout(r, 400));
  });
}
async function settle(page) {
  await page.waitForFunction(() => document.documentElement.classList.contains('loaded'), null, { timeout: 12000 }).catch(() => {});
  await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(900);
}

async function audit(browser, base, name, url, vp, label) {
  const [vn, w, h] = vp; const tag = `${label}-${name}-${vn}`;
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, colorScheme: 'dark' });
  const page = await ctx.newPage(); const errors = [], failed = [];
  page.on('console', (m) => { if (m.type() === 'error') { const l = m.location() || {}; errors.push(m.text() + (l.url ? ' @ ' + l.url : '')); } });
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('response', (r) => { if (r.status() >= 400) failed.push(`${r.status()} ${r.url()}`); });
  page.on('requestfailed', (r) => failed.push(`FAILED ${r.url()} ${(r.failure() || {}).errorText || ''}`));
  await page.goto(base + url, { waitUntil: 'load' }); await settle(page);
  const r = { page: name, viewport: vn, url };
  r.fonts = await page.evaluate(() => ({
    status: document.fonts.status,
    loaded: [...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family} ${f.style} ${f.weight}`),
    h1: getComputedStyle(document.querySelector('h1') || document.body).fontFamily.split(',')[0],
    h1weight: getComputedStyle(document.querySelector('h1') || document.body).fontWeight,
    fraunces: document.fonts.check('300 48px Fraunces'), inter: document.fonts.check('400 16px Inter'), tight: document.fonts.check('600 12px "Inter Tight"'),
  }));
  r.wordmark = await page.evaluate(() => { const s = document.querySelector('.brand svg'); if (!s) return null; const b = s.getBoundingClientRect(); const p = s.querySelector('.wm-letters');
    return { viewBox: s.getAttribute('viewBox'), width: +b.width.toFixed(1), height: +b.height.toFixed(1), letters: !!p, pathLen: p ? +p.getTotalLength().toFixed(0) : 0, fill: p && getComputedStyle(p).fill, dots: s.querySelectorAll('.wm-dot').length,
      lockup: !!document.querySelector('.f-lockup svg'), lockupDesc: document.querySelectorAll('.f-lockup .wm-desc path').length, loaderClip: !!document.querySelector('#ldClip rect') }; });
  await scrollThrough(page);
  r.signature = await page.evaluate(() => [...document.querySelectorAll('.foot2 .sig img')].map(i => ({ src: i.getAttribute('src'), ok: i.complete && i.naturalWidth > 0 })));
  await page.waitForTimeout(400);
  await page.screenshot({ ...jpg(`${tag}-dark-full.jpg`), fullPage: true });
  await page.screenshot(jpg(`${tag}-dark.jpg`));
  if (name === 'index') {                                  // galleries: filter + search
    await page.evaluate(() => { const el = document.querySelector('#collection'); (window.__lenis ? window.__lenis.scrollTo(el, { immediate: true, offset: -80 }) : el.scrollIntoView()); });
    await page.waitForTimeout(600);
    const count = () => page.evaluate(() => [...document.querySelectorAll('.collection .card')].filter(c => c.getClientRects().length && getComputedStyle(c).visibility !== 'hidden').length);
    const before = await count();
    await page.evaluate(() => document.querySelector('button[data-cat="projection"]').click()); await page.waitForTimeout(700);
    const afterFilter = await count(); const pressed = await page.evaluate(() => document.querySelector('.seg button[aria-pressed="true"]').dataset.cat);
    await page.screenshot(jpg(`${tag}-dark-gallery-filter-projection.jpg`));
    await page.fill('#search', 'Ayodhya'); await page.waitForTimeout(700); const afterSearch = await count();
    await page.evaluate(() => document.querySelector('#searchClear').click()); await page.evaluate(() => document.querySelector('button[data-cat="work"]').click()); await page.waitForTimeout(500);
    r.gallery = { visibleDefault: before, visibleProjection: afterFilter, pressed, visibleSearchAyodhya: afterSearch };
    await page.evaluate(() => { const go = (y) => { if (window.__lenis) window.__lenis.scrollTo(y, { immediate: true }); window.scrollTo(0, y); }; go(0); }); await page.waitForTimeout(400);
  }
  // theme toggle
  await page.evaluate(() => document.querySelector('.theme').click()); await page.waitForTimeout(name === 'index' ? 2600 : 900);   // index cross-fades via View Transitions
  r.theme = await page.evaluate(() => ({ after: document.documentElement.getAttribute('data-theme'), bg: getComputedStyle(document.body).backgroundColor, fg: getComputedStyle(document.body).color }));
  await page.screenshot(jpg(`${tag}-light.jpg`));
  await page.screenshot({ ...jpg(`${tag}-light-full.jpg`), fullPage: true });
  r.errors = errors; r.failed = failed;
  r.localFailures = failed.filter(f => !EXTERNAL.test(f)); r.localErrors = errors.filter(e => !EXTERNAL.test(e));
  await ctx.close(); return r;
}

async function loaderFrames(browser, base, label) {   // the loader: clip-path wipe + travelling beam dot on the new artwork
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, colorScheme: 'dark' });
  const page = await ctx.newPage(); await page.goto(base + '/', { waitUntil: 'commit' });
  await page.waitForSelector('.loader .wm svg'); await page.waitForTimeout(420);
  await page.screenshot(jpg(`${label}-index-desktop-loader-frame.jpg`)); await ctx.close();
}
async function headerShots(browser, base, name, url, label) {
  for (const [vn, w, h] of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, colorScheme: 'dark' });
    const page = await ctx.newPage(); await page.goto(base + url, { waitUntil: 'load' }); await settle(page); await page.waitForTimeout(600);
    await page.locator('header.nav').screenshot({ path: path.join(SHOTS, `${label}-${name}-${vn}-header-2x.png`) });
    await page.evaluate(() => document.querySelector('.theme').click()); await page.waitForTimeout(700);
    await page.locator('header.nav').screenshot({ path: path.join(SHOTS, `${label}-${name}-${vn}-header-2x-light.png`) });
    if (label === 'after') { await scrollThrough(page); await page.evaluate(() => { const el = document.querySelector('.foot2'); el.scrollIntoView(); }); await page.waitForTimeout(1200);
      await page.locator('.foot2').screenshot({ path: path.join(SHOTS, `${label}-${name}-${vn}-footer-2x-light.png`) }); }
    await ctx.close();
  }
}

async function files(browser, base) {
  const ctx = await browser.newContext(); const page = await ctx.newPage(); await page.goto(base + '/', { waitUntil: 'domcontentloaded' });
  const hrefs = await page.evaluate(() => [...document.querySelectorAll('link[rel~="icon"],link[rel="apple-touch-icon"],link[rel="mask-icon"],link[rel="manifest"],link[rel="preload"]')].map(l => l.href));
  const ogs = [];
  for (const [, url] of PAGES) { await page.goto(base + url, { waitUntil: 'domcontentloaded' }); ogs.push(...await page.evaluate(() => [...document.querySelectorAll('meta[property="og:image"],meta[name="twitter:image"]')].map(m => m.content))); }
  const man = await page.request.get(base + '/site.webmanifest'); const manifest = man.ok() ? await man.json() : null;
  const list = [...new Set([...hrefs, ...ogs.map(u => u.replace('https://sanzeed.com', base)), ...(manifest ? manifest.icons.map(i => base + i.src) : []), base + '/sitemap.xml', base + '/robots.txt', base + '/sanzeed-mirza.vcf', base + '/img/sanzeed-signature--white.svg', base + '/img/sanzeed-signature--ink.svg'])];
  const out = {}; for (const u of list) { const r = await page.request.get(u); out[u.replace(base, '')] = r.status() + ' ' + (r.headers()['content-type'] || ''); }
  await ctx.close(); return out;
}

(async () => {
  const srv = serve(SITE, 8765); await ready(8765); const base = 'http://127.0.0.1:8765';
  let bsrv = null, bbase = null; if (BEFORE) { bsrv = serve(BEFORE, 8766); await ready(8766); bbase = 'http://127.0.0.1:8766'; }
  const browser = await chromium.launch(); const report = { after: [], before: [], files: {} };
  try {
    for (const [name, url] of PAGES) { for (const vp of VIEWPORTS) { const r = await audit(browser, base, name, url, vp, 'after'); report.after.push(r); console.log('after', name, vp[0], 'errors', r.localErrors.length, 'failed', r.localFailures.length, 'fonts', r.fonts.fraunces, r.fonts.inter, r.fonts.tight, 'wm', JSON.stringify(r.wordmark && [r.wordmark.width, r.wordmark.height]), 'theme', r.theme.after, r.gallery ? JSON.stringify(r.gallery) : ''); } }
    await loaderFrames(browser, base, 'after');
    for (const [name, url] of PAGES) await headerShots(browser, base, name, url, 'after');
    report.files = await files(browser, base); console.log('files', JSON.stringify(report.files, null, 1));
    if (bbase) { for (const [name, url] of PAGES.slice(0, 2)) { for (const vp of VIEWPORTS) { const r = await audit(browser, bbase, name, url, vp, 'before'); report.before.push(r); console.log('before', name, vp[0], 'errors', r.localErrors.length, 'failed', r.localFailures.length); } }
      await headerShots(browser, bbase, 'index', '/', 'before'); }
  } finally { await browser.close(); srv.kill(); if (bsrv) bsrv.kill(); }
  fs.writeFileSync(path.join(SHOTS, 'verify-report.json'), JSON.stringify(report, null, 2));
  const bad = report.after.filter(r => r.localErrors.length || r.localFailures.length);
  console.log(bad.length ? 'PROBLEMS: ' + JSON.stringify(bad.map(r => [r.page, r.viewport, r.localErrors, r.localFailures]), null, 1) : 'OK — no local errors or failed requests');
})();
