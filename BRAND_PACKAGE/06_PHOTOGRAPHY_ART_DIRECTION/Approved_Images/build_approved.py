#!/usr/bin/env python3
"""build_approved.py — rebuilds the approved image library from approved.json.

  python3 build_approved.py            # grade + export everything, write index.md, render contact sheet
  python3 build_approved.py --no-sheet # skip the contact-sheet render (no node/Playwright needed)

Outputs (all relative to this folder):
  JPG/sanzeed-img-<slug>--<category>.jpg      graded, native size, JPEG q90 4:4:4
  WebP/sanzeed-img-<slug>--<category>.webp    same pixels, cwebp q90
  Portrait/sanzeed-portrait--<ratio>-2000.jpg graded crops of the portrait, 2000 px long edge (+ WebP)
  index.md                                    the table of files, projects, places, categories, uses, rights
  sanzeed-contact-sheet--approved-30.png      rendered from ../src/contact-sheet/contact-sheet.html
"""
import json, os, sys, subprocess, html
from pathlib import Path
from PIL import Image, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
from grade import grade_image, save_jpg, save_webp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                     # 06_PHOTOGRAPHY_ART_DIRECTION
KIT = ROOT.parent / "15_SOURCE_FILES/Project_Files/brand-kit"
M = json.load(open(HERE / "approved.json"))
SRC = (HERE / M["source_root"]).resolve()
RIGHTS = M["rights"]

(HERE / "JPG").mkdir(exist_ok=True); (HERE / "WebP").mkdir(exist_ok=True); (HERE / "Portrait").mkdir(exist_ok=True)

rows = []
for it in M["images"]:
    im = Image.open(SRC / it["src"]).convert("RGB")
    g = grade_image(im)
    name = f"sanzeed-img-{it['slug']}--{it['category']}"
    save_jpg(g, HERE / "JPG" / f"{name}.jpg", 90)
    save_webp(g, HERE / "WebP" / f"{name}.webp", 90)
    w, h = g.size
    orient = "landscape" if w > h else ("portrait" if h > w else "square")
    it.update(file=f"{name}.jpg", w=w, h=h, orient=orient)
    rows.append(it)
    print("exported", name, w, h)

# ---------- portrait crops ----------
P = M["portrait"]
pim = Image.open((HERE / P["src"]).resolve()).convert("RGB")
pg = grade_image(pim)
W, H = pg.size
ex, ey = P["eyes"][0] * W, P["eyes"][1] * H
save_jpg(pg, HERE / "Portrait" / f"sanzeed-portrait--native-{W}x{H}.jpg", 90)
save_webp(pg, HERE / "Portrait" / f"sanzeed-portrait--native-{W}x{H}.webp", 90)
portrait_rows = [(f"sanzeed-portrait--native-{W}x{H}.jpg", f"{W}×{H}", "native", "graded original; eye line at 36 % of height")]

def crop_ratio(img, rw, rh, eye_frac):
    """Crop img to rw:rh using the full width, placing the eye line at eye_frac of the crop height."""
    cw = img.width; ch = int(round(cw * rh / rw))
    if ch > img.height:
        ch = img.height; cw = int(round(ch * rw / rh))
    top = int(round(ey - eye_frac * ch)); top = max(0, min(top, img.height - ch))
    left = int(round(ex - cw / 2)); left = max(0, min(left, img.width - cw))
    return img.crop((left, top, left + cw, top + ch))

for tag, rw, rh, eye_frac in [("1x1", 1, 1, 0.38), ("4x5", 4, 5, 0.36), ("3x4", 3, 4, 0.35)]:
    c = crop_ratio(pg, rw, rh, eye_frac)
    long_edge = 2000
    scale = long_edge / max(c.size)
    out = c.resize((round(c.width * scale), round(c.height * scale)), Image.LANCZOS)
    fn = f"sanzeed-portrait--{tag}-2000.jpg"
    save_jpg(out, HERE / "Portrait" / fn, 90); save_webp(out, HERE / "Portrait" / fn.replace(".jpg", ".webp"), 90)
    portrait_rows.append((fn, f"{out.width}×{out.height}", tag.replace("x", ":"), f"eye line at {int(eye_frac*100)} % of height; resampled ×{scale:.2f} from source"))
    print("portrait", fn, out.size)

