# Brochures — A4 trifold and 12-page company profile

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

**A4 trifold** (297×210 mm landscape, 3 mm bleed → page 303×216, 2 pages). Outside spread, dark, panels left→right **98 | 99 | 100 mm** = inside flap (About, portrait, proof numbers, trust line) · back cover (Tell me about the room, contact, promises, descriptor lockup, rights line) · front cover (wordmark, object plate, master line). Inside spread, Plaster, panels **100 | 99 | 98 mm** = seven services · method · now showing (three case studies with wall labels). Fold guides show in the PNG previews only (screen media); the PDFs carry none. Roll fold: the 98 mm panel folds in first.

**12-page company profile** (A4 portrait, 3 mm bleed → page 216×303). 01 cover · 02 the one idea (Carry the light across + brand story) · 03 about, proof, three pillars, quote · 04 seven services · 05 method · 06–07 Prime Minister Museum · 08–09 Ram Katha Show · 10–11 Buddha Park (each a spread: brief, idea and hero image left; four case images with captions, the walk, what visitors do, type/location/role right) · 12 the galleries (all 90), journey timeline, contact. Dark pages for the gallery, Plaster pages for reading. Reader spreads exported as PNG (`--spread-*.png`, bleed cropped).

Print-ready versions add crop marks and CMYK. Saddle-stitch the profile (12 pages = 3 sheets A3 folded).

**How to edit.** `src/sanzeed-brochure--a4-trifold.html`, `src/sanzeed-company-profile--a4-12pp.html` (one `<section class="sheet">` per page), then:
```
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-company-profile--a4-12pp.html --out sanzeed-company-profile--a4-12pp-bleed.pdf --pdf --size 216x303
python3 15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py sanzeed-company-profile--a4-12pp-bleed.pdf sanzeed-company-profile--a4-12pp-print-ready-cmyk.pdf --trim=210x297 --bleed=3 --cmyk
```
Regenerate (also rebuilds the spread PNGs): `python3 _shared/build/build_brochures.py`. Images in PDFs are JPEG copies from `_shared/img/jpg/` (made by `common.jimg`).

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 4 KB |
| `sanzeed-brochure--a4-trifold-bleed.pdf` | 2 pages · 303.0×215.9 mm · fonts embedded | 1.9 MB |
| `sanzeed-brochure--a4-trifold-inside.png` | 2865×2043 px | 1.8 MB |
| `sanzeed-brochure--a4-trifold-outside.png` | 2865×2043 px | 1.3 MB |
| `sanzeed-brochure--a4-trifold-print-ready-cmyk.pdf` | 2 pages · 323.0×236.0 mm · fonts embedded | 3.2 MB |
| `sanzeed-company-profile--a4-12pp--spread-00-cover.png` | 909×1287 px | 211 KB |
| `sanzeed-company-profile--a4-12pp--spread-01-p02-03.png` | 1818×1287 px | 487 KB |
| `sanzeed-company-profile--a4-12pp--spread-02-p04-05.png` | 1818×1287 px | 200 KB |
| `sanzeed-company-profile--a4-12pp--spread-03-p06-07.png` | 1818×1287 px | 1.0 MB |
| `sanzeed-company-profile--a4-12pp--spread-04-p08-09.png` | 1818×1287 px | 1.1 MB |
| `sanzeed-company-profile--a4-12pp--spread-05-p10-11.png` | 1818×1287 px | 1.6 MB |
| `sanzeed-company-profile--a4-12pp--spread-06-back.png` | 909×1287 px | 177 KB |
| `sanzeed-company-profile--a4-12pp-bleed.pdf` | 12 pages · 215.9×303.0 mm · fonts embedded | 4.3 MB |
| `sanzeed-company-profile--a4-12pp-print-ready-cmyk.pdf` | 12 pages · 236.0×323.0 mm · fonts embedded | 9.4 MB |
| `src/sanzeed-brochure--a4-trifold.html` | HTML source (brand.css + collateral.css) | 14 KB |
| `src/sanzeed-company-profile--a4-12pp.html` | HTML source (brand.css + collateral.css) | 39 KB |
