#!/usr/bin/env python3
"""build_moodboard.py — writes moodboard.html (A3 landscape, 4 pages) from the page spec below,
renders Moodboard.pdf with the brand kit's render.js and a PNG of each page with pdftoppm.

  python3 build_moodboard.py          # build HTML + PDF + PNGs
  python3 build_moodboard.py --html   # only rewrite moodboard.html (then edit it by hand if you like)

Edit the PAGES list to change images, labels or notes. Images are referenced from
../../Approved_Images/JPG; focal points come from ../../Approved_Images/approved.json.
"""
import json, subprocess, sys, html
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent                                   # 06_PHOTOGRAPHY_ART_DIRECTION
KIT = ROOT.parent / "15_SOURCE_FILES/Project_Files/brand-kit"
M = json.load(open(ROOT / "Approved_Images/approved.json"))
IMG = {it["slug"]: it for it in M["images"]}
for it in M["images"]:
    it["path"] = f"../../Approved_Images/JPG/sanzeed-img-{it['slug']}--{it['category']}.jpg"

PAGES = [
    {
        "eyebrow": "Moodboard · 001 — Overview",
        "title": "The lit <span class='lit'>room.</span>",
        "note": "One dominant light source. Blacks that hold detail, never crushed. Highlights that lean warm, toward the lamp. A person for scale, walking in. Everything the camera sees is a room someone can enter.",
        "cues": ["Expose for the light, let the rest fall to Night.", "Warm over cool. Never both at full strength.", "Backs to camera are allowed. Posed groups are not.", "One accent in the frame: the thing that is lit."],
        "palette": True,
        "layout": "hero",
        "images": ["mountain-projection", "prime-minister-museum", "ram-katha-show-diyas", "maharishi-valmiki-museum", "yuge-yugeen-bharat-museum"],
    },
    {
        "eyebrow": "Moodboard · 002 — Museums & experience centres",
        "title": "Galleries planned as a route, not a floor&nbsp;plan.",
        "note": "Shoot along the route. Stand on the visitor's line and look where they look: the threshold, the long corridor, the one object at the centre of the room. The exhibit is the key light; the architecture is the frame.",
        "cues": ["One-point perspective down the route.", "Symmetry when the room is symmetrical; thirds when it is not.", "The lit object at the centre, the dark around it kept dark.", "Wall labels and screens in focus; they carry the story."],
        "layout": "six",
        "images": ["freedom-fighter-museum", "army-museum-abu-dhabi", "tribal-museum", "rbi-museum-interior", "space-museum", "sant-ravi-das-museum"],
    },
    {
        "eyebrow": "Moodboard · 003 — Projection & shows",
        "title": "The building is the screen. The night is the <span class='lit'>room.</span>",
        "note": "Expose for the projection and let the sky and the ground fall to black. No flash, ever: it kills the show. Tripod, low ISO, long exposure. Points of light — lamps, LEDs, embers — are the brand's own vocabulary; keep them sharp.",
        "cues": ["Shoot from the audience, at eye level or lower.", "Façade square-on for symmetry, or from the corner for depth.", "Let colour come from the show; add none in the grade.", "Keep the beam: light paths and reflections stay in frame."],
        "layout": "six",
        "images": ["ram-katha-show", "albert-hall-projection-show", "g20-tree-show", "light-and-sound-show-ayodhya", "ram-katha-show-ram-in-light", "postal-museum-projection-show"],
    },
    {
        "eyebrow": "Moodboard · 004 — Portrait & people",
        "title": "Visitors walk into the light.",
        "note": "People give the room its scale. They are seen from behind or in profile, moving toward the lit thing, never posing for the camera. The portrait standard is the existing one: a warm key, soft bokeh, a black garment, the eye line on the upper third, no retouching beyond the grade.",
        "cues": ["Backs to camera allowed; eye contact only in portraits.", "One or two figures, never a posed group.", "Walking, looking, reading — in motion or absorbed.", "Portrait: warm key from one side, Night behind, 85–105 mm."],
        "layout": "portrait",
        "images": ["PORTRAIT", "mahatma-gandhi-event", "buddha-park-stupa-path", "prime-minister-museum", "mountain-projection"],
    },
]

