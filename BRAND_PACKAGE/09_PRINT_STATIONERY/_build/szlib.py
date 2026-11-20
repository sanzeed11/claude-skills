#!/usr/bin/env python3
"""szlib.py — shared helpers for the Sanzeed print-stationery build.

Every SVG master in 09_PRINT_STATIONERY is written in millimetres (1 user unit = 1 mm) with
three Inkscape layers: `paper` (background), `artwork` (editable text + embedded logo paths) and
`guides` (trim / bleed / safe, stripped before export). Exports go through Inkscape (text → paths),
pypdf (trim crop), pdftoppm (PNG previews) and the kit's print_pdf.py (crop marks, boxes, CMYK).
"""
import glob
import os
import re
import shutil
import subprocess
import tempfile

B = '/home/user/claude-skills/BRAND_PACKAGE'
KIT = f'{B}/15_SOURCE_FILES/Project_Files/brand-kit'
OUT = f'{B}/09_PRINT_STATIONERY'
LOGO_DIR = f'{B}/02_LOGO_SYSTEM/SVG'
LOGO_PNG = f'{B}/02_LOGO_SYSTEM/PNG'
SIG_DIR = f'{B}/02_LOGO_SYSTEM/Signature'
IMG_DIR = f'{B}/00_ORIGINAL_ASSETS_BACKUP/images/img'
ASSETS = f'{OUT}/_build/assets'
os.makedirs(ASSETS, exist_ok=True)

PT = 0.352778  # mm per point

C = dict(
    black='#000000', night='#0D0D0F', charcoal='#1C1C1E', graphite='#2A2A2D', mist='#808086',
    silver='#A1A1A6', gwhite='#F5F5F7', plaster='#F5F0E7', paper='#FBF8F2', stone='#ECE7DC',
    umber='#665F55', soot='#1A1816', lamp='#E9B25A', lamplight='#F4C97A', oldgold='#B8863B',
    amber='#D9A64A', goldink='#8A6124',
)
LINE_LIGHT = ('#1A1816', 0.10)   # hairline on light (Soot at 10 %)
LINE_DARK = ('#FFFFFF', 0.10)    # hairline on dark (white at 10 %)

CONTACT = dict(name='Sanzeed Mirza', descriptor='Experiential Design Consultant',
               phone='+91 7827051270', email='sanzeed@gmail.com', web='sanzeed.com',
               linkedin='linkedin.com/in/sanzeed', city='New Delhi, India')
MASTER = 'Experiential design you can walk into'  # add the point separately
SHORT = 'Vision you can walk into'

# ----------------------------------------------------------------------------- logos

_logo_cache = {}


def _read_logo_svg(path):
    """Raw SVG text of a logo file. The synthetic name `sanzeed-horizontal-descriptor-plain--<colour>.svg`
    is the horizontal-descriptor lockup with its wordmark swapped for `wordmark-plain` (no points, Z ring and
    D stem closed) — same geometry and viewBox; used where the Z ring gap would close up (rubber stamps)."""
    m = re.search(r'sanzeed-horizontal-descriptor-plain--([a-z-]+)\.svg$', path)
    if not m:
        return open(path, encoding='utf-8').read()
    colour = m.group(1)
    lock = open(f'{LOGO_DIR}/sanzeed-horizontal-descriptor--{colour}.svg', encoding='utf-8').read()
    plain = open(f'{LOGO_DIR}/sanzeed-wordmark-plain--{colour}.svg', encoding='utf-8').read()
    plain_wm = re.search(r'<g\s+id="wordmark">.*?</g>\s*</g>', plain, flags=re.S).group(0)
    # the lockup's wordmark group = ink group + dots group; replace it with the plain wordmark group
    return re.sub(r'<g\s+id="wordmark">.*?id="wordmark-dots".*?</g>\s*</g>', lambda _: plain_wm, lock, count=1, flags=re.S)


