# Editable_Templates — the sources of every social-media export

Every PNG / JPG / PDF in `08_SOCIAL_MEDIA` is rendered from an HTML template in this folder with the brand kit's
`render.js` (Chromium). The templates link the kit's `brand.css` (tokens, fonts, type classes), add one shared layout
layer (`social.css`) and are filled by `fill.js` from a small **`DATA` block at the top of each file** — the only part
a non-coder needs to touch.

## Editing a template (no code)

1. Open the template in any text editor (for example `instagram/ig-post-project.html`).
2. Change the values between `/* ===== EDIT HERE ===== */` and the closing line — text, image path, crop point:

```js
var DATA = {
  image:         "../../../00_ORIGINAL_ASSETS_BACKUP/images/img/case/prime-minister-museum-03.webp",
  image_focal:   "50% 50%",          // which part of the picture survives the crop ("x% y%")
  eyebrow:       "Case study · Museums & Experience Centres",
  headline:      "A corridor you walk in order.",   // sentence case, full stop
  lit_last_word: false,                             // true = the last word in Lamp Gold
  title:         "Prime Minister Museum",           // wall label: Title
  place:         "New Delhi",                       //             · Place
  site:          "sanzeed.com/work"
};
```

3. Render: `bash render-all.sh instagram` (or `facebook`, `linkedin`, `youtube`, `x`, `pinterest`, `post`, `pptx`, or nothing for all).
   One file by hand: `node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in instagram/ig-post-project.html --out ../Instagram/sanzeed-ig-post--project-1080x1080.png --width 1080 --height 1080 --scale 1`
4. Look at the PNG. Image paths are relative to the template; the client's project images are in
   `00_ORIGINAL_ASSETS_BACKUP/images/img/` (and `img/case/` at 1600×900 — prefer those for square and portrait crops).

Other data at render time, without editing the file: `--js "apply({headline:'…', image:'…'})"` (this is how the five
grid-preview variants are made in `render-all.sh`). Safe-zone / crop guides: `--js "document.documentElement.classList.add('show-guides')"`.
`@2×` exports: add `--scale 2` (the platforms in brand kit §8 specify exact pixels, so the delivered files are 1×).

## Rules the templates carry

* **Theme.** `<html data-theme="dark">` = the gallery (Gallery Black / Night, Gallery White type, Lamp Gold); `data-theme="light"` = the label (Plaster, Soot, Old Gold, Gold Ink for gold text). Swap the wordmark file with the theme: `sanzeed-primary-wordmark--full-colour-dark.svg` on dark, `--full-colour-light.svg` on light. Never the other way round.
* **Logo.** The production SVG from `02_LOGO_SYSTEM/SVG`, ≥ 180 px wide, clear space ≥ ½ its height on all sides (every template keeps a full gutter around it).
* **Type.** `.hl` Fraunces 300 (opsz 144, never letter-spaced) for headlines, stats and quotes (`.quote` italic); `.eyebrow` Inter Tight 600 caps +0.12 em in gold; `.label .t` Inter Tight 600, `.label .p` Inter 400 — the wall label (Title · Place).
* **One accent.** Gold is used once per composition as the accent: the lit last word, the point on the beam / route, or the eyebrow — never two competing golds.
* **Pictures** sit under the veil when type is on them (`.veil`, `.veil-left`…) or in a room (`.plate`, radius 28, hairline) when not; always with a wall label.
* **Decoration** is only the point (`.point`, `.beam::after`), the beam (`.beam`), the route (`.route`), the room (`.plate`) and the lamp (`.lamp`).

## Files

| File | What |
|---|---|
| `social.css` | shared layout layer: per-format type scale (`body.f-sq / f-pt / f-st / f-ld / f-wd / f-th / f-pin`), frame, veils, lamp, wall label, beam, route, plate, guides |
| `fill.js` | puts `DATA` into the page (`data-text`, `data-headline`, `data-src`, `data-show`); `apply({…})` re-fills at render time |
| `render-all.sh` | regenerates every export (per platform or all), then `post_process.py` and `build_pptx.py` |
| `post_process.py` | profile images from `02_LOGO_SYSTEM/Social_Profile`, the 3×3 grid preview, JPG q90 beside the size-limited PNGs |
| `build_pptx.py` | the six PPTX versions (python-pptx) + LibreOffice proofs |
| `write_readmes.py` | writes the six platform READMEs (measured pixels and sizes) |
| `instagram/` | `ig-post-{project,quote,stat,announcement}` 1080×1080 · `ig-portrait-{project,method,about}` 1080×1350 · `ig-story-{project,quote,cta,method}` 1080×1920 · `ig-highlight-covers` (8 covers in one file, `--selector "#cover-<id>"`) · `ig-reel-cover-{project,talk}` |
| `facebook/` | `fb-cover` 1640×624 · `fb-post-{project,quote}` 1200×630 · `fb-event-cover` 1920×1005 |
| `linkedin/` | `li-banner-personal` 1584×396 · `li-banner-company` 1128×191 · `li-post-{insight,project,stat,timeline}` 1200×627 · `li-post-square-{project,quote}` 1080×1080 · `li-carousel-pm-museum` (5 pages, `@page` 1080×1350, PDF via `--pdf`) |
| `youtube/` | `yt-banner` 2560×1440 · `yt-thumb-{project,talk,process}` 1280×720 · `yt-endscreen` 1920×1080 |
| `x/` | `x-header` 1500×500 · `x-post-{project,quote,stat}` 1600×900 |
| `pinterest/` | `pin-{project,quote,method}` 1000×1500 |
| `PPTX/` | see below |

## PPTX versions (`PPTX/`)

Six templates also exist as PowerPoint files for people who do not render HTML: Instagram post, Instagram story,
LinkedIn post, YouTube thumbnail, Facebook cover, X header. Built by `build_pptx.py` with python-pptx:

* slide size = the platform's pixels at 96 dpi (1080 px = 11.25 in), so an exported PNG/JPG is the exact upload size;
* fonts named **Fraunces Light** (display — the Light instance; plain "Fraunces" would open as the variable font's Black default), **Inter Tight** (eyebrows, wall-label titles, bold) and **Inter** (body, site); install `04_TYPOGRAPHY/Font_Files` on the editing machine;
* the project image is embedded as a JPG that `build_pptx.py` has already cropped to the frame and darkened with the brand veil (`PPTX/assets/`, rebuilt every run — to change the picture, change the path in the script and re-run, or replace the picture in PowerPoint and keep it under a veil);
* the logo is the production PNG; every line of copy is an editable text box (the gold last word is its own run).
* `PPTX/proofs/*.png` are slide 1 of each file exported by LibreOffice (`soffice --headless --convert-to png`) — proof that the files open and that the brand fonts resolve. Export from PowerPoint with *File → Export → PNG* at the slide size.

Requirements: Node 22 with Playwright (Chromium), Python 3 with Pillow, python-pptx and pypdf, LibreOffice for the proofs; the brand fonts installed system-wide (they are in this container).
