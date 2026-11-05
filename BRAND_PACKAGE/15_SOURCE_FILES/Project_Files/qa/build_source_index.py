#!/usr/bin/env python3
"""build_source_index.py — writes 15_SOURCE_FILES/README.md, Original_Designs/INDEX.md and Editable_Assets/INDEX.md
by scanning the package for editable sources (HTML/CSS/SVG/PPTX/DOCX/JSON/Lottie/Python builders) and mapping
each to the deliverable folder it produces. Sources live beside their exports on purpose (edit → re-run → export);
this index is the map. Usage: python3 build_source_index.py <BRAND_PACKAGE>"""
import os, sys, re
ROOT = sys.argv[1].rstrip('/')
EDITABLE = {'.html': 'HTML+CSS (edit in any editor; render with brand-kit/render.js)', '.svg': 'SVG vector (Illustrator, Figma, Affinity, Inkscape)',
            '.pptx': 'PowerPoint / Keynote / Google Slides', '.docx': 'Word / Pages / Google Docs', '.json': 'JSON (tokens / Lottie)',
            '.py': 'Python build script (re-generates its outputs)', '.css': 'CSS tokens/styles', '.js': 'JavaScript helper', '.sh': 'Shell build script', '.md': 'Markdown'}
SKIP = ('00_ORIGINAL_ASSETS_BACKUP', '16_WEBSITE_IMPLEMENTATION/img', 'node_modules', '_frames', '/pages/', 'Key_Frames')
rows = {}
for dp, dn, fn in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT)
    if any(s in rel + '/' for s in SKIP): continue
    for f in fn:
        ext = os.path.splitext(f)[1].lower()
        if ext not in EDITABLE: continue
        if ext == '.md' and f not in ('README.md',): continue
        if ext == '.md': continue
        if ext == '.svg' and ('/PNG' in rel or 'Favicon' in rel): continue
        top = rel.split('/')[0] if rel != '.' else '(root)'
        rows.setdefault(top, []).append((os.path.join(rel, f), ext))
out = ['# Editable source index', '', 'Every export in this package has an editable source. Sources are kept **beside their exports** (so `edit → re-run → export` stays obvious) and are listed here by folder. Formats: ' + '; '.join(f'`{k}` — {v}' for k, v in EDITABLE.items() if k not in ('.md',)), '',
       '| Folder | Editable sources | Count |', '|---|---|---|']
total = 0
for top in sorted(rows):
    files = sorted(rows[top]); total += len(files)
    kinds = {}
    for p, e in files: kinds[e] = kinds.get(e, 0) + 1
    out.append(f'| `{top}` | ' + ', '.join(f'{v} × {k}' for k, v in sorted(kinds.items())) + f' | {len(files)} |')
out += ['', f'Total editable source files: **{total}**', '', '## Full listing', '']
for top in sorted(rows):
    out += [f'### {top}', ''] + [f'- `{p}`' for p, e in sorted(rows[top])] + ['']
os.makedirs(os.path.join(ROOT, '15_SOURCE_FILES/Editable_Assets'), exist_ok=True); os.makedirs(os.path.join(ROOT, '15_SOURCE_FILES/Original_Designs'), exist_ok=True)
open(os.path.join(ROOT, '15_SOURCE_FILES/Editable_Assets/INDEX.md'), 'w').write('\n'.join(out))
orig = ['# Original designs — masters', '', 'The masters from which the identity is generated. Change these, re-run the builders, and every export regenerates.', '',
 '| Master | What it defines | Regenerate with |', '|---|---|---|',
 '| `../Project_Files/logo-builder/build_logo.py` | Every letterform, dot, lockup and colourway of the logo family (parametric: cap 500, stroke 64, dot r 45) | `python3 build_logo.py construction && python3 export_logo.py construction ../../../02_LOGO_SYSTEM` |',
 '| `../Project_Files/logo-builder/construction/*.svg` | Per-stroke editable construction SVGs of every variant (also in `02_LOGO_SYSTEM/Source_Files`) | opened directly in Illustrator / Figma / Inkscape |',
 '| `../Project_Files/logo-builder/build_logo_guides.py` | Clear-space, minimum-size, incorrect-usage, construction and placement sheets | `python3 build_logo_guides.py` |',
 '| `../Project_Files/colour-builder/build_colour.py` | The palette (names, HEX, roles, usage), gradients, themes, contrast matrix, Pantone proximity, swatches | `python3 build_colour.py ../../../03_COLOUR_SYSTEM` |',
 '| `../../04_TYPOGRAPHY/typography-tokens.json` | The type scale (screen px, print pt) and rules | edit JSON; `brand.css` mirrors it |',
 '| `../Project_Files/brand-kit/brand.css` | Design tokens and base components used by every HTML-authored deliverable | edit; re-render dependants |',
 '| `../Project_Files/brand-kit/doc.css` | A4 document page model for the PDF documents | edit; re-render documents |',
 '| `../../02_LOGO_SYSTEM/Signature/sanzeed-signature--*.svg` | The vectorised signature mark | edit in a vector app |',
 '| `../../00_ORIGINAL_ASSETS_BACKUP/` | The untouched originals from sanzeed.com (reference only) | — |',
 '', 'Production helpers: `../Project_Files/brand-kit/render.js` (HTML → PNG/PDF), `capture_frames.js` (animation → MP4/WebM/GIF/MOV), `export_svg.py` (SVG → PDF/EPS/PNG/WebP), `print_pdf.py` (bleed, crop marks, CMYK), and the QA scripts in `../Project_Files/qa/`.', '',
 '**Not supplied:** Adobe Illustrator `.ai`, Photoshop `.psd`, InDesign `.indd`, After Effects `.aep`, Figma `.fig` — these proprietary formats can only be written by their own applications. Every SVG/PDF here opens as editable vector in Illustrator and Figma; HTML/CSS and PPTX/DOCX are the editable sources for layouts; Lottie JSON and HTML/CSS are the motion sources (both import into After Effects).']
open(os.path.join(ROOT, '15_SOURCE_FILES/Original_Designs/INDEX.md'), 'w').write('\n'.join(orig))
readme = ['# 15_SOURCE_FILES', '', '| Folder | Contents |', '|---|---|',
 '| `Project_Files/` | The working tooling: `brand-kit/` (tokens CSS, document CSS, render/capture/export/print helpers, the production brief `BRAND_KIT_SPEC.md`), `logo-builder/` (parametric logo master, exporter, guideline-sheet generator, construction SVGs), `colour-builder/`, `qa/` (package audit, delivery checklist and this index generator). |',
 '| `Original_Designs/` | `INDEX.md` — the masters of the identity and how to regenerate everything from them. |',
 '| `Editable_Assets/` | `INDEX.md` — every editable source file in the package, listed by folder, with the application that edits it. |',
 '', 'Sources are deliberately stored next to the exports they generate (each deliverable folder has a `src/` or `_build/` folder and a README that names the command). This folder is the map to all of them.']
open(os.path.join(ROOT, '15_SOURCE_FILES/README.md'), 'w').write('\n'.join(readme))
print('indexed', total, 'editable sources')