def _load_logo(path):
    if path in _logo_cache:
        return _logo_cache[path]
    s = _read_logo_svg(path)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1).split()
    vx, vy, vw, vh = [float(v) for v in vb]
    body = re.sub(r'^.*?<svg[^>]*>', '', s, count=1, flags=re.S)
    body = re.sub(r'<title>.*?</title>', '', body, flags=re.S)
    body = re.sub(r'<desc>.*?</desc>', '', body, flags=re.S)
    body = re.sub(r'</svg>\s*$', '', body, flags=re.S)
    _logo_cache[path] = (vx, vy, vw, vh, body.strip())
    return _logo_cache[path]


def logo(variant, colour, width_mm, x, y, prefix='lg'):
    """Embed a logo SVG from 02_LOGO_SYSTEM at width_mm with its top-left at (x, y) mm.
    Returns (svg_group_string, height_mm, cap_height_mm)."""
    vx, vy, vw, vh, body = _load_logo(f'{LOGO_DIR}/sanzeed-{variant}--{colour}.svg')
    s = width_mm / vw
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', body)
    g = (f'<g id="{prefix}" inkscape:label="logo {variant} {colour}" '
         f'transform="translate({x:.4f} {y:.4f}) scale({s:.6f}) translate({-vx} {-vy})">{body}</g>')
    cap = cap_units() * s  # cap height = height of the wordmark letters (every variant shares it)
    return g, vh * s, cap


def cap_units():
    """Cap height of the approved wordmark in logo units, read from 02_LOGO_SYSTEM (primary wordmark viewBox
    height, ≈ 519.33). The symbol, monogram and lockups are drawn at the same letter height."""
    return _load_logo(f'{LOGO_DIR}/sanzeed-primary-wordmark--black.svg')[3]


def logo_size(variant, width_mm):
    """(height_mm, cap_height_mm) of a logo variant placed at width_mm — read from its viewBox."""
    vx, vy, vw, vh, _ = _load_logo(f'{LOGO_DIR}/sanzeed-{variant}--black.svg')
    s = width_mm / vw
    return vh * s, cap_units() * s


_ring_gap = None


def z_ring_gap_units():
    """Clear gap between the Z point and the surrounding stroke (the 'ring') of the primary wordmark, in logo
    units — measured on a 2-px-per-unit raster of the production SVG (≈ 13.7 units). Multiply by
    width_mm / viewBox width to get the gap at a given size."""
    global _ring_gap
    if _ring_gap is None:
        import cairosvg, io
        import numpy as np
        from PIL import Image
        path = f'{LOGO_DIR}/sanzeed-primary-wordmark--black.svg'
        src = open(path, encoding='utf-8').read()
        vx, vy, vw, vh, _ = _load_logo(path)
        dots = [tuple(float(v) for v in m) for m in
                re.findall(r'<circle\s+cx="([\d.]+)"\s+cy="([\d.]+)"\s+r="([\d.]+)"', src)]
        dots.sort()
        zx, zy, zr = dots[1]  # A, Z, D from left to right — the Z point is the middle one
        k = 2
        png = cairosvg.svg2png(bytestring=src.encode(), output_width=int(vw * k), background_color='white')
        a = np.array(Image.open(io.BytesIO(png)).convert('L'))
        y0, y1 = int((zy - 4 * zr) * k), int((zy + 4 * zr) * k)
        x0, x1 = int((zx - 4 * zr) * k), int((zx + 4 * zr) * k)
        win = a[y0:y1, x0:x1] < 128
        ys, xs = np.nonzero(win)
        d = np.hypot(xs + x0 - zx * k, ys + y0 - zy * k) / k
        _ring_gap = float(d[d > zr + 1].min() - zr)
    return _ring_gap


def signature(colour, width_mm, x, y, prefix='sig'):
    vx, vy, vw, vh, body = _load_logo(f'{SIG_DIR}/sanzeed-signature--{colour}.svg')
    s = width_mm / vw
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}-{m.group(1)}"', body)
    g = (f'<g id="{prefix}" inkscape:label="signature {colour}" '
         f'transform="translate({x:.4f} {y:.4f}) scale({s:.6f}) translate({-vx} {-vy})">{body}</g>')
    return g, vh * s


