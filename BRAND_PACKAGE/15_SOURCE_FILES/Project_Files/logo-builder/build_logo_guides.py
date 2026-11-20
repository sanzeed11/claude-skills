#!/usr/bin/env python3
"""Generate the logo guideline diagrams (clear space, minimum sizes, incorrect usage, construction, placement)
   into 02_LOGO_SYSTEM/Guidelines as SVG + PNG. Re-run after changing build_logo.py."""
import os, re, sys, math, cairosvg
B = '/home/user/claude-skills/BRAND_PACKAGE'
SVGD = f'{B}/02_LOGO_SYSTEM/SVG'; OUT = f'{B}/02_LOGO_SYSTEM/Guidelines'; os.makedirs(OUT, exist_ok=True)
PHOTO = f'{OUT}/_photo-ram-katha-show.jpg'
FONT = "Inter, 'Inter Tight', Arial, sans-serif"; SERIF = "Fraunces, Georgia, serif"

def inner(svgfile):
    s = open(svgfile).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    m = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S); body = m.group(1)
    body = re.sub(r'<title>.*?</title>|<desc>.*?</desc>', '', body, flags=re.S)
    return body, vb[2], vb[3]

def place(svgfile, x, y, w, extra=''):
    body, vw, vh = inner(svgfile); s = w / vw
    return f'<g transform="translate({x} {y}) scale({s})" {extra}>{body}</g>', vh * s

def save(name, svg, width=2000):
    p = f'{OUT}/{name}.svg'; open(p, 'w').write(svg); cairosvg.svg2png(url=p, write_to=f'{OUT}/{name}.png', output_width=width, unsafe=True); print('wrote', name)

def frame(W, H, bg, title, sub, content):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<text x="80" y="100" font-family="{SERIF}" font-weight="300" font-size="54" fill="{"#F5F5F7" if bg!="#F5F0E7" else "#1A1816"}">{title}</text>'
            f'<text x="80" y="140" font-family="{FONT}" font-size="20" fill="{"#A1A1A6" if bg!="#F5F0E7" else "#665F55"}">{sub}</text>{content}</svg>')

# 1 — clear space (x = ½ cap height) for primary, horizontal-descriptor, vertical and symbol
def clear_space():
    W, H = 2400, 1500; c = ''
    specs = [('sanzeed-primary-wordmark--full-colour-dark.svg', 180, 330, 1200), ('sanzeed-symbol--full-colour-dark.svg', 1800, 300, 260),
             ('sanzeed-horizontal-descriptor--full-colour-dark.svg', 180, 820, 950), ('sanzeed-vertical-stacked--full-colour-dark.svg', 1560, 760, 520)]
    for f, x, y, w in specs:
        body, vw, vh = inner(f'{SVGD}/{f}'); s = w / vw; h = vh * s
        cap = 500 * s if 'vertical' not in f else 500 * s   # cap height of the wordmark in the lockup
        xx = cap / 2
        if 'symbol' in f: xx = h / 4
        c += f'<rect x="{x-xx}" y="{y-xx}" width="{w+2*xx}" height="{h+2*xx}" fill="none" stroke="#E9B25A" stroke-width="2" stroke-dasharray="10 8"/>'
        c += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="rgba(245,245,247,.35)" stroke-width="1.5"/>'
        # x boxes in the corners
        for (bx, by) in [(x-xx, y-xx), (x+w, y-xx), (x-xx, y+h), (x+w, y+h)]:
            c += f'<rect x="{bx}" y="{by}" width="{xx}" height="{xx}" fill="rgba(233,178,90,.18)" stroke="#E9B25A" stroke-width="1"/>'
            c += f'<text x="{bx+xx/2}" y="{by+xx/2+8}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="{max(18, xx*0.45)}" fill="#E9B25A">x</text>'
        c += place(f'{SVGD}/{f}', x, y, w)[0]
    c += f'<text x="80" y="1420" font-family="{FONT}" font-size="22" fill="#A1A1A6">x = ½ the cap height of the wordmark in use (for the symbol on its own, ¼ of its height). Nothing may enter the dashed zone: no text, edges, other marks or photography detail.</text>'
    save('logo-clear-space', frame(W, H, '#0D0D0F', 'Clear space', 'Minimum exclusion zone around every lockup', c))

