#!/usr/bin/env python3
"""build_templates.py — writes the editable HTML image-treatment templates, the SVG frame set,
and renders one PNG example of each into ./examples/.

  python3 build_templates.py            # write HTML + SVG, render examples
  python3 build_templates.py --no-render

Each HTML template is standalone: a JSON data block at the top (<script type="application/json" id="data">)
holds the image path, focal point, label text and options; the page reads it and lays itself out.
Edit the JSON, then render with the brand kit's render.js (commands in README.md).
"""
import json, subprocess, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
B = ROOT.parent
KIT = B / "15_SOURCE_FILES/Project_Files/brand-kit"
EX = HERE / "examples"; EX.mkdir(exist_ok=True)
SVGD = HERE / "SVG_Frames"; SVGD.mkdir(exist_ok=True)
RENDER = "--no-render" not in sys.argv

CSS_COMMON = """
  html, body { margin: 0; background: #000; }
  .plate { position: relative; width: var(--w); height: var(--h); overflow: hidden; background: #0D0D0F; }
  .plate img.photo { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: var(--focal, 50% 50%); }
  .veil { position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) var(--veil-start, 38%), rgba(0,0,0, var(--veil, .72)) 100%); }
  .veil.top { background: linear-gradient(0deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) var(--veil-start, 38%), rgba(0,0,0, var(--veil, .72)) 100%); }
  .label { position: absolute; left: var(--m); right: var(--m); bottom: var(--m); color: #F5F5F7; }
  .label .headline { font-family: var(--font-display); font-weight: 300; font-size: var(--fs-head); line-height: 1.04; letter-spacing: -0.015em; font-variation-settings: "opsz" 144, "SOFT" 30, "WONK" 0; max-width: 18ch; margin-bottom: calc(var(--m) * .45); text-wrap: balance; }
  .label .headline .lit { color: #E9B25A; }
  .label .counter { display: block; font-size: var(--fs-counter); color: #E9B25A; margin-bottom: calc(var(--m) * .22); }
  .label .title { display: block; font-family: var(--font-heading); font-weight: 600; font-size: var(--fs-title); line-height: 1.25; letter-spacing: -0.01em; }
  .label .place { display: block; font-family: var(--font-text); font-weight: 400; font-size: var(--fs-place); line-height: 1.4; color: #A1A1A6; margin-top: 0.15em; }
  .label .eyebrow { display: block; font-size: var(--fs-counter); color: #E9B25A; margin-bottom: calc(var(--m) * .22); }
  .logo { position: absolute; right: var(--m); bottom: var(--m); height: var(--logo-h); display: none; }
  .logo.on { display: block; }
  .plate.grain::after { border-radius: 0; }
"""

JS_COMMON = """
  const D = JSON.parse(document.getElementById('data').textContent);
  const q = s => document.querySelector(s);
  const photo = q('img.photo'); if (photo && D.image) { photo.src = D.image; photo.alt = (D.title || '') + (D.place ? ' — ' + D.place : ''); }
  if (D.focal) document.documentElement.style.setProperty('--focal', D.focal);
  if (D.veil !== undefined) document.documentElement.style.setProperty('--veil', D.veil);
  if (D.veil_start) document.documentElement.style.setProperty('--veil-start', D.veil_start);
  if (D.veil_top) q('.veil') && q('.veil').classList.add('top');
  const set = (sel, v) => { const el = q(sel); if (!el) return; if (v) { el.textContent = v; } else { el.remove(); } };
  set('.counter', D.counter); set('.title', D.title); set('.place', D.place); set('.eyebrow', D.eyebrow);
  const h = q('.headline');
  if (h) { if (D.headline) { const w = D.headline.trim().split(' '); const last = w.pop(); h.innerHTML = (w.length ? w.map(x => x.replace(/</g,'&lt;')).join(' ') + ' ' : '') + '<span class="lit">' + last.replace(/</g,'&lt;') + '</span>'; } else h.remove(); }
  const logo = q('.logo'); if (logo && D.logo) logo.classList.add('on');
"""

