#!/usr/bin/env python3
"""
Sanzeed logo system — parametric construction source.

This script IS the editable master of the logo family. Every letterform is
constructed from a 500-unit cap height and a 64-unit monoline stroke; dots are
45-unit radius "points of light". Change a parameter, re-run, and every
variant, colourway and lockup is regenerated as clean outlined SVG.

Usage:  python3 build_logo.py <output_dir>
Requires: fontTools (for the descriptor text outlines). Inkscape is optional
(used by export_logo.py for PDF/EPS/PNG, not here).
"""
import math, os, sys, json, re
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

# ---------------------------------------------------------------- parameters
W      = 64      # stroke weight
CAP    = 500     # cap height
DOT_R  = 45      # point-of-light radius
S_R    = 96      # S hook centreline radius
S_D    = 192     # horizontal offset between the two S hooks
S_EMID = 86      # length of the passing mid terminals
S_ETOP = 140     # length of the top/bottom terminals
A_W    = 560     # A outer width
N_W    = 460     # N (arch) width
Z_W    = 470     # Z width
E_W    = 324     # E bar width
D_W    = 380     # D width
GAPS   = {'SA': 88, 'AN': 64, 'NZ': 104, 'ZE': 118, 'EE': 132, 'ED': 118}
DESCRIPTOR = "EXPERIENTIAL DESIGN CONSULTANT"
FONT_DIR = os.environ.get("BRAND_FONT_DIR", os.path.expanduser("~/.fonts/brand"))

# ---------------------------------------------------------------- primitives
def f(v): return f"{v:.2f}".rstrip('0').rstrip('.')
def rect(x, y, w, h):
    return f"M{f(x)} {f(y)}H{f(x+w)}V{f(y+h)}H{f(x)}Z"
def pol(cx, cy, r, a):
    a = math.radians(a); return cx + r*math.cos(a), cy + r*math.sin(a)
def ring(cx, cy, R, r, a0, a1):
    """Annular sector from angle a0 to a1 (degrees, SVG y-down, clockwise positive)."""
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1-a0) > 180.0001 else 0
    ox0, oy0 = pol(cx, cy, R, a0); ox1, oy1 = pol(cx, cy, R, a1)
    ix0, iy0 = pol(cx, cy, r, a0); ix1, iy1 = pol(cx, cy, r, a1)
    return (f"M{f(ox0)} {f(oy0)}A{f(R)} {f(R)} 0 {large} {sweep} {f(ox1)} {f(oy1)}"
            f"L{f(ix1)} {f(iy1)}A{f(r)} {f(r)} 0 {large} {1-sweep} {f(ix0)} {f(iy0)}Z")
def circle(cx, cy, r):
    return (f"M{f(cx-r)} {f(cy)}A{f(r)} {f(r)} 0 1 0 {f(cx+r)} {f(cy)}"
            f"A{f(r)} {f(r)} 0 1 0 {f(cx-r)} {f(cy)}Z")
def poly(pts):
    return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts) + "Z"

# ---------------------------------------------------------------- letters
def letter_S():
    cx1 = S_R + W/2; cy1 = S_R + W/2
    cx2 = cx1 + S_D;  cy2 = CAP - S_R - W/2
    parts = [
        ring(cx1, cy1, S_R + W/2, S_R - W/2, 90, 270),          # top hook (opens right, via 180°)
        rect(cx1, cy1 - S_R - W/2, S_ETOP, W),                     # top terminal →
        rect(cx1, cy1 + S_R - W/2, S_EMID, W),                     # mid terminal → (upper)
        ring(cx2, cy2, S_R + W/2, S_R - W/2, -90, 90),            # bottom hook (opens left)
        rect(cx2 - S_EMID, cy2 - S_R - W/2, S_EMID, W),            # mid terminal ← (lower)
        rect(cx2 - S_ETOP, cy2 + S_R - W/2, S_ETOP, W),            # bottom terminal ←
    ]
    width = cx2 + S_R + W/2
    return parts, width

def letter_A():
    ang = math.atan2(CAP, A_W/2); off = W/math.sin(ang)
    y_in = CAP - (A_W/2 - off) * (CAP/(A_W/2))
    outer = [(0, CAP), (A_W/2, 0), (A_W, CAP)]
    inner = [(A_W - off, CAP), (A_W/2, y_in), (off, CAP)]
    return [poly(outer + inner)], A_W

