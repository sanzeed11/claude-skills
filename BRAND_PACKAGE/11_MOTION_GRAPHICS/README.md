# 11_MOTION_GRAPHICS — the motion identity

**Carry the light across.** A gold point of light travels a beam through the dark room; whatever it passes is revealed. Every piece in this folder is that one idea at a different length: the logo reveal, the intro and end card, the beam-wipe transition, the social animations, the lower thirds and the website loader.

Principle: **light, not bounce.** Ease-out `cubic-bezier(.22,.8,.2,1)`; durations 200 / 400 / 800 / 1100 ms; holds are calm; the beam travels left → right; glow is gold and belongs to the point; the logo is never spun, bounced or stretched. The rules are written out in [`Motion_Principles.md`](Motion_Principles.md).

## What is where

| Folder | Contents |
|---|---|
| `Logo_Animations/` | Logo reveal (4 s: dark 16:9 · light/Plaster 16:9 · 1:1 · 9:16), logo outro (3 s), symbol loop (3 s, seamless, alpha), presentation logo (4 s, alpha) |
| `Intros_Outros/` | Branded intro (6 s) and end card (6 s), each 1920×1080 and 1080×1920; the beam transition (1.5 s, alpha) and its preview over two project images |
| `Social_Animations/` | Stories ×3 (1080×1920, 6 s): project reveal with wall label · quote with light wipe · Now showing. Posts ×2 (1080×1080, 5 s): project · the method as a route. Stat counter (1080×1080, 5 s) |
| `Lower_Thirds/` | Name + descriptor · project title + place (wall label) · quote attribution — 5 s each at 1920×1080 with alpha (ProRes 4444 + WebM) and an MP4 preview over an approved image |
| `Website_Loader/` | The loader (point on beam, 2 s loop) as CSS, SVG + SMIL, Lottie JSON, GIF and MP4; the reveal-on-scroll CSS + JS; a demo page |
| `Exports/` | Key frames of every animation, contact sheets, Lottie render proofs, the easing-curve diagram |
| `Source_Files/` | Every animation as HTML + CSS `@keyframes` (`<name>/index.html`), the shared `motion.css`, the Lottie builder and validator, the render pipeline |
| `Motion_Principles.md` | Timing scale, easing curves, transitions, movement principles, logo animation rules, accessibility, delivery specs |

Every video has a `*--poster.jpg` (or `.png` with alpha) of its final hold frame, for thumbnails and reduced-motion fallbacks.

## How it is made (and how to edit it)

