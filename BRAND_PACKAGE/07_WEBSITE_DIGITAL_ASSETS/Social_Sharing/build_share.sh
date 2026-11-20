#!/usr/bin/env bash
# build_share.sh — renders the three share images (exact platform pixels) + JPG q90, and the link-preview mock at 2×.
set -e; cd "$(dirname "$0")"; R="../../15_SOURCE_FILES/Project_Files/brand-kit/render.js"
python3 ../sync_logo.py src          # re-inline the approved wordmark from 02_LOGO_SYSTEM/SVG
node $R --in src/share-16x9.html --out sanzeed-share--16x9-1920x1080.png --width 1920 --height 1080 --scale 1 --wait 700
node $R --in src/share-1x1.html  --out sanzeed-share--1x1-1080x1080.png  --width 1080 --height 1080 --scale 1 --wait 700
node $R --in src/share-9x16.html --out sanzeed-share--9x16-1080x1920.png --width 1080 --height 1920 --scale 1 --wait 700
node $R --in src/link-preview.html --out sanzeed-link-preview--mock-1600x900.png --width 1600 --height 900 --scale 2 --wait 900
python3 -I - <<'PY'
from PIL import Image
for f in ['sanzeed-share--16x9-1920x1080','sanzeed-share--1x1-1080x1080','sanzeed-share--9x16-1080x1920']:
    Image.open(f+'.png').convert('RGB').save(f+'.jpg', quality=90, subsampling=0, optimize=True)
print('jpg ok')
PY
