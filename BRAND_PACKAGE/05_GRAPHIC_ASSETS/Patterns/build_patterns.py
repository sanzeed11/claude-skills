#!/usr/bin/env python3
"""
build_patterns.py — the editable master for every seamless tile in Patterns/.

  python3 build_patterns.py            # regenerates src/, svg/, png/, patterns.css and the contact sheet

Each tile is authored in 1x CSS-pixel units (tile sizes are powers of two so a 2048 px PNG is
itself seamless). Two inks: dark (Gallery White + Lamp Gold on transparent, for #000 / Night /
Charcoal) and light (Soot + Old Gold on transparent, for Plaster / Paper / Stone).
  src/   tiles WITH the visible dashed 'tile' guide rect (so the repeat is obvious when editing)
  svg/   clean production tiles (no guide) — what patterns.css embeds
  png/   2048 x 2048 transparent PNG, rendered at 2x (1 unit = 2 px) and repeated
Edit the drawing functions below, re-run, done. Use any tile at <= 12 % opacity behind content.
"""
import sys, re, base64, urllib.parse
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '_build')); import szlib as sz

f = sz.f
TILES = {}   # name -> (w, h, draw(ink) -> body)

# ---------------------------------------------------------------- the tiles
def dot_grid(spacing, r, gold_every):
    """points on a grid; every (gold_every x gold_every)th point is the lit one."""
    size = spacing * gold_every
    def draw(c):
        out = [f'<g id="points" fill="{c["ink"]}" fill-opacity="0.45">']
        for j in range(gold_every):
            for i in range(gold_every):
                if i == gold_every // 2 and j == gold_every // 2: continue
                out.append(f'<circle cx="{f(spacing/2 + i*spacing)}" cy="{f(spacing/2 + j*spacing)}" r="{f(r)}"/>')
        out.append('</g>')
        k = gold_every // 2
        out.append(f'<g id="lit-point" fill="{c["gold"]}"><circle cx="{f(spacing/2 + k*spacing)}" cy="{f(spacing/2 + k*spacing)}" r="{f(r*1.35)}"/></g>')
        return '\n'.join(out)
    return size, size, draw
TILES['dot-grid-fine']   = dot_grid(32, 1.1, 8)      # 256 tile, 32 px pitch
TILES['dot-grid-coarse'] = dot_grid(64, 1.6, 4)      # 256 tile, 64 px pitch

