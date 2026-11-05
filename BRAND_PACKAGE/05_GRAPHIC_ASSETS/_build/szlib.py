#!/usr/bin/env python3
"""
szlib.py — shared helpers for every generator in 05_GRAPHIC_ASSETS.

  * brand colour tokens for the two inks (dark = on Gallery Black, light = on Plaster)
  * text_path(): outlines a string with the brand fonts (fontTools, variable-font
    instancing) so no SVG ever depends on an installed font
  * svg(): document wrapper with title/desc
  * export_svg(): calls the kit helper export_svg.py (Inkscape PDF, cairosvg PNG)
  * render_html(): calls the kit helper render.js (Chromium) for PNG / JPG / PDF

Every script in this folder imports it with:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '_build')); import szlib as sz
"""
import os, sys, subprocess, re
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                                  # BRAND_PACKAGE/
ASSETS = HERE.parent                                    # 05_GRAPHIC_ASSETS/
KIT = ROOT / '15_SOURCE_FILES' / 'Project_Files' / 'brand-kit'
FONTS = ROOT / '04_TYPOGRAPHY' / 'Font_Files'
LOGOS = ROOT / '02_LOGO_SYSTEM' / 'SVG'
IMAGES = ROOT / '00_ORIGINAL_ASSETS_BACKUP' / 'images' / 'img'

# ------------------------------------------------------------------ colour tokens
INK = {
    'dark': dict(bg='#000000', bg2='#0D0D0F', card='#1C1C1E', card2='#2A2A2D',
                 ink='#F5F5F7', ink2='#A1A1A6', ink3='#808086',
                 gold='#E9B25A', gold2='#F4C97A', gold_text='#E9B25A',
                 line='#FFFFFF', line_op=0.10, line2_op=0.06),
    'light': dict(bg='#F5F0E7', bg2='#FBF8F2', card='#FBF8F2', card2='#ECE7DC',
                  ink='#1A1816', ink2='#665F55', ink3='#6D665C',
                  gold='#B8863B', gold2='#D9A64A', gold_text='#8A6124',
                  line='#1A1816', line_op=0.10, line2_op=0.055),
}

# ------------------------------------------------------------------ text outlining
_FONT_FILES = {
    ('Fraunces', False): FONTS / 'Fraunces' / 'Fraunces[SOFT,WONK,opsz,wght].ttf',
    ('Fraunces', True):  FONTS / 'Fraunces' / 'Fraunces-Italic[SOFT,WONK,opsz,wght].ttf',
    ('Inter', False):    FONTS / 'Inter' / 'Inter[opsz,wght].ttf',
    ('Inter', True):     FONTS / 'Inter' / 'Inter-Italic[opsz,wght].ttf',
    ('Inter Tight', False): FONTS / 'Inter_Tight' / 'InterTight[wght].ttf',
    ('Inter Tight', True):  FONTS / 'Inter_Tight' / 'InterTight-Italic[wght].ttf',
}
_cache = {}

def _font(family, wght, opsz=None, italic=False):
    key = (family, wght, opsz, italic)
    if key in _cache: return _cache[key]
    vf = TTFont(str(_FONT_FILES[(family, italic)]))
    tags = [a.axisTag for a in vf['fvar'].axes]
    axes = {'wght': wght}
    if 'opsz' in tags: axes['opsz'] = opsz if opsz is not None else (144 if family == 'Fraunces' else 14)
    if 'SOFT' in tags: axes['SOFT'] = 30
    if 'WONK' in tags: axes['WONK'] = 0
    # clamp to axis ranges
    for a in vf['fvar'].axes:
        if a.axisTag in axes: axes[a.axisTag] = max(a.minValue, min(a.maxValue, axes[a.axisTag]))
    font = instantiateVariableFont(vf, axes)
    _cache[key] = font
    return font

def f(v):
    s = f"{v:.2f}"
    return s.rstrip('0').rstrip('.') if '.' in s else s

