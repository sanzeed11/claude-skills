# Image_Templates — the Sanzeed image treatments

Three ways to put a photograph in the brand: an editable HTML plate rendered with the brand kit, a Python script for batches, and SVG frames for Illustrator / Figma. Full documentation, options and rebuild commands are in `../README.md` (section 4).

| File | Use |
|---|---|
| `wall-label-plate--16x9.html`, `--4x5.html`, `--1x1.html`, `--9x16.html` | image + veil + wall label (Title · Place), optional headline and symbol. Edit the JSON block at the top, then render with `render.js` at the size written in the comment. |
| `room-frame.html` | the image inside the hairline "room" on Night with counter, wordmark and label (1920×1080). |
| `before-after-grade.html` | a before/after pair for grading reviews (1920×1080). |
| `portrait-plate.html` | the portrait with headline, descriptor and contact — speaker cards, banners, About (1920×1080). |
| `treat_image.py` | `python3 treat_image.py IN OUT --ratio 4:5 --focal 0.5,0.45 --width 2160 --veil 0.72 --title "…" --place "…" --counter 001 [--headline "…"] [--frame] [--concept]` |
| `build_templates.py` | regenerates the HTML templates, the SVG frames and the example PNGs in `examples/`. |
| `SVG_Frames/sanzeed-frame--*.svg` | 16:9, 4:5, 1:1, 9:16, 3:2 and room-16:9 frames with a clearly named `#IMAGE_PLACEHOLDER` rect, the veil and the wall label group. |
| `examples/` | one rendered PNG per template, plus `sanzeed-frame--16x9-preview.png`. |

Rules the templates enforce: the correct logo variant for a dark plate (full-colour-dark), one gold accent (counter / eyebrow / the headline's last word / the symbol's dots — all Lamp Gold), Fraunces 300 for the headline, Inter Tight 600 + Inter 400 for the label, the veil under any text, and image crops around the focal point recorded in `../Approved_Images/approved.json`.
