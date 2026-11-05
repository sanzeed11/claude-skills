#!/usr/bin/env python3
"""grade.py — the Sanzeed photographic grade (repeatable, importable).

The grade is deliberately subtle. It does four things and nothing else:

  1. Contrast   — a gentle S-curve (sine S, amount 0.18) pivoting on mid-grey.
  2. Blacks     — a toe that lands pure black on Night (#0D0D0F) instead of #000000,
                  so shadows keep a trace of detail and never crush.
  3. Highlights — a warm shift of the brightest 45 % of the tonal range toward
                  Lamp Gold (#E9B25A); maximum tint strength 10 % at pure white.
  4. Saturation — unchanged (1.00). The grade never boosts colour.

Reference curve (8-bit, per channel, before the warm shift):
    in   0   16   32   64  128  192  224  255
    out 13   21   30   57  128  199  229  255   (R and G; B lands on 15 at black)

Usage
    python3 grade.py in.webp out.jpg                 # graded JPG, quality 90
    python3 grade.py in.webp out.jpg --webp out.webp # also write a WebP (cwebp q90)
    python3 grade.py in.jpg  out.jpg --strength 0.6  # scale the whole grade down
    python3 grade.py --print-curve                   # print the reference curve

Import
    from grade import grade_image
    graded = grade_image(Image.open("photo.jpg"))    # returns a PIL RGB image

Requires Pillow and numpy. cwebp (libwebp) is used for WebP export when present.
"""
import sys, subprocess, shutil, math
from pathlib import Path
import numpy as np
from PIL import Image

NIGHT = (13, 13, 15)            # #0D0D0F — where pure black lands
LAMP_GOLD = (233, 178, 90)      # #E9B25A — the direction of the highlight warmth

CONTRAST = 0.18                 # sine-S amount; 0 = none, 0.35 = strong
TOE_WIDTH = 0.22                # input range (0–1) over which the Night toe fades out
WARM_START, WARM_END = 0.55, 1.0  # luminance band that receives the warm shift
WARM_MAX = 0.10                 # tint strength at pure white (0–1)
SATURATION = 1.00               # never above 1.0 for this brand


def _smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def grade_array(arr, strength=1.0):
    """arr: float32 RGB array in 0–1. Returns graded float32 array in 0–1."""
    x = np.clip(arr, 0.0, 1.0).astype(np.float32)

    # 1. contrast: sine S-curve, y = x - a*sin(2πx)/(2π)
    a = CONTRAST * strength
    x = x - a * np.sin(2.0 * math.pi * x) / (2.0 * math.pi)

    # 2. toe to Night: blend toward the Night value as x → 0
    night = np.array(NIGHT, dtype=np.float32) / 255.0
    toe = np.clip(1.0 - x / TOE_WIDTH, 0.0, 1.0) ** 2
    x = x + night * toe * strength          # additive lift: monotonic, lands 0 on Night

    # 3. warm highlights toward Lamp Gold (per-channel gain in the highlight band)
    lum = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]
    w = WARM_MAX * strength * _smoothstep(WARM_START, WARM_END, lum)
    gold = np.array(LAMP_GOLD, dtype=np.float32) / 255.0
    gain = gold / gold.max()            # (1.000, 0.764, 0.386)
    x = x * (1.0 - w[..., None]) + x * gain * w[..., None]
    # keep perceived brightness: compensate the small luminance loss of the tint
    x[..., 0] = np.clip(x[..., 0] + 0.6 * w * (1.0 - x[..., 0]) * 0.1, 0, 1)

    # 4. saturation (identity unless SATURATION != 1)
    if SATURATION != 1.0:
        l2 = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
        x = l2 + (x - l2) * SATURATION

    return np.clip(x, 0.0, 1.0)


def grade_image(im, strength=1.0):
    """PIL image in → graded PIL RGB image out."""
    arr = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    out = grade_array(arr, strength)
    return Image.fromarray((out * 255.0 + 0.5).astype(np.uint8), "RGB")


def curve_table():
    xs = np.array([0, 16, 32, 64, 128, 192, 224, 255], dtype=np.float32) / 255.0
    arr = np.stack([xs, xs, xs], axis=-1)[None, ...]
    # curve only (no warm shift): run steps 1–2
    a = CONTRAST
    x = arr - a * np.sin(2.0 * math.pi * arr) / (2.0 * math.pi)
    night = np.array(NIGHT, dtype=np.float32) / 255.0
    toe = np.clip(1.0 - x / TOE_WIDTH, 0.0, 1.0) ** 2
    x = x + night * toe
    out = (x[0] * 255.0 + 0.5).astype(int)
    return [(int(round(v * 255)), tuple(int(c) for c in o)) for v, o in zip(xs, out)]


def save_jpg(im, path, quality=90):
    im.save(path, "JPEG", quality=quality, subsampling=0, optimize=True, progressive=True)


def save_webp(im, path, quality=90):
    if shutil.which("cwebp"):
        tmp = str(path) + ".tmp.png"
        im.save(tmp, "PNG")
        subprocess.run(["cwebp", "-quiet", "-q", str(quality), "-m", "6", tmp, "-o", str(path)], check=True)
        Path(tmp).unlink()
    else:
        im.save(path, "WEBP", quality=quality, method=6)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--print-curve" in args:
        print("Sanzeed grade — reference curve (8-bit in → out, R G B)")
        for i, o in curve_table():
            print(f"  {i:3d} → {o[0]:3d} {o[1]:3d} {o[2]:3d}")
        sys.exit(0)
    src, dst = args[0], args[1]
    opts = dict(a.split("=", 1) if "=" in a else (a, "1") for a in args[2:])
    strength = float(opts.get("--strength", "1.0"))
    quality = int(opts.get("--quality", "90"))
    im = grade_image(Image.open(src), strength)
    if dst.lower().endswith(".webp"):
        save_webp(im, dst, quality)
    elif dst.lower().endswith(".png"):
        im.save(dst, "PNG")
    else:
        save_jpg(im, dst, quality)
    if "--webp" in opts and opts["--webp"] != "1":
        save_webp(im, opts["--webp"], quality)
    print("graded", dst)
