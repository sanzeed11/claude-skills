#!/usr/bin/env python3
"""build_flyers.py — Flyers/: A5 two-sided flyer (front key visual; back services + method + contact) and a
DL two-sided leaflet. HTML sources with @page; PDF (bleed page); print-ready CMYK with crop marks; PNG per side."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C

OUT = f"{MC}/Flyers"; SRC = f"{OUT}/src"; os.makedirs(SRC, exist_ok=True)
PX = 96 / 25.4

def frame_css(w, h):
    return f"""
@page {{ size: {w+6}mm {h+6}mm; margin: 0; }}
body {{ background: #000; }}
.sheet {{ width: {w+6}mm; height: {h+6}mm; font-family: var(--font-text); }}
.sheet.light {{ background: #F5F0E7; color: #1A1816; }}
.in {{ position: absolute; left: 3mm; top: 3mm; width: {w}mm; height: {h}mm; }}
.mark {{ position: absolute; display: block; }}
.hl {{ color: var(--fg); }}
.svc {{ display: grid; grid-template-columns: 7mm 1fr; gap: 0 1.5mm; }}
.svc .c {{ font-family: var(--font-heading); font-weight: 500; font-size: 6.5pt; letter-spacing: .08em; color: var(--accent-text); padding-top: .35mm; font-variant-numeric: tabular-nums; }}
.svc b {{ display: block; font-family: var(--font-heading); font-weight: 600; font-size: 8pt; line-height: 1.25; color: var(--fg); }}
.svc span {{ display: block; font-size: 6.8pt; line-height: 1.35; color: var(--fg-2); }}
.step b {{ display: block; font-family: var(--font-display); font-weight: 300; font-size: 13pt; line-height: 1; color: var(--fg); font-variation-settings: "opsz" 72; margin-top: 1mm; }}
.step .ey {{ font-family: var(--font-heading); font-weight: 600; font-size: 5.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); }}
.step span {{ display: block; font-size: 6.6pt; line-height: 1.35; color: var(--fg-2); margin-top: 1mm; }}
.step span i {{ font-style: normal; font-family: var(--font-heading); font-weight: 600; color: var(--fg); }}
.contact {{ font-size: 7.5pt; line-height: 1.6; color: var(--fg-2); }}
.contact b {{ font-family: var(--font-heading); font-weight: 600; color: var(--fg); }}
"""

def services_html(): return "".join(f'<div class="svc"><span class="c">{n}</span><div><b>{esc(t)}</b><span>{esc(l)}</span></div></div>' for n, t, l, _, _ in C.SERVICES)
def steps_html(short=False): return "".join(f'<div class="step"><div class="ey">Step {n}</div><b>{esc(t)}</b><span>{"" if short else esc(d) + " "}<i>You receive {esc(r)}.</i></span></div>' for n, t, d, r in C.METHOD)

def a5():
    css = frame_css(148, 210) + f"""
.front .mark {{ left: 14mm; top: 14mm; width: 32mm; }}
.front .eyebrow-quiet {{ position: absolute; left: 14mm; top: 44mm; font-size: 6.5pt; }}
.front .hl {{ position: absolute; left: 14mm; top: 50mm; width: 120mm; font-size: 34pt; line-height: 1.0; }}
.front .sub {{ position: absolute; left: 14mm; top: 92mm; width: 110mm; font-size: 8.5pt; line-height: 1.5; color: var(--fg-2); }}
.front .plate {{ position: absolute; left: 14mm; top: 112mm; width: 120mm; height: 67mm; border-radius: 5mm; }}
.front .wl {{ position: absolute; left: 14mm; top: 182mm; font-size: 7pt; }}
.front .url {{ position: absolute; right: 14mm; bottom: 14mm; font-size: 7.5pt; color: var(--fg-3); }}
.front .cta {{ position: absolute; left: 14mm; bottom: 12.5mm; font-size: 7.5pt; padding: 2.4mm 4mm; }}
.back .mark {{ left: 14mm; top: 14mm; width: 32mm; }}
.back .flow {{ position: absolute; left: 14mm; top: 26mm; width: 120mm; }}
.back .hl {{ font-size: 15pt; line-height: 1.05; margin: 1mm 0 4mm; }}
.back .eyebrow {{ font-size: 6pt; }}
.back .svcs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2.2mm 6mm; }}
.back .svc span {{ font-size: 6.2pt; }}
.back .svc b {{ font-size: 7.6pt; }}
.back .all {{ font-size: 6.8pt; color: var(--fg-2); border-top: 1px solid var(--line); padding-top: 2mm; margin-top: 3mm; }}
.back .all b {{ font-family: var(--font-display); font-weight: 300; font-size: 10pt; color: var(--fg); margin-right: 1.5mm; }}
.back .m-ey {{ margin-top: 6mm; }}
.back .steps {{ display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm 6mm; }}
.back .step span {{ font-size: 6.3pt; }}
.back .contact {{ position: absolute; left: 14mm; bottom: 13mm; width: 64mm; font-size: 6.8pt; }}   /* stops ½ cap height short of the 52 mm lockup (clear space) */
.back .lock {{ left: auto; top: auto; right: 14mm; bottom: 14mm; width: 52mm; }}   /* lockup minimum 50 mm */
"""
    front = f"""<section class="sheet grain front" id="front"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant</div>
  <h1 class="hl">Experiential design you can walk into<span class="pt">.</span></h1>
  <p class="sub">Museums, experience centres, pavilions, memorials and shows — one vision from the brief to opening night.</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <span class="cta">Tell me about the room →</span><div class="url">{C.SITE}</div>
</div></section>"""
    back = f"""<section class="sheet light back theme-light" id="back"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-light')}" alt="Sanzeed">
  <div class="flow">
  <div class="eyebrow">Seven services</div>
  <h2 class="hl opsz72">Between two points of light<span class="pt">.</span></h2>
  <div class="svcs">{services_html()}</div><div class="all"><b>All seven, every time.</b>{esc(C.ALL_SEVEN_SUB)}</div>
  <div class="eyebrow m-ey">Method</div>
  <h2 class="hl opsz72 m-hl">A method for the monumental<span class="pt">.</span></h2>
  <div class="steps">{steps_html(short=True)}</div>
  </div>
  <div class="contact"><b>Tell me about the room.</b> {C.PROMISES[0]}<br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE.replace(' ', '&nbsp;')}<br>{C.LINKEDIN} · {C.SITE} · {C.CITY.replace(' ', '&nbsp;')}</div>
  <img class="mark lock" src="{logo('horizontal-descriptor','full-colour-light')}" alt="Sanzeed — Experiential Design Consultant">
