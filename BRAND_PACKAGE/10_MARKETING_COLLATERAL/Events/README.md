# Events — invitation, event branding, exhibition graphics

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM`; type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

**Invitation** (the event itself is a template: `[Day, date]`, `[Time]`, `[Venue]`, `[City]`, `[RSVP date]` are fields). A5 print with 3 mm bleed (page 154×216 mm, front + back), digital 1080×1350 (PNG 2× + JPG), email 600×800 (PNG 2× + JPG).

**Event branding set.** Backdrop 3000×2400 mm at 1:10 (wordmark 1800 mm wide, centre 1700 mm from the floor); welcome board 900×1800 mm at 1:10; name badge 90×60 mm (host + guest, 3 mm bleed); lanyard strip 900×20 mm at 1:1 (wordmark repeat with gold points); table tent A6 (A5 flat 148×210, fold at 105 mm, top face rotated 180°, 3 mm bleed).

**Exhibition graphics.** Roll-up banner 850×2000 mm at 1:5 (bottom 200 mm sits in the cassette — below the dashed line); booth wall panel 2400×2400 mm at 1:10.

Scaled artwork carries the scale in its name (`-1-10` = 1:10, `-1-5` = 1:5): print at 1000 % / 500 %, or ask the producer to scale to the stated real size. Print-ready files (`-print-ready-cmyk.pdf`) have crop marks, trim and bleed boxes and CMYK conversion from `print_pdf.py`; proof the gold before the run.

**How to edit.** Sources in `src/` (HTML, mm units, `@page`). Example:
```
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-event-invitation--a5-print.html --out sanzeed-event-invitation--a5-bleed.pdf --pdf --size 154x216
python3 15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py sanzeed-event-invitation--a5-bleed.pdf sanzeed-event-invitation--a5-print-ready-cmyk.pdf --trim=148x210 --bleed=3 --cmyk
```
Regenerate everything: `python3 _shared/build/build_events.py`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 5 KB |
| `sanzeed-event-backdrop--3000x2400mm-1-10.pdf` | 1 page · 299.9×239.9 mm · fonts embedded | 115 KB |
| `sanzeed-event-backdrop--3000x2400mm-1-10.png` | 3402×2724 px | 1.7 MB |
| `sanzeed-event-invitation--a5-back.png` | 1166×1634 px | 772 KB |
| `sanzeed-event-invitation--a5-bleed.pdf` | 2 pages · 154.2×215.9 mm · fonts embedded | 381 KB |
| `sanzeed-event-invitation--a5-front.png` | 1166×1634 px | 308 KB |
| `sanzeed-event-invitation--a5-print-ready-cmyk.pdf` | 2 pages · 174.0×236.0 mm · fonts embedded | 520 KB |
| `sanzeed-event-invitation--digital-1080x1350.jpg` | 1080×1350 px | 109 KB |
| `sanzeed-event-invitation--digital-2160x2700.png` | 2160×2700 px | 1.1 MB |
| `sanzeed-event-invitation--email-1200x1600.png` | 1200×1600 px | 446 KB |
| `sanzeed-event-invitation--email-600x800.jpg` | 600×800 px | 52 KB |
| `sanzeed-event-lanyard--900x20mm.pdf` | 1 page · 899.9×20.1 mm · fonts embedded | 9 KB |
| `sanzeed-event-lanyard--900x20mm.png` | 6804×152 px | 32 KB |
| `sanzeed-event-name-badge--90x60mm-bleed.pdf` | 2 pages · 95.9×66.0 mm · fonts embedded | 37 KB |
| `sanzeed-event-name-badge--90x60mm-print-ready-cmyk.pdf` | 2 pages · 116.0×86.0 mm · fonts embedded | 38 KB |
| `sanzeed-event-name-badge--guest.png` | 1452×1000 px | 37 KB |
| `sanzeed-event-name-badge--host.png` | 1452×1000 px | 49 KB |
| `sanzeed-event-table-tent--a6-bleed.pdf` | 1 page · 154.2×215.9 mm · fonts embedded | 44 KB |
| `sanzeed-event-table-tent--a6-flat.png` | 1166×1634 px | 85 KB |
| `sanzeed-event-table-tent--a6-print-ready-cmyk.pdf` | 1 page · 174.0×236.0 mm · fonts embedded | 43 KB |
| `sanzeed-event-welcome-board--900x1800mm-1-10.pdf` | 1 page · 90.0×179.9 mm · fonts embedded | 301 KB |
| `sanzeed-event-welcome-board--900x1800mm-1-10.png` | 1364×2724 px | 1.0 MB |
| `sanzeed-exhibition-booth-wall--2400x2400mm-1-10.pdf` | 1 page · 239.9×239.9 mm · fonts embedded | 330 KB |
| `sanzeed-exhibition-booth-wall--2400x2400mm-1-10.png` | 2724×2724 px | 1.1 MB |
| `sanzeed-exhibition-rollup--850x2000mm-1-5.pdf` | 1 page · 170.0×400.0 mm · fonts embedded | 251 KB |
| `sanzeed-exhibition-rollup--850x2000mm-1-5.png` | 1929×4536 px | 925 KB |
| `src/sanzeed-event-backdrop--3000x2400mm-1-10.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-event-invitation--a5-print.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-event-invitation--digital-1080x1350.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-event-invitation--email-600x800.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-event-lanyard--900x20mm.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-event-name-badge--90x60mm-print.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-event-table-tent--a6-print.html` | HTML source (brand.css + collateral.css) | 3 KB |
| `src/sanzeed-event-welcome-board--900x1800mm-1-10.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-exhibition-booth-wall--2400x2400mm-1-10.html` | HTML source (brand.css + collateral.css) | 3 KB |
| `src/sanzeed-exhibition-rollup--850x2000mm-1-5.html` | HTML source (brand.css + collateral.css) | 4 KB |