def text_path(text, family='Inter Tight', wght=600, size=16, opsz=None, italic=False,
              tracking=0.0, tnum=False, x=0, y=0, anchor='start'):
    """Outline `text` at font-size `size` (px) with the baseline at y and the start at x.
    Returns (d, advance_width, metrics) where metrics = dict(cap, xh, asc, desc) in px."""
    font = _font(family, wght, opsz, italic)
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm
    s = size / upm
    os2 = font['OS/2']
    metrics = dict(cap=(os2.sCapHeight or 0.7*upm)*s, xh=(os2.sxHeight or 0.5*upm)*s,
                   asc=font['hhea'].ascent*s, desc=-font['hhea'].descent*s)
    glyphs = []
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None: g = cmap.get(ord('?'))
        glyphs.append(g)
    # tabular numerals: use the widest digit for every digit
    if tnum:
        dig = [cmap[ord(c)] for c in '0123456789' if ord(c) in cmap]
        tw = max(gs[g].width for g in dig)
    widths = []
    for ch, g in zip(text, glyphs):
        w = gs[g].width
        if tnum and ch.isdigit(): w = tw
        widths.append(w)
    tr = tracking * size
    total = sum(w*s for w in widths) + tr*(len(text)-1 if len(text) else 0)
    x0 = x
    if anchor == 'middle': x0 = x - total/2
    elif anchor == 'end': x0 = x - total
    cx = x0; cmds = []
    for ch, g, w in zip(text, glyphs, widths):
        pen = SVGPathPen(gs)
        gx = cx + ((w - gs[g].width)*s/2 if (tnum and ch.isdigit()) else 0)
        tp = TransformPen(pen, (s, 0, 0, -s, gx, y))
        gs[g].draw(tp)
        d = pen.getCommands()
        if d: cmds.append(d)
        cx += w*s + tr
    return ' '.join(cmds), total, metrics

# ------------------------------------------------------------------ SVG helpers
def svg(w, h, body, title, desc='', extra_attr='', viewbox=None):
    import html
    title = html.escape(title, quote=True); desc = html.escape(desc, quote=False)
    vb = viewbox or f"0 0 {f(w)} {f(h)}"
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="{vb}" width="{f(w)}" height="{f(h)}" role="img" aria-label="{title}"{extra_attr}>\n'
            f'<title>{title}</title>\n<desc>{desc}</desc>\n{body}\n</svg>\n')

def write(path, content):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return path

def logo_body(variant, colour):
    """Return the inner markup + viewBox size of a production logo SVG, for embedding as a <g>."""
    p = LOGOS / f'sanzeed-{variant}--{colour}.svg'
    t = p.read_text(encoding='utf-8')
    vb = re.search(r'viewBox="([^"]+)"', t).group(1).split()
    w, h = float(vb[2]), float(vb[3])
    inner = t[t.index('<g'):t.rindex('</svg>')]
    # strip title/desc already excluded; strip ids to avoid duplicates when embedded twice
    inner = re.sub(r'\s+id="[^"]*"', '', inner)
    return inner, w, h

def logo_group(variant, colour, x, y, width, gid='logo'):
    inner, w, h = logo_body(variant, colour)
    s = width / w
    return (f'<g id="{gid}" transform="translate({f(x)} {f(y)}) scale({f(s)})">{inner}</g>', width, h*s)

# ------------------------------------------------------------------ exports
def export_svg(src, out_base, png=(2000,), formats='pdf,png'):
    cmd = ['python3', str(KIT / 'export_svg.py'), str(src), str(out_base), f'--png={",".join(str(p) for p in png)}', f'--formats={formats}']
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0: print(r.stdout, r.stderr, file=sys.stderr)
    return r.returncode == 0

def render_html(src, out, width, height, scale=1, transparent=False, full=False, selector=None, wait=400, pdf=None, landscape=False):
    cmd = ['node', str(KIT / 'render.js'), '--in', str(src), '--out', str(out), '--width', str(width), '--height', str(height), '--scale', str(scale), '--wait', str(wait)]
    if transparent: cmd.append('--transparent')
    if full: cmd.append('--full')
    if selector: cmd += ['--selector', selector]
    if pdf: cmd += ['--pdf', '--size', pdf]
    if landscape: cmd.append('--landscape')
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or 'pageerror' in r.stderr: print(r.stdout, r.stderr, file=sys.stderr)
    return r.returncode == 0

def png_to_jpg(png, jpg, quality=90, bg='#000000'):
    from PIL import Image
    im = Image.open(png)
    if im.mode in ('RGBA', 'LA'):
        base = Image.new('RGB', im.size, bg); base.paste(im, mask=im.split()[-1]); im = base
    else: im = im.convert('RGB')
    im.save(jpg, quality=quality, subsampling=0, optimize=True, progressive=True)

def svg_to_png(src, out, width, height=None):
    import cairosvg
    cairosvg.svg2png(url=str(src), write_to=str(out), output_width=width, output_height=height)
