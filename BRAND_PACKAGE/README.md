# SANZEED — Complete Brand Package

**Brand:** Sanzeed Mirza · Experiential Design Consultant · New Delhi · sanzeed.com
**Version:** 1.0 · 5 November 2026 · prepared from an audit of the live website and its source

This package is the complete brand ecosystem: strategy, the constructed logo family, colour and type systems, graphic language, photography direction, website design system and implementation, digital and social assets, stationery, marketing collateral, motion identity, brand guidelines, the final presentation, realistic mockups, and — most importantly — **the editable sources and production exports for every one of them.** Nothing here is a mockup of a deliverable; every item is the deliverable, with its source beside it.

Start with `DELIVERY_CHECKLIST.md` (every deliverable, its path, format and measured status) and `12_BRAND_GUIDELINES/Brand_Guidelines.pdf` (the standards manual). `14_PRESENTATION/Brand_Presentation.pdf` is the reveal deck.

## The identity in one paragraph

The idea is **"Carry the light across."** A brief on one side, a visitor on the other; Sanzeed's work carries the light between them. The system is built from three things: **the point** (a gold dot — the point of light), **the beam** (the hairline it travels), and **the room** (the dark field everything sits in). The wordmark is your original hand-drawn SANZEED, cleaned letter by letter, with a new swooping Z that carries a third point of light; the symbol is the S with its full stop; the colours are Gallery Black and Plaster with one Lamp Gold accent; the type is Fraunces 300 for display and Inter / Inter Tight for everything read. The identity evolves and codifies what already existed on sanzeed.com rather than replacing it (see `01_BRAND_STRATEGY/Brand_Strategy.md`, §11, for the three routes considered).

## Folder map

| Folder | What is in it |
|---|---|
| `00_ORIGINAL_ASSETS_BACKUP/` | Untouched copies of the live site (HTML, images, fonts, icons, screenshots) before any change |
| `01_BRAND_STRATEGY/` | Brand audit, strategy, positioning, voice & tone, messaging (Markdown + designed PDF) |
| `02_LOGO_SYSTEM/` | 11 logo variants × 7 colourways in SVG, PDF, EPS, PNG, JPG, WebP; favicons, social tiles, signature mark, construction sources, guideline sheets |
| `03_COLOUR_SYSTEM/` | Tokens (JSON, CSS, SCSS, Tailwind), swatches, Colour_Palette.pdf, Colour_Reference.md |
| `04_TYPOGRAPHY/` | OFL fonts (TTF + woff2 + licences), type scale tokens, specimens, Font_Reference.pdf, Font_Licensing.md |
| `05_GRAPHIC_ASSETS/` | Patterns, textures, illustrations, icon set, backgrounds, decorative elements (SVG + PNG + PDF) |
| `06_PHOTOGRAPHY_ART_DIRECTION/` | Moodboard.pdf, Photography_Guidelines.pdf, graded approved image library, treatment templates |
| `07_WEBSITE_DIGITAL_ASSETS/` | UI component library, responsive renders, favicons/app icons, Open Graph, email header & signature, website graphics |
| `08_SOCIAL_MEDIA/` | Profiles, covers, banners and editable templates (HTML + PPTX) for Instagram, Facebook, LinkedIn, YouTube, X, Pinterest |
| `09_PRINT_STATIONERY/` | Business cards, letterheads, envelopes, invoice/quotation/proposal/official DOCX, presentation PPTX, covers, folder, notepad, ID card, stamp, thank-you cards; CMYK print-ready PDFs |
| `10_MARKETING_COLLATERAL/` | Ads, key visuals, events, exhibition, signage, posters, flyers, brochures, media kit, decks, case-study and portfolio templates, press |
| `11_MOTION_GRAPHICS/` | Logo reveal/outro, loader, transition, intro/outro, social animations, lower thirds — HTML/CSS + Lottie sources, MP4/WebM/GIF/ProRes-alpha exports, Motion_Principles.md |
| `12_BRAND_GUIDELINES/` | Brand_Guidelines.pdf (26 chapters), editable HTML source, Brand_Usage_Reference.md |
| `13_BRAND_MOCKUPS/` | Logo, stationery, digital and marketing mockups built from the real deliverables |
| `14_PRESENTATION/` | Brand_Presentation.pdf and the editable PPTX / HTML source |
| `15_SOURCE_FILES/` | The brand kit (tokens CSS, render/capture/export/print helpers, production brief), the logo master (refined original wordmark) and the colour master, QA tooling, and the index of every editable source |
| `16_WEBSITE_IMPLEMENTATION/` | The existing website rebuilt with the identity applied — deployable static site with change log and verification screenshots |

