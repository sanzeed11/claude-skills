# 04_TYPOGRAPHY — Fraunces · Inter Tight · Inter

The type system of the Sanzeed identity: the font files, the scale tokens, the licence, ten specimen sheets and a
20-page Font Reference that combines them with the rules.

## Files

| File | Format · spec | Use / how to edit |
|---|---|---|
| `Font_Reference.pdf` | PDF · 20 pages · A4 210 × 297 mm · ≈ 5 MB · fonts embedded | The one document to hand to a designer or developer: cover, contents, the three families, every specimen sheet, the eight rules from `typography-tokens.json` with do / don't tiles, and the SIL OFL licensing summary. Source: `src/Font_Reference.html` |
| `src/Font_Reference.html` | HTML | the rendered source (opens in any browser); regenerate with `src/build_font_reference.py` |
| `src/build_font_reference.py` | Python · the master | assembles the document from the specimen sheets in `Typography_Specimens/src/`, `typography-tokens.json` (rules) and `Font_Licensing.md`. Edit the cover, overview, rules and licensing pages here; edit specimen pages in `Typography_Specimens/src/build_specimens.py` |
| `Typography_Specimens/` | HTML + PDF + PNG × 10 sheets, `type-scale.css`, `render.sh` | see `Typography_Specimens/README.md` |
| `typography-tokens.json` | JSON · 8 KB | the scale: px per breakpoint (desktop / tablet / mobile), print sizes in pt, the eight rules. Source of truth for `brand.css`, `type-scale.css`, `doc.css` and every sheet |
| `Font_Licensing.md` | Markdown | licence summary (SIL OFL 1.1), designers, sources, obligations, fallback stacks |
| `Font_Files/Fraunces/` | `Fraunces[SOFT,WONK,opsz,wght].ttf`, italic TTF, `*-variable.woff2`, `OFL.txt` | install the TTFs for desktop work; the woff2 subsets are for the website |
| `Font_Files/Inter/` | `Inter[opsz,wght].ttf`, italic, woff2, `OFL.txt` | text and UI sans |
| `Font_Files/Inter_Tight/` | `InterTight[wght].ttf`, italic, woff2, `OFL.txt` | headings, labels, eyebrows, data |

## Regenerating the Font Reference

```bash
cd 04_TYPOGRAPHY/Typography_Specimens && ./render.sh            # rebuild + render the ten sheets
cd ../src && python3 build_font_reference.py                      # assemble Font_Reference.html
node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in Font_Reference.html --out ../Font_Reference.pdf --pdf --size 210x297
```

Preview any page: `pdftoppm -r 60 -f 3 -l 3 -png Font_Reference.pdf page`.

## Where the rules are applied

- `15_SOURCE_FILES/Project_Files/brand-kit/brand.css` — `.t-display-1 … .t-stat` fluid classes, fonts via `@font-face` (woff2, local() first).
- `15_SOURCE_FILES/Project_Files/brand-kit/doc.css` — the shared A4 document stylesheet: print sizes (`.doc-title` 28 pt, `.doc-h2` 18 pt, `.doc-h3` 11 pt, body 10 pt, `.doc-small` 8.5 pt, `.doc-caption` 7.5 pt, `.eyebrow` 7 pt caps, `table.doc` with tabular numerals), page model, running footer.
- `Typography_Specimens/type-scale.css` — stepped `.ts-*` screen classes and `.tp-*` print classes.
