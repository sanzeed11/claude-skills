#!/usr/bin/env node
/**
 * verify.js — loads the built site (and the untouched backup as "before") in headless Chromium and checks:
 *   console/page errors, failed requests (404s), fonts resolved (document.fonts), wordmark SVG geometry,
 *   theme toggle, gallery filter + search, favicon/manifest/OG files return 200.
 * Writes screenshots/ (desktop + mobile, dark + light, before/after, header + footer @2×) and screenshots/verify-report.json.
 *   The footer captures wait for the signature write-on to finish (the site restarts it every 5 s) and pin the end state.
 *   node 16_WEBSITE_IMPLEMENTATION/src/verify.js [--before <dir>]
 */
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const http = require('http'), path = require('path'), fs = require('fs');
const SITE = path.resolve(__dirname, '..'), SHOTS = path.join(SITE, 'screenshots');
const argv = process.argv.slice(2); const LOADER_ONLY = argv.includes('--loader-only'); const bi = argv.indexOf('--before'); const BEFORE = bi >= 0 ? argv[bi + 1] : null;
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

/* the home page switches theme through a View Transitions cross-fade (≈ 2 s); wait until the body has the new
   background (Plaster / Gallery Black) instead of a fixed delay, then let the transition paint */
async function themeSettled(page, minWait) {
  await page.waitForTimeout(minWait);
  await page.waitForFunction(() => { const t = document.documentElement.getAttribute('data-theme'); const bg = getComputedStyle(document.body).backgroundColor;
    return t === 'light' ? bg === 'rgb(245, 240, 231)' : bg === 'rgb(0, 0, 0)' || bg === 'rgb(13, 13, 15)'; }, null, { timeout: 9000, polling: 100 }).catch(() => {});
  await page.waitForTimeout(600);
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
    const paths = [...s.querySelectorAll('path.wm-letters, .wm-letters path')]; const ink = p && p.getBBox ? p.getBBox() : null; const k = b.height / s.viewBox.baseVal.height;
    const lk = [...document.querySelectorAll('.f-lockup .wm-dot')];
    return { viewBox: s.getAttribute('viewBox'), width: +b.width.toFixed(1), height: +b.height.toFixed(1), inkWidth: ink ? +(ink.width * k).toFixed(1) : 0, letters: !!p, letterPaths: paths.map(x => x.dataset.letter || '').join(' '),
      pathLen: paths.reduce((a, x) => a + x.getTotalLength(), 0).toFixed(0) * 1, fill: p && getComputedStyle(p).fill, dots: s.querySelectorAll('.wm-dot').length,
      dotCx: [...s.querySelectorAll('.wm-dot')].map(c => +c.getAttribute('cx')), dotFill: getComputedStyle(s.querySelector('.wm-dot')).fill,
      lockup: !!document.querySelector('.f-lockup svg'), lockupViewBox: (document.querySelector('.f-lockup svg') || { getAttribute: () => null }).getAttribute('viewBox'), lockupDots: lk.length,
      lockupDotDelays: lk.map(c => getComputedStyle(c).animationDelay), lockupDesc: document.querySelectorAll('.f-lockup .wm-desc path').length,
      loaderClip: !!document.querySelector('#ldClip rect'), loaderClipWidth: (document.querySelector('#ldClip rect') || { getAttribute: () => null }).getAttribute('width'),
      beamDotCy: (document.querySelector('.loader .beam-dot') || { getAttribute: () => null }).getAttribute('cy') }; });
  await scrollThrough(page);
  r.signature = await page.evaluate(() => [...document.querySelectorAll('.foot2 .sig img')].map(i => ({ src: i.getAttribute('src'), shown: getComputedStyle(i).display !== 'none', ok: i.complete && i.naturalWidth > 0 })));   // dark theme at this point: the white one is shown; the hidden lazy one stays unloaded (see report.footers for both themes)
  await page.waitForTimeout(400);
  await page.screenshot({ ...jpg(`${tag}-dark-full.jpg`), fullPage: true });
  await page.screenshot(jpg(`${tag}-dark.jpg`));
  if (name === 'index') {                                  // galleries: filter + search
    await page.evaluate(() => { const el = document.querySelector('#collection'); (window.__lenis ? window.__lenis.scrollTo(el, { immediate: true, offset: -80 }) : el.scrollIntoView()); });
    await page.waitForTimeout(600);
    const count = () => page.evaluate(() => [...document.querySelectorAll('.collection .card')].filter(c => c.getClientRects().length && getComputedStyle(c).visibility !== 'hidden').length);
    const before = await count();
    await page.evaluate(() => document.querySelector('button[data-cat="projection"]').click()); await page.waitForTimeout(700);
    const afterFilter = await count(); const pressed = await page.evaluate(() => document.querySelector('.seg button[aria-pressed="true"]').dataset.cat); const labelProjection = await page.evaluate(() => document.querySelector('#count').textContent.trim());
    await page.screenshot(jpg(`${tag}-dark-gallery-filter-projection.jpg`));
    await page.fill('#search', 'Ayodhya'); await page.waitForTimeout(700); const afterSearch = await count(); const labelSearch = await page.evaluate(() => document.querySelector('#count').textContent.trim());
    await page.evaluate(() => document.querySelector('#searchClear').click()); await page.evaluate(() => document.querySelector('button[data-cat="work"]').click()); await page.waitForTimeout(500);
    r.gallery = { visibleDefault: before, visibleProjection: afterFilter, pressed, countLabelProjection: labelProjection, visibleSearchAyodhya: afterSearch, countLabelSearch: labelSearch };
    await page.evaluate(() => { const go = (y) => { if (window.__lenis) window.__lenis.scrollTo(y, { immediate: true }); window.scrollTo(0, y); }; go(0); }); await page.waitForTimeout(400);
  }
  // theme toggle
  await page.evaluate(() => document.querySelector('.theme').click()); await themeSettled(page, name === 'index' ? 1500 : 500);   // index cross-fades via View Transitions
  r.theme = await page.evaluate(() => ({ after: document.documentElement.getAttribute('data-theme'), bg: getComputedStyle(document.body).backgroundColor, fg: getComputedStyle(document.body).color }));
  await page.screenshot(jpg(`${tag}-light.jpg`));
  await page.screenshot({ ...jpg(`${tag}-light-full.jpg`), fullPage: true });
  r.errors = errors; r.failed = failed;
  r.localFailures = failed.filter(f => !EXTERNAL.test(f)); r.localErrors = errors.filter(e => !EXTERNAL.test(e));
  await ctx.close(); return r;
}

