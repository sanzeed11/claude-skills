# Patterns — seamless brand tiles

Seven tiles drawn from the graphic vocabulary (§6 of the brand kit): **dot-grid** (two densities), **beam-lines**
(hairlines with a travelling point), **arch-repeat** (the N/M doorway as a window pattern), **route** (a dotted
meander with lit rooms), **monogram-repeat** (the SM. monogram, M built from two of the wordmark's N, at 8 %), **s-curve** (the refined S's two
tapered hooks, read from the production symbol and alternated as a flowing field).
Each exists in two inks: **dark** = Gallery White + Lamp Gold on transparent (for Gallery Black, Night, Charcoal)
and **light** = Soot + Old Gold on transparent (for Plaster, Paper, Stone).

**Rule of use:** behind content at **≤ 12 % opacity** (the tiles are drawn at full strength so you can see them;
dim them in the layout, e.g. a pseudo-element with `opacity:.12`). Never on gold. One tile per composition.

| Folder / file | What it is |
|---|---|
| `src/*.svg` | the editable tiles **with the dashed gold `tile` guide rect** so the repeat boundary is obvious in Illustrator / Figma / Inkscape |
| `svg/*.svg` | clean production tiles (identical drawing, no guide) — the files `patterns.css` embeds |
| `png/*-2048.png` | 2048 × 2048 transparent PNG, the tile rendered at 2 × (1 unit = 2 px) and repeated; itself seamless |
| `patterns.css` | one class per tile (`.pat-<name>--dark` / `--light`) with the SVG as a data-URI background, `background-size` = tile size |
| `sanzeed-patterns-contact-sheet.png` | all 14 tiles repeated at 50 % on black and on Plaster (source `src/contact-sheet.html`) |
| `build_patterns.py` | **the master.** Every tile is a small drawing function; edit a number, run `python3 build_patterns.py`, and src/, svg/, png/, patterns.css and the contact sheet are regenerated |

Tile sizes (1 ×): dot-grid 256 (pitch 32 / 64), all others 512. Powers of two, so the 2048 px PNGs tile without a seam
(verified numerically: the repeated halves of every PNG differ only by anti-aliasing noise).

**Edit by hand instead:** open `src/<tile>.svg`, keep everything inside the dashed rect, save a copy without the guide layer into
`svg/`, then `python3 build_patterns.py` is still the easiest way to refresh the PNG and CSS (or re-export the PNG at 2048 px from your app).

| File | Format | Spec | Size |
|---|---|---|---|
| `build_patterns.py` | PY | Python generator | 15 KB |
| `patterns.css` | CSS | CSS | 44 KB |
| `sanzeed-patterns-contact-sheet.png` | PNG | 1920 × 1200 px | 92 KB |
| `src/contact-sheet.html` | HTML | HTML source | 4 KB |
| `png/sanzeed-pattern-*-2048.png` (14 files, e.g. `png/sanzeed-pattern-arch-repeat--dark-2048.png`) | PNG | 2048 × 2048 px · alpha | 581 KB total |
| `src/sanzeed-pattern-*.svg` (14 files, e.g. `src/sanzeed-pattern-arch-repeat--dark.svg`) | SVG | 256 × 256 units (vector) / 512 × 512 units (vector) | 44 KB total |
| `svg/sanzeed-pattern-*.svg` (14 files, e.g. `svg/sanzeed-pattern-arch-repeat--dark.svg`) | SVG | 256 × 256 units (vector) / 512 × 512 units (vector) | 40 KB total |

**46 files · 820 KB**
