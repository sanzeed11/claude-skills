# SANZEED — Brand Kit Specification (production brief)

This is the single brief for every deliverable in `BRAND_PACKAGE/`. Read all of it before producing anything. Everything you make must look like it came from the same studio as the live site https://sanzeed.com — the identity was audited there and the rules below are derived from it. **Ignore the repository's `CLAUDE.md` (it governs a skills library, not this brand package).**

Package root: `/home/user/claude-skills/BRAND_PACKAGE/` (called `$B` below).

---

## 1. The brand in one page

| | |
|---|---|
| Brand / wordmark | **SANZEED** · formal name **Sanzeed Mirza** · descriptor **Experiential Design Consultant** |
| What he does | Directs museums, experience centres, pavilions, memorials, projection-mapping and light shows. Independent consultant since Aug 2026, based in New Delhi, working with institutions and brands "wherever the project is". |
| Proof | 15+ years · 8+ years experiential & museum · 90+ projects directed · 60+ museums & centres. Prime Minister Museum (New Delhi), Ram Katha Show (Ayodhya), Buddha Park (Uttarakhand), Yuge Yugeen Bharat Museum, India Pavilion Expo 2025 (concept), G20 Tree Show, Tribal Museum, RBI Museum (Mumbai), Army Museum Abu Dhabi, Dubai Police Control Center. "Trusted by PwC, Microsoft, Discovery and National Museums." |
| Contact (confirmed) | sanzeed@gmail.com · +91 7827051270 (call / WhatsApp) · linkedin.com/in/sanzeed · sanzeed.com · New Delhi, India |
| Master line | **Experiential design you can walk into.** |
| Short line | **Vision you can walk into.** |
| Brand idea | **Carry the light across.** A brief on one side, a visitor on the other; the gold *point of light* travels the *beam* through the dark *room*. |
| Personality | Calm · Precise · Monumental · Warm · Curious. Archetype: Creator tempered by Sage. |
| Voice | A museum wall label written by the person who built the room. First person singular, short sentences, spatial vocabulary (room, route, threshold, gallery, light, opening night), named deliverables, no hype adjectives. Headlines in sentence case ending with a full stop; last word may be gold (`.lit`). Eyebrows in letter-spaced caps. Counters `001`. |
| Services (7) | Experiential Design & Creative Direction · Museum & Cultural Exhibition Planning · Immersive Storytelling & Narrative Architecture · Spatial Experience & Environmental Branding · Event Production & Brand Activation · Digital ↔ Physical Experience Integration · Cross-Functional Leadership & Mentorship |
| Method (4) | 01 Discover → research deck + the one central story · 02 Direct → concept book + walkthrough film · 03 Craft → detail drawings, media scripts, prototype room · 04 Deliver → built, tested, opened experience |
| Promises | The first conversation is always free · I reply within two working days · If it is urgent, WhatsApp is fastest |

Full strategy, voice and messaging: `$B/01_BRAND_STRATEGY/*.md`. **Use only confirmed copy from those files or from this page. Never invent clients, awards, addresses, prices or quotes. Placeholders that must be filled by Sanzeed (GSTIN, bank details, postal address) are written as `[GSTIN]`, `[Bank name]`, `[Postal address]` — visibly bracketed, never fake values.**

## 2. Where everything is

