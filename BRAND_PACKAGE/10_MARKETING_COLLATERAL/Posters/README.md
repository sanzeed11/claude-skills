# Posters — campaign, method, typographic

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

Three posters at A2 (420×594 mm) and A3 (297×420 mm), each with 3 mm bleed in the PDF (A2 page 426×600, A3 page 303×426):

1. **Campaign** — “Carry the light across.” on black, the point-of-light object in a room plate, wall label, contact.
2. **Method** — “A method for the monumental.” on black; the four steps on a vertical route with gold points and “You receive …” deliverables.
3. **Typographic** — “90 projects, one continuous craft.” on Plaster; all ninety projects listed by gallery with 001–090 counters and wall labels.

Exports per poster and size: `-bleed.pdf` (RGB, for screen proofing), `-print-ready-cmyk.pdf` (crop marks, trim/bleed boxes, CMYK), `-preview.png`. The A3 is the A2 layout scaled by 0.7071 in the source.

**Resolution note.** The campaign poster’s image is the 1600×900 px site render, upsampled to 2400 px; at A2 it prints at ≈ 170 dpi. For a press run at full quality, supply a higher-resolution render of the object and drop it into `_shared/img/hero-object--dark-2400.jpg`.

**How to edit.** `src/sanzeed-poster--<name>-<size>.html`, then:
```
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-poster--campaign-a2.html --out sanzeed-poster--campaign-a2-bleed.pdf --pdf --size 426x600
python3 15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py sanzeed-poster--campaign-a2-bleed.pdf sanzeed-poster--campaign-a2-print-ready-cmyk.pdf --trim=420x594 --bleed=3 --cmyk
```
Regenerate all six: `python3 _shared/build/build_posters.py`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 4 KB |
| `sanzeed-poster--campaign-a2-bleed.pdf` | 1 page · 426.1×600.0 mm · fonts embedded | 230 KB |
| `sanzeed-poster--campaign-a2-preview.png` | 2417×3402 px | 1.3 MB |
| `sanzeed-poster--campaign-a2-print-ready-cmyk.pdf` | 1 page · 446.0×620.0 mm · fonts embedded | 417 KB |
| `sanzeed-poster--campaign-a3-bleed.pdf` | 1 page · 303.0×426.1 mm · fonts embedded | 230 KB |
| `sanzeed-poster--campaign-a3-preview.png` | 2292×3222 px | 1.1 MB |
| `sanzeed-poster--campaign-a3-print-ready-cmyk.pdf` | 1 page · 323.0×446.0 mm · fonts embedded | 417 KB |
| `sanzeed-poster--method-a2-bleed.pdf` | 1 page · 426.1×600.0 mm · fonts embedded | 120 KB |
| `sanzeed-poster--method-a2-preview.png` | 2417×3402 px | 378 KB |
| `sanzeed-poster--method-a2-print-ready-cmyk.pdf` | 1 page · 446.0×620.0 mm · fonts embedded | 104 KB |
| `sanzeed-poster--method-a3-bleed.pdf` | 1 page · 303.0×426.1 mm · fonts embedded | 117 KB |
| `sanzeed-poster--method-a3-preview.png` | 2292×3222 px | 351 KB |
| `sanzeed-poster--method-a3-print-ready-cmyk.pdf` | 1 page · 323.0×446.0 mm · fonts embedded | 105 KB |
| `sanzeed-poster--typographic-a2-bleed.pdf` | 1 page · 426.1×600.0 mm · fonts embedded | 126 KB |
| `sanzeed-poster--typographic-a2-preview.png` | 2417×3402 px | 637 KB |
| `sanzeed-poster--typographic-a2-print-ready-cmyk.pdf` | 1 page · 446.0×620.0 mm · fonts embedded | 101 KB |
| `sanzeed-poster--typographic-a3-bleed.pdf` | 1 page · 303.0×426.1 mm · fonts embedded | 126 KB |
| `sanzeed-poster--typographic-a3-preview.png` | 2292×3222 px | 608 KB |
| `sanzeed-poster--typographic-a3-print-ready-cmyk.pdf` | 1 page · 323.0×446.0 mm · fonts embedded | 102 KB |
| `src/sanzeed-poster--campaign-a2.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-poster--campaign-a3.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-poster--method-a2.html` | HTML source (brand.css + collateral.css) | 5 KB |
| `src/sanzeed-poster--method-a3.html` | HTML source (brand.css + collateral.css) | 5 KB |
| `src/sanzeed-poster--typographic-a2.html` | HTML source (brand.css + collateral.css) | 13 KB |
| `src/sanzeed-poster--typographic-a3.html` | HTML source (brand.css + collateral.css) | 13 KB |
