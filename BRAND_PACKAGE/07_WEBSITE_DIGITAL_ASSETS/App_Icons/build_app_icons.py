#!/usr/bin/env python3
"""build_app_icons.py — builds every app icon from the logo-system SVGs with cairosvg.
   iOS (square, no alpha), Android (rounded tile + maskable with 20 % safe padding), Windows tiles (transparent,
   symbol centred), PWA (rounded + maskable), Safari pinned tab (mono SVG copy). Run from this folder."""
import pathlib, shutil, cairosvg, re
from PIL import Image
HERE = pathlib.Path(__file__).parent; LOGO = HERE / '../../02_LOGO_SYSTEM'
SRC = HERE / 'src'; SRC.mkdir(exist_ok=True)
sq_svg   = (LOGO / 'SVG/sanzeed-symbol-tile-square--dark.svg').read_text()
tile_svg = (LOGO / 'SVG/sanzeed-symbol-tile--dark.svg').read_text()
sym_svg  = (LOGO / 'SVG/sanzeed-symbol--full-colour-dark.svg').read_text()
# the approved symbol: the refined (hooked, tapered) S + the point — unioned S path and the dot, box read from the viewBox
_sym = re.sub(r'\s+', ' ', sym_svg)
SW, SH = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', _sym).groups())   # ≈ 603.8 × 519.3
sym_path = re.search(r'<g id="symbol-ink"[^>]*>.*?<path[^>]*?\sd="([^"]+)"', _sym).group(1)
dot = re.search(r'<g id="symbol-dots"[^>]*>\s*(<circle[^>]*/>)', _sym).group(1)
def wrap(w, h, inner, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{rect}{inner}</svg>'
def symbol_at(x, y, s):  # symbol (SW×SH units) translated and scaled
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({s:.5f})"><path fill="#F5F5F7" d="{sym_path}"/><g fill="#E9B25A">{dot}</g></g>'
# maskable: full-bleed Night, symbol inside the centre 60 % (20 % padding on every side)
ms = 600 / max(SW, SH)
maskable = wrap(1000, 1000, symbol_at((1000 - SW * ms) / 2, (1000 - SH * ms) / 2, ms), bg='#0D0D0F')
# windows tiles: transparent, symbol ≈ 50 % of the short side
def tile(w, h):
    s = (min(w, h) * 0.5) / SW; sw, sh = SW * s, SH * s
    return wrap(w, h, symbol_at((w - sw) / 2, (h - sh) / 2, s))
(SRC / 'maskable-1000.svg').write_text(maskable)
for name, svg in [('ios-source', sq_svg), ('android-source', tile_svg)]: (SRC / f'{name}.svg').write_text(svg)
def png(svg, out, size, w=None, h=None, alpha=True):
    w = w or size; h = h or size
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out), output_width=w, output_height=h)
    if not alpha:
        im = Image.open(out).convert('RGBA'); bg = Image.new('RGB', im.size, '#0D0D0F'); bg.paste(im, mask=im.split()[3]); bg.save(out, optimize=True)
made = []
for s in (1024, 180, 167, 152, 120):
    out = HERE / f'iOS/ios-icon-{s}.png'; out.parent.mkdir(exist_ok=True); png(sq_svg, out, s, alpha=False); made.append(out)
shutil.copy(HERE / 'iOS/ios-icon-1024.png', HERE / 'iOS/ios-app-store-1024.png'); made.append(HERE / 'iOS/ios-app-store-1024.png')
for s in (48, 72, 96, 144, 192, 256, 384, 512):
    out = HERE / f'Android/android-icon-{s}.png'; out.parent.mkdir(exist_ok=True); png(tile_svg, out, s); made.append(out)
png(maskable, HERE / 'Android/android-maskable-512.png', 512); made.append(HERE / 'Android/android-maskable-512.png')
(HERE / 'Windows').mkdir(exist_ok=True)
for w, h in ((70, 70), (150, 150), (310, 310), (310, 150)):
    out = HERE / f'Windows/mstile-{w}x{h}.png'; png(tile(w, h), out, None, w, h); made.append(out)
(HERE / 'Windows/browserconfig.xml').write_text('''<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square70x70logo src="/mstile-70x70.png"/>
      <square150x150logo src="/mstile-150x150.png"/>
      <square310x310logo src="/mstile-310x310.png"/>
      <wide310x150logo src="/mstile-310x150.png"/>
      <TileColor>#0D0D0F</TileColor>
    </tile>
  </msapplication>
</browserconfig>
''')
(HERE / 'macOS').mkdir(exist_ok=True)   # copy of the logo system's pinned-tab SVG; a stale <desc> about the retired construction is dropped
(HERE / 'macOS/safari-pinned-tab.svg').write_text(re.sub(r'\s*<desc>[^<]*(?:500-unit|64-unit)[^<]*</desc>', '', (LOGO / 'Favicon/safari-pinned-tab.svg').read_text()))
(HERE / 'PWA').mkdir(exist_ok=True)
for s in (192, 512): png(tile_svg, HERE / f'PWA/pwa-icon-{s}.png', s)
png(maskable, HERE / 'PWA/pwa-maskable-512.png', 512)
(HERE / 'PWA/manifest.webmanifest').write_text('''{
  "name": "Sanzeed Mirza — Experiential Design Consultant",
  "short_name": "Sanzeed",
  "description": "Experiential design you can walk into.",
  "icons": [
    { "src": "/pwa-icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/pwa-icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/pwa-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "theme_color": "#0D0D0F",
  "background_color": "#0D0D0F",
  "display": "standalone",
  "start_url": "/"
}
''')
# preview sheet (dark and light ground, with the maskable safe circle drawn)
from PIL import ImageDraw
cells = [('iOS/ios-icon-180.png', 'iOS 180'), ('Android/android-icon-192.png', 'Android 192'), ('Android/android-maskable-512.png', 'Maskable 512'),
         ('Windows/mstile-150x150.png', 'Windows 150'), ('Windows/mstile-310x150.png', 'Windows wide'), ('PWA/pwa-icon-192.png', 'PWA 192')]
sheet = Image.new('RGBA', (6 * 220 + 40, 2 * 240 + 40), (0, 0, 0, 255)); d = ImageDraw.Draw(sheet)
for row, ground in enumerate(((13, 13, 15, 255), (245, 240, 231, 255))):
    d.rectangle([0, row * 260 + 20, sheet.width, row * 260 + 260], fill=ground)
    for i, (f, label) in enumerate(cells):
        im = Image.open(HERE / f).convert('RGBA'); im.thumbnail((180, 180))
        x = 20 + i * 220 + (180 - im.width) // 2; y = row * 260 + 40 + (180 - im.height) // 2
        sheet.alpha_composite(im, (x, y))
        if 'maskable' in f:
            r = im.width * 0.4; cx, cy = x + im.width / 2, y + im.height / 2; d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(233, 178, 90, 255), width=2)
sheet.convert('RGB').save(HERE / 'app-icons-preview.png')
print('built', len(made) + 4, 'icons')