CSS = """
  @page { size: 420mm 297mm; margin: 0; }
  html, body { background: #000; }
  .page { position: relative; width: 420mm; height: 297mm; overflow: hidden; background: var(--bg); color: var(--fg);
          padding: 16mm 18mm 14mm; display: grid; grid-template-rows: auto 1fr auto; page-break-after: always; break-after: page; }
  .page:last-child { page-break-after: auto; break-after: auto; }
  .hdr { display: flex; justify-content: space-between; align-items: center; height: 10mm; }
  .hdr .eyebrow { font-size: 11px; }
  .hdr img { height: 5mm; }
  .body { display: grid; grid-template-columns: 112mm 1fr; gap: 14mm; margin-top: 10mm; min-height: 0; }
  .col h1 { font-size: 58px; line-height: 1.02; margin-bottom: 9mm; }
  .col .note { font-size: 15.5px; line-height: 1.55; color: var(--fg-2); max-width: 100%; margin-bottom: 8mm; }
  .cues { list-style: none; padding: 0; margin: 0; border-top: var(--hairline); }
  .cues li { display: flex; gap: 10px; padding: 7px 0; border-bottom: var(--hairline); font-size: 13.5px; line-height: 1.4; color: var(--fg); }
  .cues li .counter { padding-top: 2px; min-width: 26px; }
  .palette { display: flex; gap: 6px; margin-top: 10mm; }
  .sw { flex: 1; height: 16mm; border-radius: 8px; border: var(--hairline); display: flex; align-items: flex-end; padding: 6px; font: 500 9.5px/1.2 var(--font-text); color: var(--fg-3); }
  .sw b { display: block; color: var(--fg-2); font-weight: 500; }
  .sw.gold b { color: #000; } .sw.gold { color: rgba(0,0,0,.65); }
  .sw.white b, .sw.white { color: #1A1816; }
  .grid { display: grid; gap: 6mm; min-height: 0; }
  .grid.six { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr 1fr; }
  .grid.hero { grid-template-columns: 1fr 1fr 1fr; grid-template-rows: 1fr 1fr; }
  .grid.hero .cell:first-child { grid-column: 1 / 3; grid-row: 1 / 3; }
  .grid.portrait { grid-template-columns: 0.74fr 1fr 1fr; grid-template-rows: 1fr 1fr; }
  .grid.portrait .cell:first-child { grid-row: 1 / 3; }
  .cell { display: flex; flex-direction: column; min-height: 0; }
  .cell .pic { flex: 1; min-height: 0; border-radius: 20px; overflow: hidden; border: var(--hairline); background: var(--card); }
  .cell img { width: 100%; height: 100%; object-fit: cover; }
  .wl { display: flex; gap: 10px; align-items: baseline; margin-top: 7px; font-size: 12.5px; line-height: 1.35; color: var(--fg-3); }
  .wl b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); margin-right: 6px; }
  .wl .counter { font-size: 11px; }
  .ftr { display: flex; justify-content: space-between; align-items: flex-end; padding-top: 6mm; margin-top: 6mm; position: relative; font-size: 12px; color: var(--fg-3); }
  .ftr .beam { position: absolute; top: 0; left: 0; right: 0; }
  .ftr img { height: 4.2mm; }
"""

def cell(slug, n):
    if slug == "PORTRAIT":
        return f'''        <figure class="cell">
          <div class="pic"><img src="../../Approved_Images/Portrait/sanzeed-portrait--4x5-2000.jpg" alt="Sanzeed Mirza — portrait" style="object-position: 50% 30%"></div>
          <figcaption class="wl"><span class="counter">{n:03d}</span><span><b>Sanzeed Mirza</b>New Delhi · the portrait standard</span></figcaption>
        </figure>'''
    it = IMG[slug]; fx, fy = it["focal"]
    return f'''        <figure class="cell">
          <div class="pic"><img src="{it['path']}" alt="{html.escape(it['title'])} — {html.escape(it['place'])}" style="object-position: {fx*100:.0f}% {fy*100:.0f}%"></div>
          <figcaption class="wl"><span class="counter">{n:03d}</span><span><b>{html.escape(it['title'])}</b>{html.escape(it['place'])}</span></figcaption>
        </figure>'''

def page(p, i):
    cues = "\n".join(f'          <li><span class="counter">{j:02d}</span><span>{html.escape(c)}</span></li>' for j, c in enumerate(p["cues"], 1))
    palette = ""
    if p.get("palette"):
        palette = '''        <div class="palette">
          <div class="sw" style="background:#000"><span><b>Gallery Black</b>#000000</span></div>
          <div class="sw" style="background:#0D0D0F"><span><b>Night</b>#0D0D0F</span></div>
          <div class="sw" style="background:#1C1C1E"><span><b>Charcoal</b>#1C1C1E</span></div>
          <div class="sw gold" style="background:#E9B25A"><span><b>Lamp Gold</b>#E9B25A</span></div>
          <div class="sw white" style="background:#F5F5F7"><span><b>Gallery White</b>#F5F5F7</span></div>
        </div>'''
    cells = "\n".join(cell(s, n) for n, s in enumerate(p["images"], 1))
    return f'''  <section class="page grain">
    <header class="hdr">
      <div class="eyebrow">{p['eyebrow']}</div>
      <img src="../../../02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg" alt="Sanzeed">
    </header>
    <div class="body">
      <div class="col">
        <h1 class="t-display-2">{p['title']}</h1>
        <p class="note">{p['note']}</p>
        <ul class="cues">
{cues}
        </ul>
{palette}
      </div>
      <div class="grid {p['layout']}">
{cells}
      </div>
    </div>
    <footer class="ftr">
      <div class="beam"></div>
      <span>Sanzeed Mirza · Experiential Design Consultant · Photography &amp; art direction</span>
      <span class="tnum">Moodboard · {i:02d} / {len(PAGES):02d}</span>
    </footer>
  </section>'''

doc = f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Sanzeed — Photography moodboard (A3 landscape)</title>
<link rel="stylesheet" href="../../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>{CSS}</style>
</head>
<body>
{chr(10).join(page(p, i) for i, p in enumerate(PAGES, 1))}
</body>
</html>
'''
(HERE / "moodboard.html").write_text(doc, encoding="utf-8")
print("wrote moodboard.html")
if "--html" in sys.argv: sys.exit(0)

pdf = ROOT / "Moodboard.pdf"
subprocess.run(["node", str(KIT / "render.js"), "--in", str(HERE / "moodboard.html"), "--out", str(pdf), "--pdf",
                "--size", "420x297", "--landscape", "--wait", "900"], check=True)
out = ROOT / "Moodboard_Pages"; out.mkdir(exist_ok=True)
for f in out.glob("*.png"): f.unlink()
subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf), str(out / "sanzeed-moodboard--p")], check=True)
names = ["overview", "museums-experience-centres", "projection-shows", "portrait-people"]
for i, f in enumerate(sorted(out.glob("sanzeed-moodboard--p*.png"))):
    f.rename(out / f"sanzeed-moodboard--p{i+1:02d}-{names[i]}.png")
print("rendered", pdf, "and", len(names), "PNGs")
