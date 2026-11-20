#!/usr/bin/env python3
"""build_site.py — applies the refined Sanzeed identity to the live-site source.

Input : 00_ORIGINAL_ASSETS_BACKUP/site_source/{index.html, work/*.html, sitemap.xml}
Output: 16_WEBSITE_IMPLEMENTATION/{index.html, work/*.html, sitemap.xml}

Every edit is a targeted string/regex replacement on the original markup, so the
site's CSS, JS (GSAP, Lenis, three.js hero, galleries, enquiry form) stays byte-for-byte
the same apart from the items listed in CHANGES.md.  Re-run after editing this file:

    python3 16_WEBSITE_IMPLEMENTATION/src/build_site.py

The wordmark / lockup artwork is read live from 02_LOGO_SYSTEM/SVG, the colour tokens
from 03_COLOUR_SYSTEM/colour-variables.css, so a logo or palette change upstream only
needs a rebuild here.
"""
import re, pathlib, sys, json

B   = pathlib.Path(__file__).resolve().parents[2]          # BRAND_PACKAGE
SRC = B / '00_ORIGINAL_ASSETS_BACKUP' / 'site_source'
OUT = B / '16_WEBSITE_IMPLEMENTATION'
LOGO = B / '02_LOGO_SYSTEM' / 'SVG'
TOKENS = B / '03_COLOUR_SYSTEM' / 'colour-variables.css'
TODAY = '2026-11-20'

# ---------------------------------------------------------------- artwork
# Approved logo (20 Nov 2026): the refined original wordmark, option B — three gold points (A, Z, D), the Z point in
# its ring. Header + loader use the per-letter raw master (same 3729 × 561 viewBox as the live site's hand-traced
# wordmark); the footer lockup uses the unioned production horizontal-descriptor from 02_LOGO_SYSTEM/SVG.
MASTER = B / '15_SOURCE_FILES' / 'Project_Files' / 'logo-builder' / 'refined_master.svg'

def master_wordmark(path):
    """Return (viewBox w, h, [(letter, d)], dots [(cx,cy,r)]) from the raw master (paths id="wm-S" … "wm-D")."""
    s = path.read_text()
    w, h = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()
    letters = re.findall(r'<path id="wm-([A-Z0-9]+)" d="([^"]+)"', s)
    dots = re.findall(r'<circle class="wm-dot" cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', s)
    return w, h, letters, dots

