#!/usr/bin/env python3
"""build_events.py — Events/: invitation (A5 print, 1080x1350 digital, 600x800 email), event branding set
(backdrop, welcome board, name badge, lanyard, table tent) and exhibition graphics (roll-up, booth wall).
Scaled artwork is noted in each file name (…-1-10 = 1:10, …-1-5 = 1:5)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C

OUT = f"{MC}/Events"; SRC = f"{OUT}/src"; os.makedirs(SRC, exist_ok=True)
PX = 96 / 25.4   # css px per mm

def mm_png_job(html, out, w_mm, h_mm, scale=2, selector=None):
    return png(html, out, math.ceil(w_mm * PX) + 2, math.ceil(h_mm * PX) + 2, scale, selector=selector)

PRINT_CSS = """
@page { margin: 0; }
body { background: #000; }
.sheet { font-family: var(--font-text); }
.mark { position: absolute; display: block; }
.eyebrow-quiet { font-size: 7.5pt; }
.hl { color: var(--fg); }
.details { font-size: 9pt; line-height: 1.6; color: var(--fg-2); }
.details b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); display: inline-block; min-width: 18mm; }
.details .field { color: var(--fg); }
.wl { font-size: 7.5pt; }
"""

# ------------------------------------------------------------------ Invitation
INVITE_SUB = ("An evening with Sanzeed Mirza, Experiential Design Consultant — a walk through three rooms, "
              "the Prime Minister Museum, the Ram Katha Show and Buddha Park, and the method behind them.")
DETAILS = [("When", "[Day, date] · [Time]"), ("Where", "[Venue], [City]"), ("RSVP", "by [date] · sanzeed@gmail.com · WhatsApp +91 7827051270")]

def details_html(cls="details"):
    rows = "".join(f'<div><b>{k}</b><span class="field">{esc(v)}</span></div>' for k, v in DETAILS)
    return f'<div class="{cls}">{rows}</div>'

def invitation_print():
    css = PRINT_CSS + """
@page { size: 154mm 216mm; }
.sheet { width: 154mm; height: 216mm; }
.in { position: absolute; left: 3mm; top: 3mm; width: 148mm; height: 210mm; }
.mark { left: 15mm; top: 15mm; width: 30mm; }
.eyebrow-quiet { position: absolute; left: 15mm; top: 44mm; }
.hl { position: absolute; left: 15mm; top: 50mm; width: 120mm; font-size: 30pt; line-height: 1.02; }
.sub { position: absolute; left: 15mm; top: 86mm; width: 112mm; font-size: 9pt; line-height: 1.55; color: var(--fg-2); }
.plate { position: absolute; left: 15mm; top: 118mm; width: 118mm; height: 50mm; border-radius: 5mm; }
.wl { position: absolute; left: 15mm; top: 171mm; }
.details { position: absolute; left: 15mm; top: 180mm; width: 118mm; font-size: 8pt; }
.details b { min-width: 14mm; }
/* back */
.back .plate { top: 15mm; height: 96mm; }
.back .wl { top: 114mm; }
.back .hl { top: 128mm; font-size: 22pt; }
.back .lines { position: absolute; left: 15mm; top: 150mm; width: 118mm; font-size: 9pt; line-height: 1.7; color: var(--fg-2); }
.back .lines b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.back .mark { top: auto; bottom: 15mm; }
.back .url { position: absolute; right: 15mm; bottom: 15.5mm; font-size: 8pt; color: var(--fg-3); }
"""
    front = f"""<section class="sheet grain" id="front"><div class="in">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">An invitation</div>
  <h1 class="hl">Carry the light across<span class="pt">.</span></h1>
  <p class="sub">{esc(INVITE_SUB)}</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  {details_html()}
