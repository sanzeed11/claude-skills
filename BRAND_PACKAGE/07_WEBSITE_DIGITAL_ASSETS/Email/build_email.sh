#!/usr/bin/env bash
# build_email.sh — renders the headers at 2× (1200×400 / 1200×300) as PNG + JPG q90, and the signature preview.
set -e; cd "$(dirname "$0")"; R="../../15_SOURCE_FILES/Project_Files/brand-kit/render.js"
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