def beam_lines():
    size = 512; pitch = 64
    def draw(c):
        out = [f'<clipPath id="tile-clip"><rect width="{size}" height="{size}"/></clipPath>',
               f'<g id="beams" clip-path="url(#tile-clip)" stroke="{c["ink"]}" stroke-opacity="0.22" stroke-width="1" shape-rendering="crispEdges">']
        for i in range(size // pitch):
            y = pitch/2 + i*pitch
            out.append(f'<line x1="-4" y1="{f(y)}" x2="{f(size+4)}" y2="{f(y)}"/>')
        out.append('</g>')
        out.append(f'<g id="travelling-points" fill="{c["gold"]}">')
        for i in range(size // pitch):
            y = pitch/2 + i*pitch
            x = 8 + (37 + i*197) % (size - 16)            # fixed pseudo-random stagger, clear of the tile edge
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.2"/>')
        out.append('</g>')
        return '\n'.join(out)
    return size, size, draw
TILES['beam-lines'] = beam_lines()

def arch_repeat():
    size = 512; aw, ah = 144, 216; rowh = 256                    # arch width/height, row pitch
    def arch(cx, top):
        r = aw/2
        return f'M{f(cx-r)} {f(top+ah)} V{f(top+r)} A{f(r)} {f(r)} 0 0 1 {f(cx+r)} {f(top+r)} V{f(top+ah)}'
    def draw(c):
        pad = (rowh - ah)/2
        d = []
        for cx in (128, 384): d.append(arch(cx, pad))                  # row A
        for cx in (0, 256, 512): d.append(arch(cx, rowh + pad))        # row B (brick offset)
        out = [f'<clipPath id="tile-clip"><rect width="{size}" height="{size}"/></clipPath>',
               f'<g id="arches" clip-path="url(#tile-clip)" fill="none" stroke="{c["ink"]}" stroke-opacity="0.38" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">',
               f'<path d="{" ".join(d)}"/>', '</g>',
               f'<g id="lit-point" fill="{c["gold"]}"><circle cx="128" cy="{f(pad + aw/2)}" r="3"/></g>']
        return '\n'.join(out)
    return size, size, draw
TILES['arch-repeat'] = arch_repeat()

def route():
    size = 512
    segs = [((0,256),(96,256),(96,128),(192,128)), ((192,128),(288,128),(288,384),(384,384)), ((384,384),(448,384),(480,256),(512,256))]
    path = 'M0 256 C96 256 96 128 192 128 C288 128 288 384 384 384 C448 384 480 256 512 256'
    def blen():                                   # numeric length of the three cubics
        L = 0
        for p0,p1,p2,p3 in segs:
            prev = p0
            for k in range(1, 401):
                t = k/400; u = 1-t
                x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
                y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
                L += ((x-prev[0])**2 + (y-prev[1])**2) ** .5; prev = (x, y)
        return L
    L = blen(); n = round(L / 11); gap = L / n           # an exact number of dots per tile
    def draw(c):
        return '\n'.join([
            f'<clipPath id="tile-clip"><rect width="{size}" height="{size}"/></clipPath>',
            f'<g id="route" clip-path="url(#tile-clip)" fill="none" stroke="{c["ink"]}" stroke-opacity="0.5" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="0 {f(gap)}" stroke-dashoffset="{f(-gap/2)}">',
            f'<path d="{path}"/>', '</g>',
            f'<g id="rooms" fill="{c["gold"]}"><circle cx="192" cy="128" r="3.4"/><circle cx="384" cy="384" r="3.4"/></g>'])
    return size, size, draw
TILES['route'] = route()

def monogram_repeat():
    size = 512; mw = 176
    inner, w, h = sz.logo_body('monogram', 'full-colour-dark')
    # pull the two path groups out of the production monogram so we can set opacity per group
    ink_path = re.search(r'<path\s+d="([^"]+)"', inner).group(1)
    dot = re.search(r'<circle\s+cx="([\d.]+)"\s+cy="([\d.]+)"\s+r="([\d.]+)"', inner)
    s = mw / w; mh = h*s
    def draw(c):
        out = [f'<clipPath id="tile-clip"><rect width="{size}" height="{size}"/></clipPath>',
               f'<defs><g id="sm"><path d="{ink_path}" fill="{c["ink"]}" fill-opacity="0.08"/>'
               f'<circle cx="{dot.group(1)}" cy="{dot.group(2)}" r="{dot.group(3)}" fill="{c["gold"]}" fill-opacity="0.3"/></g></defs>',
               '<g id="monograms" clip-path="url(#tile-clip)">']
        rowh = size/2
        for row in range(2):
            y = row*rowh + (rowh - mh)/2
            xs = (168,) if row == 0 else (-88, 424)      # brick stagger: row B straddles the tile edge
            for x in xs:
                out.append(f'<use href="#sm" transform="translate({f(x)} {f(y)}) scale({f(s)})"/>')
        out.append('</g>')
        return '\n'.join(out)
    return size, size, draw
TILES['monogram-repeat'] = monogram_repeat()

def s_curve():
    """The refined S's two hooks (bar sweeping into a tapered terminal), read straight from the production
    symbol and alternated along each row like the halves of the S, so the field follows the real letter."""
    size = 512; rowh = 128; pitch = 128; hw = 76          # hook width in px (the S hook is ~356 x 302 symbol units)
    inner, w, h = sz.logo_body('symbol', 'full-colour-dark')
    d = re.search(r'<path\s+d="([^"]+)"', inner).group(1)
    subs = [s.strip() for s in re.split(r'(?=M)', d) if s.strip()]           # [0] top hook, [1] bottom hook
    dot = re.search(r'<circle\s+cx="([\d.]+)"\s+cy="([\d.]+)"\s+r="([\d.]+)"', inner)
    def bbox(sp):
        n = [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?(?:e-?\d+)?', sp)]
        return min(n[0::2]), min(n[1::2]), max(n[0::2]), max(n[1::2])
    boxes = [bbox(sp) for sp in subs]
    s = hw / max(b[2] - b[0] for b in boxes)
    def place(i, cx, cy):                                   # transform that centres hook i on (cx, cy)
        x0, y0, x1, y1 = boxes[i]
        return f'translate({f(cx - (x0 + x1)/2*s)} {f(cy - (y0 + y1)/2*s)}) scale({f(s)})'
    def draw(c):
        out = [f'<clipPath id="tile-clip"><rect width="{size}" height="{size}"/></clipPath>',
               f'<defs><path id="hook-top" d="{subs[0]}"/><path id="hook-bottom" d="{subs[1]}"/></defs>',
               f'<g id="hooks" clip-path="url(#tile-clip)" fill="{c["ink"]}" fill-opacity="0.12">']
        for row in range(size // rowh):
            cy = rowh/2 + row*rowh; phase = (row % 2)
            for k in range(-1, size // pitch + 1):
                i = (k + phase) % 2
                out.append(f'<use href="#hook-{"top" if i == 0 else "bottom"}" transform="{place(i, k*pitch + pitch/2, cy)}"/>')
        out.append('</g>')
        # the lit point: the symbol's own full stop, beside one bottom hook (row 0, second hook), same relation as in the S.
        x0, y0, x1, y1 = boxes[1]
        tx, ty = pitch + pitch/2 - (x0 + x1)/2*s, rowh/2 - (y0 + y1)/2*s
        out.append(f'<g id="lit-point" fill="{c["gold"]}" fill-opacity="0.6"><circle cx="{f(tx + float(dot.group(1))*s)}" cy="{f(ty + float(dot.group(2))*s)}" r="{f(float(dot.group(3))*s)}"/></g>')
        return '\n'.join(out)
    return size, size, draw
TILES['s-curve'] = s_curve()

# ---------------------------------------------------------------- writers
def tile_svg(name, ink, guide):
    w, h, draw = TILES[name]; c = sz.INK[ink]
    body = draw(c)
    if guide:
        body = (f'<g id="guide-tile" fill="none" stroke="{c["gold"]}" stroke-opacity="0.6" stroke-width="1" stroke-dasharray="4 4">'
                f'<rect id="tile" x="0.5" y="0.5" width="{f(w-1)}" height="{f(h-1)}"/></g>\n' + body)
    title = f'Sanzeed pattern — {name} ({ink} ink)'
    desc = (f'Seamless tile {f(w)}x{f(h)} px. {"Dark ink: Gallery White + Lamp Gold" if ink=="dark" else "Light ink: Soot + Old Gold"} on transparent. '
            f'Use at <= 12 % opacity behind content. Generated by Patterns/build_patterns.py — edit there.'
            + (' The dashed rect is the tile boundary (guide layer, not in the production tile).' if guide else ''))
    return sz.svg(w, h, body, title, desc), w, h

def repeated_svg(name, ink, px=2048, scale=2):
    """Production tile repeated to fill px x px at `scale` device px per unit."""
    w, h, draw = TILES[name]; c = sz.INK[ink]
    body = draw(c)
    units = px / scale
    nx, ny = int(units // w), int(units // h)
    uses = ''.join(f'<use href="#tile" x="{f(i*w)}" y="{f(j*h)}"/>' for j in range(ny) for i in range(nx))
    inner = f'<defs><g id="tile">{body}</g></defs><g transform="scale({scale})">{uses}</g>'
    inner = inner.replace('id="tile-clip"', 'id="tile-clip"')  # same id reused inside <defs> is fine for cairosvg
    return sz.svg(px, px, inner, f'Sanzeed pattern — {name} ({ink}) repeated', 'rendered from the production tile')

def main():
    out_src, out_svg, out_png = HERE/'src', HERE/'svg', HERE/'png'
    for d in (out_src, out_svg, out_png): d.mkdir(exist_ok=True)
    css = ['/* SANZEED — patterns.css  (generated by Patterns/build_patterns.py)',
           '   Each class paints one seamless brand tile as a CSS background. Tiles are transparent:',
           '   put them on the brand background colour and keep them at <= 12 % opacity behind content',
           '   (e.g. with a pseudo-element and `opacity: .12`). --dark = white/gold ink for #000, Night,',
           '   Charcoal; --light = soot/old-gold ink for Plaster, Paper, Stone. */', '']
    manifest = []
    for name in TILES:
        for ink in ('dark', 'light'):
            stem = f'sanzeed-pattern-{name}--{ink}'
            s, w, h = tile_svg(name, ink, guide=True); sz.write(out_src/f'{stem}.svg', s)
            s, w, h = tile_svg(name, ink, guide=False); sz.write(out_svg/f'{stem}.svg', s)
            rep = repeated_svg(name, ink); tmp = HERE/'_tmp.svg'; tmp.write_text(rep)
            sz.svg_to_png(tmp, out_png/f'{stem}-2048.png', 2048, 2048); tmp.unlink()
            mini = re.sub(r'<\?xml[^>]*>\s*', '', s); mini = re.sub(r'<title>.*?</title>\s*<desc>.*?</desc>\s*', '', mini, flags=re.S)
            mini = re.sub(r'\s+', ' ', mini).strip()
            uri = 'data:image/svg+xml;charset=utf-8,' + urllib.parse.quote(mini, safe="=:/ '-.,;%()")
            css.append(f'.pat-{name}--{ink} {{ background-image: url("{uri}"); background-size: {f(w)}px {f(h)}px; background-repeat: repeat; }}')
            manifest.append((name, ink, w, h))
            print('tile', stem, f'{f(w)}x{f(h)}')
    css.append(''); css.append('/* example: <div class="room pat-dot-grid-fine--dark" style="opacity:.12"></div> */')
    sz.write(HERE/'patterns.css', '\n'.join(css) + '\n')
    # ---- contact sheet
    cells = {'dark': [], 'light': []}
    for name, ink, w, h in manifest:
        cells[ink].append(f'<figure><div class="sw pat-{name}--{ink}" style="background-size:{f(w/2)}px {f(h/2)}px"></div><figcaption><b>{name}</b><span>{f(w)} × {f(h)} px · {ink} ink</span></figcaption></figure>')
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sanzeed — pattern contact sheet</title>
<link rel="stylesheet" href="../../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css"><link rel="stylesheet" href="../patterns.css">
<style>
body{{margin:0;width:1920px}} .half{{padding:56px 64px 64px}} .half.dark{{background:#000;color:#F5F5F7}} .half.light{{background:#F5F0E7;color:#1A1816}}
.head{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:28px}}
h1{{font:300 40px/1.1 "Fraunces";font-variation-settings:"opsz" 72,"SOFT" 30;letter-spacing:-.01em}} h1 .lit{{color:var(--accent)}}
.light h1 .lit{{color:#B8863B}} .eyebrow{{font:600 12px/1 "Inter Tight";letter-spacing:.12em;text-transform:uppercase;color:#E9B25A}} .light .eyebrow{{color:#8A6124}}
.grid{{display:grid;grid-template-columns:repeat(7,1fr);gap:24px}} figure{{margin:0}}
.sw{{aspect-ratio:1;border-radius:20px;border:1px solid rgba(255,255,255,.10)}} .light .sw{{border-color:rgba(40,30,10,.10)}}
figcaption{{margin-top:12px;font:400 13px/1.5 "Inter";color:#808086}} figcaption b{{display:block;font:600 14px/1.4 "Inter Tight";color:inherit}} .dark figcaption b{{color:#F5F5F7}} .light figcaption b{{color:#1A1816}}
.light figcaption{{color:#6D665C}}
</style></head><body>
<section class="half dark"><div class="head"><div><div class="eyebrow">Patterns · dark ink</div><h1>Seven tiles, <span class="lit">lit.</span></h1></div><div class="eyebrow">tiles shown at 50 % · use at ≤ 12 % opacity</div></div><div class="grid">{''.join(cells['dark'])}</div></section>
<section class="half light"><div class="head"><div><div class="eyebrow">Patterns · light ink</div><h1>The same seven, on <span class="lit">Plaster.</span></h1></div><div class="eyebrow">tiles shown at 50 % · use at ≤ 12 % opacity</div></div><div class="grid">{''.join(cells['light'])}</div></section>
</body></html>'''
    sz.write(HERE/'src'/'contact-sheet.html', html)
    sz.render_html(HERE/'src'/'contact-sheet.html', HERE/'sanzeed-patterns-contact-sheet.png', 1920, 1200, scale=1, full=True)
    print('wrote patterns.css and contact sheet')

if __name__ == '__main__': main()
