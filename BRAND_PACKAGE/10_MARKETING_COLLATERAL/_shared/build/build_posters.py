#!/usr/bin/env python3
"""build_posters.py — Posters/: three posters (campaign, method, typographic) at A2 and A3.
Each size has its own HTML source (A3 is the A2 layout scaled by 0.7071 in mm). Exports: PDF (bleed page),
print-ready CMYK PDF with crop marks (print_pdf.py), PNG preview."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C

OUT = f"{MC}/Posters"; SRC = f"{OUT}/src"; os.makedirs(SRC, exist_ok=True)
PX = 96 / 25.4
SIZES = {"a2": (420, 594, 1.0), "a3": (297, 420, 297 / 420)}

def base_css(w, h, s, theme):
    bleed = 3
    return f"""
@page {{ size: {w + 2*bleed}mm {h + 2*bleed}mm; margin: 0; }}
body {{ background: {'#000' if theme == 'dark' else '#F5F0E7'}; }}
.sheet {{ width: {w + 2*bleed}mm; height: {h + 2*bleed}mm; font-family: var(--font-text); }}
.in {{ position: absolute; left: {bleed}mm; top: {bleed}mm; width: {w}mm; height: {h}mm; }}
.mark {{ position: absolute; display: block; }}
.hl {{ color: var(--fg); }}
"""

def mm(v, s): return f"{v*s:.2f}mm"
def pt(v, s): return f"{v*s:.2f}pt"

def campaign(size):
    w, h, s = SIZES[size]
    css = base_css(w, h, s, "dark") + f"""
.mark {{ left: {mm(30,s)}; top: {mm(30,s)}; width: {mm(90,s)}; }}
.eyebrow-quiet {{ position: absolute; left: {mm(30,s)}; top: {mm(96,s)}; font-size: {pt(11,s)}; }}
.hl {{ position: absolute; left: {mm(30,s)}; top: {mm(108,s)}; width: {mm(360,s)}; font-size: {pt(150,s)}; line-height: 1.0; }}
.sub {{ position: absolute; left: {mm(30,s)}; top: {mm(240,s)}; width: {mm(250,s)}; font-size: {pt(16,s)}; line-height: 1.5; color: var(--fg-2); }}
.plate {{ position: absolute; left: {mm(30,s)}; top: {mm(290,s)}; width: {mm(360,s)}; height: {mm(202,s)}; border-radius: {mm(10,s)}; }}
.wl {{ position: absolute; left: {mm(30,s)}; top: {mm(498,s)}; font-size: {pt(11,s)}; }}
.contact {{ position: absolute; left: {mm(30,s)}; bottom: {mm(30,s)}; font-size: {pt(13,s)}; line-height: 1.7; color: var(--fg-2); }}
.contact b {{ font-family: var(--font-heading); font-weight: 600; color: var(--fg); }}
.url {{ position: absolute; right: {mm(30,s)}; bottom: {mm(31,s)}; font-size: {pt(13,s)}; color: var(--fg-3); }}
"""
    body = f"""<body><section class="sheet grain" id="art"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant</div>
  <h1 class="hl">Carry the light across<span class="pt">.</span></h1>
  <p class="sub">{esc(C.BETWEEN_SUB)}</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <div class="contact"><b>Tell me about the room.</b><br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE}</div>
  <div class="url">{C.SITE}</div>
</div></section></body>
</html>
"""
    return head(f"Sanzeed — campaign poster {size.upper()}", "dark", css) + body

def method(size):
    w, h, s = SIZES[size]
    css = base_css(w, h, s, "dark") + f"""
