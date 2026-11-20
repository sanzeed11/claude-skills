# Media kit

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

`sanzeed-media-kit--a4.pdf` — 7 pages: cover · 01 biographies (10 / 25 / 50 words, in his words, boilerplate, naming) · 02 headshots (three crops, with file names and use notes) · 03 fact sheet (confirmed facts only) · 04 logo usage summary (refers to `02_LOGO_SYSTEM`) · 05 projects (the eight “now showing” rooms and all ninety by gallery) · 06 contact. Page previews at 90 dpi. `media-kit-contents.md` lists everything a journalist receives, with the copy blocks as plain text. The headshot JPGs live in `../Press/`.

**How to edit.** `src/sanzeed-media-kit--a4.html`, then `node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-media-kit--a4.html --out sanzeed-media-kit--a4.pdf --pdf --size 210x297`. Regenerate (also re-exports the headshots): `python3 _shared/build/build_mediakit.py`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 2 KB |
| `media-kit-contents.md` | Markdown | 3 KB |
| `sanzeed-media-kit--a4-page-01.png` | 744×1053 px | 382 KB |
| `sanzeed-media-kit--a4-page-02.png` | 744×1053 px | 119 KB |
| `sanzeed-media-kit--a4-page-03.png` | 744×1053 px | 234 KB |
| `sanzeed-media-kit--a4-page-04.png` | 744×1053 px | 124 KB |
| `sanzeed-media-kit--a4-page-05.png` | 744×1053 px | 88 KB |
| `sanzeed-media-kit--a4-page-06.png` | 744×1053 px | 309 KB |
| `sanzeed-media-kit--a4-page-07.png` | 744×1053 px | 37 KB |
| `sanzeed-media-kit--a4.pdf` | 7 pages · 209.9×297.0 mm · fonts embedded | 3.9 MB |
| `src/sanzeed-media-kit--a4.html` | HTML source (brand.css + collateral.css) | 28 KB |