</div></section>"""
    back = f"""<section class="sheet grain back" id="back"><div class="in">
  <div class="plate"><img src="{jimg('case/ram-katha-show-01')}" alt="A field of lamps opens the night — Ram Katha Show, Ayodhya"></div>
  <div class="wl"><b>Ram Katha Show</b><span class="sep">·</span>Ayodhya</div>
  <h2 class="hl">Vision you can walk into<span class="pt">.</span></h2>
  <div class="lines"><b>{C.AVAILABLE}</b><br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE}<br>{C.LINKEDIN} · {C.CITY}</div>
  <img class="mark" src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed — Experiential Design Consultant" style="width:52mm">
  <div class="url">{C.SITE}</div>
</div></section>"""
    return head("Sanzeed — event invitation A5 (print, 3 mm bleed)", "dark", css) + "<body>\n" + front + "\n" + back + "\n</body>\n</html>\n"

def invitation_screen(w, h, kind):
    big = kind == "digital"
    css = f"""
.page {{ width: {w}px; height: {h}px; font-family: var(--font-text); }}
.mark {{ position: absolute; left: {72 if big else 40}px; top: {66 if big else 36}px; width: {190 if big else 120}px; }}
.eyebrow-quiet {{ position: absolute; left: {72 if big else 40}px; top: {190 if big else 110}px; font-size: {14 if big else 11}px; }}
.hl {{ position: absolute; left: {72 if big else 40}px; top: {220 if big else 130}px; width: {900 if big else 520}px; font-size: {88 if big else 52}px; color: var(--fg); }}
.sub {{ position: absolute; left: {72 if big else 40}px; top: {440 if big else 262}px; width: {860 if big else 500}px; font-size: {21 if big else 14}px; line-height: 1.5; color: var(--fg-2); }}
.plate {{ position: absolute; left: {72 if big else 40}px; top: {600 if big else 350}px; width: {936 if big else 520}px; height: {526 if big else 292}px; }}
.wl {{ position: absolute; left: {72 if big else 40}px; top: {1142 if big else 652}px; font-size: {15 if big else 12}px; }}
.details {{ position: absolute; left: {72 if big else 40}px; top: {1190 if big else 690}px; width: {936 if big else 520}px; font-size: {17 if big else 12.5}px; line-height: 1.6; color: var(--fg-2); }}
.details b {{ font-family: var(--font-heading); font-weight: 600; color: var(--fg); display: inline-block; min-width: {90 if big else 64}px; }}
.details .field {{ color: var(--fg); }}
"""
    body = f"""<body><div class="page grain">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">An invitation</div>
  <h1 class="hl">Carry the light across<span class="pt">.</span></h1>
  <p class="sub">{esc(INVITE_SUB)}</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  {details_html()}
</div></body>
</html>
"""
    return head(f"Sanzeed — event invitation ({kind} {w}x{h})", "dark", css) + body

# ------------------------------------------------------------------ Event branding set
def backdrop():   # 3000 x 2400 mm at 1:10 → 300 x 240 mm
    css = PRINT_CSS + """
@page { size: 300mm 240mm; }
.sheet { width: 300mm; height: 240mm; }
.lamp { left: 50mm; top: 10mm; width: 200mm; height: 120mm; }
.mark { left: 60mm; top: 48mm; width: 180mm; }
.beam-h { position: absolute; left: 60mm; right: 60mm; top: 92mm; }
.hl { position: absolute; left: 60mm; top: 100mm; width: 200mm; font-size: 24pt; line-height: 1.05; text-align: center; }
.mark.sm { width: 60mm; top: auto; bottom: 60mm; }
.mark.sm.l { left: 30mm; } .mark.sm.r { left: auto; right: 30mm; }
.url { position: absolute; left: 0; right: 0; bottom: 18mm; text-align: center; font-size: 9pt; color: var(--fg-3); letter-spacing: .02em; }
.scale { position: absolute; left: 10mm; bottom: 6mm; font-size: 5pt; color: var(--fg-3); }
"""
    body = f"""<body><section class="sheet grain" id="art">
  <div class="lamp"></div>
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="beam-h"></div>
  <h1 class="hl">Experiential design you can walk into<span class="pt">.</span></h1>
  <img class="mark sm l" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <img class="mark sm r" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="url">{C.SITE}</div>
  <div class="scale">Backdrop 3000 × 2400 mm · artwork at 1:10 · wordmark 1800 mm wide, centre 1700 mm from the floor · small wordmarks 600 mm at 600 mm · print on matt fabric or PVC, Gallery Black 100 K / rich black</div>
