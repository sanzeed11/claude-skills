#!/usr/bin/env python3
"""build_contact_sheets.py — contact sheets of key frames for every rendered animation.

Reads ../Exports/Key_Frames/<Deliverable>/<name>/<name>--t<time>s.{jpg,png} (written by render.sh: six frames per animation)
and writes
  ../Exports/Contact_Sheets/sanzeed-motion-contact-sheet--<Deliverable>.png   one row per animation
  ../Exports/Contact_Sheets/sanzeed-motion-contact-sheet.png                   everything, one row per animation
Transparent frames are shown over Night (#0D0D0F) with a thin frame line. Run after the renders:  python3 build_contact_sheets.py
"""
import os, re, glob
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
KF = os.path.join(HERE, "..", "Exports", "Key_Frames"); OUT = os.path.join(HERE, "..", "Exports", "Contact_Sheets"); os.makedirs(OUT, exist_ok=True)
FONTS = os.path.join(HERE, "..", "..", "04_TYPOGRAPHY", "Font_Files")
F_H = ImageFont.truetype(os.path.join(FONTS, "Inter_Tight", "InterTight[wght].ttf"), 26); F_H.set_variation_by_axes([600])
F_T = ImageFont.truetype(os.path.join(FONTS, "Fraunces", "Fraunces[SOFT,WONK,opsz,wght].ttf"), 44); F_T.set_variation_by_axes([30, 0, 72, 300])
F_S = ImageFont.truetype(os.path.join(FONTS, "Inter", "Inter[opsz,wght].ttf"), 17); F_S.set_variation_by_axes([14, 400])
F_E = ImageFont.truetype(os.path.join(FONTS, "Inter_Tight", "InterTight[wght].ttf"), 13); F_E.set_variation_by_axes([600])
BG, CARD, FG, FG2, FG3, GOLD, LINE = (0, 0, 0), (13, 13, 15), (245, 245, 247), (161, 161, 166), (128, 128, 134), (233, 178, 90), (38, 38, 40)
TW = 300; PAD = 24; GAP = 10; LABEL_W = 420

def rows_for(deliv):
    rows = []
    for d in sorted(glob.glob(os.path.join(KF, deliv, "*"))):
        frames = sorted(glob.glob(os.path.join(d, "*--t*s.*")), key=lambda f: float(re.search(r"--t([\d.]+)s", f).group(1)))
        if frames: rows.append((os.path.basename(d), frames))
    return rows

def thumb(f):
    im = Image.open(f).convert("RGBA")
    th = int(im.height * TW / im.width); im = im.resize((TW, th), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, CARD + (255,)); bg.alpha_composite(im); return bg.convert("RGB")

def sheet(title, groups, path):
    # groups: list of (deliverable, rows); each row = (name, frames). Row height follows the tallest thumb in that row.
    heights = [];
    for deliv, rows in groups:
        heights.append(56)
        for name, frames in rows: heights.append(max(int(Image.open(f).height * TW / Image.open(f).width) for f in frames) + 30 + GAP)
    W = PAD * 2 + LABEL_W + 6 * (TW + GAP); H = 110 + sum(heights) + PAD
    s = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(s)
    d.text((PAD, 30), "MOTION IDENTITY  ·  KEY FRAMES", fill=GOLD, font=F_E); d.text((PAD, 50), title, fill=FG, font=F_T)
    y = 110
    for deliv, rows in groups:
        d.text((PAD, y + 18), deliv.replace("_", " "), fill=FG, font=F_H); d.line([(PAD, y + 52), (W - PAD, y + 52)], fill=LINE, width=1); y += 56
        for name, frames in rows:
            d.text((PAD, y + 6), name.replace("sanzeed-", "").replace("--", " · ").replace("-", " "), fill=FG2, font=F_S)
            x = PAD + LABEL_W; rh = 0
            for f in frames:
                t = thumb(f); s.paste(t, (x, y)); d.rectangle([x, y, x + TW - 1, y + t.height - 1], outline=LINE)
                d.text((x, y + t.height + 6), re.search(r"--t([\d.]+)s", f).group(1) + " s", fill=FG3, font=F_E); x += TW + GAP; rh = max(rh, t.height)
            y += rh + 30 + GAP
    d.text((PAD, H - PAD - 4), "Sanzeed — 11_MOTION_GRAPHICS · frames rendered by capture_frames.js (deterministic stepping) · sheet by build_contact_sheets.py", fill=FG3, font=F_E)
    s.save(path, optimize=True); print("wrote", os.path.relpath(path, HERE), s.size)

if __name__ == "__main__":
    delivs = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(KF, "*"))) if os.path.isdir(p)]
    allg = []
    for deliv in delivs:
        rows = rows_for(deliv)
        if not rows: continue
        sheet(deliv.replace("_", " ") + ".", [(deliv, rows)], os.path.join(OUT, f"sanzeed-motion-contact-sheet--{deliv.lower()}.png")); allg.append((deliv, rows))
    sheet("Every animation, six frames each.", allg, os.path.join(OUT, "sanzeed-motion-contact-sheet.png"))
