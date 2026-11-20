# Flyers — A5 two-sided flyer and DL leaflet

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

**A5 flyer** (148×210 mm, 3 mm bleed → page 154×216). Front, dark: the key visual (master line, point-of-light object, wall label, CTA). Back, Plaster: the seven services with their lines, “All seven, every time.”, the four method steps with “You receive …”, and contact with the descriptor lockup.

**DL leaflet** (99×210 mm, 3 mm bleed → page 105×216). Front, dark: “Carry the light across.” with the object in a 4:5 plate. Back, Plaster: “Seven ways to carry the light across.” — services, method in one line each, contact.

Exports: `-bleed.pdf` (2 pages, RGB), `-print-ready-cmyk.pdf` (crop marks, CMYK), `-front.png` / `-back.png` previews at 3×.

**How to edit.** `src/*.html`, then:
```
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-flyer--a5-two-sided.html --out sanzeed-flyer--a5-two-sided-bleed.pdf --pdf --size 154x216
python3 15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py sanzeed-flyer--a5-two-sided-bleed.pdf sanzeed-flyer--a5-two-sided-print-ready-cmyk.pdf --trim=148x210 --bleed=3 --cmyk
```
Regenerate: `python3 _shared/build/build_flyers.py`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 3 KB |
| `sanzeed-flyer--a5-two-sided-back.png` | 1749×2451 px | 359 KB |
| `sanzeed-flyer--a5-two-sided-bleed.pdf` | 2 pages · 154.2×215.9 mm · fonts embedded | 389 KB |
| `sanzeed-flyer--a5-two-sided-front.png` | 1749×2451 px | 642 KB |
| `sanzeed-flyer--a5-two-sided-print-ready-cmyk.pdf` | 2 pages · 174.0×236.0 mm · fonts embedded | 331 KB |
| `sanzeed-leaflet--dl-two-sided-back.png` | 1191×2451 px | 308 KB |
| `sanzeed-leaflet--dl-two-sided-bleed.pdf` | 2 pages · 105.2×215.9 mm · fonts embedded | 413 KB |
| `sanzeed-leaflet--dl-two-sided-front.png` | 1191×2451 px | 732 KB |
| `sanzeed-leaflet--dl-two-sided-print-ready-cmyk.pdf` | 2 pages · 125.0×236.0 mm · fonts embedded | 347 KB |
| `src/sanzeed-flyer--a5-two-sided.html` | HTML source (brand.css + collateral.css) | 8 KB |
| `src/sanzeed-leaflet--dl-two-sided.html` | HTML source (brand.css + collateral.css) | 7 KB |
