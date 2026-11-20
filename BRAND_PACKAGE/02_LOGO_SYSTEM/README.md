# 02_LOGO_SYSTEM — the Sanzeed logo family

**Approved master (20 November 2026): the refined original wordmark, option B.** It is the hand-drawn wordmark from sanzeed.com, cleaned letter by letter rather than redrawn: S, A, N and D keep their original shapes with smooth edges and truly straight lines; the E bars are exact rectangles at their original sizes; the two original gold points keep their size and position. The only new letter is the Z: straight top and bottom bars, a diagonal that swoops like the N's right leg, and a third point of light at the D-point height, separated from the stroke by a thin ring.

Every file here is generated from that master: `15_SOURCE_FILES/Project_Files/logo-builder/refined_master.svg` (the outlines) and `build_logo_refined.py` (derives the symbol, monogram, lockups, small sizes and tiles), exported by `export_logo.py` (Inkscape boolean union → genuine PDF/EPS via Inkscape, transparent PNG via cairosvg, JPG via Pillow, WebP via cwebp). The symbol is the refined S with its full stop; the monogram is "SM." with an M built from two of your N's. The hand-lettered signature is traced from the original artwork with potrace. The earlier geometric redraw is retained only as `build_logo_geometric_v1.py` for reference; it is no longer used.

## The family

| # | Variant | File stem | Use |
|---|---|---|---|
| 1 | **Primary logo** — wordmark with its three points of light (A, Z, D) | `sanzeed-primary-wordmark` | Default everywhere: website header, covers, social banners, signage |
| 2 | **Secondary logo** — symbol + wordmark, horizontal | `sanzeed-secondary-symbol-wordmark` | Partner lockups, document footers, when the symbol needs introducing |
| 3 | **Horizontal logo** — wordmark with descriptor justified beneath | `sanzeed-horizontal-descriptor` | Stationery, proposals, invoices, press, anything formal |
| 4 | **Vertical / stacked logo** — symbol, wordmark, descriptor centred | `sanzeed-vertical-stacked` | Square and centred layouts, end cards, stamps, ID cards |
| 5 | **Symbol / icon** — the S with its full stop ("S.") | `sanzeed-symbol` | Avatars, favicons, app icons, watermarks, pattern |
| 6 | **Monogram** — "SM." (Sanzeed Mirza), the M built from two of the wordmark's N | `sanzeed-monogram` | Seals, embossing, ID-card reverse, cufflink-scale uses |
| 7 | **Wordmark (plain)** — letters without points; the Z ring and the D stem are closed | `sanzeed-wordmark-plain` | Engraving, embroidery, single-tool cutting where a dot cannot be produced |
| 8 | **Simplified / small-size logo** — strokes thickened by 10 units per side, rings re-opened around larger points | `sanzeed-simplified-small-size` | 24–120 px on screen, 6–28 mm in print |
| 9 | **Small-size symbol** | `sanzeed-symbol-small-size` | Under 24 px / 6 mm |
| 10 | **Symbol tile** (rounded square, dark / light / gold) and square tile | `sanzeed-symbol-tile--*`, `sanzeed-symbol-tile-square--*` | Favicon, app icon, social profile image |
| 11 | **Signature mark** | `Signature/sanzeed-signature--*` | Personal layer: letters, thank-you cards, sign-offs |

## Colour versions (every variant 1–9)

| Suffix | Letters | Dots | For |
|---|---|---|---|
| `--full-colour-dark` | Gallery White #F5F5F7 | Lamp Gold #E9B25A | dark backgrounds (default on screen) |
| `--full-colour-light` | Soot #1A1816 | Old Gold #B8863B | light backgrounds (documents, print) |
| `--black` | #000000 | #000000 | single-ink print, fax, engraving |
| `--white` | #FFFFFF | #FFFFFF | reversed out of dark photography or solid colour |
| `--grayscale` / `--grayscale-inverted` | black / white | 55 % grey | mono print on light / on dark |
| `--single-colour-gold` | Old Gold | Old Gold | spot-colour or foil |

## Formats

| Folder | Format | Produced by | Notes |
|---|---|---|---|
| `Source_Files/` | SVG with every stroke as a separate editable sub-path (`id="wordmark-S-0"` …) | `build_logo.py` | the construction source; open in Illustrator, Figma, Affinity, Inkscape |
| `SVG/` | SVG, one unioned outline per colour group | Inkscape path-union | production vector for web and apps |
| `PDF/` | PDF 1.5, vector, cairo | Inkscape | print and office |
| `EPS/` | EPS Level 2, vector, cairo | Inkscape `--export-type=eps` | legacy print workflows — a genuine EPS, not a renamed file |
| `PNG/` | transparent, widths in the filename | cairosvg | screen |
| `JPG/` | on white (or on Night for white/dark versions, named `-on-dark`) | Pillow, q 94 | where transparency is not supported |
| `WebP/` | lossless-quality 92 with exact alpha | cwebp | website |
| `Favicon/` | ICO (16/32/48/64), PNG 16–1024, SVG, apple-touch, android-chrome, maskable, `site.webmanifest`, `favicon-head-snippet.html` | `export_logo.py` | |
| `Social_Profile/` | square PNG at each platform's size, dark and light, plus a circle-crop preview | `export_logo.py` | |
| `Full_Color/ Black/ White/ Grayscale/ Single_Color/` | SVG + largest PNG of every variant in that colour | copies | convenience sets |
| `Signature/` | SVG, PDF, EPS, PNG 2400 w in ink, white, gold, gold-light, black | potrace + Inkscape | |

**Not supplied: `.ai` files.** Adobe Illustrator's native format can only be written by Illustrator. Every SVG and PDF here opens in Illustrator as fully editable vector artwork (File → Open; the PDFs are cairo vector PDFs with no rasterisation). Save-as `.ai` from Illustrator if you need the native format. The EPS files are genuine, written by Inkscape's cairo backend.

## Rules (see also `12_BRAND_GUIDELINES`)

- **Clear space:** x = ½ cap height of the logo in use, on all sides (symbol on its own: ¼ of its height).
- **Minimum size:** wordmark 120 px / 28 mm; horizontal-descriptor 220 px / 50 mm; vertical 90 px / 22 mm; symbol 16 px / 6 mm; below those use the simplified/small-size versions.
- **Backgrounds:** flat brand colours or photography darkened to ≥ 80 % black under the logo. Never on gold (except the black logo on the gold tile), never on busy imagery.
- **Placement:** top-left or centred; on documents the horizontal-descriptor lockup sits top-left at 20 mm margins; on covers the primary wordmark sits bottom-left or centred with the lamp glow behind.
- **Incorrect usage:** no stretching, rotation, outlines, drop shadows, bevels, recolouring of dots to non-gold, letter-spacing changes, typeset substitutes, cropping of the S, the light version on dark or the dark version on light.

## Regenerating

```bash
python3 15_SOURCE_FILES/Project_Files/logo-builder/build_logo_refined.py 15_SOURCE_FILES/Project_Files/logo-builder/construction
python3 15_SOURCE_FILES/Project_Files/logo-builder/export_logo.py 15_SOURCE_FILES/Project_Files/logo-builder/construction 02_LOGO_SYSTEM
python3 15_SOURCE_FILES/Project_Files/logo-builder/build_logo_guides.py
```
To change a letter, edit its path in `refined_master.svg` (ids `wm-S`, `wm-A`, `wm-N`, `wm-Z`, `wm-E1`, `wm-E2`, `wm-D`) in any vector editor, save, and re-run. Requires Python 3 with fontTools, cairosvg, Pillow, numpy; Inkscape 1.2+; potrace; cwebp.
