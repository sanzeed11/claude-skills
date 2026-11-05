#!/usr/bin/env python3
"""
build_decorative.py — editable master for Decorative_Elements/ (SVG + PNG).

  python3 build_decorative.py          # writes svg/<group>/ and png/<group>/ for every element

Units are CSS pixels at 1x. PNGs are exported at 2x (4x for the small elements: counters, eyebrows, arrows)
with a transparent background — cairosvg for pure graphics, Chromium (kit render.js) for the templates that
keep live <text> so the fonts are rendered properly. Eyebrow lockups, counter numerals and the 'lit.' glyph
are OUTLINED from the brand fonts with fontTools (they are stamps, not templates); the wall-label template
and the room frames keep live text so they can be edited in any vector app.
Inks: dark = Gallery White / Lamp Gold on transparent (for black); light = Soot / Old Gold / Gold Ink (for Plaster).
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '_build')); import szlib as sz
f = sz.f
ITEMS = []   # (group, stem, w, h, body, title, desc, scale)

def add(group, stem, w, h, body, title, desc, scale=2):
    ITEMS.append((group, stem, w, h, body, title, desc, scale))

def hair(c): return f'stroke="{c["line"]}" stroke-opacity="{c["line_op"]}"'
def glow(c, cx, cy, r=18, gid='glow'):
    return (f'<radialGradient id="{gid}" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{c["gold"]}" stop-opacity="0.55"/><stop offset="1" stop-color="{c["gold"]}" stop-opacity="0"/></radialGradient>',
            f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="url(#{gid})"/>')

for ink in ('dark', 'light'):
    c = sz.INK[ink]; on = 'for Gallery Black / Night / Charcoal' if ink == 'dark' else 'for Plaster / Paper / Stone'
    # ------------------------------------------------------------------ dividers
    for L in (480, 960, 1440):
        gdef, gcirc = glow(c, 12, 12) if ink == 'dark' else ('', '')
        body = (f'<defs>{gdef}</defs>{gcirc}<line id="beam" x1="12" y1="12" x2="{L-4}" y2="12" {hair(c)} stroke-width="1" shape-rendering="crispEdges"/>'
                f'<circle id="point" cx="12" cy="12" r="4.5" fill="{c["gold"]}"/>')
        add('dividers', f'sanzeed-divider-beam-point--{L}--{ink}', L, 24, body, f'Beam with point · {L} px', f'The beam (1 px hairline at 10 %) with the point of light at its start, {on}. Matches brand.css .beam.')
        add('dividers', f'sanzeed-divider-hairline--{L}--{ink}', L, 8, f'<line x1="0" y1="4" x2="{L}" y2="4" {hair(c)} stroke-width="1" shape-rendering="crispEdges"/>', f'Hairline · {L} px', f'Plain 1 px hairline at 10 % {on}.')
    gdef, gcirc = glow(c, 480, 12) if ink == 'dark' else ('', '')
    add('dividers', f'sanzeed-divider-beam-centre-point--960--{ink}', 960, 24, f'<defs>{gdef}</defs>{gcirc}<line x1="4" y1="12" x2="956" y2="12" {hair(c)} stroke-width="1" shape-rendering="crispEdges"/><circle cx="480" cy="12" r="4.5" fill="{c["gold"]}"/>', 'Beam with centre point · 960 px', f'Beam with the point at the centre, {on}.')
    add('dividers', f'sanzeed-divider-hairline-dotted--960--{ink}', 960, 8, f'<line x1="4" y1="4" x2="956" y2="4" stroke="{c["ink"]}" stroke-opacity="0.35" stroke-width="2" stroke-linecap="round" stroke-dasharray="0 8"/>', 'Dotted hairline (route) · 960 px', f'A route-style dotted rule, {on}.')
    add('dividers', f'sanzeed-divider-short-rule--48--{ink}', 48, 8, f'<line x1="0" y1="4" x2="48" y2="4" stroke="{c["gold"]}" stroke-width="1"/>', 'Short gold rule · 48 px', f'A 48 px gold rule for section openers, {on}.')
    # ------------------------------------------------------------------ corner marks
    for name, W, H in (('640x400', 640, 400),):
        leg = 36; s = f'stroke="{c["ink"]}" stroke-opacity="0.6" stroke-width="1.5" stroke-linecap="round" fill="none"'
        corners = (f'<path id="corner-tl" d="M0 {leg} V0 H{leg}" {s}/><path id="corner-tr" d="M{W-leg} 0 H{W} V{leg}" {s}/>'
                   f'<path id="corner-bl" d="M0 {H-leg} V{H} H{leg}" {s}/><path id="corner-br" d="M{W-leg} {H} H{W} V{H-leg}" {s}/>')
        add('corner-marks', f'sanzeed-corner-marks--set-{name}--{ink}', W, H, corners, 'Corner marks · set', f'Four corner marks framing a {W}x{H} area; move the four paths to any size. {on}.')
        add('corner-marks', f'sanzeed-corner-marks--set-with-point-{name}--{ink}', W, H, corners + f'<circle cx="18" cy="18" r="4" fill="{c["gold"]}"/>', 'Corner marks with point · set', f'The set with the point of light inside the top-left corner, {on}.')
    add('corner-marks', f'sanzeed-corner-mark--single--{ink}', 40, 40, f'<path d="M2 38 V2 H38" stroke="{c["ink"]}" stroke-opacity="0.6" stroke-width="1.5" stroke-linecap="round" fill="none"/>', 'Corner mark · single', f'One corner mark (top-left); rotate for the others. {on}.')
    # ------------------------------------------------------------------ eyebrow lockups (outlined)
    for text in ('Now showing', 'Method', 'About', 'Journey', 'Get in touch', 'Services', 'The walk', 'Case study', 'Step 01'):
        d, adv, m = sz.text_path(text.upper(), 'Inter Tight', 600, 32, tracking=0.12, x=0, y=32)
        w = math.ceil(adv) + 2
        add('eyebrows', f'sanzeed-eyebrow--{text.lower().replace(" ", "-")}--{ink}', w, 44, f'<path d="{d}" fill="{c["gold_text"]}"/>', f'Eyebrow · {text.upper()}', f'Letter-spaced caps eyebrow, Inter Tight 600, +0.12 em, outlined. Gold text {"(Lamp Gold)" if ink=="dark" else "(Gold Ink #8A6124, the only gold allowed as text on light)"}; {on}. In UI the eyebrow is 12 px.')
    d, adv, m = sz.text_path('NOW SHOWING', 'Inter Tight', 600, 32, tracking=0.12, x=72, y=32)
    add('eyebrows', f'sanzeed-eyebrow--now-showing-with-beam--{ink}', math.ceil(adv) + 76, 44, f'<line x1="0" y1="21" x2="52" y2="21" stroke="{c["line"]}" stroke-opacity="0.35" stroke-width="1"/><circle cx="52" cy="21" r="4" fill="{c["gold"]}"/><path d="{d}" fill="{c["gold_text"]}"/>', 'Eyebrow · NOW SHOWING with beam', f'The eyebrow preceded by a short beam and the point, {on}.')
    # ------------------------------------------------------------------ counter badges (outlined numerals)
    for n in range(1, 11):
        num = f'{n:03d}'
        d, adv, m = sz.text_path(num, 'Inter Tight', 500, 13, tracking=0.08, tnum=True, x=34, y=18.6, anchor='middle')
        body = (f'<rect x="0.5" y="0.5" width="67" height="27" rx="13.5" fill="none" stroke="{c["ink"]}" stroke-opacity="0.25" stroke-width="1"/>'
                f'<path d="{d}" fill="{c["gold_text"]}"/>')
        add('counters', f'sanzeed-counter-badge--{num}--{ink}', 68, 28, body, f'Counter badge · {num}', f'Three-digit counter in a hairline pill, Inter Tight 500, +0.08 em, tabular, outlined; {on}.', scale=4)
    # one strip with all ten
    strip = ''.join(f'<g transform="translate({i*84} 0)"><rect x="0.5" y="0.5" width="67" height="27" rx="13.5" fill="none" stroke="{c["ink"]}" stroke-opacity="0.25" stroke-width="1"/><path d="{sz.text_path(f"{i+1:03d}", "Inter Tight", 500, 13, tracking=0.08, tnum=True, x=34, y=18.6, anchor="middle")[0]}" fill="{c["gold_text"]}"/></g>' for i in range(10))
    add('counters', f'sanzeed-counter-badges--001-010--{ink}', 10*84-16, 28, strip, 'Counter badges · 001–010', f'All ten badges in one strip, {on}.', scale=4)
    # ------------------------------------------------------------------ arrows
    s = f'fill="none" stroke="{c["ink"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
    arrows = {
        'right-long': (64, 24, f'<path d="M4 12h56M53 5l7 7-7 7" {s}/>'),
        'left-long':  (64, 24, f'<path d="M60 12H4M11 5l-7 7 7 7" {s}/>'),
        'up-long':    (24, 64, f'<path d="M12 60V4M5 11l7-7 7 7" {s}/>'),
        'down-long':  (24, 64, f'<path d="M12 4v56M5 53l7 7 7-7" {s}/>'),
        'diagonal':   (32, 32, f'<path d="M6 26L26 6M10 6h16v16" {s}/>'),
        'right-with-point': (80, 24, f'<circle cx="8" cy="12" r="3.5" fill="{c["gold"]}"/><path d="M16 12h60M69 5l7 7-7 7" {s}/>'),
        'cta':        (24, 24, f'<path d="M5 12h14M13 6l6 6-6 6" {s}/>'),
    }
    for name, (w, h, body) in arrows.items():
        add('arrows', f'sanzeed-arrow--{name}--{ink}', w, h, body, f'Arrow · {name}', f'1.5 px round-capped arrow, {on}. The with-point version is the point travelling the beam.', scale=4)
    # ------------------------------------------------------------------ the 'lit.' full stop glyph (Fraunces 300)
    size = 160
    dlit, adv_lit, m = sz.text_path('lit', 'Fraunces', 300, size, opsz=144, tracking=-0.015, x=0, y=size*0.8)
    # measure Fraunces' own period so the point sits where the full stop would
    font = sz._font('Fraunces', 300, 144, False); gs = font.getGlyphSet(); per = font.getBestCmap()[ord('.')]
    from fontTools.pens.boundsPen import BoundsPen
    bp = BoundsPen(gs); gs[per].draw(bp); x0, y0, x1, y1 = bp.bounds; upm = font['head'].unitsPerEm; k = size/upm
    pr = (x1 - x0) * k / 2 * 1.08; pcx = adv_lit + (x0 + x1)/2 * k; pcy = size*0.8 - (y0 + y1)/2 * k
    add('lit-glyph', f'sanzeed-glyph-lit-fullstop--{ink}', math.ceil(pr*2 + 4), math.ceil(pr*2 + 4), f'<circle cx="{f(pr+2)}" cy="{f(pr+2)}" r="{f(pr)}" fill="{c["gold"]}"/>', "The 'lit.' full stop", f'The gold point sized to the Fraunces 300 full stop at {size} px (r = {f(pr)} px, i.e. {f(pr/size*100)} % of the font size). Scale with the type. {on}.', scale=4)
    add('lit-glyph', f'sanzeed-lockup-lit--{ink}', math.ceil(pcx + pr + 8), math.ceil(size*1.05), f'<path d="{dlit}" fill="{c["ink"]}"/><circle cx="{f(pcx)}" cy="{f(pcy)}" r="{f(pr)}" fill="{c["gold"]}"/>', "'lit.' lockup", f"'lit' in Fraunces 300 (opsz 144, outlined) with the gold point as its full stop, {on}.")
    dh, adv_h, m = sz.text_path('Eight rooms, lit', 'Fraunces', 300, size, opsz=144, tracking=-0.015, x=0, y=size*0.8)
    pcx2 = adv_h + (x0 + x1)/2 * k
    add('lit-glyph', f'sanzeed-lockup-eight-rooms-lit--{ink}', math.ceil(pcx2 + pr + 8), math.ceil(size*1.05), f'<path d="{dh}" fill="{c["ink"]}"/><circle cx="{f(pcx2)}" cy="{f(pcy)}" r="{f(pr)}" fill="{c["gold"]}"/>', "'Eight rooms, lit.' headline lockup", f'The headline from sanzeed.com with the point as its full stop (the last word may be gold instead — never both), {on}.')
    # ------------------------------------------------------------------ visitor's book rule block
    W, H = 720, 400
    body = (f'<defs><linearGradient id="book-rule" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["gold"]}"/><stop offset="0.5" stop-color="{c["gold2"]}"/><stop offset="1" stop-color="{c["gold2"]}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect id="rule" x="0" y="0" width="2" height="{H}" fill="url(#book-rule)"/>'
            f'<circle id="point" cx="1" cy="10" r="4.5" fill="{c["gold"]}"/>'
            + ''.join(f'<line x1="40" y1="{64 + i*48}" x2="{W}" y2="{64 + i*48}" {hair(c)} stroke-width="1" shape-rendering="crispEdges"/>' for i in range(7)))
    add('visitors-book', f'sanzeed-visitors-book-rule-block--{ink}', W, H, body, "Visitor's book rule block", f"The site's book-rule (a 2 px gold rule fading downward, the point at its head) with seven writing hairlines; {on}. For forms, guest-book pages, quote blocks.")
    # ------------------------------------------------------------------ wall-label template (live text)
    tcol, pcol, lcol = c['ink'], c['ink3'], c['ink2']
    def wall_label(title, place, line):
        return (f'<g id="wall-label" font-family="Inter Tight, Inter, sans-serif">'
                f'<line x1="0" y1="0.5" x2="480" y2="0.5" {hair(c)} stroke-width="1" shape-rendering="crispEdges"/>'
                f'<text id="title" x="0" y="34" font-family="Inter Tight" font-weight="600" font-size="20" letter-spacing="-0.2" fill="{tcol}">{title}</text>'
                f'<text id="place" x="0" y="58" font-family="Inter" font-weight="400" font-size="15" fill="{pcol}">{place}</text>'
                f'<text id="line" x="0" y="84" font-family="Inter" font-weight="400" font-size="15" fill="{lcol}">{line}</text></g>')
    add('wall-label', f'sanzeed-wall-label-template--{ink}', 480, 100, wall_label('[Project title]', '[Place]', '[One line about the room.]'), 'Wall label · template', f'Caption block: Title (Inter Tight 600, 20) · Place (Inter 400, 15, fg-3) · one line (Inter 400, 15, fg-2) under a hairline. Live text — edit the three <text> elements. {on}.')
    add('wall-label', f'sanzeed-wall-label-example--{ink}', 480, 100, wall_label('Prime Minister Museum', 'New Delhi', 'A corridor you walk in order.'), 'Wall label · example', f'The template filled with confirmed copy from sanzeed.com, {on}.')
    # ------------------------------------------------------------------ room frames (live text label slot)
    for ratio, W, H in (('16x9', 1600, 900), ('4x5', 1080, 1350), ('1x1', 1080, 1080), ('9x16', 1080, 1920)):
        rad = 28; lab_y = H - 120
        body = (f'<defs><clipPath id="room-clip"><rect x="0" y="0" width="{W}" height="{H}" rx="{rad}"/></clipPath>'
                f'<linearGradient id="veil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.72"/></linearGradient></defs>'
                f'<g clip-path="url(#room-clip)">'
                f'<rect id="room" width="{W}" height="{H}" fill="{c["card"]}"/>'
                f'<rect id="image-placeholder" x="0" y="0" width="{W}" height="{H}" fill="{c["card2"]}"><title>IMAGE PLACEHOLDER — replace with a project image cropped to {ratio.replace("x", ":")}</title></rect>'
                f'<rect id="veil" x="0" y="{f(H*0.45)}" width="{W}" height="{f(H*0.55)}" fill="url(#veil)"/></g>'
                f'<rect id="hairline" x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{rad}" fill="none" {hair(c)} stroke-width="1"/>'
                f'<g id="wall-label" transform="translate(48 {lab_y})">'
                f'<text x="0" y="24" font-family="Inter Tight" font-weight="600" font-size="22" fill="#F5F5F7">[Project title]</text>'
                f'<text x="0" y="50" font-family="Inter" font-weight="400" font-size="16" fill="#A1A1A6">[Place]</text></g>')
        add('frames', f'sanzeed-frame-room--{ratio}--{ink}', W, H, body, f'Room frame · {ratio.replace("x", ":")}', f'The room (radius {rad}, hairline border, {"Charcoal" if ink=="dark" else "Paper"} fill) with a clearly named <rect id="image-placeholder"> under the veil and a wall-label slot (live text, white over the veil). {on}.', scale=1)

def main():
    for group, stem, w, h, body, title, desc, scale in ITEMS:
        svgp = sz.write(HERE / 'svg' / group / f'{stem}.svg', sz.svg(w, h, body, f'Sanzeed — {title}', desc + ' Generated by Decorative_Elements/build_decorative.py.'))
        png = HERE / 'png' / group / f'{stem}.png'; png.parent.mkdir(parents=True, exist_ok=True)
        if '<text' in body:
            sz.render_html(svgp, png, w, h, scale=scale, transparent=True)
        else:
            sz.svg_to_png(svgp, png, int(round(w*scale)), int(round(h*scale)))
        print(stem, f'{w}x{h} @{scale}x')
    print(len(ITEMS), 'elements')

if __name__ == '__main__': main()