async function loaderFrames(browser, base, label) {   // the loader: clip-path wipe + travelling beam dot on the new artwork
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, colorScheme: 'dark' });
  const page = await ctx.newPage();
  await page.addInitScript(() => { const iv = setInterval(() => { const r = document.querySelector('#ldClip rect'); if (!r || !window.gsap) return;
    const w = +r.getAttribute('width'), W = r.closest('svg').viewBox.baseVal.width; if (w > 0 && w < W) { window.gsap.globalTimeline.pause(); window.__ldFrozen = true; clearInterval(iv); } }, 4); });
  await page.goto(base + '/', { waitUntil: 'commit' });
  await page.waitForSelector('.loader .wm svg');
  // the wipe lasts 1.1 s while the three.js module is still booting, so a fixed delay is unreliable: an in-page watcher
  // (added before the page's scripts) freezes GSAP as soon as the clip is 40–75 % open; capture, then let it run on
  await page.waitForFunction(() => window.__ldFrozen, null, { timeout: 15000, polling: 100 }).catch(() => console.log('loader: watcher did not fire'));
  // the main thread is busy compiling the three.js module during the wipe, so the frozen moment is early; seek the site's own
  // loader timeline (paused) to its midpoint so the frame shows the clip half open and the beam dot mid-travel
  console.log('loader frame', await page.evaluate(() => { const r = document.querySelector('#ldClip rect'); const tw = window.gsap && window.gsap.getTweensOf(r)[0];
    if (tw && tw.parent) tw.parent.progress(.55); return [r.getAttribute('width'), document.querySelector('.loader .beam-dot').getAttribute('cx')]; }));
  await page.screenshot(jpg(`${label}-index-desktop-loader-frame.jpg`));
  await page.evaluate(() => window.gsap && window.gsap.globalTimeline.resume()); await ctx.close();
}
/* The footer signature writes itself when it arrives (`.sig.on` → sigWrite 2.2 s) and the site's JS restarts the write
   every 5 s while it stays on screen, so a capture taken at a fixed delay can catch it mid-stroke (pen line + a few
   letters). Scroll the footer in, wait for the write to finish, then pin the finished state (inline !important beats the
   animation) so the light and dark captures are stable; measure the signature box and both <img>s for the report. */