def plate_html(name, w, h, data, title, css_extra="", m=None, fs=None):
    """Wall-label plate template at w×h px."""
    m = m or round(min(w, h) * 0.066)
    fs = fs or {"head": round(min(w, h) * 0.072), "counter": round(min(w, h) * 0.016), "title": round(min(w, h) * 0.026), "place": round(min(w, h) * 0.021), "logo": round(min(w, h) * 0.052)}
    return f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<!-- ============================ DATA BLOCK — edit this, nothing else needs to change ============================
     image      : path to a graded approved image (relative to this file)
     focal      : CSS object-position for the crop, e.g. "50% 45%" (from Approved_Images/approved.json)
     counter    : "001" (gold) — leave "" to omit
     title/place: the wall label (Inter Tight 600 / Inter 400)
     headline   : optional Fraunces 300 line; the last word is set in Lamp Gold. Sentence case, full stop.
     veil       : 0–1 strength of the bottom veil (0.72 is the brand default); veil_start: where it begins ("38%")
     veil_top   : true to veil from the top instead
     logo       : true to add the symbol (full-colour-dark) bottom-right
     Render:  node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in {name}.html --out out.png --width {w} --height {h} --scale 2
     ======================================================================================================== -->
<script type="application/json" id="data">
{json.dumps(data, indent=2, ensure_ascii=False)}
</script>
<link rel="stylesheet" href="../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
  :root {{ --w: {w}px; --h: {h}px; --m: {m}px; --fs-head: {fs['head']}px; --fs-counter: {fs['counter']}px; --fs-title: {fs['title']}px; --fs-place: {fs['place']}px; --logo-h: {fs['logo']}px; }}
{CSS_COMMON}{css_extra}
</style>
</head>
<body>
<div class="plate grain">
  <img class="photo" src="" alt="">
  <div class="veil"></div>
  <div class="label">
    <div class="headline"></div>
    <span class="counter"></span>
    <span class="eyebrow"></span>
    <span class="title"></span>
    <span class="place"></span>
  </div>
  <img class="logo" src="../../02_LOGO_SYSTEM/SVG/sanzeed-symbol--full-colour-dark.svg" alt="Sanzeed">
