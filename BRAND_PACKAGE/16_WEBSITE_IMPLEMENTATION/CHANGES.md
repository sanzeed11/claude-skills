# sanzeed.com — brand implementation, change log

Date: 5 November 2026. Base: the live site as backed up in `00_ORIGINAL_ASSETS_BACKUP/site_source/` (untouched). Everything in this folder is produced by `src/build_site.py` + `src/build_og.py` from that backup and the brand kit; nothing was hand-edited in the HTML, so the build is repeatable.

No copy was changed. No JavaScript was rewritten — one numeric constant was updated (see `index.html` below).

## What changed, file by file

### `index.html` (1,294,445 → 1,030,568 bytes, −20 %)

| Area | Before | After |
|---|---|---|
| Wordmark (loader + header) | Hand-traced inline SVG, `viewBox 0 0 3729 561`, one 36 KB path | Constructed primary wordmark from `02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg`, `viewBox 0 0 3590 500`, one 1.7 KB unioned path. Same structure and class names: `path.wm-letters`, two `circle.wm-dot` (816,412 / 3242,250, r 45), `circle.beam-dot` (cy 250) and `clipPath#ldClip` (rect 3590×500) in the loader, so the dot-pulse (`dotPulse`), idle (`dotIdle`), beam travel and the GSAP "landing dot" keep working unchanged. Fills still come from CSS (`var(--fg)` / `var(--accent)`), so both themes are correct automatically. |
| Loader JS | `const W = 3729;` (clip width + beam-dot end position) | `const W = 3590;` — the only JS edit, needed for the new artwork bounds. |
| Header logo size | `.brand svg{height:14px}` → 93 px wide (below the 120 px minimum) | `.brand svg{height:17px}` → 122 px wide, meeting the wordmark minimum size. The unused `.foot .wm`, `.f-brand .wm`, `.c-foot .wm` rules were bumped to 17 px for consistency. |
| Favicons | 64 px PNG + SVG + 180 px apple-touch-icon as data URIs (≈ 18 KB in the head) | `favicon.ico`, `favicon.svg`, `apple-touch-icon.png`, `safari-pinned-tab.svg` (mask-icon), `site.webmanifest` (192 / 512 / maskable 512 PNGs) served as files from the site root, per `02_LOGO_SYSTEM/Favicon/favicon-head-snippet.html`. |
| theme-color | `#f5f0e7` light / `#000000` dark | `#F5F0E7` / `#0D0D0F` (Night), matching the manifest and the kit snippet. |
| Fonts | Four base64 `@font-face` blocks (Inter Tight 400–800, Inter 400–600, Fraunces 300, Fraunces 300 italic; ≈ 190 KB inline) | `assets/fonts/*.woff2` variable fonts from `04_TYPOGRAPHY/Font_Files` with `font-weight:100 900`, `font-display:swap`, plus `<link rel="preload">` for Fraunces, Inter Tight and Inter. Family names are unchanged so every existing CSS rule resolves. |
| Fraunces optical size | Static instance (opsz 144) | Variable font with explicit axes so headlines look like the rest of the kit: `h1,h2,.f-big,.numbers .v` → `"opsz" 144,"SOFT" 30,"WONK" 0`; `h3,h4` → opsz 72; `.quote p` → opsz 72, SOFT 50; `.sv-item .n` → opsz 36. |
| Colour tokens | Site variables only | Same variable names, values set from `03_COLOUR_SYSTEM/colour-variables.css` (identical families; the only value differences were rgba notation). Added aliases with the token names (`--bg-2`, `--card-2`, `--fg-2`, `--fg-3`, `--line-2`, `--accent-2`), the functional set (`--success`, `--warning`, `--error`, `--info`, per theme), the `--sz-*` palette and gradient tokens. `.book-err` now uses `var(--error)` instead of `#c0392b`. |
| Signature | `img/signature-dark.png` / `img/signature-light.png` (raster, 1694×698) in the footer and the "Your line is in the book" state | `img/sanzeed-signature--ink.svg` (light theme) / `img/sanzeed-signature--white.svg` (dark theme) from `02_LOGO_SYSTEM/Signature`; `.sig{aspect-ratio:1215/498}`. The write-on animation (`sigWrite`, `sigPen`) is untouched. |
| Footer | Headline → columns | Headline → **horizontal-descriptor lockup** (inline SVG, `.f-lockup`, 320 px max, dots idle-pulse like the header) → columns. |
| Headline accents | `.muted` only | Added token-matched `.lit` (`var(--accent)`) and `.dim` (`var(--fg3)`) scoped to headings, so new copy can use the brand classes. Scoped on purpose: `.hero.lit` is an existing JS state class. |
| Open Graph | `og.jpg` (old wordmark, three thumbnails) | New `og.jpg` 1200×630: dark lamp background, master line with "into." lit, descriptor eyebrow, primary wordmark. Meta tags unchanged (same URL, 1200×630). |

### `work/prime-minister-museum.html`, `work/ram-katha-show.html`, `work/buddha-park.html` (≈ 322 KB → 93 KB each, −71 %)

Same favicon, font, token, wordmark (header), signature and footer-lockup changes as above (paths relative to `../`). Inter Tight is not preloaded on these pages because no text on them is set in it. `og:image` / `twitter:image` now point to `img/og/<slug>-1200x630.jpg` with `og:image:width/height/alt`.

### New files

