#!/usr/bin/env python3
"""treat_image.py — the Sanzeed image treatment, in Pillow.

Crops to a ratio around a focal point, applies the brand grade, adds the veil, a wall label
(Title · Place), an optional counter, an optional headline, and an optional "room" frame.
Text is set in the brand variable TTFs from 04_TYPOGRAPHY/Font_Files (Inter Tight 600 for the
title, Inter 400 for the place, Inter Tight 500 for the counter, Fraunces 300 for a headline).

Usage
  python3 treat_image.py IN OUT [options]

  --ratio 16:9|4:5|1:1|9:16|3:2|WxH   crop ratio (default: keep)
  --focal 0.5,0.45                    focal point as fractions of width,height (default 0.5,0.5)
  --width 2160                        output width in px (height follows the ratio); default: crop size
  --grade 1.0                         grade strength, 0 = off (default 1.0)
  --veil 0.72                         bottom veil strength 0–1 (default 0 = none); --veil-top for a top veil
  --title "Ram Katha Show" --place "Ayodhya"   wall label (bottom-left on the veil)
  --counter 001                       gold counter above the label
  --headline "Eight rooms, lit."      Fraunces 300 headline; the last word is set in Lamp Gold
  --label-scale 1.0                   scale of the label block relative to the image width
  --frame                             wrap in the "room": Night canvas, hairline, radius 28, padding
  --concept                           adds the "Concept visualisation" eyebrow (for unbuilt work / AI concepts)
  --quality 90                        JPEG quality (PNG when OUT ends with .png, WebP with .webp)

Examples
  python3 treat_image.py ../Approved_Images/JPG/sanzeed-img-ram-katha-show--projection.jpg out.jpg \
      --ratio 4:5 --focal 0.5,0.45 --width 2160 --veil 0.72 --title "Ram Katha Show" --place "Ayodhya" --counter 001
  python3 treat_image.py in.jpg out.png --ratio 16:9 --frame --title "Prime Minister Museum" --place "New Delhi"

Import
  from treat_image import treat
  im = treat(Image.open("in.jpg"), ratio="4:5", focal=(0.5, 0.45), veil=0.72, title="…", place="…")
"""
import sys, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
B = HERE.parent.parent                              # BRAND_PACKAGE
FONTS = B / "04_TYPOGRAPHY/Font_Files"
sys.path.insert(0, str(HERE.parent / "Approved_Images"))
from grade import grade_image, save_jpg, save_webp   # noqa: E402

# ---- tokens ----
NIGHT = (13, 13, 15); BLACK = (0, 0, 0); CHARCOAL = (28, 28, 30)
GALLERY_WHITE = (245, 245, 247); SILVER = (161, 161, 166); MIST = (128, 128, 134)
LAMP_GOLD = (233, 178, 90)
RATIOS = {"16:9": (16, 9), "4:5": (4, 5), "1:1": (1, 1), "9:16": (9, 16), "3:2": (3, 2), "3:4": (3, 4), "2:3": (2, 3), "1.91:1": (191, 100)}


def font(kind, size):
    """kind: 'title' (Inter Tight 600), 'place' (Inter 400), 'counter' (Inter Tight 500), 'display' (Fraunces 300), 'eyebrow' (Inter Tight 600)."""
    if kind in ("title", "eyebrow", "counter"):
        f = ImageFont.truetype(str(FONTS / "Inter_Tight/InterTight[wght].ttf"), size)
        f.set_variation_by_axes([600 if kind != "counter" else 500])
    elif kind == "place":
        f = ImageFont.truetype(str(FONTS / "Inter/Inter[opsz,wght].ttf"), size)
        f.set_variation_by_axes([min(32, max(14, size)), 400])
    elif kind == "display":
        f = ImageFont.truetype(str(FONTS / "Fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf"), size)
        # axes: opsz, wght, SOFT, WONK
        f.set_variation_by_axes([144 if size >= 48 else 72, 300, 30, 0])
    else:
        raise ValueError(kind)
    return f


def parse_ratio(r):
    if r in RATIOS: return RATIOS[r]
    if "x" in r: a, b = r.lower().split("x"); return (float(a), float(b))
    a, b = r.split(":"); return (float(a), float(b))


def crop_to_ratio(im, ratio, focal=(0.5, 0.5)):
    """Largest crop of the given ratio, centred on the focal point and clamped to the image."""
    rw, rh = parse_ratio(ratio) if isinstance(ratio, str) else ratio
    W, H = im.size
    if W / H > rw / rh:
        ch = H; cw = int(round(H * rw / rh))
    else:
        cw = W; ch = int(round(W * rh / rw))
    fx, fy = focal[0] * W, focal[1] * H
    left = int(round(fx - cw / 2)); top = int(round(fy - ch / 2))
    left = max(0, min(left, W - cw)); top = max(0, min(top, H - ch))
    return im.crop((left, top, left + cw, top + ch))


def add_veil(im, strength=0.72, top=False, start=0.35):
    """Gradient to black over the lower (or upper) part of the image. start = where the veil begins (fraction)."""
    W, H = im.size
    mask = Image.new("L", (1, H))
    px = mask.load()
    for y in range(H):
        t = y / max(1, H - 1)
        if top: t = 1 - t
        a = 0.0 if t < start else ((t - start) / (1 - start))
        a = a * a * (3 - 2 * a)                         # smoothstep
        px[0, y] = int(255 * strength * a)
    mask = mask.resize((W, H))
    black = Image.new("RGB", (W, H), BLACK)
    return Image.composite(black, im, mask)


