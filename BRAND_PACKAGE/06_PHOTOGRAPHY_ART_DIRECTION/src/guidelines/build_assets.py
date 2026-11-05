#!/usr/bin/env python3
"""build_assets.py — generates the example images used by photography-guidelines.html into ./assets/.

  python3 build_assets.py

Produces
  grade-before.jpg / grade-after.jpg        the before/after pair (source vs. graded), same crop
  curve.svg                                  the grade's reference curve as an SVG plot
  bad-busy.jpg, bad-flat.jpg, bad-saturated.jpg, bad-logo-on-busy.jpg   deliberately wrong treatments
  crop-16x9.jpg, crop-4x5.jpg, crop-1x1.jpg, crop-9x16.jpg, crop-3x2.jpg  one image cropped around its focal point
  veil-off.jpg / veil-on.jpg                 background treatment pair
All examples are made from approved images (../../Approved_Images) — nothing is stock or generated.
"""
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cairosvg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
B = ROOT.parent
sys.path.insert(0, str(ROOT / "Image_Templates")); sys.path.insert(0, str(ROOT / "Approved_Images"))
from treat_image import crop_to_ratio, add_veil, add_label          # noqa: E402
from grade import grade_image, grade_array, save_jpg, CONTRAST, NIGHT, TOE_WIDTH  # noqa: E402

OUT = HERE / "assets"; OUT.mkdir(exist_ok=True)
JPG = ROOT / "Approved_Images/JPG"
SRC = B / "00_ORIGINAL_ASSETS_BACKUP/images/img"
M = json.load(open(ROOT / "Approved_Images/approved.json"))
IMG = {it["slug"]: it for it in M["images"]}
def approved(slug): it = IMG[slug]; return Image.open(JPG / f"sanzeed-img-{slug}--{it['category']}.jpg").convert("RGB")
def source(slug): return Image.open(SRC / IMG[slug]["src"]).convert("RGB")

# ---- before / after ----
before = source("maharishi-valmiki-museum"); after = grade_image(before)
save_jpg(before, OUT / "grade-before.jpg", 90); save_jpg(after, OUT / "grade-after.jpg", 90)
# a second pair on a dark projection image
b2 = source("postal-museum-projection-show"); save_jpg(b2, OUT / "grade-before-2.jpg", 90); save_jpg(grade_image(b2), OUT / "grade-after-2.jpg", 90)

# ---- curve.svg (identity vs grade; R channel) ----
xs = np.linspace(0, 1, 256).astype(np.float32)
x = xs - CONTRAST * np.sin(2 * math.pi * xs) / (2 * math.pi)
night = np.array(NIGHT, dtype=np.float32) / 255
toe = np.clip(1 - x / TOE_WIDTH, 0, 1) ** 2
yr = np.clip(x + night[0] * toe, 0, 1)
W = H = 400; pad = 1
pts = " ".join(f"{pad + xi * (W - 2*pad):.1f},{pad + (1 - yi) * (H - 2*pad):.1f}" for xi, yi in zip(xs, yr))
grid = "".join(f'<line x1="{W*i/4:.0f}" y1="0" x2="{W*i/4:.0f}" y2="{H}"/><line x1="0" y1="{H*i/4:.0f}" x2="{W}" y2="{H*i/4:.0f}"/>' for i in range(1, 4))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#1C1C1E" rx="20"/>
  <g stroke="rgba(255,255,255,.10)" stroke-width="1">{grid}</g>
  <line x1="0" y1="{H}" x2="{W}" y2="0" stroke="rgba(255,255,255,.22)" stroke-width="1" stroke-dasharray="4 5"/>
  <polyline points="{pts}" fill="none" stroke="#E9B25A" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="{pad:.0f}" cy="{pad + (1 - yr[0]) * (H - 2*pad):.1f}" r="4" fill="#E9B25A"/>
</svg>'''
(OUT / "curve.svg").write_text(svg, encoding="utf-8")

# ---- unacceptable examples ----
def saturate(im, f):
    return ImageEnhance.Color(im).enhance(f)

# 1 busy: a tight crop of a cluttered corner, over-sharpened, mid-tone everywhere
busy = approved("vadnagar-archaeological-museum")
busy = busy.crop((int(busy.width * 0.30), int(busy.height * 0.05), int(busy.width * 0.95), int(busy.height * 0.70)))
busy = busy.resize((960, 540), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=3, percent=220, threshold=0))
busy = ImageEnhance.Brightness(busy).enhance(1.25)
save_jpg(busy, OUT / "bad-busy.jpg", 88)

# 2 flat-lit: blacks lifted, contrast gone — the "flash snapshot" look
flat = source("freedom-fighter-museum")
arr = np.asarray(flat).astype(np.float32) / 255
arr = 0.33 + arr * 0.52                      # black point 84, white point 217
flat = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8))
flat = saturate(flat, 0.8)
save_jpg(flat, OUT / "bad-flat.jpg", 88)

# 3 over-saturated
sat = saturate(approved("ram-katha-show-ceiling"), 2.1)
sat = ImageEnhance.Contrast(sat).enhance(1.25)
save_jpg(sat, OUT / "bad-saturated.jpg", 88)

# 4 logo on busy: the full-colour-dark wordmark dropped on a bright, busy area with no veil
lob = approved("g20-tree-show").copy()
png = cairosvg.svg2png(url=str(B / "02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg"), output_width=int(lob.width * 0.46))
from io import BytesIO
logo = Image.open(BytesIO(png)).convert("RGBA")
lob.paste(logo, (int(lob.width * 0.27), int(lob.height * 0.36)), logo)
save_jpg(lob, OUT / "bad-logo-on-busy.jpg", 88)

# ---- crop set around the focal point ----
it = IMG["india-pavilion-expo-2025"]; im = approved("india-pavilion-expo-2025")
for tag, r in [("16x9", "16:9"), ("4x5", "4:5"), ("1x1", "1:1"), ("9x16", "9:16"), ("3x2", "3:2")]:
    c = crop_to_ratio(im, r, tuple(it["focal"]))
    save_jpg(c, OUT / f"crop-{tag}.jpg", 88)
save_jpg(im, OUT / "crop-source.jpg", 88)

# ---- veil pair ----
v = approved("sant-ravi-das-museum")
save_jpg(v, OUT / "veil-off.jpg", 88)
save_jpg(add_veil(v.copy(), 0.72), OUT / "veil-on.jpg", 88)
print("assets written to", OUT)
