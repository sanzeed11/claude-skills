#!/usr/bin/env python3
"""
build_illustrations.py — editable master for every vector illustration in Illustrations/.

  python3 build_illustrations.py              # writes svg/, then png/ (2000 w, transparent) and pdf/ via export_svg.py

Drawing language = the brand's monoline language: one even stroke (W = 64 on the drawing grid), round caps and joins,
and 45-unit gold "points of light" (r = 0.7 x stroke). Secondary lines (beams, hairlines) are 20 units.
Two inks: dark (Gallery White / Silver / Lamp Gold, for black) and light (Soot / Umber / Old Gold, for Plaster).
All labels are outlined from the brand fonts with fontTools (szlib.text_path), so nothing depends on
installed fonts. Change a number here, re-run, and every export is regenerated.
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '_build')); import szlib as sz
f = sz.f
W, HAIR, R = 64, 20, 45           # stroke, hairline, point radius

def pal(ink):
    c = sz.INK[ink]
    return dict(ink=c['ink'], ink2=c['ink2'], ink3=c['ink3'], gold=c['gold'], gold_text=c['gold_text'], card=c['card'])

def stroke(colour, w=W, extra=''):
    return f'fill="none" stroke="{colour}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"{extra}'

def point(x, y, colour, r=R): return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{colour}"/>'

def label(text, x, y, colour, family='Inter Tight', wght=600, size=28, tracking=0.12, anchor='middle', italic=False, opsz=None, tnum=False, upper=True):
    t = text.upper() if (upper and family == 'Inter Tight' and wght == 600 and tracking > 0) else text
    d, adv, m = sz.text_path(t, family, wght, size, opsz, italic, tracking=tracking, tnum=tnum, x=x, y=y, anchor=anchor)
    return f'<path d="{d}" fill="{colour}"/>'

ILLUS = {}

# ----------------------------------------------------------------------------- orbit object
def orbit(ink):
    c = pal(ink); cw, ch = 2000, 1480
    cx, cy, sr = 1000, 640, 360                     # sphere
    rx, ry, rot = 700, 200, -16                     # ring
    out = ['<defs>',
           f'<mask id="behind-sphere" maskUnits="userSpaceOnUse" x="0" y="0" width="{cw}" height="{ch}"><rect width="{cw}" height="{ch}" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{sr + W/2 + 6}" fill="#000"/></mask>',
           '</defs>']
    # plinth
    px, py, prx, pry, ph = 1000, 1190, 520, 120, 96
    out.append(f'<g id="plinth" {stroke(c["ink"])}>'
               f'<ellipse cx="{px}" cy="{py}" rx="{prx}" ry="{pry}"/>'
               f'<path d="M{px-prx} {py} v{ph} A{prx} {pry} 0 0 0 {px+prx} {py+ph} v{-ph}"/></g>')
    out.append(f'<g id="pool-of-light" {stroke(c["ink2"], HAIR)} stroke-opacity="0.7"><ellipse cx="{px}" cy="{py}" rx="300" ry="68"/></g>')
    # ring: back half (masked where it passes behind the sphere) then sphere, then front half
    ring_back  = f'<g mask="url(#behind-sphere)"><path d="M{-rx} 0 A{rx} {ry} 0 0 1 {rx} 0" transform="translate({cx} {cy}) rotate({rot})" {stroke(c["gold"])}/></g>'
    ring_front = f'<path d="M{-rx} 0 A{rx} {ry} 0 0 0 {rx} 0" transform="translate({cx} {cy}) rotate({rot})" {stroke(c["gold"])}/>'
    out.append(f'<g id="ring-back">{ring_back}</g>')
    out.append(f'<g id="sphere" {stroke(c["ink"])}><circle cx="{cx}" cy="{cy}" r="{sr}"/></g>')
    out.append(f'<g id="sphere-highlight" {stroke(c["ink2"], HAIR)}><path d="M{cx-250} {cy-150} A290 290 0 0 1 {cx-110} {cy-268}"/></g>')
    out.append(f'<g id="ring-front">{ring_front}</g>')
    # glass beads (particles) and the one point of light
    beads = [(300, 430, 30), (1730, 560, 24), (420, 980, 20), (1660, 1000, 28), (1290, 150, 22), (560, 170, 18)]
    out.append(f'<g id="beads" {stroke(c["ink2"], HAIR)}>' + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in beads) + '</g>')
    out.append(f'<g id="point-of-light">{point(cx-118, cy-120, c["gold"])}</g>')
    return cw, ch, '\n'.join(out), 'The orbit object — a flat monoline reading of the site hero: a glass sphere inside a gold ring on a plinth, with glass beads.'
ILLUS['orbit-object'] = orbit

# ----------------------------------------------------------------------------- method diagram
STEPS = [('01', 'Discover', ('a research deck', '+ the one central story')),
         ('02', 'Direct',   ('a concept book', '+ a walkthrough film')),
         ('03', 'Craft',    ('detail drawings, media scripts', '+ a prototype room')),
         ('04', 'Deliver',  ('a built, tested', 'and opened experience'))]
def method(ink):
    c = pal(ink); cw, ch = 2400, 760; y = 330
    xs = [330, 910, 1490, 2070]
    out = [f'<g id="beam" {stroke(c["ink"], 6)} stroke-opacity="0.35"><line x1="120" y1="{y}" x2="2280" y2="{y}"/></g>']
    out.append(f'<g id="direction" {stroke(c["ink"], 6)} stroke-opacity="0.35"><path d="M2246 {y-28} l34 28 -34 28"/></g>')
    out.append('<g id="points">' + ''.join(point(x, y, c['gold'], 34) for x in xs) + '</g>')
    out.append(f'<g id="travelling-point">{point(xs[0] + 290, y, c["gold"], 14)}</g>')
    for (n, name, deliver), x in zip(STEPS, xs):
        out.append(f'<g id="step-{n}">')
        out.append(label(f'STEP {n}', x, y - 96, c['gold_text'], size=30, tracking=0.12))
        out.append(label(name, x, y + 150, c['ink'], family='Fraunces', wght=300, size=96, tracking=-0.015, opsz=144))
        out.append(label('You receive', x, y + 216, c['ink3'], family='Inter', wght=400, size=28, tracking=0, upper=False))
        out.append(label(deliver[0], x, y + 262, c['ink2'], family='Inter', wght=400, size=30, tracking=0, upper=False))
        out.append(label(deliver[1], x, y + 304, c['ink2'], family='Inter', wght=400, size=30, tracking=0, upper=False))
        out.append('</g>')
    return cw, ch, '\n'.join(out), 'Method diagram — Discover, Direct, Craft, Deliver as four points of light on one beam, with the deliverable under each.'
ILLUS['method-diagram'] = method

# ----------------------------------------------------------------------------- between two points of light
def two_points(ink):
    c = pal(ink); cw, ch = 2400, 1200
    L, Rr = (300, 790), (2100, 430)
    out = []
    # six faint routes (the other services) + the lit line
    faint = []
    for k, (c1, c2) in enumerate([((700, 300), (1700, 300)), ((800, 1050), (1600, 980)), ((600, 560), (1900, 900)),
                                  ((1000, 150), (1300, 1080)), ((500, 980), (1900, 240)), ((900, 700), (1500, 520))]):
        faint.append(f'<path d="M{L[0]} {L[1]} C{c1[0]} {c1[1]} {c2[0]} {c2[1]} {Rr[0]} {Rr[1]}"/>')
    out.append(f'<g id="seven-ways-faint" {stroke(c["ink"], 10)} stroke-opacity="0.18">{"".join(faint)}</g>')
    out.append(f'<g id="the-line" {stroke(c["ink"], 24)}><path d="M{L[0]} {L[1]} C800 790 1600 430 {Rr[0]} {Rr[1]}"/></g>')
    out.append(f'<g id="points">{point(*L, c["gold"], 52)}{point(*Rr, c["gold"], 52)}</g>')
    # the travelling pen (a smaller point on the line, 62 % along)
    t = .62; u = 1 - t
    px = u**3*L[0] + 3*u*u*t*800 + 3*u*t*t*1600 + t**3*Rr[0]; py = u**3*L[1] + 3*u*u*t*790 + 3*u*t*t*430 + t**3*Rr[1]
    out.append(f'<g id="travelling-point">{point(px, py, c["gold"], 18)}</g>')
    out.append('<g id="labels">' + label('The brief', L[0], L[1] + 150, c['gold_text'], size=34) + label('The visitor', Rr[0], Rr[1] - 110, c['gold_text'], size=34) + '</g>')
    out.append('<g id="caption">' + label('Seven ways to carry the light across.', 1200, 1120, c['ink2'], family='Inter', wght=400, size=34, tracking=0, upper=False) + '</g>')
    return cw, ch, '\n'.join(out), 'Between two points of light — the brief on the left, the visitor on the right, one line of light drawn between them (six fainter ways behind it).'
ILLUS['between-two-points'] = two_points

# ----------------------------------------------------------------------------- museum route diagram
def route_plan(ink):
    c = pal(ink); cw, ch = 2400, 1560
    rw, rh, gap, rad = 440, 560, 80, 28
    x0, y0 = 200, 120
    rooms = {}
    for i in range(4):  rooms[f'00{i+1}'] = (x0 + i*(rw+gap), y0)
    for i in range(4):  rooms[f'00{i+5}'] = (x0 + (3-i)*(rw+gap), y0 + rh + gap)
    door = 150
    def wall(x, y, doors):
        """rounded room outline with gaps for doors ('L','R','T','B')"""
        cy_, cx_ = y + rh/2, x + rw/2; d = door/2; p = []
        # top edge (left corner -> right corner)
        p.append(f'M{x+rad} {y}')
        if 'T' in doors: p.append(f'H{cx_-d} M{cx_+d} {y}')
        p.append(f'H{x+rw-rad} A{rad} {rad} 0 0 1 {x+rw} {y+rad}')
        if 'R' in doors: p.append(f'V{cy_-d} M{x+rw} {cy_+d}')
        p.append(f'V{y+rh-rad} A{rad} {rad} 0 0 1 {x+rw-rad} {y+rh}')
        if 'B' in doors: p.append(f'H{cx_+d} M{cx_-d} {y+rh}')
        p.append(f'H{x+rad} A{rad} {rad} 0 0 1 {x} {y+rh-rad}')
        if 'L' in doors: p.append(f'V{cy_+d} M{x} {cy_-d}')
        p.append(f'V{y+rad} A{rad} {rad} 0 0 1 {x+rad} {y}')
        return ' '.join(p)
    doors = {'001': 'LR', '002': 'LR', '003': 'LR', '004': 'LB', '005': 'TL', '006': 'RL', '007': 'RL', '008': 'RL'}
    out = [f'<g id="rooms" {stroke(c["ink"], 16)} stroke-opacity="0.6">' + ''.join(f'<path id="room-{n}" d="{wall(x, y, doors[n])}"/>' for n, (x, y) in rooms.items()) + '</g>']
    centres = {n: (x + rw/2, y + rh/2) for n, (x, y) in rooms.items()}
    pts = [(x0 - 120, centres['001'][1])] + [centres[n] for n in ['001','002','003','004','005','006','007','008']] + [(x0 - 120, centres['008'][1])]
    out.append(f'<g id="route" {stroke(c["ink2"], 16)} stroke-dasharray="0 44"><path d="M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts) + '"/></g>')
    out.append('<g id="exhibits">' + ''.join(point(x, y, c['gold'], 26) for x, y in centres.values()) + '</g>')
    out.append('<g id="counters">' + ''.join(label(n, x + 44, y + 76, c['gold_text'], wght=500, size=34, tracking=0.08, tnum=True, anchor='start') for n, (x, y) in rooms.items()) + '</g>')
    out.append('<g id="entry-exit">' + label('Entry', x0 - 120, centres['001'][1] - 60, c['ink2'], family='Inter', wght=400, size=30, tracking=0, upper=False)
               + label('Exit', x0 - 120, centres['008'][1] + 86, c['ink2'], family='Inter', wght=400, size=30, tracking=0, upper=False)
               + f'<g {stroke(c["ink2"], 12)}><path d="M{x0-170} {centres["001"][1]} h60 m-24 -24 l24 24 -24 24"/><path d="M{x0-110} {centres["008"][1]} h-60 m24 -24 l-24 24 24 24"/></g></g>')
    out.append('<g id="caption">' + label('Galleries planned as a route, not a floor plan.', 1200, 1480, c['ink2'], family='Inter', wght=400, size=34, tracking=0, upper=False) + '</g>')
    return cw, ch, '\n'.join(out), 'Museum route diagram — eight numbered rooms in plan, one dotted route through them, a point of light in each.'
ILLUS['museum-route'] = route_plan

# ----------------------------------------------------------------------------- lamp
def lamp(ink):
    c = pal(ink); cw, ch = 1600, 2000
    cx = 800; top = 60; shade_y = 760; sw, sh = 520, 280
    out = ['<defs>',
           f'<radialGradient id="lamp-glow" cx="{cx}" cy="{shade_y + 130}" r="620" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{c["gold"]}" stop-opacity="0.45"/><stop offset="0.35" stop-color="{c["gold"]}" stop-opacity="0.12"/><stop offset="1" stop-color="{c["gold"]}" stop-opacity="0"/></radialGradient>',
           '</defs>',
           f'<g id="glow"><circle cx="{cx}" cy="{shade_y + 130}" r="620" fill="url(#lamp-glow)"/></g>',
           f'<g id="cord" {stroke(c["ink"])}><line x1="{cx}" y1="{top}" x2="{cx}" y2="{shade_y - sh}"/></g>',
           # the shade is the N/M arch, open downward
           f'<g id="shade" {stroke(c["ink"])}><path d="M{cx-sw/2} {shade_y} V{shade_y - sh + sw/2} A{sw/2} {sw/2} 0 0 1 {cx+sw/2} {shade_y - sh + sw/2} V{shade_y}"/></g>',
           f'<g id="cone" {stroke(c["ink2"], HAIR)} stroke-opacity="0.6"><path d="M{cx-sw/2} {shade_y} L{cx-700} {1760}"/><path d="M{cx+sw/2} {shade_y} L{cx+700} {1760}"/></g>',
           f'<g id="pool" {stroke(c["ink2"], HAIR)} stroke-opacity="0.6"><ellipse cx="{cx}" cy="1760" rx="700" ry="120"/></g>',
           f'<g id="floor" {stroke(c["ink"], 6)} stroke-opacity="0.35"><line x1="60" y1="1760" x2="1540" y2="1760"/></g>',
           f'<g id="point-of-light">{point(cx, shade_y + 20, c["gold"], 58)}</g>']
    return cw, ch, '\n'.join(out), 'Lamp — the doorway arch turned into a shade, one point of light beneath it, a cone and a pool of light on the floor.'
ILLUS['lamp'] = lamp

# ----------------------------------------------------------------------------- the seven service glyphs (128 grid)
GW, GR = 6, 4.2
def glyph(ink, n):
    c = pal(ink)
    s = lambda col=None, w=GW: stroke(col or c['ink'], w)
    g = {
      '01-experiential-design': [f'<path d="M26 94 L102 34" {s()}/>',
                                 point(26, 94, c['gold'], GR+1), point(102, 34, c['gold'], GR+1), point(64, 64, c['gold'], 2.4)],
      '02-museum-planning':     [f'<path d="M16 56 V30 h40 v26 M56 72 v26 h-40 V72 M72 56 V30 h40 v26 M112 72 v26 h-40 V72" {s()} stroke-opacity="0.7"/>',
                                 f'<path d="M10 64 H36 M56 64 H72 M92 64 H118" {s(c["ink2"], 3)} stroke-dasharray="0 7"/>',
                                 point(36, 64, c['gold'], GR), point(92, 64, c['gold'], GR)],
      '03-storytelling':        [f'<path d="M14 70 C34 20 50 20 64 64 S94 108 114 58" {s()}/>',
                                 point(34, 40, c['gold'], GR), point(64, 64, c['gold'], GR), point(94, 88, c['gold'], GR)],
      '04-spatial-branding':    [f'<path d="M34 108 V62 A30 30 0 0 1 94 62 V108" {s()}/>', f'<path d="M14 108 H114" {s(c["ink2"], 3)} stroke-opacity="0.8"/>',
                                 point(64, 84, c['gold'], GR)],
      '05-event-production':    [f'<path d="M34 24 L24 98 M34 24 L104 98" {s(c["ink2"], 3)} stroke-opacity="0.8"/>', f'<ellipse cx="64" cy="98" rx="44" ry="10" {s()}/>',
                                 point(34, 24, c['gold'], GR+1)],
      '06-digital-physical':    [f'<path d="M12 64 H42" {s()}/>', f'<rect x="42" y="38" width="44" height="52" rx="6" {s()}/>',
                                 f'<path d="M86 64 H116" {s()}/>', f'<rect x="54" y="52" width="6" height="6" fill="{c["ink2"]}"/><rect x="66" y="60" width="6" height="6" fill="{c["ink2"]}"/><rect x="58" y="70" width="6" height="6" fill="{c["ink2"]}"/><rect x="72" y="46" width="6" height="6" fill="{c["ink2"]}"/>',
                                 point(116, 64, c['gold'], GR)],
      '07-leadership':          [f'<circle cx="64" cy="64" r="42" {s()}/>'] + [f'<path d="M64 64 L{f(64+42*math.cos(a))} {f(64+42*math.sin(a))}" {s(c["ink2"], 3)} stroke-opacity="0.8"/>' for a in [-math.pi/2 + k*2*math.pi/7 for k in range(7)]]
                                + [point(64+52*math.cos(a), 64+52*math.sin(a), c['ink'], 3.2) for a in [-math.pi/2 + k*2*math.pi/7 for k in range(7)]] + [point(64, 64, c['gold'], GR+1)],
    }[n]
    return 128, 128, '\n'.join(g), f'Service glyph {n} — monoline on a 128 grid (stroke 6, point r 4.2), in the brand’s monoline vocabulary.'
for _n in ['01-experiential-design', '02-museum-planning', '03-storytelling', '04-spatial-branding', '05-event-production', '06-digital-physical', '07-leadership']:
    ILLUS[f'service-glyph-{_n}'] = (lambda n: (lambda ink: glyph(ink, n)))(_n)

# ----------------------------------------------------------------------------- main
def main(only=None):
    for d in ('svg', 'png', 'pdf'): (HERE / d).mkdir(exist_ok=True)
    for name, fn in ILLUS.items():
        if only and only not in name: continue
        for ink in ('dark', 'light'):
            w, h, body, desc = fn(ink)
            stem = f'sanzeed-illustration-{name}--{ink}'
            svgp = sz.write(HERE / 'svg' / f'{stem}.svg', sz.svg(w, h, body, f'Sanzeed illustration — {name} ({ink} ink)',
                            desc + f' {"Dark ink for Gallery Black / Night / Charcoal." if ink == "dark" else "Light ink for Plaster / Paper / Stone."} Generated by Illustrations/build_illustrations.py.'))
            ok = sz.export_svg(svgp, HERE / 'png' / stem, png=(2000,), formats='pdf,png')   # one call: PNG 2000 w + vector PDF
            (HERE / 'png' / f'{stem}.pdf').replace(HERE / 'pdf' / f'{stem}.pdf')
            print(stem, f'{w}x{h}', 'png+pdf' if ok else 'EXPORT FAILED')

if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else None)