.mark {{ left: {mm(30,s)}; top: {mm(30,s)}; width: {mm(90,s)}; }}
.eyebrow-quiet {{ position: absolute; left: {mm(30,s)}; top: {mm(96,s)}; font-size: {pt(11,s)}; }}
.hl {{ position: absolute; left: {mm(30,s)}; top: {mm(108,s)}; width: {mm(360,s)}; font-size: {pt(96,s)}; line-height: 1.0; }}
.sub {{ position: absolute; left: {mm(30,s)}; top: {mm(190,s)}; width: {mm(300,s)}; font-size: {pt(15,s)}; line-height: 1.5; color: var(--fg-2); }}
.route {{ position: absolute; left: {mm(38,s)}; top: {mm(236,s)}; width: 1px; height: {mm(292,s)}; background: var(--line); }}
.step {{ position: absolute; left: {mm(30,s)}; width: {mm(360,s)}; }}
.step .dotp {{ position: absolute; left: {mm(5.2,s)}; top: {mm(3.5,s)}; width: {mm(6,s)}; height: {mm(6,s)}; border-radius: 50%; background: var(--accent); box-shadow: var(--glow); }}
.step .body {{ position: absolute; left: {mm(26,s)}; top: 0; width: {mm(330,s)}; }}
.step .ey {{ font-family: var(--font-heading); font-weight: 600; font-size: {pt(10,s)}; letter-spacing: .12em; text-transform: uppercase; color: var(--fg-3); }}
.step .name {{ font-family: var(--font-display); font-weight: 300; font-size: {pt(48,s)}; line-height: 1; margin-top: {mm(3,s)}; color: var(--fg); font-variation-settings: "opsz" 144, "SOFT" 30, "WONK" 0; }}
.step .desc {{ font-size: {pt(13,s)}; line-height: 1.5; color: var(--fg-2); margin-top: {mm(4,s)}; max-width: {mm(240,s)}; }}
.step .rec {{ font-family: var(--font-heading); font-weight: 600; font-size: {pt(13,s)}; color: var(--fg); margin-top: {mm(3,s)}; }}
.step .rec span {{ font-weight: 400; color: var(--fg-3); }}
.foot {{ position: absolute; left: {mm(30,s)}; right: {mm(30,s)}; bottom: {mm(30,s)}; display: flex; justify-content: space-between; align-items: flex-end; font-size: {pt(13,s)}; color: var(--fg-3); }}
.foot img {{ width: {mm(60,s)}; }}
"""
    steps = ""
    for i, (n, name, desc, rec) in enumerate(C.METHOD):
        steps += f"""<div class="step" style="top:{mm(236 + i*74, s)}"><span class="dotp"></span><div class="body">
      <div class="ey">Step {n}</div><div class="name">{esc(name)}</div><div class="desc">{esc(desc)}</div>
      <div class="rec"><span>You receive</span> {esc(rec)}</div></div></div>"""
    body = f"""<body><section class="sheet grain" id="art"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">Method</div>
  <h1 class="hl">A method for the monumental<span class="pt">.</span></h1>
  <p class="sub">{esc(C.METHOD_SUB)}</p>
  <div class="route"></div>
  {steps}
  <div class="foot"><span>{C.SITE} · {C.EMAIL} · {C.PHONE}</span><img src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed — Experiential Design Consultant"></div>
</div></section></body>
</html>
"""
    return head(f"Sanzeed — method poster {size.upper()}", "dark", css) + body

def typographic(size):
    w, h, s = SIZES[size]
    css = base_css(w, h, s, "light") + f"""