# ----------------------------------------------------------------------------- text

FAM = dict(display="Fraunces", heading="Inter Tight", text="Inter")


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def text(x, y, s, pt, fam='text', weight=400, fill=None, anchor='start', italic=False, ls=0,
         opsz=None, tnum=False, upper=False, extra=''):
    """One editable <text> line. pt = size in points; ls = letter-spacing in em."""
    size = pt * PT
    fill = fill or C['soot']
    family = f"'{FAM[fam]}'"
    if fam == 'display':
        # Inkscape ignores font-variation-settings, so the optical size is carried by static
        # instances (Fraunces 36pt / 72pt, see make_font_instances.py); the variable font is the fallback.
        o = opsz or (144 if pt >= 36 else 72 if pt >= 18 else 36)
        family = "'Fraunces'" if o >= 144 else f"'Fraunces {o}pt','Fraunces'"
    style = [f"font-family:{family}", f'font-weight:{weight}', f'font-size:{size:.4f}px',
             f'fill:{fill}', 'line-height:1']
    if italic:
        style.append('font-style:italic')
    if fam == 'display':
        style.append(f"font-variation-settings:'opsz' {o},'SOFT' 30,'WONK' 0")
    if ls:
        style.append(f'letter-spacing:{ls * size:.4f}px')
    if tnum:
        style.append("font-variant-numeric:tabular-nums")
        style.append("font-feature-settings:'tnum'")
    if upper:
        s = s.upper()
    ta = {'start': 'start', 'middle': 'middle', 'end': 'end'}[anchor]
    return (f'<text x="{x:.4f}" y="{y:.4f}" text-anchor="{ta}" xml:space="preserve" '
            f'style="{";".join(style)}" {extra}>{esc(s)}</text>')


def text_point(x, y, s, pt, point_fill, **kw):
    """A headline that ends with the gold point: the full stop is a tspan in point_fill."""
    kw.setdefault('fam', 'display'); kw.setdefault('weight', 300)
    t = text(x, y, s, pt, **kw)
    return t.replace(f'>{esc(s)}</text>', f'>{esc(s)}<tspan style="fill:{point_fill}">.</tspan></text>')


def eyebrow(x, y, s, pt=6.5, fill=None, anchor='start'):
    return text(x, y, s, pt, fam='heading', weight=600, fill=fill or C['goldink'], ls=0.12,
                upper=True, anchor=anchor)


def lines(x, y, items, pt, leading, **kw):
    """Several lines of the same style; leading in mm."""
    out = []
    for i, s in enumerate(items):
        out.append(text(x, y + i * leading, s, pt, **kw))
    return '\n'.join(out)


def hairline(x1, y1, x2, y2, dark=False, w=0.12, colour=None, opacity=None):
    col, op = (LINE_DARK if dark else LINE_LIGHT)
    if colour:
        col, op = colour, (1 if opacity is None else opacity)
    elif opacity is not None:
        op = opacity
    return (f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{col}" '
            f'stroke-opacity="{op}" stroke-width="{w}" />')


def beam(x1, y, x2, dark=False, point_at='start', r=0.6, w=0.12):
    """A hairline with the gold point at one end."""
    col = C['lamp'] if dark else C['oldgold']
    px = x1 if point_at == 'start' else x2
    return (hairline(x1, y, x2, y, dark=dark, w=w) +
            f'<circle cx="{px:.3f}" cy="{y:.3f}" r="{r}" fill="{col}" />')


def point(x, y, r, dark=False):
    return f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{C["lamp"] if dark else C["oldgold"]}" />'


