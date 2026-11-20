#!/usr/bin/env python3
"""ID card — CR80 portrait 54 × 85.6 mm (+3 mm bleed). Front: portrait photo plate, name, descriptor, symbol.
Back: monogram, contact, QR to sanzeed.com (qrcode module) on a Paper tile. Plus a 20 × 900 mm lanyard strip."""
import base64, io, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from PIL import Image

D = f'{OUT}/ID_Card'
SRC = f'{D}/src'
AS = f'{SRC}/assets'
os.makedirs(AS, exist_ok=True)
BL, SAFE = 3, 4
TW, TH = 54, 85.6
W, H = TW + 2 * BL, TH + 2 * BL
R = 3.18  # CR80 corner radius

# portrait 4:5, 1000 px high, JPG q88 — embedded as base64 so the SVG master is self-contained
im = Image.open(f'{IMG_DIR}/portrait.webp').convert('RGB')
w0, h0 = im.size
nh = int(w0 * 5 / 4)
y0 = max(0, int((h0 - nh) * 0.35))
im = im.crop((0, y0, w0, y0 + nh)).resize((800, 1000), Image.LANCZOS)
im.save(f'{AS}/sanzeed-portrait--4x5.jpg', quality=88, subsampling=0)
buf = io.BytesIO(); im.save(buf, format='JPEG', quality=88, subsampling=0)
PORTRAIT_B64 = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

# ------------------------------------------------------------------ front
pw, ph = 40, 50
px, py = BL + (TW - pw) / 2, BL + 7
front = []
front.append(f'<clipPath id="plate"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="4" /></clipPath>')
front.append(f'<image x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#plate)" xlink:href="{PORTRAIT_B64}" />')
front.append(rect(px, py, pw, ph, stroke='#FFFFFF', sw=0.15, rx=4, extra='stroke-opacity="0.10"'))
front.append(text(BL + 7, BL + 66.5, 'Sanzeed Mirza', 12, fam='display', weight=300, fill=C['gwhite'], opsz=36))
front.append(eyebrow(BL + 7, BL + 71.3, 'Experiential Design Consultant', pt=5.2, fill=C['silver']))
g, sh, cap = logo('symbol', 'full-colour-dark', 7, BL + 7, BL + TH - 7 - logo_size('symbol', 7)[0], 'sym')
front.append(g)
front.append(text(BL + TW - 7, BL + TH - 7.6, 'New Delhi  ·  sanzeed.com', 6, fill=C['silver'], anchor='end'))
paper_dark = rect(0, 0, W, H, fill=C['night'])
gd = guides(TW, TH, BL, SAFE, label=False) + rect(BL, BL, TW, TH, stroke='#2F62A0', sw=0.12, rx=R) + text(BL + 1, BL + TH - 1, 'CR80 54 × 85.6 · r 3.18 · bleed 3 · safe 4', 3.4, fam='heading', weight=500, fill='#2F62A0')
FRONT = write(f'{SRC}/sanzeed-id-card--front.svg', svg_doc(W, H, paper_dark, '\n'.join(front), gd, title='Sanzeed ID card — front',
              desc='Portrait plate (the room), name in Fraunces, descriptor eyebrow, symbol bottom-left. Night background.'))

# ------------------------------------------------------------------ back
back = []
mw = 16
g, mh, cap = logo('monogram', 'full-colour-dark', mw, BL + (TW - mw) / 2, BL + 9, 'mono')
back.append(g)
back.append(hairline(BL + 7, BL + 22, BL + TW - 7, BL + 22, dark=True))
lines_ = ['Sanzeed Mirza', 'Experiential Design Consultant', '+91 7827051270', 'sanzeed@gmail.com', 'linkedin.com/in/sanzeed', 'New Delhi, India']
for i, l in enumerate(lines_):
    back.append(text(BL + TW / 2, BL + 28 + i * 3.9, l, 6.2 if i else 7.5, fam='heading' if i == 0 else 'text', weight=600 if i == 0 else 400,
                     fill=C['gwhite'] if i == 0 else C['silver'], anchor='middle'))