1. **Author** — each piece is a self-contained `Source_Files/<name>/index.html` that links the brand kit (`15_SOURCE_FILES/Project_Files/brand-kit/brand.css`) and the shared `Source_Files/motion.css` (timing tokens, the keyframe library, frame formats). Copy, image and timing sit in **EDIT HERE** blocks at the top of each file (the social animations keep their copy and image in a `DATA` object that `Source_Files/fill.js` writes into the markup, as the static social templates do). The logo is the approved refined original wordmark (20 Nov 2026): hooked S, swooping N, the Z with the N swoop, and **three gold points — A, Z, D** — the Z's point sitting inside a thin open ring. It is inlined as SVG with one unioned outline per letter so letters and points animate individually; fills follow the theme (`data-theme="dark"` or `"light"`). `python3 Source_Files/_shared/build_shared_logo.py` reads `02_LOGO_SYSTEM/Source_Files` (primary wordmark letters S, A, N, Z, E1, E2, D + three points; symbol = refined S + point), unions each letter with Inkscape path-union (no construction seams), writes `_shared/wordmark-source.svg`, `wordmark-letters-unioned.svg`, `symbol-source.svg` and `logo-geometry.json` (viewBox 3692.52 × 519.33, point centres, the Z-ring radius and the reveal windows derived from the easing curve), and rewrites the path data between the `<!-- @letters:… -->` / `<!-- @path:… -->` markers in every source. In the reveal the point travels the beam S → D at the height of the Z and D points; letters bloom as it passes; the A's point settles as it passes, the Z's point settles into its ring, and the travelling point becomes the D's point; a `#zring` mask keeps every glow out of the Z's ring so the background always shows through it. The outro collapses the wordmark to the symbol S. (its own 603.82 × 519.33 box, centred). Everything is CSS animation — no `requestAnimationFrame`, no timers — so frames are deterministic.
2. **Look** — `node Source_Files/preview_frames.js --in <name>/index.html --width W --height H --times 0.8,1.6,3.9 --out /tmp/pv` writes stills at those times plus a strip. Open a source in a browser to play it live.
3. **Render** — `Source_Files/render.sh <name>/index.html W H seconds ../<Deliverable> <out-base> mp4,webm,gif[,mov] [transparent] [gif-fps] [gif-long-edge]`. It calls the brand kit's `capture_frames.js` (every animation paused and stepped to each frame time at 30 fps) and encodes: MP4 H.264 CRF 20 · WebM VP9 CRF 30 (alpha when transparent) · MOV ProRes 4444 q9 (alpha when transparent) · GIF ≤ 960 px, 128 colours. It also keeps six key frames in `Exports/Key_Frames/` and the poster. Each source's header comment carries its exact render command.
4. **Colour tags** — `Source_Files/retag_colour.sh` stamps BT.709 metadata on every MP4 and WebM without re-encoding (bitstream filters); `render.sh` sets the same tags at encode time.
5. **Sheets** — `python3 Source_Files/build_contact_sheets.py` rebuilds the contact sheets from the key frames; `python3 Source_Files/build_readme_table.py` re-measures every file into the tables below.
6. **Lottie** — `python3 Source_Files/lottie/build_lottie.py` writes `sanzeed-logo-reveal.json` and `sanzeed-loader.json` by hand (shape layers: ellipses, rectangles, béziers; position / scale / opacity keyframes; the brand easing as handles `o {.22,.8} i {.2,1}`), plus a self-contained player for each. The reveal reads the letters from `_shared/wordmark-letters-unioned.svg` and the points / timings from `_shared/logo-geometry.json`: three points settle (A, Z, D) and a layer mask keeps the Z's ring open. `node Source_Files/lottie/validate_lottie.js` loads them in Chromium through lottie-web, screenshots six frames each and writes the proofs to `Exports/Lottie_Proofs/`. The loader JSON is copied to `Website_Loader/`.

Sizes and timings for the two formats of a piece come from one source: the layout adapts to the viewport (`@media (aspect-ratio: 1/1)`, `(max-aspect-ratio: 9/16)`), so `intro/index.html` renders both 1920×1080 and 1080×1920. The light logo reveal is `logo-reveal/index-light.html` (identical to `index.html` except `data-theme="light"`). The lower-third and transition `preview.html` files are the same markup over an approved image; edit `index.html` and mirror the change.

Requirements: Node 22 with Playwright (Chromium), ffmpeg 6, Python 3 with Pillow, Inkscape 1.2 (only for `build_shared_logo.py`, to rebuild the unioned letters from 02). Fonts load from `04_TYPOGRAPHY/Font_Files` through `brand.css`.

## Copy, imagery, pairing

All copy is confirmed brand copy (`01_BRAND_STRATEGY`): the master line, "Tell me about the room.", the headline bank, the method steps, the proof figures, the contact lines. Project images come from `06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images` (graded) and the case images in `00_ORIGINAL_ASSETS_BACKUP`, always with a wall label (Title · Place). Dark pieces use the `full-colour-dark` pairing on Gallery Black; the Plaster reveal uses `full-colour-light`; transparent pieces are built for dark backgrounds (switch `data-theme` to `light` for Plaster slides and re-render).

## Delivery notes

