# 08_SOCIAL_MEDIA — the Sanzeed social-media identity

Profile images, covers and banners, post, story, reel and pin templates for Instagram, Facebook, LinkedIn, YouTube, X and
Pinterest — every file at the platform's exact pixels (brand kit §8), every export with its editable source beside it.

**The language.** Dark gallery by default: Gallery Black / Night ground, Gallery White type, one Lamp Gold accent (the lit
last word of a headline, or the point on the beam). A light *label* variant (Plaster, Soot, Old Gold) for the 4:5 project
post, the LinkedIn insight post and the Pinterest method pin. The `full-colour-dark` wordmark top-left with its clear space
(`full-colour-light` on the light variant). Fraunces 300 headlines in sentence case ending with a full stop; Inter Tight 600
eyebrows and wall-label titles; Inter 400 for places, body and the site line. The client's own project images, always with
a wall label (Title · Place), under the veil when type sits on them or in a rounded "room" when not. The point and the beam
are the only decoration; no gradients on type, no shadows, no second accent.

**The copy** is confirmed copy from `01_BRAND_STRATEGY` and sanzeed.com — case-study lines (*A corridor you walk in order.*
*The building is the screen.* *A garden of gestures.*), service lines, the headline bank, the method steps with their named
deliverables, the four proof figures and the contact details. The only placeholder is `[Date and time]` on the event cover.

| Folder | Contents | Files |
|---|---|---|
| [`Instagram/`](Instagram/README.md) | profile 320 + 1024 (dark / light), 9 square posts (4 templates + 5 variants), 3 portrait posts, `Stories/` ×4 + safe-zone guide, `Highlight_Covers/` ×8, `Reels/` ×2 + crop guides, 3×3 grid preview | 34 |
| [`Facebook/`](Facebook/README.md) | profile 320 + 720, cover PNG + JPG + safe-zone guide, 2 post images, event cover PNG + JPG | 11 |
| [`LinkedIn/`](LinkedIn/README.md) | profile 400, company logo 300, personal banner (+ JPG, avatar guide), company banner (+ JPG), 4 posts 1200×627, 2 posts 1080×1080, `Carousel/` 5-page PDF + page PNGs | 21 |
| [`YouTube/`](YouTube/README.md) | profile 800, banner PNG + JPG + safe-area guide, 3 thumbnails (PNG + JPG), end screen PNG + JPG + element-zones guide | 14 |
| [`X/`](X/README.md) | profile 400, header PNG + JPG + avatar guide, 3 post images 1600×900 | 8 |
| [`Pinterest/`](Pinterest/README.md) | profile 165 + 600, 3 pins 1000×1500 | 7 |
| [`Editable_Templates/`](Editable_Templates/README.md) | the HTML+CSS sources (one file per template, `DATA` block at the top), `social.css`, `fill.js`, `render-all.sh`, `post_process.py`, `build_pptx.py`, `write_readmes.py`, `PPTX/` (6 PPTX + proofs + baked image assets) | 38 + 6 PPTX |

## Editing and regenerating

Open the template in `Editable_Templates/<platform>/`, change the `DATA` block at the top (text, image path, crop point),
then `bash Editable_Templates/render-all.sh <platform>` — or `bash Editable_Templates/render-all.sh` for everything,
including the profile images, grid preview, JPGs and the PPTX proofs. Details, the data keys and the rules the templates
carry are in [`Editable_Templates/README.md`](Editable_Templates/README.md). Every platform README lists each file with
its measured pixels, size, use, upload notes and source.

## Verified

Every render was opened after generation and checked: the wordmark variant matches its ground (dark on dark, light on
light) and sits on ≥ 80 % black with its clear space; one gold accent per composition; Fraunces renders as the light serif;
nothing clipped or overlapping; no empty boxes; story copy inside the 1080×1420 band; banner copy inside the platform safe
areas and clear of the avatar overlaps (the `--guide` renders show the zones). All 94 raster exports were measured at their
exact platform pixels; the carousel PDF has five 1080 × 1351 px pages (CSS `@page` 1080 × 1350 px; Chromium rounds the height up by one pixel — LinkedIn accepts it as 4:5); the six PPTX files open in LibreOffice with the brand
fonts resolved (proofs in `Editable_Templates/PPTX/proofs/`).

## Requirements

Node 22 with Playwright (Chromium) for `render.js`; Python 3 with Pillow, python-pptx and pypdf; LibreOffice for the
PPTX proofs; the brand fonts in `04_TYPOGRAPHY/Font_Files` installed system-wide (all present in the production container).
Helpers used are the kit's own: `15_SOURCE_FILES/Project_Files/brand-kit/render.js`.
