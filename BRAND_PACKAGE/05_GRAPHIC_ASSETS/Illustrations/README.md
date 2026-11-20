# Illustrations — the monoline brand language

Every drawing speaks the brand's monoline language: **one even stroke (64 units on the drawing grid), round caps and joins,
gold points of light** sized to the stroke (r = 0.7 × stroke, 45 units); secondary lines are 20 units; labels are the brand fonts outlined (Fraunces 300
opsz 144 for names, Inter Tight 600 letter-spaced caps for eyebrows and counters, Inter 400 for captions), so no file
depends on an installed font. **dark** ink (Gallery White / Silver / Lamp Gold) is for black backgrounds; **light** ink
(Soot / Umber / Old Gold, Gold Ink for text) is for Plaster. Export set per drawing: `svg/` (editable), `png/` (2000 px wide,
transparent) and `pdf/` (vector, Inkscape, text already outlines).

| Drawing | Files (× dark / light) | What it shows |
|---|---|---|
| **Orbit object** | `sanzeed-illustration-orbit-object--*` | a flat reading of the site's 3D hero: glass sphere, tilted gold ring (passes behind the sphere, in front below), black plinth with the pool of light, glass beads, one point of light. 2000 × 1480 |
| **Method diagram** | `sanzeed-illustration-method-diagram--*` | Discover → Direct → Craft → Deliver as four points on one beam, STEP 01–04 eyebrows, the deliverable under each ("You receive …"), the travelling point. 2400 × 760 |
| **Between two points of light** | `sanzeed-illustration-between-two-points--*` | the brief (left, low) and the visitor (right, high), one line of light between them and six fainter ways behind it — "Seven ways to carry the light across." 2400 × 1200 |
| **Museum route** | `sanzeed-illustration-museum-route--*` | plan view: eight rooms (the room shape, radius 28) numbered 001–008, doorways where the dotted route passes, a point of light in each, entry and exit. 2400 × 1560 |
| **Seven service glyphs** | `sanzeed-illustration-service-glyph-01…07-*--*` | one per service on a 128 grid (stroke 6, point r 4.2): 01 creative direction (line between two points) · 02 museum planning (route through two rooms) · 03 storytelling (a script line with three beats) · 04 spatial & branding (the threshold) · 05 events (beam onto a stage) · 06 digital ↔ physical (line through a screen, out as pixels) · 07 leadership (a ring, seven hands) |
| **Lamp** | `sanzeed-illustration-lamp--*` | the doorway arch as a shade, the point beneath it, cone and pool of light on the floor, with the gold glow. 1600 × 2000 |

**Edit:** `build_illustrations.py` is the master — each drawing is a function returning SVG; change coordinates or copy
there and run `python3 build_illustrations.py [name]` (a name filter such as `orbit` rebuilds one drawing). Or open the
SVG in any vector app: groups are named (`sphere`, `ring-front`, `rooms`, `route`, `labels` …). Exports go through the
kit's `export_svg.py` (cairosvg PNG, Inkscape PDF).

Minimum sizes: diagrams ≥ 600 px wide on screen (labels stay ≥ 12 px); glyphs ≥ 24 px (they are UI-icon scale at 32–64 px).

