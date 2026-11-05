#!/usr/bin/env bash
# render-kit.sh — renders ui-kit.html full-page at the four widths (and the light theme at 1440).
# Chromium cannot capture more than 16 384 px in one screenshot, so the page is captured in parts
# (sections hidden with --js) and stitched with Pillow. Run from this folder:  bash render-kit.sh
set -e
R="../../15_SOURCE_FILES/Project_Files/brand-kit/render.js"
mkdir -p renders/.parts
render_width () {  # $1 width  $2 theme  $3 out name  $4 parts-per-page (sections are split into N groups)
  local W=$1 T=$2 OUT=$3 N=$4; local files=()
  for ((p=0; p<N; p++)); do
    local JS="document.documentElement.setAttribute('data-theme','$T');var S=[...document.querySelectorAll('.kit-section')],n=S.length,per=Math.ceil(n/$N);S.forEach((s,i)=>{if(Math.floor(i/per)!=$p)s.style.display='none'});if($p>0)document.querySelector('.kit-head').style.display='none';if($p<$N-1)document.querySelector('.kit-foot').style.display='none';"
    node "$R" --in ui-kit.html --out "renders/.parts/$OUT-$p.png" --width "$W" --height 900 --scale 1 --full --wait 900 --js "$JS"
    files+=("renders/.parts/$OUT-$p.png")
  done
  python3 -I - "$OUT" "${files[@]}" <<'PY'
import sys; from PIL import Image; Image.MAX_IMAGE_PIXELS=None
out=sys.argv[1]; ims=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
W=ims[0].width; H=sum(i.height for i in ims); sheet=Image.new('RGB',(W,H)); y=0
for i in ims: sheet.paste(i,(0,y)); y+=i.height
sheet.save(f'renders/{out}.png', optimize=True); print(out, sheet.size)
PY
}
render_width 1440 dark  ui-kit--1440 3
render_width 1280 dark  ui-kit--1280 3
render_width 834  dark  ui-kit--834  3
render_width 390  dark  ui-kit--390  4
render_width 1440 light ui-kit--1440-light 3
rm -rf renders/.parts
