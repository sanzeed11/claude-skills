# Backgrounds — lamp, dusk, plaster, presentation, covers, photo plates

All rendered by `build_backgrounds.py` from the sources in `src/` with the kit's `render.js` (Chromium, brand.css tokens and
fonts), so every pixel matches the website's CSS. Photographic / gradient renders are JPG q90; slide backgrounds are
PNG 1920 × 1080 (exact slide pixels) plus JPG 3840 × 2160 (2 ×).

| Set | Files | Notes |
|---|---|---|
| **Lamp** (dark) | `sanzeed-bg-lamp--dark-{1920x1080,2560x1440,1080x1920,1080x1080}.jpg` | Gallery Black + `--sz-gradient-lamp` + 7 % grain. Behind a single lit object, the logo, a cover title. Source `src/sanzeed-bg-lamp--dark.html` |
| **Dusk** (dark) | `sanzeed-bg-dusk--dark-*.jpg` (4 sizes) | `#000 → #1C1C1E`. Section and slide backgrounds |
| **Plaster** (light) | `sanzeed-bg-plaster--light-*.jpg` (4 sizes) | `#FBF8F2 → #ECE7DC`. Documents, light mode |
| **Grain variants** | `sanzeed-bg-grain--{charcoal,dusk,lamp}-1920x1080.jpg` | the brand `.grain` (7 % soft-light) on surfaces where it reads; on pure black it is invisible by definition, so use Night/Charcoal or the Textures grain tile instead |
| **Presentation 16:9** | `sanzeed-bg-presentation-{title,content,section,end}--{dark,light}-1920x1080.png` + `-3840x2160.jpg` | title: lamp low + beam + primary wordmark bottom-left (300 px). content: hairline + point top, wordmark 180 px bottom-left. section: dusk / plaster + the doorway arch right. end: lamp centred + wordmark centred (520 px) + beam. Dark uses `full-colour-dark`, light `full-colour-light`; clear space ≥ ½ cap height is kept everywhere. Sources `src/sanzeed-bg-presentation-*.html` |
| **A4 covers** | `sanzeed-cover-a4--{dark,light}.svg` + `.pdf` + `-2480x3508.png` | 210 × 297 mm, 20 mm margins, `horizontal-descriptor` lockup bottom-left at 70 mm (rule for document covers), beam + point above it, the doorway arch as a window motif (fading legs), lamp glow / plaster gradient. The SVG is the master (1 unit = 0.1 mm; logo embedded as paths); PDF via Inkscape (vector); PNG at 300 dpi via Chromium (`src/sanzeed-cover-a4--*.html` wrapper). Title goes top-left in Fraunces 300 |
| **Photo plates** | `sanzeed-bg-photo-plate--{prime-minister-museum,ram-katha-show,buddha-park}-1920x1080.jpg` | approved project images (from `00_ORIGINAL_ASSETS_BACKUP/images/img/`) under the veil (→ 88 % black at the base), wall label bottom-left (Title · Place), wordmark bottom-right on ≥ 80 % black, grain. Swap the image and the two label lines in `src/sanzeed-bg-photo-plate--*.html` for any other project; the 960 × 540 masters are upscaled 2 × under the veil |

**Edit:** change a source in `src/` (they are plain HTML using `brand.css` + `src/_base.css`) and run
`python3 build_backgrounds.py <group>` with `lamp`, `dusk`, `plaster`, `grain`, `presentation`, `covers` or `plates`.
The JPGs are written at q90 by Pillow; the PNGs come straight from Chromium.

