# Signage — door plate, wayfinding, totem, window vinyl, spec sheet

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

Every sign is Gallery Black with Gallery White letters and one gold point. Door plate and wayfinding plates are 300×100 mm (files carry 3 mm bleed: page 306×106 mm); the totem is 600×1800 mm at 1:10; the window vinyl is previewed on a 3000×2000 mm glass bay at 1:10 with a 1:1 cut file of the wordmark at 1200 mm.

| Sign | Content | Cap height |
|---|---|---|
| Door plate | horizontal-descriptor lockup, 180 mm wide | wordmark ≈ 25 mm (3 m viewing) |
| Arrow plates ×4 | monoline arrow (left / right / ahead / down) from `_shared/icons`, symbol at right | arrow box 48 mm |
| Room numbers 001–004 | Fraunces 300 numerals ending in the gold point, symbol at right | ≈ 36 mm |
| Totem | vertical-stacked lockup, directory 001–004 with arrows, master line, URL | directory numerals 90 mm real |
| Window vinyl | frosted band 600 mm, wordmark 1200 mm in white cut vinyl | — |

Each sign: `.html` source → `.pdf` (vector, fonts embedded) → `.svg` (pdftocairo, text as outlines — hand to the sign-maker) → `.png` preview → `-print-ready-cmyk.pdf` for printed plates. `sanzeed-wayfinding-set--8-plates-300x100mm.pdf` collects the eight plates. The spec sheet (A4, light) lists materials, minimum cap heights per viewing distance (25 mm per 3 m), mounting heights and finishes.

