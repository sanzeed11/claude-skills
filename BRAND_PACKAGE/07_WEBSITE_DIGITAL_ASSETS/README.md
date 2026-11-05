# 07_WEBSITE_DIGITAL_ASSETS — website design system and digital brand assets

Everything a developer or a platform needs to put the Sanzeed identity on screen: the component library the site is built from, every share image, the favicon and app-icon sets, the email pieces, and the website graphics (hero orbit, card frame, method route, 404, loader, cursor, social-proof strip).

Every export has an editable source beside it (`src/` or the `.html`/`.svg` it was rendered from) and a build script that re-makes it with the brand-kit helpers in `15_SOURCE_FILES/Project_Files/brand-kit/` (`render.js`, `capture_frames.js`, `export_svg.py`). Nothing here is hand-retouched: edit the source, re-run the script.

| Folder | What is in it | Rebuild with |
|---|---|---|
| `UI_Components/` | `ui-kit.html` (26 components, every state), `components.css`, `tokens-reference.html`, responsive specimen, full-page renders at 1440 / 1280 / 834 / 390 and the light theme, responsive sheet | `bash render-kit.sh` · `bash render-responsive.sh` |
| `Open_Graph/` | og-default, og-home, og-work (template + Prime Minister Museum, Ram Katha Show, Buddha Park), og-about, og-contact — 1200×630 and 1200×1200, PNG + JPG q90 | `python3 build_og.py` |
| `Social_Sharing/` | generic share images 1920×1080, 1080×1080, 1080×1920 (PNG + JPG) and the link-preview mock | `bash build_share.sh` |
| `Favicon/` | the production favicon set copied from `02_LOGO_SYSTEM/Favicon` (ICO, SVG, PNG 16–1024, apple-touch, android-chrome, maskable, manifest, head snippet) | regenerate in the logo system (`export_logo.py`) |
| `App_Icons/` | iOS, Android (+ maskable), Windows tiles + `browserconfig.xml`, macOS Safari pinned tab, PWA icons + manifest, mapping README | `python3 build_app_icons.py` |
| `Email/` | email header 1200×400 dark/light, newsletter masthead 1200×300 dark/light, HTML + plain-text signature, 320×100 @2× logo PNG, rendered preview | `bash build_email.sh` |
| `Website_Graphics/` | hero orbit-on-lamp backgrounds (SVG/PNG/WebP, dark/light), “Now showing” card frame, method route graphic, 404 doorway illustration, loading animation (CSS + SVG + MP4/GIF), cursor dot, social-proof strip | `export_svg.py` per SVG; `render.js`; `capture_frames.js` (commands in the folder README) |

## Conventions

- **Brand CSS first.** Every HTML source links `../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css` (tokens, type, buttons, cards, lamp, grain). `UI_Components/components.css` adds the site components; `Open_Graph/src/og.css`, `Social_Sharing/src/share.css` and `Email/src/email-headers.css` add only layout for their formats.
- **Logos** are the production SVGs from `02_LOGO_SYSTEM/SVG`, inlined so they follow the theme: letters `currentColor` (Gallery White on dark, Soot on light), the two points `--accent` (Lamp Gold / Old Gold). Never below 120 px wide; clear space = half the cap height.
- **Images** are the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP/images/img/` and always carry a wall label (Title · Place). No stock, no AI imagery.
- **Copy** is confirmed copy from `01_BRAND_STRATEGY` and sanzeed.com. The only placeholders are bracketed labels (`[Project title]`, `[Month Year]`).
- **Naming:** `sanzeed-<deliverable>--<variant>-<size>.<ext>`.
- **Colour:** one gold accent per composition; functional colours (Moss, Ochre, Signal Red, Slate) mark states only.
- **Chromium limit:** full-page captures cannot exceed 16 384 px, so the kit renders in parts and is stitched (see `UI_Components/render-kit.sh`).

## Requirements

Node 22 with Playwright (Chromium), Python 3 with Pillow and cairosvg, Inkscape, ffmpeg, cwebp — all present in the production container; fonts in `04_TYPOGRAPHY/Font_Files` installed system-wide so Fraunces renders as a light serif everywhere.