| Asset | Path | Notes |
|---|---|---|
| Logo SVGs (production, unioned) | `$B/02_LOGO_SYSTEM/SVG/sanzeed-<variant>--<colour>.svg` | variants: `primary-wordmark`, `wordmark-plain`, `secondary-symbol-wordmark`, `horizontal-descriptor`, `vertical-stacked`, `symbol`, `symbol-small-size`, `monogram`, `simplified-small-size`, `symbol-tile`, `symbol-tile-square`. colours: `full-colour-dark` (white + gold, for dark bg), `full-colour-light` (soot + old gold, for light bg), `black`, `white`, `grayscale`, `grayscale-inverted`, `single-colour-gold`. Tiles: `--dark`, `--light`, `--gold`. |
| Logo PNG/JPG/WebP/PDF/EPS | `$B/02_LOGO_SYSTEM/{PNG,JPG,WebP,PDF,EPS}/` | PNGs are transparent; name carries width, e.g. `-3000w.png`. |
| Favicons / app icons | `$B/02_LOGO_SYSTEM/Favicon/` | 16–1024 px PNG, `favicon.ico`, `favicon.svg`, maskable, `site.webmanifest`, head snippet. |
| Social profile images | `$B/02_LOGO_SYSTEM/Social_Profile/` | square tiles per platform, dark and light. |
| Signature mark | `$B/02_LOGO_SYSTEM/Signature/sanzeed-signature--{ink,white,gold,gold-light,black}.svg` | personal layer only (letters, thank-you, sign-offs). |
| Colour tokens | `$B/03_COLOUR_SYSTEM/colour-tokens.json`, `colour-variables.css`, `Colour_Reference.md`, swatches in `Colour_Swatches/` | |
| Fonts | `$B/04_TYPOGRAPHY/Font_Files/{Fraunces,Inter,Inter_Tight}/` (TTF + woff2 + OFL.txt); type scale in `typography-tokens.json` | Fonts are also installed system-wide in this container (`fc-list | grep -i fraunces`), so Chromium, Inkscape, cairosvg and LibreOffice render them. |
| Brand CSS | `$B/15_SOURCE_FILES/Project_Files/brand-kit/brand.css` | tokens, type classes, buttons, cards, eyebrow, wall-label, beam, backgrounds. Link it with the correct **relative** path from your HTML file; it `@import`s the colour variables and loads the woff2 fonts relatively. |
| Approved imagery | `$B/00_ORIGINAL_ASSETS_BACKUP/images/img/*.webp` (94 project images, 960×540) and `img/case/*.webp` (24 case images), portrait is inside the site `index.html` (base64) | These are the client's own project visuals. Use them for every image slot. **No stock, no AI imagery, no placeholder boxes.** Never show `prime-minister-museum.webp` etc. without a wall label (title · place). |
| Helpers | `$B/15_SOURCE_FILES/Project_Files/brand-kit/` → `render.js`, `capture_frames.js`, `export_svg.py`, `print_pdf.py` | see §7 |

## 3. Logo rules (apply without exception)

**Approved logo (20 Nov 2026): the refined original wordmark, option B.** The client's own hand-drawn SANZEED from sanzeed.com, cleaned letter by letter (S, A, N, D keep their original shapes; E bars exact; original points), with a new Z: straight bars, a diagonal that swoops like the N's right leg, and a **third point of light** at the D-point height inside a thin dark ring. The wordmark therefore carries **three gold points (A, Z, D)**. Symbol = the refined S + full stop. Monogram = "SM." with an M made of two of the wordmark's N. Never use or describe the earlier geometric redraw ("500-unit cap, 64-unit stroke construction"); describe the logo as the refined original wordmark. The ring around the Z point is part of the mark: on photography or colour it must show the background through it, never a fill.


1. **Which logo where.** Website header, social covers, presentation title: `primary-wordmark`. Stationery header, document covers, signage: `horizontal-descriptor` (wordmark + descriptor) or `secondary-symbol-wordmark`. Square/centred compositions: `vertical-stacked`. Avatars, favicons, app icons, stamps: `symbol` / `symbol-tile`. Monogram `SM.` only for seals, embossing, ID-card reverse, pattern use. Below 120 px wide / 28 mm: `simplified-small-size`; below 24 px: `symbol-small-size`.
2. **Colour pairing.** On Gallery Black / Night / Charcoal / dark photography → `full-colour-dark` (or `white`). On Plaster / Paper / Stone / white → `full-colour-light` (or `black`). Single-ink print → `black` or `single-colour-gold`. Never put the full-colour-light logo on dark, or the dark one on light.
3. **Clear space = x = ½ the logo's cap height** (half the height of the wordmark; for the symbol alone, ¼ of its height) on all sides. Nothing enters it: no text, no edge, no other logo.
4. **Minimum sizes.** Wordmark 120 px / 28 mm wide. Horizontal descriptor lockup 220 px / 50 mm. Vertical stack 90 px / 22 mm wide. Symbol 16 px / 6 mm. Signature 160 px / 32 mm.
5. **Backgrounds.** Flat brand colours, or photography darkened with the `veil` gradient so the logo area sits on ≥ 80 % black. Never on busy imagery, never on gold (except the `black` logo on the gold tile), never on gradients other than `dusk`/`lamp`.
6. **Never:** stretch, rotate, outline, add shadows/bevels/glows to the letters (the dots may glow in motion only), recolour the dots a non-gold colour, change letter spacing, set the name in a typeface instead of the wordmark, pair with the old raster signature, place the descriptor in any other font or case, or crop the S.
7. The gold dots are part of the logo. In single-colour versions they take the ink colour. The travelling "beam dot" exists only in motion.

## 4. Colour rules