</section></body>
</html>
"""
    return head("Sanzeed — event backdrop 3000x2400 mm (1:10)", "dark", css) + body

def welcome_board():   # 900 x 1800 mm at 1:10 → 90 x 180 mm
    css = PRINT_CSS + """
@page { size: 90mm 180mm; }
.sheet { width: 90mm; height: 180mm; }
.mark { left: 9mm; top: 10mm; width: 24mm; }
.eyebrow-quiet { position: absolute; left: 9mm; top: 28mm; font-size: 5.5pt; }
.hl { position: absolute; left: 9mm; top: 33mm; width: 72mm; font-size: 30pt; }
.sub { position: absolute; left: 9mm; top: 50mm; width: 70mm; font-size: 6.5pt; line-height: 1.5; color: var(--fg-2); }
.plate { position: absolute; left: 9mm; top: 70mm; width: 72mm; height: 90mm; border-radius: 4mm; }
.wl { position: absolute; left: 9mm; top: 162mm; font-size: 5.5pt; }
.arrow { position: absolute; right: 9mm; top: 160mm; width: 8mm; height: 8mm; }
.scale { position: absolute; left: 9mm; bottom: 3mm; font-size: 3.5pt; color: var(--fg-3); }
"""
    body = f"""<body><section class="sheet grain" id="art">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">An evening with Sanzeed Mirza</div>
  <h1 class="hl">Welcome<span class="pt">.</span></h1>
  <p class="sub">{esc(C.MASTER_LINE)}<br>[Venue] · [Day, date] · [Time]</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-4x5-1600.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <img class="arrow" src="{icon('arrow-right--white')}" alt="This way">
  <div class="scale">Welcome board 900 × 1800 mm · artwork at 1:10 · headline cap height ≈ 75 mm · foam board 10 mm on an easel, or fabric on a frame</div>
</section></body>
</html>
"""
    return head("Sanzeed — welcome board 900x1800 mm (1:10)", "dark", css) + body

def name_badge():   # 90 x 60 mm, 3 mm bleed → 96 x 66
    css = PRINT_CSS + """
@page { size: 96mm 66mm; }
.sheet { width: 96mm; height: 66mm; }
.in { position: absolute; left: 3mm; top: 3mm; width: 90mm; height: 60mm; }
.sym { position: absolute; right: 7mm; top: 7mm; width: 7mm; }
.eyebrow-quiet { position: absolute; left: 7mm; top: 8mm; font-size: 5.5pt; }
.name { position: absolute; left: 7mm; top: 20mm; width: 76mm; font-size: 17pt; line-height: 1.05; color: var(--fg); }
.role { position: absolute; left: 7mm; top: 36mm; width: 76mm; font-size: 7.5pt; color: var(--fg-2); }
.mark { left: 7mm; bottom: 7mm; width: 28mm; }
.url { position: absolute; right: 7mm; bottom: 7.3mm; font-size: 6pt; color: var(--fg-3); }
"""
    def badge(id_, eyebrow, name, role):
        return f"""<section class="sheet grain" id="{id_}"><div class="in">
  <img class="sym" src="{logo('symbol','full-colour-dark')}" alt="S.">
  <div class="eyebrow-quiet">{esc(eyebrow)}</div>
  <div class="name hl">{esc(name)}</div>
  <div class="role">{esc(role)}</div>
  <img class="mark" src="{logo('simplified-small-size','full-colour-dark')}" alt="Sanzeed">
  <div class="url">{C.SITE}</div>
</div></section>"""
    body = "<body>\n" + badge("host", "Host", "Sanzeed Mirza", "Experiential Design Consultant") + "\n" + badge("guest", "Guest", "[Name]", "[Organisation]") + "\n</body>\n</html>\n"
    return head("Sanzeed — name badge 90x60 mm (print, 3 mm bleed)", "dark", css) + body

def lanyard():   # 900 x 20 mm strip, 1:1
    css = PRINT_CSS + """
