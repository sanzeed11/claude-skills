#!/usr/bin/env python3
"""write_readmes.py — writes README.md in every subfolder of 10_MARKETING_COLLATERAL from manifest.json plus
hand-written notes (intended use, how to edit). Run after manifest.py."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import MC
MAN = json.load(open(f"{MC}/_shared/build/manifest.json"))
R = "node 15_SOURCE_FILES/Project_Files/brand-kit/render.js"
PP = "python3 15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py"

def table(folder):
    rows = [r for r in MAN if r["path"].startswith(folder + "/")]
    out = ["| File | Spec | Size |", "|---|---|---|"]
    for r in rows:
        rel = r["path"][len(folder) + 1:]
        out.append(f"| `{rel}` | {r['spec']} | {r['bytes']/1e6:.1f} MB |" if r["bytes"] > 1e6 else f"| `{rel}` | {r['spec']} | {r['bytes']/1e3:.0f} KB |")
    return "\n".join(out)

HEAD = "All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM` (the approved refined original wordmark, option B, 20 Nov 2026 — hooked S, three gold points on A, Z and D, the Z point in its ring; HTML sources link the SVGs and the PPTX/DOCX builders embed the PNGs at build time, so no logo geometry is copied into this folder); type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed."

NOTES = {
"Campaign_Templates": ("Campaign templates — “Carry the light across.”", f"""
Three campaign lines, each as a key visual in 16:9, 1:1 and 9:16; a digital ad set at IAB sizes; promotional web banners in dark and light.

**Composition rule (every piece):** black field (or Plaster for the light banners) · one lit object or one lit room inside a rounded “room” plate with a hairline · headline in Fraunces 300, sentence case, ending with a full stop — the stop is the single gold point · wall-label caption (Title · Place) · primary wordmark top-left (full-colour-dark on dark, full-colour-light on light) · `sanzeed.com` in the footer.

| Line | Image | Wall label |
|---|---|---|
| Carry the light across. | the point-of-light object (`_shared/img/hero-object--dark-2400.jpg`, from `poster-dark.webp`) | Between two points of light · sanzeed.com |
| Experiential design you can walk into. | Prime Minister Museum, the tricolour corridor (`_shared/img/jpg/case--prime-minister-museum-03.jpg` — the site exports this frame washed out, so the build uses a levels-restored copy; see `_shared/README.md`) | Prime Minister Museum · New Delhi |
| Tell me about the room. | the portrait, 4:5 crop | Sanzeed Mirza · New Delhi |

**Exports.** Key visuals: PNG at 2× (3840×2160 / 2160×2160 / 2160×3840) + JPG at 1× (q88). Ads: PNG at 2× (`@2x`) + JPG at exact IAB pixels. Banners: PNG at 2× + JPG at 1×. 9:16 keeps text inside the centre-safe 1080×1420 band.

**How to edit.** Every export has an HTML source in `src/`. Change the copy or swap the `<img>` in the HTML (paths are relative to `BRAND_PACKAGE`), then re-render, e.g.

```
{R} --in src/sanzeed-key-visual--carry-the-light-16x9.html --out sanzeed-key-visual--carry-the-light-16x9-3840x2160.png --width 1920 --height 1080 --scale 2
{R} --in src/sanzeed-ad--300x250.html --out sanzeed-ad--300x250@2x.png --width 300 --height 250 --scale 2
```
To regenerate the whole set from the templates: `python3 _shared/build/build_campaign.py`.
"""),
"Events": ("Events — invitation, event branding, exhibition graphics", f"""
**Invitation** (the event itself is a template: `[Day, date]`, `[Time]`, `[Venue]`, `[City]`, `[RSVP date]` are fields). A5 print with 3 mm bleed (page 154×216 mm, front + back), digital 1080×1350 (PNG 2× + JPG), email 600×800 (PNG 2× + JPG).