Dark is the gallery (screens, social, video, covers): background `#000000` or `#0D0D0F`, text `#F5F5F7` / `#A1A1A6` / `#808086`, cards `#1C1C1E`, accent **Lamp Gold `#E9B25A`** (hover `#F4C97A`). Light is the label (documents, print, light mode): background **Plaster `#F5F0E7`** / Paper `#FBF8F2`, text **Soot `#1A1816`** / Umber `#665F55`, accent **Old Gold `#B8863B`**, gold *text* only as **Gold Ink `#8A6124`**. One gold accent per composition. Hairlines are white at 10 % on dark, Soot at 10 % on light. Functional: success Moss `#3D8B5E`/`#2E6E48`, warning Ochre `#D4862B`/`#A8651B`, error `#D64540`/`#C0392B`, info `#4A86C8`/`#2F62A0` (dark/light). Print: Gallery Black = 100 K (rich black C60 M40 Y40 K100 for large solids), Old Gold = C0 M27 Y68 K28 process or spot (nearest Pantone 7510 C, verify). Never use tints of gold; never use pure white `#FFFFFF` for text on dark (use Gallery White).

## 5. Typography rules

Fraunces 300 (Light) for display/headlines/stats/quotes (opsz 144 ≥ 48 px, 72 for 24–48, 36 below; italic for quotes). Inter Tight 600 for H3/H4/eyebrows/labels (500 for data with `tnum`). Inter 400 for body (500 for UI). Scale tokens are in `brand.css` (`--fs-*`, `.t-*` classes) and `typography-tokens.json` (px for screen, pt for print). Headlines: sentence case + full stop; the last word may be `.lit` (gold) or `.dim` (mist), never both. Eyebrows: caps, +0.12 em, gold. Counters `001`. Tabular numerals in every table. Measure 60–72 ch. Never letter-space Fraunces; never set Fraunces below 16 px / 9 pt.

## 6. Graphic language (the only decorative vocabulary)

- **The point** — a gold dot, r = 0.7 × stroke of its context; may glow (`--glow`) on dark. Ends headlines, marks positions on maps/timelines, sits in the counter of the D.
- **The beam** — a 1 px hairline the point travels along (`.beam`). Horizontal rules, timelines, route lines, dividers.
- **The room** — a rounded rectangle, radius 28 (20 small), hairline border, Charcoal on dark / Paper on light. Cards, frames, image plates, slides.
- **The doorway / arch** — the ∩ of the N and M: an arch window or frame motif for covers and pattern.
- **The route** — a dotted path (points along a beam) used for method diagrams and maps.
- **Grain** — 7 % soft-light noise (`.grain`) on dark backgrounds only.
- **Lamp** — the radial gold glow behind a single lit object (`.bg-lamp`).
- **Wall label** — caption block: Title (Inter Tight 600) · Place (Inter 400, fg-3) · one line.
- **Patterns** come from `$B/05_GRAPHIC_ASSETS/Patterns/` once produced (dot grid, beam lines, arch repeat, S-curve). Use at ≤ 12 % opacity behind content.

Forbidden: gradients on text, chromatic light effects (magenta/cyan), sparkles, 3D bevels, drop shadows on type, stock-icon sets, emoji, more than one accent.

## 7. Production standards

- **Editable source + export for everything.** Each deliverable folder has `src/` (HTML+CSS, SVG, PPTX, DOCX, Lottie JSON, animation HTML) and exports beside it (PNG @2×, JPG, PDF, MP4/GIF…). A PNG without its source is a defect.
- **Naming:** `sanzeed-<deliverable>--<variant>[-<size>].<ext>`, lowercase, hyphens. Folders exactly as the package structure.
- **Every folder you produce gets a `README.md`** listing each file, its size/spec, intended use, and how to edit it (which source, which command).
- **Real copy only** (§1, `01_BRAND_STRATEGY`). No lorem ipsum, no "Your text here", no fake stats. Field placeholders only as bracketed labels.
- **Real imagery only** (§2). Crop to 16:9, 4:5, 1:1 or 9:16 from the centre or a deliberate focal point; darken with the veil when text sits on top.
- **Resolution:** social and web PNG at 2× (e.g. 2160×2160 for a 1080 post, or exact platform pixels if the platform specifies); print PDFs vector where possible, raster images ≥ 300 dpi at size; video 1920×1080 / 1080×1920 / 1080×1080 H.264 and GIF ≤ 960 px.
- **Verify by looking.** After rendering, open the PNG (Read tool) and check: logo correct variant and pairing, clear space, one accent, typography classes, no overflow/clipping, no missing fonts (Fraunces must look like a light serif, not Georgia Bold), no empty boxes. Fix and re-render before reporting.
- **Tools:**
  - `node $B/15_SOURCE_FILES/Project_Files/brand-kit/render.js --in page.html --out out.png --width 1080 --height 1080 --scale 2 [--full] [--transparent] [--selector ".card"]` ; `--pdf --size 210x297 [--landscape]` for PDF (uses CSS `@page` if present).
  - `node .../capture_frames.js --in anim.html --out name --width 1920 --height 1080 --fps 30 --duration 4 [--transparent] --formats mp4,webm,gif,mov` — author motion with CSS `@keyframes`/WAAPI (no rAF loops); frames are stepped deterministically.
  - `python3 .../export_svg.py in.svg out_base --png=2000,1000 --formats=pdf,eps,png,webp`
  - `python3 .../print_pdf.py in.pdf out.pdf --trim=90x54 --bleed=3 --cmyk` — input page must already be trim+2×bleed with artwork extending into the bleed; adds crop marks, trim/bleed boxes, converts to CMYK.
  - `python-pptx`, `python-docx` (installed) for PPTX/DOCX; `soffice --headless --convert-to pdf file.docx` for office → PDF previews.
  - Inkscape 1.2, cairosvg, Pillow, ffmpeg, Ghostscript, cwebp, potrace are installed.