| File | Format | Spec | Size |
|---|---|---|---|
| `build_illustrations.py` | PY | Python generator | 16 KB |
| `pdf/sanzeed-illustration-between-two-points--dark.pdf` | PDF | 635 × 318 mm (vector PDF) | 16 KB |
| `pdf/sanzeed-illustration-between-two-points--light.pdf` | PDF | 635 × 318 mm (vector PDF) | 16 KB |
| `pdf/sanzeed-illustration-lamp--dark.pdf` | PDF | 423 × 529 mm (vector PDF) | 3 KB |
| `pdf/sanzeed-illustration-lamp--light.pdf` | PDF | 423 × 529 mm (vector PDF) | 3 KB |
| `pdf/sanzeed-illustration-method-diagram--dark.pdf` | PDF | 635 × 201 mm (vector PDF) | 85 KB |
| `pdf/sanzeed-illustration-method-diagram--light.pdf` | PDF | 635 × 201 mm (vector PDF) | 85 KB |
| `pdf/sanzeed-illustration-museum-route--dark.pdf` | PDF | 635 × 413 mm (vector PDF) | 26 KB |
| `pdf/sanzeed-illustration-museum-route--light.pdf` | PDF | 635 × 413 mm (vector PDF) | 26 KB |
| `pdf/sanzeed-illustration-orbit-object--dark.pdf` | PDF | 529 × 392 mm (vector PDF) | 32 KB |
| `pdf/sanzeed-illustration-orbit-object--light.pdf` | PDF | 529 × 392 mm (vector PDF) | 32 KB |
| `png/sanzeed-illustration-between-two-points--dark.png` | PNG | 2000 × 1000 px · alpha | 103 KB |
| `png/sanzeed-illustration-between-two-points--light.png` | PNG | 2000 × 1000 px · alpha | 102 KB |
| `png/sanzeed-illustration-lamp--dark.png` | PNG | 2000 × 2500 px · alpha | 354 KB |
| `png/sanzeed-illustration-lamp--light.png` | PNG | 2000 × 2500 px · alpha | 331 KB |
| `png/sanzeed-illustration-method-diagram--dark.png` | PNG | 2000 × 633 px · alpha | 88 KB |
| `png/sanzeed-illustration-method-diagram--light.png` | PNG | 2000 × 633 px · alpha | 89 KB |
| `png/sanzeed-illustration-museum-route--dark.png` | PNG | 2000 × 1300 px · alpha | 73 KB |
| `png/sanzeed-illustration-museum-route--light.png` | PNG | 2000 × 1300 px · alpha | 74 KB |
| `png/sanzeed-illustration-orbit-object--dark.png` | PNG | 2000 × 1480 px · alpha | 131 KB |
| `png/sanzeed-illustration-orbit-object--light.png` | PNG | 2000 × 1480 px · alpha | 133 KB |
| `svg/sanzeed-illustration-between-two-points--dark.svg` | SVG | 2400 × 1200 units (vector) | 53 KB |
| `svg/sanzeed-illustration-between-two-points--light.svg` | SVG | 2400 × 1200 units (vector) | 53 KB |
| `svg/sanzeed-illustration-lamp--dark.svg` | SVG | 1600 × 2000 units (vector) | 2 KB |
| `svg/sanzeed-illustration-lamp--light.svg` | SVG | 1600 × 2000 units (vector) | 2 KB |
| `svg/sanzeed-illustration-method-diagram--dark.svg` | SVG | 2400 × 760 units (vector) | 296 KB |
| `svg/sanzeed-illustration-method-diagram--light.svg` | SVG | 2400 × 760 units (vector) | 296 KB |
| `svg/sanzeed-illustration-museum-route--dark.svg` | SVG | 2400 × 1560 units (vector) | 94 KB |
| `svg/sanzeed-illustration-museum-route--light.svg` | SVG | 2400 × 1560 units (vector) | 94 KB |
| `svg/sanzeed-illustration-orbit-object--dark.svg` | SVG | 2000 × 1480 units (vector) | 2 KB |
| `svg/sanzeed-illustration-orbit-object--light.svg` | SVG | 2000 × 1480 units (vector) | 2 KB |
| `pdf/sanzeed-illustration-service-glyph-*.pdf` (14 files, e.g. `pdf/sanzeed-illustration-service-glyph-01-experiential-design--dark.pdf`) | PDF | 34 × 34 mm (vector PDF) | 19 KB total |
| `png/sanzeed-illustration-service-glyph-*.png` (14 files, e.g. `png/sanzeed-illustration-service-glyph-01-experiential-design--dark.png`) | PNG | 2000 × 2000 px · alpha | 933 KB total |
| `svg/sanzeed-illustration-service-glyph-*.svg` (14 files, e.g. `svg/sanzeed-illustration-service-glyph-01-experiential-design--dark.svg`) | SVG | 128 × 128 units (vector) | 16 KB total |

**73 files · 3.6 MB**
