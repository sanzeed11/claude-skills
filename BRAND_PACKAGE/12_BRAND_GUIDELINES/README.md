# 12_BRAND_GUIDELINES — the brand standards manual

**Sanzeed Mirza · Experiential Design Consultant · New Delhi.** The comprehensive brand guidelines for the Sanzeed identity — 26 chapters plus an appendix on A4 landscape, every page showing the real asset it governs (linked or copied from the other folders of the package, never redrawn) — with its editable HTML + CSS source, a PNG preview of every page, and a two-page quick reference.

Built on the brand kit (`15_SOURCE_FILES/Project_Files/brand-kit`): `doc.css` for the page model, footer and print type scale; `guide.css` beside the chapters for the landscape page, the chapter divider, the figure plates and the small components the manual needs. Body pages on Plaster with Soot type and Gold Ink eyebrows; dark divider pages and dark pages for dark-mode assets; figures carry wall labels (Title · Place · line · source path); running footer `Sanzeed — Brand Guidelines · <chapter> · <page>`.

## Files

| File | Format · spec | Contents / use |
|---|---|---|
| `Brand_Guidelines.pdf` | PDF · 130 pages · A4 landscape 297 × 210 mm · 37 MB · fonts embedded (Fraunces, Inter, Inter Tight; DejaVu Sans Mono for file paths) | Cover · contents · 26 chapters, each opening on a dark divider with its counter and Fraunces title · appendix (delivery index) · back cover. Chapters: 01 Brand introduction · 02 Brand strategy · 03 Positioning · 04 Personality & voice summary · 05 Logo system · 06 Logo construction · 07 Logo variations & colour versions · 08 Clear space & placement · 09 Minimum sizes · 10 Incorrect usage · 11 Signature mark and monogram · 12 Colour system · 13 Typography · 14 Graphic elements · 15 Iconography · 16 Photography standards & art direction · 17 Website application · 18 Digital assets · 19 Social media application · 20 Print & corporate stationery · 21 Marketing materials · 22 Signage & environmental · 23 Motion design · 24 Brand voice & communication · 25 Applications gallery · 26 File formats, naming & production specifications · A Delivery index |
| `Brand_Usage_Reference.md` | Markdown · ≈ 2–3 printed pages | The ten rules, which logo where (with file stems), colour values (HEX / RGB / CMYK / nearest Pantone), the type scale (screen px per breakpoint, print pt), where the files are, naming, contact |
| `Editable_Source/Brand_Guidelines.html` | HTML · the concatenated document | What the PDF is rendered from; opens in a browser (paths are relative to this folder) |
| `Editable_Source/00-cover.html` … `27-appendix.html`, `99-back-cover.html` | HTML · one file per chapter, each a complete page that opens on its own | **The editable layer.** Edit copy or layout here, run `build.py`. `page-manifest.txt` lists each chapter's first page and length |
| `Editable_Source/guide.css` | CSS | Imports the kit's `doc.css`; landscape page, divider, plates, chips, tables, type specimens |
| `Editable_Source/generate_chapters.py` + `lib/guide.py`, `lib/ch_a.py` … `ch_d.py` | Python · the generator | Writes the chapter HTML from the chapter modules; reads `03_COLOUR_SYSTEM/colour-tokens.json`, `04_TYPOGRAPHY/typography-tokens.json`, `06_…/approved.json` and the package file system (folder counts) so data-driven pages never drift. `lib/guide.A()` copies large rasters, downsampled, into `assets/`; `lib/guide.L()` links everything else by relative path and fails the build if a file is missing |
| `Editable_Source/build.py` | Python · the build | Concatenates the chapters → renders the PDF with the kit's `render.js --pdf --size 297x210 --landscape` → writes `pages/*.png` → checks that every `<img src>` resolves and that `pdffonts` lists only the brand fonts. `--ui` re-renders the 26 UI-kit sections used in chapter 17 into `assets/ui/` |
| `Editable_Source/assets/` | PNG / JPG · 36 MB · ≈ 330 files | Working copies of large rasters (contact sheets, mockups, screenshots, specimen sheets, key frames), downsampled to ≤ 1 600 px so the PDF stays compact; `assets/ui/` holds the UI-kit sections rendered at 1440 px. Everything else (logo SVGs, icons, patterns, small PNGs) is linked directly into its folder |
| `Editable_Source/pages/sanzeed-brand-guidelines--p001.png` … `p130.png` | PNG · 1170 × 827 px (100 dpi) · 23 MB | A preview of every page |

