"""common.py — helpers shared by every build script in 10_MARKETING_COLLATERAL/_shared/build.
Paths, the standard HTML head, logo/image path builders, and wrappers around the brand-kit tools
(render.js, print_pdf.py) plus pdftoppm / Pillow for previews."""
import os, subprocess, json, tempfile, html as _html
from PIL import Image, ImageOps

B = "/home/user/claude-skills/BRAND_PACKAGE"
MC = f"{B}/10_MARKETING_COLLATERAL"
KIT = f"{B}/15_SOURCE_FILES/Project_Files/brand-kit"
RENDER = f"{KIT}/render.js"
BATCH = f"{MC}/_shared/build/render_batch.js"
PRINT_PDF = f"{KIT}/print_pdf.py"
IMG = f"{B}/00_ORIGINAL_ASSETS_BACKUP/images/img"
PORTRAIT = f"{B}/00_ORIGINAL_ASSETS_BACKUP/images/portrait-sanzeed-mirza-1100x1574.jpg"
LOGO_SVG = f"{B}/02_LOGO_SYSTEM/SVG"

# relative prefixes from <Sub>/src/*.html
REL_B = "../../.."          # BRAND_PACKAGE
REL_MC = "../.."            # 10_MARKETING_COLLATERAL

def esc(s): return _html.escape(s, quote=False)

def head(title, theme="dark", extra_css="", rel_b=REL_B, rel_mc=REL_MC, page_css=""):
    """Standard head: brand.css + collateral.css, theme attribute, optional inline CSS."""
    return f"""<!doctype html>
<html lang="en" data-theme="{theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{rel_b}/15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<link rel="stylesheet" href="{rel_mc}/_shared/collateral.css">
<style>
{page_css}
{extra_css}
</style>
</head>
"""

def logo(variant="primary-wordmark", colour="full-colour-dark", rel_b=REL_B):
    return f"{rel_b}/02_LOGO_SYSTEM/SVG/sanzeed-{variant}--{colour}.svg"

def img(name, rel_b=REL_B):
    """Project image by stem, e.g. 'prime-minister-museum' or 'case/ram-katha-show-03'."""
    return f"{rel_b}/00_ORIGINAL_ASSETS_BACKUP/images/img/{name}.webp"

def shared_img(name, rel_mc=REL_MC):
    return f"{rel_mc}/_shared/img/{name}"

def icon(name, rel_mc=REL_MC):
    return f"{rel_mc}/_shared/icons/{name}.svg"

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(text)
    return path

def run(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 and check:
        raise RuntimeError(f"{' '.join(map(str, cmd))}\n{r.stdout}\n{r.stderr}")
    return r

def render_jobs(jobs):
    """Render a list of jobs (dicts as render.js flags) in one browser."""
    if not jobs: return
    for j in jobs: os.makedirs(os.path.dirname(j["out"]), exist_ok=True)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False); json.dump(jobs, tmp); tmp.close()
    r = run(["node", BATCH, tmp.name]); os.remove(tmp.name)
    bad = [l for l in (r.stderr or "").splitlines() if "[pageerror]" in l or "[requestfailed]" in l]
    if bad: print("\n".join(bad))

def png(html, out, w, h, scale=2, full=False, selector=None, transparent=False, wait=300):
    j = dict(**{"in": html}, out=out, width=w, height=h, scale=scale, wait=wait)
    if full: j["full"] = True
    if selector: j["selector"] = selector
    if transparent: j["transparent"] = True
    return j

def pdf(html, out, w_mm, h_mm, landscape=False, wait=500):
    j = dict(**{"in": html}, out=out, pdf=True, size=f"{w_mm}x{h_mm}", wait=wait)
    if landscape: j["landscape"] = True
    return j

def print_ready(src_pdf, out_pdf, trim, bleed=3, cmyk=True):
    cmd = ["python3", PRINT_PDF, src_pdf, out_pdf, f"--trim={trim}", f"--bleed={bleed}"]
    if cmyk: cmd.append("--cmyk")
    run(cmd); return out_pdf

def pdf_pages_png(pdf_path, out_prefix, dpi=60, first=None, last=None):
    cmd = ["pdftoppm", "-r", str(dpi), "-png"]
    if first: cmd += ["-f", str(first)]
    if last: cmd += ["-l", str(last)]
    run(cmd + [pdf_path, out_prefix])
    d = os.path.dirname(out_prefix) or "."; base = os.path.basename(out_prefix)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.startswith(base + "-") and f.endswith(".png"))

def pdfinfo(pdf_path):
    r = run(["pdfinfo", pdf_path]); return r.stdout

def page_sizes(pdf_path):
    from pypdf import PdfReader
    rd = PdfReader(pdf_path)
    return [(round(float(p.mediabox.width)/72*25.4, 1), round(float(p.mediabox.height)/72*25.4, 1)) for p in rd.pages]

def to_jpg(png_path, jpg_path, quality=88, width=None, bg=(0, 0, 0)):
    im = Image.open(png_path)
    if im.mode in ("RGBA", "LA", "P"):
        base = Image.new("RGB", im.size, bg); base.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[3]); im = base
    else: im = im.convert("RGB")
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(jpg_path, quality=quality, subsampling=0, optimize=True); return jpg_path

def resize_png(png_path, out_path, width):
    im = Image.open(png_path); im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS); im.save(out_path, optimize=True); return out_path

def spreads(page_pngs, out_dir, stem, gap=0):
    """Combine single pages into reader spreads: [1], [2,3], [4,5] ... [last]."""
    os.makedirs(out_dir, exist_ok=True); outs = []
    pages = [Image.open(p) for p in page_pngs]; n = len(pages)
    groups = [[0]] + [[i, i + 1] for i in range(1, n - 1, 2)]
    if n % 2 == 0: groups.append([n - 1])
    for k, g in enumerate(groups):
        ims = [pages[i] for i in g]; w = sum(i.width for i in ims) + gap * (len(ims) - 1); h = max(i.height for i in ims)
        sp = Image.new("RGB", (w, h), (0, 0, 0)); x = 0
        for i in ims: sp.paste(i.convert("RGB"), (x, 0)); x += i.width + gap
        label = "cover" if k == 0 else ("back" if len(g) == 1 else f"p{g[0]+1:02d}-{g[1]+1:02d}")
        out = os.path.join(out_dir, f"{stem}--spread-{k:02d}-{label}.png"); sp.save(out, optimize=True); outs.append(out)
    return outs

def folder_size_mb(path):
    t = 0
    for root, _, files in os.walk(path):
        for f in files: t += os.path.getsize(os.path.join(root, f))
    return round(t / 1e6, 1)

def jimg(name, rel_mc=REL_MC, q=82, width=1400):
    """JPEG copy of a project image (webp → jpg, q86) for PDF embedding; cached in _shared/img/jpg/."""
    out_dir = f"{MC}/_shared/img/jpg"; os.makedirs(out_dir, exist_ok=True)
    stem = name.replace("/", "--"); out = f"{out_dir}/{stem}.jpg"
    if not os.path.exists(out):
        im = Image.open(f"{IMG}/{name}.webp").convert("RGB")
        if im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(out, quality=q, subsampling=0, optimize=True)
    return f"{rel_mc}/_shared/img/jpg/{stem}.jpg"