def letter_N():
    r = (N_W - W)/2; cy = r + W/2
    return [ring(N_W/2, cy, r + W/2, r - W/2, 180, 360),
            rect(0, cy, W, CAP - cy), rect(N_W - W, cy, W, CAP - cy)], N_W

def letter_Z():
    dx, dy = Z_W, CAP - 2*W
    dz = W / math.sin(math.atan2(dy, dx))
    return [rect(0, 0, Z_W, W), rect(0, CAP - W, Z_W, W),
            poly([(Z_W - dz, W), (Z_W, W), (dz, CAP - W), (0, CAP - W)])], Z_W

def letter_E():
    mid = (CAP - W)/2
    return [rect(0, 0, E_W, W), rect(0, mid, E_W, W), rect(0, CAP - W, E_W, W)], E_W

def letter_D(dot=True):
    R = CAP/2; straight = D_W - R
    parts = [rect(0, 0, straight, W), rect(0, CAP - W, straight, W),
             ring(straight, R, R, R - W, -90, 90)]
    if dot:   # stem broken around the point of light
        clear = 14
        parts += [rect(0, 0, W, R - DOT_R - clear), rect(0, R + DOT_R + clear, W, R - DOT_R - clear)]
    else:
        parts += [rect(0, 0, W, CAP)]
    return parts, D_W

def letter_M():
    stem_gap = 268; arch_r = (stem_gap + W)/2; cy = arch_r
    parts = []
    for i, x0 in enumerate([0, stem_gap, 2*stem_gap]):
        parts.append(rect(x0, cy, W, CAP - cy))
    for cx in [arch_r + 0, arch_r + stem_gap]:
        parts.append(ring(cx, cy, arch_r, arch_r - W, 180, 360))
    return parts, 2*stem_gap + W




_NARGS = {'M':2,'L':2,'H':1,'V':1,'C':6,'S':4,'Q':4,'T':2,'A':7,'Z':0}
def _xform(p, fx, fy, fr):
    """Apply fx to x coords, fy to y coords, fr to radii in an absolute-command SVG path."""
    toks = re.findall(r'[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?', p)
    out = []; i = 0; cmd = None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t.upper(); out.append(cmd); i += 1; continue
        n = _NARGS.get(cmd, 2)
        if n == 0: i += 1; continue
        if out and out[-1] and not out[-1][-1].isalpha(): out.append(cmd)  # implicit repeat -> explicit command
        args = [float(a) for a in toks[i:i+n]]; i += n
        if cmd == 'H': out.append(f(fx(args[0])))
        elif cmd == 'V': out.append(f(fy(args[0])))
        elif cmd == 'A':
            rx, ry, rot, la, sw, x, y = args
            out.append(f"{f(fr(rx))} {f(fr(ry))} {int(rot)} {int(la)} {int(sw)} {f(fx(x))} {f(fy(y))}")
        else:
            out.append(" ".join(f"{f(fx(args[k]))} {f(fy(args[k+1]))}" for k in range(0, n, 2)))
        if cmd == 'M': cmd = 'L'   # implicit linetos after a moveto (SVG grammar)
    return "".join(out)

def shift_path(p, dx, dy=0):
    return _xform(p, lambda x: x+dx, lambda y: y+dy, lambda r: r)

def scale_path(p, s):
    return _xform(p, lambda x: x*s, lambda y: y*s, lambda r: r*s)

# ---------------------------------------------------------------- wordmark assembly
def wordmark(dots=True, stroke_scale=1.0):
    """Returns dict: letters -> list of (id, path), dots -> list of (cx,cy,r), width."""
    letters = []; dots_out = []; x = 0
    seq = [('S', letter_S), ('A', letter_A), ('N', letter_N), ('Z', letter_Z),
           ('E', letter_E), ('E2', letter_E), ('D', lambda: letter_D(dot=dots))]
    gaps = ['SA', 'AN', 'NZ', 'ZE', 'EE', 'ED']
    for i, (name, fn) in enumerate(seq):
        parts, w = fn()
        for j, p in enumerate(parts):
            letters.append((f"{name}-{j}", shift_path(p, x)))
        if name == 'A' and dots: dots_out.append((x + A_W/2, CAP - 88, DOT_R))
        if name == 'D' and dots: dots_out.append((x + W/2, CAP/2, DOT_R))
        x += w
        if i < len(gaps): x += GAPS[gaps[i]]
    return {'letters': letters, 'dots': dots_out, 'width': x, 'height': CAP}