Folder total ≈ 100 MB.

## Regenerating

```bash
cd 12_BRAND_GUIDELINES/Editable_Source
python3 build.py --ui              # only if the UI kit changed: re-render its sections (≈ 2 min)
python3 generate_chapters.py       # rewrite the chapter HTML from lib/ch_*.py and the tokens (≈ 1 min; copies assets)
python3 build.py                   # Brand_Guidelines.html → ../Brand_Guidelines.pdf → pages/*.png → checks (≈ 1 min)
python3 build.py --check           # only the image / font checks
```

- **To change copy or a layout on one page:** edit the chapter file (`NN-*.html`) directly and run `build.py`. Re-running `generate_chapters.py` overwrites the chapter files from the Python modules, so carry a hand edit into `lib/ch_*.py` if it must survive regeneration.
- **To change a colour, a type size or an image path everywhere:** edit the token files (or the asset) and run both scripts; the colour, typography, scale and contrast pages, the folder counts in chapter 26 and the appendix are computed.
- **To add a chapter:** add a builder in a `lib/ch_*.py` module and a row to `CHAPTERS` in `generate_chapters.py`; the contents page and footers follow.
- **Verify by looking:** `pdftoppm -r 50 -f N -l N -png ../Brand_Guidelines.pdf page` or open `pages/`.

Requirements (present in the production container): Python 3 with Pillow; Node 22 with Playwright (Chromium) for `render.js`; poppler (`pdftoppm`, `pdffonts`, `pdfinfo`); the brand fonts installed system-wide (`04_TYPOGRAPHY/Font_Files`).

## Rules applied and verified

Every page was rendered and looked at (contact sheets of all 130 pages, plus samples at 80–110 dpi across the chapters): logo variant and pairing per background (`full-colour-dark` on black, `full-colour-light` on Plaster, `black` on the gold tile only), clear space on every plate, one gold accent per page, Fraunces 300 as the light serif, nothing clipped, no empty boxes. `build.py --check`: 486 image references, 0 missing; `pdffonts`: Fraunces, Inter, Inter Tight and DejaVu Sans Mono (the `.mono` face for file paths, as in the other kit documents) — no fallback faces. Copy is confirmed copy from `01_BRAND_STRATEGY` and the package READMEs; the only bracketed placeholders are the ones the templates themselves carry (`[Month Year]`, `[Client]`, `[GSTIN]` …).

## Limitations

- **Length.** The brief expected 70–90 pages; the manual runs to 130 because each of the 26 chapters opens on its own divider page (27 dividers) and the application chapters show every delivered asset rather than a selection. Nothing is padding; trim by dropping gallery pages (chapter 25) or merging dividers if a shorter edition is wanted.
- **No `.indd` / `.ai`.** InDesign and Illustrator can only write their own formats; the editable source is HTML + CSS (and the Python generator), rendered by Chromium. The PDF is vector with embedded fonts and opens in Acrobat, Illustrator and InDesign (place) as any PDF does.
- **Rasters inside the PDF** are working copies at ≤ 1 600 px (≈ 150–250 dpi at the sizes shown), chosen to keep the file at 37 MB; the originals, at full resolution, are in their own folders and are named on each page. The UI-kit sections, website screenshots and mockups are screen assets by nature.
- **Chromium names the Fraunces instances `Fraunces-9ptBlack` in `pdffonts`**; the rendered weight is 300 (the same naming appears in every other PDF of the package).
- Page previews are 100 dpi PNGs for review, not print masters; the PDF is the master.
