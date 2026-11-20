#!/usr/bin/env python3
"""Rubber stamps — round 40 mm (symbol + ring text) and rectangular 58 × 22 mm (lockup + contact).
Single colour black; rings ≥ 0.5 mm; text converted to outlines by Inkscape for the deliverable SVG.
A 'stamp impression' preview in Gold Ink on Plaster is rendered from the outlined artwork."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *

D = f'{OUT}/Stamp'
SRC = f'{D}/src'
os.makedirs(SRC, exist_ok=True)
BLACK = '#000000'


def stamp_doc(w, h, art, title, desc):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" version="1.1">
  <title>{esc(title)}</title>
  <desc>{esc(desc)} 1 unit = 1 mm. Single colour black (100 K). No bleed — the stamp maker uses the outer cut circle/rectangle.</desc>
  <defs></defs>
  <g inkscape:groupmode="layer" inkscape:label="artwork" id="layer-artwork">
{art}
  </g>
</svg>
'''


# ------------------------------------------------------------------ round 40 mm
S = 40
cx = cy = S / 2
r_out, r_in, r_txt = 19.4, 12.6, 15.95
sw = 14
sh_ = logo_size('symbol', sw)[0]
g, sh, cap = logo('symbol', 'black', sw, cx - sw / 2, cy - sh_ / 2, 'sym')  # the S. centred in the inner ring
ring = [
    f'<circle cx="{cx}" cy="{cy}" r="{r_out}" fill="none" stroke="{BLACK}" stroke-width="0.7" />',
    f'<circle cx="{cx}" cy="{cy}" r="{r_in}" fill="none" stroke="{BLACK}" stroke-width="0.5" />',
    # text path: a full circle starting at 9 o'clock, clockwise, so the name reads across the top
    f'<path id="ringpath" d="M {cx - r_txt} {cy} A {r_txt} {r_txt} 0 1 1 {cx + r_txt} {cy} A {r_txt} {r_txt} 0 1 1 {cx - r_txt} {cy}" fill="none" stroke="none" />',
    f'<text style="font-family:\'Inter Tight\';font-weight:700;font-size:{7.0 * PT:.4f}px;fill:{BLACK};letter-spacing:{0.10 * 7.0 * PT:.4f}px" xml:space="preserve">'
    f'<textPath xlink:href="#ringpath" startOffset="0">SANZEED MIRZA · EXPERIENTIAL DESIGN CONSULTANT · NEW DELHI ·</textPath></text>',
    g,
]
ROUND_SRC = write(f'{SRC}/sanzeed-stamp--round-40mm--editable.svg', stamp_doc(S, S, '\n'.join(ring), 'Sanzeed stamp — round 40 mm (editable text)',
                  'Outer ring 0.7 mm, inner ring 0.5 mm, ring text Inter Tight Bold 7 pt (+0.10 em) on a 15.95 mm radius, symbol (the S with its full stop) 14 mm.'))

# ------------------------------------------------------------------ rectangular 58 × 22 mm
RW, RH = 58, 22
lw = 50
MIN_LINE = 0.5  # mm — minimum line weight / gap a rubber or photopolymer stamp holds
# The wordmark's Z point sits inside a thin ring (a gap cut into the diagonal). At stamp sizes that gap closes
# up below the minimum, so the stamp takes the plain wordmark (no points, Z ring and D stem closed) in the
# horizontal-descriptor lockup geometry. If the lockup is ever enlarged enough to hold the gap, the full mark returns.
z_gap_mm = z_ring_gap_units() * logo_size('primary-wordmark', lw)[1] / cap_units()  # units → mm at lw
LOCKUP = 'horizontal-descriptor' if z_gap_mm >= MIN_LINE else 'horizontal-descriptor-plain'
print(f'rectangular stamp: Z ring gap at {lw} mm = {z_gap_mm:.2f} mm (min {MIN_LINE}) -> {LOCKUP}')
g2, lh2, cap2 = logo(LOCKUP, 'black', lw, (RW - lw) / 2, 2.8, 'lockup')
rect_art = [
    rect(0.35, 0.35, RW - 0.7, RH - 0.7, stroke=BLACK, sw=0.6, rx=1.2),
    g2,
    text(RW / 2, 16.9, '+91 7827051270  ·  sanzeed@gmail.com', 6.2, fam='heading', weight=700, fill=BLACK, anchor='middle', ls=0.02),
    text(RW / 2, 20.1, 'sanzeed.com  ·  New Delhi, India', 6.2, fam='heading', weight=700, fill=BLACK, anchor='middle', ls=0.02),
]
RECT_SRC = write(f'{SRC}/sanzeed-stamp--rectangular-58x22mm--editable.svg', stamp_doc(RW, RH, '\n'.join(rect_art), 'Sanzeed stamp — rectangular 58 × 22 mm (editable text)',
                 f'Border 0.6 mm, horizontal-descriptor lockup 50 mm (minimum size)'
                 + (' with the plain wordmark (no points: the Z ring gap would be {:.2f} mm, below the 0.5 mm stamp minimum)'.format(z_gap_mm) if LOCKUP.endswith('plain') else '')
                 + ', contact in Inter Tight Bold 6.2 pt.'))

# ------------------------------------------------------------------ exports: outlined SVG (deliverable), PDF, PNG, impression preview
for src, name, w, h in ((ROUND_SRC, 'round-40mm', S, S), (RECT_SRC, 'rectangular-58x22mm', RW, RH)):
    outlined = f'{D}/sanzeed-stamp--{name}.svg'
    svg_to_outlined_svg(src, outlined)
    s = open(outlined, encoding='utf-8').read()
    assert '<text' not in s, 'text not outlined'
    svg_to_pdf(outlined, f'{D}/sanzeed-stamp--{name}.pdf')
    svg_to_png(outlined, f'{D}/sanzeed-stamp--{name}.png', width_px=mm_to_px(w, 600))
    # impression: Gold Ink on Plaster, 92 % ink
    imp = s.replace('#000000', C['goldink']).replace('fill:#000000', f'fill:{C["goldink"]}')
    imp = re.sub(r'(<svg[^>]*>)', r'\1<rect width="100%" height="100%" fill="#F5F0E7"/>', imp, count=1)
    imp = imp.replace('<g', '<g opacity="0.92"', 1)
    tmp = write(f'{SRC}/_impression-{name}.svg', imp)
    svg_to_png(tmp, f'{D}/sanzeed-stamp--{name}--impression-gold-ink.png', width_px=mm_to_px(w, 400))
    os.remove(tmp)
    print(name, pdfinfo(f'{D}/sanzeed-stamp--{name}.pdf').split('Page size:')[1].split('\n')[0].strip())
print('stamp done')
