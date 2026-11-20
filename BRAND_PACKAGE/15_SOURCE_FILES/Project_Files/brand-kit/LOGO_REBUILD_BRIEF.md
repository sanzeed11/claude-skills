# Logo rebuild brief — swap every deliverable to the approved logo

The client has approved a new master logo (20 Nov 2026): **the refined original wordmark, option B**. Folder `02_LOGO_SYSTEM/` has already been fully regenerated with it (same file names as before). Your job is to make every deliverable in your assigned folders use it, then re-export, and verify.

## What changed
- **Wordmark:** the client's own hand-drawn SANZEED (S, A, N, D cleaned; E bars exact) with a new **Z**: straight bars, a diagonal that swoops like the N's right leg, and a **third gold point** at the D-point height inside a thin dark ring. So the wordmark now has **three points (A, Z, D)**, not two.
- **Symbol:** the refined S + full stop (hooked, tapered S — not the old blocky geometric S).
- **Monogram:** "SM." with the M built from two of the wordmark's N.
- **Plain wordmark:** no points; Z ring and D stem closed.
- **Small sizes, tiles, favicons, social profile images:** regenerated.
- The earlier geometric redraw ("500-unit cap / 64-unit stroke construction", blocky S, symmetric arch N, straight Z, two dots) is **retired**. Remove it everywhere.

## Where the new logo lives
- Production SVGs (unioned, use these for embedding): `02_LOGO_SYSTEM/SVG/sanzeed-<variant>--<colour>.svg` — variants: `primary-wordmark`, `wordmark-plain`, `secondary-symbol-wordmark`, `horizontal-descriptor`, `vertical-stacked`, `symbol`, `symbol-small-size`, `monogram`, `simplified-small-size`, `symbol-tile`, `symbol-tile-square`; colours: `full-colour-dark`, `full-colour-light`, `black`, `white`, `grayscale`, `grayscale-inverted`, `single-colour-gold`; tiles `--dark|--light|--gold`.
- Per-letter editable SVGs (for animation): `02_LOGO_SYSTEM/Source_Files/` — the primary wordmark has paths with ids `wordmark-S`, `wordmark-A`, `wordmark-N`, `wordmark-Z`, `wordmark-E1`, `wordmark-E2`, `wordmark-D` and three dot circles (A, Z, D in that order). The raw master with ids `wm-S` … `wm-D` and `class="wm-dot"` circles is `15_SOURCE_FILES/Project_Files/logo-builder/refined_master.svg` (viewBox 0 0 3729 561, same as the live site's wordmark).
- PNG/JPG/WebP/PDF/EPS, `Favicon/`, `Social_Profile/` in `02_LOGO_SYSTEM/`.
- **Aspect ratios changed slightly** (primary wordmark is now ≈ 3692 × 519 units, ratio 7.11:1). Any layout that hard-coded the old width/height or viewBox must be adjusted so the logo is not stretched or clipped.

## How to rebuild
1. Find every place in your folders that carries the logo: file references (paths into 02), **inlined SVG path data** (copied geometry — search for `<svg` blocks with `wordmark`/`symbol`/`monogram` ids or classes, `wordmark-S-0`, `symbol-S-0`, data URIs), rasterised copies (PNG/JPG made from the old logo), embedded images in PPTX/DOCX/PDF, Lottie JSON shapes, favicon copies, and text that describes the old construction (e.g. "500-unit", "64-unit stroke", "two points of light", "geometric construction").
2. Update the sources (HTML/CSS/SVG/Python builders/JSON) to use the new files or new geometry — prefer linking/reading the files in 02 at build time over pasting path data; where inlining is required (websites, animation), inline the new SVG and keep any ids/classes that code depends on.
3. Re-run that folder's own build scripts (see each folder's README for commands) so **every export** is regenerated: PNG, JPG, WebP, PDF, print-ready CMYK PDFs (`brand-kit/print_pdf.py`), PPTX/DOCX (and their soffice PDF/PNG previews), videos/GIFs, contact sheets.
4. Verify: grep your folders again for old-geometry markers and for stale copies; open (Read) a representative sample of renders — the wordmark must show **three gold points with the ringed Z**, the hooked S, the swooping N; correct colourway for the background; nothing stretched or clipped.
5. Update READMEs where they describe the logo.

Rules: do not touch folders outside your assignment; do not change copy, layouts or design beyond what the logo swap requires; keep file names unchanged; never invent content. Do not run git. Finish with a short report: files regenerated (counts per subfolder), anything you could not rebuild and why, remaining references to the old logo (should be none).
