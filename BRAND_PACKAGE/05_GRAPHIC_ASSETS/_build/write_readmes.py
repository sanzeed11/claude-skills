#!/usr/bin/env python3
"""write_readmes.py — writes README.md for 05_GRAPHIC_ASSETS and each subfolder: hand-written guidance +
an inventory table generated from the files on disk (format, pixel size / page size, bytes). Re-run after
any regeneration so the tables stay true:  python3 _build/write_readmes.py"""
import os, re, sys, json
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
Image.MAX_IMAGE_PIXELS = None

def human(n):
    return f'{n/1024/1024:.1f} MB' if n >= 1024*1024 else (f'{n/1024:.0f} KB' if n >= 1024 else f'{n} B')

def spec(p: Path):
    ext = p.suffix.lower()
    try:
        if ext in ('.png', '.jpg', '.jpeg', '.webp'):
            im = Image.open(p); return f'{im.width} × {im.height} px' + (' · alpha' if im.mode in ('RGBA', 'LA') else '')
        if ext == '.svg':
            t = p.read_text(errors='ignore'); m = re.search(r'viewBox="([^"]+)"', t)
            if m:
                vb = m.group(1).split(); w, h = float(vb[2]), float(vb[3])
                mm = re.search(r'width="([\d.]+)mm"', t)
                return f'{mm.group(1)} × {re.search(r"height=\"([\d.]+)mm\"", t).group(1)} mm (vector)' if mm else f'{w:g} × {h:g} units (vector)'
            return 'vector'
        if ext == '.pdf':
            from pypdf import PdfReader
            b = PdfReader(p).pages[0].mediabox; return f'{float(b.width)/72*25.4:.0f} × {float(b.height)/72*25.4:.0f} mm (vector PDF)'
        if ext == '.css': return 'CSS'
        if ext == '.html': return 'HTML source'
        if ext == '.py': return 'Python generator'
    except Exception as e:
        return ext[1:]
    return ext[1:]

def table(folder: Path, skip=('README.md',), collapse=None):
    """collapse: list of (regex, label) → rows matching the regex are summarised as one row."""
    rows = []; groups = {}
    files = sorted(p for p in folder.rglob('*') if p.is_file() and p.name not in skip and '__pycache__' not in p.parts and not p.name.startswith('_tmp'))
    for p in files:
        rel = p.relative_to(folder).as_posix()
        if collapse:
            hit = False
            for rx, label in collapse:
                if re.search(rx, rel):
                    g = groups.setdefault(label, dict(n=0, bytes=0, specs=set(), example=rel))
                    g['n'] += 1; g['bytes'] += p.stat().st_size; g['specs'].add(spec(p)); hit = True; break
            if hit: continue
        rows.append(f'| `{rel}` | {p.suffix[1:].upper()} | {spec(p)} | {human(p.stat().st_size)} |')
    for label, g in groups.items():
        specs = ' / '.join(sorted(g['specs']))[:160]
        rows.append(f'| `{label}` ({g["n"]} files, e.g. `{g["example"]}`) | {Path(g["example"]).suffix[1:].upper()} | {specs} | {human(g["bytes"])} total |')
    total = sum(p.stat().st_size for p in files)
    return '| File | Format | Spec | Size |\n|---|---|---|---|\n' + '\n'.join(rows) + f'\n\n**{len(files)} files · {human(total)}**\n'

def write(path, text): Path(path).write_text(text.strip() + '\n', encoding='utf-8'); print('wrote', path)

