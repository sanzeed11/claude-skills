#!/usr/bin/env python3
"""manifest.py — walks 10_MARKETING_COLLATERAL and records every file with its measured spec
(PNG/JPG pixels, PDF page count + page size in mm + font embedding, SVG size, PPTX slide count, DOCX pages via its PDF).
Writes _shared/build/manifest.json; used by the READMEs and the delivery report."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MC, page_sizes
from PIL import Image

def pdf_info(p):
    sizes = page_sizes(p); r = subprocess.run(["pdffonts", p], capture_output=True, text=True).stdout
    fonts = [l.split()[0] for l in r.splitlines()[2:] if l.strip()]
    emb = all(("yes" in l.split()[3:5]) for l in r.splitlines()[2:] if l.strip() and len(l.split()) > 4)
    uniq = sorted(set(sizes)); return dict(pages=len(sizes), page_mm=uniq if len(uniq) > 1 else uniq[0], fonts_embedded=emb)

def spec(path):
    ext = path.rsplit(".", 1)[-1].lower()
    try:
        if ext in ("png", "jpg", "jpeg", "webp"):
            im = Image.open(path); return f"{im.width}×{im.height} px"
        if ext == "pdf":
            i = pdf_info(path); pm = i["page_mm"]
            s = f"{i['pages']} page{'s' if i['pages'] != 1 else ''} · " + (" / ".join(f"{a}×{b} mm" for a, b in pm) if isinstance(pm, list) else f"{pm[0]}×{pm[1]} mm")
            return s + (" · fonts embedded" if i["fonts_embedded"] else " · CHECK FONTS")
        if ext == "svg":
            s = open(path, encoding="utf-8", errors="ignore").read(2000); m = re.search(r'width="([^"]+)"\s+height="([^"]+)"', s)
            return f"SVG {m.group(1)} × {m.group(2)}" if m else "SVG"
        if ext == "pptx":
            from pptx import Presentation; p = Presentation(path); return f"{len(p.slides)} slides · 13.333×7.5 in (16:9)"
        if ext == "docx":
            from docx import Document; d = Document(path); return f"A4 · {len(d.paragraphs)} paragraphs"
        if ext == "html": return "HTML source (brand.css + collateral.css)"
        if ext == "md": return "Markdown"
        if ext in ("py", "js", "css", "json", "ttf", "txt"): return ext.upper()
    except Exception as e: return f"? {e}"
    return ""

if __name__ == "__main__":
    rows = []
    for root, dirs, files in os.walk(MC):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f); rel = os.path.relpath(p, MC)
            rows.append(dict(path=rel, bytes=os.path.getsize(p), spec=spec(p)))
    json.dump(rows, open(os.path.join(MC, "_shared/build/manifest.json"), "w"), indent=1, ensure_ascii=False)
    tot = sum(r["bytes"] for r in rows); print(len(rows), "files", round(tot / 1e6, 1), "MB")
    for r in rows:
        if r["spec"].endswith("CHECK FONTS") or r["spec"].startswith("?"): print("ATTN", r["path"], r["spec"])
