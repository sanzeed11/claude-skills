#!/usr/bin/env python3
"""build_readme_table.py — measures every delivered file (pixels, duration, frames, size, codec) and writes the file tables
into ../README.md between <!--@files--> and <!--@/files-->. Run after the renders:  python3 build_readme_table.py
Nothing here is typed by hand: ffprobe reads the videos, Pillow the images, os.path the rest."""
import os, re, json, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, ".."))

SOURCE = [  # output-name prefix -> editable source (relative to 11_MOTION_GRAPHICS)
    ("sanzeed-logo-reveal--light", "Source_Files/logo-reveal/index-light.html"), ("sanzeed-logo-reveal", "Source_Files/logo-reveal/index.html"),
    ("sanzeed-logo-presentation", "Source_Files/logo-presentation/index.html"), ("sanzeed-logo-outro", "Source_Files/logo-outro/index.html"),
    ("sanzeed-symbol-loop", "Source_Files/symbol-loop/index.html"), ("sanzeed-intro", "Source_Files/intro/index.html"), ("sanzeed-outro", "Source_Files/outro-card/index.html"),
    ("sanzeed-transition--preview", "Source_Files/transition/preview.html"), ("sanzeed-transition", "Source_Files/transition/index.html"),
    ("sanzeed-lower-third--name--preview", "Source_Files/lower-third-name/preview.html"), ("sanzeed-lower-third--name", "Source_Files/lower-third-name/index.html"),
    ("sanzeed-lower-third--wall-label--preview", "Source_Files/lower-third-label/preview.html"), ("sanzeed-lower-third--wall-label", "Source_Files/lower-third-label/index.html"),
    ("sanzeed-lower-third--quote-attribution--preview", "Source_Files/lower-third-quote/preview.html"), ("sanzeed-lower-third--quote-attribution", "Source_Files/lower-third-quote/index.html"),
    ("sanzeed-story--project-reveal", "Source_Files/story-project/index.html"), ("sanzeed-story--quote-light-wipe", "Source_Files/story-quote/index.html"),
    ("sanzeed-story--now-showing", "Source_Files/story-now-showing/index.html"), ("sanzeed-post--project", "Source_Files/post-project/index.html"),
    ("sanzeed-post--method-route", "Source_Files/post-method/index.html"), ("sanzeed-post--stat-counter", "Source_Files/post-stats/index.html"),
    ("sanzeed-loader--960x120", "Source_Files/loader/index.html + Website_Loader/sanzeed-loader.css"),
    ("sanzeed-loader.json", "Source_Files/lottie/build_lottie.py"), ("sanzeed-loader", "itself (hand-written)"),
    ("sanzeed-reveal-on-scroll", "itself (hand-written)"), ("sanzeed-lottie--", "Source_Files/lottie/validate_lottie.js"),
    ("sanzeed-motion-contact-sheet", "Source_Files/build_contact_sheets.py"), ("sanzeed-motion--easing-curves", "Source_Files/motion-principles/easing-curves.html"),
]
USE = {
    "Logo_Animations": "Logo reveal (4 s) in four formats and two pairings; logo outro (3 s); seamless symbol loop and the presentation logo with alpha.",
    "Intros_Outros": "Branded intro and end card (6 s) in 16:9 and 9:16; the beam-wipe transition with alpha and a preview of it carrying a cut.",
    "Social_Animations": "Three stories (6 s), two posts (5 s) and the stat counter (5 s). MP4 for the platforms, GIF for previews and messaging.",
    "Lower_Thirds": "Three lower thirds (5 s: in · hold · out) with alpha for the edit, each with an MP4 preview over an approved project image.",
    "Website_Loader": "The loader as CSS, SVG + SMIL, Lottie, GIF and MP4; the reveal-on-scroll snippet; a self-contained demo page.",
}

def source_for(name):
    for pre, src in SOURCE:
        if name.startswith(pre): return src
    return "—"

