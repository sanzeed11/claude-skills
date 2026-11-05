#!/usr/bin/env python3
"""Notepad sheets — A5 (148×210) and A4 (210×297), 3 mm bleed. Header lockup, ruled 'beams' (hairlines,
the first one carrying the single gold point), footer contact line."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *

D = f'{OUT}/Notepad'
SRC = f'{D}/src'
os.makedirs(SRC, exist_ok=True)
BL = 3
SIZES = {'a5': (148, 210, 12, 50, 8.0), 'a4': (210, 297, 20, 56, 9.0)}  # trim, margin, lockup width, rule pitch


def sheet(key, tw, th, m, lw, pitch):
    W, H = tw + 2 * BL, th + 2 * BL
    a = []
    g, lh, cap = logo('horizontal-descriptor', 'full-colour-light', lw, BL + m, BL + m, 'lockup')
    a.append(g)
    y = BL + m + lh + cap  # clear space below the lockup, then the first beam
    y0 = round(y + 6, 1)
    fy = BL + th - m
    yy = y0
    first = True
    while yy < fy - 12:
        if first:
            a.append(beam(BL + m, yy, BL + tw - m, point_at='start', r=0.55))
            first = False
        else:
            a.append(hairline(BL + m, yy, BL + tw - m, yy))
        yy = round(yy + pitch, 1)
    a.append(text(BL + m, fy - 1.2, 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  +91 7827051270  ·  sanzeed@gmail.com', 6.5, fill=C['umber']))
    a.append(text(BL + tw - m, fy - 1.2, 'sanzeed.com', 6.5, fill=C['umber'], anchor='end'))
    paper = rect(0, 0, W, H, fill=C['paper'])
    return svg_doc(W, H, paper, '\n'.join(a), guides(tw, th, BL, m, label=True), title=f'Sanzeed notepad — {key.upper()} sheet',
                   desc=f'Ruled sheet: hairlines every {pitch:g} mm (the beams), first beam with the point; lockup {lw} mm; margins {m} mm. Paper tone #FBF8F2 (omit when printing on natural-white stock).')


tmpd = tempfile.mkdtemp()
for key, (tw, th, m, lw, pitch) in SIZES.items():
    svg = write(f'{SRC}/sanzeed-notepad--{key}.svg', sheet(key, tw, th, m, lw, pitch))
    bleed_pdf = f'{tmpd}/{key}-bleed.pdf'
    svg_to_pdf(svg, bleed_pdf)
    crop_pdf(bleed_pdf, f'{D}/sanzeed-notepad--{key}.pdf', BL)
    print_ready(bleed_pdf, f'{D}/sanzeed-notepad--{key}--print-cmyk.pdf', tw, th, BL)
    pdf_to_png(f'{D}/sanzeed-notepad--{key}.pdf', f'{D}/sanzeed-notepad--{key}.png', dpi=150)
    print(key, pdfinfo(f'{D}/sanzeed-notepad--{key}.pdf').split('Page size:')[1].split('\n')[0].strip())
print('notepad done')
