#!/usr/bin/env bash
# build_email.sh — renders the headers at 2× (1200×400 / 1200×300) as PNG + JPG q90, and the signature preview.
set -e; cd "$(dirname "$0")"; R="../../15_SOURCE_FILES/Project_Files/brand-kit/render.js"
python3 ../sync_logo.py src   # re-inline the approved wordmark (02_LOGO_SYSTEM/SVG) in the header sources
# signature logo: the production wordmark (full-colour-light / -dark) centred on a 640×200 transparent canvas, 540 px wide
# (clear space ≥ ½ cap height on every side) → src/email-logo--<t>.svg → images/sanzeed-email-logo--<t>-640x200.png
python3 -I - <<'PY'
import re, cairosvg
for t in ('light', 'dark'):
    s = re.sub(r'\s+', ' ', open(f'../../02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-{t}.svg').read())
    w, h = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups())
    body = re.search(r'(<g id="wordmark-ink".*</g>)\s*</g>\s*</g>\s*</svg>', s).group(1)
    body = re.sub(r'\s+id="[^"]*"', '', body)
    k = 540 / w; x, y = (640 - w * k) / 2, (200 - h * k) / 2
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 200" width="640" height="200">'
           f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.5f})">{body}</g></svg>')
    open(f'src/email-logo--{t}.svg', 'w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f'images/sanzeed-email-logo--{t}-640x200.png', output_width=640, output_height=200)
    print('email logo', t, f'{w*k:.0f}x{h*k:.1f} px on 640x200')
PY
for T in dark light; do
  node $R --in src/email-header--$T.html --out sanzeed-email-header--$T-1200x400.png --width 600 --height 200 --scale 2 --wait 600
  node $R --in src/newsletter-header--$T.html --out sanzeed-newsletter-header--$T-1200x300.png --width 600 --height 150 --scale 2 --wait 600
done
python3 -I - <<'PY'
sig=open('email-signature.html').read().replace('images/sanzeed-email-logo--light-640x200.png','../images/sanzeed-email-logo--light-640x200.png')
open('src/signature-preview--built.html','w').write(open('src/signature-preview.html').read().replace('<!--SIGNATURE-->',sig))
PY
node $R --in src/signature-preview--built.html --out sanzeed-email-signature--preview.png --width 816 --height 760 --scale 2 --wait 800 --full
python3 -I - <<'PY'
from PIL import Image
import glob
for f in glob.glob('sanzeed-*-header--*.png'):
    Image.open(f).convert('RGB').save(f[:-4]+'.jpg', quality=90, subsampling=0, optimize=True)
print('jpg ok')
PY