# ------------------------------------------------------------------------------------------ Patterns
write(ROOT/'Patterns'/'README.md', f'''
# Patterns — seamless brand tiles

Seven tiles drawn from the graphic vocabulary (§6 of the brand kit): **dot-grid** (two densities), **beam-lines**
(hairlines with a travelling point), **arch-repeat** (the N/M doorway as a window pattern), **route** (a dotted
meander with lit rooms), **monogram-repeat** (the SM. monogram, M built from two of the wordmark's N, at 8 %), **s-curve** (the refined S's two
tapered hooks, read from the production symbol and alternated as a flowing field).
Each exists in two inks: **dark** = Gallery White + Lamp Gold on transparent (for Gallery Black, Night, Charcoal)
and **light** = Soot + Old Gold on transparent (for Plaster, Paper, Stone).

**Rule of use:** behind content at **≤ 12 % opacity** (the tiles are drawn at full strength so you can see them;
dim them in the layout, e.g. a pseudo-element with `opacity:.12`). Never on gold. One tile per composition.

| Folder / file | What it is |
|---|---|
| `src/*.svg` | the editable tiles **with the dashed gold `tile` guide rect** so the repeat boundary is obvious in Illustrator / Figma / Inkscape |
| `svg/*.svg` | clean production tiles (identical drawing, no guide) — the files `patterns.css` embeds |
| `png/*-2048.png` | 2048 × 2048 transparent PNG, the tile rendered at 2 × (1 unit = 2 px) and repeated; itself seamless |
| `patterns.css` | one class per tile (`.pat-<name>--dark` / `--light`) with the SVG as a data-URI background, `background-size` = tile size |
| `sanzeed-patterns-contact-sheet.png` | all 14 tiles repeated at 50 % on black and on Plaster (source `src/contact-sheet.html`) |
| `build_patterns.py` | **the master.** Every tile is a small drawing function; edit a number, run `python3 build_patterns.py`, and src/, svg/, png/, patterns.css and the contact sheet are regenerated |

Tile sizes (1 ×): dot-grid 256 (pitch 32 / 64), all others 512. Powers of two, so the 2048 px PNGs tile without a seam
(verified numerically: the repeated halves of every PNG differ only by anti-aliasing noise).

**Edit by hand instead:** open `src/<tile>.svg`, keep everything inside the dashed rect, save a copy without the guide layer into
`svg/`, then `python3 build_patterns.py` is still the easiest way to refresh the PNG and CSS (or re-export the PNG at 2048 px from your app).

{table(ROOT/'Patterns', collapse=[(r'^src/sanzeed-pattern', 'src/sanzeed-pattern-*.svg'), (r'^svg/', 'svg/sanzeed-pattern-*.svg'), (r'^png/', 'png/sanzeed-pattern-*-2048.png')])}
''')

# ------------------------------------------------------------------------------------------ Textures
write(ROOT/'Textures'/'README.md', f'''
# Textures — grain, paper, lamp glow, vignette

Procedural, deterministic (fixed seeds), generated by `generate_textures.py` (numpy + Pillow). Re-run the script
to regenerate; change the parameters at the bottom of the file (sigma, strength, radii) to tune.

| File | Use | How |
|---|---|---|
| `sanzeed-texture-grain--tile-1024.png` | the brand **grain**: 7 % soft-light noise on dark backgrounds only | layer over the dark background, blend **Soft Light**, opacity **7 %**. Seamless (white noise), so tile it. Transparent: white/black pixels whose alpha is the distance from mid-grey, so it is neutral at 50 % grey |
| `sanzeed-texture-grain--fine-1024.png` | finer, quieter grain for small screens and print proofs | same, 7–10 % |
| `sanzeed-texture-paper--plaster-2048.jpg` | Plaster `#F5F0E7` with a subtle laid-paper fibre | full-bleed background for documents / light mode; fits under body text without lowering contrast (± 5 levels) |
| `sanzeed-texture-paper--paper-2048.jpg` | the same fibre on Paper `#FBF8F2` | cards and sheets on Plaster |
| `sanzeed-texture-lamp-glow--2048.png` | the **lamp**: Lamp Gold radial glow = `--sz-gradient-lamp` (centre 50 % / 40 %, .55 → .12 at 28 % → 0 at 70 %) | place behind the single lit object on black; scale freely |
| `sanzeed-texture-lamp-glow--light-2048.png` | the Old Gold version | behind a lit object on Plaster, at reduced opacity |
| `sanzeed-texture-vignette--1920x1080.png` · `--1080x1920` · `--1080x1080` | transparent black vignette (clear centre → 62 % at the corners, smoothstep from 55 % radius) | over photography or the lamp background; also the darkening for video end frames |

Grain belongs only on dark backgrounds; on pure `#000` a soft-light grain is mathematically invisible — put it on
Night, Charcoal, the dusk gradient or the lamp glow, where it reads.

{table(ROOT/'Textures')}
''')