@page { size: 900mm 20mm; }
.sheet { width: 900mm; height: 20mm; display: flex; align-items: center; justify-content: space-around; padding: 0 20mm; }
.sheet img { width: 56mm; display: block; }
.sheet .dot { width: 2mm; height: 2mm; }
"""
    items = []
    for i in range(10):
        items.append(f'<img src="{logo("primary-wordmark","full-colour-dark")}" alt="Sanzeed">')
        if i < 9: items.append('<span class="dot"></span>')
    body = f"""<body><section class="sheet" id="art">{''.join(items)}</section></body>\n</html>\n"""
    return head("Sanzeed — lanyard strip 900x20 mm", "dark", css) + body

def table_tent():   # A5 flat 148 x 210 → folded A6 faces 148 x 105; 3 mm bleed → 154 x 216
    css = PRINT_CSS + """
@page { size: 154mm 216mm; }
.sheet { width: 154mm; height: 216mm; }
.in { position: absolute; left: 3mm; top: 3mm; width: 148mm; height: 210mm; }
.face { position: absolute; left: 0; width: 148mm; height: 105mm; }
.face.top { top: 0; transform: rotate(180deg); }
.face.bottom { top: 105mm; }
.fold { position: absolute; left: -3mm; right: -3mm; top: 105mm; border-top: 0.2pt dashed rgba(255,255,255,.25); }
.face .mark { left: 12mm; top: 12mm; width: 30mm; }
.face .hl { position: absolute; left: 12mm; top: 30mm; width: 124mm; font-size: 24pt; }
.face .lines { position: absolute; left: 12mm; top: 62mm; width: 124mm; font-size: 8pt; line-height: 1.7; color: var(--fg-2); }
.face .lines b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.face .url { position: absolute; right: 12mm; bottom: 12mm; font-size: 7pt; color: var(--fg-3); }
.face .dot { position: absolute; left: 12mm; bottom: 12.6mm; width: 2.2mm; height: 2.2mm; }
"""
    face = f"""<img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
    <div class="hl">Tell me about the room<span class="pt">.</span></div>
    <div class="lines"><b>{C.PROMISES[0]}</b><br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE}</div>
    <span class="dot"></span><div class="url">{C.SITE}</div>"""
    body = f"""<body><section class="sheet grain" id="art"><div class="in">
  <div class="face top">{face}</div>
  <div class="fold"></div>
  <div class="face bottom">{face}</div>
</div></section></body>
</html>
"""
    return head("Sanzeed — table tent A6 (A5 flat, fold at 105 mm, 3 mm bleed)", "dark", css) + body

# ------------------------------------------------------------------ Exhibition graphics
def rollup():   # 850 x 2000 mm at 1:5 → 170 x 400 mm
    css = PRINT_CSS + """