def probe(path):
    ext = path.rsplit(".", 1)[-1].lower()
    if ext in ("mp4", "webm", "mov", "gif"):
        j = json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", path], capture_output=True, text=True).stdout)
        v = next(s for s in j["streams"] if s["codec_type"] == "video")
        dur = float(j["format"].get("duration") or v.get("duration") or 0)
        fr = v.get("avg_frame_rate", "0/1"); num, den = fr.split("/"); fps = round(float(num) / float(den)) if float(den) else 0
        frames = v.get("nb_frames") or (round(dur * fps) if fps else "")
        codec = {"h264": "H.264", "vp9": "VP9", "prores": "ProRes 4444", "gif": "GIF"}.get(v["codec_name"], v["codec_name"])
        alpha = "alpha" if (v.get("pix_fmt", "").startswith("yuva") or any(k.lower() == "alpha_mode" and str(val) == "1" for k, val in v.get("tags", {}).items())) and ext != "gif" else ""
        prof = v.get("profile", "");
        if v["codec_name"] == "prores": codec = "ProRes 4444"
        return f"{v['width']}×{v['height']}", f"{dur:.1f} s · {frames} f · {fps} fps", (codec + (" · " + alpha if alpha else "") + (f" · {v.get('pix_fmt')}" if ext in ("mp4", "webm", "mov") else "")).strip()
    if ext in ("png", "jpg", "jpeg", "webp"):
        from PIL import Image
        im = Image.open(path); return f"{im.width}×{im.height}", "", {"png": "PNG" + (" · alpha" if im.mode == "RGBA" else ""), "jpg": "JPEG q90", "jpeg": "JPEG", "webp": "WebP"}[ext]
    if ext == "svg":
        s = open(path).read(); m = re.search(r'viewBox="([^"]+)"', s); return (m.group(1).replace(" ", " ") if m else ""), "", "SVG" + (" + SMIL" if "<animate" in s else "")
    if ext == "json":
        j = json.load(open(path)); return f"{j['w']}×{j['h']}", f"{j['op']/j['fr']:.1f} s · {j['op']} f · {j['fr']} fps", "Lottie JSON (bodymovin 5.7)"
    return "", "", {"css": "CSS", "js": "JavaScript", "html": "HTML", "md": "Markdown"}.get(ext, ext.upper())

def human(n): return f"{n/1048576:.2f} MB" if n >= 1048576 else f"{n/1024:.0f} KB"

def table(folder):
    rows = ["| File | Pixels | Length | Format | Size | Editable from |", "|---|---|---|---|---|---|"]
    files = sorted(f for f in os.listdir(os.path.join(ROOT, folder)) if not f.startswith(".") and f != "README.md" and os.path.isfile(os.path.join(ROOT, folder, f)))
    total = 0
    for f in files:
        p = os.path.join(ROOT, folder, f); px, ln, fmt = probe(p); sz = os.path.getsize(p); total += sz
        rows.append(f"| `{f}` | {px} | {ln} | {fmt} | {human(sz)} | `{source_for(f)}` |")
    return "\n".join(rows), total, len(files)

if __name__ == "__main__":
    out = []; grand = 0; count = 0
    for folder in ["Logo_Animations", "Intros_Outros", "Social_Animations", "Lower_Thirds", "Website_Loader"]:
        t, total, n = table(folder); grand += total; count += n
        out.append(f"### `{folder}/` — {n} files, {human(total)}\n\n{USE[folder]}\n\n{t}\n")
    # Exports: summarise by subfolder
    ex = ["### `Exports/`\n", "| Folder | Contents | Files | Size | Produced by |", "|---|---|---|---|---|"]
    for sub, what, by in [("Key_Frames", "six key frames per rendered animation (960 px JPG q90, PNG with alpha for transparent pieces), one folder per animation", "`Source_Files/render.sh`"),
                          ("Contact_Sheets", "one contact sheet per deliverable folder and one master sheet of every animation", "`Source_Files/build_contact_sheets.py`"),
                          ("Lottie_Proofs", "frames of the two Lottie files rendered by lottie-web in Chromium, with a labelled proof strip each", "`Source_Files/lottie/validate_lottie.js`"),
                          ("Motion_Principles", "the easing-curve and timing-scale diagram used in Motion_Principles.md (3200×2000 PNG)", "`Source_Files/motion-principles/easing-curves.html` via render.js")]:
        fs = [p for p in glob.glob(os.path.join(ROOT, "Exports", sub, "**", "*"), recursive=True) if os.path.isfile(p)]
        sz = sum(os.path.getsize(p) for p in fs); grand += sz; count += len(fs)
        ex.append(f"| `Exports/{sub}/` | {what} | {len(fs)} | {human(sz)} | {by} |")
    out.append("\n".join(ex) + "\n")
    src = [p for p in glob.glob(os.path.join(ROOT, "Source_Files", "**", "*"), recursive=True) if os.path.isfile(p)]
    ssz = sum(os.path.getsize(p) for p in src); grand += ssz; count += len(src)
    for f in ("Motion_Principles.md", "README.md"):
        if os.path.exists(os.path.join(ROOT, f)): grand += os.path.getsize(os.path.join(ROOT, f)); count += 1
    out.append(f"`Source_Files/`: {len(src)} files, {human(ssz)} (of which lottie.min.js is {human(os.path.getsize(os.path.join(ROOT, 'Source_Files', 'lottie', 'lottie.min.js')))}).\n\n**Whole folder: {count} files, {human(grand)}.**\n")
    body = "\n".join(out)
    rp = os.path.join(ROOT, "README.md"); s = open(rp).read()
    s = re.sub(r"<!--@files-->.*?<!--@/files-->", "<!--@files-->\n" + body + "<!--@/files-->", s, flags=re.S)
    open(rp, "w").write(s); print(f"README tables written: {count} files, {human(grand)}")