def symbol():
    parts, w = letter_S()
    dot_cx = w + 60 + DOT_R
    return {'letters': [(f"S-{j}", p) for j, p in enumerate(parts)],
            'dots': [(dot_cx, CAP - DOT_R, DOT_R)], 'width': dot_cx + DOT_R, 'height': CAP}

def monogram():
    s_parts, sw = letter_S(); m_parts, mw = letter_M()
    gap = 96; x = sw + gap
    letters = [(f"S-{j}", p) for j, p in enumerate(s_parts)] + \
              [(f"M-{j}", shift_path(p, x)) for j, p in enumerate(m_parts)]
    dot_cx = x + mw + 60 + DOT_R
    return {'letters': letters, 'dots': [(dot_cx, CAP - DOT_R, DOT_R)], 'width': dot_cx + DOT_R, 'height': CAP}

# ---------------------------------------------------------------- descriptor text (outlined)
_font_cache = {}
def text_outline(text, family="InterTight", wght=600, cap_height=100, tracking_em=0.18, fit_width=None):
    key = (family, wght)
    if key not in _font_cache:
        path = {'InterTight': 'InterTight[wght].ttf', 'Inter': 'Inter[opsz,wght].ttf'}[family]
        vf = TTFont(os.path.join(FONT_DIR, path))
        axes = {'wght': wght}
        if 'opsz' in [a.axisTag for a in vf['fvar'].axes]: axes['opsz'] = 14
        _font_cache[key] = instantiateVariableFont(vf, axes)
    font = _font_cache[key]
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    capH = font['OS/2'].sCapHeight or 0.73*upm
    s = cap_height / capH
    glyphs = [cmap[ord(c)] for c in text]
    widths = [gs[g].width for g in glyphs]
    natural = sum(widths) * s
    n = len(text)
    if fit_width:
        tracking = (fit_width - natural) / (n - 1)
    else:
        tracking = tracking_em * cap_height / 0.73
    paths = []; x = 0
    for g, w in zip(glyphs, widths):
        pen = SVGPathPen(gs)
        tp = TransformPen(pen, (s, 0, 0, -s, x, cap_height))
        gs[g].draw(tp)
        d = pen.getCommands()
        if d: paths.append(d)
        x += w*s + tracking
    total = x - tracking
    return paths, total, cap_height

# ---------------------------------------------------------------- SVG writer
COLOURWAYS = {
    'full-colour-dark':  {'ink': '#F5F5F7', 'dot': '#E9B25A', 'bg': None},
    'full-colour-light': {'ink': '#1A1816', 'dot': '#B8863B', 'bg': None},
    'black':             {'ink': '#000000', 'dot': '#000000', 'bg': None},
    'white':             {'ink': '#FFFFFF', 'dot': '#FFFFFF', 'bg': None},
    'grayscale':         {'ink': '#000000', 'dot': '#8C8C8C', 'bg': None},
    'grayscale-inverted':{'ink': '#FFFFFF', 'dot': '#9A9A9A', 'bg': None},
    'single-colour-gold':{'ink': '#B8863B', 'dot': '#B8863B', 'bg': None},
}

def svg_doc(groups, width, height, colour, pad=0, bg=None, title="", ids=True, viewbox_pad=None):
    """groups: list of dicts {name, letters:[(id,path)], dots:[(cx,cy,r)], text:[paths]}"""
    c = COLOURWAYS[colour]
    vp = pad if viewbox_pad is None else viewbox_pad
    vw, vh = width + 2*vp, height + 2*vp
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(vw)} {f(vh)}" width="{f(vw)}" height="{f(vh)}" role="img" aria-label="{title}">',
           f'<title>{title}</title>',
           f'<desc>Sanzeed logo system — {colour}. Constructed on a 500-unit cap height with a 64-unit stroke. Generated by build_logo.py (editable master).</desc>']
    if bg: out.append(f'<rect width="{f(vw)}" height="{f(vh)}" fill="{bg}"/>')
    out.append(f'<g transform="translate({f(vp)} {f(vp)})">')
    for g in groups:
        out.append(f'<g id="{g["name"]}">')
        if g.get('letters'):
            out.append(f'<g id="{g["name"]}-ink" fill="{c["ink"]}">')
            for lid, p in g['letters']:
                out.append(f'<path id="{g["name"]}-{lid}" d="{p}"/>' if ids else f'<path d="{p}"/>')
            out.append('</g>')
        if g.get('dots'):
            out.append(f'<g id="{g["name"]}-dots" fill="{c["dot"]}">')
            for (cx, cy, r) in g['dots']:
                out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"/>')
            out.append('</g>')
        if g.get('text'):
            out.append(f'<g id="{g["name"]}-text" fill="{c["ink"]}">')
            for p in g['text']:
                out.append(f'<path d="{p}"/>')
            out.append('</g>')
        out.append('</g>')
    out.append('</g></svg>')
    return "\n".join(out)

