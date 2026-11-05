#!/usr/bin/env python3
"""build_signage.py — Signage/: door plate, wayfinding arrow plates + room numbers, totem (1:10), window vinyl,
and the signage spec sheet. Each sign is an HTML source → PDF (vector, fonts embedded) → SVG (pdftocairo, text as
paths, for sign-makers) → PNG preview → print-ready PDF with bleed, crop marks and CMYK (print_pdf.py)."""
import os, sys, math, shutil, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C
from pypdf import PdfWriter, PdfReader

OUT = f"{MC}/Signage"; SRC = f"{OUT}/src"; os.makedirs(SRC, exist_ok=True)
PX = 96 / 25.4
def mm_png_job(html, out, w, h, scale=3, selector="#art"):
    return png(html, out, math.ceil(w * PX) + 2, math.ceil(h * PX) + 2, scale, selector=selector)

BASE = """
@page { margin: 0; }
body { background: #000; }
.sheet { font-family: var(--font-text); background: #000; color: var(--fg); }
.in { position: absolute; left: 3mm; top: 3mm; }
.note { position: absolute; left: 0; right: 0; bottom: 0; font-size: 0; }
"""

def plate(id_, inner, extra=""):
    css = BASE + """
@page { size: 306mm 106mm; }
.sheet { width: 306mm; height: 106mm; }
.in { width: 300mm; height: 100mm; }
.lock { position: absolute; left: 20mm; top: 50%; transform: translateY(-50%); width: 180mm; display: block; }
.arrow { position: absolute; left: 24mm; top: 26mm; width: 48mm; height: 48mm; }
.sym { position: absolute; right: 22mm; top: 50%; transform: translateY(-50%); width: 24mm; }
.room { position: absolute; left: 24mm; top: 50%; transform: translateY(-50%); font-family: var(--font-display); font-weight: 300; font-size: 150pt; line-height: 1; font-variant-numeric: tabular-nums; font-variation-settings: "opsz" 144, "SOFT" 30, "WONK" 0; letter-spacing: -0.01em; color: var(--fg); }
.room .pt { color: var(--accent); }
.dir { position: absolute; left: 86mm; top: 50%; transform: translateY(-50%); font-family: var(--font-heading); font-weight: 600; font-size: 44pt; letter-spacing: -0.01em; color: var(--fg); }
""" + extra
    return head(f"Sanzeed — signage plate 300x100 mm ({id_})", "dark", css) + f'<body><section class="sheet" id="art"><div class="in">{inner}</div></section></body>\n</html>\n'

def door_plate():
    return plate("door", f'<img class="lock" src="{logo("horizontal-descriptor","full-colour-dark")}" alt="Sanzeed — Experiential Design Consultant">')

ARROWS = [("left", "arrow-left"), ("right", "arrow-right"), ("ahead", "arrow-up"), ("down", "arrow-down")]
def arrow_plate(name, ic):
    inner = f'<img class="arrow" src="{icon(ic + "--white")}" alt="{name}"><img class="sym" src="{logo("symbol","full-colour-dark")}" alt="S.">'
    return plate(f"arrow-{name}", inner)

def room_plate(n):
    inner = f'<div class="room">{n:03d}<span class="pt">.</span></div><img class="sym" src="{logo("symbol","full-colour-dark")}" alt="S.">'
    return plate(f"room-{n:03d}", inner)

