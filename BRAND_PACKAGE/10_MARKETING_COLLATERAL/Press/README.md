# Press — release template, sample release, headshots, fact sheet, logo note, About page

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM`; type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

- `sanzeed-press-release--2026-independent-practice.docx` — sample release, dated New Delhi, 5 November 2026, using only confirmed facts (dates and roles from the site timeline, the 90/60/15 numbers, the three case studies, Sanzeed’s own two quotes). PDF preview alongside.
- `sanzeed-press-release--template.docx` — the same structure with bracketed fields; boilerplate and media contact pre-filled.
- `sanzeed-fact-sheet.docx` (+ PDF) — editable fact sheet, two pages.
- `sanzeed-mirza-headshot--1x1 / 4x5 / 3x4-2000.jpg` — portrait crops at 2000 px (upsampled from the 1100 px source; request the original for print above A5).
- `logo-pack-note.md` — points to `02_LOGO_SYSTEM`; no logo files are duplicated here.
- `sanzeed-about--one-page.pdf` (+ PNG, HTML source) — one-page About Sanzeed on Plaster.

DOCX files are generated with python-docx (`_shared/build/build_press.py`): A4, 20 mm margins, logo in the header, contact in the footer; headings in Fraunces Light, labels in Inter Tight SemiBold, body in Inter. Install `_shared/fonts-static/` for Word to show the right weights.

**How to edit.** Open the DOCX in Word, or change the copy in `_shared/build/build_press.py` and re-run it (PDF previews via `soffice --headless --convert-to pdf`). About page: `src/sanzeed-about--one-page.html` → `node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-about--one-page.html --out sanzeed-about--one-page.pdf --pdf --size 210x297`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 3 KB |
| `logo-pack-note.md` | Markdown | 1 KB |
| `sanzeed-about--one-page.pdf` | 1 page · 209.9×297.0 mm · fonts embedded | 774 KB |
| `sanzeed-about--one-page.png` | 1588×2246 px | 707 KB |
| `sanzeed-fact-sheet.docx` | A4 · 6 paragraphs | 73 KB |
| `sanzeed-fact-sheet.pdf` | 2 pages · 210.0×297.0 mm · fonts embedded | 59 KB |
| `sanzeed-mirza-headshot--1x1-2000.jpg` | 2000×2000 px | 537 KB |
| `sanzeed-mirza-headshot--3x4-2000.jpg` | 2000×2667 px | 653 KB |
| `sanzeed-mirza-headshot--4x5-2000.jpg` | 2000×2500 px | 626 KB |
| `sanzeed-press-release--2026-independent-practice.docx` | A4 · 17 paragraphs | 73 KB |
| `sanzeed-press-release--2026-independent-practice.pdf` | 2 pages · 210.0×297.0 mm · fonts embedded | 53 KB |
| `sanzeed-press-release--template.docx` | A4 · 17 paragraphs | 72 KB |
| `sanzeed-press-release--template.pdf` | 1 page · 210.0×297.0 mm · fonts embedded | 50 KB |
| `src/sanzeed-about--one-page.html` | HTML source (brand.css + collateral.css) | 9 KB |