async function settledSignature(page, wait) {
  await page.evaluate(() => { const el = document.querySelector('.foot2'); el.scrollIntoView(); });
  await page.waitForFunction(() => { const s = document.querySelector('.foot2 .sig'); if (!s) return true; const b = s.getBoundingClientRect(); return b.top >= 0 && b.bottom <= innerHeight; }, null, { timeout: 8000, polling: 100 }).catch(() => {});
  await page.waitForTimeout(3600);                     // ≥ 3.5 s: the write-on (2.2 s) has finished before anything is pinned or captured
  if (wait) await page.waitForFunction(() => { const i = document.querySelector('.foot2 .sig-ink'); if (!i) return true; const a = i.getAnimations(); return a.length > 0 && a.every(x => x.playState === 'finished'); }, null, { timeout: 9000, polling: 100 }).catch(() => {});
  await page.evaluate(() => {
    document.querySelectorAll('.foot2 .sig-ink').forEach(e => e.style.setProperty('clip-path', 'inset(0 -2% 0 0)', 'important'));
    document.querySelectorAll('.foot2 .sig-pen').forEach(e => e.style.setProperty('display', 'none', 'important'));
  });
  await page.waitForTimeout(500);                      // let a theme-switched lazy <img> decode
  return page.evaluate(() => { const s = document.querySelector('.foot2 .sig'); if (!s) return null; const b = s.getBoundingClientRect();
    return { theme: document.documentElement.getAttribute('data-theme'), box: [Math.round(b.width), Math.round(b.height)], clip: getComputedStyle(s.querySelector('.sig-ink')).clipPath,
      imgs: [...s.querySelectorAll('img')].map(i => { const r = i.getBoundingClientRect(); return { src: i.getAttribute('src').replace(/^.*\//, ''), shown: getComputedStyle(i).display !== 'none', loaded: i.complete && i.naturalWidth > 0, box: [Math.round(r.width), Math.round(r.height)] }; }) }; });
}
/* element capture that does not hang on a box that never reports "stable" (the header carries GSAP/CSS motion):
   try Playwright's element screenshot briefly, then fall back to a page capture clipped to the element's box */
async function shot(page, sel, file) {
  const loc = page.locator(sel).first();
  try { await loc.screenshot({ path: path.join(SHOTS, file), timeout: 6000 }); }
  catch (e) { const b = await loc.boundingBox(); await page.screenshot({ path: path.join(SHOTS, file), clip: b, fullPage: true }); console.log('clip capture', file); }
}
async function headerShots(browser, base, name, url, label, footers) {
  for (const [vn, w, h] of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, colorScheme: 'dark' });
    const page = await ctx.newPage(); await page.goto(base + url, { waitUntil: 'load' }); await settle(page); await page.waitForTimeout(600);
    await shot(page, 'header.nav', `${label}-${name}-${vn}-header-2x.png`);
    await page.evaluate(() => document.querySelector('.theme').click()); await themeSettled(page, name === 'index' ? 1500 : 500);   // index cross-fades via View Transitions
    await shot(page, 'header.nav', `${label}-${name}-${vn}-header-2x-light.png`);
    if (label === 'after') {                              // footer: lockup + signature, light then dark, signature settled
      await scrollThrough(page);
      const light = await settledSignature(page, true);
      await shot(page, '.foot2', `${label}-${name}-${vn}-footer-2x-light.png`);
      await page.evaluate(() => document.querySelector('.theme').click()); await themeSettled(page, name === 'index' ? 1500 : 500);   // index cross-fades via View Transitions
      const dark = await settledSignature(page, false);
      await shot(page, '.foot2', `${label}-${name}-${vn}-footer-2x.png`);
      if (footers) footers.push({ page: name, viewport: vn, light, dark });
      console.log('footer', name, vn, 'light', JSON.stringify(light), 'dark', JSON.stringify(dark));
    }
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
  const browser = await chromium.launch(); const report = { after: [], before: [], footers: [], files: {} };
  try {
    if (LOADER_ONLY) { await loaderFrames(browser, base, 'after'); console.log('loader frame only'); return; }
    for (const [name, url] of PAGES) { for (const vp of VIEWPORTS) { const r = await audit(browser, base, name, url, vp, 'after'); report.after.push(r); console.log('after', name, vp[0], 'errors', r.localErrors.length, 'failed', r.localFailures.length, 'fonts', r.fonts.fraunces, r.fonts.inter, r.fonts.tight, 'wm', JSON.stringify(r.wordmark && [r.wordmark.width, r.wordmark.height]), 'theme', r.theme.after, r.gallery ? JSON.stringify(r.gallery) : ''); } }
    await loaderFrames(browser, base, 'after');
    for (const [name, url] of PAGES) await headerShots(browser, base, name, url, 'after', report.footers);
    report.files = await files(browser, base); console.log('files', JSON.stringify(report.files, null, 1));
    if (bbase) { for (const [name, url] of PAGES.slice(0, 2)) { for (const vp of VIEWPORTS) { const r = await audit(browser, bbase, name, url, vp, 'before'); report.before.push(r); console.log('before', name, vp[0], 'errors', r.localErrors.length, 'failed', r.localFailures.length); } }
      await headerShots(browser, bbase, 'index', '/', 'before', null); }
  } finally { await browser.close(); srv.kill(); if (bsrv) bsrv.kill(); }
  fs.writeFileSync(path.join(SHOTS, 'verify-report.json'), JSON.stringify(report, null, 2));
  const badFoot = report.footers.filter(f => [f.light, f.dark].some(t => !t || t.clip !== 'inset(0px -2% 0px 0px)' || t.imgs.some(i => i.shown && !i.loaded)));
  if (badFoot.length) console.log('FOOTER SIGNATURE PROBLEMS: ' + JSON.stringify(badFoot, null, 1));
  const bad = report.after.filter(r => r.localErrors.length || r.localFailures.length);
  console.log(bad.length ? 'PROBLEMS: ' + JSON.stringify(bad.map(r => [r.page, r.viewport, r.localErrors, r.localFailures]), null, 1) : 'OK — no local errors or failed requests');
})();