def rect(x, y, w, h, fill='none', stroke='none', sw=0.12, rx=0, extra=''):
    return (f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')


def room(x, y, w, h, dark=False, rx=5, fill=None):
    """The 'room' — rounded rectangle with a hairline border (Charcoal on dark, Paper on light)."""
    f = fill or (C['charcoal'] if dark else C['paper'])
    col, op = (LINE_DARK if dark else LINE_LIGHT)
    return rect(x, y, w, h, fill=f, stroke=col, rx=rx, extra=f'stroke-opacity="{op}"')


def lamp_defs(id_='lamp', cx='50%', cy='40%', r='60%', strength=0.55):
    return (f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">'
            f'<stop offset="0" stop-color="#E9B25A" stop-opacity="{strength}"/>'
            f'<stop offset="0.28" stop-color="#E9B25A" stop-opacity="0.12"/>'
            f'<stop offset="0.7" stop-color="#E9B25A" stop-opacity="0"/></radialGradient>')


def image(href, x, y, w, h, extra=''):
    return (f'<image x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" '
            f'xlink:href="{href}" preserveAspectRatio="xMidYMid slice" {extra}/>')


def guides(trim_w, trim_h, bleed=3, safe=4, label=True):
    """Non-printing guides: bleed edge (red), trim (blue), safe area (green)."""
    bx, by, bw, bh = 0, 0, trim_w + 2 * bleed, trim_h + 2 * bleed
    g = []
    g.append(rect(bx + 0.06, by + 0.06, bw - 0.12, bh - 0.12, stroke='#C0392B', sw=0.12,
                  extra='stroke-dasharray="1 0.6"'))
    g.append(rect(bleed, bleed, trim_w, trim_h, stroke='#2F62A0', sw=0.12))
    g.append(rect(bleed + safe, bleed + safe, trim_w - 2 * safe, trim_h - 2 * safe,
                  stroke='#2E6E48', sw=0.12, extra='stroke-dasharray="0.6 0.6"'))
    # corner trim marks
    for (x, y, sx, sy) in [(bleed, bleed, -1, -1), (bleed + trim_w, bleed, 1, -1),
                           (bleed, bleed + trim_h, -1, 1), (bleed + trim_w, bleed + trim_h, 1, 1)]:
        g.append(f'<line x1="{x}" y1="{y}" x2="{x + sx * bleed}" y2="{y}" stroke="#2F62A0" stroke-width="0.12"/>')
        g.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + sy * bleed}" stroke="#2F62A0" stroke-width="0.12"/>')
    if label:
        g.append(text(bleed + 1, bleed + trim_h - 0.8, f'TRIM {trim_w:g} × {trim_h:g} mm · BLEED {bleed:g} mm · SAFE {safe:g} mm',
                      4, fam='heading', weight=500, fill='#2F62A0'))
    return '\n'.join(g)


# ----------------------------------------------------------------------------- documents

def svg_doc(w, h, paper_layer, artwork_layer, guides_layer='', defs='', title='', desc=''):
    """Compose an Inkscape-layered SVG in mm."""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
     xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
     width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" version="1.1">
  <title>{esc(title)}</title>
  <desc>{esc(desc)} Units: 1 user unit = 1 mm. Layers: paper, artwork, guides (non-printing). Fonts: Fraunces 300, Inter Tight 600, Inter 400 (04_TYPOGRAPHY/Font_Files). Logo paths embedded from 02_LOGO_SYSTEM/SVG.</desc>
  <sodipodi:namedview inkscape:document-units="mm" showgrid="false" />
  <defs>{defs}</defs>
  <g inkscape:groupmode="layer" inkscape:label="paper" id="layer-paper">
{paper_layer}
  </g>
  <g inkscape:groupmode="layer" inkscape:label="artwork" id="layer-artwork">
{artwork_layer}
  </g>
<!--GUIDES-->
  <g inkscape:groupmode="layer" inkscape:label="guides (non-printing)" id="layer-guides" style="display:inline">
{guides_layer}
  </g>