@page { size: 170mm 400mm; }
.sheet { width: 170mm; height: 400mm; }
.mark { left: 16mm; top: 20mm; width: 60mm; }
.eyebrow-quiet { position: absolute; left: 16mm; top: 62mm; font-size: 7pt; }
.hl { position: absolute; left: 16mm; top: 70mm; width: 138mm; font-size: 44pt; }
.sub { position: absolute; left: 16mm; top: 125mm; width: 130mm; font-size: 10pt; line-height: 1.5; color: var(--fg-2); }
.plate { position: absolute; left: 16mm; top: 150mm; width: 138mm; height: 78mm; border-radius: 6mm; }
.wl { position: absolute; left: 16mm; top: 231mm; font-size: 7.5pt; }
.stats { position: absolute; left: 16mm; top: 250mm; width: 138mm; display: grid; grid-template-columns: 1fr 1fr; gap: 10mm 8mm; }
.stat .n { font-family: var(--font-display); font-weight: 300; font-size: 34pt; line-height: 1; color: var(--fg); font-variant-numeric: tabular-nums; }
.stat .n .plus { color: var(--accent); }
.stat .l { font-size: 7.5pt; color: var(--fg-2); margin-top: 2mm; }
.contact { position: absolute; left: 16mm; top: 330mm; width: 138mm; font-size: 9pt; line-height: 1.7; color: var(--fg-2); }
.contact b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.cassette { position: absolute; left: 0; right: 0; top: 360mm; border-top: 0.2pt dashed rgba(255,255,255,.25); }
.scale { position: absolute; left: 16mm; bottom: 6mm; font-size: 4.5pt; color: var(--fg-3); }
"""
    stats = "".join(f'<div class="stat"><div class="n">{n}<span class="plus">+</span></div><div class="l">{esc(l)}</div></div>' for n, l in C.PROOF)
    body = f"""<body><section class="sheet grain" id="art">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant</div>
  <h1 class="hl">Experiential design you can walk into<span class="pt">.</span></h1>
  <p class="sub">Museums, experience centres, pavilions, memorials and shows — one vision from the brief to opening night.</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-2400.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <div class="stats">{stats}</div>
  <div class="contact"><b>Tell me about the room.</b><br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE}<br>{C.SITE} · {C.CITY}</div>
  <div class="cassette"></div>
  <div class="scale">Roll-up banner 850 × 2000 mm · artwork at 1:5 · the bottom 200 mm (below the dashed line) sits in the cassette · print on blockout PVC or PET film, matt</div>
</section></body>
</html>
"""
    return head("Sanzeed — roll-up banner 850x2000 mm (1:5)", "dark", css) + body

def booth_wall():   # 2400 x 2400 mm at 1:10 → 240 x 240 mm
    css = PRINT_CSS + """
@page { size: 240mm 240mm; }
.sheet { width: 240mm; height: 240mm; }
.mark { left: 20mm; top: 20mm; width: 50mm; }
.eyebrow-quiet { position: absolute; left: 20mm; top: 84mm; font-size: 6pt; }
.hl { position: absolute; left: 20mm; top: 92mm; width: 100mm; font-size: 40pt; }
.sub { position: absolute; left: 20mm; top: 150mm; width: 92mm; font-size: 8pt; line-height: 1.55; color: var(--fg-2); }
.plate { position: absolute; left: 130mm; top: 20mm; width: 90mm; height: 112mm; border-radius: 6mm; }
.wl { position: absolute; left: 130mm; top: 136mm; font-size: 6.5pt; }
.contact { position: absolute; left: 20mm; bottom: 20mm; font-size: 7.5pt; line-height: 1.7; color: var(--fg-2); }
.contact b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.beam-h { position: absolute; left: 20mm; width: 200mm; top: 196mm; }
.url { position: absolute; right: 20mm; bottom: 20.6mm; font-size: 7.5pt; color: var(--fg-3); }
.scale { position: absolute; left: 20mm; bottom: 6mm; font-size: 4.5pt; color: var(--fg-3); }
"""
    body = f"""<body><section class="sheet grain" id="art">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant</div>
  <h1 class="hl">Carry the light across<span class="pt">.</span></h1>
  <p class="sub">{esc(C.BETWEEN_SUB)}<br><br>{esc(C.ABOUT_2)}</p>
  <div class="plate"><img src="{shared_img('hero-object--dark-4x5-1600.jpg')}" alt="The point of light"></div>
  <div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>
  <div class="beam-h end"></div>
  <div class="contact"><b>Tell me about the room.</b><br>{C.EMAIL} · {C.WHATSAPP} · {C.PHONE}</div>
  <div class="url">{C.SITE}</div>
  <div class="scale">Booth wall panel 2400 × 2400 mm · artwork at 1:10 · headline cap height ≈ 100 mm · fabric SEG or direct print on 5 mm foam PVC, matt</div>