| File | Format | Spec | Size |
|---|---|---|---|
| `build_backgrounds.py` | PY | Python generator | 7 KB |
| `sanzeed-bg-dusk--dark-1080x1080.jpg` | JPG | 1080 × 1080 px | 14 KB |
| `sanzeed-bg-dusk--dark-1080x1920.jpg` | JPG | 1080 × 1920 px | 24 KB |
| `sanzeed-bg-dusk--dark-1920x1080.jpg` | JPG | 1920 × 1080 px | 24 KB |
| `sanzeed-bg-dusk--dark-2560x1440.jpg` | JPG | 2560 × 1440 px | 43 KB |
| `sanzeed-bg-grain--charcoal-1920x1080.jpg` | JPG | 1920 × 1080 px | 29 KB |
| `sanzeed-bg-grain--dusk-1920x1080.jpg` | JPG | 1920 × 1080 px | 31 KB |
| `sanzeed-bg-grain--lamp-1920x1080.jpg` | JPG | 1920 × 1080 px | 42 KB |
| `sanzeed-bg-lamp--dark-1080x1080.jpg` | JPG | 1080 × 1080 px | 27 KB |
| `sanzeed-bg-lamp--dark-1080x1920.jpg` | JPG | 1080 × 1920 px | 43 KB |
| `sanzeed-bg-lamp--dark-1920x1080.jpg` | JPG | 1920 × 1080 px | 42 KB |
| `sanzeed-bg-lamp--dark-2560x1440.jpg` | JPG | 2560 × 1440 px | 67 KB |
| `sanzeed-bg-photo-plate--buddha-park-1920x1080.jpg` | JPG | 1920 × 1080 px | 444 KB |
| `sanzeed-bg-photo-plate--prime-minister-museum-1920x1080.jpg` | JPG | 1920 × 1080 px | 277 KB |
| `sanzeed-bg-photo-plate--ram-katha-show-1920x1080.jpg` | JPG | 1920 × 1080 px | 419 KB |
| `sanzeed-bg-plaster--light-1080x1080.jpg` | JPG | 1080 × 1080 px | 15 KB |
| `sanzeed-bg-plaster--light-1080x1920.jpg` | JPG | 1080 × 1920 px | 26 KB |
| `sanzeed-bg-plaster--light-1920x1080.jpg` | JPG | 1920 × 1080 px | 26 KB |
| `sanzeed-bg-plaster--light-2560x1440.jpg` | JPG | 2560 × 1440 px | 46 KB |
| `sanzeed-bg-presentation-content--dark-1920x1080.png` | PNG | 1920 × 1080 px | 14 KB |
| `sanzeed-bg-presentation-content--dark-3840x2160.jpg` | JPG | 3840 × 2160 px | 105 KB |
| `sanzeed-bg-presentation-content--light-1920x1080.png` | PNG | 1920 × 1080 px | 12 KB |
| `sanzeed-bg-presentation-content--light-3840x2160.jpg` | JPG | 3840 × 2160 px | 105 KB |
| `sanzeed-bg-presentation-end--dark-1920x1080.png` | PNG | 1920 × 1080 px | 833 KB |
| `sanzeed-bg-presentation-end--dark-3840x2160.jpg` | JPG | 3840 × 2160 px | 164 KB |
| `sanzeed-bg-presentation-end--light-1920x1080.png` | PNG | 1920 × 1080 px | 422 KB |
| `sanzeed-bg-presentation-end--light-3840x2160.jpg` | JPG | 3840 × 2160 px | 128 KB |
| `sanzeed-bg-presentation-section--dark-1920x1080.png` | PNG | 1920 × 1080 px | 328 KB |
| `sanzeed-bg-presentation-section--dark-3840x2160.jpg` | JPG | 3840 × 2160 px | 161 KB |
| `sanzeed-bg-presentation-section--light-1920x1080.png` | PNG | 1920 × 1080 px | 48 KB |
| `sanzeed-bg-presentation-section--light-3840x2160.jpg` | JPG | 3840 × 2160 px | 120 KB |
| `sanzeed-bg-presentation-title--dark-1920x1080.png` | PNG | 1920 × 1080 px | 809 KB |
| `sanzeed-bg-presentation-title--dark-3840x2160.jpg` | JPG | 3840 × 2160 px | 155 KB |
| `sanzeed-bg-presentation-title--light-1920x1080.png` | PNG | 1920 × 1080 px | 417 KB |
| `sanzeed-bg-presentation-title--light-3840x2160.jpg` | JPG | 3840 × 2160 px | 122 KB |
| `sanzeed-cover-a4--dark-2480x3508.png` | PNG | 2480 × 3508 px | 1.3 MB |
| `sanzeed-cover-a4--dark.pdf` | PDF | 210 × 297 mm (vector PDF) | 11 KB |
| `sanzeed-cover-a4--dark.svg` | SVG | 210 × 297 mm (vector) | 12 KB |
| `sanzeed-cover-a4--light-2480x3508.png` | PNG | 2480 × 3508 px | 196 KB |
| `sanzeed-cover-a4--light.pdf` | PDF | 210 × 297 mm (vector PDF) | 9 KB |
| `sanzeed-cover-a4--light.svg` | SVG | 210 × 297 mm (vector) | 11 KB |
| `src/_base.css` | CSS | CSS | 2 KB |
| `src/sanzeed-bg-dusk--dark.html` | HTML | HTML source | 359 B |
| `src/sanzeed-bg-grain--charcoal.html` | HTML | HTML source | 387 B |
| `src/sanzeed-bg-grain--dusk.html` | HTML | HTML source | 365 B |
| `src/sanzeed-bg-grain--lamp.html` | HTML | HTML source | 365 B |
| `src/sanzeed-bg-lamp--dark.html` | HTML | HTML source | 376 B |
| `src/sanzeed-bg-photo-plate--buddha-park.html` | HTML | HTML source | 1 KB |
| `src/sanzeed-bg-photo-plate--prime-minister-museum.html` | HTML | HTML source | 1 KB |
| `src/sanzeed-bg-photo-plate--ram-katha-show.html` | HTML | HTML source | 1 KB |
| `src/sanzeed-bg-plaster--light.html` | HTML | HTML source | 397 B |
| `src/sanzeed-bg-presentation-content--dark.html` | HTML | HTML source | 695 B |
| `src/sanzeed-bg-presentation-content--light.html` | HTML | HTML source | 733 B |
| `src/sanzeed-bg-presentation-end--dark.html` | HTML | HTML source | 678 B |
| `src/sanzeed-bg-presentation-end--light.html` | HTML | HTML source | 719 B |
| `src/sanzeed-bg-presentation-section--dark.html` | HTML | HTML source | 844 B |
| `src/sanzeed-bg-presentation-section--light.html` | HTML | HTML source | 882 B |
| `src/sanzeed-bg-presentation-title--dark.html` | HTML | HTML source | 680 B |
| `src/sanzeed-bg-presentation-title--light.html` | HTML | HTML source | 717 B |
| `src/sanzeed-cover-a4--dark.html` | HTML | HTML source | 288 B |
| `src/sanzeed-cover-a4--light.html` | HTML | HTML source | 290 B |

**61 files · 7.0 MB**