def totem():   # 600 x 1800 mm at 1:10 → 60 x 180 mm (no bleed; panel is cut to size)
    css = BASE + """
@page { size: 60mm 180mm; }
.sheet { width: 60mm; height: 180mm; }
.lock { position: absolute; left: 10mm; top: 14mm; width: 40mm; }
.beam-h { position: absolute; left: 10mm; width: 40mm; top: 44mm; }
.dir { position: absolute; left: 10mm; top: 52mm; width: 40mm; }
.dir .row { display: flex; align-items: center; justify-content: space-between; height: 14mm; border-bottom: 0.2pt solid rgba(255,255,255,.12); }
.dir .n { font-family: var(--font-display); font-weight: 300; font-size: 26pt; line-height: 1; font-variant-numeric: tabular-nums; font-variation-settings: "opsz" 72; }
.dir img { width: 7mm; height: 7mm; }
.line { position: absolute; left: 10mm; top: 128mm; width: 40mm; font-family: var(--font-display); font-weight: 300; font-size: 12pt; line-height: 1.1; font-variation-settings: "opsz" 72; }
.url { position: absolute; left: 10mm; bottom: 12mm; font-size: 5pt; color: var(--fg-3); }
"""
    rows = "".join(f'<div class="row"><span class="n">{n:03d}</span><img src="{icon(ic + "--white")}" alt=""></div>' for n, ic in [(1, "arrow-left"), (2, "arrow-right"), (3, "arrow-up"), (4, "arrow-down")])
    body = f"""<body><section class="sheet" id="art">
  <img class="lock" src="{logo('vertical-stacked','full-colour-dark')}" alt="Sanzeed — Experiential Design Consultant">
  <div class="beam-h"></div>
  <div class="dir">{rows}</div>
  <div class="line">Experiential design you can walk into<span class="pt">.</span></div>
  <div class="url">{C.SITE}</div>
</section></body>
</html>
"""
    return head("Sanzeed — totem 600x1800 mm (1:10)", "dark", css) + body

def window_vinyl():   # glass bay 3000 x 2000 mm at 1:10 → 300 x 200 mm preview
    css = BASE + """
@page { size: 300mm 200mm; }
.sheet { width: 300mm; height: 200mm; background: #0D0D0F; }
.glass { position: absolute; inset: 0; background: linear-gradient(160deg, #15161a 0%, #0b0b0d 100%); }
.frost { position: absolute; left: 0; right: 0; top: 70mm; height: 60mm; background: rgba(245,245,247,.16); backdrop-filter: blur(1px); }
.mark { position: absolute; left: 90mm; top: 91.6mm; width: 120mm; }
.mullion { position: absolute; top: 0; bottom: 0; width: 1.2mm; background: #000; }
.cap { position: absolute; left: 10mm; bottom: 6mm; font-size: 5pt; color: var(--fg-3); }
"""
    body = f"""<body><section class="sheet" id="art">
  <div class="glass"></div>
  <div class="frost"></div>
  <img class="mark" src="{logo('primary-wordmark','white')}" alt="Sanzeed">
  <div class="mullion" style="left:99.4mm"></div><div class="mullion" style="left:199.4mm"></div>
  <div class="cap">Window vinyl · glass bay 3000 × 2000 mm at 1:10 · frosted etch film band 600 mm high, bottom edge 700 mm above floor · wordmark 1200 mm wide, cut in white vinyl (or reverse-cut clear in the frost) · cut file: sanzeed-window-vinyl--wordmark-cut-1200mm.svg</div>
</section></body>
</html>
"""
    return head("Sanzeed — window vinyl preview 3000x2000 mm (1:10)", "dark", css) + body

def cut_file(out):
    """1:1 cut file: the white wordmark at 1200 mm wide (SVG units = mm)."""
    src = open(f"{LOGO_SVG}/sanzeed-primary-wordmark--white.svg", encoding="utf-8").read()
    src = re.sub(r'width="3590"', 'width="1200mm"', src, count=1); src = re.sub(r'height="500"', f'height="{1200*500/3590:.2f}mm"', src, count=1)
    src = src.replace("<title>Sanzeed — primary-wordmark (white)</title>", "<title>Sanzeed — window vinyl cut file — wordmark 1200 mm (white)</title>")
    open(out, "w", encoding="utf-8").write(src); return out