def svg_paths(path):
    """Return (viewBox, ink path d, dots [(cx,cy,r)], descriptor path ds) from a production SVG."""
    s = path.read_text()
    s = re.sub(r'\s+', ' ', s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    ink = re.search(r'id="wordmark-ink"[^>]*>(.*?)</g>', s).group(1)
    ink_d = ' '.join(d.strip() for d in re.findall(r'(?<=\s)d="([^"]+)"', ink))   # (?<=\s) so id="…" is not read as d="…"
    dots = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', s)
    desc = re.search(r'id="descriptor-text"[^>]*>(.*?)</g>', s)
    desc_ds = re.findall(r'(?<=\s)d="([^"]+)"', desc.group(1)) if desc else []
    return vb, ink_d, dots, desc_ds

WM_W, WM_H, WM_LETTERS, WM_DOTS = master_wordmark(MASTER)
LK_VB, LK_D, LK_DOTS, LK_DESC = svg_paths(LOGO / 'sanzeed-horizontal-descriptor--full-colour-dark.svg')
assert (WM_W, WM_H) == ('3729', '561'), 'master viewBox changed: update the loader constant and the header height'
assert [l for l, _ in WM_LETTERS] == ['S', 'A', 'N', 'Z', 'E1', 'E2', 'D'], 'master letters not found'
assert len(WM_DOTS) == 3 and len(LK_DOTS) == 3 and len(LK_DESC) > 20, 'logo artwork not found (three points expected)'
assert LK_D.startswith('M') and all(d.startswith('M') for d in LK_DESC), 'path data must start with a moveto'
# DOM order of the points is A, D, Z (as in the master): the site's JS uses the first point (A) for the loader's
# landing dot and the first two (A, D) for the dots that fly into the services stage, exactly as with the old artwork.
BEAM_CY = max(WM_DOTS, key=lambda d: float(d[0]))[1]          # the beam dot travels at the D-point height (= the Z point)

def dots_markup(dots):
    return ''.join(f'<circle class="wm-dot" cx="{cx}" cy="{cy}" r="{r}"/>' for cx, cy, r in dots)

# letters as one group carrying class="wm-letters" (CSS fills it), one path per letter (data-letter instead of ids,
# so the loader and header copies on the same page do not duplicate ids)
WM_LETTERS_MARKUP = '<g class="wm-letters">' + ''.join(f'<path data-letter="{l}" d="{d}"/>' for l, d in WM_LETTERS) + '</g>'
# Header / footer wordmark — same class names and structure as the original inline SVG
WM_SVG = (f'<svg viewBox="0 0 {WM_W} {WM_H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="SANZEED">'
          f'{WM_LETTERS_MARKUP}{dots_markup(WM_DOTS)}</svg>')
# Loader wordmark — keeps the clip-path (#ldClip) and the travelling beam dot the JS animates
WM_SVG_LOADER = (f'<svg viewBox="0 0 {WM_W} {WM_H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="SANZEED">'
                 f'<defs><clipPath id="ldClip"><rect x="0" y="0" width="{WM_W}" height="{WM_H}"/></clipPath></defs>'
                 f'<g clip-path="url(#ldClip)">{WM_LETTERS_MARKUP}{dots_markup(WM_DOTS)}</g>'
                 f'<circle class="beam-dot" cx="0" cy="{BEAM_CY}" r="30"/></svg>')
# Footer lockup — horizontal descriptor (wordmark + "EXPERIENTIAL DESIGN CONSULTANT")
LOCKUP_SVG = (f'<div class="f-lockup"><svg viewBox="{LK_VB}" xmlns="http://www.w3.org/2000/svg" role="img" '
              'aria-label="Sanzeed — Experiential Design Consultant">'
              f'<path class="wm-letters" d="{LK_D}"/>{dots_markup(LK_DOTS)}'
              '<g class="wm-desc">' + ''.join(f'<path d="{d}"/>' for d in LK_DESC) + '</g></svg></div>\n  ')

# ---------------------------------------------------------------- colour tokens
tok = TOKENS.read_text()
palette = re.search(r':root \{(.*?)/\* Gradients', tok, re.S).group(1)
palette_lines = [l.strip() for l in palette.splitlines() if l.strip().startswith('--sz-')]
gradients = re.search(r'/\* Gradients \*/(.*?)/\* Semantic', tok, re.S).group(1)
gradient_lines = [l.strip() for l in gradients.splitlines() if l.strip().startswith('--sz-')]
def semantic(block):
    m = re.search(block + r'\s*\{(.*?)\}', tok, re.S).group(1)
    return dict(re.findall(r'(--[a-z0-9-]+):\s*([^;]+);', m))
TOK_DARK  = semantic(r':root')
TOK_LIGHT = semantic(r'html\[data-theme="light"\], \.theme-light')
# site variable name -> token name (the site keeps its names; values come from the token file)
MAP = {'--bg':'--bg','--bg2':'--bg-2','--card':'--card','--card2':'--card-2','--fg':'--fg','--fg2':'--fg-2','--fg3':'--fg-3',
       '--line':'--line','--line2':'--line-2','--accent':'--accent','--accent2':'--accent-2','--accent-ink':'--accent-ink',
       '--btn':'--btn','--btn-fg':'--btn-fg','--glass':'--glass','--veil':'--veil','--accent-text':'--accent-text'}
FUNCTIONAL = ['--success','--warning','--error','--info']

def retoken(block, tokens):
    """Rewrite the values of the site's own variables from the token set; report differences."""
    diffs = []
    def sub(m):
        name, old = m.group(1), m.group(2).strip()
        new = tokens.get(MAP[name])
        if new is None: return m.group(0)
        new = new.strip()
        if old.lower().replace(' ', '') != new.lower().replace(' ', ''): diffs.append((name, old, new))
        return f'{name}:{new};'
    block = re.sub(r'(--(?:bg2?|card2?|fg[23]?|line2?|accent2?|accent-ink|btn|btn-fg|glass|veil|accent-text)):([^;]+);', sub, block)
    return block, diffs

# ---------------------------------------------------------------- page transform
FAVICON_HEAD = ('<link rel="icon" href="/favicon.ico" sizes="48x48">'
                '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
                '<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
                '<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#0D0D0F">'
                '<link rel="manifest" href="/site.webmanifest">')
THEME_META = ('<meta name="theme-color" content="#F5F0E7" media="(prefers-color-scheme: light)">'
              '<meta name="theme-color" content="#0D0D0F" media="(prefers-color-scheme: dark)">')

def fontfaces(rel):
    f = rel + 'assets/fonts/'
    return (f'@font-face{{font-family:"Inter Tight";font-style:normal;font-weight:100 900;font-display:swap;src:url({f}InterTight-variable.woff2) format("woff2")}}'
            f'@font-face{{font-family:"Inter";font-style:normal;font-weight:100 900;font-display:swap;src:url({f}Inter-variable.woff2) format("woff2")}}'
            f'@font-face{{font-family:"Fraunces";font-style:normal;font-weight:100 900;font-display:swap;src:url({f}Fraunces-variable.woff2) format("woff2")}}'
            f'@font-face{{font-family:"Fraunces";font-style:italic;font-weight:100 900;font-display:swap;src:url({f}Fraunces-Italic-variable.woff2) format("woff2")}}')

def preloads(rel, tight=True):
    f = rel + 'assets/fonts/'
    names = ('Fraunces-variable.woff2', 'InterTight-variable.woff2', 'Inter-variable.woff2') if tight else ('Fraunces-variable.woff2', 'Inter-variable.woff2')
    return ''.join(f'<link rel="preload" href="{f}{n}" as="font" type="font/woff2" crossorigin>' for n in names)

CSS_ADDENDUM = '''
/* ---------- v8: brand system alignment (16_WEBSITE_IMPLEMENTATION/src/build_site.py) ---------- */
.f-lockup{margin:0 0 clamp(32px,4vw,56px)}
.f-lockup svg{width:min(320px,100%);height:auto;display:block;overflow:visible}
.f-lockup .wm-letters,.f-lockup .wm-desc{fill:var(--fg)}
.f-lockup .wm-dot{fill:var(--accent);transform-box:fill-box;transform-origin:center;animation:dotIdle 6s ease-in-out infinite}
/* three points (DOM order A, D, Z): the idle pulse runs left to right A → Z → D, A and D keep their old timing */
.f-lockup .wm-dot:nth-of-type(2){animation-delay:.35s}
.f-lockup .wm-dot:nth-of-type(3){animation-delay:.175s}
.foot .wm .wm-dot:nth-of-type(2){animation-delay:.35s}
.foot .wm .wm-dot:nth-of-type(3){animation-delay:.175s}
h1 .lit,h2 .lit,h3 .lit,.h1 .lit,.h2 .lit,.h3 .lit,.f-big .lit{color:var(--accent);font-style:normal}
h1 .dim,h2 .dim,h3 .dim,.h1 .dim,.h2 .dim,.h3 .dim,.f-big .dim{color:var(--fg3);font-style:normal}
h1,h2,.f-big,.numbers .v{font-variation-settings:"opsz" 144,"SOFT" 30,"WONK" 0}
h3,h4{font-variation-settings:"opsz" 72,"SOFT" 30,"WONK" 0}
.quote p{font-variation-settings:"opsz" 72,"SOFT" 50,"WONK" 0}
.sv-item .n{font-variation-settings:"opsz" 36,"SOFT" 30,"WONK" 0}
html.reduce .f-lockup .wm-dot{animation:none}
'''

OG = {  # slug -> (alt text)
 'prime-minister-museum': 'Prime Minister Museum, New Delhi — a case study by Sanzeed Mirza',
 'ram-katha-show':        'Ram Katha Show, Ayodhya — a case study by Sanzeed Mirza',
 'buddha-park':           'Buddha Park, Uttarakhand — a case study by Sanzeed Mirza',
}

def transform(html, rel, slug=None):
    log = []
    n0 = len(html)

    # 1. favicons: real files instead of data URIs; theme-color aligned with the kit
    html, k = re.subn(r'<link rel="icon"[^>]*>\s*', '', html); log.append(f'removed {k} data-URI icon links')
    html, k = re.subn(r'<link rel="apple-touch-icon"[^>]*>', FAVICON_HEAD, html); assert k == 1
    html, k = re.subn(r'<meta name="theme-color" content="#f5f0e7" media="\(prefers-color-scheme: light\)"><meta name="theme-color" content="#000000" media="\(prefers-color-scheme: dark\)">', THEME_META, html); assert k == 1

    # 2. fonts: woff2 variable subsets served from assets/fonts
    html, k = re.subn(r'@font-face\{font-family:"Inter Tight";[^}]*\}\s*@font-face\{font-family:"Inter";[^}]*\}\s*@font-face\{font-family:"Fraunces";font-style:normal;[^}]*\}\s*@font-face\{font-family:"Fraunces";font-style:italic;[^}]*\}', fontfaces(rel), html)
    assert k == 1, 'font-face block not matched'
    html = html.replace('<style>', preloads(rel, tight=slug is None) + '\n<style>', 1)   # case pages set no text in Inter Tight

    # 3. wordmark artwork (loader keeps clip + beam dot; header is plain)
    def wm(m):
        return WM_SVG_LOADER if 'ldClip' in m.group(0) else WM_SVG
    html, k = re.subn(r'<svg viewBox="0 0 3729 561".*?</svg>', wm, html, flags=re.S); log.append(f'replaced {k} wordmark SVGs')
    html, k = re.subn(r'const W = \d+;', f'const W = {WM_W};', html); log.append(f'loader width constant (= viewBox width {WM_W}): {k}')
    # header height: 18.5 px → the letters span 18.5 × 3692.5 / 561 ≈ 122 px (≥ 120 px minimum), cap ≈ 17 px as before
    html = html.replace('.brand svg{height:14px;width:auto;display:block}', '.brand svg{height:18.5px;width:auto;display:block}')
    html = html.replace('.foot .wm svg{height:12px;width:auto}', '.foot .wm svg{height:18.5px;width:auto}')
    html = html.replace('.f-brand .wm svg{height:14px;width:auto;display:block}', '.f-brand .wm svg{height:18.5px;width:auto;display:block}')
    html = html.replace('.c-foot .wm svg{height:12px;width:auto}', '.c-foot .wm svg{height:18.5px;width:auto}')

    # 4. colour tokens — same variable names, values from colour-variables.css + functional + palette
    m = re.search(r':root\{\n(.*?)\n\}\nhtml\[data-theme="dark"\]\{\n(.*?)\n\}', html, re.S)
    light, dark = m.group(1), m.group(2)
    alias = '  --bg-2:var(--bg2); --card-2:var(--card2); --fg-2:var(--fg2); --fg-3:var(--fg3); --line-2:var(--line2); --accent-2:var(--accent2);'
    func_l = '  ' + ' '.join(f'{k}:{TOK_LIGHT[k]};' for k in FUNCTIONAL)
    func_d = '  ' + ' '.join(f'{k}:{TOK_DARK[k]};' for k in FUNCTIONAL)
    pal = '  /* palette + gradient tokens (03_COLOUR_SYSTEM/colour-variables.css) */\n  ' + ' '.join(palette_lines) + '\n  ' + '\n  '.join(gradient_lines)
    light = light.replace('  --accent-text:#8a6124;', '  --accent-text:#8a6124;\n' + alias + '\n' + func_l + '\n' + pal, 1)
    dark  = dark.replace('  --accent-text:#e9b25a;', '  --accent-text:#e9b25a;\n' + func_d, 1)
    light2, d1 = retoken(light, TOK_LIGHT); dark2, d2 = retoken(dark, TOK_DARK)
    for d in d1: log.append(f'light {d[0]}: {d[1]} -> {d[2]}')
    for d in d2: log.append(f'dark  {d[0]}: {d[1]} -> {d[2]}')
    assert '--success' in light2 and '--success' in dark2
    html = html.replace(m.group(0), f':root{{\n{light2}\n}}\nhtml[data-theme="dark"]{{\n{dark2}\n}}', 1)
    html = html.replace('.book-err{grid-column:1/-1;font-size:13px;color:#c0392b;', '.book-err{grid-column:1/-1;font-size:13px;color:var(--error);')

    # 5. signature: vector SVGs instead of the raster PNGs (sig-d = ink on light, sig-l = white on dark)
    html, k = re.subn(r'src="(\.\./)?img/signature-dark\.png" alt="" width="1694" height="698"', r'src="\1img/sanzeed-signature--ink.svg" alt="" width="1215" height="498"', html); log.append(f'signature dark->ink: {k}')
    html, k = re.subn(r'src="(\.\./)?img/signature-light\.png" alt="" width="1694" height="698"', r'src="\1img/sanzeed-signature--white.svg" alt="" width="1215" height="498"', html); log.append(f'signature light->white: {k}')
    html = html.replace('aspect-ratio:1694/698', 'aspect-ratio:1215/498')
    assert 'signature-dark.png' not in html and 'signature-light.png' not in html

    # 6. footer lockup above the columns + CSS addendum (.lit/.dim, Fraunces optical sizes)
    html, k = re.subn(r'(\n  )<div class="f-grid">', r'\1' + LOCKUP_SVG.replace('\\', '\\\\') + '<div class="f-grid">', html, count=1); assert k == 1
    html = html.replace('\n</style>', CSS_ADDENDUM + '</style>', 1)
    assert '.f-lockup{' in html

    # 7. Open Graph images
    if slug:
        og = f'https://sanzeed.com/img/og/{slug}-1200x630.jpg'
        html, k = re.subn(r'<meta property="og:image" content="https://sanzeed\.com/img/[a-z0-9-]+\.webp">',
                          f'<meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{OG[slug]}">', html); assert k == 1
        html, k = re.subn(r'<meta name="twitter:image" content="https://sanzeed\.com/img/[a-z0-9-]+\.webp">', f'<meta name="twitter:image" content="{og}">', html); assert k == 1
    log.append(f'size {n0:,} -> {len(html):,} bytes')
    return html, log

FAVICON_DIR = B / '02_LOGO_SYSTEM' / 'Favicon'
FAVICON_FILES = ['favicon.ico', 'favicon.svg', 'apple-touch-icon.png', 'android-chrome-192x192.png',
                 'android-chrome-512x512.png', 'maskable-icon-512x512.png', 'safari-pinned-tab.svg', 'site.webmanifest']

def copy_favicons():
    """Favicon + PWA set served from the site root, copied from the logo system. SVG <desc> lines that still describe
    the retired geometric construction are dropped from the copies (the artwork itself is the approved logo)."""
    for name in FAVICON_FILES:
        src, dst = FAVICON_DIR / name, OUT / name
        if name.endswith('.svg'):
            dst.write_text(re.sub(r'\s*<desc>[^<]*(?:500-unit|64-unit)[^<]*</desc>', '', src.read_text()))
        else:
            dst.write_bytes(src.read_bytes())
    return len(FAVICON_FILES)

def main():
    report = {'favicons': [f'copied {copy_favicons()} files from 02_LOGO_SYSTEM/Favicon']}
    html, log = transform((SRC / 'index.html').read_text(), '')
    (OUT / 'index.html').write_text(html); report['index.html'] = log
    for slug in OG:
        html, log = transform((SRC / 'work' / f'{slug}.html').read_text(), '../', slug)
        (OUT / 'work' / f'{slug}.html').write_text(html); report[f'work/{slug}.html'] = log
    sm = (SRC / 'sitemap.xml').read_text().replace('2026-10-21', TODAY)
    (OUT / 'sitemap.xml').write_text(sm)
    for k, v in report.items():
        print(k); [print('   ', l) for l in v]

if __name__ == '__main__':
    main()
