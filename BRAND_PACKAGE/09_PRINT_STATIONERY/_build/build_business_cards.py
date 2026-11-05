#!/usr/bin/env python3
"""Business cards — two concepts, 89×51 mm trim + 3 mm bleed (95×57 page)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *

D = f'{OUT}/Business_Cards'
SRC = f'{D}/src'
os.makedirs(SRC, exist_ok=True)
TW, TH, BL, SAFE = 89, 51, 3, 4
W, H = TW + 2 * BL, TH + 2 * BL
G = guides(TW, TH, BL, SAFE)


def paper(fill):
    return rect(0, 0, W, H, fill=fill)


def back_plaster(prefix):
    """Shared back: name, descriptor, contacts, master line with the single gold point."""
    x = BL + 8  # 11 mm from trim edge
    a = []
    a.append(text(x, BL + 14.5, CONTACT['name'], 12, fam='display', weight=300, fill=C['soot']))
    a.append(eyebrow(x, BL + 19.6, CONTACT['descriptor'], pt=5.6, fill=C['umber']))
    a.append(hairline(x, BL + 23.5, BL + TW - 8, BL + 23.5))
    a.append(lines(x, BL + 29.2, [f"{CONTACT['phone']}  ·  {CONTACT['email']}",
                                 f"{CONTACT['web']}  ·  {CONTACT['linkedin']}"], 7, 4.0, fill=C['soot']))
    a.append(text(x, BL + 37.2, CONTACT['city'], 7, fill=C['umber']))
    a.append(text_point(x, BL + 45.2, MASTER, 9.5, C['oldgold'], fill=C['soot'], opsz=36))
    return '\n'.join(a)


# Concept A — Plaster both sides. Front: horizontal-descriptor lockup, centred.
lw = 54
g, lh, cap = logo('horizontal-descriptor', 'full-colour-light', lw, BL + (TW - lw) / 2, BL + (TH - 11.2) / 2 - 0.3, 'lockup')
a_front = svg_doc(W, H, paper(C['plaster']), g, G, title='Sanzeed business card — concept A, front',
                  desc='Horizontal-descriptor lockup (full-colour-light) on Plaster, centred. Clear space = ½ cap height (3.8 mm) all round.')
a_back = svg_doc(W, H, paper(C['plaster']), back_plaster('a'), G, title='Sanzeed business card — concept A, back',
                 desc='Name, descriptor, contacts and the master line ending on the gold point.')

# Concept B — dark front with the primary wordmark and a lamp glow; Plaster back.
lw2 = 46
gw, lh2, cap2 = logo('primary-wordmark', 'full-colour-dark', lw2, BL + (TW - lw2) / 2, BL + (TH - lw2 * 500 / 3590) / 2, 'wm')
b_front_art = (f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#lamp)" />\n' + gw)
b_front = svg_doc(W, H, paper(C['black']), b_front_art, G, defs=lamp_defs('lamp', '50%', '50%', '58%', 0.34),
                  title='Sanzeed business card — concept B, front',
                  desc='Primary wordmark (full-colour-dark) on Gallery Black with the lamp glow. Clear space = ½ cap height (3.2 mm).')
b_back = svg_doc(W, H, paper(C['plaster']), back_plaster('b'), G, title='Sanzeed business card — concept B, back',
                 desc='Name, descriptor, contacts and the master line ending on the gold point.')

files = {
    'a-front': a_front, 'a-back': a_back, 'b-front': b_front, 'b-back': b_back,
}
for k, s in files.items():
    write(f'{SRC}/sanzeed-business-card--{k}.svg', s)

# exports
tmpd = tempfile.mkdtemp()
for concept in ('a', 'b'):
    pages = []
    for side in ('front', 'back'):
        svg = f'{SRC}/sanzeed-business-card--{concept}-{side}.svg'
        pdf = f'{tmpd}/{concept}-{side}.pdf'
        svg_to_pdf(svg, pdf)
        pages.append(pdf)
    bleed_pdf = f'{tmpd}/{concept}-bleed.pdf'
    merge_pdfs(pages, bleed_pdf)
    crop_pdf(bleed_pdf, f'{D}/sanzeed-business-card--concept-{concept}.pdf', BL)
    print_ready(bleed_pdf, f'{D}/sanzeed-business-card--concept-{concept}--print-cmyk.pdf', TW, TH, BL)
    for i, side in enumerate(('front', 'back'), 1):
        pdf_to_png(f'{D}/sanzeed-business-card--concept-{concept}.pdf', f'{D}/sanzeed-business-card--{concept}-{side}-2x.png', dpi=300, page=i)
print('business cards done')
