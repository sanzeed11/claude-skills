# Open_Graph — share cards for every page of sanzeed.com

Open Graph / Twitter-card images at the platform size (1200×630, key content inside the centre 1200×600) and a 1200×1200 square variant for WhatsApp and LinkedIn messaging previews. Each card is rendered from an HTML source on `brand.css` + `src/og.css`; the work cards are filled from one template.

## Files

| File | Use on | Spec | Source |
|---|---|---|---|
| `sanzeed-og--default-1200x630.png` / `.jpg` | site-wide fallback (`og:image` on any page without its own card) | 1200×630, wordmark + master line on the lamp, PNG 8-bit / JPG q90 | `src/og-default.html` |
| `sanzeed-og--default-1200x1200.png` / `.jpg` | square fallback | 1200×1200 | `src/og-default.html` (square media query) |
| `sanzeed-og--home-1200x630.png` / `.jpg`, `-1200x1200` | `/` | headline + lead + orbit monoline, wordmark bottom-left | `src/og-home.html` |
| `sanzeed-og--work--prime-minister-museum-1200x630.png` / `.jpg`, `-1200x1200` | `/work/prime-minister-museum` | case image under the veil, title in Fraunces 300, place · idea line, wordmark bottom-right on ≥ 80 % black | `src/og-work--prime-minister-museum.html` (generated) |
| `sanzeed-og--work--ram-katha-show-…` | `/work/ram-katha-show` | as above | `src/og-work--ram-katha-show.html` (generated) |
| `sanzeed-og--work--buddha-park-…` | `/work/buddha-park` | as above | `src/og-work--buddha-park.html` (generated) |
| `sanzeed-og--about-1200x630.png` / `.jpg`, `-1200x1200` | `/#about` | the portrait right, “Strategy, craft and calm leadership, in one person.” left | `src/og-about.html` |
| `sanzeed-og--contact-1200x630.png` / `.jpg`, `-1200x1200` | `/#contact` | “Tell me about the room.” + the confirmed contact details | `src/og-contact.html` |
| `src/og-work--template.html` | the template for any new case study | fields `{{IMAGE}} {{CATEGORY}} {{TITLE}} {{PLACE}} {{LINE}} {{SLUG}}` | edit the layout here, not in the generated files |
| `src/og.css` | shared layout, landscape + square (`@media (max-aspect-ratio: 1.3/1)`) | | |
| `build_og.py` | fills the template, renders both sizes with `render.js`, writes the JPGs | `python3 build_og.py` (~1 min) | |

JPGs are q90, 4:4:4; use them where a platform caps file size (X, WhatsApp), PNG elsewhere.

## Adding a work card

Add a line to the `WORK` list in `build_og.py`: slug, a case image from `00_ORIGINAL_ASSETS_BACKUP/images/img/case/` (1600×900), category, title, place and the “idea” line from the case study. Run the script. Dark, low-contrast frames carry type best; the veil darkens the lower half to ≥ 80 % black for the wordmark.

## Head tags

```html
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sanzeed">
<meta property="og:title" content="Sanzeed Mirza — Experiential Design Consultant">
<meta property="og:description" content="Sanzeed Mirza directs museums, experience centres, pavilions, memorials and projection shows for institutions and brands. New Delhi.">
<meta property="og:url" content="https://sanzeed.com/">
<meta property="og:image" content="https://sanzeed.com/og/sanzeed-og--home-1200x630.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Experiential design you can walk into. — Sanzeed">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://sanzeed.com/og/sanzeed-og--home-1200x630.png">
```
Per page swap `og:image` (and `og:title`/`og:description`) for the matching card: `home` on `/`, `work--<slug>` on each case study, `about` and `contact` on those sections if they become pages, `default` everywhere else. A second `og:image` pointing at the `-1200x1200` file lets WhatsApp pick the square.