.mark {{ left: {mm(30,s)}; top: {mm(30,s)}; width: {mm(90,s)}; }}
.eyebrow {{ position: absolute; left: {mm(30,s)}; top: {mm(96,s)}; font-size: {pt(11,s)}; }}
.hl {{ position: absolute; left: {mm(30,s)}; top: {mm(108,s)}; width: {mm(370,s)}; font-size: {pt(118,s)}; line-height: 0.98; }}
.sub {{ position: absolute; left: {mm(30,s)}; top: {mm(222,s)}; width: {mm(300,s)}; font-size: {pt(14,s)}; line-height: 1.5; color: var(--fg-2); }}
.cols {{ position: absolute; left: {mm(30,s)}; top: {mm(252,s)}; width: {mm(360,s)}; display: grid; grid-template-columns: 1.1fr 1fr 1fr; gap: 0 {mm(10,s)}; }}
.cat {{ font-family: var(--font-heading); font-weight: 600; font-size: {pt(10.5,s)}; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); padding-bottom: {mm(2,s)}; border-bottom: 1px solid var(--line); margin-bottom: {mm(3,s)}; display: flex; justify-content: space-between; }}
.cat span {{ color: var(--fg-3); font-variant-numeric: tabular-nums; }}
.item {{ display: grid; grid-template-columns: {mm(11,s)} 1fr; font-size: {pt(9.6,s)}; line-height: 1.55; color: var(--fg-3); padding: {mm(0.6,s)} 0; border-bottom: 1px solid var(--line-2); }}
.item .c {{ font-family: var(--font-heading); font-weight: 500; font-variant-numeric: tabular-nums; color: var(--accent-text); font-size: {pt(7.5,s)}; letter-spacing: .06em; padding-top: 0.25em; }}
.item b {{ font-family: var(--font-heading); font-weight: 600; color: var(--fg); }}
.foot {{ position: absolute; left: {mm(30,s)}; right: {mm(30,s)}; bottom: {mm(30,s)}; display: flex; justify-content: space-between; align-items: flex-end; font-size: {pt(12,s)}; color: var(--fg-3); }}
.foot img {{ width: {mm(60,s)}; }}
.foot .rights {{ font-size: {pt(7,s)}; }}
"""
    cols = ""; k = 0
    for cat, n in C.CATEGORIES:
        items = [g for g in C.GALLERY if g["cat"] == cat]
        if cat == "Museums & Experience Centres":
            half = (len(items) + 1) // 2
            for part in (items[:half], items[half:]):
                rows = "".join(f'<div class="item"><span class="c">{(k:=k+1):03d}</span><span><b>{esc(g["title"])}</b> · {esc(g["place"])}</span></div>' for g in part)
                cols += f'<div><div class="cat">{esc(cat)}<span>{n}</span></div>{rows}</div>'
            continue
        rows = "".join(f'<div class="item"><span class="c">{(k:=k+1):03d}</span><span><b>{esc(g["title"])}</b> · {esc(g["place"])}</span></div>' for g in items)
        cols += f'<div><div class="cat">{esc(cat)}<span>{n}</span></div>{rows}</div>'
    css = css.replace("grid-template-columns: 1.1fr 1fr 1fr;", "grid-template-columns: 1fr 1fr 1fr 1fr;")
    body = f"""<body><section class="sheet" id="art"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-light')}" alt="Sanzeed">
  <div class="eyebrow">The galleries</div>
  <h1 class="hl">90 projects, one continuous craft<span class="pt">.</span></h1>
  <p class="sub">Every museum, show and film in one place. Museums & Experience Centres 60 · Projection Mapping & Shows 15 · Explainer Videos & Others 15.</p>
  <div class="cols">{cols}</div>
  <div class="foot"><div>{C.SITE} · {C.EMAIL} · {C.PHONE}<br><span class="rights">{esc(C.RIGHTS)}</span></div><img src="{logo('horizontal-descriptor','full-colour-light')}" alt="Sanzeed — Experiential Design Consultant"></div>
</div></section></body>
</html>
"""
    return head(f"Sanzeed — typographic poster {size.upper()}", "light", css) + body

POSTERS = {"campaign": campaign, "method": method, "typographic": typographic}

if __name__ == "__main__":
    jobs = []; pr = []
    for key, fn in POSTERS.items():
        for size, (w, h, s) in SIZES.items():
            stem = f"sanzeed-poster--{key}-{size}"
            hp = write(f"{SRC}/{stem}.html", fn(size))
            jobs.append(pdf(hp, f"{OUT}/{stem}-bleed.pdf", w + 6, h + 6))
            jobs.append(png(hp, f"{OUT}/{stem}-preview.png", math.ceil((w + 6) * PX) + 2, math.ceil((h + 6) * PX) + 2, 1.5 if size == "a2" else 2, selector="#art"))
            pr.append((f"{OUT}/{stem}-bleed.pdf", f"{OUT}/{stem}-print-ready-cmyk.pdf", f"{w}x{h}"))
    render_jobs(jobs)
    for a, b, t in pr: print_ready(a, b, t)
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"): print(f, page_sizes(f"{OUT}/{f}"))
    print("posters done", folder_size_mb(OUT), "MB")