# 2 — minimum sizes at true pixel size (render PNG at 1× width = viewBox width)
def min_sizes():
    W, H = 1400, 1000; c = ''; y = 200
    rows = [('sanzeed-primary-wordmark--full-colour-dark.svg', 120, 'Primary wordmark — minimum 120 px / 28 mm'),
            ('sanzeed-simplified-small-size--full-colour-dark.svg', 120, 'Simplified wordmark — use from 120 px down to 24 px (shown at 120 px)'),
            ('sanzeed-simplified-small-size--full-colour-dark.svg', 60, 'Simplified wordmark at 60 px'),
            ('sanzeed-horizontal-descriptor--full-colour-dark.svg', 220, 'Horizontal lockup with descriptor — minimum 220 px / 50 mm'),
            ('sanzeed-vertical-stacked--full-colour-dark.svg', 90, 'Vertical stack — minimum 90 px / 22 mm wide'),
            ('sanzeed-symbol--full-colour-dark.svg', 16, 'Symbol — minimum 16 px / 6 mm (favicon)'),
            ('sanzeed-symbol-small-size--full-colour-dark.svg', 16, 'Small-size symbol at 16 px (heavier stroke)'),
            ('sanzeed-symbol-tile--dark.svg', 32, 'Symbol tile at 32 px')]
    for f, w, lab in rows:
        g, h = place(f'{SVGD}/{f}', 80, y, w); c += g
        c += f'<line x1="80" y1="{y+h+14}" x2="{80+w}" y2="{y+h+14}" stroke="#E9B25A" stroke-width="1"/>'
        c += f'<text x="{max(360, 80+w+40)}" y="{y+h/2+7}" font-family="{FONT}" font-size="20" fill="#F5F5F7">{lab}</text>'
        y += max(h, 30) + 56
    c += f'<text x="80" y="{H-50}" font-family="{FONT}" font-size="18" fill="#A1A1A6">This sheet is exported at 1:1 pixels (1400 px wide) so the marks appear at their true minimum sizes on a 1× screen.</text>'
    p = f'{OUT}/logo-minimum-sizes.svg'; open(p, 'w').write(frame(W, H, '#0D0D0F', 'Minimum sizes', 'Below these, switch to the simplified or small-size versions', c))
    cairosvg.svg2png(url=p, write_to=f'{OUT}/logo-minimum-sizes.png', output_width=W); cairosvg.svg2png(url=p, write_to=f'{OUT}/logo-minimum-sizes@2x.png', output_width=W*2); print('wrote min sizes')