**Event branding set.** Backdrop 3000×2400 mm at 1:10 (wordmark 1800 mm wide, centre 1700 mm from the floor); welcome board 900×1800 mm at 1:10; name badge 90×60 mm (host + guest, 3 mm bleed); lanyard strip 900×20 mm at 1:1 (wordmark repeat with gold points); table tent A6 (A5 flat 148×210, fold at 105 mm, top face rotated 180°, 3 mm bleed).

**Exhibition graphics.** Roll-up banner 850×2000 mm at 1:5 (bottom 200 mm sits in the cassette — below the dashed line); booth wall panel 2400×2400 mm at 1:10.

Scaled artwork carries the scale in its name (`-1-10` = 1:10, `-1-5` = 1:5): print at 1000 % / 500 %, or ask the producer to scale to the stated real size. Print-ready files (`-print-ready-cmyk.pdf`) have crop marks, trim and bleed boxes and CMYK conversion from `print_pdf.py`; proof the gold before the run.

**How to edit.** Sources in `src/` (HTML, mm units, `@page`). Example:
```
{R} --in src/sanzeed-event-invitation--a5-print.html --out sanzeed-event-invitation--a5-bleed.pdf --pdf --size 154x216
{PP} sanzeed-event-invitation--a5-bleed.pdf sanzeed-event-invitation--a5-print-ready-cmyk.pdf --trim=148x210 --bleed=3 --cmyk
```
Regenerate everything: `python3 _shared/build/build_events.py`.
"""),
"Signage": ("Signage — door plate, wayfinding, totem, window vinyl, spec sheet", f"""
Every sign is Gallery Black with Gallery White letters and one gold point. Door plate and wayfinding plates are 300×100 mm (files carry 3 mm bleed: page 306×106 mm); the totem is 600×1800 mm at 1:10; the window vinyl is previewed on a 3000×2000 mm glass bay at 1:10 with a 1:1 cut file of the wordmark at 1200 mm.

| Sign | Content | Cap height |
|---|---|---|
| Door plate | horizontal-descriptor lockup, 180 mm wide | wordmark ≈ 25 mm (3 m viewing) |
| Arrow plates ×4 | monoline arrow (left / right / ahead / down) from `_shared/icons`, symbol at right | arrow box 48 mm |
| Room numbers 001–004 | Fraunces 300 numerals ending in the gold point, symbol at right | ≈ 36 mm |
| Totem | vertical-stacked lockup, directory 001–004 with arrows, master line, URL | directory numerals 90 mm real |
| Window vinyl | frosted band 600 mm, wordmark 1200 mm in white cut vinyl | — |

Each sign: `.html` source → `.pdf` (vector, fonts embedded) → `.svg` (pdftocairo, text as outlines — hand to the sign-maker) → `.png` preview → `-print-ready-cmyk.pdf` for printed plates. `sanzeed-wayfinding-set--8-plates-300x100mm.pdf` collects the eight plates. The spec sheet (A4, light) lists materials, minimum cap heights per viewing distance (25 mm per 3 m), mounting heights and finishes.