- **Alpha masters.** ProRes 4444 MOV (straight alpha, 10-bit 4:4:4:4) for Premiere / After Effects / Resolve / Final Cut; WebM VP9 alpha for the web and for tools that read it (Chrome, DaVinci). ProRes has a hard size floor at 1080p and a soft gradient costs most of its bits, so the transparent pieces carry no lamp wash — only the points glow — and stay between 8 and 16 MB. For a lamp behind the logo, use the opaque reveal or compose the `Logo_Animations` reveal over `05_GRAPHIC_ASSETS/Backgrounds/sanzeed-bg-lamp--dark-1920x1080.jpg`.
- **GIF** cannot hold soft alpha: transparent pieces are delivered on black. GIFs are previews and messaging assets; post the MP4s.
- **Loops.** The symbol loop and the loader are frame-exact loops (last frame = first frame). Set the player to loop; do not cross-fade the join.
- **Reduced motion.** Every CSS source and both web snippets honour `prefers-reduced-motion: reduce`. On the site, show the poster frame instead of autoplaying video when the preference is set.
- **Frame rate** is 30 fps throughout. For 25 fps broadcast delivery, re-render with `--fps 25` in `capture_frames.js` (edit `render.sh`), not by retiming the MP4.

## Files

<!--@files-->
### `Logo_Animations/` — 30 files, 27.64 MB

Logo reveal (4 s) in four formats and two pairings; logo outro (3 s); seamless symbol loop and the presentation logo with alpha.

| File | Pixels | Length | Format | Size | Editable from |
|---|---|---|---|---|---|
| `sanzeed-logo-outro--dark-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 44 KB | `Source_Files/logo-outro/index.html` |
| `sanzeed-logo-outro--dark-1920x1080.gif` | 960×540 | 3.0 s · 45 f · 17 fps | GIF | 163 KB | `Source_Files/logo-outro/index.html` |
| `sanzeed-logo-outro--dark-1920x1080.mp4` | 1920×1080 | 3.0 s · 90 f · 30 fps | H.264 · yuv420p | 104 KB | `Source_Files/logo-outro/index.html` |
| `sanzeed-logo-outro--dark-1920x1080.webm` | 1920×1080 | 3.0 s · 90 f · 30 fps | VP9 · yuv420p | 57 KB | `Source_Files/logo-outro/index.html` |
| `sanzeed-logo-presentation--alpha-1920x1080--poster.png` | 1920×1080 |  | PNG · alpha | 51 KB | `Source_Files/logo-presentation/index.html` |
| `sanzeed-logo-presentation--alpha-1920x1080.gif` | 960×540 | 4.0 s · 60 f · 17 fps | GIF | 99 KB | `Source_Files/logo-presentation/index.html` |
| `sanzeed-logo-presentation--alpha-1920x1080.mov` | 1920×1080 | 4.0 s · 120 f · 30 fps | ProRes 4444 · alpha · yuva444p12le | 11.79 MB | `Source_Files/logo-presentation/index.html` |
| `sanzeed-logo-presentation--alpha-1920x1080.mp4` | 1920×1080 | 4.0 s · 120 f · 30 fps | H.264 · yuv420p | 39 KB | `Source_Files/logo-presentation/index.html` |
| `sanzeed-logo-presentation--alpha-1920x1080.webm` | 1920×1080 | 4.0 s · 120 f · 30 fps | VP9 · alpha · yuv420p | 204 KB | `Source_Files/logo-presentation/index.html` |
| `sanzeed-logo-reveal--dark-1080x1080--poster.jpg` | 1080×1080 |  | JPEG q90 | 33 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1080.gif` | 960×960 | 4.0 s · 60 f · 17 fps | GIF | 2.82 MB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1080.mp4` | 1080×1080 | 4.0 s · 120 f · 30 fps | H.264 · yuv420p | 153 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1080.webm` | 1080×1080 | 4.0 s · 120 f · 30 fps | VP9 · yuv420p | 49 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1920--poster.jpg` | 1080×1920 |  | JPEG q90 | 46 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1920.gif` | 406×720 | 4.0 s · 60 f · 17 fps | GIF | 742 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1920.mp4` | 1080×1920 | 4.0 s · 120 f · 30 fps | H.264 · yuv420p | 239 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1080x1920.webm` | 1080×1920 | 4.0 s · 120 f · 30 fps | VP9 · yuv420p | 56 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 46 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1920x1080.gif` | 960×540 | 4.0 s · 60 f · 17 fps | GIF | 1.21 MB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1920x1080.mp4` | 1920×1080 | 4.0 s · 120 f · 30 fps | H.264 · yuv420p | 243 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--dark-1920x1080.webm` | 1920×1080 | 4.0 s · 120 f · 30 fps | VP9 · yuv420p | 57 KB | `Source_Files/logo-reveal/index.html` |
| `sanzeed-logo-reveal--light-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 42 KB | `Source_Files/logo-reveal/index-light.html` |
| `sanzeed-logo-reveal--light-1920x1080.gif` | 960×540 | 4.0 s · 60 f · 17 fps | GIF | 825 KB | `Source_Files/logo-reveal/index-light.html` |
| `sanzeed-logo-reveal--light-1920x1080.mp4` | 1920×1080 | 4.0 s · 120 f · 30 fps | H.264 · yuv420p | 180 KB | `Source_Files/logo-reveal/index-light.html` |
| `sanzeed-logo-reveal--light-1920x1080.webm` | 1920×1080 | 4.0 s · 120 f · 30 fps | VP9 · yuv420p | 47 KB | `Source_Files/logo-reveal/index-light.html` |
| `sanzeed-symbol-loop--alpha-1920x1080--poster.png` | 1920×1080 |  | PNG · alpha | 37 KB | `Source_Files/symbol-loop/index.html` |
| `sanzeed-symbol-loop--alpha-1920x1080.gif` | 960×540 | 3.0 s · 59 f · 20 fps | GIF | 132 KB | `Source_Files/symbol-loop/index.html` |
| `sanzeed-symbol-loop--alpha-1920x1080.mov` | 1920×1080 | 3.0 s · 90 f · 30 fps | ProRes 4444 · alpha · yuva444p12le | 7.96 MB | `Source_Files/symbol-loop/index.html` |
| `sanzeed-symbol-loop--alpha-1920x1080.mp4` | 1920×1080 | 3.0 s · 90 f · 30 fps | H.264 · yuv420p | 18 KB | `Source_Files/symbol-loop/index.html` |
| `sanzeed-symbol-loop--alpha-1920x1080.webm` | 1920×1080 | 3.0 s · 90 f · 30 fps | VP9 · alpha · yuv420p | 244 KB | `Source_Files/symbol-loop/index.html` |

