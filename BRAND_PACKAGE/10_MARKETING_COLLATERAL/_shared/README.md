# _shared — common layer for 10_MARKETING_COLLATERAL

| Path | What it is |
|---|---|
| `collateral.css` | the campaign vocabulary on top of `brand.css`: `.plate` (the room), `.wl` (wall label), `.hl` + `.pt` (Fraunces headline with the gold point), `.beam-h`, `.lamp`, print helpers; grain is dropped in print media |
| `img/` | derived imagery: the point-of-light object (`poster-dark.webp` upsampled to 2400 px, plus 4:5 and 1:1 crops; light version from `poster-light.webp`), portrait crops at 2000 px, and `jpg/` JPEG copies of project images used inside PDFs |
| `icons/` | monoline arrow icons on the logo construction (500-unit box, 64-unit stroke, 45-unit gold point at the tail); `--white` and `--soot` variants |
| `fonts-static/` | static instances (Fraunces Light + Italic, Inter Tight SemiBold / Medium, Inter Regular / Medium / Italic) made from the variable fonts in `04_TYPOGRAPHY` with fontTools, for Office documents (PPTX/DOCX name fonts by instance). OFL licences included. |
| `build/` | generators: `brandcopy.py` (all approved copy), `common.py` (paths, render/print helpers, `jimg`), `render_batch.js` (same as `render.js`, many jobs per browser), `build_*.py` one per subfolder, `pptx_kit.py` (brand on slides), `docstyle.py`, `manifest.py` (measures every file → `manifest.json`), `write_readmes.py` |

Rebuild everything: run each `build_*.py` from this folder, then `manifest.py` and `write_readmes.py`.