**How to edit.** Edit the HTML in `src/`, then:
```
{R} --in src/sanzeed-door-plate--300x100mm.html --out sanzeed-door-plate--300x100mm.pdf --pdf --size 306x106
pdftocairo -svg sanzeed-door-plate--300x100mm.pdf sanzeed-door-plate--300x100mm.svg
{PP} sanzeed-door-plate--300x100mm.pdf sanzeed-door-plate--300x100mm-print-ready-cmyk.pdf --trim=300x100 --bleed=3 --cmyk
```
Regenerate everything: `python3 _shared/build/build_signage.py`. The cut file `sanzeed-window-vinyl--wordmark-cut-1200mm.svg` is rebuilt by `cut_file()` from `02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--white.svg`: 1200 × 168.77 mm (the wordmark's own 7.11:1 ratio), filled closed paths only — the letter outline (Z ring included as a cut-out) plus the three points A, Z, D converted from circles to arc paths — ready for the plotter.
"""),
"Posters": ("Posters — campaign, method, typographic", f"""
Three posters at A2 (420×594 mm) and A3 (297×420 mm), each with 3 mm bleed in the PDF (A2 page 426×600, A3 page 303×426):

1. **Campaign** — “Carry the light across.” on black, the point-of-light object in a room plate, wall label, contact.
2. **Method** — “A method for the monumental.” on black; the four steps on a vertical route with gold points and “You receive …” deliverables.
3. **Typographic** — “90 projects, one continuous craft.” on Plaster; all ninety projects listed by gallery with 001–090 counters and wall labels.

Exports per poster and size: `-bleed.pdf` (RGB, for screen proofing), `-print-ready-cmyk.pdf` (crop marks, trim/bleed boxes, CMYK), `-preview.png`. The A3 is the A2 layout scaled by 0.7071 in the source.

**Resolution note.** The campaign poster’s image is the 1600×900 px site render, upsampled to 2400 px; at A2 it prints at ≈ 170 dpi. For a press run at full quality, supply a higher-resolution render of the object and drop it into `_shared/img/hero-object--dark-2400.jpg`.

**How to edit.** `src/sanzeed-poster--<name>-<size>.html`, then:
```
{R} --in src/sanzeed-poster--campaign-a2.html --out sanzeed-poster--campaign-a2-bleed.pdf --pdf --size 426x600
{PP} sanzeed-poster--campaign-a2-bleed.pdf sanzeed-poster--campaign-a2-print-ready-cmyk.pdf --trim=420x594 --bleed=3 --cmyk
```
Regenerate all six: `python3 _shared/build/build_posters.py`.
"""),
"Flyers": ("Flyers — A5 two-sided flyer and DL leaflet", f"""
**A5 flyer** (148×210 mm, 3 mm bleed → page 154×216). Front, dark: the key visual (master line, point-of-light object, wall label, CTA). Back, Plaster: the seven services with their lines, “All seven, every time.”, the four method steps with “You receive …”, and contact with the descriptor lockup.

**DL leaflet** (99×210 mm, 3 mm bleed → page 105×216). Front, dark: “Carry the light across.” with the object in a 4:5 plate. Back, Plaster: “Seven ways to carry the light across.” — services, method in one line each, contact.

Exports: `-bleed.pdf` (2 pages, RGB), `-print-ready-cmyk.pdf` (crop marks, CMYK), `-front.png` / `-back.png` previews at 3×.

**How to edit.** `src/*.html`, then:
```
{R} --in src/sanzeed-flyer--a5-two-sided.html --out sanzeed-flyer--a5-two-sided-bleed.pdf --pdf --size 154x216
{PP} sanzeed-flyer--a5-two-sided-bleed.pdf sanzeed-flyer--a5-two-sided-print-ready-cmyk.pdf --trim=148x210 --bleed=3 --cmyk
```
Regenerate: `python3 _shared/build/build_flyers.py`.
"""),
"Brochures": ("Brochures — A4 trifold and 12-page company profile", f"""
**A4 trifold** (297×210 mm landscape, 3 mm bleed → page 303×216, 2 pages). Outside spread, dark, panels left→right **98 | 99 | 100 mm** = inside flap (About, portrait, proof numbers, trust line) · back cover (Tell me about the room, contact, promises, descriptor lockup, rights line) · front cover (wordmark, object plate, master line). Inside spread, Plaster, panels **100 | 99 | 98 mm** = seven services · method · now showing (three case studies with wall labels). Fold guides show in the PNG previews only (screen media); the PDFs carry none. Roll fold: the 98 mm panel folds in first.

**12-page company profile** (A4 portrait, 3 mm bleed → page 216×303). 01 cover · 02 the one idea (Carry the light across + brand story) · 03 about, proof, three pillars, quote · 04 seven services · 05 method · 06–07 Prime Minister Museum · 08–09 Ram Katha Show · 10–11 Buddha Park (each a spread: brief, idea and hero image left; four case images with captions, the walk, what visitors do, type/location/role right) · 12 the galleries (all 90), journey timeline, contact. Dark pages for the gallery, Plaster pages for reading. Reader spreads exported as PNG (`--spread-*.png`, bleed cropped).

Print-ready versions add crop marks and CMYK. Saddle-stitch the profile (12 pages = 3 sheets A3 folded).

**How to edit.** `src/sanzeed-brochure--a4-trifold.html`, `src/sanzeed-company-profile--a4-12pp.html` (one `<section class="sheet">` per page), then:
```
{R} --in src/sanzeed-company-profile--a4-12pp.html --out sanzeed-company-profile--a4-12pp-bleed.pdf --pdf --size 216x303
{PP} sanzeed-company-profile--a4-12pp-bleed.pdf sanzeed-company-profile--a4-12pp-print-ready-cmyk.pdf --trim=210x297 --bleed=3 --cmyk
```
Regenerate (also rebuilds the spread PNGs): `python3 _shared/build/build_brochures.py`. Images in PDFs are JPEG copies from `_shared/img/jpg/` (made by `common.jimg`).
"""),
"Media_Kit": ("Media kit", f"""
`sanzeed-media-kit--a4.pdf` — 7 pages: cover · 01 biographies (10 / 25 / 50 words, in his words, boilerplate, naming) · 02 headshots (three crops, with file names and use notes) · 03 fact sheet (confirmed facts only) · 04 logo usage summary (refers to `02_LOGO_SYSTEM`) · 05 projects (the eight “now showing” rooms and all ninety by gallery) · 06 contact. Page previews at 90 dpi. `media-kit-contents.md` lists everything a journalist receives, with the copy blocks as plain text. The headshot JPGs live in `../Press/`.

**How to edit.** `src/sanzeed-media-kit--a4.html`, then `{R} --in src/sanzeed-media-kit--a4.html --out sanzeed-media-kit--a4.pdf --pdf --size 210x297`. Regenerate (also re-exports the headshots): `python3 _shared/build/build_mediakit.py`.
"""),
"Presentations": ("Presentations — sales deck, proposal template, case-study and portfolio templates", f"""
**Sales presentation** `sanzeed-sales-presentation--16-slides.pptx` (16:9, 13.333×7.5 in, 16 slides): 01 cover · 02 the one idea · 03 about · 04 proof · 05 three pillars · 06 seven services · 07 now showing (eight rooms) · 08 method · 09–10 Prime Minister Museum · 11 Ram Katha Show · 12 Buddha Park · 13 journey · 14 how a project starts (project types, timelines, budget bands from the enquiry form) · 15 quote · 16 contact. Also as PDF and one PNG per slide (`--slide-NN.png`).

**Proposal template** `sanzeed-proposal-template--12-slides.pptx` (12 slides): cover · the room · the story · approach · scope · deliverables · timeline · investment bands · team · why Sanzeed · selected work · next step. Every `[bracketed]` field is for the client/project; the investment slide carries `[GSTIN]` and `[Bank name]` fields. Also PDF + PNG per slide.

Both decks are built with python-pptx and are fully editable in PowerPoint/Keynote/Google Slides. Fonts used by name: **Fraunces Light**, **Inter Tight SemiBold**, **Inter**, **Inter Medium** — install the static instances from `_shared/fonts-static/` (derived from `04_TYPOGRAPHY`) so the decks render as designed. Images are JPEG copies in `src/assets/` (the Prime Minister Museum corridor, `case--prime-minister-museum-03.jpg`, is the levels-restored copy — see `_shared/README.md`); pictures are masked to rounded rectangles (the room) with a hairline.

**Case-study template** — A4, 2 pages, from HTML: `--filled-prime-minister-museum` (complete) and `--blank` (bracketed fields and labelled image slots). **Portfolio template** — A4 landscape, 12 pages: cover · 10 projects (one per page, full-bleed-style plate, counter, title, place, category, wall label; the three case studies carry their idea line) · contact.

**How to edit.** Decks: open the PPTX, or edit `_shared/build/build_presentations.py` and re-run (`python3 _shared/build/build_presentations.py`; PDF/PNG come from `soffice --headless --convert-to pdf` + `pdftoppm`). Templates: `src/*.html` then e.g. `{R} --in src/sanzeed-portfolio-template--a4-landscape.html --out sanzeed-portfolio-template--a4-landscape.pdf --pdf --size 297x210`.
"""),
"Press": ("Press — release template, sample release, headshots, fact sheet, logo note, About page", f"""
- `sanzeed-press-release--2026-independent-practice.docx` — sample release, dated New Delhi, 5 November 2026, using only confirmed facts (dates and roles from the site timeline, the 90/60/15 numbers, the three case studies, Sanzeed’s own two quotes). PDF preview alongside.
- `sanzeed-press-release--template.docx` — the same structure with bracketed fields; boilerplate and media contact pre-filled.
- `sanzeed-fact-sheet.docx` (+ PDF) — editable fact sheet, two pages.
- `sanzeed-mirza-headshot--1x1 / 4x5 / 3x4-2000.jpg` — portrait crops at 2000 px (upsampled from the 1100 px source; request the original for print above A5).
- `logo-pack-note.md` — points to `02_LOGO_SYSTEM`; no logo files are duplicated here.
- `sanzeed-about--one-page.pdf` (+ PNG, HTML source) — one-page About Sanzeed on Plaster.

DOCX files are generated with python-docx (`_shared/build/build_press.py`): A4, 20 mm margins, logo in the header, contact in the footer; headings in Fraunces Light, labels in Inter Tight SemiBold, body in Inter. Install `_shared/fonts-static/` for Word to show the right weights.

**How to edit.** Open the DOCX in Word, or change the copy in `_shared/build/build_press.py` and re-run it (PDF previews via `soffice --headless --convert-to pdf`). About page: `src/sanzeed-about--one-page.html` → `{R} --in src/sanzeed-about--one-page.html --out sanzeed-about--one-page.pdf --pdf --size 210x297`.
"""),
}

if __name__ == "__main__":
    for folder, (title, body) in NOTES.items():
        md = f"# {title}\n\n{HEAD}\n{body}\n## Files\n\n{table(folder)}\n"
        open(f"{MC}/{folder}/README.md", "w", encoding="utf-8").write(md); print("wrote", folder)
    shared = f"""# _shared — common layer for 10_MARKETING_COLLATERAL

| Path | What it is |
|---|---|
| `collateral.css` | the campaign vocabulary on top of `brand.css`: `.plate` (the room), `.wl` (wall label), `.hl` + `.pt` (Fraunces headline with the gold point), `.beam-h`, `.lamp`, print helpers; grain is dropped in print media |
| `img/` | derived imagery: the point-of-light object (`poster-dark.webp` upsampled to 2400 px, plus 4:5 and 1:1 crops; light version from `poster-light.webp`), portrait crops at 2000 px, and `jpg/` JPEG copies of project images used inside PDFs. One frame, `case/prime-minister-museum-03` (the tricolour corridor), is served by the site washed out — mean luminance 218 with a floor at 171, where every other case frame sits at 40–150 — so `common.TONE_FIX` restores it with linear levels (black point to the veil floor, gamma 1.15, 0.4 px blur against banding; no retouching) in every derived copy (`jpg/`, `Presentations/src/assets/`). Replace both copies with the original render when the client supplies it. |
| `icons/` | monoline arrow icons (round-capped line, gold point of light at the tail; drawn independently of the logo); `--white` and `--soot` variants |
| `fonts-static/` | static instances (Fraunces Light + Italic, Inter Tight SemiBold / Medium, Inter Regular / Medium / Italic) made from the variable fonts in `04_TYPOGRAPHY` with fontTools, for Office documents (PPTX/DOCX name fonts by instance). OFL licences included. |
| `build/` | generators: `brandcopy.py` (all approved copy), `common.py` (paths, render/print helpers, `jimg`), `render_batch.js` (same as `render.js`, many jobs per browser), `build_*.py` one per subfolder, `pptx_kit.py` (brand on slides), `docstyle.py`, `manifest.py` (measures every file → `manifest.json`), `write_readmes.py` |

Rebuild everything: run each `build_*.py` from this folder, then `manifest.py` and `write_readmes.py`.
"""
    open(f"{MC}/_shared/README.md", "w", encoding="utf-8").write(shared)
    tot = sum(r["bytes"] for r in MAN)
    top = f"""# 10_MARKETING_COLLATERAL — the integrated marketing identity

Campaign idea carried through every piece: **Carry the light across.** — a single lit object (the point-of-light object from the site hero) or a single lit room on black; headline in Fraunces 300 ending with a full stop, where the stop is the one gold point; wall-label captions (Title · Place); the primary wordmark; `sanzeed.com`.

{HEAD}

| Folder | Contents |
|---|---|
| `Campaign_Templates/` | 3 key visuals × 3 ratios, 7 digital ads (IAB + 1080² social), 4 web banners (1920×600, 1440×500; dark + light) |
| `Events/` | invitation (A5 print, 1080×1350, 600×800), backdrop, welcome board, name badges, lanyard, table tent, roll-up, booth wall |
| `Signage/` | door plate, 4 arrow plates + 4 room numbers, totem, window vinyl (+ cut file), spec sheet |
| `Posters/` | campaign, method and typographic posters at A2 and A3 |
| `Flyers/` | A5 two-sided flyer, DL leaflet |
| `Brochures/` | A4 trifold, 12-page company profile |
| `Media_Kit/` | 7-page media kit PDF, contents list |
| `Presentations/` | 16-slide sales deck, 12-slide proposal template (PPTX), case-study template (filled + blank), portfolio template |
| `Press/` | press-release template + sample, fact sheet (DOCX), headshots, logo-pack note, About one-pager |
| `_shared/` | collateral.css, derived images, arrow icons, static fonts for Office, build scripts, `build/manifest.json` |

Every export has an editable source beside it (`src/*.html`, `.pptx`, `.docx`); each subfolder’s `README.md` lists every file with its measured spec and the command to re-export it. Print-ready PDFs (`-print-ready-cmyk.pdf`) carry crop marks, trim and bleed boxes and CMYK conversion from `print_pdf.py` — proof gold on the chosen stock before a run. Total size of this folder: {tot/1e6:.0f} MB, {len(MAN)} files.

**Known limitations.** Source imagery is the site's 960×540 / 1600×900 renders and the 1100 px portrait, so large-format print (A2 poster plate, 1:10 backdrops) is below 300 dpi — supply higher-resolution originals for press. The 12-page profile holds the three case studies as spreads by merging the three pillars into the About page and the galleries, journey and contact onto page 12. Office documents need the static fonts in `_shared/fonts-static/` installed to show Fraunces Light and Inter Tight SemiBold. The Prime Minister Museum corridor frame (`case/prime-minister-museum-03`) is served by the site washed out; every piece that shows it (walk-into key visuals, sales deck 09, proposal 11, case-study and portfolio templates, trifold, profile p06) uses a levels-restored copy made by `_shared/build/common.py` (`TONE_FIX`) — swap in the original render when supplied.
"""
    open(f"{MC}/README.md", "w", encoding="utf-8").write(top); print("wrote top README")