def offset_group(g, dx, dy, name=None):
    return {'name': name or g.get('name', 'g'),
            'letters': [(i, shift_path(p, dx, dy)) for i, p in g.get('letters', [])],
            'dots': [(cx+dx, cy+dy, r) for cx, cy, r in g.get('dots', [])],
            'text': [shift_path(p, dx, dy) for p in g.get('text', [])]}

def scale_group(g, s, name=None):
    return {'name': name or g.get('name', 'g'),
            'letters': [(i, scale_path(p, s)) for i, p in g.get('letters', [])],
            'dots': [(cx*s, cy*s, r*s) for cx, cy, r in g.get('dots', [])],
            'text': [scale_path(p, s) for p in g.get('text', [])]}

# ---------------------------------------------------------------- variants
def build_variants():
    V = {}
    wm = wordmark(); wm['name'] = 'wordmark'
    V['primary-wordmark'] = ([wm], wm['width'], CAP)

    plain = wordmark(dots=False); plain['name'] = 'wordmark'
    V['wordmark-plain'] = ([plain], plain['width'], CAP)

    sym = symbol(); sym['name'] = 'symbol'
    V['symbol'] = ([sym], sym['width'], CAP)

    mono = monogram(); mono['name'] = 'monogram'
    V['monogram'] = ([mono], mono['width'], CAP)

    # secondary: symbol + wordmark, horizontal
    gap = 200
    V['secondary-symbol-wordmark'] = ([sym, offset_group(wm, sym['width'] + gap, 0, 'wordmark')],
                                      sym['width'] + gap + wm['width'], CAP)

    # horizontal lockup: wordmark with descriptor justified beneath
    tp, tw, th = text_outline(DESCRIPTOR, cap_height=92, fit_width=wm['width'])
    desc = {'name': 'descriptor', 'text': [shift_path(p, 0, CAP + 150) for p in tp]}
    V['horizontal-descriptor'] = ([wm, desc], wm['width'], CAP + 150 + th)

    # vertical / stacked: symbol centred above wordmark, descriptor beneath
    sym_s = 1.0
    sx = (wm['width'] - sym['width'])/2
    gap_v = 190
    top = offset_group(sym, sx, 0, 'symbol')
    mid = offset_group(wm, 0, CAP + gap_v, 'wordmark')
    tp2, tw2, th2 = text_outline(DESCRIPTOR, cap_height=92, tracking_em=0.22)
    desc2 = {'name': 'descriptor', 'text': [shift_path(p, (wm['width']-tw2)/2, 2*CAP + gap_v + 150) for p in tp2]}
    V['vertical-stacked'] = ([top, mid, desc2], wm['width'], 2*CAP + gap_v + 150 + th2)

    # simplified / small-size: heavier stroke, larger dots, no stem break
    global W, DOT_R
    W0, D0 = W, DOT_R
    W, DOT_R = 84, 56
    small = wordmark(); small['name'] = 'wordmark'
    V['simplified-small-size'] = ([small], small['width'], CAP)
    sym_small = symbol(); sym_small['name'] = 'symbol'
    V['symbol-small-size'] = ([sym_small], sym_small['width'], CAP)
    W, DOT_R = W0, D0

    # symbol tile (app icon / favicon / social avatar): S. centred in rounded square
    V['symbol-tile'] = ([sym], sym['width'], CAP)   # handled specially in writer
    return V

