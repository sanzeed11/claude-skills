# 05_GRAPHIC_ASSETS — the supporting graphic language

Everything here is derived from the seven words of the brand vocabulary (brand kit §6): **the point** (a gold dot, r = 0.7 × its
stroke), **the beam** (the 1 px hairline the point travels), **the room** (radius-28 rounded rectangle, hairline border), **the
doorway / arch** (the ∩ of the N and M), **the route** (points along a beam), **grain** (7 % soft-light, dark only), **the lamp**
(the radial gold glow behind one lit object) and **the wall label** (Title · Place · one line). One gold accent per composition:
Lamp Gold `#E9B25A` on dark, Old Gold `#B8863B` on light (Gold Ink `#8A6124` when gold is text on light).

| Folder | Contents | Files |
|---|---|---|
| [`Patterns/`](Patterns/README.md) | 7 seamless tiles × 2 inks: SVG (with tile guide in `src/`), PNG 2048, `patterns.css`, contact sheet | 46 |
| [`Textures/`](Textures/README.md) | grain tiles, paper for Plaster / Paper, lamp glow (gold / old gold), vignettes; `generate_textures.py` | 10 |
| [`Illustrations/`](Illustrations/README.md) | orbit object, method diagram, between-two-points, museum route, 7 service glyphs, lamp — SVG + PNG 2000 w + PDF, dark and light | 73 |
| [`Icons/`](Icons/README.md) | 54 icons on the 24 grid: SVG, sprite, PNG 48 / 96 in dark and light ink, `icons.html` sheet | 274 |
| [`Backgrounds/`](Backgrounds/README.md) | lamp / dusk / plaster fills in 4 sizes, grain variants, presentation 16:9 set (dark + light), A4 covers (SVG + PDF + PNG), photo plates with wall labels | 61 |
| [`Decorative_Elements/`](Decorative_Elements/README.md) | dividers, room frames with named image placeholder, corner marks, eyebrow lockups, wall-label template, counter badges 001–010, arrows, the 'lit.' full stop, visitor's-book rule block | 201 |
| `_build/` | `szlib.py` (shared: colour tokens, brand-font outlining with fontTools, kit-helper wrappers) and `write_readmes.py` | — |

Total: **17.2 MB** on disk.

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
