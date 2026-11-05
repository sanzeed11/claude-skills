#!/usr/bin/env python3
"""build_guidelines.py — renders photography-guidelines.html to ../../Photography_Guidelines.pdf (A4 portrait)
and a PNG preview of every page into ../../Photography_Guidelines_Pages/.

  python3 build_assets.py      # first, if the example images in ./assets are missing or the grade changed
  python3 build_guidelines.py  # render PDF + PNG previews
"""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
KIT = ROOT.parent / "15_SOURCE_FILES/Project_Files/brand-kit"
pdf = ROOT / "Photography_Guidelines.pdf"
subprocess.run(["node", str(KIT / "render.js"), "--in", str(HERE / "photography-guidelines.html"), "--out", str(pdf),
                "--pdf", "--size", "210x297", "--wait", "1200"], check=True)
out = ROOT / "Photography_Guidelines_Pages"; out.mkdir(exist_ok=True)
for f in out.glob("*.png"): f.unlink()
subprocess.run(["pdftoppm", "-r", "120", "-png", str(pdf), str(out / "sanzeed-photography-guidelines--p")], check=True)
n = 0
for f in sorted(out.glob("sanzeed-photography-guidelines--p*.png")):
    n += 1
    num = int("".join(ch for ch in f.stem.rsplit("--p", 1)[-1] if ch.isdigit()))
    f.rename(out / f"sanzeed-photography-guidelines--p{num:02d}.png")
print("rendered", pdf, "with", n, "page previews")
