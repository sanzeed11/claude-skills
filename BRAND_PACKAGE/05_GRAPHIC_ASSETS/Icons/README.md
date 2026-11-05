# Icons — 54 icons, one line

**Grid 24 px · stroke 1.5 px · round caps and joins · no fills** except the brand point (a filled dot). Drawn, not taken from
a stock set, in the same monoline grammar as the logo and the illustrations.

* **contact (8):** mail, phone, whatsapp, linkedin, location, calendar, clock, globe
* **ui (31):** arrow-left/right/up/down, chevron-left/right/up/down, close, menu, search, filter, grid, list, play, pause, sun, moon,
  external-link, download, upload, check, info, warning, error, plus, minus, copy, share, zoom-in, zoom-out
* **domain (15):** museum, pavilion, projection, light-beam, route, doorway, stage, screen, ar-vr, team, script, drawing, film, award, book

| Folder / file | What |
|---|---|
| `svg/sanzeed-icon-<name>.svg` | one icon per file, `stroke="currentColor"` — on the web it takes the text colour. Size with CSS (`width:24px`), never change the stroke |
| `sanzeed-icons-sprite.svg` | all icons as `<symbol id="icon-<name>">`; inline once, then `<svg class="icon"><use href="#icon-mail"/></svg>` |
| `png/dark/48`, `png/dark/96` | PNG in **dark ink** Gallery White `#F5F5F7` (for black / Night / Charcoal), 48 and 96 px, transparent |
| `png/light/48`, `png/light/96` | PNG in **light ink** Soot `#1A1816` (for Plaster / Paper / Stone) |
| `icons.html` + `sanzeed-icons-sheet.png` | the preview sheet, both inks (1920 px wide) |
| `build_icons.py` | **the master**: every icon is one line of path data in `ICONS`; add or edit a line and run `python3 build_icons.py` |

Colour: icons are single-colour. When the icon's point is the only accent in the composition it may be set gold (class `.pt` in the
light-beam, route and stage icons; `fill:#E9B25A` on dark, `#B8863B` on light). Tap targets ≥ 44 px.

| File | Format | Spec | Size |
|---|---|---|---|
| `build_icons.py` | PY | Python generator | 10 KB |
| `icons.html` | HTML | HTML source | 22 KB |
| `sanzeed-icons-sheet.png` | PNG | 1920 × 1230 px | 158 KB |
| `sanzeed-icons-sprite.svg` | SVG | 24 × 24 units (vector) | 7 KB |
| `png/dark/48/sanzeed-icon-*--dark-48.png` (54 files, e.g. `png/dark/48/sanzeed-icon-ar-vr--dark-48.png`) | PNG | 48 × 48 px · alpha | 42 KB total |
| `png/dark/96/sanzeed-icon-*--dark-96.png` (54 files, e.g. `png/dark/96/sanzeed-icon-ar-vr--dark-96.png`) | PNG | 96 × 96 px · alpha | 81 KB total |
| `png/light/48/sanzeed-icon-*--light-48.png` (54 files, e.g. `png/light/48/sanzeed-icon-ar-vr--light-48.png`) | PNG | 48 × 48 px · alpha | 47 KB total |
| `png/light/96/sanzeed-icon-*--light-96.png` (54 files, e.g. `png/light/96/sanzeed-icon-ar-vr--light-96.png`) | PNG | 96 × 96 px · alpha | 87 KB total |
| `svg/sanzeed-icon-*.svg` (54 files, e.g. `svg/sanzeed-icon-ar-vr.svg`) | SVG | 24 × 24 units (vector) | 17 KB total |

**274 files · 471 KB**