def spec_sheet():
    css = """
@page { size: 210mm 297mm; margin: 0; }
body { background: var(--bg); }
.sheet { width: 210mm; height: 297mm; padding: 18mm 18mm 0; font-size: 8pt; line-height: 1.45; color: var(--fg); }
.mark { width: 48mm; display: block; }
.eyebrow { margin-top: 7mm; font-size: 7pt; }
h1 { font-size: 22pt; margin: 1.5mm 0 3mm; }
h2 { font-family: var(--font-heading); font-weight: 600; font-size: 9.5pt; margin: 5mm 0 1.5mm; }
table { width: 100%; }
th, td { font-size: 7.5pt; line-height: 1.35; padding: 1.1mm 2.5mm 1.1mm 0; }
.cols2 { display: grid; grid-template-columns: 1fr 1.25fr; gap: 0 8mm; }
.cols3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0 6mm; }
.foot { position: absolute; left: 18mm; right: 18mm; bottom: 12mm; font-size: 6.5pt; color: var(--fg-3); display: flex; justify-content: space-between; }
ul { padding-left: 3.5mm; margin: 0; } li { margin: 0 0 0.8mm; }
.rule { color: var(--fg-2); margin-top: 1.5mm; font-size: 7.5pt; }
"""
    dist = [(1, 10), (2, 17), (3, 25), (5, 42), (8, 67), (10, 85), (15, 125), (20, 170), (30, 250)]
    uses = ["Desk and door plates, directories", "Door plates, room numbers", "Wayfinding plates in corridors", "Lobby directories, welcome boards", "Totem headline, backdrop line", "Exterior door signs, booth wall copy", "Wordmark on backdrops and booth walls", "Window vinyl wordmark, fascia", "Building fascia, large wall"]
    rows = "".join(f'<tr><td class="num">{d} m</td><td class="num">{h} mm</td><td>{u}</td></tr>' for (d, h), u in zip(dist, uses))
    body = f"""<body><section class="sheet" id="art">
  <img class="mark" src="{logo('horizontal-descriptor','full-colour-light')}" alt="Sanzeed — Experiential Design Consultant">
  <div class="eyebrow">Signage specification</div>
  <h1 class="hl opsz72">Signs, materials and mounting<span class="pt">.</span></h1>
  <p>This sheet accompanies the artwork in <b>10_MARKETING_COLLATERAL/Signage</b>. Every sign uses the wordmark or the symbol from <b>02_LOGO_SYSTEM</b>, Gallery Black backgrounds, Gallery White letters and one gold point. Scaled artwork is marked in the file name (1:10 = 10 % of real size).</p>
  <div class="cols2">
  <div>
  <h2>Minimum cap height by viewing distance</h2>
  <table><tr><th>Viewing distance</th><th>Cap height ≥</th><th>Typical sign</th></tr>{rows}</table>
  <p class="rule">Rule: 25 mm cap height per 3 m of viewing distance (≈ 8.5 mm per metre); never below 10 mm on any sign. Cap height is the height of a capital letter, not the point size.</p>
  </div>
  <div>
  <h2>Materials</h2>
  <table>
  <tr><th>Sign</th><th>Size</th><th>Construction</th></tr>
  <tr><td>Door plate, arrow plates, room numbers</td><td class="num">300 × 100 × 3 mm</td><td>Matt black acrylic or powder-coated aluminium (RAL 9005 matt). Letters and arrows in white cut vinyl or UV print; the point in gold vinyl (Old Gold; nearest Pantone 7510 C — verify) or a brushed-brass inlay.</td></tr>
  <tr><td>Totem</td><td class="num">600 × 1800 mm</td><td>4 mm aluminium composite panel on a steel frame, matt black; graphics UV-printed or cut vinyl; optional edge-lit gold point.</td></tr>
  <tr><td>Window vinyl</td><td class="num">1200 mm wordmark</td><td>Frosted etch film band 600 mm high, bottom edge 700 mm above floor; wordmark cut in white vinyl on the frost, or reverse-cut clear. Apply wet, squeegee from the centre.</td></tr>
  <tr><td>Backdrop, booth wall, roll-up</td><td class="num">1:10 / 1:5 artwork</td><td>Matt fabric (SEG) or blockout PVC; rich black C60 M40 Y40 K100 for large solids; gold as process C0 M27 Y68 K28 or spot.</td></tr>
  </table>
  </div></div>
  <div class="cols3">
  <div><h2>Clear space and minimum sizes</h2>
  <ul><li>Clear space x = ½ the cap height of the wordmark in use, on all sides; nothing enters it.</li>
  <li>Minimum widths: wordmark 28 mm; horizontal-descriptor lockup 50 mm; vertical stack 22 mm; symbol 6 mm.</li>
  <li>Arrow icons: monoline, 64/500 stroke, round caps; the gold point at the tail. Arrow box 48 mm on a 300 × 100 plate.</li></ul></div>
  <div><h2>Mounting</h2>
  <ul><li>Plates: four Ø12 mm black stand-offs, 10 mm projection, 12 mm from each corner; or VHB tape on glass and laminate.</li>
  <li>Door plates: centre line 1500 mm above finished floor, 50 mm from the latch-side architrave.</li>
  <li>Wayfinding: centre line 1600 mm, at decision points, perpendicular to the route; room numbers beside the door, latch side.</li>
  <li>Totem: free-standing, weighted base; directory centred 1200–1500 mm.</li>
  <li>Backdrop: wordmark centre 1700 mm above floor, visible behind standing guests.</li></ul></div>
  <div><h2>Colour and finish</h2>
  <ul><li>Black: Gallery Black 100 K (rich black for solids). White: Gallery White.</li>
  <li>Gold: one point per sign. Never tints of gold, never gradients, never glow effects in print.</li>
  <li>Finish matt throughout; no gloss on black panels (fingerprints, reflections).</li>
  <li>Proof every gold on the chosen substrate before the run.</li></ul></div>
  </div>
  <div class="foot"><span>Sanzeed Mirza · Experiential Design Consultant · {C.SITE}</span><span>Signage spec · sources in Signage/src · logos in 02_LOGO_SYSTEM</span></div>
</section></body>
</html>
"""
    return head("Sanzeed — signage specification sheet A4", "light", css) + body