# ------------------------------------------------------------------------------------------ Illustrations
write(ROOT/'Illustrations'/'README.md', f'''
# Illustrations — the monoline brand language

Every drawing speaks the brand's monoline language: **one even stroke (64 units on the drawing grid), round caps and joins,
gold points of light** sized to the stroke (r = 0.7 × stroke, 45 units); secondary lines are 20 units; labels are the brand fonts outlined (Fraunces 300
opsz 144 for names, Inter Tight 600 letter-spaced caps for eyebrows and counters, Inter 400 for captions), so no file
depends on an installed font. **dark** ink (Gallery White / Silver / Lamp Gold) is for black backgrounds; **light** ink
(Soot / Umber / Old Gold, Gold Ink for text) is for Plaster. Export set per drawing: `svg/` (editable), `png/` (2000 px wide,
transparent) and `pdf/` (vector, Inkscape, text already outlines).

| Drawing | Files (× dark / light) | What it shows |
|---|---|---|
| **Orbit object** | `sanzeed-illustration-orbit-object--*` | a flat reading of the site's 3D hero: glass sphere, tilted gold ring (passes behind the sphere, in front below), black plinth with the pool of light, glass beads, one point of light. 2000 × 1480 |
| **Method diagram** | `sanzeed-illustration-method-diagram--*` | Discover → Direct → Craft → Deliver as four points on one beam, STEP 01–04 eyebrows, the deliverable under each ("You receive …"), the travelling point. 2400 × 760 |
| **Between two points of light** | `sanzeed-illustration-between-two-points--*` | the brief (left, low) and the visitor (right, high), one line of light between them and six fainter ways behind it — "Seven ways to carry the light across." 2400 × 1200 |
| **Museum route** | `sanzeed-illustration-museum-route--*` | plan view: eight rooms (the room shape, radius 28) numbered 001–008, doorways where the dotted route passes, a point of light in each, entry and exit. 2400 × 1560 |
| **Seven service glyphs** | `sanzeed-illustration-service-glyph-01…07-*--*` | one per service on a 128 grid (stroke 6, point r 4.2): 01 creative direction (line between two points) · 02 museum planning (route through two rooms) · 03 storytelling (a script line with three beats) · 04 spatial & branding (the threshold) · 05 events (beam onto a stage) · 06 digital ↔ physical (line through a screen, out as pixels) · 07 leadership (a ring, seven hands) |
| **Lamp** | `sanzeed-illustration-lamp--*` | the doorway arch as a shade, the point beneath it, cone and pool of light on the floor, with the gold glow. 1600 × 2000 |

**Edit:** `build_illustrations.py` is the master — each drawing is a function returning SVG; change coordinates or copy
there and run `python3 build_illustrations.py [name]` (a name filter such as `orbit` rebuilds one drawing). Or open the
SVG in any vector app: groups are named (`sphere`, `ring-front`, `rooms`, `route`, `labels` …). Exports go through the
kit's `export_svg.py` (cairosvg PNG, Inkscape PDF).

Minimum sizes: diagrams ≥ 600 px wide on screen (labels stay ≥ 12 px); glyphs ≥ 24 px (they are UI-icon scale at 32–64 px).

{table(ROOT/'Illustrations', collapse=[(r'^svg/.*service-glyph', 'svg/sanzeed-illustration-service-glyph-*.svg'), (r'^png/.*service-glyph', 'png/sanzeed-illustration-service-glyph-*.png'), (r'^pdf/.*service-glyph', 'pdf/sanzeed-illustration-service-glyph-*.pdf')])}
''')