### `Intros_Outros/` — 22 files, 19.74 MB

Branded intro and end card (6 s) in 16:9 and 9:16; the beam-wipe transition with alpha and a preview of it carrying a cut.

| File | Pixels | Length | Format | Size | Editable from |
|---|---|---|---|---|---|
| `sanzeed-intro--1080x1920--poster.jpg` | 1080×1920 |  | JPEG q90 | 86 KB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1080x1920.gif` | 406×720 | 6.0 s · 72 f · 12 fps | GIF | 668 KB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1080x1920.mp4` | 1080×1920 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 325 KB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1080x1920.webm` | 1080×1920 | 6.0 s · 180 f · 30 fps | VP9 · yuv420p | 133 KB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 76 KB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1920x1080.gif` | 960×540 | 6.0 s · 72 f · 12 fps | GIF | 1.08 MB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1920x1080.mp4` | 1920×1080 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 308 KB | `Source_Files/intro/index.html` |
| `sanzeed-intro--1920x1080.webm` | 1920×1080 | 6.0 s · 180 f · 30 fps | VP9 · yuv420p | 119 KB | `Source_Files/intro/index.html` |
| `sanzeed-outro--1080x1920--poster.jpg` | 1080×1920 |  | JPEG q90 | 99 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1080x1920.gif` | 406×720 | 6.0 s · 72 f · 12 fps | GIF | 352 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1080x1920.mp4` | 1080×1920 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 254 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1080x1920.webm` | 1080×1920 | 6.0 s · 180 f · 30 fps | VP9 · yuv420p | 161 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 89 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1920x1080.gif` | 960×540 | 6.0 s · 72 f · 12 fps | GIF | 569 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1920x1080.mp4` | 1920×1080 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 232 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-outro--1920x1080.webm` | 1920×1080 | 6.0 s · 180 f · 30 fps | VP9 · yuv420p | 135 KB | `Source_Files/outro-card/index.html` |
| `sanzeed-transition--alpha-1920x1080--poster.png` | 1920×1080 |  | PNG · alpha | 10 KB | `Source_Files/transition/index.html` |
| `sanzeed-transition--alpha-1920x1080.mov` | 1920×1080 | 1.5 s · 45 f · 30 fps | ProRes 4444 · alpha · yuva444p12le | 13.93 MB | `Source_Files/transition/index.html` |
| `sanzeed-transition--alpha-1920x1080.webm` | 1920×1080 | 1.5 s · 45 f · 30 fps | VP9 · alpha · yuv420p | 80 KB | `Source_Files/transition/index.html` |
| `sanzeed-transition--preview-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 191 KB | `Source_Files/transition/preview.html` |
| `sanzeed-transition--preview-1920x1080.gif` | 960×540 | 1.5 s · 23 f · 17 fps | GIF | 603 KB | `Source_Files/transition/preview.html` |
| `sanzeed-transition--preview-1920x1080.mp4` | 1920×1080 | 1.5 s · 45 f · 30 fps | H.264 · yuv420p | 354 KB | `Source_Files/transition/preview.html` |

