#!/usr/bin/env node
/**
 * capture_frames.js — deterministic frame capture of CSS / Web Animations API animations, then encode.
 *   node capture_frames.js --in anim.html --out logo-reveal --width 1920 --height 1080 --fps 30 --duration 4 [--scale 1] [--transparent] [--formats mp4,webm,gif,mov]
 * Every animation on the page is paused and stepped with Animation.currentTime, so output is frame-exact
 * regardless of machine speed. Author animations with CSS @keyframes or element.animate(); avoid rAF loops.
 * Encoders: MP4 (H.264, yuv420p), WebM (VP9, alpha when --transparent), GIF (palette), MOV (ProRes 4444, alpha when --transparent).
 */
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs'); const path = require('path');
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => { if (v.startsWith('--')) a.push([v.slice(2), (arr[i+1] && !arr[i+1].startsWith('--')) ? arr[i+1] : true]); return a; }, []));
(async () => {
  const width = parseInt(args.width || 1920), height = parseInt(args.height || 1080), fps = parseInt(args.fps || 30), dur = parseFloat(args.duration || 4);
  const formats = (args.formats || 'mp4,webm,gif').split(',');
  const out = args.out || 'animation'; const framesDir = out + '_frames'; fs.rmSync(framesDir, { recursive: true, force: true }); fs.mkdirSync(framesDir, { recursive: true });
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: parseFloat(args.scale || 1) });
  const page = await ctx.newPage();
  page.on('pageerror', e => console.error('[pageerror]', e.message));
  await page.goto('file://' + path.resolve(args.in), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  await page.evaluate(() => { document.getAnimations({ subtree: true }).forEach(a => { a.pause(); a.currentTime = 0; }); });
  const n = Math.round(dur * fps);
  for (let i = 0; i < n; i++) {
    const t = (i / fps) * 1000;
    await page.evaluate(t => { document.getAnimations({ subtree: true }).forEach(a => { a.currentTime = t; }); if (window.__sz_tick) window.__sz_tick(t); }, t);
    await page.screenshot({ path: path.join(framesDir, `f${String(i).padStart(5, '0')}.png`), omitBackground: !!args.transparent });
  }
  await browser.close();
  const inp = `-framerate ${fps} -i ${framesDir}/f%05d.png`;
  if (formats.includes('mp4')) execSync(`ffmpeg -y -loglevel error ${inp} -c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" ${out}.mp4`);
  if (formats.includes('webm')) execSync(`ffmpeg -y -loglevel error ${inp} -c:v libvpx-vp9 -pix_fmt ${args.transparent ? 'yuva420p' : 'yuv420p'} -b:v 0 -crf 28 ${out}.webm`);
  if (formats.includes('mov')) execSync(`ffmpeg -y -loglevel error ${inp} -c:v prores_ks -profile:v 4444 -pix_fmt ${args.transparent ? 'yuva444p10le' : 'yuv444p10le'} ${out}.mov`);
  if (formats.includes('gif')) execSync(`ffmpeg -y -loglevel error ${inp} -vf "fps=${Math.min(fps, 20)},scale=${Math.min(width, 960)}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=sierra2_4a" ${out}.gif`);
  if (!args.keepframes) fs.rmSync(framesDir, { recursive: true, force: true });
  console.log('encoded', out, formats.join(','));
})();
