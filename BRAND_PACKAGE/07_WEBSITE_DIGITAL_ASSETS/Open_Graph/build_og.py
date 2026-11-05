#!/usr/bin/env python3
"""build_og.py — fills src/og-work--template.html for the three case studies, renders every card at
1200×630 and 1200×1200 with brand-kit/render.js, and writes a JPG (q90) beside each PNG.
Run from this folder:  python3 build_og.py        (needs node + playwright, Pillow)"""
import subprocess, pathlib, sys
from PIL import Image
HERE = pathlib.Path(__file__).parent; SRC = HERE / 'src'
RENDER = HERE / '../../15_SOURCE_FILES/Project_Files/brand-kit/render.js'
IMG = '../../../00_ORIGINAL_ASSETS_BACKUP/images/img/case/'
WORK = [  # slug, image, category, title, place, the idea line (all from the case studies on sanzeed.com)
  ('prime-minister-museum', IMG + 'prime-minister-museum-07.webp', 'Museums &amp; Experience Centres', 'Prime Minister Museum', 'New Delhi', 'A corridor you walk in order.'),
  ('ram-katha-show',        IMG + 'ram-katha-show-07.webp',        'Projection Mapping &amp; Shows',   'Ram Katha Show',        'Ayodhya',   'The building is the screen.'),
  ('buddha-park',           IMG + 'buddha-park-02.webp',           'Museums &amp; Experience Centres', 'Buddha Park',           'Uttarakhand', 'A garden of gestures.'),
]
tpl = (SRC / 'og-work--template.html').read_text()
for slug, image, cat, title, place, line in WORK:
    html = tpl.replace('{{IMAGE}}', image).replace('{{CATEGORY}}', cat).replace('{{TITLE}}', title).replace('{{PLACE}}', place).replace('{{LINE}}', line).replace('{{SLUG}}', slug)
    (SRC / f'og-work--{slug}.html').write_text(html)
cards = ['default', 'home', 'about', 'contact'] + [f'work--{s[0]}' for s in WORK]
for name in cards:
    src = SRC / f'og-{name}.html'
    for w, h in ((1200, 630), (1200, 1200)):
        out = HERE / f'sanzeed-og--{name}-{w}x{h}.png'
        subprocess.run(['node', str(RENDER), '--in', str(src), '--out', str(out), '--width', str(w), '--height', str(h), '--scale', '1', '--wait', '700'], check=True, capture_output=True)
        im = Image.open(out).convert('RGB'); im.save(out.with_suffix('.jpg'), quality=90, subsampling=0, optimize=True)
        print('rendered', out.name, im.size)