### `Social_Animations/` — 18 files, 7.32 MB

Three stories (6 s), two posts (5 s) and the stat counter (5 s). MP4 for the platforms, GIF for previews and messaging.

| File | Pixels | Length | Format | Size | Editable from |
|---|---|---|---|---|---|
| `sanzeed-post--method-route-1080x1080--poster.jpg` | 1080×1080 |  | JPEG q90 | 70 KB | `Source_Files/post-method/index.html` |
| `sanzeed-post--method-route-1080x1080.gif` | 720×720 | 5.0 s · 60 f · 12 fps | GIF | 501 KB | `Source_Files/post-method/index.html` |
| `sanzeed-post--method-route-1080x1080.mp4` | 1080×1080 | 5.0 s · 150 f · 30 fps | H.264 · yuv420p | 150 KB | `Source_Files/post-method/index.html` |
| `sanzeed-post--project-1080x1080--poster.jpg` | 1080×1080 |  | JPEG q90 | 248 KB | `Source_Files/post-project/index.html` |
| `sanzeed-post--project-1080x1080.gif` | 720×720 | 5.0 s · 60 f · 12 fps | GIF | 1.47 MB | `Source_Files/post-project/index.html` |
| `sanzeed-post--project-1080x1080.mp4` | 1080×1080 | 5.0 s · 150 f · 30 fps | H.264 · yuv420p | 519 KB | `Source_Files/post-project/index.html` |
| `sanzeed-post--stat-counter-1080x1080--poster.jpg` | 1080×1080 |  | JPEG q90 | 74 KB | `Source_Files/post-stats/index.html` |
| `sanzeed-post--stat-counter-1080x1080.gif` | 720×720 | 5.0 s · 60 f · 12 fps | GIF | 574 KB | `Source_Files/post-stats/index.html` |
| `sanzeed-post--stat-counter-1080x1080.mp4` | 1080×1080 | 5.0 s · 150 f · 30 fps | H.264 · yuv420p | 192 KB | `Source_Files/post-stats/index.html` |
| `sanzeed-story--now-showing-1080x1920--poster.jpg` | 1080×1920 |  | JPEG q90 | 210 KB | `Source_Files/story-now-showing/index.html` |
| `sanzeed-story--now-showing-1080x1920.gif` | 406×720 | 6.0 s · 72 f · 12 fps | GIF | 561 KB | `Source_Files/story-now-showing/index.html` |
| `sanzeed-story--now-showing-1080x1920.mp4` | 1080×1920 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 428 KB | `Source_Files/story-now-showing/index.html` |
| `sanzeed-story--project-reveal-1080x1920--poster.jpg` | 1080×1920 |  | JPEG q90 | 342 KB | `Source_Files/story-project/index.html` |
| `sanzeed-story--project-reveal-1080x1920.gif` | 406×720 | 6.0 s · 72 f · 12 fps | GIF | 702 KB | `Source_Files/story-project/index.html` |
| `sanzeed-story--project-reveal-1080x1920.mp4` | 1080×1920 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 706 KB | `Source_Files/story-project/index.html` |
| `sanzeed-story--quote-light-wipe-1080x1920--poster.jpg` | 1080×1920 |  | JPEG q90 | 121 KB | `Source_Files/story-quote/index.html` |
| `sanzeed-story--quote-light-wipe-1080x1920.gif` | 406×720 | 6.0 s · 72 f · 12 fps | GIF | 335 KB | `Source_Files/story-quote/index.html` |
| `sanzeed-story--quote-light-wipe-1080x1920.mp4` | 1080×1920 | 6.0 s · 180 f · 30 fps | H.264 · yuv420p | 256 KB | `Source_Files/story-quote/index.html` |

