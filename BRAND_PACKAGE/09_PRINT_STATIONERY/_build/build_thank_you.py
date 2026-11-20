#!/usr/bin/env python3
"""Thank-you cards — A6 folded (A5 flat 210 × 148, fold on the short axis) and a flat A6 postcard (148 × 105).
Outside: 'Thank you.' in Fraunces with the point. Inside: signature mark left, hairline right."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *

D = f'{OUT}/Thank_You_Cards'
SRC = f'{D}/src'
os.makedirs(SRC, exist_ok=True)
BL, SAFE = 3, 6
FW, FH = 210, 148      # folded card flat (A5 landscape); fold at x = 105
PW, PH = 148, 105      # postcard A6 landscape


def fold_guides(tw, th):
    g = guides(tw, th, BL, SAFE, label=True)
    g += f'<line x1="{BL + tw / 2}" y1="{BL - 2}" x2="{BL + tw / 2}" y2="{BL + th + 2}" stroke="#0066FF" stroke-width="0.15" stroke-dasharray="2 1" />'
    g += text(BL + tw / 2 + 1.5, BL + 4, 'FOLD', 4, fam='heading', weight=600, fill='#0066FF')
    return g


paper = rect(0, 0, FW + 2 * BL, FH + 2 * BL, fill=C['plaster'])
# outside: back (left half) · front (right half)
out = []
fx = BL + FW / 2  # front panel left edge
out.append(text_point(fx + FW / 4, BL + FH / 2 + 4, 'Thank you', 36, C['oldgold'], fill=C['soot'], anchor='middle', opsz=144))
g, sh, cap = logo('symbol', 'full-colour-light', 7, BL + FW / 4 - 3.5, BL + FH - SAFE - 10 - logo_size('symbol', 7)[0], 'sym')
out.append(g)
out.append(text(BL + FW / 4, BL + FH - SAFE - 4, 'sanzeed.com', 6.5, fill=C['umber'], anchor='middle'))
OUT_SVG = write(f'{SRC}/sanzeed-thank-you-card--folded-outside.svg', svg_doc(FW + 2 * BL, FH + 2 * BL, paper, '\n'.join(out), fold_guides(FW, FH),
                title='Sanzeed thank-you card — folded, outside (back · front)', desc='Front: "Thank you." Fraunces Light 36 pt with the gold point. Back: symbol and sanzeed.com.'))
# inside: left page signature mark · right page blank with a hairline
ins = []
sg, sh2 = signature('ink', 40, BL + FW / 4 - 20, BL + FH * 0.56, 'sig')
ins.append(sg)
ins.append(text(BL + FW / 4, BL + FH * 0.56 + sh2 + 8, 'Sanzeed Mirza  ·  Experiential Design Consultant', 6.5, fill=C['umber'], anchor='middle'))
ins.append(hairline(fx + SAFE + 8, BL + SAFE + 14, BL + FW - SAFE - 8, BL + SAFE + 14))
IN_SVG = write(f'{SRC}/sanzeed-thank-you-card--folded-inside.svg', svg_doc(FW + 2 * BL, FH + 2 * BL, paper, '\n'.join(ins), fold_guides(FW, FH),
               title='Sanzeed thank-you card — folded, inside (left · right)', desc='Left page: signature mark 40 mm. Right page: blank, one hairline for the hand-written note.'))

# postcard A6 — front and back
pp = rect(0, 0, PW + 2 * BL, PH + 2 * BL, fill=C['plaster'])
pf = [text_point(BL + PW / 2, BL + PH / 2 + 4, 'Thank you', 34, C['oldgold'], fill=C['soot'], anchor='middle', opsz=72)]
PF_SVG = write(f'{SRC}/sanzeed-thank-you-postcard--front.svg', svg_doc(PW + 2 * BL, PH + 2 * BL, pp, '\n'.join(pf), guides(PW, PH, BL, SAFE),
               title='Sanzeed thank-you postcard — front', desc='"Thank you." Fraunces Light 34 pt with the gold point, centred.'))
pb = []
mid = BL + PW * 0.54
pb.append(hairline(mid, BL + SAFE + 4, mid, BL + PH - SAFE - 4))
for i in range(4):
    pb.append(hairline(mid + 8, BL + PH * 0.46 + i * 8, BL + PW - SAFE - 2, BL + PH * 0.46 + i * 8))
pb.append(rect(BL + PW - SAFE - 2 - 20, BL + SAFE + 2, 20, 24, stroke='#1A1816', sw=0.12, rx=1, extra='stroke-opacity="0.25" stroke-dasharray="1 1"'))
sg, sh3 = signature('ink', 34, BL + SAFE + 6, BL + 16, 'sig2')
pb.append(sg)
pb.append(text(BL + SAFE + 6, BL + 16 + sh3 + 8, 'Sanzeed Mirza', 7.5, fam='heading', weight=600, fill=C['soot']))
pb.append(text(BL + SAFE + 6, BL + 16 + sh3 + 12, 'Experiential Design Consultant', 6.5, fill=C['umber']))
pb.append(text(BL + SAFE + 6, BL + 16 + sh3 + 16, '+91 7827051270  ·  sanzeed@gmail.com', 6.5, fill=C['umber']))
pb.append(text(BL + SAFE + 6, BL + 16 + sh3 + 20, 'sanzeed.com  ·  New Delhi, India', 6.5, fill=C['umber']))
g, sh, cap = logo('symbol', 'full-colour-light', 6, BL + SAFE + 6, BL + PH - SAFE - logo_size('symbol', 6)[0] - 2, 'sym3')
pb.append(g)
PB_SVG = write(f'{SRC}/sanzeed-thank-you-postcard--back.svg', svg_doc(PW + 2 * BL, PH + 2 * BL, pp, '\n'.join(pb), guides(PW, PH, BL, SAFE),
               title='Sanzeed thank-you postcard — back', desc='Postal layout: divider, address lines, stamp box; signature mark and contact on the left.'))

# exports
tmpd = tempfile.mkdtemp()
for name, svgs, tw, th in (('folded', (OUT_SVG, IN_SVG), FW, FH), ('postcard', (PF_SVG, PB_SVG), PW, PH)):
    pages = []
    for i, s in enumerate(svgs):
        p = f'{tmpd}/{name}-{i}.pdf'; svg_to_pdf(s, p); pages.append(p)
    bleed_pdf = f'{tmpd}/{name}-bleed.pdf'; merge_pdfs(pages, bleed_pdf)
    out_pdf = f'{D}/sanzeed-thank-you-card--{name}.pdf'
    crop_pdf(bleed_pdf, out_pdf, BL)
    print_ready(bleed_pdf, f'{D}/sanzeed-thank-you-card--{name}--print-cmyk.pdf', tw, th, BL)
    labels = ('outside', 'inside') if name == 'folded' else ('front', 'back')
    for i, lb in enumerate(labels, 1):
        pdf_to_png(out_pdf, f'{D}/sanzeed-thank-you-card--{name}-{lb}.png', dpi=200, page=i)
    print(name, pdfinfo(out_pdf).split('Page size:')[1].split('\n')[0].strip())
print('thank-you done')