# 16:9 — the portrait is upright, so a true 16:9 crop would cut the head. The 16:9 plate extends the
# bokeh background (blurred, darkened to Night) and places the figure on the right third.
CW, CH = 2000, 1125
# background: the left bokeh strip of the portrait (no face), stretched to the canvas, blurred, darkened to Night
strip = pg.crop((0, 0, 330, H))
bg = strip.resize((CW, CH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(90))
bg = Image.blend(bg, Image.new("RGB", bg.size, (13, 13, 15)), 0.56)
fig_h = CH; fig_w = round(W * fig_h / H)
fig = pg.resize((fig_w, fig_h), Image.LANCZOS)
fx = CW - fig_w - 140
mask = Image.new("L", fig.size, 255)
from PIL import ImageDraw
d = ImageDraw.Draw(mask)
fade = 220
for i in range(fade):
    d.line([(i, 0), (i, fig_h)], fill=int(255 * (i / fade) ** 1.6))
bg.paste(fig, (fx, 0), mask)
fn = "sanzeed-portrait--16x9-extended-2000.jpg"
save_jpg(bg, HERE / "Portrait" / fn, 90); save_webp(bg, HERE / "Portrait" / fn.replace(".jpg", ".webp"), 90)
portrait_rows.append((fn, f"{CW}×{CH}", "16:9", "extended plate — figure on the right third, background continued and darkened to Night (not a crop)"))
print("portrait", fn)

# ---------- index.md ----------
cats = {"museum": "Museums & experience centres", "projection": "Projection & shows", "event": "Events & activations", "architecture": "Architecture & environment"}
L = []
L.append("# Approved images — index\n")
L.append("Thirty graded images from the client's own project visuals, plus the portrait. Grade: `grade.py` (contrast +0.18 sine-S, blacks to Night #0D0D0F, highlights warmed toward Lamp Gold #E9B25A, saturation unchanged). Rebuild everything with `python3 build_approved.py`.\n")
L.append(f"**Rights note (applies to every row):** {RIGHTS}\n")
L.append("| # | File | Project | Place | Category | Size | Orientation | Suggested uses | Rights |")
L.append("|---|---|---|---|---|---|---|---|---|")
for i, it in enumerate(rows, 1):
    L.append(f"| {i:03d} | `JPG/{it['file']}` · `WebP/{it['file'][:-4]}.webp` | {it['title']} | {it['place']} | {cats[it['category']]} | {it['w']}×{it['h']} | {it['orient']} | {it['uses']} | employee work — rights remain with the commissioning studio; portfolio and credential use |")
L.append("\n## Portrait\n")
L.append(f"Source: `{P['src']}` ({W}×{H}). {P['note']}\n")
L.append("| File | Size | Ratio | Note | Rights |")
L.append("|---|---|---|---|---|")
for fn, size, ratio, note in portrait_rows:
    L.append(f"| `Portrait/{fn}` (+ `.webp`) | {size} | {ratio} | {note} | own portrait — Sanzeed Mirza; all brand uses |")
L.append("\n## Category counts\n")
from collections import Counter
cnt = Counter(it["category"] for it in rows)
L.append("| Category | Count |\n|---|---|")
for k, v in cnt.items():
    L.append(f"| {cats[k]} | {v} |")
L.append(f"| **Total** | **{len(rows)}** |")
L.append("\n## Wall labels\n")
L.append("Every image is captioned Title · Place when published. The one-line art-direction notes used on the moodboard are stored in `approved.json` (`line`), together with the focal point (`focal`, fractions of width and height) that `../Image_Templates/treat_image.py` and the HTML templates crop around.\n")
(HERE / "index.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("wrote index.md")

# ---------- contact sheet (HTML → PNG) ----------
if "--no-sheet" not in sys.argv:
    cells = []
    for i, it in enumerate(rows, 1):
        cells.append(f'''      <figure class="cell">
        <img src="../../Approved_Images/JPG/{it['file']}" alt="{html.escape(it['title'])} — {html.escape(it['place'])}">
        <figcaption><span class="counter">{i:03d}</span><span class="wl"><b>{html.escape(it['title'])}</b><span>{html.escape(it['place'])}</span></span></figcaption>
      </figure>''')
    page = f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Sanzeed — approved images, contact sheet</title>
<link rel="stylesheet" href="../../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
  html, body {{ background: var(--bg); }}
  .sheet {{ width: 2000px; padding: 72px 80px 64px; }}
  header {{ display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 40px; }}
  header .eyebrow {{ margin-bottom: 14px; }}
  header h1 {{ font-size: 64px; line-height: 1.02; }}
  header .meta {{ text-align: right; color: var(--fg-3); font-size: 15px; line-height: 1.5; }}
  header img {{ height: 28px; margin-left: auto; margin-bottom: 12px; }}
  .grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 28px 24px; }}
  .cell {{ margin: 0; }}
  .cell img {{ width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 12px; border: var(--hairline); }}
  figcaption {{ display: flex; gap: 10px; align-items: flex-start; margin-top: 10px; }}
  .wl {{ display: flex; flex-direction: column; font-size: 13px; line-height: 1.4; color: var(--fg-3); }}
  .wl b {{ font-family: var(--font-heading); font-weight: 600; color: var(--fg); }}
  footer {{ margin-top: 44px; padding-top: 20px; border-top: var(--hairline); display: flex; justify-content: space-between; color: var(--fg-3); font-size: 13px; }}
</style>
</head>
<body>
<div class="sheet grain">
  <header>
    <div>
      <div class="eyebrow">Approved images · 001 – 030</div>
      <h1 class="t-display-2">Thirty rooms, one light.</h1>
    </div>
    <div class="meta">Graded with grade.py · JPG q90 + WebP · index.md for uses and rights<br>Employee work — rights remain with the commissioning studio; portfolio and credential use.</div>
  </header>
  <div class="grid">
{chr(10).join(cells)}
  </div>
  <footer><span>Sanzeed Mirza · Experiential Design Consultant · sanzeed.com</span><span>06_PHOTOGRAPHY_ART_DIRECTION / Approved_Images</span></footer>
</div>
</body>
</html>
'''
    sheet_dir = ROOT / "src" / "contact-sheet"; sheet_dir.mkdir(parents=True, exist_ok=True)
    (sheet_dir / "contact-sheet.html").write_text(page, encoding="utf-8")
    out_png = HERE / "sanzeed-contact-sheet--approved-30.png"
    subprocess.run(["node", str(KIT / "render.js"), "--in", str(sheet_dir / "contact-sheet.html"), "--out", str(out_png),
                    "--width", "2000", "--height", "1200", "--scale", "1.5", "--full", "--wait", "800"], check=True)
    print("wrote", out_png)
