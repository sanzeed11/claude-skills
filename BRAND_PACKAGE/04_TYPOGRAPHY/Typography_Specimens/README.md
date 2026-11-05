# 04_TYPOGRAPHY / Typography_Specimens — the type system on paper

Ten A4 specimen sheets for the three brand families (Fraunces · Inter Tight · Inter), each delivered as an editable
HTML source, a vector PDF and a 2× PNG preview, plus `type-scale.css`, a stepped export of the scale. Every sheet is set
with the brand kit itself (`brand.css` + the shared document stylesheet `doc.css`), so the specimens *are* the system,
not pictures of it. All copy is confirmed brand copy (headline bank, service lines, the three case studies on sanzeed.com);
amounts the client must supply are shown as bracketed fields (`[Fee]`, `[GSTIN]`), never invented values.

## Files

| File | Format · spec | What it shows |
|---|---|---|
| `sanzeed-type-specimen--fraunces.pdf` / `-1.png`, `-2.png` | PDF 2 pages A4 · PNG 1587 × 2246 px (2×) | Fraunces: display line at 300/opsz 144, the 100–900 weight range with 300 marked as the only weight in use, opsz 36/72/144 compared at one size, headline mechanics (.lit / .dim); page 2: italic pull quote, SOFT and WONK axes, stat numerals with the gold plus, the rules, the character set |
| `sanzeed-type-specimen--inter-tight.pdf` / `.png` | PDF 1 page · PNG 1588 × 2246 | Inter Tight weights 400–800 with their roles, caps tracking (0 / +0.08 / +0.12 em) and heading tracking (−0.01 em), eyebrows, counters, wall-label title |
| `sanzeed-type-specimen--inter.pdf` / `.png` | PDF 1 page · PNG 1588 × 2246 | Inter 400/500/600 with confirmed copy, optical size 14 vs 32, proportional vs tabular numerals side by side, the 66-character measure |
| `sanzeed-type-hierarchy.pdf` / `-1.png` … `-3.png` | PDF 3 pages · PNG | display-1 … counter at true desktop pixel size, each set in a line from the headline bank, labelled with family, weight, size, line height, tracking and use |
| `sanzeed-type-responsive-scale.pdf` / `-1.png`, `-2.png` | PDF 2 pages · PNG | the desktop / tablet / mobile table from `typography-tokens.json` with proportional device columns; page 2 the print scale in points at true size |
| `sanzeed-type-pairing.pdf` / `.png` | PDF 1 page · PNG | a case-study page composition (Prime Minister Museum) with callouts naming the token of every line |
| `sanzeed-type-numbers-data.pdf` / `.png` | PDF 1 page · PNG | the four stats, a quotation table (bracketed fees), the enquiry-form budget bands, gallery counts, the career timeline as points on a beam, dash / currency / counter rules |
| `sanzeed-type-editorial.pdf` / `.png` | PDF 1 page · PNG | the Ram Katha Show case study in the editorial style (Fraunces 300, opsz 36, 11 pt / 1.6) with a serif pull quote and two wall-labelled figures |
| `sanzeed-type-character-set.pdf` / `.png` | PDF 1 page · PNG | A–Z, a–z, three numeral styles, punctuation, currency, arrows (Inter families; Fraunces has none) and diacritics for all four faces |
| `sanzeed-type-ui.pdf` / `.png` | PDF 1 page · PNG | the same UI components in the dark gallery and the light label: navigation, buttons, card with wall label, focused field, tags, eyebrow + headline |
| `type-scale.css` | CSS · 8 KB | the scale as classes: `.ts-<token>` (desktop values, tablet ≤ 1023 px, mobile ≤ 639 px via media queries) and `.tp-<token>` print sizes in pt. `brand.css` already provides the fluid `clamp()` versions as `.t-<token>`; use this file where clamp() is unavailable (email, office tools, hand-off) or exact breakpoint values are required. Generated from `typography-tokens.json` |
| `render.sh` | shell | rebuilds the HTML and renders every sheet to PDF + PNG |
| `src/build_specimens.py` | Python · the master | writes all ten HTML sheets and `type-scale.css` from `typography-tokens.json`; the copy and layout of every sheet live here |
| `src/sanzeed-type-*.html` | HTML · 10 files | the generated sheets — open in a browser, or edit directly if you prefer not to touch Python |

PDF pages are 210 × 297 mm with all three fonts embedded (Chromium subsets the variable fonts; `pdffonts` lists
Fraunces instances as "Fraunces-9ptBlack" — that is the variable font's internal default-instance name, the glyphs are Light 300).
PNGs are the page at 2× (794 × 1123 CSS px → 1588 × 2246 px); multi-page sheets have one PNG per page, rendered from the PDF at 192 dpi.

## How to edit

1. Edit `src/build_specimens.py` (copy, samples, sheet structure) — or the generated HTML in `src/` for a one-off change.
2. Run `./render.sh` (from any directory). It runs the builder, then for every sheet:
   `node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/<sheet>.html --out <sheet>.pdf --pdf --size 210x297`
   and the PNG (`--selector ".page" --width 794 --height 1123 --scale 2`, or `pdftoppm -r 192` for multi-page sheets).
3. To change sizes or rules, edit `../typography-tokens.json` first — the hierarchy, responsive-scale and rules content, and `type-scale.css`, are read from it.

Page model, footer, print sizes: `15_SOURCE_FILES/Project_Files/brand-kit/doc.css` (shared by every A4 document in the package).
Fonts: `../Font_Files/`, SIL OFL 1.1 — see `../Font_Licensing.md`.