Every folder has its own `README.md` listing each file, its spec and how to edit it.

## How to edit and regenerate

- **Logos:** edit the outlines in `15_SOURCE_FILES/Project_Files/logo-builder/refined_master.svg`, run `build_logo_refined.py`, then `export_logo.py` → every format regenerates. Or open any `02_LOGO_SYSTEM/Source_Files/*.svg` in Illustrator / Figma / Affinity / Inkscape.
- **Colours:** edit the palette in `15_SOURCE_FILES/Project_Files/colour-builder/build_colour.py` and run it → tokens, CSS, swatches and reference regenerate.
- **Layouts (documents, social, ads, posters, UI):** each has an HTML+CSS source using `15_SOURCE_FILES/Project_Files/brand-kit/brand.css`; render with `node brand-kit/render.js --in file.html --out file.png|pdf …` (commands are in each folder's README).
- **Office templates:** `.docx` / `.pptx` open in Word, PowerPoint, Pages, Keynote, Google Docs/Slides. Install the fonts from `04_TYPOGRAPHY/Font_Files` first (Fraunces, Inter, Inter Tight — SIL OFL, free to install and redistribute).
- **Motion:** edit the CSS `@keyframes` in `11_MOTION_GRAPHICS/Source_Files/<name>/index.html`, re-render with `brand-kit/capture_frames.js`; Lottie JSON files import into After Effects / LottieFiles.
- **Print:** `brand-kit/print_pdf.py` adds bleed sheets, crop marks, trim/bleed boxes and converts to CMYK.

Requirements for regeneration: Python 3 (fontTools, cairosvg, Pillow, pypdf, reportlab, python-docx, python-pptx, numpy), Node with Playwright (Chromium), Inkscape 1.2+, Ghostscript, ffmpeg, cwebp, LibreOffice. Exported files need nothing.

## Formats and honest limitations

- **Supplied:** SVG, PDF (vector), EPS (genuine, written by Inkscape's cairo backend), PNG (transparent), JPG, WebP, ICO, DOCX, PPTX, HTML/CSS/JS, Lottie JSON, MP4 (H.264), WebM (VP9, alpha where relevant), MOV (ProRes 4444 alpha), GIF, TTF/woff2 fonts, JSON/CSS/SCSS tokens.
- **Not supplied:** Adobe Illustrator `.ai`, Photoshop `.psd`, InDesign `.indd`, After Effects `.aep`, Figma `.fig`, Canva. These proprietary formats can only be written by their own applications and no file here has been renamed to fake them. Every SVG and PDF opens as fully editable vector artwork in Illustrator and Figma; the HTML/CSS, DOCX and PPTX files are the editable layouts; Lottie and HTML/CSS are the editable motion sources and import into After Effects.
- **Imagery:** all project imagery is the client's own (from sanzeed.com) at web resolution (960–1600 px). Large-format print items that use it are flagged in their READMEs; supply original photographs ≥ 2000 px and re-run the build scripts for litho print.
- **Business details** not stated on the website (GSTIN/PAN, bank details, postal address, fees) are left as bracketed fields in templates, never invented.
- **Pantone:** references are nearest matches with a reliability note; verify against a physical swatch book before specifying a spot colour.
- **Office fonts:** Word/PowerPoint cannot drive Fraunces' optical-size axis; templates name the static "Fraunces Light" instance.

## Deploying the website

`16_WEBSITE_IMPLEMENTATION/` is a drop-in replacement for the live Netlify site (same structure, same functionality, same copy; new wordmark, served favicons, token-aligned CSS, web-font subsets, new OG images). See its `CHANGES.md` for the file-by-file list and the six hover-loop videos that must be copied from the current deploy.

## For Sanzeed to supply or confirm

Registered business name, GSTIN/PAN, postal address and bank details for invoices and quotations · priority audience segments · which project images may be used outside the portfolio · social handles (recommended `@sanzeed` everywhere) · original high-resolution photography for print.

## Licences

Fonts: Fraunces, Inter and Inter Tight under the SIL Open Font License 1.1 (`04_TYPOGRAPHY/Font_Licensing.md`). All other artwork in this package was created for Sanzeed Mirza; project imagery remains subject to the rights note on sanzeed.com ("Employee work for Tagbin, Sociopixel, DWS and B2W; rights remain with those companies").
