# 10_MARKETING_COLLATERAL — the integrated marketing identity

Campaign idea carried through every piece: **Carry the light across.** — a single lit object (the point-of-light object from the site hero) or a single lit room on black; headline in Fraunces 300 ending with a full stop, where the stop is the one gold point; wall-label captions (Title · Place); the primary wordmark; `sanzeed.com`.

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM`; type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

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

Every export has an editable source beside it (`src/*.html`, `.pptx`, `.docx`); each subfolder’s `README.md` lists every file with its measured spec and the command to re-export it. Print-ready PDFs (`-print-ready-cmyk.pdf`) carry crop marks, trim and bleed boxes and CMYK conversion from `print_pdf.py` — proof gold on the chosen stock before a run. Total size of this folder: 114 MB, 402 files.

**Known limitations.** Source imagery is the site's 960×540 / 1600×900 renders and the 1100 px portrait, so large-format print (A2 poster plate, 1:10 backdrops) is below 300 dpi — supply higher-resolution originals for press. The 12-page profile holds the three case studies as spreads by merging the three pillars into the About page and the galleries, journey and contact onto page 12. Office documents need the static fonts in `_shared/fonts-static/` installed to show Fraunces Light and Inter Tight SemiBold.