</div>
<script>{JS_COMMON}</script>
</body>
</html>
'''

IMG = lambda slug, cat: f"../Approved_Images/JPG/sanzeed-img-{slug}--{cat}.jpg"
PLATES = [
    ("wall-label-plate--16x9", 1920, 1080, {"image": IMG("prime-minister-museum", "museum"), "focal": "50% 50%", "counter": "001", "title": "Prime Minister Museum", "place": "New Delhi", "headline": "", "veil": 0.72, "veil_start": "38%", "logo": False}),
    ("wall-label-plate--4x5", 1080, 1350, {"image": IMG("ram-katha-show", "projection"), "focal": "50% 45%", "counter": "015", "title": "Ram Katha Show", "place": "Ayodhya", "headline": "The script comes first.", "veil": 0.72, "veil_start": "34%", "logo": False}),
    ("wall-label-plate--1x1", 1080, 1080, {"image": IMG("raja-bhoj-museum", "architecture"), "focal": "50% 60%", "counter": "030", "title": "Raja Bhoj Museum", "place": "New Delhi", "headline": "", "veil": 0.72, "veil_start": "40%", "logo": True}),
    ("wall-label-plate--9x16", 1080, 1920, {"image": IMG("mountain-projection", "projection"), "focal": "46% 63%", "counter": "024", "title": "Mountain Projection", "place": "Uttarakhand", "headline": "Vision you can walk into.", "veil": 0.78, "veil_start": "45%", "logo": False}),
]
for name, w, h, data in PLATES:
    (HERE / f"{name}.html").write_text(plate_html(name, w, h, data, f"Sanzeed — {name}"), encoding="utf-8")

# ---------- room frame ----------
room = {"image": IMG("army-museum-abu-dhabi", "museum"), "focal": "52% 50%", "counter": "003", "title": "Army Museum Abu Dhabi", "place": "Abu Dhabi", "note": "A single chair at the centre of concentric rings of calligraphy, so the visitor circles the story before reaching its heart."}
(HERE / "room-frame.html").write_text(f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Sanzeed — room frame</title>
<!-- ===================== DATA BLOCK =====================
     image / focal / counter / title / place / note (one line, optional)
     Render: node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in room-frame.html --out out.png --width 1920 --height 1080 --scale 2
     ====================================================== -->
<script type="application/json" id="data">
{json.dumps(room, indent=2, ensure_ascii=False)}
</script>
<link rel="stylesheet" href="../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
  html, body {{ margin: 0; background: #000; }}
  .stage {{ position: relative; width: 1920px; height: 1080px; background: #0D0D0F; padding: 72px 96px 0; box-sizing: border-box; }}
  .top {{ display: flex; justify-content: space-between; align-items: center; height: 40px; margin-bottom: 20px; }}
  .top .counter {{ font-size: 17px; }}
  .top img {{ height: 22px; }}
  .room {{ position: relative; width: 100%; height: 800px; border-radius: 28px; overflow: hidden; border: 1px solid rgba(255,255,255,.10); background: #1C1C1E; }}
  .room img {{ width: 100%; height: 100%; object-fit: cover; object-position: var(--focal, 50% 50%); display: block; }}
  .wl {{ display: flex; gap: 18px; align-items: baseline; margin-top: 22px; font-size: 20px; line-height: 1.4; color: #808086; }}
  .wl b {{ font-family: var(--font-heading); font-weight: 600; color: #F5F5F7; font-size: 22px; }}
  .wl .note {{ color: #A1A1A6; margin-left: auto; max-width: 70ch; text-align: right; }}
</style>
</head>
<body>
<div class="stage grain">
  <div class="top"><span class="counter"></span><img src="../../02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg" alt="Sanzeed"></div>
  <div class="room"><img class="photo" src="" alt=""></div>
  <div class="wl"><b class="title"></b><span class="place"></span><span class="note"></span></div>
</div>
<script>
  const D = JSON.parse(document.getElementById('data').textContent);
  document.querySelector('img.photo').src = D.image; document.querySelector('img.photo').alt = D.title + ' — ' + D.place;
  document.documentElement.style.setProperty('--focal', D.focal || '50% 50%');
  for (const k of ['counter', 'title', 'place', 'note']) {{ const el = document.querySelector('.' + k); if (D[k]) el.textContent = D[k]; else el.remove(); }}
</script>
</body>
</html>
''', encoding="utf-8")

# ---------- before / after ----------
ba = {"before": "../src/guidelines/assets/grade-before.jpg", "after": "../src/guidelines/assets/grade-after.jpg", "focal": "50% 45%",
      "title": "Maharishi Valmiki Museum", "place": "Punjab", "before_label": "Before · camera file", "after_label": "After · grade.py",
      "note": "Contrast +0.18 sine-S · blacks to Night #0D0D0F · highlights warmed toward Lamp Gold #E9B25A · saturation unchanged"}