**How to edit.** Edit the HTML in `src/`, then:
```
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-door-plate--300x100mm.html --out sanzeed-door-plate--300x100mm.pdf --pdf --size 306x106
pdftocairo -svg sanzeed-door-plate--300x100mm.pdf sanzeed-door-plate--300x100mm.svg
python3 15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py sanzeed-door-plate--300x100mm.pdf sanzeed-door-plate--300x100mm-print-ready-cmyk.pdf --trim=300x100 --bleed=3 --cmyk
```
Regenerate everything: `python3 _shared/build/build_signage.py`. The cut file `sanzeed-window-vinyl--wordmark-cut-1200mm.svg` is rebuilt by `cut_file()` from `02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--white.svg`: 1200 × 168.77 mm (the wordmark's own 7.11:1 ratio), filled closed paths only — the letter outline (Z ring included as a cut-out) plus the three points A, Z, D converted from circles to arc paths — ready for the plotter.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 8 KB |
| `sanzeed-door-plate--300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 18 KB |
| `sanzeed-door-plate--300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 15 KB |
| `sanzeed-door-plate--300x100mm.png` | 3471×1203 px | 69 KB |
| `sanzeed-door-plate--300x100mm.svg` | SVG 866.88 × 300 | 50 KB |
| `sanzeed-signage-spec-sheet--a4.pdf` | 1 page · 209.9×297.0 mm · fonts embedded | 95 KB |
| `sanzeed-signage-spec-sheet--a4.png` | 1588×2246 px | 469 KB |
| `sanzeed-totem--600x1800mm-1-10.pdf` | 1 page · 59.9×179.9 mm · fonts embedded | 52 KB |
| `sanzeed-totem--600x1800mm-1-10.png` | 908×2724 px | 96 KB |
| `sanzeed-totem--600x1800mm-1-10.svg` | SVG 169.92 × 510 | 137 KB |
| `sanzeed-wayfinding--arrow-ahead-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 9 KB |
| `sanzeed-wayfinding--arrow-ahead-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 4 KB |
| `sanzeed-wayfinding--arrow-ahead-300x100mm.png` | 3471×1203 px | 28 KB |
| `sanzeed-wayfinding--arrow-ahead-300x100mm.svg` | SVG 866.88 × 300 | 10 KB |
| `sanzeed-wayfinding--arrow-down-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 9 KB |
| `sanzeed-wayfinding--arrow-down-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 4 KB |
| `sanzeed-wayfinding--arrow-down-300x100mm.png` | 3471×1203 px | 28 KB |
| `sanzeed-wayfinding--arrow-down-300x100mm.svg` | SVG 866.88 × 300 | 10 KB |
| `sanzeed-wayfinding--arrow-left-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 9 KB |
| `sanzeed-wayfinding--arrow-left-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 4 KB |
| `sanzeed-wayfinding--arrow-left-300x100mm.png` | 3471×1203 px | 28 KB |
| `sanzeed-wayfinding--arrow-left-300x100mm.svg` | SVG 866.88 × 300 | 10 KB |
| `sanzeed-wayfinding--arrow-right-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 9 KB |
| `sanzeed-wayfinding--arrow-right-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 4 KB |
| `sanzeed-wayfinding--arrow-right-300x100mm.png` | 3471×1203 px | 28 KB |
| `sanzeed-wayfinding--arrow-right-300x100mm.svg` | SVG 866.88 × 300 | 10 KB |
| `sanzeed-wayfinding--room-001-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 10 KB |
| `sanzeed-wayfinding--room-001-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 7 KB |
| `sanzeed-wayfinding--room-001-300x100mm.png` | 3471×1203 px | 50 KB |
| `sanzeed-wayfinding--room-001-300x100mm.svg` | SVG 866.88 × 300 | 12 KB |
| `sanzeed-wayfinding--room-002-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 11 KB |
| `sanzeed-wayfinding--room-002-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 8 KB |
| `sanzeed-wayfinding--room-002-300x100mm.png` | 3471×1203 px | 62 KB |
| `sanzeed-wayfinding--room-002-300x100mm.svg` | SVG 866.88 × 300 | 13 KB |
| `sanzeed-wayfinding--room-003-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 11 KB |
| `sanzeed-wayfinding--room-003-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 7 KB |
| `sanzeed-wayfinding--room-003-300x100mm.png` | 3471×1203 px | 60 KB |
| `sanzeed-wayfinding--room-003-300x100mm.svg` | SVG 866.88 × 300 | 13 KB |
| `sanzeed-wayfinding--room-004-300x100mm-print-ready-cmyk.pdf` | 1 page · 326.0×126.0 mm · fonts embedded | 11 KB |
| `sanzeed-wayfinding--room-004-300x100mm.pdf` | 1 page · 305.8×105.8 mm · fonts embedded | 7 KB |
| `sanzeed-wayfinding--room-004-300x100mm.png` | 3471×1203 px | 56 KB |
| `sanzeed-wayfinding--room-004-300x100mm.svg` | SVG 866.88 × 300 | 13 KB |
| `sanzeed-wayfinding-set--8-plates-300x100mm.pdf` | 8 pages · 305.8×105.8 mm · fonts embedded | 40 KB |
| `sanzeed-window-vinyl--preview-3000x2000mm-1-10.pdf` | 1 page · 299.9×200.1 mm · fonts embedded | 124 KB |
| `sanzeed-window-vinyl--preview-3000x2000mm-1-10.png` | 3402×2268 px | 1.3 MB |
| `sanzeed-window-vinyl--preview-3000x2000mm-1-10.svg` | SVG 850.07996 × 567.12 | 333 KB |
| `sanzeed-window-vinyl--wordmark-cut-1200mm.svg` | SVG 1200mm × 168.77mm | 15 KB |
| `src/sanzeed-door-plate--300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-signage-spec-sheet--a4.html` | HTML source (brand.css + collateral.css) | 6 KB |
| `src/sanzeed-totem--600x1800mm-1-10.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--arrow-ahead-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--arrow-down-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--arrow-left-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--arrow-right-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--room-001-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--room-002-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--room-003-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-wayfinding--room-004-300x100mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-window-vinyl--preview-3000x2000mm-1-10.html` | HTML source (brand.css + collateral.css) | 2 KB |
