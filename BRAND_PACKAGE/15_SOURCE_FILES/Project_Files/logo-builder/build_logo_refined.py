#!/usr/bin/env python3
"""
Sanzeed logo system — REFINED ORIGINAL master (approved option B).

Source of truth: refined_master.svg — the original sanzeed.com wordmark cleaned letter by letter
(S, A, N, D re-traced with smooth edges; E bars exact rectangles; original gold points), with the new Z:
straight bars, a diagonal that swoops like the N's right leg, and a point of light at the D-dot height
separated from the stroke by a ring.

This script derives every variant (wordmark, plain, symbol, monogram, lockups, small sizes, tiles) from that
master and writes the construction SVG set + manifest.json consumed by export_logo.py — the same contract as
build_logo.py, which it reuses for lockups, descriptor outlines, colourways and the SVG writer.

Usage: python3 build_logo_refined.py <output_dir>
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_logo_geometric_v1 as bl
from retrace_lib import retrace

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = os.path.join(HERE, 'refined_master.svg')
src = open(MASTER).read()
P = dict(re.findall(r'<path id="wm-(\w+)" d="([^"]+)"', src))
DOTS = [(float(a), float(b), float(c)) for a, b, c in re.findall(r'<circle class="wm-dot" cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', src)]
Z_PLAIN = dict(re.findall(r'<path id="wm-(\w+)" d="([^"]+)"', open(os.path.join(HERE, 'refined_master_plain_z.svg')).read()))['Z']

def nums(d): return [float(v) for v in re.findall(r'-?\d+\.?\d*', d)]
def bbox(paths):
    """Bounding box from a real path parse (handles M/L/H/V/C/A/Z)."""
    xs, ys = [], []
    for d in paths:
        bl._xform(d, lambda x: (xs.append(x), x)[1], lambda y: (ys.append(y), y)[1], lambda r: r)
    return min(xs), min(ys), max(xs), max(ys)

ORDER = ['S', 'A', 'N', 'Z', 'E1', 'E2', 'D']
X0, Y0, X1, Y1 = bbox([P[k] for k in ORDER])
H = Y1 - Y0                                   # full height incl. the S overshoot (≈ 520)
bl.CAP = H                                    # lockup maths in build_logo uses CAP as the mark height
RING_GAP = 14.0

def shift(d, dx, dy): return bl.shift_path(d, dx, dy)

def _thicken(paths, dots, grow, dot_r, gap, name):
    """Small-size version: grow every stroke by `grow` units per side (raster dilation + re-trace), then re-open
    clear rings around the points so they never touch a stroke."""
    body = ''.join(f'<path d="{d}" stroke="#000" stroke-width="{2*grow}" stroke-linejoin="round"/>' for d in paths)
    body += ''.join(f'<circle cx="{x}" cy="{y}" r="{dot_r + gap}" fill="#fff"/>' for x, y, _ in dots)
    xs = bbox(paths)
    return retrace(body, [xs[0] - grow - 5, xs[1] - grow - 5, xs[2] + grow + 5, xs[3] + grow + 5], blur_units=0.6, opttol=0.3, name=name, workdir='/tmp')

def wordmark(dots=True, stroke_scale=1.0):
    small = bl.W > 64                          # build_logo flips W to 84 for the small-size pass
    dx, dy = -X0, -Y0
    letters = [(k, shift(P[k], dx, dy)) for k in ORDER]
    d_out = [(x + dx, y + dy, r) for x, y, r in DOTS] if dots else []
    width = X1 - X0
    if not dots:                               # plain version: whole Z (no ring) and a closed D stem
        dX0 = bbox([P['D']])[0]; dcy = DOTS[1][1]
        xs, ys = [], []
        bl._xform(P['D'], lambda x: (xs.append(x), x)[1], lambda y: (ys.append(y), y)[1], lambda r: r)
        near = [(x, y) for x, y in zip(xs, ys) if x < dX0 + 80 and abs(y - dcy) < 130]   # the two cut ends of the stem
        stem_r = max(x for x, _ in near); g0 = min(y for _, y in near) - 2; g1 = max(y for _, y in near) + 2
        bridge = f'M{dX0:.2f} {g0:.2f}H{stem_r:.2f}V{g1:.2f}H{dX0:.2f}Z'
        letters = [(k, shift(Z_PLAIN, dx, dy) if k == 'Z' else d) for k, d in letters] + [('D-bridge', shift(bridge, dx, dy))]
    if small:
        g, r = 10.0, 50.0
        thick = _thicken([d for _, d in letters], d_out, g, r, 12.0, 'wm_small')
        sc = H / (H + 2 * g)                   # fit the grown outline back inside the mark's box
        letters = [('all', bl.scale_path(shift(thick, g, g), sc))]
        d_out = [((x + g) * sc, (y + g) * sc, r * sc) for x, y, _ in d_out]; width = (width + 2 * g) * sc
    return {'letters': letters, 'dots': d_out, 'width': width, 'height': H}

def _symbol_parts():
    sx0, sy0, sx1, sy1 = bbox([P['S']])
    s = shift(P['S'], -sx0, -Y0)
    w = sx1 - sx0
    return s, w

def symbol():
    s, w = _symbol_parts(); r = 45.0
    small = bl.W > 64
    dot = (w + 60 + r, H - r - 1, r)
    letters = [('S', s)]
    if small:
        g = 10.0; sc = H / (H + 2 * g); r = 52.0
        thick = bl.scale_path(shift(_thicken([s], [], g, r, 0, 'sym_small'), g, g), sc)
        letters = [('S', thick)]; ws = (w + 2 * g) * sc
        dot = (ws + 56 + r, H - r - 1, r)
    return {'letters': letters, 'dots': [dot], 'width': dot[0] + dot[2], 'height': H}

def _m_path():
    nx0, _, nx1, _ = bbox([P['N']]); nw = nx1 - nx0
    first = shift(P['N'], -nx0, -Y0)
    second = shift(P['N'], -nx0 + nw - 45, -Y0)      # second N's stem swallows the first N's foot
    return [first, second], 2 * nw - 45

def monogram():
    s, sw = _symbol_parts(); (m1, m2), mw = _m_path(); gap = 110; r = 45.0
    x = sw + gap
    letters = [('S', s), ('M-0', shift(m1, x, 0)), ('M-1', shift(m2, x, 0))]
    dot = (x + mw + 60 + r, H - r - 1, r)
    return {'letters': letters, 'dots': [dot], 'width': dot[0] + r, 'height': H}

bl.wordmark = wordmark; bl.symbol = symbol; bl.monogram = monogram
_svg_doc = bl.svg_doc
def svg_doc(*a, **k):
    return _svg_doc(*a, **k).replace('Constructed on a 500-unit cap height with a 64-unit stroke. Generated by build_logo.py (editable master).',
                                     'Refined original Sanzeed wordmark (approved option B). Generated by build_logo_refined.py from refined_master.svg.')
bl.svg_doc = svg_doc

def write_construction(out_dir, wm):
    """Refined construction sheet: the outline on a 20-unit grid, cap/baseline/mid guides, the three points."""
    w, h = wm['width'], wm['height']; cs = h * 0.5; pad = cs + 120; vw, vh = w + 2 * pad, h + 2 * pad
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw:.0f} {vh:.0f}" width="{vw:.0f}" height="{vh:.0f}">',
         '<rect width="100%" height="100%" fill="#0D0D0F"/>',
         '<defs><pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="rgba(233,178,90,0.12)" stroke-width="1"/></pattern></defs>',
         '<rect width="100%" height="100%" fill="url(#g)"/>',
         f'<rect x="{pad-cs:.1f}" y="{pad-cs:.1f}" width="{w+2*cs:.1f}" height="{h+2*cs:.1f}" fill="none" stroke="#E9B25A" stroke-width="3" stroke-dasharray="18 14"/>',
         f'<g transform="translate({pad:.1f} {pad:.1f})"><g fill="rgba(245,245,247,0.92)">' + ''.join(f'<path d="{d}"/>' for _, d in wm['letters']) + '</g>',
         '<g fill="#E9B25A">' + ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>' for x, y, r in wm['dots']) + '</g>']
    for y, lab in [(40 - Y0, 'cap'), (h / 2, 'mid / D-point / Z-point'), (h - 1, 'baseline')]:
        o.append(f'<line x1="{-cs:.0f}" y1="{y:.1f}" x2="{w+cs:.0f}" y2="{y:.1f}" stroke="#E9B25A" stroke-width="2" stroke-opacity="0.6"/>')
        o.append(f'<text x="{w+cs+16:.0f}" y="{y+10:.1f}" font-family="Inter, sans-serif" font-size="30" fill="#E9B25A">{lab}</text>')
    o.append(f'<text x="0" y="{h+cs+90:.0f}" font-family="Inter, sans-serif" font-size="34" fill="#F5F5F7">Refined original wordmark · stroke ≈ 64 · points r 45 · Z point ringed at 14 · clear space x = ½ height.</text>')
    o.append('</g></svg>')
    open(os.path.join(out_dir, 'sanzeed-construction-sheet.svg'), 'w').write('\n'.join(o))
bl.write_construction = write_construction

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else 'construction'
    m = bl.write_all(out)
    print(f'wrote {len(m)} SVG files to {out} (refined master, height {H:.1f}, width {X1-X0:.1f})')