(HERE / "before-after-grade.html").write_text(f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Sanzeed — before / after grade</title>
<!-- ===================== DATA BLOCK =====================
     before / after : the two image paths (same crop; make them with Approved_Images/grade.py)
     focal          : CSS object-position for both halves
     title / place  : wall label;  before_label / after_label : the tags;  note : one line under the pair
     Render: node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in before-after-grade.html --out out.png --width 1920 --height 1080 --scale 2
     ====================================================== -->
<script type="application/json" id="data">
{json.dumps(ba, indent=2, ensure_ascii=False)}
</script>
<link rel="stylesheet" href="../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
  html, body {{ margin: 0; background: #000; }}
  .stage {{ position: relative; width: 1920px; height: 1080px; background: #0D0D0F; padding: 72px 96px 0; box-sizing: border-box; }}
  .top {{ display: flex; justify-content: space-between; align-items: center; height: 40px; margin-bottom: 20px; }}
  .top .eyebrow {{ font-size: 15px; }}
  .top img {{ height: 22px; }}
  .pair {{ position: relative; display: grid; grid-template-columns: 1fr 1fr; gap: 0; height: 780px; border-radius: 28px; overflow: hidden; border: 1px solid rgba(255,255,255,.10); background: #1C1C1E; }}
  .pair .half {{ position: relative; overflow: hidden; }}
  .pair img {{ width: 100%; height: 100%; object-fit: cover; object-position: var(--focal, 50% 50%); display: block; }}
  .pair .half + .half {{ border-left: 1px solid rgba(255,255,255,.35); }}
  .tag {{ position: absolute; left: 28px; top: 28px; padding: 10px 16px; border-radius: 999px; font: 600 14px/1 var(--font-heading); letter-spacing: .08em; text-transform: uppercase; background: rgba(0,0,0,.72); color: #F5F5F7; border: 1px solid rgba(255,255,255,.14); }}
  .tag.gold {{ color: #E9B25A; }}
  .wl {{ display: flex; gap: 18px; align-items: baseline; margin-top: 22px; font-size: 20px; line-height: 1.4; color: #808086; }}
  .wl b {{ font-family: var(--font-heading); font-weight: 600; color: #F5F5F7; font-size: 22px; }}
  .wl .note {{ color: #A1A1A6; margin-left: auto; font-variant-numeric: tabular-nums; }}
</style>
</head>
<body>
<div class="stage grain">
  <div class="top"><span class="eyebrow">Colour grading · before / after</span><img src="../../02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg" alt="Sanzeed"></div>
  <div class="pair">
    <div class="half"><img class="before" src="" alt="Before"><span class="tag before_label"></span></div>
    <div class="half"><img class="after" src="" alt="After"><span class="tag gold after_label"></span></div>
  </div>
  <div class="wl"><b class="title"></b><span class="place"></span><span class="note"></span></div>
</div>
<script>
  const D = JSON.parse(document.getElementById('data').textContent);
  document.querySelector('img.before').src = D.before; document.querySelector('img.after').src = D.after;
  document.documentElement.style.setProperty('--focal', D.focal || '50% 50%');
  for (const k of ['title', 'place', 'note', 'before_label', 'after_label']) {{ const el = document.querySelector('.' + k); if (D[k]) el.textContent = D[k]; else el.remove(); }}
</script>
</body>
</html>
''', encoding="utf-8")

# ---------- portrait plate ----------
pp = {"image": "../Approved_Images/Portrait/sanzeed-portrait--native-1100x1574.jpg", "focal": "50% 30%", "eyebrow": "Sanzeed Mirza",
      "name": "Experiential design you can walk into.", "descriptor": "Experiential Design Consultant · New Delhi",
      "line": "Museums, experience centres, pavilions, memorials and projection shows — directed from the brief to opening night.",
      "contact": "sanzeed@gmail.com · +91 7827051270 · sanzeed.com"}
(HERE / "portrait-plate.html").write_text(f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Sanzeed — portrait plate</title>
<!-- ===================== DATA BLOCK =====================
     image      : the portrait (Approved_Images/Portrait/…); focal : object-position inside the right-hand panel
     eyebrow    : small gold line above the headline (the name)
     name       : the Fraunces 300 headline (sentence case, full stop; the last word is set in gold)
     descriptor : Inter Tight 600 line;  line : one sentence;  contact : footer line
     Render: node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in portrait-plate.html --out out.png --width 1920 --height 1080 --scale 2
     ====================================================== -->
<script type="application/json" id="data">
{json.dumps(pp, indent=2, ensure_ascii=False)}
</script>
<link rel="stylesheet" href="../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
  html, body {{ margin: 0; background: #000; }}
  .stage {{ position: relative; width: 1920px; height: 1080px; background: #000; overflow: hidden; display: grid; grid-template-columns: 1fr 760px; }}
  .lamp {{ position: absolute; right: -120px; top: -140px; width: 1100px; height: 1100px; background: radial-gradient(50% 50% at 50% 50%, rgba(233,178,90,.42) 0%, rgba(233,178,90,.10) 35%, rgba(0,0,0,0) 70%); }}
  .text {{ position: relative; padding: 110px 72px 96px 112px; display: flex; flex-direction: column; justify-content: space-between; }}
  .text .eyebrow {{ font-size: 15px; margin-bottom: 28px; }}
  .text h1 {{ font-family: var(--font-display); font-weight: 300; font-size: 84px; line-height: 1.0; letter-spacing: -0.015em; font-variation-settings: "opsz" 144, "SOFT" 30, "WONK" 0; color: #F5F5F7; max-width: 11ch; text-wrap: balance; }}
  .text h1 .lit {{ color: #E9B25A; }}
  .text .descriptor {{ font-family: var(--font-heading); font-weight: 600; font-size: 24px; color: #F5F5F7; margin-top: 36px; }}
  .text .line {{ font-size: 20px; line-height: 1.5; color: #A1A1A6; max-width: 46ch; margin-top: 14px; }}
  .text .bottom {{ display: flex; justify-content: space-between; align-items: flex-end; gap: 40px; }}
  .text .bottom img {{ width: 300px; }}
  .text .contact {{ font-size: 16px; color: #808086; }}
  .figure {{ position: relative; height: 100%; }}
  .figure img {{ width: 100%; height: 100%; object-fit: cover; object-position: var(--focal, 50% 30%); display: block; }}
  .figure::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, #000 0%, rgba(0,0,0,.55) 18%, rgba(0,0,0,0) 45%), linear-gradient(180deg, rgba(0,0,0,0) 70%, rgba(0,0,0,.7) 100%); }}
</style>
</head>
<body>
<div class="stage grain">
  <div class="lamp"></div>
  <div class="text">
    <div>
      <div class="eyebrow"></div>
      <h1 class="name"></h1>
      <div class="descriptor"></div>
      <p class="line"></p>
    </div>
    <div class="bottom"><img src="../../02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg" alt="Sanzeed"><span class="contact"></span></div>
  </div>
  <div class="figure"><img class="photo" src="" alt=""></div>
</div>
<script>
  const D = JSON.parse(document.getElementById('data').textContent);
  const ph = document.querySelector('img.photo'); ph.src = D.image; ph.alt = D.eyebrow || 'Portrait';
  document.documentElement.style.setProperty('--focal', D.focal || '50% 30%');
  for (const k of ['eyebrow', 'descriptor', 'line', 'contact']) {{ const el = document.querySelector('.' + k); if (D[k]) el.textContent = D[k]; else el.remove(); }}
  const w = D.name.trim().split(' '); const last = w.pop();
  document.querySelector('h1.name').innerHTML = (w.length ? w.join(' ') + ' ' : '') + '<span class="lit">' + last + '</span>';
</script>
</body>
</html>
''', encoding="utf-8")

# ---------- SVG frame set ----------
def frame_svg(w, h, name, room=False):
    m = round(min(w, h) * 0.066); r = 28 if not room else 28
    fs_c = round(min(w, h) * 0.016); fs_t = round(min(w, h) * 0.026); fs_p = round(min(w, h) * 0.021)
    inner = (m, m, w - 2*m, h - 2*m) if room else (0, 0, w, h)
    ix, iy, iw, ih = inner
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <title>Sanzeed — {name} frame ({w}×{h})</title>
  <desc>Editable image frame. Replace the rect #IMAGE_PLACEHOLDER with your photograph (clip it with #image-clip). Keep the veil above the image and the wall label above the veil. Fonts: Inter Tight (600 / 500) and Inter (400) — install from 04_TYPOGRAPHY/Font_Files. Lamp Gold #E9B25A is the only accent.</desc>
  <defs>
    <linearGradient id="veil" x1="0" y1="0" x2="0" y2="1"><stop offset="0.38" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.72"/></linearGradient>
    <clipPath id="image-clip"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r if room else 0}"/></clipPath>
  </defs>
  <rect id="background" width="{w}" height="{h}" fill="#0D0D0F"/>
  <g id="IMAGE" clip-path="url(#image-clip)">
    <rect id="IMAGE_PLACEHOLDER" x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="#1C1C1E"/>
  </g>
  <rect id="veil-gradient" x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="{r if room else 0}" fill="url(#veil)"/>
  {'<rect id="hairline" x="%s" y="%s" width="%s" height="%s" rx="%s" fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="2"/>' % (ix+1, iy+1, iw-2, ih-2, r) if room else ''}
  <g id="wall-label" font-family="'Inter Tight', 'Inter', 'Helvetica Neue', Arial, sans-serif">
    <text id="counter" x="{ix + m}" y="{iy + ih - m - fs_t - fs_p - round(fs_c*1.4)}" font-size="{fs_c}" font-weight="500" letter-spacing="{fs_c*0.12:.1f}" fill="#E9B25A">001</text>
    <text id="title" x="{ix + m}" y="{iy + ih - m - fs_p - round(fs_t*0.35)}" font-size="{fs_t}" font-weight="600" fill="#F5F5F7">[Project title]</text>
    <text id="place" x="{ix + m}" y="{iy + ih - m}" font-family="'Inter', 'Helvetica Neue', Arial, sans-serif" font-size="{fs_p}" font-weight="400" fill="#A1A1A6">[Place]</text>
  </g>
  <g id="GUIDES — delete before export" stroke="#E9B25A" stroke-opacity="0.35" stroke-dasharray="6 8" fill="none">
    <rect x="{m}" y="{m}" width="{w - 2*m}" height="{h - 2*m}"/>
  </g>
</svg>
'''
FRAMES = [("16x9", 1920, 1080, False), ("4x5", 1080, 1350, False), ("1x1", 1080, 1080, False), ("9x16", 1080, 1920, False), ("3x2", 3000, 2000, False), ("room-16x9", 1920, 1080, True)]
for tag, w, h, room_ in FRAMES:
    (SVGD / f"sanzeed-frame--{tag}.svg").write_text(frame_svg(w, h, tag, room_), encoding="utf-8")
print("wrote", len(PLATES) + 3, "HTML templates and", len(FRAMES), "SVG frames")

if RENDER:
    def render(src, out, w, h, scale):
        subprocess.run(["node", str(KIT / "render.js"), "--in", str(src), "--out", str(out), "--width", str(w), "--height", str(h), "--scale", str(scale), "--wait", "700"], check=True)
    for name, w, h, _ in PLATES:
        render(HERE / f"{name}.html", EX / f"sanzeed-template--{name.replace('--', '-')}.png", w, h, 2 if w <= 1080 else 1)
    for name in ["room-frame", "before-after-grade", "portrait-plate"]:
        render(HERE / f"{name}.html", EX / f"sanzeed-template--{name}.png", 1920, 1080, 1)
    # SVG frame preview: the 16:9 frame with an approved image dropped into the placeholder (preview only)
    import base64
    svg = (SVGD / "sanzeed-frame--16x9.svg").read_text(encoding="utf-8")
    img = (ROOT / "Approved_Images/JPG/sanzeed-img-g20-led-show--projection.jpg").read_bytes()
    svg = svg.replace('<rect id="IMAGE_PLACEHOLDER" x="0" y="0" width="1920" height="1080" fill="#1C1C1E"/>',
                      f'<image id="IMAGE_PLACEHOLDER" x="0" y="0" width="1920" height="1080" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/jpeg;base64,{base64.b64encode(img).decode()}"/>')
    svg = svg.replace("[Project title]", "G20 LED Show").replace("[Place]", "Gujarat").replace(">001<", ">019<")
    svg = svg.replace('<g id="GUIDES — delete before export"', '<g id="GUIDES — delete before export" visibility="hidden"')
    tmp = EX / "_frame-preview.svg"; tmp.write_text(svg, encoding="utf-8")
    import cairosvg
    cairosvg.svg2png(url=str(tmp), write_to=str(EX / "sanzeed-frame--16x9-preview.png"), output_width=1920)
    tmp.unlink()
    print("rendered examples into", EX)