# 3 — incorrect usage (12 tiles)
def incorrect():
    W, H = 2400, 2200; c = ''; tw, th = 700, 420; gx, gy = 80, 200
    wm = f'{SVGD}/sanzeed-primary-wordmark--full-colour-dark.svg'; wml = f'{SVGD}/sanzeed-primary-wordmark--full-colour-light.svg'
    tiles = []
    def tile(bg, content, label):
        tiles.append((bg, content, label))
    body0, vw0, vh0 = inner(wm); tiles.append(('#1C1C1E', f'<g transform="translate(60 120) scale({580/vw0},{580/vw0*1.7})">{body0}</g>', 'Do not stretch or squash'))
    g, h = place(wm, 0, 0, 500); tiles.append(('#1C1C1E', f'<g transform="translate(140 110) rotate(-12)">{g}</g>', 'Do not rotate'))
    body, vw, vh = inner(wm); ob = re.sub(r'fill="[^"]*"', 'fill="none"', body); tiles.append(('#1C1C1E', f'<g transform="translate(60 170) scale({580/vw})" fill="none" stroke="#F5F5F7" stroke-width="12">{ob}</g>', 'Do not outline'))
    tiles.append(('#1C1C1E', f'<defs><filter id="sh"><feDropShadow dx="0" dy="14" stdDeviation="10" flood-color="#000" flood-opacity=".9"/></filter></defs><g filter="url(#sh)">{place(wm,60,170,580)[0]}</g>', 'Do not add shadows, bevels or effects'))
    tiles.append(('#1C1C1E', place(wm, 60, 170, 580)[0].replace('#E9B25A', '#4A86C8'), 'Do not recolour the points of light'))
    tiles.append(('#1C1C1E', f'<text x="60" y="235" font-family="{FONT}" font-weight="700" font-size="92" fill="#F5F5F7" letter-spacing="2">SANZEED</text>', 'Do not typeset the name instead of the wordmark'))
    tiles.append(('#1C1C1E', place(wml, 60, 170, 580)[0], 'Do not use the light version on dark'))
    tiles.append(('#F5F0E7', place(wm, 60, 170, 580)[0], 'Do not use the dark version on light'))
    tiles.append(('photo', place(wm, 60, 170, 580)[0], 'Do not place on busy photography without the veil'))
    tiles.append(('#B8863B', place(wm, 60, 170, 580)[0], 'Do not place the full-colour logo on gold'))
    tiles.append(('#1C1C1E', f'<defs><linearGradient id="gr" x1="0" x2="1"><stop offset="0" stop-color="#F4C97A"/><stop offset="1" stop-color="#4A86C8"/></linearGradient></defs><g style="fill:url(#gr)">{re.sub(r"fill=\"#F5F5F7\"", "", place(wm,60,170,580)[0])}</g>', 'Do not fill with gradients'))
    tiles.append(('#1C1C1E', f'<clipPath id="cp"><rect x="150" y="120" width="500" height="200"/></clipPath><g clip-path="url(#cp)">{place(wm,60,170,580)[0]}</g>', 'Do not crop the wordmark'))
    for i, (bg, content, label) in enumerate(tiles):
        r, col = divmod(i, 3); x = gx + col * (tw + 60); y = gy + r * (th + 60)
        fill = bg if bg != 'photo' else '#000'
        c += f'<g transform="translate({x} {y})"><rect width="{tw}" height="{th}" rx="24" fill="{fill}"/>'
        if bg == 'photo': c += f'<clipPath id="pc{i}"><rect width="{tw}" height="{th}" rx="24"/></clipPath><image xlink:href="{PHOTO}" x="0" y="0" width="{tw}" height="{th}" preserveAspectRatio="xMidYMid slice" clip-path="url(#pc{i})"/>'
        c += content
        c += f'<circle cx="{tw-44}" cy="44" r="22" fill="#D64540"/><path d="M{tw-52} 36l16 16M{tw-36} 36l-16 16" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
        c += f'<text x="24" y="{th-24}" font-family="{FONT}" font-size="20" fill="{"#F5F5F7" if bg in ("#1C1C1E","photo","#B8863B") else "#1A1816"}">{label}</text></g>'
    save('logo-incorrect-usage', frame(W, H, '#0D0D0F', 'Incorrect usage', 'Twelve things never to do with the logo', c), 2400)

# 4 — construction: the refined original wordmark on a grid, with its guides and the three points
def construction():
    import importlib.util
    spec = importlib.util.spec_from_file_location('blr', f'{B}/15_SOURCE_FILES/Project_Files/logo-builder/build_logo_refined.py'); blr = importlib.util.module_from_spec(spec); spec.loader.exec_module(blr)
    wm = blr.wordmark(); W, H = 2400, 1200; s = 2240 / wm['width']; ox, oy = 80, 380; h = wm['height']
    c = f'<defs><pattern id="g20" width="{20*s}" height="{20*s}" patternUnits="userSpaceOnUse" x="{ox}" y="{oy}"><path d="M{20*s} 0H0V{20*s}" fill="none" stroke="rgba(233,178,90,.18)"/></pattern></defs>'
    c += f'<rect x="{ox}" y="{oy}" width="2240" height="{h*s}" fill="url(#g20)"/>'
    c += f'<g transform="translate({ox} {oy}) scale({s})"><g fill="rgba(245,245,247,.9)">' + ''.join(f'<path d="{p}"/>' for _, p in wm['letters']) + '</g>'
    c += '<g fill="#E9B25A">' + ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>' for cx, cy, r in wm['dots']) + '</g>'
    for (cx, cy, r) in wm['dots']:
        c += f'<circle cx="{cx}" cy="{cy}" r="{r+14}" fill="none" stroke="#E9B25A" stroke-width="2" stroke-dasharray="6 6"/>'
    cap = 40 - blr.Y0; base = h - 1; mid = wm['dots'][2][1]
    for y in (cap, mid, base):
        c += f'<line x1="-40" y1="{y}" x2="{wm["width"]+40}" y2="{y}" stroke="#E9B25A" stroke-width="2" stroke-opacity="0.6"/>'
    c += '</g>'
    c += f'<g font-family="{FONT}" font-size="20" fill="#A1A1A6"><text x="80" y="{oy-60}">The refined original wordmark: the hand-drawn SANZEED from sanzeed.com, cleaned letter by letter (smooth edges, straight lines, exact E bars), with a new swooping Z.</text>'
    c += f'<text x="80" y="{oy+h*s+60}">Guides: cap line · point line (the Z and D points share one height) · baseline. Points r 45; each sits in a 14-unit clear ring (dashed). Stroke weight ≈ 64 throughout; the S overshoots the cap line as in the original.</text></g>'
    save('logo-construction', frame(W, H, '#0D0D0F', 'Construction', 'The refined original wordmark on a 20-unit grid', c), 2400)