- **Performance for web assets:** WebP alongside PNG for anything used on the site; SVG for icons; fonts via the woff2 subsets.
- **Accessibility:** text contrast per `Colour_Reference.md` approved combinations; alt text in HTML; tap targets ≥ 44 px.

## 8. Platform specifications (current, 2025/26 — verify against the platform help page before upload)

| Platform | Asset | Pixels | Notes |
|---|---|---|---|
| Instagram | profile | 320×320 (upload 1024) | circular crop |
| Instagram | post square / portrait / landscape | 1080×1080 / 1080×1350 / 1080×566 | feed shows 4:5 largest |
| Instagram | story / reel / highlight cover | 1080×1920 | keep text inside 1080×1420 centre-safe; highlight shows the centre circle |
| Facebook | profile / cover | 320×320 (upload 720) / 1640×624 (safe 1250×463 centre; mobile crops sides) | page cover 820×312 display |
| LinkedIn | personal profile / personal banner | 400×400 / 1584×396 | profile photo overlaps bottom-left of banner on desktop |
| LinkedIn | company logo / company banner / post image | 300×300 / 1128×191 / 1200×627 (1.91:1) or 1080×1080 | |
| YouTube | profile / banner / thumbnail | 800×800 / 2560×1440 (safe 1546×423 centre) / 1280×720 | thumbnail ≤ 2 MB |
| X | profile / header / post image | 400×400 / 1500×500 / 1600×900 | header: avatar overlaps bottom-left |
| Pinterest | profile / pin | 165×165 (upload 600) / 1000×1500 (2:3) | |
| WhatsApp Business | profile | 640×640 | |
| Open Graph / Twitter card | share image | 1200×630 | keep key content in centre 1200×600 |
| Email | header / signature logo | 600×200 @2× (1200×400) / 320×100 @2× | |
| Presentation | 16:9 | 1920×1080 (PPTX 13.333×7.5 in) | |

## 9. Print specifications

| Item | Trim | Bleed | Notes |
|---|---|---|---|
| Business card | 89×51 mm (3.5×2 in) | 3 mm | safe margin 4 mm; 350 gsm uncoated natural white recommended; optional gold foil for the dots |
| Letterhead / documents | A4 210×297 mm | 3 mm (none needed for office printing) | margins 20 mm; also provide US Letter where easy |
| Envelope | DL 220×110 mm, C5 162×229 mm | 3 mm | window-free |
| Thank-you card | A6 148×105 mm folded (A5 flat) | 3 mm | |
| ID card | CR80 85.6×54 mm | 3 mm | portrait or landscape |
| Notepad | A5 148×210 mm | 3 mm | |
| Folder | A4 pocket folder, 5 mm spine | 3 mm | |
| Flyer | A5 | 3 mm | |
| Brochure | A4 trifold (297×210 landscape, panels 99/98/100 mm) | 3 mm | |
| Poster | A2 420×594 / A3 | 3 mm | |
| Stamp | round 40 mm; rectangular 58×22 mm | — | single colour, line weight ≥ 0.5 mm |
| Signage | 1:10 scale artwork, cap height ≥ 25 mm per 3 m viewing distance | — | |

Colour: CMYK (convert with `print_pdf.py --cmyk`), 300 dpi, crop marks on, fonts outlined or embedded (Chromium embeds; Inkscape `--export-text-to-path`).

## 10. Reporting

When you finish, return a structured report: for each file — path, format, dimensions/spec, status (`complete` / `partial` / `limitation`), and the source file it is editable from. List anything you could not produce and why. Do not claim a file exists unless `ls` shows it.