</div></section>"""
    return head("Sanzeed — A5 flyer, two sides (3 mm bleed)", "dark", css) + "<body>\n" + front + "\n" + back + "\n</body>\n</html>\n"

def dl():
    css = frame_css(99, 210) + f"""
.front .mark {{ left: 10mm; top: 12mm; width: 28mm; }}
.front .eyebrow-quiet {{ position: absolute; left: 10mm; top: 32mm; font-size: 5.5pt; }}
.front .hl {{ position: absolute; left: 10mm; top: 37mm; width: 80mm; font-size: 26pt; line-height: 1.0; }}
.front .sub {{ position: absolute; left: 10mm; top: 70mm; width: 76mm; font-size: 7.5pt; line-height: 1.5; color: var(--fg-2); }}
.front .plate {{ position: absolute; left: 10mm; top: 92mm; width: 79mm; height: 86mm; border-radius: 4mm; }}
.front .wl {{ position: absolute; left: 10mm; top: 181mm; font-size: 6.5pt; }}
.front .contact {{ position: absolute; left: 10mm; bottom: 10mm; font-size: 6.8pt; }}
.back .mark {{ left: 10mm; top: 12mm; width: 36mm; }}
.back .eyebrow {{ position: absolute; left: 10mm; top: 24mm; font-size: 5.5pt; }}
.back .hl {{ position: absolute; left: 10mm; top: 29mm; width: 80mm; font-size: 13pt; line-height: 1.05; }}
.back .svcs {{ position: absolute; left: 10mm; top: 44mm; width: 79mm; display: grid; gap: 2mm; }}
.back .svc b {{ font-size: 7.5pt; }} .back .svc span {{ font-size: 6.2pt; }}
.back .svc b {{ font-size: 7.6pt; }}
.back .m-ey {{ position: absolute; left: 10mm; top: 129mm; font-size: 5.5pt; }}
.back .m-hl {{ position: absolute; left: 10mm; top: 134mm; font-size: 13pt; }}
.back .steps {{ position: absolute; left: 10mm; top: 146mm; width: 79mm; font-size: 6.5pt; line-height: 1.5; color: var(--fg-2); }}
.back .steps div {{ display: grid; grid-template-columns: 7mm 1fr; }}
.back .steps .c {{ font-family: var(--font-heading); font-weight: 500; font-size: 6pt; letter-spacing: .08em; color: var(--accent-text); padding-top: .3mm; }}
.back .steps b {{ font-family: var(--font-heading); font-weight: 600; color: var(--fg); }}
.back .contact {{ position: absolute; left: 10mm; bottom: 10mm; width: 79mm; font-size: 6.8pt; }}
"""
    front = f"""<section class="sheet grain front" id="front"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant</div>
  <h1 class="hl">Carry the light across<span class="pt">.</span></h1>
  <p class="sub">{esc(C.BETWEEN_SUB)}</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-4x5-1600.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <div class="contact"><b>{C.SITE}</b> · {C.EMAIL} · {C.PHONE}</div>