| File | Spec |
|---|---|
| `og.jpg` | 1200×630 JPG q90, 65 KB — home share card |
| `img/og/prime-minister-museum-1200x630.jpg` | 1200×630 JPG q90, 144 KB — hero image, veil, title · place · idea line, wordmark corner |
| `img/og/ram-katha-show-1200x630.jpg` | 1200×630 JPG q90, 191 KB — uses `img/case/ram-katha-show-07.webp` (same frame as the hero at 1600×900) |
| `img/og/buddha-park-1200x630.jpg` | 1200×630 JPG q90, 206 KB |
| `img/sanzeed-signature--ink.svg`, `img/sanzeed-signature--white.svg` | vector signature, 56 KB each |
| `assets/fonts/*.woff2` + OFL licences | Fraunces 147 KB, Fraunces Italic 178 KB, Inter 109 KB, Inter Tight 60 KB |
| `favicon.ico` (16/32/48), `favicon.svg`, `apple-touch-icon.png` (180), `android-chrome-192x192.png`, `android-chrome-512x512.png`, `maskable-icon-512x512.png`, `safari-pinned-tab.svg`, `site.webmanifest` | from `02_LOGO_SYSTEM/Favicon` |
| `sitemap.xml` | `lastmod` → 2026-11-05 |

### Unchanged

`robots.txt`, `sanzeed-mirza.vcf`, all 93 `img/*.webp` (960×540 gallery images, portrait, two hero posters) and the 24 `img/case/*.webp`, the JSON-LD, the GoatCounter tag, the Netlify form attributes, the three.js hero module (still inline), GSAP/Lenis, galleries, pager, lightbox, enquiry drawer.

## Verification (headless Chromium via Playwright, `src/verify.js`)

Run on the built folder served with `python3 -m http.server` at 1440×900 and 390×844, dark and light, for `/`, `/work/prime-minister-museum.html`, `/work/ram-katha-show.html`, `/work/buddha-park.html`; the untouched backup was served the same way for the "before" screenshots. Results are in `screenshots/verify-report.json`.

- Console / page errors: none from the site. The only console error on every page (before and after) is `net::ERR_NAME_NOT_RESOLVED` for the external GoatCounter script `gc.zgo.at/count.js`, which this sandbox cannot reach.
- Failed requests to local files: none. Favicons, manifest icons, fonts, OG images, sitemap, robots, vCard and signature SVGs all return 200 with the right content type.
- Fonts: `document.fonts` reports Fraunces (normal + italic), Inter and Inter Tight loaded; `h1` computes to Fraunces 300.
- Wordmark: `.brand svg` renders at 122×17 px (viewBox 0 0 3590 500, path length 17,114 units, 2 gold dots); the loader `#ldClip` is present; the footer lockup renders with its 28 descriptor glyph paths.
- Theme toggle: clicking `.theme` sets `html[data-theme=light]`, body background becomes Plaster `rgb(245,240,231)`; on the home page the switch runs through the View Transitions cross-fade, as before.
- Galleries: "Projection Mapping & Shows" filter → `aria-pressed`, count reads "15 projects"; search "Ayodhya" → 2 cards; pager intact.
- Loader: `screenshots/after-index-desktop-loader-frame.jpg` shows the clip-path wipe and the travelling beam dot on the new artwork.

## Lighthouse-style note (manual, not a Lighthouse run)

| Metric | Before | After |
|---|---|---|
| HTML, home | 1,294 KB raw / 451 KB gzip (fonts, icons and a 36 KB traced logo path inlined) | 1,031 KB raw / 273 KB gzip, −40 % on the wire (≈ 700 KB of the raw size is the inline three.js hero module) |
| HTML, case page | 322 KB raw / 188 KB gzip | 93 KB raw / 24 KB gzip, −87 % on the wire |
| Fonts | 190 KB, inline, blocks the HTML parse and can never be cached separately | 316 KB preloaded (Fraunces + Inter + Inter Tight) + 178 KB Fraunces Italic on demand; cached across all four pages; `font-display:swap` |
| Favicons | data URIs in every page | 8 small files, cached once |
| Requests on first load (home, dark) | 1 HTML + 1 poster + lazy images | 1 HTML + 3–4 fonts + 2 icons + 1 poster + lazy images |
| Images | all WebP with width/height | unchanged (WebP, width/height, `loading="lazy"`, `decoding="async"`) |
| Layout shift | none observed | none observed; the header logo keeps `height`+`width:auto` |

Net: ~25 % less HTML to parse per visit, repeat visits fetch ≈ 93 KB per case page instead of 322 KB, and the fonts are a one-time download. The next performance step, outside this brief, is moving the inline three.js module (`<script type="module">`, ≈ 700 KB) into `assets/js/` so it caches independently.

## Known limitation

The home page references six hover loops `img/loop-*.mp4` (`<video preload="none">`). They were not part of the backup and could not be recreated here, so they are not in this folder. No request is made for them on page load; on hover/scroll the existing JS swallows the play error (`play().catch`). Copy the six MP4s from the current deploy into `img/` before publishing to keep the hover loops.

## Deploy to Netlify

The folder is a complete static site; the root is this folder.

- Drag-and-drop: open https://app.netlify.com/drop (or the site's *Deploys* tab) and drop the whole `16_WEBSITE_IMPLEMENTATION` folder, minus `src/`, `screenshots/`, `CHANGES.md` and `README.md` if you prefer a clean publish (they are harmless if included).
- Connected repository: commit this folder, set *Base directory* to `BRAND_PACKAGE/16_WEBSITE_IMPLEMENTATION`, *Publish directory* to the same, no build command.
- After deploy, check `https://sanzeed.com/favicon.ico`, `/site.webmanifest`, `/og.jpg` and `/img/og/prime-minister-museum-1200x630.jpg` return 200, then re-scrape the home and case URLs in the LinkedIn Post Inspector / Facebook Sharing Debugger so the new share images replace the cached ones.
- The enquiry form keeps its Netlify attributes; no form settings need to change.