</section></body>
</html>
"""
    return head("Sanzeed — booth wall panel 2400x2400 mm (1:10)", "dark", css) + body

if __name__ == "__main__":
    jobs = []; after = []
    # invitation
    hp = write(f"{SRC}/sanzeed-event-invitation--a5-print.html", invitation_print())
    jobs.append(pdf(hp, f"{OUT}/sanzeed-event-invitation--a5-bleed.pdf", 154, 216))
    jobs.append(mm_png_job(hp, f"{OUT}/sanzeed-event-invitation--a5-front.png", 154, 216, 2, "#front"))
    jobs.append(mm_png_job(hp, f"{OUT}/sanzeed-event-invitation--a5-back.png", 154, 216, 2, "#back"))
    hp = write(f"{SRC}/sanzeed-event-invitation--digital-1080x1350.html", invitation_screen(1080, 1350, "digital"))
    jobs.append(png(hp, f"{OUT}/sanzeed-event-invitation--digital-2160x2700.png", 1080, 1350, 2)); after.append((f"{OUT}/sanzeed-event-invitation--digital-2160x2700.png", f"{OUT}/sanzeed-event-invitation--digital-1080x1350.jpg", 1080))
    hp = write(f"{SRC}/sanzeed-event-invitation--email-600x800.html", invitation_screen(600, 800, "email"))
    jobs.append(png(hp, f"{OUT}/sanzeed-event-invitation--email-1200x1600.png", 600, 800, 2)); after.append((f"{OUT}/sanzeed-event-invitation--email-1200x1600.png", f"{OUT}/sanzeed-event-invitation--email-600x800.jpg", 600))
    # branding set
    for stem, fn, w, h, sc in [("sanzeed-event-backdrop--3000x2400mm-1-10", backdrop, 300, 240, 3),
                               ("sanzeed-event-welcome-board--900x1800mm-1-10", welcome_board, 90, 180, 4),
                               ("sanzeed-event-lanyard--900x20mm", lanyard, 900, 20, 2),
                               ("sanzeed-exhibition-rollup--850x2000mm-1-5", rollup, 170, 400, 3),
                               ("sanzeed-exhibition-booth-wall--2400x2400mm-1-10", booth_wall, 240, 240, 3)]:
        hp = write(f"{SRC}/{stem}.html", fn())
        jobs.append(pdf(hp, f"{OUT}/{stem}.pdf", w, h)); jobs.append(mm_png_job(hp, f"{OUT}/{stem}.png", w, h, sc, "#art"))
    hp = write(f"{SRC}/sanzeed-event-name-badge--90x60mm-print.html", name_badge())
    jobs.append(pdf(hp, f"{OUT}/sanzeed-event-name-badge--90x60mm-bleed.pdf", 96, 66))
    jobs.append(mm_png_job(hp, f"{OUT}/sanzeed-event-name-badge--host.png", 96, 66, 4, "#host"))
    jobs.append(mm_png_job(hp, f"{OUT}/sanzeed-event-name-badge--guest.png", 96, 66, 4, "#guest"))
    hp = write(f"{SRC}/sanzeed-event-table-tent--a6-print.html", table_tent())
    jobs.append(pdf(hp, f"{OUT}/sanzeed-event-table-tent--a6-bleed.pdf", 154, 216))
    jobs.append(mm_png_job(hp, f"{OUT}/sanzeed-event-table-tent--a6-flat.png", 154, 216, 2, "#art"))
    render_jobs(jobs)
    for p, j, w in after: to_jpg(p, j, 88, width=w)
    print_ready(f"{OUT}/sanzeed-event-invitation--a5-bleed.pdf", f"{OUT}/sanzeed-event-invitation--a5-print-ready-cmyk.pdf", "148x210")
    print_ready(f"{OUT}/sanzeed-event-name-badge--90x60mm-bleed.pdf", f"{OUT}/sanzeed-event-name-badge--90x60mm-print-ready-cmyk.pdf", "90x60")
    print_ready(f"{OUT}/sanzeed-event-table-tent--a6-bleed.pdf", f"{OUT}/sanzeed-event-table-tent--a6-print-ready-cmyk.pdf", "148x210")
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"): print(f, page_sizes(f"{OUT}/{f}"))
    print("events done", folder_size_mb(OUT), "MB")