def write_all(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    V = build_variants()
    manifest = []
    for vname, (groups, w, h) in V.items():
        for colour in COLOURWAYS:
            if vname == 'symbol-tile':
                # 1000-unit tile, 22% corner radius, symbol scaled to 60% width
                tile = 1000; rad = 220
                s = 0.58 * tile / w
                g = scale_group(groups[0], s, 'symbol')
                gw, gh = w*s, h*s
                g = offset_group(g, (tile-gw)/2, (tile-gh)/2 + 10, 'symbol')
                for bgname, bgcol, ink in [('dark', '#0D0D0F', 'full-colour-dark'), ('light', '#F5F0E7', 'full-colour-light'), ('gold', '#B8863B', 'black')]:
                    if colour != ink: continue
                    c = COLOURWAYS[colour]
                    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tile} {tile}" width="{tile}" height="{tile}" role="img" aria-label="Sanzeed symbol tile">',
                           f'<title>Sanzeed — symbol tile ({bgname})</title>',
                           f'<rect id="tile" width="{tile}" height="{tile}" rx="{rad}" fill="{bgcol}"/>',
                           f'<g id="symbol-ink" fill="{c["ink"]}">'] + [f'<path id="symbol-{lid}" d="{p}"/>' for lid, p in g['letters']] + ['</g>',
                           f'<g id="symbol-dots" fill="{c["dot"]}">'] + [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"/>' for cx, cy, r in g['dots']] + ['</g></svg>']
                    fn = f"sanzeed-symbol-tile--{bgname}.svg"
                    open(os.path.join(out_dir, fn), 'w').write("\n".join(svg))
                    manifest.append({'file': fn, 'variant': 'symbol-tile', 'colour': bgname, 'w': tile, 'h': tile})
                    # square (no rounding) version for platforms that mask themselves
                    fn2 = f"sanzeed-symbol-tile-square--{bgname}.svg"
                    open(os.path.join(out_dir, fn2), 'w').write("\n".join(svg).replace(f'rx="{rad}" ', ''))
                    manifest.append({'file': fn2, 'variant': 'symbol-tile-square', 'colour': bgname, 'w': tile, 'h': tile})
                continue
            pad = 0
            svg = svg_doc(groups, w, h, colour, pad=pad, title=f"Sanzeed — {vname} ({colour})")
            fn = f"sanzeed-{vname}--{colour}.svg"
            open(os.path.join(out_dir, fn), 'w').write(svg)
            manifest.append({'file': fn, 'variant': vname, 'colour': colour, 'w': round(w, 2), 'h': round(h, 2)})
    json.dump(manifest, open(os.path.join(out_dir, 'manifest.json'), 'w'), indent=1)
    # construction sheet with grid and clear-space for the guidelines
    wm = wordmark(); wm['name'] = 'wordmark'
    write_construction(out_dir, wm)
    return manifest

def write_construction(out_dir, wm):
    w, h = wm['width'], CAP
    cs = CAP * 0.5   # clear space = height of the S hooks' half (= 0.5 cap) — documented as "x"
    pad = cs + 120
    vw, vh = w + 2*pad, h + 2*pad
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(vw)} {f(vh)}" width="{f(vw)}" height="{f(vh)}">',
           '<rect width="100%" height="100%" fill="#0D0D0F"/>',
           '<defs><pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse">'
           '<path d="M64 0H0V64" fill="none" stroke="rgba(233,178,90,0.18)" stroke-width="1"/></pattern></defs>',
           f'<rect width="100%" height="100%" fill="url(#grid)"/>',
           f'<rect x="{f(pad-cs)}" y="{f(pad-cs)}" width="{f(w+2*cs)}" height="{f(h+2*cs)}" fill="none" stroke="#E9B25A" stroke-width="3" stroke-dasharray="18 14"/>',
           f'<rect x="{f(pad)}" y="{f(pad)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="rgba(245,245,247,0.5)" stroke-width="2"/>',
           f'<g transform="translate({f(pad)} {f(pad)})">']
    out.append('<g fill="rgba(245,245,247,0.92)">' + "".join(f'<path d="{p}"/>' for _, p in wm['letters']) + '</g>')
    out.append('<g fill="#E9B25A">' + "".join(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}"/>' for cx, cy, r in wm['dots']) + '</g>')
    # guides: cap, baseline, mid
    for y, lab in [(0, 'cap height 500'), (CAP/2, 'mid 250'), (CAP, 'baseline')]:
        out.append(f'<line x1="{f(-cs)}" y1="{f(y)}" x2="{f(w+cs)}" y2="{f(y)}" stroke="#E9B25A" stroke-width="2" stroke-opacity="0.6"/>')
        out.append(f'<text x="{f(w+cs+16)}" y="{f(y+10)}" font-family="Inter, sans-serif" font-size="30" fill="#E9B25A">{lab}</text>')
    out.append(f'<text x="0" y="{f(CAP+cs+90)}" font-family="Inter, sans-serif" font-size="34" fill="#F5F5F7">Clear space = x, where x = ½ cap height (250 units). Stroke 64 · dot radius 45 · cap 500.</text>')
    out.append('</g></svg>')
    open(os.path.join(out_dir, 'sanzeed-construction-sheet.svg'), 'w').write("\n".join(out))

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'out'
    m = write_all(out)
    print(f"wrote {len(m)} SVG files to {out}")
