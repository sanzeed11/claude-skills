#!/usr/bin/env python3
"""A4 presentation folder — flat dieline (back panel · 5 mm spine · front panel, one pocket with a glue tab and
business-card slits). Printed 4/0 outside on Gallery Black; the pocket's visible face is the printed face,
so its artwork is rotated 180° on the flat sheet."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *

D = f'{OUT}/Folder'
SRC = f'{D}/src'
os.makedirs(SRC, exist_ok=True)
BL = 3
PW, PH, SP, PK, TAB = 220, 305, 5, 90, 12  # panel w/h, spine, pocket height, glue tab
TW = TAB + PW + SP + PW   # 457 cut width
TH = PH + PK              # 395 cut height
W, H = TW + 2 * BL, TH + 2 * BL
x0, y0 = BL, BL          # cut origin
xb = x0 + TAB            # back panel left
xs = xb + PW             # spine left
xf = xs + SP             # front panel left
yp = y0 + PH             # pocket fold line

# ---------------- artwork (outside, printed face)
art = []
art.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{C["black"]}" />')
# lamp behind the wordmark on the front panel
art.append(f'<rect x="{xf - 10}" y="{y0 - BL}" width="{PW + 20}" height="{PH + BL}" fill="url(#lamp)" />')
lw = 120
g, lh, cap = logo('primary-wordmark', 'full-colour-dark', lw, xf + (PW - lw) / 2, y0 + (PH - logo_size('primary-wordmark', lw)[0]) / 2 - 8, 'wm')
art.append(g)
art.append(text(xf + PW / 2, y0 + PH / 2 + 22, 'Experiential Design Consultant', 8, fam='heading', weight=600, fill=C['silver'], ls=0.12, upper=True, anchor='middle'))
# back panel: symbol small + contact at the bottom (outside back)
g2, sh, _ = logo('symbol', 'full-colour-dark', 10, xb + 20, y0 + PH - 20 - logo_size('symbol', 10)[0], 'sym')
art.append(g2)
art.append(text(xb + PW - 20, y0 + PH - 24.5, 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  New Delhi, India', 7.5, fill=C['silver'], anchor='end'))
art.append(text(xb + PW - 20, y0 + PH - 20.5, '+91 7827051270  ·  sanzeed@gmail.com  ·  sanzeed.com  ·  linkedin.com/in/sanzeed', 7.5, fill=C['silver'], anchor='end'))
# spine: nothing (5 mm) — keep clean
# pocket (under the back panel): master line, rotated 180° so it reads when folded up inside
pcx, pcy = xb + PW / 2, yp + PK / 2
art.append(f'<g transform="rotate(180 {pcx:.3f} {pcy:.3f})">')
art.append(text_point(pcx, pcy + 3, MASTER, 16, C['lamp'], fill=C['gwhite'], anchor='middle', opsz=72))
art.append('</g>')
defs = lamp_defs('lamp', '50%', '46%', '60%', 0.38)

# ---------------- dieline layer (separate layer, spot colour, not for printing)
CUT, FOLD, GLUE = '#FF00FF', '#0066FF', '#2E6E48'
dl = []
# outer cut path: panels + pocket (pocket only under the back panel, with the glue tab on the outer edge)
ch = 8  # chamfer on pocket outer top corner
cut = (f'M{xb} {y0} L{xf + PW} {y0} L{xf + PW} {y0 + PH} L{xb} {y0 + PH} '
       f'L{xb} {yp + PK} L{x0} {yp + PK} L{x0} {yp + ch} L{x0 + ch} {yp} L{xb} {yp} Z')
# correction: pocket spans the back panel width; tab is left of it; make the path explicit
cut = (f'M{xb} {y0} L{xf + PW} {y0} L{xf + PW} {y0 + PH} L{xs + SP} {y0 + PH} L{xs} {y0 + PH} L{xb} {y0 + PH} '
       f'L{xb + PW} {y0 + PH} L{xb + PW} {yp + PK} L{x0} {yp + PK} L{x0} {yp + ch} L{x0 + ch} {yp} L{xb} {yp} Z')
# simpler, unambiguous outline (clockwise): top edge → right edge → bottom of front panel → spine/back bottom
# → pocket right edge down → pocket bottom (incl. tab) → tab left edge up → chamfer → back to the fold.
cut = (f'M{xb} {y0} H{xf + PW} V{y0 + PH} H{xb + PW} V{yp + PK} H{x0} V{yp + ch} L{x0 + ch} {yp} H{xb} Z')
dl.append(f'<path d="{cut}" fill="none" stroke="{CUT}" stroke-width="0.25" />')
# fold lines: spine (2), pocket fold, tab fold
for x in (xs, xs + SP):
    dl.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0 + PH}" stroke="{FOLD}" stroke-width="0.25" stroke-dasharray="3 1.5" />')
dl.append(f'<line x1="{xb}" y1="{yp}" x2="{xb + PW}" y2="{yp}" stroke="{FOLD}" stroke-width="0.25" stroke-dasharray="3 1.5" />')
dl.append(f'<line x1="{xb}" y1="{yp}" x2="{xb}" y2="{yp + PK}" stroke="{FOLD}" stroke-width="0.25" stroke-dasharray="3 1.5" />')
# glue area on the tab
dl.append(rect(x0 + 1, yp + ch + 1, TAB - 2, PK - ch - 2, fill=GLUE, extra='fill-opacity="0.18"'))
dl.append(text(x0 + TAB / 2, yp + PK / 2, 'GLUE', 5, fam='heading', weight=600, fill=GLUE, anchor='middle', extra=f'transform="rotate(-90 {x0 + TAB / 2} {yp + PK / 2})"'))
# business-card slits on the pocket (card 89 × 51, centred horizontally; slits 20 mm, 1 mm outside the card edges)
cw, chh = 89, 51
cx = xb + (PW - cw) / 2; cy = yp + (PK - chh) / 2
dl.append(rect(cx, cy, cw, chh, stroke='#808086', sw=0.2, extra='stroke-dasharray="1 1"'))
for sx in (cx - 1, cx + cw + 1):
    dl.append(f'<line x1="{sx}" y1="{cy + chh / 2 - 12}" x2="{sx}" y2="{cy + chh / 2 + 12}" stroke="{CUT}" stroke-width="0.35" />')
# labels (die key)
key_y = y0 + 6
dl.append(text(x0 + 2, y0 - 0.8, f'FOLDER DIELINE · cut size {TW} × {TH} mm · panels {PW} × {PH} · spine {SP} · pocket {PK} high · glue tab {TAB} · bleed {BL} · magenta = cut, blue dashed = crease, green = glue', 5, fam='heading', weight=500, fill=CUT))
for lbl, x in (('BACK COVER (outside)', xb + PW / 2), ('FRONT COVER (outside)', xf + PW / 2)):
    dl.append(text(x, y0 + 8, lbl, 6, fam='heading', weight=600, fill=CUT, anchor='middle', ls=0.1))
dl.append(text(xb + PW / 2, yp + PK - 3, 'POCKET — folds up inside the back cover; artwork rotated 180° · card slits for 89 × 51 mm', 5, fam='heading', weight=600, fill=CUT, anchor='middle', ls=0.06))

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}" version="1.1">
  <title>Sanzeed A4 presentation folder — flat dieline and outside artwork</title>
  <desc>Cut size {TW} × {TH} mm (+3 mm bleed). Layers: artwork (print), dieline (separate — supply as a spot/non-printing layer), guides. 1 unit = 1 mm.</desc>
  <defs>{defs}</defs>
  <g inkscape:groupmode="layer" inkscape:label="artwork" id="layer-artwork">
{chr(10).join(art)}
  </g>
<!--DIELINE-->
  <g inkscape:groupmode="layer" inkscape:label="dieline (spot — do not print)" id="layer-dieline">
{chr(10).join(dl)}
  </g>
<!--/DIELINE-->
<!--GUIDES-->
  <g inkscape:groupmode="layer" inkscape:label="guides (non-printing)" id="layer-guides">
{guides(TW, TH, BL, 15, label=False)}
  </g>
<!--/GUIDES-->
</svg>
'''
SVG = write(f'{SRC}/sanzeed-folder--a4-dieline.svg', svg)

# exports: artwork-only print PDF, dieline-only PDF, combined preview PNG
tmpd = tempfile.mkdtemp()
s = open(SVG).read()
art_only = re.sub(r'<!--DIELINE-->.*?<!--/DIELINE-->', '', s, flags=re.S)
die_only = re.sub(r'<g inkscape:groupmode="layer" inkscape:label="artwork".*?</g>\n<!--DIELINE-->', '<!--DIELINE-->', s, flags=re.S)
write(f'{tmpd}/art.svg', art_only); write(f'{tmpd}/die.svg', die_only)
svg_to_pdf(f'{tmpd}/art.svg', f'{tmpd}/art-bleed.pdf')
crop_pdf(f'{tmpd}/art-bleed.pdf', f'{D}/sanzeed-folder--a4-outside.pdf', BL)
print_ready(f'{tmpd}/art-bleed.pdf', f'{D}/sanzeed-folder--a4--print-cmyk.pdf', TW, TH, BL)
svg_to_pdf(f'{tmpd}/die.svg', f'{D}/sanzeed-folder--a4-dieline.pdf')
svg_to_png(SVG, f'{D}/sanzeed-folder--a4-flat-with-dieline.png', width_px=2400, keep_guides=False)
pdf_to_png(f'{D}/sanzeed-folder--a4-outside.pdf', f'{D}/sanzeed-folder--a4-outside.png', dpi=100)
print('folder done', pdfinfo(f'{D}/sanzeed-folder--a4-outside.pdf').split('Page size:')[1].split('\n')[0].strip())