def add_label(im, title=None, place=None, counter=None, headline=None, concept=False, scale=1.0, margin=None):
    """Wall label bottom-left: [counter] / Title / Place. Optional headline above it (Fraunces 300, last word gold)."""
    W, H = im.size
    base = max(W, H) / 1920 * scale                       # long-edge reference (1920 = 1.0)
    m = margin if margin is not None else int(72 * base)
    d = ImageDraw.Draw(im)
    y = H - m
    lines = []                                            # drawn bottom-up
    if place:   lines.append(("place", place, SILVER, int(22 * base), 1.45))
    if title:   lines.append(("title", title, GALLERY_WHITE, int(26 * base), 1.35))
    if counter: lines.append(("counter", counter, LAMP_GOLD, int(16 * base), 1.9))
    if concept: lines.append(("eyebrow", "CONCEPT VISUALISATION", LAMP_GOLD if not counter else MIST, int(15 * base), 1.9))
    for kind, text, col, size, lh in lines:
        f = font(kind, size)
        y -= int(size * lh)
        if kind in ("counter", "eyebrow"):
            # letter-spaced caps
            x = m; sp = size * 0.12
            for ch in text:
                d.text((x, y), ch, font=f, fill=col); x += d.textlength(ch, font=f) + sp
        else:
            d.text((m, y), text, font=f, fill=col)
    if headline:
        size = int(76 * base); f = font("display", size)
        words = headline.split(" ")
        # wrap to ~60% of width
        maxw = W * 0.62; rows = []; cur = ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if d.textlength(t, font=f) > maxw and cur: rows.append(cur); cur = w_
            else: cur = t
        rows.append(cur)
        y -= int(size * 0.5)
        for r in reversed(rows):
            y -= int(size * 1.04)
            if r is rows[-1]:
                parts = r.rsplit(" ", 1)
                if len(parts) == 2:
                    d.text((m, y), parts[0] + " ", font=f, fill=GALLERY_WHITE)
                    d.text((m + d.textlength(parts[0] + " ", font=f), y), parts[1], font=f, fill=LAMP_GOLD)
                else:
                    d.text((m, y), r, font=f, fill=LAMP_GOLD)
            else:
                d.text((m, y), r, font=f, fill=GALLERY_WHITE)
    return im


def add_frame(im, radius=None, pad=None, counter=None):
    """The 'room': the image sits in a rounded rectangle with a hairline on a Night canvas."""
    W, H = im.size
    base = W / 1920
    pad = pad if pad is not None else int(64 * base)
    radius = radius if radius is not None else int(28 * base * 1.5)
    canvas = Image.new("RGB", (W + 2 * pad, H + 2 * pad), NIGHT)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), radius=radius, fill=255)
    canvas.paste(im, (pad, pad), mask)
    d = ImageDraw.Draw(canvas, "RGBA")
    d.rounded_rectangle((pad, pad, pad + W - 1, pad + H - 1), radius=radius, outline=(255, 255, 255, 26), width=max(1, int(2 * base)))
    if counter:
        f = font("counter", int(16 * base * 1.2)); x = pad; y = int(pad * 0.5) - int(10 * base)
        sp = 16 * base * 0.12
        for ch in counter:
            d.text((x, y), ch, font=f, fill=LAMP_GOLD); x += d.textlength(ch, font=f) + sp
    return canvas


def treat(im, ratio=None, focal=(0.5, 0.5), width=None, grade=1.0, veil=0.0, veil_top=False,
          title=None, place=None, counter=None, headline=None, concept=False, label_scale=1.0, frame=False):
    im = im.convert("RGB")
    if ratio: im = crop_to_ratio(im, ratio, focal)
    if width and width != im.width:
        if ratio:  # exact platform pixels: height from the requested ratio, not from the rounded crop
            rw, rh = parse_ratio(ratio) if isinstance(ratio, str) else ratio
            h = int(round(width * rh / rw))
        else:
            h = int(round(im.height * width / im.width))
        im = im.resize((int(width), h), Image.LANCZOS)
    if grade: im = grade_image(im, grade)
    if veil: im = add_veil(im, veil, top=veil_top)
    if title or place or counter or headline or concept:
        im = add_label(im, title, place, counter, headline, concept, label_scale)
    if frame: im = add_frame(im, counter=None)
    return im


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: print(__doc__); sys.exit(1)
    src, dst = a[0], a[1]
    o = {}; i = 2
    while i < len(a):
        k = a[i]
        if k.startswith("--"):
            if i + 1 < len(a) and not a[i + 1].startswith("--"): o[k[2:]] = a[i + 1]; i += 2
            else: o[k[2:]] = True; i += 1
        else: i += 1
    focal = tuple(float(v) for v in o.get("focal", "0.5,0.5").split(","))
    im = treat(Image.open(src), ratio=o.get("ratio"), focal=focal, width=int(o["width"]) if "width" in o else None,
               grade=float(o.get("grade", 1.0)), veil=float(o.get("veil", 0)), veil_top="veil-top" in o,
               title=o.get("title"), place=o.get("place"), counter=o.get("counter"), headline=o.get("headline"),
               concept="concept" in o, label_scale=float(o.get("label-scale", 1.0)), frame="frame" in o)
    q = int(o.get("quality", 90))
    if dst.lower().endswith(".png"): im.save(dst, "PNG")
    elif dst.lower().endswith(".webp"): save_webp(im, dst, q)
    else: save_jpg(im, dst, q)
    print("treated", dst, im.size)
