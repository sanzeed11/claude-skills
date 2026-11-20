"""Shared helpers for the Brand Guidelines generator.

Every chapter module builds a list of page strings with these helpers. Paths given to L()/A() are
relative to the package root (BRAND_PACKAGE/). L() links an existing file by relative path from
Editable_Source/; A() copies a downsampled working copy into Editable_Source/assets/ (for large
rasters, so the PDF stays compact) and returns that relative path. Both raise if the file is missing,
so a missing asset fails the build instead of leaving an empty box.
"""
import os, re, json, html, hashlib
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)                       # Editable_Source/
ROOT = os.path.abspath(os.path.join(SRC, '..', '..'))   # BRAND_PACKAGE/
ASSETS = os.path.join(SRC, 'assets')
os.makedirs(ASSETS, exist_ok=True)

def esc(s): return html.escape(str(s), quote=False)

def L(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): raise FileNotFoundError(rel)
    return '../../' + rel

def A(rel, maxw=1600, maxh=None, quality=86, name=None, crop=None, bg=None):
    """Copy an image into assets/, resized so its long edge is <= maxw (or height <= maxh).
    crop = (left, top, right, bottom) in source pixels, applied before resizing. Returns 'assets/<file>'."""
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): raise FileNotFoundError(rel)
    base = name or os.path.splitext(os.path.basename(rel))[0]
    if crop: base += '--crop-' + hashlib.md5(str(crop).encode()).hexdigest()[:6]
    im = Image.open(p)
    if crop: im = im.crop(crop)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    ext = '.png' if has_alpha else '.jpg'
    out = os.path.join(ASSETS, base + ext)
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(p):   # refresh stale copies
        w, h = im.size
        s = min(1.0, maxw / w, (maxh / h) if maxh else 1.0)
        if s < 1: im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
        if has_alpha:
            im.convert('RGBA').save(out, optimize=True)
        else:
            im = im.convert('RGB')
            im.save(out, quality=quality, subsampling=0, optimize=True, progressive=True)
    return 'assets/' + base + ext

def ui_crop(name):
    """A UI-kit section rendered by build.py --ui into assets/ui/; referenced here, produced there."""
    return f'assets/ui/{name}.png'

# ---------------------------------------------------------------- page scaffolding
def page(section, body, cls='', attrs=''):
    return f'<section class="page {cls}" data-section="{esc(section)}" {attrs}>\n{body}\n</section>\n'

def head(eyebrow, title, lead='', solo=False):
    lead_html = f'<p class="doc-lead">{lead}</p>' if lead else '<div></div>'
    return (f'<header class="ph{" solo" if solo else ""}"><div><span class="eyebrow">{esc(eyebrow)}</span>'
            f'<h2 class="doc-title">{title}</h2></div>{lead_html}</header>')

def body(inner, cls=''):
    return f'<div class="body {cls}">{inner}</div>'

def lit(text):
    """Set the last word of a sentence-case headline in gold (the .lit convention)."""
    m = re.match(r'^(.*\s)(\S+?)([.!?]?)$', text.strip())
    if not m: return esc(text)
    return f'{esc(m.group(1))}<span class="lit">{esc(m.group(2))}</span>{esc(m.group(3))}'

def wl(title, place=None, line=None, src=None):
    out = f'<span class="title">{esc(title)}</span>'
    if place: out += f'<span class="place">{esc(place)}</span>'
    if line: out += f'<span class="line">{line}</span>'
    if src: out += f'<span class="src">{esc(src)}</span>'
    return f'<figcaption class="wall-label">{out}</figcaption>'

def fig(src, title=None, place=None, line=None, plate='', h='h40', note=None, alt='', badge='', extra='', cls=''):
    """A figure: plate (fixed height, object-fit contain) + wall label."""
    cap = wl(title, place, line, note) if title else ''
    return (f'<figure class="fig {cls}"><div class="plate {plate} {h}">{extra}<img src="{src}" alt="{esc(alt or title or "")}">{badge}</div>{cap}</figure>')

def plate(src, plate='', h='h40', alt='', extra='', badge=''):
    return f'<div class="plate {plate} {h}">{extra}<img src="{src}" alt="{esc(alt)}">{badge}</div>'

def table(headers, rows, cls='', widths=None):
    th = ''.join(f'<th{" class=num" if hh.startswith("#") else ""}>{esc(hh.lstrip("#"))}</th>' for hh in headers)
    cg = ''
    if widths: cg = '<colgroup>' + ''.join(f'<col style="width:{w}">' for w in widths) + '</colgroup>'
    trs = ''
    for r in rows:
        tds = ''.join(f'<td>{c}</td>' for c in r)
        trs += f'<tr>{tds}</tr>'
    return f'<table class="doc {cls}">{cg}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def rules(items, cls=''):
    # each li is a 2-column grid (counter + text): wrap the content in one span so mixed text/<b> runs stay together
    return '<ol class="rules ' + cls + '">' + ''.join(f'<li><span>{i}</span></li>' for i in items) + '</ol>'

def divider(num, title, lead, items, section):
    """The dark chapter divider: counter, Fraunces title, lead, and the chapter's contents."""
    wm = L('02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg')
    lis = ''.join(f'<li><span>{esc(k)}</span>{esc(v)}</li>' for k, v in items)
    inner = (f'<div class="op-top"><div class="op-num"><small>Chapter</small>{num}</div><div class="wm"><img src="{wm}" alt="Sanzeed"></div></div>'
             f'<div class="op-main"><div><h1 class="opener-title op-title">{title}</h1><p class="op-lead">{lead}</p></div>'
             f'<ol class="op-list">{lis}</ol></div>'
             f'<div class="op-foot"><span>Sanzeed Mirza · Experiential Design Consultant</span><span>Brand Guidelines · Version 1.0 · November 2026</span></div>')
    return page(section, inner, cls='opener theme-dark')

def chapter_file(num, slug, title, pages):
    """Wrap a chapter's pages as a standalone HTML document (opens in a browser on its own)."""
    doc = ('<!doctype html>\n<html lang="en" data-theme="light">\n<head>\n<meta charset="utf-8">\n'
           f'<title>Sanzeed — Brand Guidelines — {esc(num)} {esc(title)}</title>\n'
           '<link rel="stylesheet" href="guide.css">\n</head>\n<body>\n<main class="doc" style="--doc:\'Brand Guidelines\'">\n'
           '<!-- chapter:start -->\n' + ''.join(pages) + '<!-- chapter:end -->\n</main>\n</body>\n</html>\n')
    fn = f'{num}-{slug}.html'
    with open(os.path.join(SRC, fn), 'w') as f: f.write(doc)
    return fn, len(pages)

# ---------------------------------------------------------------- data
def tokens():
    with open(os.path.join(ROOT, '03_COLOUR_SYSTEM/colour-tokens.json')) as f: return json.load(f)
def typo():
    with open(os.path.join(ROOT, '04_TYPOGRAPHY/typography-tokens.json')) as f: return json.load(f)
def approved():
    with open(os.path.join(ROOT, '06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/approved.json')) as f: return json.load(f)

SVG = '02_LOGO_SYSTEM/SVG/'
def logo(variant, colour): return L(f'{SVG}sanzeed-{variant}--{colour}.svg')

CONTACT = 'sanzeed@gmail.com · +91 7827051270 · linkedin.com/in/sanzeed · sanzeed.com · New Delhi, India'
