#!/usr/bin/env python3
"""build_brochures.py — Brochures/: A4 trifold (outside + inside spreads, panels 98/99/100 and 100/99/98 mm)
and the 12-page A4 company profile. HTML sources with @page; PDF via render.js; print-ready CMYK via print_pdf.py;
PNG previews (trifold spreads; profile reader spreads)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C
from PIL import Image

OUT = f"{MC}/Brochures"; SRC = f"{OUT}/src"; os.makedirs(SRC, exist_ok=True)
PX = 96 / 25.4

COMMON = """
.mark { position: absolute; display: block; }
.hl { color: var(--fg); }
.svc { display: grid; grid-template-columns: 7mm 1fr; gap: 0 1mm; margin-bottom: 2.4mm; }
.svc .c { font-family: var(--font-heading); font-weight: 500; font-size: 6.5pt; letter-spacing: .08em; color: var(--accent-text); padding-top: .4mm; font-variant-numeric: tabular-nums; }
.svc b { display: block; font-family: var(--font-heading); font-weight: 600; font-size: 8pt; line-height: 1.25; color: var(--fg); }
.svc span { display: block; font-size: 6.8pt; line-height: 1.4; color: var(--fg-2); }
.svc em { display: block; font-style: normal; font-size: 6.2pt; color: var(--fg-3); margin-top: .4mm; }
.step { position: relative; padding-left: 7mm; margin-bottom: 3.5mm; }
.step::before { content: ""; position: absolute; left: 0; top: 1.6mm; width: 2.2mm; height: 2.2mm; border-radius: 50%; background: var(--accent); }
.step .ey { font-family: var(--font-heading); font-weight: 600; font-size: 5.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); }
.step b { display: block; font-family: var(--font-display); font-weight: 300; font-size: 14pt; line-height: 1; color: var(--fg); font-variation-settings: "opsz" 72; margin: .6mm 0 1mm; }
.step span { display: block; font-size: 6.8pt; line-height: 1.4; color: var(--fg-2); }
.step span i { font-style: normal; font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.stat .n { font-family: var(--font-display); font-weight: 300; font-size: 22pt; line-height: 1; color: var(--fg); font-variant-numeric: tabular-nums; font-variation-settings: "opsz" 144; }
.stat .n .plus { color: var(--accent); }
.stat .l { font-size: 6.5pt; color: var(--fg-2); margin-top: 1mm; }
.contact { font-size: 7.5pt; line-height: 1.65; color: var(--fg-2); }
.contact b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.wl { font-size: 6.5pt; }
"""

def services_html(asin=True):
    return "".join(f'<div class="svc"><span class="c">{n}</span><div><b>{esc(t)}</b><span>{esc(l)}</span>{("<em>As in " + esc(a) + "</em>") if asin else ""}</div></div>' for n, t, l, a, _ in C.SERVICES)
def steps_html():
    return "".join(f'<div class="step"><div class="ey">Step {n}</div><b>{esc(t)}</b><span>{esc(d)} <i>You receive {esc(r)}.</i></span></div>' for n, t, d, r in C.METHOD)
def stats_html():
    return "".join(f'<div class="stat"><div class="n">{n}<span class="plus">+</span></div><div class="l">{esc(l)}</div></div>' for n, l in C.PROOF)

# ------------------------------------------------------------------ Trifold
def trifold():
    css = COMMON + """
@page { size: 303mm 216mm; margin: 0; }
body { background: #000; }
.sheet { width: 303mm; height: 216mm; font-family: var(--font-text); }
.sheet.light { background: #F5F0E7; }
.in { position: absolute; left: 3mm; top: 3mm; width: 297mm; height: 210mm; }
.panel { position: absolute; top: 0; height: 210mm; }
.fold { position: absolute; top: -3mm; bottom: -3mm; border-left: 0.2pt dashed rgba(128,128,134,.6); }
@media print { .fold { display: none; } }
/* outside: flap 98 | back 99 | front 100 */
.p-flap { left: 0; width: 98mm; } .p-back { left: 98mm; width: 99mm; } .p-front { left: 197mm; width: 100mm; }
/* inside: 100 | 99 | 98 */
.p-i1 { left: 0; width: 100mm; } .p-i2 { left: 100mm; width: 99mm; } .p-i3 { left: 199mm; width: 98mm; }
.pad { position: absolute; left: 10mm; right: 10mm; top: 12mm; bottom: 12mm; }
.eyebrow, .eyebrow-quiet { font-size: 5.8pt; }
.p-front .mark { left: 10mm; top: 12mm; width: 30mm; }
.p-front .plate { position: absolute; left: 10mm; top: 40mm; width: 80mm; height: 100mm; border-radius: 5mm; }
.p-front .wl { position: absolute; left: 10mm; top: 143mm; }
.p-front .hl { position: absolute; left: 10mm; top: 156mm; width: 80mm; font-size: 20pt; line-height: 1.02; }
.p-front .url { position: absolute; left: 10mm; bottom: 12mm; font-size: 7pt; color: var(--fg-3); }
.p-back .hl { font-size: 17pt; margin: 1mm 0 4mm; }
.p-back .promises { font-size: 7pt; line-height: 1.6; color: var(--fg-2); margin-top: 4mm; border-top: 1px solid var(--line); padding-top: 3mm; }
.p-back .lock { left: 10mm; bottom: 13.5mm; width: 52mm; }   /* lockup minimum 50 mm; clear space ½ cap height above the rights line */
.p-back .rights { position: absolute; left: 10mm; right: 10mm; bottom: 4mm; font-size: 4.8pt; color: var(--fg-3); }
.p-flap .hl { font-size: 14pt; margin: 1mm 0 3mm; line-height: 1.05; }
.p-flap p { font-size: 7pt; line-height: 1.5; color: var(--fg-2); margin-bottom: 2.5mm; }
.p-flap .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 4mm; margin-top: 5mm; }
.p-flap .trust { font-size: 6.5pt; line-height: 1.45; color: var(--fg-3); margin-top: 5mm; border-top: 1px solid var(--line); padding-top: 3mm; }
.p-flap .plate { width: 78mm; height: 40mm; border-radius: 4mm; margin-top: 4mm; }
.p-i1 .hl, .p-i2 .hl, .p-i3 .hl { font-size: 14pt; margin: 1mm 0 3mm; line-height: 1.05; }
.p-i1 .sub, .p-i2 .sub { font-size: 7pt; line-height: 1.45; color: var(--fg-2); margin-bottom: 4mm; }
.p-i1 .all { font-size: 6.6pt; color: var(--fg-2); border-top: 1px solid var(--line); padding-top: 2mm; margin-top: 1mm; }
.p-i1 .all b { font-family: var(--font-display); font-weight: 300; font-size: 9.5pt; color: var(--fg); margin-right: 1mm; }
.case { margin-bottom: 4mm; }
.case .plate { width: 78mm; height: 36mm; border-radius: 4mm; }
.case .wl { margin-top: 1.5mm; }
.case p { font-size: 6.6pt; line-height: 1.4; color: var(--fg-2); margin-top: 1mm; }
.case p b { font-family: var(--font-display); font-weight: 300; font-size: 9pt; color: var(--fg); }
.p-i3 .see { position: absolute; left: 0; bottom: 0; font-size: 6.8pt; color: var(--fg-2); border-top: 1px solid var(--line); padding-top: 2mm; width: 78mm; }
.p-i3 .see b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
"""
    outside = f"""<section class="sheet grain" id="outside"><div class="in">
  <div class="panel p-flap"><div class="pad">
    <div class="eyebrow-quiet">About</div>
    <h2 class="hl opsz72">Strategy, craft and calm leadership, in one person<span class="pt">.</span></h2>
    <p>{esc(C.ABOUT_1)}</p><p>{esc(C.ABOUT_2)}</p>
    <div class="plate"><img src="{shared_img('portrait--4x5-2000.jpg')}" alt="Sanzeed Mirza" style="object-position: 50% 30%"></div>
    <div class="wl" style="margin-top:1.5mm"><b>Sanzeed Mirza</b><span class="sep">·</span>New Delhi</div>
    <div class="stats">{stats_html()}</div>
    <div class="trust">{esc(C.TRUST)}</div>
  </div></div>
  <div class="fold" style="left:98mm"></div>
  <div class="panel p-back"><div class="pad">
    <div class="eyebrow-quiet">Get in touch</div>
    <h2 class="hl opsz72">Tell me about the room<span class="pt">.</span></h2>
    <div class="contact">{esc(C.CALL_SUB)}<br><br><b>{C.EMAIL}</b><br>{C.WHATSAPP}<br>Call {C.PHONE}<br>{C.LINKEDIN}<br>{C.SITE}<br>{C.CITY}</div>
    <div class="promises">{'<br>'.join(esc(p) for p in C.PROMISES)}</div>
    <img class="mark lock" src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed — Experiential Design Consultant">
    <div class="rights">{esc(C.RIGHTS)}</div>
  </div></div>
  <div class="fold" style="left:197mm"></div>
  <div class="panel p-front">
    <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
    <div class="plate"><img src="{shared_img('hero-object--dark-4x5-1600.jpg')}" alt="The point of light"></div>
    <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
    <h1 class="hl">Experiential design you can walk into<span class="pt">.</span></h1>
    <div class="url">Sanzeed Mirza · Experiential Design Consultant · {C.SITE}</div>
  </div>
</div></section>"""
    cases = ""
    for key in C.CASE_ORDER:
        c = C.CASES[key]; im = {"prime-minister-museum": "case/prime-minister-museum-03", "ram-katha-show": "case/ram-katha-show-07", "buddha-park": "case/buddha-park-05"}[key]
        cases += f"""<div class="case"><div class="plate"><img src="{jimg(im)}" alt="{esc(c['title'])}"></div>
      <div class="wl"><b>{esc(c['title'])}</b><span class="sep">·</span>{esc(c['place'])}</div>
      <p><b>{esc(c['idea'])}</b> {esc(c['visitors'])}</p></div>"""
    inside = f"""<section class="sheet light theme-light" id="inside"><div class="in">
  <div class="panel p-i1"><div class="pad">
    <div class="eyebrow">Seven services</div>
    <h2 class="hl opsz72">Between two points of light<span class="pt">.</span></h2>
    <p class="sub">{esc(C.BETWEEN_SUB)}</p>
    {services_html(asin=False)}
    <div class="all"><b>All seven, every time.</b>{esc(C.ALL_SEVEN_SUB)}</div>
  </div></div>
  <div class="fold" style="left:100mm"></div>
  <div class="panel p-i2"><div class="pad">
    <div class="eyebrow">Method</div>
    <h2 class="hl opsz72">A method for the monumental<span class="pt">.</span></h2>
    <p class="sub">{esc(C.METHOD_SUB)}</p>
    {steps_html()}
  </div></div>
  <div class="fold" style="left:199mm"></div>
  <div class="panel p-i3"><div class="pad">
    <div class="eyebrow">Now showing</div>
    <h2 class="hl opsz72">Vision you can walk into<span class="pt">.</span></h2>
    {cases}
    <div class="see"><b>See the work.</b> Ninety projects, three case studies and the films at {C.SITE}</div>
  </div></div>
</div></section>"""
    return head("Sanzeed — A4 trifold brochure (outside + inside, 3 mm bleed)", "dark", css) + "<body>\n" + outside + "\n" + inside + "\n</body>\n</html>\n"

# ------------------------------------------------------------------ 12-page profile
PROFILE_CSS = COMMON + """
@page { size: 216mm 303mm; margin: 0; }
body { background: #000; }
.sheet { width: 216mm; height: 303mm; font-family: var(--font-text); }
.sheet.light { background: #F5F0E7; }
.in { position: absolute; left: 3mm; top: 3mm; width: 210mm; height: 297mm; }
.pad { position: absolute; left: 18mm; right: 18mm; top: 18mm; bottom: 18mm; }
.eyebrow, .eyebrow-quiet { font-size: 6.5pt; }
.folio { position: absolute; left: 18mm; right: 18mm; bottom: 10mm; display: flex; justify-content: space-between; font-size: 6.5pt; color: var(--fg-3); }
.hl { line-height: 1.04; }
h2.hl { font-size: 26pt; margin: 1.5mm 0 5mm; }
p.body { font-size: 8.5pt; line-height: 1.6; color: var(--fg-2); margin-bottom: 3.5mm; max-width: 120mm; }
p.lead { font-size: 10.5pt; line-height: 1.5; color: var(--fg-2); margin-bottom: 5mm; max-width: 130mm; }
.cover .mark { left: 18mm; top: 18mm; width: 44mm; }
.cover .plate { position: absolute; left: 18mm; top: 52mm; width: 174mm; height: 130mm; border-radius: 7mm; }
.cover .wl { position: absolute; left: 18mm; top: 186mm; font-size: 7pt; }
.cover .eyebrow-quiet { position: absolute; left: 18mm; top: 206mm; }
.cover .hl { position: absolute; left: 18mm; top: 213mm; width: 170mm; font-size: 40pt; line-height: 1.0; }
.cover .url { position: absolute; left: 18mm; bottom: 18mm; font-size: 7.5pt; color: var(--fg-3); }
.idea .hl { font-size: 44pt; margin-bottom: 7mm; }
.idea .story { columns: 2; column-gap: 8mm; max-width: none; }
.idea .plate { position: absolute; left: 0; right: 0; bottom: 8mm; height: 92mm; border-radius: 6mm; }
.idea .wl { position: absolute; left: 0; bottom: 0; }
.idea .story p { font-size: 9pt; line-height: 1.6; color: var(--fg-2); margin-bottom: 3.5mm; break-inside: avoid; }
.idea .story p:last-child { font-family: var(--font-display); font-weight: 300; font-size: 13pt; color: var(--fg); line-height: 1.25; }
.idea .beam-h { display: none; }
.about .plate { position: absolute; right: 0; top: 0; width: 62mm; height: 78mm; border-radius: 5mm; }
.about .wl { position: absolute; right: 0; top: 80mm; width: 62mm; }
.about .text { width: 100mm; }
.about .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; margin-top: 8mm; padding-top: 5mm; border-top: 1px solid var(--line); }
.about .trust { font-size: 7.5pt; color: var(--fg-3); margin-top: 5mm; }
.pillars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; margin-top: 10mm; padding-top: 5mm; border-top: 1px solid var(--line); }
.pillar .r { font-family: var(--font-display); font-weight: 300; font-size: 14pt; color: var(--accent-text); font-variation-settings: "opsz" 72; }
.pillar b { display: block; font-family: var(--font-heading); font-weight: 600; font-size: 11pt; color: var(--fg); margin: 1.5mm 0 1.5mm; }
.pillar span { font-size: 8.5pt; line-height: 1.5; color: var(--fg-2); }
.quote { position: absolute; left: 0; right: 0; bottom: 0; font-family: var(--font-display); font-style: italic; font-weight: 300; font-size: 13pt; line-height: 1.35; color: var(--fg); font-variation-settings: "opsz" 72, "SOFT" 50; max-width: 150mm; }
.quote span { display: block; font-family: var(--font-text); font-style: normal; font-size: 7.5pt; color: var(--fg-3); margin-top: 2mm; }
.services .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm 10mm; }
.services .grid { gap: 6mm 10mm; } .services .svc { grid-template-columns: 8mm 1fr; } .services .svc b { font-size: 11.5pt; margin-bottom: 1mm; } .services .svc span { font-size: 9pt; } .services .svc em { font-size: 7.5pt; margin-top: 1mm; }
.services .all { margin-top: 8mm; border-top: 1px solid var(--line); padding-top: 5mm; font-size: 8.5pt; color: var(--fg-2); }
.services .all b { font-family: var(--font-display); font-weight: 300; font-size: 16pt; color: var(--fg); display: block; margin-bottom: 1.5mm; }
.method .steps { position: relative; margin-top: 4mm; }
.method .step { padding-left: 12mm; margin-bottom: 13mm; }
.method .step::before { width: 3mm; height: 3mm; top: 2mm; }
.method .step b { font-size: 26pt; margin: 1mm 0 2.5mm; }
.method .step span { font-size: 9.5pt; max-width: 135mm; }
.method .route { position: absolute; left: 1.4mm; top: 4mm; bottom: 10mm; width: 1px; background: var(--line); }
.case-l .n { font-family: var(--font-heading); font-weight: 500; font-size: 6.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--fg-3); }
.case-l .title { font-size: 34pt; margin: 2mm 0 1mm; }
.case-l .place { font-size: 9pt; color: var(--fg-2); margin-bottom: 7mm; }
.case-l h3 { font-family: var(--font-heading); font-weight: 600; font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); margin: 5mm 0 1.5mm; }
.case-l .idea-l { font-family: var(--font-display); font-weight: 300; font-size: 18pt; color: var(--fg); margin: 1mm 0 2mm; font-variation-settings: "opsz" 72; }
.case-l .plate { position: absolute; left: 0; right: 0; bottom: 8mm; height: 118mm; border-radius: 6mm; }
.case-l .wl { position: absolute; left: 0; bottom: 0; }
.case-r .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.case-r .plate { height: 58mm; border-radius: 4mm; }
.case-r .cap { font-size: 6.5pt; color: var(--fg-3); margin-top: 1.5mm; line-height: 1.4; }
.case-r .cap b { font-family: var(--font-heading); font-weight: 500; color: var(--accent-text); letter-spacing: .08em; margin-right: 1.5mm; font-variant-numeric: tabular-nums; }
.case-r h3 { font-family: var(--font-heading); font-weight: 600; font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); margin: 6mm 0 1.5mm; }
.case-r .meta { position: absolute; left: 0; right: 0; bottom: 0; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; border-top: 1px solid var(--line); padding-top: 3mm; font-size: 7.5pt; color: var(--fg-2); }
.case-r .meta b { display: block; font-family: var(--font-heading); font-weight: 600; font-size: 6.5pt; letter-spacing: .1em; text-transform: uppercase; color: var(--fg-3); margin-bottom: 1mm; }
.back h2.hl { font-size: 20pt; margin: 1mm 0 3mm; }
.back .cols { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0 4mm; }
.back .cat { font-family: var(--font-heading); font-weight: 600; font-size: 5.8pt; letter-spacing: .1em; text-transform: uppercase; color: var(--accent-text); border-bottom: 1px solid var(--line); padding-bottom: 1mm; margin-bottom: 1.2mm; }
.back .item { font-size: 5.6pt; line-height: 1.45; color: var(--fg-3); display: grid; grid-template-columns: 5.5mm 1fr; }
.back .item .c { font-family: var(--font-heading); font-weight: 500; color: var(--accent-text); font-size: 5pt; letter-spacing: .05em; padding-top: .3mm; font-variant-numeric: tabular-nums; }
.back .item b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.back .tl { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2mm 5mm; margin-top: 3mm; }
.back .tl div { font-size: 6.8pt; line-height: 1.4; color: var(--fg-2); border-top: 1px solid var(--line); padding-top: 1.5mm; }
.back .tl b { display: block; font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.back .tl i { font-style: normal; color: var(--accent-text); font-size: 6pt; letter-spacing: .06em; font-variant-numeric: tabular-nums; }
.back .touch { display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; margin-top: 6mm; border-top: 1px solid var(--line); padding-top: 5mm; }
.back .touch .hl { font-size: 20pt; margin-bottom: 3mm; }
.back .lock { position: absolute; right: 0; bottom: 0; width: 50mm; }
.back .rights { position: absolute; left: 0; bottom: 0; width: 100mm; font-size: 5.5pt; color: var(--fg-3); }
.back .sec { margin-top: 7mm; }
"""

def page(id_, cls, inner, theme, folio_l, folio_r, grain=True):
    th = "theme-light light" if theme == "light" else ("grain" if grain else "")
    return f'<section class="sheet {th} {cls}" id="{id_}"><div class="in"><div class="pad">{inner}</div><div class="folio"><span>{esc(folio_l)}</span><span>{esc(folio_r)}</span></div></div></section>'

def case_pages(key, n, pno):
    c = C.CASES[key]; hero = {"prime-minister-museum": 3, "ram-katha-show": 7, "buddha-park": 8}[key]
    grid_imgs = {"prime-minister-museum": [1, 4, 5, 7], "ram-katha-show": [1, 2, 3, 5], "buddha-park": [2, 3, 5, 6]}[key]
    left = f"""<div class="n">Case study · {n:03d} · {esc(c['type'])}</div>
    <h2 class="hl title">{esc(c['title'])}<span class="pt">.</span></h2><div class="place">{esc(c['place'])}</div>
    <h3>The brief</h3><p class="body">{esc(c['brief'])}</p>
    <h3>The idea</h3><div class="idea-l">{esc(c['idea'])}</div><p class="body">{esc(c['idea_text'])}</p>
    <div class="plate"><img src="{jimg(f'case/{key}-{hero:02d}')}" alt="{esc(c['captions'][hero-1])}"></div>
    <div class="wl"><b>{esc(c['title'])}</b><span class="sep">·</span>{esc(c['place'])}<span class="sep">·</span>{hero:03d} {esc(c['captions'][hero-1])}</div>"""
    grid = "".join(f'<div><div class="plate"><img src="{jimg(f"case/{key}-{i:02d}")}" alt="{esc(c["captions"][i-1])}"></div><div class="cap"><b>{i:03d}</b>{esc(c["captions"][i-1])}</div></div>' for i in grid_imgs)
    right = f"""<div class="grid">{grid}</div>
    <h3>The walk</h3><p class="body">{esc(c['walk'])}</p>
    <h3>What visitors do</h3><p class="body" style="font-family:var(--font-display);font-weight:300;font-size:13pt;line-height:1.3;color:var(--fg);font-variation-settings:'opsz' 72">{esc(c['visitors'])}</p>
    <div class="meta"><div><b>Type</b>{esc(c['type'])}</div><div><b>Location</b>{esc(c['place'])}</div><div><b>Role</b>{esc(c['role'])}</div></div>"""
    return (page(f"p{pno}", "case-l", left, "dark", f"{pno:02d}", f"Sanzeed Mirza · Experiential Design Consultant"),
            page(f"p{pno+1}", "case-r", right, "dark", f"{esc(c['title'])} · {esc(c['place'])}", f"{pno+1:02d}"))

def profile():
    pages = []
    # 1 cover
    pages.append(f"""<section class="sheet grain cover" id="p1"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant · Profile 2026</div>
  <h1 class="hl">Experiential design you can walk into<span class="pt">.</span></h1>
  <div class="url">{C.SITE} · {C.CITY}</div>
</div></section>""")
    # 2 the one idea
    story = "".join(f"<p>{esc(p)}</p>" for p in C.STORY)
    pages.append(page("p2", "idea", f"""<div class="eyebrow-quiet">The one idea</div><h2 class="hl">Carry the light across<span class="pt">.</span></h2>
    <p class="lead">{esc(C.BETWEEN_SUB)}</p><div class="story">{story}</div>
    <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div><div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>""", "dark", "02", "The one idea"))
    # 3 about + pillars
    pillars = "".join(f'<div class="pillar"><div class="r">{r}</div><b>{esc(t)}</b><span>{esc(d)}</span></div>' for r, t, d in C.PILLARS)
    pages.append(page("p3", "about", f"""<div class="text"><div class="eyebrow">About</div><h2 class="hl">Strategy, craft and calm leadership, in one person<span class="pt">.</span></h2>
    <p class="body">{esc(C.ABOUT_1)}</p><p class="body">{esc(C.ABOUT_2)}</p></div>
    <div class="plate"><img src="{shared_img('portrait--4x5-2000.jpg')}" alt="Sanzeed Mirza"></div><div class="wl"><b>Sanzeed Mirza</b><span class="sep">·</span>New Delhi</div>
    <div class="stats">{stats_html()}</div><div class="trust">{esc(C.TRUST)}</div>
    <div class="pillars">{pillars}</div>
    <div class="quote">“{esc(C.QUOTE)}”<span>— Sanzeed Mirza</span></div>""", "light", "About · Three pillars", "03"))
    # 4 services
    pages.append(page("p4", "services", f"""<div class="eyebrow">Seven services</div><h2 class="hl">Between two points of light<span class="pt">.</span></h2>
    <p class="lead">{esc(C.BETWEEN_SUB)}</p><div class="grid">{services_html()}</div>
    <div class="all"><b>All seven, every time.</b>{esc(C.ALL_SEVEN_SUB)}</div>""", "light", "04", "Seven services"))
    # 5 method
    pages.append(page("p5", "method", f"""<div class="eyebrow">Method</div><h2 class="hl">A method for the monumental<span class="pt">.</span></h2>
    <p class="lead">{esc(C.METHOD_SUB)}</p><div class="steps"><div class="route"></div>{steps_html()}</div>""", "light", "Method", "05"))
    # 6-11 cases
    for i, key in enumerate(C.CASE_ORDER):
        l, r = case_pages(key, i + 1, 6 + i * 2); pages += [l, r]
    # 12 galleries + journey + contact
    cols = ""; k = 0
    groups = []
    mus = [g for g in C.GALLERY if g["cat"] == "Museums & Experience Centres"]
    groups.append(("Museums & Experience Centres", mus[:30])); groups.append(("Museums & Experience Centres", mus[30:]))
    groups.append(("Projection Mapping & Shows", [g for g in C.GALLERY if g["cat"] == "Projection Mapping & Shows"]))
    groups.append(("Explainer Videos & Others", [g for g in C.GALLERY if g["cat"] == "Explainer Videos & Others"]))
    for cat, items in groups:
        rows = "".join(f'<div class="item"><span class="c">{(k:=k+1):03d}</span><span><b>{esc(g["title"])}</b> · {esc(g["place"])}</span></div>' for g in items)
        cols += f'<div><div class="cat">{esc(cat)}</div>{rows}</div>'
    tl = "".join(f'<div><i>{esc(d)}</i><b>{esc(r)}</b>{esc(o)}</div>' for d, r, o, _ in C.TIMELINE)
    pages.append(page("p12", "back", f"""<div class="eyebrow">The galleries</div><h2 class="hl">90 projects, one continuous craft<span class="pt">.</span></h2>
    <div class="cols">{cols}</div>
    <div class="sec"><div class="eyebrow">Journey</div><h2 class="hl" style="font-size:16pt">Fifteen years, one through-line<span class="pt">.</span></h2><div class="tl">{tl}</div></div>
    <div class="touch"><div><div class="eyebrow">Get in touch</div><h2 class="hl">Tell me about the room<span class="pt">.</span></h2><div class="contact">{esc(C.CALL_SUB)} {esc(C.PROMISES[0])}</div></div>
    <div class="contact" style="padding-top:9mm"><b>{C.EMAIL}</b><br>{C.WHATSAPP} · Call {C.PHONE}<br>{C.LINKEDIN} · {C.SITE}<br>{C.CITY}</div></div>
    <div class="rights">{esc(C.RIGHTS)}</div><img class="lock" src="{logo('horizontal-descriptor','full-colour-light')}" alt="Sanzeed — Experiential Design Consultant">""", "light", "The galleries · Journey · Get in touch", "12"))
    return head("Sanzeed — company profile, 12 pages A4 (3 mm bleed)", "dark", PROFILE_CSS) + "<body>\n" + "\n".join(pages) + "\n</body>\n</html>\n"

def trim_png(path, px):
    im = Image.open(path); im.crop((px, px, im.width - px, im.height - px)).save(path)

if __name__ == "__main__":
    jobs = []
    hp = write(f"{SRC}/sanzeed-brochure--a4-trifold.html", trifold())
    jobs.append(pdf(hp, f"{OUT}/sanzeed-brochure--a4-trifold-bleed.pdf", 303, 216))
    for side in ("outside", "inside"):
        jobs.append(png(hp, f"{OUT}/sanzeed-brochure--a4-trifold-{side}.png", math.ceil(303 * PX) + 2, math.ceil(216 * PX) + 2, 2.5, selector=f"#{side}"))
    hp2 = write(f"{SRC}/sanzeed-company-profile--a4-12pp.html", profile())
    jobs.append(pdf(hp2, f"{OUT}/sanzeed-company-profile--a4-12pp-bleed.pdf", 216, 303))
    render_jobs(jobs)
    print_ready(f"{OUT}/sanzeed-brochure--a4-trifold-bleed.pdf", f"{OUT}/sanzeed-brochure--a4-trifold-print-ready-cmyk.pdf", "297x210")
    print_ready(f"{OUT}/sanzeed-company-profile--a4-12pp-bleed.pdf", f"{OUT}/sanzeed-company-profile--a4-12pp-print-ready-cmyk.pdf", "210x297")
    # profile spreads (bleed cropped)
    tmp = f"{OUT}/_pages"; os.makedirs(tmp, exist_ok=True)
    pages = pdf_pages_png(f"{OUT}/sanzeed-company-profile--a4-12pp-bleed.pdf", f"{tmp}/p", 110)
    for p in pages: trim_png(p, round(3 / 25.4 * 110))
    outs = spreads(pages, OUT, "sanzeed-company-profile--a4-12pp")
    for p in pages: os.remove(p)
    os.rmdir(tmp)
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"): print(f, len(page_sizes(f"{OUT}/{f}")), page_sizes(f"{OUT}/{f}")[0])
    print("brochures done", folder_size_mb(OUT), "MB")
