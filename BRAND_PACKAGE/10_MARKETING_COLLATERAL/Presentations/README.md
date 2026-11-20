# Presentations — sales deck, proposal template, case-study and portfolio templates

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

**Sales presentation** `sanzeed-sales-presentation--16-slides.pptx` (16:9, 13.333×7.5 in, 16 slides): 01 cover · 02 the one idea · 03 about · 04 proof · 05 three pillars · 06 seven services · 07 now showing (eight rooms) · 08 method · 09–10 Prime Minister Museum · 11 Ram Katha Show · 12 Buddha Park · 13 journey · 14 how a project starts (project types, timelines, budget bands from the enquiry form) · 15 quote · 16 contact. Also as PDF and one PNG per slide (`--slide-NN.png`).

**Proposal template** `sanzeed-proposal-template--12-slides.pptx` (12 slides): cover · the room · the story · approach · scope · deliverables · timeline · investment bands · team · why Sanzeed · selected work · next step. Every `[bracketed]` field is for the client/project; the investment slide carries `[GSTIN]` and `[Bank name]` fields. Also PDF + PNG per slide.

Both decks are built with python-pptx and are fully editable in PowerPoint/Keynote/Google Slides. Fonts used by name: **Fraunces Light**, **Inter Tight SemiBold**, **Inter**, **Inter Medium** — install the static instances from `_shared/fonts-static/` (derived from `04_TYPOGRAPHY`) so the decks render as designed. Images are JPEG copies in `src/assets/` (the Prime Minister Museum corridor, `case--prime-minister-museum-03.jpg`, is the levels-restored copy — see `_shared/README.md`); pictures are masked to rounded rectangles (the room) with a hairline.

**Case-study template** — A4, 2 pages, from HTML: `--filled-prime-minister-museum` (complete) and `--blank` (bracketed fields and labelled image slots). **Portfolio template** — A4 landscape, 12 pages: cover · 10 projects (one per page, full-bleed-style plate, counter, title, place, category, wall label; the three case studies carry their idea line) · contact.