def to_svg(pdf_path, svg_path):
    run(["pdftocairo", "-svg", pdf_path, svg_path]); return svg_path

if __name__ == "__main__":
    jobs = []; items = []
    items.append(("sanzeed-door-plate--300x100mm", door_plate(), 306, 106, "300x100"))
    for name, ic in ARROWS: items.append((f"sanzeed-wayfinding--arrow-{name}-300x100mm", arrow_plate(name, ic), 306, 106, "300x100"))
    for n in range(1, 5): items.append((f"sanzeed-wayfinding--room-{n:03d}-300x100mm", room_plate(n), 306, 106, "300x100"))
    items.append(("sanzeed-totem--600x1800mm-1-10", totem(), 60, 180, None))
    items.append(("sanzeed-window-vinyl--preview-3000x2000mm-1-10", window_vinyl(), 300, 200, None))
    for stem, html_, w, h, trim in items:
        hp = write(f"{SRC}/{stem}.html", html_)
        jobs.append(pdf(hp, f"{OUT}/{stem}.pdf", w, h)); jobs.append(mm_png_job(hp, f"{OUT}/{stem}.png", w, h, 4 if w < 100 else 3))
    hp = write(f"{SRC}/sanzeed-signage-spec-sheet--a4.html", spec_sheet())
    jobs.append(pdf(hp, f"{OUT}/sanzeed-signage-spec-sheet--a4.pdf", 210, 297)); jobs.append(mm_png_job(hp, f"{OUT}/sanzeed-signage-spec-sheet--a4.png", 210, 297, 2))
    render_jobs(jobs)
    for stem, _, w, h, trim in items:
        to_svg(f"{OUT}/{stem}.pdf", f"{OUT}/{stem}.svg")
        if trim: print_ready(f"{OUT}/{stem}.pdf", f"{OUT}/{stem}-print-ready-cmyk.pdf", trim)
    cut_file(f"{OUT}/sanzeed-window-vinyl--wordmark-cut-1200mm.svg")
    # combined wayfinding set PDF
    wr = PdfWriter()
    for stem, _, w, h, trim in items[1:9]:
        for p in PdfReader(f"{OUT}/{stem}.pdf").pages: wr.add_page(p)
    wr.write(f"{OUT}/sanzeed-wayfinding-set--8-plates-300x100mm.pdf")
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"): print(f, page_sizes(f"{OUT}/{f}")[:2])
    print("signage done", folder_size_mb(OUT), "MB")
