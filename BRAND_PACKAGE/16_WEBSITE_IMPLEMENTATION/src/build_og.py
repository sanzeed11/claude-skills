#!/usr/bin/env python3
"""build_og.py — renders the Open Graph share images for the site.
   og.jpg (home, 1200×630) and img/og/<slug>-1200x630.jpg for the three case studies.
   Sources: src/og/og-home.html, src/og/og-work--template.html, src/og/og.css (brand.css linked).
   Run from anywhere:  python3 16_WEBSITE_IMPLEMENTATION/src/build_og.py   (needs node + playwright, Pillow)"""
import subprocess, pathlib, re
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent; SITE = HERE.parent; B = SITE.parent
SRC = HERE / 'og'; BUILD = SRC / 'build'; BUILD.mkdir(exist_ok=True)
RENDER = B / '15_SOURCE_FILES/Project_Files/brand-kit/render.js'
LOGO = B / '02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg'
s = re.sub(r'\s+', ' ', LOGO.read_text())
d = re.search(r'id="wordmark-ink"[^>]*>.*?\sd="([^"]+)"', s).group(1).strip()   # \sd= so id="…" is skipped
assert d.startswith('M'), d[:40]
dots = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', s)
vb = re.search(r'viewBox="([^"]+)"', s).group(1)          # tight bounds of the approved wordmark (≈ 3692.5 × 519.3)
assert len(dots) == 3, 'the approved wordmark has three points (A, Z, D)'
WM = ('<svg class="wm" viewBox="%s" role="img" aria-label="Sanzeed"><path class="wm-letters" d="%s"/>' % (vb, d)
      + ''.join('<circle class="wm-dot" cx="%s" cy="%s" r="%s"/>' % c for c in dots) + '</svg>')
WORK = [  # slug, image (relative to src/og/build/), category, title, place, the idea line (all from the case-study pages)
  ('prime-minister-museum', '../../../img/prime-minister-museum.webp', 'Museums &amp; Experience Centres', 'Prime Minister Museum', 'New Delhi', 'A corridor you walk in order.'),
  ('ram-katha-show',        '../../../img/case/ram-katha-show-07.webp', 'Projection Mapping &amp; Shows',   'Ram Katha Show',        'Ayodhya',     'The building is the screen.'),
  ('buddha-park',           '../../../img/buddha-park.webp',           'Museums &amp; Experience Centres', 'Buddha Park',           'Uttarakhand', 'A garden of gestures.'),
]
def render(html_name, out_jpg):
    png = BUILD / (out_jpg.stem + '.png')
    subprocess.run(['node', str(RENDER), '--in', str(BUILD / html_name), '--out', str(png), '--width', '1200', '--height', '630', '--scale', '1', '--wait', '900'], check=True)
    im = Image.open(png).convert('RGB'); assert im.size == (1200, 630), im.size
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_jpg, quality=90, subsampling=0, optimize=True, progressive=True)
    png.unlink()   # the JPG is the deliverable; the HTML in src/og/ is the editable source
    print('wrote', out_jpg.relative_to(SITE), im.size, f'{out_jpg.stat().st_size//1024} KB')
# css is linked relatively from src/og/, the built copies live one level deeper
css_fix = lambda h: h.replace('href="../../../15_SOURCE_FILES', 'href="../../../../15_SOURCE_FILES').replace('href="og.css"', 'href="../og.css"')
(BUILD / 'og-home.html').write_text(css_fix((SRC / 'og-home.html').read_text()).replace('{{WM}}', WM))
render('og-home.html', SITE / 'og.jpg')
tpl = css_fix((SRC / 'og-work--template.html').read_text())
for slug, image, cat, title, place, line in WORK:
    html = (tpl.replace('{{IMAGE}}', image).replace('{{CATEGORY}}', cat).replace('{{TITLE}}', title)
               .replace('{{PLACE}}', place).replace('{{LINE}}', line).replace('{{WM}}', WM))
    (BUILD / f'og-work--{slug}.html').write_text(html)
    render(f'og-work--{slug}.html', SITE / 'img' / 'og' / f'{slug}-1200x630.jpg')