# ------------------------------------------------------------------------------------------ Icons
write(ROOT/'Icons'/'README.md', f'''
# Icons — 54 icons, one line

**Grid 24 px · stroke 1.5 px · round caps and joins · no fills** except the brand point (a filled dot). Drawn, not taken from
a stock set, in the same monoline grammar as the logo and the illustrations.

* **contact (8):** mail, phone, whatsapp, linkedin, location, calendar, clock, globe
* **ui (31):** arrow-left/right/up/down, chevron-left/right/up/down, close, menu, search, filter, grid, list, play, pause, sun, moon,
  external-link, download, upload, check, info, warning, error, plus, minus, copy, share, zoom-in, zoom-out
* **domain (15):** museum, pavilion, projection, light-beam, route, doorway, stage, screen, ar-vr, team, script, drawing, film, award, book

| Folder / file | What |
|---|---|
| `svg/sanzeed-icon-<name>.svg` | one icon per file, `stroke="currentColor"` — on the web it takes the text colour. Size with CSS (`width:24px`), never change the stroke |
| `sanzeed-icons-sprite.svg` | all icons as `<symbol id="icon-<name>">`; inline once, then `<svg class="icon"><use href="#icon-mail"/></svg>` |
| `png/dark/48`, `png/dark/96` | PNG in **dark ink** Gallery White `#F5F5F7` (for black / Night / Charcoal), 48 and 96 px, transparent |
| `png/light/48`, `png/light/96` | PNG in **light ink** Soot `#1A1816` (for Plaster / Paper / Stone) |
| `icons.html` + `sanzeed-icons-sheet.png` | the preview sheet, both inks (1920 px wide) |
| `build_icons.py` | **the master**: every icon is one line of path data in `ICONS`; add or edit a line and run `python3 build_icons.py` |

Colour: icons are single-colour. When the icon's point is the only accent in the composition it may be set gold (class `.pt` in the
light-beam, route and stage icons; `fill:#E9B25A` on dark, `#B8863B` on light). Tap targets ≥ 44 px.

{table(ROOT/'Icons', collapse=[(r'^svg/', 'svg/sanzeed-icon-*.svg'), (r'^png/dark/48/', 'png/dark/48/sanzeed-icon-*--dark-48.png'), (r'^png/dark/96/', 'png/dark/96/sanzeed-icon-*--dark-96.png'), (r'^png/light/48/', 'png/light/48/sanzeed-icon-*--light-48.png'), (r'^png/light/96/', 'png/light/96/sanzeed-icon-*--light-96.png')])}
''')

