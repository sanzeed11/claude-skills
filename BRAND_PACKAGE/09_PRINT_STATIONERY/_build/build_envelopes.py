#!/usr/bin/env python3
"""Envelopes — DL 220×110 and C5 229×162 (landscape, flap on the long edge). Front: lockup top-left,
address zone and stamp zone marked on the guides layer. Back: symbol on the flap, return line below."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *

D = f'{OUT}/Envelopes'
SRC = f'{D}/src'
os.makedirs(SRC, exist_ok=True)
BL = 3
SIZES = {'dl': (220, 110, 12, 52, 36), 'c5': (229, 162, 15, 56, 46)}  # trim w, h, margin, lockup width, flap depth


def zone(x, y, w, h, label, colour='#2F62A0'):
    return (rect(x, y, w, h, stroke=colour, sw=0.15, extra='stroke-dasharray="1.2 0.8"') +
            text(x + 1.5, y + 3.2, label, 5, fam='heading', weight=500, fill=colour, upper=True, ls=0.08))


def front(tw, th, m, lw):
    W, H = tw + 2 * BL, th + 2 * BL
    g, lh, cap = logo('horizontal-descriptor', 'full-colour-light', lw, BL + m, BL + m, 'lockup')
    art = [g]
    # address zone (non-printing) — postal convention: lower right, clear of the stamp
    ax, ay, aw, ah = BL + tw * 0.46, BL + th * 0.42, tw * 0.46, th * 0.40
    gd = guides(tw, th, BL, m, label=True)
    gd += zone(ax, ay, aw, ah, 'Address zone — Inter 10 pt, Soot, left aligned, 4–6 lines')
    gd += zone(BL + tw - m - 32, BL + m, 32, 24, 'Stamp / franking')
    paper = rect(0, 0, W, H, fill=C['plaster'])
    return svg_doc(W, H, paper, '\n'.join(art), gd, title=f'Sanzeed envelope {tw:g}×{th:g} — front',
                   desc='Front: horizontal-descriptor lockup top-left. Address and stamp zones are guides only.')


def back(tw, th, m, flap):
    W, H = tw + 2 * BL, th + 2 * BL
    art = []
    # the flap: full-width straight flap with 6 mm chamfers, fold line at the top edge
    chamfer = 6
    fx0, fy0 = BL, BL
    flap_path = (f'M{fx0:.2f} {fy0:.2f} L{fx0 + tw:.2f} {fy0:.2f} L{fx0 + tw:.2f} {fy0 + flap - chamfer:.2f} '
                 f'L{fx0 + tw - chamfer:.2f} {fy0 + flap:.2f} L{fx0 + chamfer:.2f} {fy0 + flap:.2f} L{fx0:.2f} {fy0 + flap - chamfer:.2f} Z')
    # a Paper tint on the flap so the fold reads on screen (printer: optional)
    art.append(f'<path d="{flap_path}" fill="{C["paper"]}" />')
    sw = 9
    g, sh, cap = logo('symbol', 'full-colour-light', sw, BL + (tw - sw) / 2, BL + (flap - sh if False else 0) + (flap - sw * 500 / 598) / 2 - 1.5, 'symbol')
    art.append(g)
    # return line below the flap edge
    art.append(hairline(BL + m, BL + flap + 9, BL + tw - m, BL + flap + 9))
    art.append(text(BL + m, BL + flap + 13.5, 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  [Postal address], New Delhi, India  ·  sanzeed.com', 7, fill=C['umber']))
    gd = guides(tw, th, BL, m, label=True)
    gd += (f'<path d="{flap_path}" fill="none" stroke="#C0392B" stroke-width="0.15" />'
           f'<line x1="{BL}" y1="{BL + flap}" x2="{BL + tw}" y2="{BL + flap}" stroke="#C0392B" stroke-width="0.15" stroke-dasharray="2 1" />'
           + text(BL + m, BL + flap - 1.5, f'Flap — {flap} mm deep, fold on the top edge (dieline: adapt to the converter\'s standard flap)', 5,
                  fam='heading', weight=500, fill='#C0392B', upper=True, ls=0.08))
    paper = rect(0, 0, W, H, fill=C['plaster'])
    return svg_doc(W, H, paper, '\n'.join(art), gd, title=f'Sanzeed envelope {tw:g}×{th:g} — back',
                   desc='Back: symbol centred on the flap; return line under the fold. Dieline on the guides layer.')


tmpd = tempfile.mkdtemp()
for key, (tw, th, m, lw, flap) in SIZES.items():
    write(f'{SRC}/sanzeed-envelope--{key}-front.svg', front(tw, th, m, lw))
    write(f'{SRC}/sanzeed-envelope--{key}-back.svg', back(tw, th, m, flap))
    pages = []
    for side in ('front', 'back'):
        pdf = f'{tmpd}/{key}-{side}.pdf'
        svg_to_pdf(f'{SRC}/sanzeed-envelope--{key}-{side}.svg', pdf)
        pages.append(pdf)
    bleed_pdf = f'{tmpd}/{key}-bleed.pdf'
    merge_pdfs(pages, bleed_pdf)
    crop_pdf(bleed_pdf, f'{D}/sanzeed-envelope--{key}.pdf', BL)
    print_ready(bleed_pdf, f'{D}/sanzeed-envelope--{key}--print-cmyk.pdf', tw, th, BL)
    for i, side in enumerate(('front', 'back'), 1):
        pdf_to_png(f'{D}/sanzeed-envelope--{key}.pdf', f'{D}/sanzeed-envelope--{key}-{side}.png', dpi=200, page=i)
    # dieline preview with guides visible
    svg_to_png(f'{SRC}/sanzeed-envelope--{key}-front.svg', f'{D}/sanzeed-envelope--{key}-front-with-guides.png', width_px=1600, keep_guides=True)
    svg_to_png(f'{SRC}/sanzeed-envelope--{key}-back.svg', f'{D}/sanzeed-envelope--{key}-back-with-guides.png', width_px=1600, keep_guides=True)
print('envelopes done')