**How to edit.** Decks: open the PPTX, or edit `_shared/build/build_presentations.py` and re-run (`python3 _shared/build/build_presentations.py`; PDF/PNG come from `soffice --headless --convert-to pdf` + `pdftoppm`). Templates: `src/*.html` then e.g. `node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-portfolio-template--a4-landscape.html --out sanzeed-portfolio-template--a4-landscape.pdf --pdf --size 297x210`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 10 KB |
| `sanzeed-case-study-template--blank-a4--page-01.png` | 662×936 px | 26 KB |
| `sanzeed-case-study-template--blank-a4--page-02.png` | 662×936 px | 32 KB |
| `sanzeed-case-study-template--blank-a4.pdf` | 2 pages · 209.9×297.0 mm · fonts embedded | 132 KB |
| `sanzeed-case-study-template--filled-prime-minister-museum-a4--page-01.png` | 662×936 px | 267 KB |
| `sanzeed-case-study-template--filled-prime-minister-museum-a4--page-02.png` | 662×936 px | 297 KB |
| `sanzeed-case-study-template--filled-prime-minister-museum-a4.pdf` | 2 pages · 209.9×297.0 mm · fonts embedded | 886 KB |
| `sanzeed-portfolio-template--a4-landscape--page-01.png` | 936×662 px | 293 KB |
| `sanzeed-portfolio-template--a4-landscape--page-02.png` | 936×662 px | 388 KB |
| `sanzeed-portfolio-template--a4-landscape--page-03.png` | 936×662 px | 543 KB |
| `sanzeed-portfolio-template--a4-landscape--page-04.png` | 936×662 px | 564 KB |
| `sanzeed-portfolio-template--a4-landscape--page-05.png` | 936×662 px | 525 KB |
| `sanzeed-portfolio-template--a4-landscape--page-06.png` | 936×662 px | 396 KB |
| `sanzeed-portfolio-template--a4-landscape--page-07.png` | 936×662 px | 656 KB |
| `sanzeed-portfolio-template--a4-landscape--page-08.png` | 936×662 px | 569 KB |
| `sanzeed-portfolio-template--a4-landscape--page-09.png` | 936×662 px | 499 KB |
| `sanzeed-portfolio-template--a4-landscape--page-10.png` | 936×662 px | 553 KB |
| `sanzeed-portfolio-template--a4-landscape--page-11.png` | 936×662 px | 362 KB |
| `sanzeed-portfolio-template--a4-landscape--page-12.png` | 936×662 px | 37 KB |
| `sanzeed-portfolio-template--a4-landscape.pdf` | 12 pages · 297.0×209.9 mm · fonts embedded | 1.9 MB |
| `sanzeed-proposal-template--12-slides--slide-01.png` | 1280×720 px | 87 KB |
| `sanzeed-proposal-template--12-slides--slide-02.png` | 1280×720 px | 60 KB |
| `sanzeed-proposal-template--12-slides--slide-03.png` | 1280×720 px | 39 KB |
| `sanzeed-proposal-template--12-slides--slide-04.png` | 1280×720 px | 69 KB |
| `sanzeed-proposal-template--12-slides--slide-05.png` | 1280×720 px | 93 KB |
| `sanzeed-proposal-template--12-slides--slide-06.png` | 1280×720 px | 44 KB |
| `sanzeed-proposal-template--12-slides--slide-07.png` | 1280×720 px | 36 KB |
| `sanzeed-proposal-template--12-slides--slide-08.png` | 1280×720 px | 54 KB |
| `sanzeed-proposal-template--12-slides--slide-09.png` | 1280×720 px | 126 KB |
| `sanzeed-proposal-template--12-slides--slide-10.png` | 1280×720 px | 67 KB |
| `sanzeed-proposal-template--12-slides--slide-11.png` | 1280×720 px | 480 KB |
| `sanzeed-proposal-template--12-slides--slide-12.png` | 1280×720 px | 76 KB |
| `sanzeed-proposal-template--12-slides.pdf` | 12 pages · 338.7×190.5 mm · fonts embedded | 928 KB |
| `sanzeed-proposal-template--12-slides.pptx` | 12 slides · 13.333×7.5 in (16:9) | 1.1 MB |
| `sanzeed-sales-presentation--16-slides--slide-01.png` | 1280×720 px | 128 KB |
| `sanzeed-sales-presentation--16-slides--slide-02.png` | 1280×720 px | 220 KB |
| `sanzeed-sales-presentation--16-slides--slide-03.png` | 1280×720 px | 340 KB |
| `sanzeed-sales-presentation--16-slides--slide-04.png` | 1280×720 px | 44 KB |
| `sanzeed-sales-presentation--16-slides--slide-05.png` | 1280×720 px | 60 KB |
| `sanzeed-sales-presentation--16-slides--slide-06.png` | 1280×720 px | 121 KB |
| `sanzeed-sales-presentation--16-slides--slide-07.png` | 1280×720 px | 769 KB |
| `sanzeed-sales-presentation--16-slides--slide-08.png` | 1280×720 px | 84 KB |
| `sanzeed-sales-presentation--16-slides--slide-09.png` | 1280×720 px | 414 KB |
| `sanzeed-sales-presentation--16-slides--slide-10.png` | 1280×720 px | 391 KB |
| `sanzeed-sales-presentation--16-slides--slide-11.png` | 1280×720 px | 499 KB |
| `sanzeed-sales-presentation--16-slides--slide-12.png` | 1280×720 px | 570 KB |
| `sanzeed-sales-presentation--16-slides--slide-13.png` | 1280×720 px | 81 KB |
| `sanzeed-sales-presentation--16-slides--slide-14.png` | 1280×720 px | 73 KB |
| `sanzeed-sales-presentation--16-slides--slide-15.png` | 1280×720 px | 41 KB |
| `sanzeed-sales-presentation--16-slides--slide-16.png` | 1280×720 px | 73 KB |
| `sanzeed-sales-presentation--16-slides.pdf` | 16 pages · 338.7×190.5 mm · fonts embedded | 3.5 MB |
| `sanzeed-sales-presentation--16-slides.pptx` | 16 slides · 13.333×7.5 in (16:9) | 4.6 MB |
| `src/sanzeed-case-study-template--blank.html` | HTML source (brand.css + collateral.css) | 7 KB |
| `src/sanzeed-case-study-template--filled-prime-minister-museum.html` | HTML source (brand.css + collateral.css) | 8 KB |
| `src/sanzeed-portfolio-template--a4-landscape.html` | HTML source (brand.css + collateral.css) | 12 KB |
| `src/assets/_hero-object--dark-2400.jpg` | 1400×788 px | 57 KB |
| `src/assets/_hero-object--dark-4x5-1600.jpg` | 1400×1750 px | 142 KB |
| `src/assets/_portrait--1x1-2000.jpg` | 1400×1400 px | 230 KB |
| `src/assets/_portrait--4x5-2000.jpg` | 1400×1750 px | 265 KB |
| `src/assets/buddha-park.jpg` | 960×541 px | 186 KB |
| `src/assets/case--buddha-park-02.jpg` | 1400×788 px | 342 KB |
| `src/assets/case--buddha-park-05.jpg` | 1400×788 px | 261 KB |
| `src/assets/case--buddha-park-06.jpg` | 1400×788 px | 274 KB |
| `src/assets/case--buddha-park-08.jpg` | 1400×788 px | 348 KB |
| `src/assets/case--prime-minister-museum-01.jpg` | 1400×788 px | 135 KB |
| `src/assets/case--prime-minister-museum-02.jpg` | 1400×788 px | 206 KB |
| `src/assets/case--prime-minister-museum-03.jpg` | 1400×788 px | 152 KB |
| `src/assets/case--prime-minister-museum-04.jpg` | 1400×788 px | 151 KB |
| `src/assets/case--prime-minister-museum-05.jpg` | 1400×788 px | 156 KB |
| `src/assets/case--prime-minister-museum-06.jpg` | 1400×788 px | 190 KB |
| `src/assets/case--prime-minister-museum-07.jpg` | 1400×788 px | 145 KB |
| `src/assets/case--ram-katha-show-01.jpg` | 1400×788 px | 114 KB |
| `src/assets/case--ram-katha-show-02.jpg` | 1400×788 px | 85 KB |
| `src/assets/case--ram-katha-show-03.jpg` | 1400×788 px | 77 KB |
| `src/assets/case--ram-katha-show-07.jpg` | 1400×788 px | 289 KB |
| `src/assets/g20-tree-show.jpg` | 920×516 px | 142 KB |
| `src/assets/india-pavilion-expo-2025.jpg` | 960×540 px | 93 KB |
| `src/assets/prime-minister-museum.jpg` | 960×540 px | 110 KB |
| `src/assets/ram-katha-show.jpg` | 920×514 px | 156 KB |
| `src/assets/rbi-museum-interior.jpg` | 960×541 px | 159 KB |
| `src/assets/tribal-museum.jpg` | 960×541 px | 168 KB |
| `src/assets/yuge-yugin-bharat-museum.jpg` | 960×541 px | 137 KB |