# ------------------------------------------------------------------------------------------ Backgrounds
write(ROOT/'Backgrounds'/'README.md', f'''
# Backgrounds — lamp, dusk, plaster, presentation, covers, photo plates

All rendered by `build_backgrounds.py` from the sources in `src/` with the kit's `render.js` (Chromium, brand.css tokens and
fonts), so every pixel matches the website's CSS. Photographic / gradient renders are JPG q90; slide backgrounds are
PNG 1920 × 1080 (exact slide pixels) plus JPG 3840 × 2160 (2 ×).

| Set | Files | Notes |
|---|---|---|
| **Lamp** (dark) | `sanzeed-bg-lamp--dark-{{1920x1080,2560x1440,1080x1920,1080x1080}}.jpg` | Gallery Black + `--sz-gradient-lamp` + 7 % grain. Behind a single lit object, the logo, a cover title. Source `src/sanzeed-bg-lamp--dark.html` |
| **Dusk** (dark) | `sanzeed-bg-dusk--dark-*.jpg` (4 sizes) | `#000 → #1C1C1E`. Section and slide backgrounds |
| **Plaster** (light) | `sanzeed-bg-plaster--light-*.jpg` (4 sizes) | `#FBF8F2 → #ECE7DC`. Documents, light mode |
| **Grain variants** | `sanzeed-bg-grain--{{charcoal,dusk,lamp}}-1920x1080.jpg` | the brand `.grain` (7 % soft-light) on surfaces where it reads; on pure black it is invisible by definition, so use Night/Charcoal or the Textures grain tile instead |
| **Presentation 16:9** | `sanzeed-bg-presentation-{{title,content,section,end}}--{{dark,light}}-1920x1080.png` + `-3840x2160.jpg` | title: lamp low + beam + primary wordmark bottom-left (300 px). content: hairline + point top, wordmark 180 px bottom-left. section: dusk / plaster + the doorway arch right. end: lamp centred + wordmark centred (520 px) + beam. Dark uses `full-colour-dark`, light `full-colour-light`; clear space ≥ ½ cap height is kept everywhere. Sources `src/sanzeed-bg-presentation-*.html` |
| **A4 covers** | `sanzeed-cover-a4--{{dark,light}}.svg` + `.pdf` + `-2480x3508.png` | 210 × 297 mm, 20 mm margins, `horizontal-descriptor` lockup bottom-left at 70 mm (rule for document covers), beam + point above it, the doorway arch as a window motif (fading legs), lamp glow / plaster gradient. The SVG is the master (1 unit = 0.1 mm; logo embedded as paths); PDF via Inkscape (vector); PNG at 300 dpi via Chromium (`src/sanzeed-cover-a4--*.html` wrapper). Title goes top-left in Fraunces 300 |
| **Photo plates** | `sanzeed-bg-photo-plate--{{prime-minister-museum,ram-katha-show,buddha-park}}-1920x1080.jpg` | approved project images (from `00_ORIGINAL_ASSETS_BACKUP/images/img/`) under the veil (→ 88 % black at the base), wall label bottom-left (Title · Place), wordmark bottom-right on ≥ 80 % black, grain. Swap the image and the two label lines in `src/sanzeed-bg-photo-plate--*.html` for any other project; the 960 × 540 masters are upscaled 2 × under the veil |

**Edit:** change a source in `src/` (they are plain HTML using `brand.css` + `src/_base.css`) and run
`python3 build_backgrounds.py <group>` with `lamp`, `dusk`, `plaster`, `grain`, `presentation`, `covers` or `plates`.
The JPGs are written at q90 by Pillow; the PNGs come straight from Chromium.

{table(ROOT/'Backgrounds')}
''')