### `Lower_Thirds/` — 15 files, 31.90 MB

Three lower thirds (5 s: in · hold · out) with alpha for the edit, each with an MP4 preview over an approved project image.

| File | Pixels | Length | Format | Size | Editable from |
|---|---|---|---|---|---|
| `sanzeed-lower-third--name--alpha-1920x1080--poster.png` | 1920×1080 |  | PNG · alpha | 10 KB | `Source_Files/lower-third-name/index.html` |
| `sanzeed-lower-third--name--alpha-1920x1080.mov` | 1920×1080 | 5.0 s · 150 f · 30 fps | ProRes 4444 · alpha · yuva444p12le | 8.57 MB | `Source_Files/lower-third-name/index.html` |
| `sanzeed-lower-third--name--alpha-1920x1080.webm` | 1920×1080 | 5.0 s · 150 f · 30 fps | VP9 · alpha · yuv420p | 62 KB | `Source_Files/lower-third-name/index.html` |
| `sanzeed-lower-third--name--preview-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 195 KB | `Source_Files/lower-third-name/preview.html` |
| `sanzeed-lower-third--name--preview-1920x1080.mp4` | 1920×1080 | 5.0 s · 150 f · 30 fps | H.264 · yuv420p | 251 KB | `Source_Files/lower-third-name/preview.html` |
| `sanzeed-lower-third--quote-attribution--alpha-1920x1080--poster.png` | 1920×1080 |  | PNG · alpha | 10 KB | `Source_Files/lower-third-quote/index.html` |
| `sanzeed-lower-third--quote-attribution--alpha-1920x1080.mov` | 1920×1080 | 5.0 s · 150 f · 30 fps | ProRes 4444 · alpha · yuva444p12le | 8.92 MB | `Source_Files/lower-third-quote/index.html` |
| `sanzeed-lower-third--quote-attribution--alpha-1920x1080.webm` | 1920×1080 | 5.0 s · 150 f · 30 fps | VP9 · alpha · yuv420p | 78 KB | `Source_Files/lower-third-quote/index.html` |
| `sanzeed-lower-third--quote-attribution--preview-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 526 KB | `Source_Files/lower-third-quote/preview.html` |
| `sanzeed-lower-third--quote-attribution--preview-1920x1080.mp4` | 1920×1080 | 5.0 s · 150 f · 30 fps | H.264 · yuv420p | 461 KB | `Source_Files/lower-third-quote/preview.html` |
| `sanzeed-lower-third--wall-label--alpha-1920x1080--poster.png` | 1920×1080 |  | PNG · alpha | 10 KB | `Source_Files/lower-third-label/index.html` |
| `sanzeed-lower-third--wall-label--alpha-1920x1080.mov` | 1920×1080 | 5.0 s · 150 f · 30 fps | ProRes 4444 · alpha · yuva444p12le | 12.24 MB | `Source_Files/lower-third-label/index.html` |
| `sanzeed-lower-third--wall-label--alpha-1920x1080.webm` | 1920×1080 | 5.0 s · 150 f · 30 fps | VP9 · alpha · yuv420p | 95 KB | `Source_Files/lower-third-label/index.html` |
| `sanzeed-lower-third--wall-label--preview-1920x1080--poster.jpg` | 1920×1080 |  | JPEG q90 | 222 KB | `Source_Files/lower-third-label/preview.html` |
| `sanzeed-lower-third--wall-label--preview-1920x1080.mp4` | 1920×1080 | 5.0 s · 150 f · 30 fps | H.264 · yuv420p | 296 KB | `Source_Files/lower-third-label/preview.html` |

