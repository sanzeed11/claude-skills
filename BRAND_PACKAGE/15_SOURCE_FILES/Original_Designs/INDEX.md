# Original designs — masters

The masters from which the identity is generated. Change these, re-run the builders, and every export regenerates.

| Master | What it defines | Regenerate with |
|---|---|---|
| `../Project_Files/logo-builder/refined_master.svg` + `build_logo_refined.py` | The approved refined original wordmark (option B) and every variant derived from it: symbol, monogram, lockups, small sizes, tiles, colourways | `python3 build_logo_refined.py construction && python3 export_logo.py construction ../../../02_LOGO_SYSTEM` |
| `../Project_Files/logo-builder/construction/*.svg` | Per-stroke editable construction SVGs of every variant (also in `02_LOGO_SYSTEM/Source_Files`) | opened directly in Illustrator / Figma / Inkscape |
| `../Project_Files/logo-builder/build_logo_guides.py` | Clear-space, minimum-size, incorrect-usage, construction and placement sheets | `python3 build_logo_guides.py` |
| `../Project_Files/colour-builder/build_colour.py` | The palette (names, HEX, roles, usage), gradients, themes, contrast matrix, Pantone proximity, swatches | `python3 build_colour.py ../../../03_COLOUR_SYSTEM` |
| `../../04_TYPOGRAPHY/typography-tokens.json` | The type scale (screen px, print pt) and rules | edit JSON; `brand.css` mirrors it |
| `../Project_Files/brand-kit/brand.css` | Design tokens and base components used by every HTML-authored deliverable | edit; re-render dependants |
| `../Project_Files/brand-kit/doc.css` | A4 document page model for the PDF documents | edit; re-render documents |
| `../../02_LOGO_SYSTEM/Signature/sanzeed-signature--*.svg` | The vectorised signature mark | edit in a vector app |
| `../../00_ORIGINAL_ASSETS_BACKUP/` | The untouched originals from sanzeed.com (reference only) | — |

Production helpers: `../Project_Files/brand-kit/render.js` (HTML → PNG/PDF), `capture_frames.js` (animation → MP4/WebM/GIF/MOV), `export_svg.py` (SVG → PDF/EPS/PNG/WebP), `print_pdf.py` (bleed, crop marks, CMYK), and the QA scripts in `../Project_Files/qa/`.

**Not supplied:** Adobe Illustrator `.ai`, Photoshop `.psd`, InDesign `.indd`, After Effects `.aep`, Figma `.fig` — these proprietary formats can only be written by their own applications. Every SVG/PDF here opens as editable vector in Illustrator and Figma; HTML/CSS and PPTX/DOCX are the editable sources for layouts; Lottie JSON and HTML/CSS are the motion sources (both import into After Effects).