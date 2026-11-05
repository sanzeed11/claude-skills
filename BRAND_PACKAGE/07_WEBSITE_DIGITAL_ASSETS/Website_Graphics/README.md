# Website_Graphics — the site's drawn pieces

The orbit on the lamp (the hero's alternative to the three.js scene, drawn in monoline), the “Now showing” card frame, the method route, the 404 doorway, the loader, the cursor and the social-proof strip. SVG sources live in `src/`; exports sit in the named folders. Export any SVG with `python3 ../../15_SOURCE_FILES/Project_Files/brand-kit/export_svg.py src/<file>.svg <out_base> --png=<widths> --formats=png,webp[,pdf]`.

## Section_Backgrounds — hero orbit on the lamp

| File | Spec | Edit |
|---|---|---|
| `sanzeed-hero-orbit-lamp--dark.svg`, `--light.svg` | 1600×900 SVG: background, lamp radial gradient, sphere + ring + plinth in 1.5 px hairlines, one gold point on the ring (glow by blur filter), a few dust points. Dark: Gallery Black / Gallery White lines / Lamp Gold; light: Plaster / Soot / Old Gold | `src/orbit-lamp--dark.svg`, `--light.svg` (strokes in the `<style>` block, geometry in the groups) |
| `…--dark-1600w.png`, `--3200w.png` + `.webp` | 1600×900 and 3200×1800 (2×) | `export_svg.py … --png=1600,3200 --formats=png,webp` |
| `…--light-1600w.png`, `--3200w.png` + `.webp` | as above | |

Use as `background: #000 url(…) center / cover` behind the hero, or as the `<img>` poster when WebGL is off. The same drawing is inlined in `UI_Components/ui-kit.html` (hero) with `currentColor` so it follows the theme.

## Card_Frame — “Now showing”

| File | Spec | Edit |
|---|---|---|
| `sanzeed-now-showing-frame--1920x1080.svg` / `.png` / `.webp` | 1920×1080 transparent overlay: the room (radius 56 = 28 at 960), 2 px hairline at 14 %, veil gradient over the lower half, NOW SHOWING glass tag with the point, wall-label slot `[Project title]` / `[Place]` bottom-left, arrow bottom-right | `src/now-showing-frame.svg`; replace the bracketed labels, place the project image under the layer clipped to the rounded rectangle |

## Method — the route

| File | Spec | Edit |
|---|---|---|
| `sanzeed-method-route--dark.svg` / `--light.svg` | 1600×420: a beam with four points (STEP 01 Discover · 02 Direct · 03 Craft · 04 Deliver), the lit point on step 01, “You receive …” under each, OPENING NIGHT at the end. Fraunces 300 / Inter Tight 600 / Inter 400 as live text | `src/method-route--dark.svg`, `--light.svg` (text is editable; move the gold point to the current step) |
| `…-1600w.png`, `-3200w.png`, `.webp`, `.pdf` | raster at 1× and 2×, PDF with text outlined (Inkscape) for decks and print | `export_svg.py … --png=1600,3200 --formats=png,webp,pdf` |

## Illustration_404 — the closed doorway

| File | Spec | Edit |
|---|---|---|
| `sanzeed-404-doorway--dark.svg` / `--light.svg` | 800×800 transparent: the arch (the N/M doorway), closed by a hairline, the point of light waiting outside | `src/illustration-404--dark.svg`, `--light.svg`; `-on-ground` variants in `src/` add the background rect |
| `…-800w.png`, `-1600w.png`, `.webp` | 1× and 2× transparent PNG + WebP | |

Pairs with the kit's 019 state: “This room isn't open.”

## Loading — the point travels the beam

| File | Spec | Edit |
|---|---|---|
| `loading.css` | drop-in CSS: `<div class="sz-loader" role="status" aria-label="Loading"></div>`; 160 px beam, 9 px point with the glow, `sz-beam` 1.6 s on `cubic-bezier(.65,0,.2,1)` forever; reduced-motion rests the point at the end | edit the custom properties `--w`, `--dot` |
| `sanzeed-loading--beam.svg` | 200×40 SMIL-animated SVG (works as `<img>` or inline) | edit `dur` / `keySplines` |
| `sanzeed-loading--beam-960x240.mp4` | 960×240, 30 fps, 3.2 s (two cycles), H.264 CRF 20, yuv420p, faststart | `node capture_frames.js --in src/loading-demo.html --out Loading/sanzeed-loading--beam-960x240 --width 960 --height 240 --fps 30 --duration 3.2 --formats mp4,gif --keepframes` then `ffmpeg … -crf 20` on the frames (commands in the build history; see root README) |
| `sanzeed-loading--beam-960x240.gif` | 960×240, 20 fps palette GIF | same capture |
| `src/loading-demo.html` | the page the frames are captured from (320 px beam, 12 px point) | |

## Cursor — the point of light

| File | Spec | Edit |
|---|---|---|
| `sanzeed-cursor-dot.svg` | 32×32, gold point r 5 with a soft glow and a 35 % black keyline so it reads on both grounds; hotspot 16 16 | edit colours / radius |
| `sanzeed-cursor-dot-32.png`, `-64.png` | 1× and 2× cursor PNGs | cairosvg from the SVG |
| `cursor.css` | `.sz-cursor` with `image-set` for 1×/2×, resets to `pointer` / `auto` on links, buttons, inputs and text; `.sz-dot` trailing-dot fallback positioned with `--x`/`--y` | |

Use on dark sections and the gallery only; keep the system cursor on forms and reading text.

## Social_Proof — “Trusted by …”, text only

| File | Spec | Edit |
|---|---|---|
| `social-proof-strip.html` | the strip: eyebrow TRUSTED BY, the four names in Fraunces 300 separated by points, “from concept to public unveiling.” — no logos (the names are set as text, as on sanzeed.com) | edit the names in the HTML; `src/social-proof-strip.html` is the same file |
| `sanzeed-social-proof-strip--dark-3200x400.png` / `.webp` | 1600×200 at 2× | `render.js --in src/social-proof-strip.html --width 1600 --height 200 --scale 2` |
| `sanzeed-social-proof-strip--light-3200x400.png` / `.webp` | light theme (`--js "document.documentElement.setAttribute('data-theme','light')"`) | |