# QR tile — Paper tile with Soot modules so it scans on the dark card
qs = 22
qx, qy = BL + (TW - qs) / 2, BL + TH - 7 - qs - 4
back.append(rect(qx - 2, qy - 2, qs + 4, qs + 4, fill=C['paper'], rx=2.5))
d, n = qr_path('https://sanzeed.com', qs, qx, qy, ec='M')
back.append(f'<path d="{d}" fill="{C["soot"]}" />')
back.append(text(BL + TW / 2, BL + TH - 4.2, 'sanzeed.com', 6, fam='heading', weight=600, fill=C['silver'], anchor='middle', ls=0.08, upper=True))
BACK = write(f'{SRC}/sanzeed-id-card--back.svg', svg_doc(W, H, paper_dark, '\n'.join(back), gd, title='Sanzeed ID card — back',
             desc=f'Monogram SM., contact lines, QR code ({n}×{n} modules, EC level M) to https://sanzeed.com on a Paper tile.'))

# ------------------------------------------------------------------ lanyard strip 20 × 900 mm (print both faces), repeat of the wordmark
LW, LH = 900, 20
lan = [rect(0, 0, LW + 2 * BL, LH + 2 * BL, fill=C['black'])]
step = 110
x = BL + 15
while x + 60 < LW + BL:
    g, h_, cap = logo('primary-wordmark', 'white', 60, x, BL + (LH - logo_size('primary-wordmark', 60)[0]) / 2, f'wm{int(x)}')
    lan.append(g)
    lan.append(point(x + 85, BL + LH / 2, 0.9, dark=True))
    x += step
LAN = write(f'{SRC}/sanzeed-lanyard--strip.svg', svg_doc(LW + 2 * BL, LH + 2 * BL, lan[0], '\n'.join(lan[1:]), guides(LW, LH, BL, 3, label=False),
            title='Sanzeed lanyard — 20 mm strip artwork', desc='Repeat: white wordmark 60 mm + gold point, pitch 110 mm, on Gallery Black. Woven or dye-sublimation; supply as print PDF.'))

# ------------------------------------------------------------------ exports
tmpd = tempfile.mkdtemp()
pages = []
for side, svg in (('front', FRONT), ('back', BACK)):
    pdf = f'{tmpd}/{side}.pdf'; svg_to_pdf(svg, pdf); pages.append(pdf)
bleed_pdf = f'{tmpd}/card-bleed.pdf'; merge_pdfs(pages, bleed_pdf)
crop_pdf(bleed_pdf, f'{D}/sanzeed-id-card.pdf', BL)
print_ready(bleed_pdf, f'{D}/sanzeed-id-card--print-cmyk.pdf', TW, TH, BL)
for i, side in enumerate(('front', 'back'), 1):
    pdf_to_png(f'{D}/sanzeed-id-card.pdf', f'{D}/sanzeed-id-card--{side}.png', dpi=300, page=i)
lan_bleed = f'{tmpd}/lanyard-bleed.pdf'; svg_to_pdf(LAN, lan_bleed)
crop_pdf(lan_bleed, f'{D}/sanzeed-lanyard--strip.pdf', BL)
print_ready(lan_bleed, f'{D}/sanzeed-lanyard--strip--print-cmyk.pdf', LW, LH, BL)
pdf_to_png(f'{D}/sanzeed-lanyard--strip.pdf', f'{D}/sanzeed-lanyard--strip.png', dpi=72)
print('id card', pdfinfo(f'{D}/sanzeed-id-card.pdf').split('Page size:')[1].split('\n')[0].strip(), '| lanyard', pdfinfo(f'{D}/sanzeed-lanyard--strip.pdf').split('Page size:')[1].split('\n')[0].strip())
print('id card done')