# ------------------------------------------------------------------------------------------ Decorative
write(ROOT/'Decorative_Elements'/'README.md', f'''
# Decorative elements — dividers, frames, marks, lockups, badges, arrows, the 'lit.' stop, the visitor's book

Every element in SVG (`svg/<group>/`) and transparent PNG (`png/<group>/`, 2 × — 4 × for the small ones). Two inks:
**dark** (Gallery White / Lamp Gold, for black) and **light** (Soot / Old Gold / Gold Ink, for Plaster). Generated by
`build_decorative.py` — the master; edit there and run `python3 build_decorative.py`.

| Group | Files | Spec and use |
|---|---|---|
| `dividers` | `sanzeed-divider-beam-point--{{480,960,1440}}--*` · `beam-centre-point--960` · `hairline--{{480,960,1440}}` · `hairline-dotted--960` · `short-rule--48` | the **beam**: 1 px hairline at 10 % with the 9 px point at its start (glow on dark only), three lengths; plain hairlines; a route-style dotted rule; a 48 px gold rule for section openers. Matches `brand.css` `.beam` / `.hairline` |
| `frames` | `sanzeed-frame-room--{{16x9,4x5,1x1,9x16}}--*` | the **room**: radius 28, hairline border, Charcoal / Paper fill, with `<rect id="image-placeholder">` (replace with the project image, it is clipped to the corners), the veil, and a wall-label slot in live text. 1600 × 900 · 1080 × 1350 · 1080 × 1080 · 1080 × 1920 |
| `corner-marks` | `sanzeed-corner-marks--set-640x400--*` · `set-with-point` · `sanzeed-corner-mark--single--*` | four 36 px corner brackets (1.5 px, ink at 60 %) framing an area; move the four paths to any size; the version with the point inside the top-left |
| `eyebrows` | `sanzeed-eyebrow--{{now-showing,method,about,journey,get-in-touch,services,the-walk,case-study,step-01}}--*` · `now-showing-with-beam` | letter-spaced caps, Inter Tight 600, +0.12 em, **outlined**; gold text (Lamp Gold on dark, **Gold Ink #8A6124** on light — the only gold allowed as text on light). Drawn at 32 px; in UI the eyebrow is 12 px |
| `counters` | `sanzeed-counter-badge--001…010--*` · `sanzeed-counter-badges--001-010--*` (strip) | 68 × 28 hairline pill, Inter Tight 500, +0.08 em, tabular numerals, outlined; for step and room numbering |
| `arrows` | `sanzeed-arrow--{{right-long,left-long,up-long,down-long,diagonal,right-with-point,cta}}--*` | 1.5 px round-capped arrows; `right-with-point` is the point travelling the beam; `cta` is the 24 px "→" used after "Tell me about the room" |
| `lit-glyph` | `sanzeed-glyph-lit-fullstop--*` · `sanzeed-lockup-lit--*` · `sanzeed-lockup-eight-rooms-lit--*` | the gold point sized to the Fraunces 300 full stop (r ≈ 5.6 % of the font size — scale with the type) and the headline lockups "lit." / "Eight rooms, lit." in Fraunces 300 opsz 144, outlined. The last word may be gold **or** the stop may be the point, never both |
| `wall-label` | `sanzeed-wall-label-template--*` · `sanzeed-wall-label-example--*` | caption block under a hairline: Title (Inter Tight 600, 20) · Place (Inter 400, 15, fg-3) · one line (Inter 400, 15, fg-2). Live `<text>` — edit the three lines. The example carries confirmed copy (Prime Minister Museum · New Delhi · "A corridor you walk in order.") |
| `visitors-book` | `sanzeed-visitors-book-rule-block--*` | the site's book-rule (2 px gold rule fading downward, the point at its head) with seven writing hairlines, 720 × 400 — forms, guest-book pages, quote blocks |

PNGs of the live-text templates (frames, wall labels) are rendered with Chromium so the fonts are exact; everything else
through cairosvg.

{table(ROOT/'Decorative_Elements', collapse=[(r'^(svg|png)/counters/sanzeed-counter-badge--', 'counters/sanzeed-counter-badge--001…010--{{dark,light}}'), (r'^(svg|png)/eyebrows/', 'eyebrows/sanzeed-eyebrow--*--{{dark,light}}'), (r'^(svg|png)/arrows/', 'arrows/sanzeed-arrow--*--{{dark,light}}'), (r'^(svg|png)/dividers/', 'dividers/sanzeed-divider-*--{{dark,light}}')])}
''')