### `Website_Loader/` — 9 files, 51 KB

The loader as CSS, SVG + SMIL, Lottie, GIF and MP4; the reveal-on-scroll snippet; a self-contained demo page.

| File | Pixels | Length | Format | Size | Editable from |
|---|---|---|---|---|---|
| `sanzeed-loader--960x120--poster.jpg` | 960×120 |  | JPEG q90 | 2 KB | `Source_Files/loader/index.html + Website_Loader/sanzeed-loader.css` |
| `sanzeed-loader--960x120.gif` | 960×120 | 2.0 s · 40 f · 20 fps | GIF | 31 KB | `Source_Files/loader/index.html + Website_Loader/sanzeed-loader.css` |
| `sanzeed-loader--960x120.mp4` | 960×120 | 2.0 s · 60 f · 30 fps | H.264 · yuv420p | 5 KB | `Source_Files/loader/index.html + Website_Loader/sanzeed-loader.css` |
| `sanzeed-loader--smil.svg` | 0 0 480 48 |  | SVG + SMIL | 1 KB | `itself (hand-written)` |
| `sanzeed-loader.css` |  |  | CSS | 2 KB | `itself (hand-written)` |
| `sanzeed-loader.html` |  |  | HTML | 4 KB | `itself (hand-written)` |
| `sanzeed-loader.json` | 480×48 | 2.0 s · 60 f · 30 fps | Lottie JSON (bodymovin 5.7) | 3 KB | `Source_Files/lottie/build_lottie.py` |
| `sanzeed-reveal-on-scroll.css` |  |  | CSS | 2 KB | `itself (hand-written)` |
| `sanzeed-reveal-on-scroll.js` |  |  | JavaScript | 1 KB | `itself (hand-written)` |

### `Exports/`

| Folder | Contents | Files | Size | Produced by |
|---|---|---|---|---|
| `Exports/Key_Frames/` | six key frames per rendered animation (960 px JPG q90, PNG with alpha for transparent pieces), one folder per animation | 156 | 7.14 MB | `Source_Files/render.sh` |
| `Exports/Contact_Sheets/` | one contact sheet per deliverable folder and one master sheet of every animation | 6 | 3.97 MB | `Source_Files/build_contact_sheets.py` |
| `Exports/Lottie_Proofs/` | frames of the two Lottie files rendered by lottie-web in Chromium, with a labelled proof strip each | 14 | 1.62 MB | `Source_Files/lottie/validate_lottie.js` |
| `Exports/Motion_Principles/` | the easing-curve and timing-scale diagram used in Motion_Principles.md (3200×2000 PNG) | 1 | 278 KB | `Source_Files/motion-principles/easing-curves.html` via render.js |

`Source_Files/`: 44 files, 729 KB (of which lottie.min.js is 298 KB).

**Whole folder: 317 files, 100.40 MB.**
<!--@/files-->

## Limitations

- ProRes 4444 is delivered for the transparent pieces only (symbol loop, presentation logo, transition, three lower thirds); opaque pieces are MP4 / WebM / GIF as specified. The lamp wash is omitted from the transparent masters for size (see Delivery notes).
- The Lottie files cover the logo reveal and the loader, as specified. Lottie-web's SVG renderer draws the radial gold halos as gradient fills (no blur effects), so the glow is a touch flatter than in the video renders; the proof strips show the actual result.
- No `.aep` / `.mogrt` files: the editable sources are HTML + CSS and Lottie JSON. The ProRes masters and the Lottie JSON import directly into After Effects (Bodymovin / LottieFiles plug-in) and Premiere.