<!--/GUIDES-->
</svg>
'''


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f'{cmd[0]} failed: {r.stderr[-2000:]}')
    return r


def inkscape(args):
    r = subprocess.run(['inkscape', *args], capture_output=True, text=True)
    err = '\n'.join(l for l in r.stderr.splitlines() if 'Gtk' not in l and 'Fontconfig' not in l and l.strip())
    if r.returncode != 0:
        raise RuntimeError('inkscape failed: ' + err)
    return err


def strip_guides(svg_path):
    s = open(svg_path, encoding='utf-8').read()
    s = re.sub(r'<!--GUIDES-->.*?<!--/GUIDES-->', '', s, flags=re.S)
    tmp = tempfile.NamedTemporaryFile(suffix='.svg', delete=False, dir=os.path.dirname(svg_path) or '.').name
    open(tmp, 'w', encoding='utf-8').write(s)
    return tmp


def svg_to_pdf(svg_path, pdf_path, outline=True):
    """Inkscape export; text converted to outlines so the PDF needs no fonts."""
    tmp = strip_guides(svg_path)
    try:
        args = [tmp, '--export-type=pdf', f'--export-filename={pdf_path}']
        if outline:
            args.append('--export-text-to-path')
        inkscape(args)
    finally:
        os.remove(tmp)
    return pdf_path


def svg_to_outlined_svg(svg_path, out_path):
    tmp = strip_guides(svg_path)
    try:
        inkscape([tmp, '--export-type=svg', '--export-plain-svg', '--export-text-to-path',
                  f'--export-filename={out_path}'])
    finally:
        os.remove(tmp)
    return out_path


def svg_to_png(svg_path, png_path, width_px=None, dpi=None, keep_guides=False):
    tmp = svg_path if keep_guides else strip_guides(svg_path)
    try:
        args = [tmp, '--export-type=png', f'--export-filename={png_path}']
        if width_px:
            args.append(f'--export-width={int(width_px)}')
        elif dpi:
            args.append(f'--export-dpi={dpi}')
        inkscape(args)
    finally:
        if tmp != svg_path:
            os.remove(tmp)
    return png_path


def merge_pdfs(paths, out):
    from pypdf import PdfWriter
    w = PdfWriter()
    for p in paths:
        w.append(p)
    w.write(out)
    return out


def crop_pdf(src, dst, bleed_mm):
    """Crop every page of a bleed-size PDF to its trim box (all boxes set to the trim)."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject
    b = bleed_mm * 72 / 25.4
    r = PdfReader(src)
    w = PdfWriter()
    for pg in r.pages:
        mb = pg.mediabox
        box = RectangleObject([float(mb.left) + b, float(mb.bottom) + b, float(mb.right) - b, float(mb.top) - b])
        pg.mediabox = box
        pg.cropbox = box
        pg.trimbox = box
        pg.bleedbox = box
        w.add_page(pg)
    w.write(dst)
    return dst


def pdf_to_png(pdf, out_png, dpi=150, page=1):
    """Rasterise one page with pdftoppm (poppler) → out_png."""
    base = tempfile.mkdtemp()
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', '-f', str(page), '-l', str(page), pdf, f'{base}/p'],
                   check=True, capture_output=True)
    files = sorted(glob.glob(f'{base}/p*.png'))
    shutil.move(files[0], out_png)
    shutil.rmtree(base)
    return out_png


def pdf_to_jpg(pdf, out_jpg, dpi=150, page=1, quality=88):
    from PIL import Image
    tmp = out_jpg + '.png'
    pdf_to_png(pdf, tmp, dpi=dpi, page=page)
    Image.open(tmp).convert('RGB').save(out_jpg, quality=quality, subsampling=0)
    os.remove(tmp)
    return out_jpg


def pdf_pages_to_png(pdf, out_prefix, dpi=110):
    base = tempfile.mkdtemp()
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', pdf, f'{base}/p'], check=True, capture_output=True)
    outs = []
    for i, f in enumerate(sorted(glob.glob(f'{base}/p*.png')), 1):
        o = f'{out_prefix}-{i:02d}.png'
        shutil.move(f, o)
        outs.append(o)
    shutil.rmtree(base)
    return outs


def print_ready(bleed_pdf, out_pdf, trim_w, trim_h, bleed=3, cmyk=True):
    cmd = ['python3', f'{KIT}/print_pdf.py', bleed_pdf, out_pdf, f'--trim={trim_w:g}x{trim_h:g}', f'--bleed={bleed:g}']
    if cmyk:
        cmd.append('--cmyk')
    run(cmd)
    return out_pdf


def pdfinfo(path):
    r = subprocess.run(['pdfinfo', path], capture_output=True, text=True)
    return r.stdout


def render_html(html, out, width=None, height=None, scale=2, pdf=False, size=None, landscape=False,
                full=False, transparent=False, selector=None, wait=500):
    cmd = ['node', f'{KIT}/render.js', '--in', html, '--out', out, '--wait', str(wait)]
    if pdf:
        cmd += ['--pdf', '--size', size or '210x297']
        if landscape:
            cmd.append('--landscape')
    else:
        cmd += ['--width', str(width), '--height', str(height), '--scale', str(scale)]
        if full:
            cmd.append('--full')
        if transparent:
            cmd.append('--transparent')
        if selector:
            cmd += ['--selector', selector]
    run(cmd)
    return out


def soffice_pdf(doc, outdir):
    run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, doc])
    return os.path.join(outdir, os.path.splitext(os.path.basename(doc))[0] + '.pdf')


# ----------------------------------------------------------------------------- images

def jpg_from_webp(name, out, quality=88, crop=None, size=None, darken=0.0):
    """Convert a kit image to JPG. crop = 'w:h' aspect from the centre; size = (w, h) max."""
    from PIL import Image, ImageEnhance
    src = f'{IMG_DIR}/{name}.webp'
    im = Image.open(src).convert('RGB')
    if crop:
        aw, ah = [float(v) for v in crop.split(':')]
        W, H = im.size
        if W / H > aw / ah:
            nw = int(H * aw / ah); x0 = (W - nw) // 2; im = im.crop((x0, 0, x0 + nw, H))
        else:
            nh = int(W * ah / aw); y0 = (H - nh) // 2; im = im.crop((0, y0, W, y0 + nh))
    if size:
        im = im.resize(size, Image.LANCZOS)
    if darken:
        im = ImageEnhance.Brightness(im).enhance(1 - darken)
    im.save(out, quality=quality, subsampling=0)
    return out


def png_from_webp(name, out, crop=None, size=None):
    from PIL import Image
    im = Image.open(f'{IMG_DIR}/{name}.webp').convert('RGB')
    if crop:
        aw, ah = [float(v) for v in crop.split(':')]
        W, H = im.size
        if W / H > aw / ah:
            nw = int(H * aw / ah); x0 = (W - nw) // 2; im = im.crop((x0, 0, x0 + nw, H))
        else:
            nh = int(W * ah / aw); y0 = (H - nh) // 2; im = im.crop((0, y0, W, y0 + nh))
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(out)
    return out


def qr_path(data, size_mm, x=0, y=0, ec='M'):
    """QR code as a single SVG path (modules as squares) sized to size_mm. Returns (path_element, modules)."""
    import qrcode
    from qrcode.constants import ERROR_CORRECT_M, ERROR_CORRECT_H
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H if ec == 'H' else ERROR_CORRECT_M, border=0, box_size=1)
    q.add_data(data)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    u = size_mm / n
    d = []
    for r, row in enumerate(m):
        for c, v in enumerate(row):
            if v:
                d.append(f'M{x + c * u:.3f} {y + r * u:.3f}h{u:.3f}v{u:.3f}h{-u:.3f}z')
    return ''.join(d), n


def mm_to_px(mm, dpi):
    return int(round(mm / 25.4 * dpi))


def size_mb(path):
    return os.path.getsize(path) / 1e6