</div></section>"""
    steps = "".join(f'<div><span class="c">{n}</span><span><b>{esc(t)}</b> — you receive {esc(r)}.</span></div>' for n, t, d, r in C.METHOD)
    back = f"""<section class="sheet light back theme-light" id="back"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-light')}" alt="Sanzeed">
  <div class="eyebrow">Seven services</div>
  <h2 class="hl opsz72">Seven ways to carry the light across<span class="pt">.</span></h2>
  <div class="svcs">{services_html()}</div>
  <div class="eyebrow m-ey">Method</div>
  <h2 class="hl opsz72 m-hl">A method for the monumental<span class="pt">.</span></h2>
  <div class="steps">{steps}</div>
  <div class="contact"><b>Tell me about the room.</b> {C.PROMISES[0]}<br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE}<br>{C.SITE} · {C.CITY}</div>
</div></section>"""
    return head("Sanzeed — DL leaflet, two sides (3 mm bleed)", "dark", css) + "<body>\n" + front + "\n" + back + "\n</body>\n</html>\n"

if __name__ == "__main__":
    jobs = []
    for stem, fn, w, h in [("sanzeed-flyer--a5-two-sided", a5, 148, 210), ("sanzeed-leaflet--dl-two-sided", dl, 99, 210)]:
        hp = write(f"{SRC}/{stem}.html", fn())
        jobs.append(pdf(hp, f"{OUT}/{stem}-bleed.pdf", w + 6, h + 6))
        for side in ("front", "back"):
            jobs.append(png(hp, f"{OUT}/{stem}-{side}.png", math.ceil((w + 6) * PX) + 2, math.ceil((h + 6) * PX) + 2, 3, selector=f"#{side}"))
    render_jobs(jobs)
    print_ready(f"{OUT}/sanzeed-flyer--a5-two-sided-bleed.pdf", f"{OUT}/sanzeed-flyer--a5-two-sided-print-ready-cmyk.pdf", "148x210")
    print_ready(f"{OUT}/sanzeed-leaflet--dl-two-sided-bleed.pdf", f"{OUT}/sanzeed-leaflet--dl-two-sided-print-ready-cmyk.pdf", "99x210")
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"): print(f, page_sizes(f"{OUT}/{f}"))
    print("flyers done", folder_size_mb(OUT), "MB")
