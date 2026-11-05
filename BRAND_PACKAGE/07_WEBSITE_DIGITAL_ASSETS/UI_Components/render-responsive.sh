#!/usr/bin/env bash
# render-responsive.sh — renders responsive-specimen.html (nav + hero + cards) at 1440 / 1280 / 834 / 390
# and composes the four captures side by side into renders/responsive-sheet.png (labels drawn with Inter).
set -e
R="../../15_SOURCE_FILES/Project_Files/brand-kit/render.js"; mkdir -p renders/.parts
for W in 1440 1280 834 390; do node "$R" --in responsive-specimen.html --out "renders/.parts/resp-$W.png" --width $W --height 900 --scale 1 --full --wait 900; done
python3 -I - <<'PY'
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS=None
widths=[1440,1280,834,390]; gap=60; pad=80; labelh=70
ims=[Image.open(f'renders/.parts/resp-{w}.png').convert('RGB') for w in widths]
H=max(i.height for i in ims)
sheet=Image.new('RGB',(sum(widths)+gap*3+pad*2, H+pad*2+labelh),(13,13,15))
d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('/home/user/claude-skills/BRAND_PACKAGE/04_TYPOGRAPHY/Font_Files/Inter_Tight/InterTight[wght].ttf',22)
try: font.set_variation_by_axes([600])
except Exception: pass
x=pad
for w,im,name in zip(widths,ims,['Desktop 1440','Laptop 1280','Tablet 834','Mobile 390']):
    d.text((x,pad),name.upper(),fill=(233,178,90),font=font)
    d.text((x+ (len(name)*14+40),pad+2),f'{w} px',fill=(128,128,134),font=font)
    d.rectangle([x-1,pad+labelh-1,x+w,pad+labelh+im.height],outline=(42,42,45))
    sheet.paste(im,(x,pad+labelh)); x+=w+gap
sheet.save('renders/responsive-sheet.png',optimize=True); print('responsive-sheet',sheet.size)
PY
rm -rf renders/.parts
