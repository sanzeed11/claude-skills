# 16_WEBSITE_IMPLEMENTATION — sanzeed.com with the refined identity

A deployable static site: the live site (backed up untouched in `00_ORIGINAL_ASSETS_BACKUP/site_source/`) with the new wordmark, favicon set, token-aligned colours, served web fonts, vector signature, footer lockup and new share images. Nothing else changed — copy, layout, JavaScript, forms and analytics are the originals. See `CHANGES.md` for the file-by-file diff, the verification results and the deploy steps.

Folder size ≈ 32 MB: 10.1 MB deployable site (194 files incl. 117 WebP images), 41 KB sources, the rest verification screenshots.

## Files

### Site (publish this)

| File | Spec | Edit via |
|---|---|---|
| `index.html` | 1,031 KB; inline CSS + JS (GSAP, Lenis, three.js hero module), new inline wordmark SVG (viewBox 0 0 3590 500) in loader + header, inline horizontal-descriptor lockup in the footer | `src/build_site.py` (re-run it; it rebuilds from the backup) |
| `work/prime-minister-museum.html` · `work/ram-katha-show.html` · `work/buddha-park.html` | ≈ 93 KB each, same treatment, paths relative to `../` | `src/build_site.py` |
| `og.jpg` | 1200×630 JPG q90, 65 KB — home share image (dark lamp, master line, descriptor, wordmark) | `src/og/og-home.html` + `src/og/og.css`, then `python3 src/build_og.py` |
| `img/og/<slug>-1200x630.jpg` ×3 | 1200×630 JPG q90 — case-study share images (hero image, veil, title · place · idea line, wordmark corner) | `src/og/og-work--template.html` + the `WORK` table in `src/build_og.py` |
| `img/*.webp` (93) | 960×540 gallery images, `portrait.webp` 1100×1574, `poster-dark.webp` / `poster-light.webp` 1600×900 | copied from `00_ORIGINAL_ASSETS_BACKUP/images/img/` |
| `img/case/*.webp` (24) | 1600×900 case-study galleries | copied from the backup |
| `img/sanzeed-signature--white.svg` · `img/sanzeed-signature--ink.svg` | vector signature, 1215×498 viewBox, 56 KB each (dark theme / light theme) | `02_LOGO_SYSTEM/Signature/` |
| `assets/fonts/Fraunces-variable.woff2` (147 KB) · `Fraunces-Italic-variable.woff2` (178 KB) · `Inter-variable.woff2` (109 KB) · `InterTight-variable.woff2` (60 KB) · `OFL-*.txt` | variable woff2, SIL OFL 1.1 | `04_TYPOGRAPHY/Font_Files/` |
| `favicon.ico` (16/32/48, 6.5 KB) · `favicon.svg` · `apple-touch-icon.png` (180) · `android-chrome-192x192.png` · `android-chrome-512x512.png` · `maskable-icon-512x512.png` · `safari-pinned-tab.svg` · `site.webmanifest` | favicon + PWA set | `02_LOGO_SYSTEM/Favicon/` |
| `robots.txt` · `sitemap.xml` · `sanzeed-mirza.vcf` | as live (sitemap `lastmod` 2026-11-05) | `src/build_site.py` (sitemap) |

### Sources and tooling (`src/`)

| File | What it does |
|---|---|
| `src/build_site.py` | Reads the backup HTML, applies every change with targeted replacements (favicons, fonts, wordmark, tokens, signature, lockup, OG meta, `.lit/.dim`, Fraunces axes) and writes the four pages + sitemap. Reads the artwork live from `02_LOGO_SYSTEM/SVG/` and the tokens from `03_COLOUR_SYSTEM/colour-variables.css`. `python3 src/build_site.py` |
| `src/build_og.py` | Fills the OG templates, renders them with `15_SOURCE_FILES/Project_Files/brand-kit/render.js` (Playwright) and writes the JPGs. `python3 src/build_og.py` |
| `src/og/og-home.html` · `src/og/og-work--template.html` · `src/og/og.css` | Editable OG card sources (brand.css linked relatively; `{{WM}}`, `{{TITLE}}`… filled by the builder). `src/og/build/` holds the last filled copies. |
| `src/verify.js` | Playwright check: console errors, failed requests, `document.fonts`, wordmark geometry, theme toggle, gallery filter/search, favicon/manifest/OG files → `screenshots/` + `screenshots/verify-report.json`. `node src/verify.js [--before <dir>]` |

### Screenshots (`screenshots/`)

`after-<page>-<desktop|mobile>-<dark|light>.jpg` (viewport), `…-full.jpg` (full page), `…-header-2x.png` / `…-header-2x-light.png` (header at 2×), `…-footer-2x-light.png`, `after-index-desktop-dark-gallery-filter-projection.jpg`, `after-index-desktop-loader-frame.jpg`, and the same `before-…` set for the home and Prime Minister Museum pages from the untouched backup. `verify-report.json` is the machine-readable result.

## How to edit

- **Copy or layout** — do not hand-edit the generated pages. If the live site's copy or layout changes, update the source pages in `00_ORIGINAL_ASSETS_BACKUP/site_source/` and re-run `src/build_site.py`. For brand-level changes (another logo variant, a token tweak, the lockup size), change the constants at the top of `src/build_site.py` or its `CSS_ADDENDUM` block and rebuild.
- **Logo** — the wordmark path is read from `02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg` (unioned production artwork; the editable master is `02_LOGO_SYSTEM/Source_Files/`). Rebuild after any logo update; the loader/beam JS only needs `const W` to equal the viewBox width (3590).
- **Share images** — edit the HTML/CSS in `src/og/`, run `python3 src/build_og.py`. Work cards take their title, place and idea line from the `WORK` table in the builder (all copy is from the case-study pages).
- **Fonts** — replace the woff2 files in `assets/fonts/` with the ones from `04_TYPOGRAPHY/Font_Files/`; the `@font-face` names must stay `Fraunces`, `Inter`, `Inter Tight`.
- **Verify** — `node src/verify.js --before /path/to/served/backup` (needs node + playwright; serve the backup with its `img/` folder next to it for before-shots).

## Deploy

Netlify drag-and-drop of this folder, or connect the repository with this folder as base + publish directory and no build command. Details and the post-deploy checklist are in `CHANGES.md`.

## Not included

`img/loop-*.mp4` (six hover loops referenced by the home page with `preload="none"`) were not in the backup and are not recreated here — copy them from the current deploy into `img/` before publishing.