# ------------------------------------------------------------------------------------------ root
total = sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
counts = {d.name: sum(1 for p in d.rglob('*') if p.is_file() and p.name != 'README.md' and '__pycache__' not in p.parts) for d in sorted(ROOT.iterdir()) if d.is_dir() and not d.name.startswith('_')}
write(ROOT/'README.md', f'''
# 05_GRAPHIC_ASSETS — the supporting graphic language

Everything here is derived from the seven words of the brand vocabulary (brand kit §6): **the point** (a gold dot, r = 0.7 × its
stroke), **the beam** (the 1 px hairline the point travels), **the room** (radius-28 rounded rectangle, hairline border), **the
doorway / arch** (the ∩ of the N and M), **the route** (points along a beam), **grain** (7 % soft-light, dark only), **the lamp**
(the radial gold glow behind one lit object) and **the wall label** (Title · Place · one line). One gold accent per composition:
Lamp Gold `#E9B25A` on dark, Old Gold `#B8863B` on light (Gold Ink `#8A6124` when gold is text on light).

| Folder | Contents | Files |
|---|---|---|
| [`Patterns/`](Patterns/README.md) | 7 seamless tiles × 2 inks: SVG (with tile guide in `src/`), PNG 2048, `patterns.css`, contact sheet | {counts['Patterns']} |
| [`Textures/`](Textures/README.md) | grain tiles, paper for Plaster / Paper, lamp glow (gold / old gold), vignettes; `generate_textures.py` | {counts['Textures']} |
| [`Illustrations/`](Illustrations/README.md) | orbit object, method diagram, between-two-points, museum route, 7 service glyphs, lamp — SVG + PNG 2000 w + PDF, dark and light | {counts['Illustrations']} |
| [`Icons/`](Icons/README.md) | 54 icons on the 24 grid: SVG, sprite, PNG 48 / 96 in dark and light ink, `icons.html` sheet | {counts['Icons']} |
| [`Backgrounds/`](Backgrounds/README.md) | lamp / dusk / plaster fills in 4 sizes, grain variants, presentation 16:9 set (dark + light), A4 covers (SVG + PDF + PNG), photo plates with wall labels | {counts['Backgrounds']} |
| [`Decorative_Elements/`](Decorative_Elements/README.md) | dividers, room frames with named image placeholder, corner marks, eyebrow lockups, wall-label template, counter badges 001–010, arrows, the 'lit.' full stop, visitor's-book rule block | {counts['Decorative_Elements']} |
| `_build/` | `szlib.py` (shared: colour tokens, brand-font outlining with fontTools, kit-helper wrappers) and `write_readmes.py` | — |

Total: **{human(total)}** on disk.

## Conventions

* **Naming** `sanzeed-<deliverable>--<variant>[-<size>].<ext>`, lowercase, hyphens. `--dark` = drawn for Gallery Black / Night /
  Charcoal (white + Lamp Gold ink); `--light` = drawn for Plaster / Paper / Stone (Soot + Old Gold ink). Never swap them.
* **Editable source + export.** Every PNG / JPG / PDF has its SVG or HTML source beside it, and every folder has a generator
  script that *is* the master (change a number, re-run). Labels inside SVG exports are outlined from the brand fonts, so nothing
  depends on fonts being installed — except the two live-text templates (room frames, wall label), which are templates by design.
* **Logos** are never redrawn here: covers and slide backgrounds embed the production SVGs from `02_LOGO_SYSTEM/SVG/` with the
  pairing rule (`full-colour-dark` on dark, `full-colour-light` on light) and clear space = ½ cap height.
* **Type** Fraunces 300 (opsz 144 / 72) for display words, Inter Tight 600 +0.12 em caps for eyebrows, Inter Tight 500 tabular for
  counters, Inter 400 for captions. Fraunces is never letter-spaced.
* **Imagery** only the client's approved project images (`00_ORIGINAL_ASSETS_BACKUP/images/img/`), always under the veil and
  with a wall label.

## Regenerating

```bash
cd 05_GRAPHIC_ASSETS
python3 Patterns/build_patterns.py
python3 Textures/generate_textures.py
python3 Illustrations/build_illustrations.py        # add a name filter to rebuild one drawing
python3 Icons/build_icons.py
python3 Backgrounds/build_backgrounds.py             # or one group: lamp | dusk | plaster | grain | presentation | covers | plates
python3 Decorative_Elements/build_decorative.py
python3 _build/write_readmes.py                      # refreshes the inventory tables in every README
```

Requirements (all present in the production container): Python 3 with fontTools, cairosvg, Pillow, numpy, pypdf; Inkscape 1.2;
Node with Playwright (Chromium) for `render.js`; the brand fonts in `04_TYPOGRAPHY/Font_Files` (read directly by fontTools; also
installed system-wide for Chromium). The helpers used are the kit's own: `render.js` and `export_svg.py` in
`15_SOURCE_FILES/Project_Files/brand-kit/`.

## Verified

Every render was opened and checked after generation: logo variant and pairing per background, clear space, a single gold accent,
Fraunces rendering as the light serif (outlined from the variable font at wght 300), nothing clipped, no placeholder boxes or dummy
copy (only bracketed field labels in the two templates). Pattern PNGs were tested numerically for seamlessness; photo plates were
measured at ≥ 81 % black under the label and ≥ 88 % under the wordmark; cover PDFs are 210 × 297 mm vector pages.

## Known limits

* The approved project images exist only at 960 × 540, so the 1920 × 1080 photo plates upscale them 2 × (softened under the veil).
* Soft-light grain is invisible on pure `#000000`; the grain backgrounds are therefore supplied on Charcoal, dusk and lamp.
* No `.ai` files (Illustrator-native); every SVG and PDF opens in Illustrator as editable vector.
''')
