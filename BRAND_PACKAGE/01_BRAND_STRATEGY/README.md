# 01_BRAND_STRATEGY — audit, strategy, positioning, voice, messaging

Five markdown documents written from the live site (sanzeed.com, fetched 5 November 2026), and one designed A4
document, `Brand_Strategy.pdf`, that lays all five out faithfully. The markdown files are the source of truth: the PDF
is built from them at render time, so the two never drift. Everything taken from the site carries a **Confirmed** tag;
everything the agency proposes carries a **Recommendation** tag, in the document exactly as in the markdown.

## Files

| File | Format · spec | Contents |
|---|---|---|
| `Brand_Audit.md` | Markdown · 14 KB | confirmed facts (identity, services, method, timeline, portfolio, measured visual identity), strengths, weaknesses, opportunities, assumptions |
| `Brand_Strategy.md` | Markdown · 12 KB | the one idea, vision / mission / purpose, values, positioning, promise, personality, audience, differentiation, brand story, taglines, three creative routes, design principles |
| `Brand_Positioning.md` | Markdown · 4 KB | positioning statement and map, competitive frame, pillars, proof, naming rules, missing information |
| `Brand_Voice_and_Tone.md` | Markdown · 4 KB | voice principles, tone by situation, vocabulary, mechanics, three tests |
| `Brand_Messaging.md` | Markdown · 4 KB | message architecture, elevator messages, key messages by audience, headline bank, calls to action, promises, email signature |
| `Brand_Strategy.pdf` | PDF · 32 pages · A4 210 × 297 mm · ≈ 13 MB · fonts embedded | cover · contents · five sections, each with a counter opener (001–005), the tables and lists of the markdown restyled, pull quotes from confirmed copy, audit screenshots as wall-labelled figures, the positioning map as an SVG diagram, the message architecture as a beam diagram, the three creative routes as tiles (Route A built from the real wordmark and project imagery, B and C as abstract stand-ins), the [Confirmed] / [Recommendation] labels as small tags · back cover with the contact line |
| `src/Brand_Strategy.html` | HTML · 93 KB | the rendered source (opens in a browser) |
| `src/build_brand_strategy.py` | Python · the master | converts the five markdown files (tables, lists, bold, code, tags) and places each section on a page; the page plan is the list of `P.append(...)` calls near the end |
| `src/positioning-map.svg` | SVG 640 × 440 · vector, editable | the positioning map drawn from `Brand_Positioning.md`; inlined into the PDF |
| `src/figures/site-desktop-*.jpg` (9 files) · `src/figures/site-mobile-hero.jpg` | JPG q88 · 1440 px wide crops (390 px for mobile) | crops of `00_ORIGINAL_ASSETS_BACKUP/site_source/screenshot-desktop-2026-11-05.png` and `screenshot-mobile-2026-11-05.png`: hero, now-showing, services, method, galleries, about, journey, quote, contact, mobile hero. Used as the audit figures, each with a wall label (title · place · one line) |

The PDF also uses project imagery from `00_ORIGINAL_ASSETS_BACKUP/images/img/` (Prime Minister Museum, Ram Katha
Show, Buddha Park case images) with wall labels taken from the case-study pages. No stock, no placeholders.

## Regenerating

```bash
cd 01_BRAND_STRATEGY/src && python3 build_brand_strategy.py
node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in Brand_Strategy.html --out ../Brand_Strategy.pdf --pdf --size 210x297
pdftoppm -r 50 -png ../Brand_Strategy.pdf page      # look at the pages
```

- To change copy: edit the markdown, re-run. Headings, tables, numbered lists, bullets, bold, inline code and the
  `[Confirmed]` / `[Recommendation …]` labels are converted automatically.
- To move a section to another page or add a figure: edit the `P.append(page(...))` calls in `build_brand_strategy.py`;
  `S(doc, "heading prefix")` renders a markdown section, `fig(src, title, place, line)` a wall-labelled figure.
- To re-crop a screenshot: crop the source PNG and save over the JPG (keep 1440 px wide, quality 85–90). The boxes used
  (left, top, right, bottom in px of `screenshot-desktop-2026-11-05.png`): hero 0,0,1440,880 · now-showing 0,1000,1440,1860 ·
  services 0,2150,1440,2720 · method 0,7050,1440,7440 · galleries 0,10300,1440,12060 · about 0,12300,1440,13380 ·
  journey 0,13420,1440,14880 · quote 0,14900,1440,15320 · contact 0,15600,1440,16250; mobile hero 0,0,390,1000 of the mobile screenshot.
- Page model, footer and print type sizes: `15_SOURCE_FILES/Project_Files/brand-kit/doc.css`.

Contents page numbers are computed from the opener positions at build time.