# 5 — placement
def placement():
    W, H = 2400, 1300; c = ''
    pages = [(80, 200, 560, 790, 'A4 document: horizontal lockup top-left, 20 mm margins', 'sanzeed-horizontal-descriptor--full-colour-light.svg', '#FBF8F2', 'tl'),
             (720, 200, 1100, 620, '16:9 slide / cover: primary wordmark bottom-left or centred over the lamp', 'sanzeed-primary-wordmark--full-colour-dark.svg', '#0D0D0F', 'bl'),
             (1900, 200, 420, 420, 'Square: symbol tile or vertical stack centred', 'sanzeed-vertical-stacked--full-colour-dark.svg', '#0D0D0F', 'c')]
    for x, y, w, h, lab, f, bg, pos in pages:
        c += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="rgba(255,255,255,.12)"/>'
        m = w * 0.095
        if pos == 'tl': g, gh = place(f'{SVGD}/{f}', x+m, y+m, w*0.42)
        elif pos == 'bl':
            lw = w*0.3; body, vw, vh = inner(f'{SVGD}/{f}'); gh = vh*lw/vw; g, _ = place(f'{SVGD}/{f}', x+m, y+h-m-gh, lw)
            c += f'<ellipse cx="{x+w/2}" cy="{y+h*0.45}" rx="{w*0.28}" ry="{h*0.3}" fill="#E9B25A" opacity=".16"/>'
        else:
            lw = w*0.5; body, vw, vh = inner(f'{SVGD}/{f}'); gh = vh*lw/vw; g, _ = place(f'{SVGD}/{f}', x+(w-lw)/2, y+(h-gh)/2, lw)
        c += g
        if pos == 'tl':
            for yy in range(5): c += f'<rect x="{x+m}" y="{y+m+170+yy*34}" width="{w-2*m if yy else (w-2*m)*0.6}" height="10" rx="5" fill="#ECE7DC"/>'
            c += f'<line x1="{x+m}" y1="{y+h-m}" x2="{x+w-m}" y2="{y+h-m}" stroke="#B8863B" stroke-width="1"/><circle cx="{x+m}" cy="{y+h-m}" r="4" fill="#B8863B"/>'
        c += f'<text x="{x}" y="{y+h+40}" font-family="{FONT}" font-size="20" fill="#A1A1A6">{lab}</text>'
    c += f'<text x="80" y="{H-60}" font-family="{FONT}" font-size="20" fill="#A1A1A6">Placement: top-left for reading surfaces, bottom-left or centred for covers and screens. The logo never shares its edge with another logo; partner marks sit on the opposite side separated by a hairline and 2x clear space.</text>'
    save('logo-placement', frame(W, H, '#0D0D0F', 'Placement', 'Where the logo lives on the three basic formats', c), 2400)

from PIL import Image
Image.open(f'{B}/00_ORIGINAL_ASSETS_BACKUP/images/img/ram-katha-show.webp').convert('RGB').save(PHOTO, quality=88)
clear_space(); min_sizes(); incorrect(); construction(); placement()
