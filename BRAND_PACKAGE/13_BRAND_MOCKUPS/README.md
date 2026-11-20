# 13_BRAND_MOCKUPS — the identity, applied

35 premium application mockups of the finished Sanzeed identity, the way the agency shows it at final delivery:
logo finishes, stationery, digital surfaces and marketing applications. Every scene is built from the **real deliverables of the
other folders** — logos from `02_LOGO_SYSTEM`, textures from `05_GRAPHIC_ASSETS/Textures`, print pieces from `09_PRINT_STATIONERY`
and `10_MARKETING_COLLATERAL`, social from `08_SOCIAL_MEDIA`, share images / email / app icons from `07_WEBSITE_DIGITAL_ASSETS`,
the live site from `16_WEBSITE_IMPLEMENTATION`, motion frames from `11_MOTION_GRAPHICS`, photography from `06_PHOTOGRAPHY_ART_DIRECTION`
and `00_ORIGINAL_ASSETS_BACKUP`. Nothing is redrawn or restyled; the scenes only light, bend, reflect and place them.

**Logo.** Every scene carries the approved master logo (20 Nov 2026): the **refined original wordmark, option B** — the client's own
hand-drawn SANZEED with the hooked S, the swooping N, and a Z whose diagonal swoops like the N's right leg; **three gold points**
(A, Z, D), the Z point inside a thin ring that shows the background through it. The symbol is the refined, hooked S with its full stop;
the monogram is "SM." (on the ID-card reverse). All 35 scenes and their plates were regenerated from the rebuilt upstream folders on
20 Nov 2026. The masked finishes size their boxes to the production SVGs' proportions: wordmark 3692.52 × 519.33 (≈ 7.11 : 1),
symbol 603.82 × 519.33 (≈ 1.16 : 1).

| Folder | Contents |
|---|---|
| `Logo_Mockups/` | 7 scenes: blind deboss, gold foil, halo-lit signage, engraved brass plaque, window vinyl on a frosted door, app icon, favicon |
| `Stationery_Mockups/` | 9 scenes: cards fanned, cards flat lay, letterhead + envelope + card, proposal cover, ID card and lanyard, thank-you card, stamp impression, notepad, presentation folder |
| `Digital_Mockups/` | 9 scenes: website on a laptop (dark, light), website on a phone, Instagram profile, LinkedIn profile, email signature, link preview in chat, YouTube channel, presentation on a conference screen |
| `Marketing_Mockups/` | 10 scenes: A2 poster on a gallery wall, trifold, roll-up at an entrance, door plate + wayfinding (composite), totem in a lobby (composite), event backdrop at the G20-style show (composite), flyer in hand, social ad, lower third over the Ram Katha Show, logo reveal on a cinema screen |
| `sanzeed-mockups-contact-sheet.png` | all 35 scenes on one 3000 px sheet, numbered 001–035 |
| `_build/` | `build_mockups.py` (the master), `mockup.css` (shared devices, surfaces, textures, shadows), `make_plates.py` + `plates/` (the deliverables re-rasterised at mockup resolution), `capture_site.js`, `contact-sheet.html` |

Each scene: **editable HTML + CSS source** in the folder's `src/` (1500 × 1000 CSS px, all brand tokens via `brand.css`), a **3000 × 2000 JPG q90** (`-3000w.jpg`) and a **1600 × 1067 web JPG** (`-1600w.jpg`). Folder total: **43 MB**.

## How the scenes are made

* **One master.** `_build/build_mockups.py` holds every scene (markup + scene CSS) and writes the `src/*.html` files, renders them with
  the brand kit's `render.js` (Chromium, 2×), exports both JPGs, the contact sheet and this README. `python3 _build/build_mockups.py`
  rebuilds everything; `python3 _build/build_mockups.py cards-fanned` rebuilds the scenes whose name contains the filter; `--html-only`
  writes sources only; `--sheet` rebuilds the contact sheet. A source can also be edited by hand and re-rendered with the command in its
  header comment.
* **Materials and light** are CSS: 3-D perspective transforms (`perspective` / `rotateX` / `rotateY`, `preserve-3d`) for cards, pages,
  panels and the composited signage; layered `box-shadow` for contact and ambient shadows; gradients for light fall-off and the
  `sweep` of a window; reflections are mirrored copies under a gradient mask; the brand **grain**, **paper** and **lamp glow**
  textures come from `05_GRAPHIC_ASSETS/Textures`. The emboss, foil and engraving use the production logo SVGs from `02_LOGO_SYSTEM`
  as CSS masks (inlined as data URIs — Chromium will not load a `mask-image` from `file://`), filled with the paper colour, the
  `--sz-gradient-foil` gradient, or the ink of the engraving.
* **Devices and windows** (phone, laptop, tablet, monitor, browser, mail and chat windows) are drawn in `mockup.css` — generic chrome,
  no third-party branding. Screens show the real site captured at device pixel density (`capture_site.js`, 1440 × 900 @ 2× and
  390 × 844 @ 3×), the real social assets, the OG image, the email signature loaded live in an iframe.
* **Plates** (`_build/plates/`, built by `make_plates.py`): the delivered PDFs of the business cards, letterhead, envelopes, thank-you
  card, notepad, ID card, proposal, presentation and folder re-rasterised with `pdftoppm` at 160–600 dpi; previews that carry bleed
  cropped back to trim; the trifold cut into its six panels; the four composite photographs upscaled to 3000 px (Lanczos + unsharp);
  the lower-third hold frame rendered from its motion source with alpha. (The stamp impression masks with the outlined stamp SVG
  from `09_PRINT_STATIONERY/Stamp` directly.) Delete the old plates and re-run `python3 _build/make_plates.py` whenever an upstream
  deliverable changes, then `python3 _build/build_mockups.py`.
* **Composites into approved imagery** (door plate / wayfinding, totem, event backdrop) place the real sign on a plane whose perspective
  matches the photograph, under a veil that keeps the plate on ≥ 80 % black, with a wall label (Title · Place) in the corner.
* **Captions.** Every scene carries a small wall-label caption (scene · spec · source folder) at the bottom-left in the brand's caption
  style; delete the `.cap` div in the source for an uncaptioned export.

## Rules applied and verified

Every render was opened and checked: the wordmark shows the three gold points with the ringed Z and the hooked S; the logo variant matches its background (`full-colour-dark` on black, `full-colour-light` on
Plaster, `white` for the vinyl and backlit letters, `black` masks for the finishes (`wordmark-plain` for the blind deboss, so no points), `symbol` on the plaque / avatars, `monogram`
only on the ID-card reverse as delivered); clear space is kept; one gold accent per composition (the deliverable's own point, or the
lamp); Fraunces 300 renders as the light serif in every caption and UI; nothing clipped, no missing fonts, no placeholder boxes;
the only copy is confirmed copy from `01_BRAND_STRATEGY`, the deliverables themselves and the site's own `<title>` / `og:` meta;
no invented statistics (the Instagram and YouTube mock profiles show no follower or view counts).

## Mockup index

| # | Scene | Deliverable used | Source (editable) | Export |
|---|---|---|---|---|
| 001 | Blind deboss · wordmark on Plaster card stock | 02 wordmark-plain--black.svg (as the deboss mask); 05 paper texture | `Logo_Mockups/src/sanzeed-mockup--logo-blind-deboss-plaster.html` | `Logo_Mockups/sanzeed-mockup--logo-blind-deboss-plaster-3000w.jpg` (286 KB) · `…-1600w.jpg` (77 KB) |
| 002 | Gold foil · wordmark hot-stamped on black stock | 02 primary-wordmark--black.svg (as the foil mask); 03 foil gradient; 05 grain | `Logo_Mockups/src/sanzeed-mockup--logo-gold-foil-black.html` | `Logo_Mockups/sanzeed-mockup--logo-gold-foil-black-3000w.jpg` (1.0 MB) · `…-1600w.jpg` (166 KB) |
| 003 | Halo-lit signage · fabricated letters on a dark wall | 02 primary-wordmark--full-colour-dark.svg; 05 lamp glow + grain | `Logo_Mockups/src/sanzeed-mockup--logo-backlit-signage-night.html` | `Logo_Mockups/sanzeed-mockup--logo-backlit-signage-night-3000w.jpg` (1.1 MB) · `…-1600w.jpg` (236 KB) |
| 004 | Engraved brass plaque · the symbol | 02 symbol--black.svg (as the engraving mask) | `Logo_Mockups/src/sanzeed-mockup--logo-brass-plaque-symbol.html` | `Logo_Mockups/sanzeed-mockup--logo-brass-plaque-symbol-3000w.jpg` (1.2 MB) · `…-1600w.jpg` (260 KB) |
| 005 | Window vinyl · wordmark on a frosted glass door | 02 primary-wordmark--white.svg (cut vinyl); 10 Signage window-vinyl spec (600 mm band, 1200 mm wordmark); 00/06 Prime Minister Museum lobby (behind the glass) | `Logo_Mockups/src/sanzeed-mockup--logo-frosted-glass-door.html` | `Logo_Mockups/sanzeed-mockup--logo-frosted-glass-door-3000w.jpg` (207 KB) · `…-1600w.jpg` (64 KB) |
| 006 | App icon · the symbol tile on a phone home screen | 07 App_Icons/iOS/ios-icon-1024.png; 05 Backgrounds lamp 1080×1920 (wallpaper) | `Logo_Mockups/src/sanzeed-mockup--logo-app-icon-phone.html` | `Logo_Mockups/sanzeed-mockup--logo-app-icon-phone-3000w.jpg` (635 KB) · `…-1600w.jpg` (133 KB) |
| 007 | Favicon · the symbol tile in a browser tab strip | 02 Favicon/favicon-32.png; 16 site capture (dark) | `Logo_Mockups/src/sanzeed-mockup--logo-favicon-browser-tab.html` | `Logo_Mockups/sanzeed-mockup--logo-favicon-browser-tab-3000w.jpg` (578 KB) · `…-1600w.jpg` (155 KB) |
| 008 | Business cards · fanned on a dark surface | 09 Business_Cards concept A + B (PDF, 600 dpi); 05 lamp glow, grain | `Stationery_Mockups/src/sanzeed-mockup--stationery-cards-fanned-dark.html` | `Stationery_Mockups/sanzeed-mockup--stationery-cards-fanned-dark-3000w.jpg` (720 KB) · `…-1600w.jpg` (148 KB) |
| 009 | Business cards · front and back, flat lay on Plaster | 09 Business_Cards concept A + B (PDF, 600 dpi); 05 paper texture | `Stationery_Mockups/src/sanzeed-mockup--stationery-cards-flat-lay-plaster.html` | `Stationery_Mockups/sanzeed-mockup--stationery-cards-flat-lay-plaster-3000w.jpg` (317 KB) · `…-1600w.jpg` (88 KB) |
| 010 | Stationery set · letterhead, DL envelope, business card | 09 Letterheads sample letter (PDF, 220 dpi); 09 Envelopes DL front + back (PDF, 300 dpi); 09 Business_Cards concept A | `Stationery_Mockups/src/sanzeed-mockup--stationery-letterhead-envelope-card.html` | `Stationery_Mockups/sanzeed-mockup--stationery-letterhead-envelope-card-3000w.jpg` (356 KB) · `…-1600w.jpg` (114 KB) |
| 011 | Proposal · cover on a desk | 09 Proposals template cover (PDF, 250 dpi); 05 lamp glow | `Stationery_Mockups/src/sanzeed-mockup--stationery-proposal-cover-desk.html` | `Stationery_Mockups/sanzeed-mockup--stationery-proposal-cover-desk-3000w.jpg` (781 KB) · `…-1600w.jpg` (163 KB) |
| 012 | ID card · on the lanyard, front and back | 09 ID_Card front + back (PDF, 600 dpi); 09 ID_Card lanyard strip | `Stationery_Mockups/src/sanzeed-mockup--stationery-id-card-lanyard.html` | `Stationery_Mockups/sanzeed-mockup--stationery-id-card-lanyard-3000w.jpg` (708 KB) · `…-1600w.jpg` (168 KB) |
| 013 | Thank-you card · open, with the signature | 09 Thank_You_Cards folded outside + inside (PDF, 300 dpi); 05 paper texture | `Stationery_Mockups/src/sanzeed-mockup--stationery-thank-you-card-open.html` | `Stationery_Mockups/sanzeed-mockup--stationery-thank-you-card-open-3000w.jpg` (280 KB) · `…-1600w.jpg` (62 KB) |
| 014 | Rubber stamp · impression in Gold Ink on the letterhead | 09 Stamp round 40 mm (outlined SVG, as the ink mask); 09 Letterheads sample letter (PDF, 220 dpi) | `Stationery_Mockups/src/sanzeed-mockup--stationery-stamp-impression.html` | `Stationery_Mockups/sanzeed-mockup--stationery-stamp-impression-3000w.jpg` (291 KB) · `…-1600w.jpg` (86 KB) |
| 015 | Notepad · A5 pad with a pen | 09 Notepad A5 (PDF, 300 dpi); 05 paper texture | `Stationery_Mockups/src/sanzeed-mockup--stationery-notepad-pen.html` | `Stationery_Mockups/sanzeed-mockup--stationery-notepad-pen-3000w.jpg` (309 KB) · `…-1600w.jpg` (75 KB) |
| 016 | Presentation folder · open, with the letterhead and card inserted | 09 Folder A4 outside (PDF, 160 dpi): front panel, pocket; 09 Letterheads sample letter; 09 Business_Cards concept A | `Stationery_Mockups/src/sanzeed-mockup--stationery-folder-open-insert.html` | `Stationery_Mockups/sanzeed-mockup--stationery-folder-open-insert-3000w.jpg` (524 KB) · `…-1600w.jpg` (117 KB) |
| 017 | Website · hero on a laptop, dark theme | 16 site capture, dark, 1440 × 900 @ 2× | `Digital_Mockups/src/sanzeed-mockup--digital-website-laptop-dark.html` | `Digital_Mockups/sanzeed-mockup--digital-website-laptop-dark-3000w.jpg` (440 KB) · `…-1600w.jpg` (115 KB) |
| 018 | Website · hero on a laptop, light theme | 16 site capture, light, 1440 × 900 @ 2× | `Digital_Mockups/src/sanzeed-mockup--digital-website-laptop-light.html` | `Digital_Mockups/sanzeed-mockup--digital-website-laptop-light-3000w.jpg` (323 KB) · `…-1600w.jpg` (96 KB) |
| 019 | Website · on a phone, dark theme | 16 site capture, mobile 390 × 844 @ 3× | `Digital_Mockups/src/sanzeed-mockup--digital-website-phone-dark.html` | `Digital_Mockups/sanzeed-mockup--digital-website-phone-dark-3000w.jpg` (740 KB) · `…-1600w.jpg` (156 KB) |
| 020 | Instagram · profile and feed grid on a phone | 08 Instagram profile 1024 (dark); 08 Instagram highlight covers ×5; 08 Instagram grid preview 3 × 3 | `Digital_Mockups/src/sanzeed-mockup--digital-instagram-feed-phone.html` | `Digital_Mockups/sanzeed-mockup--digital-instagram-feed-phone-3000w.jpg` (790 KB) · `…-1600w.jpg` (169 KB) |
| 021 | LinkedIn · personal profile with banner and avatar, on a laptop | 08 LinkedIn personal banner 1584 × 396; 08 LinkedIn profile 400 (dark) | `Digital_Mockups/src/sanzeed-mockup--digital-linkedin-profile-laptop.html` | `Digital_Mockups/sanzeed-mockup--digital-linkedin-profile-laptop-3000w.jpg` (378 KB) · `…-1600w.jpg` (122 KB) |
| 022 | Email signature · as received, in a mail window | 07 Email/email-signature.html (live, in an iframe); 07 Email signature preview copy | `Digital_Mockups/src/sanzeed-mockup--digital-email-signature-mail-window.html` | `Digital_Mockups/sanzeed-mockup--digital-email-signature-mail-window-3000w.jpg` (525 KB) · `…-1600w.jpg` (135 KB) |
| 023 | Share card · the Open Graph image in a chat link preview | 07 Open_Graph og-home 1200 × 630; 16 og:title / og:description; 02 symbol tile (avatar) | `Digital_Mockups/src/sanzeed-mockup--digital-og-card-chat-bubble.html` | `Digital_Mockups/sanzeed-mockup--digital-og-card-chat-bubble-3000w.jpg` (688 KB) · `…-1600w.jpg` (140 KB) |
| 024 | YouTube · channel page on a tablet | 08 YouTube banner 2560 × 1440 (safe band); 08 YouTube profile 800 (dark); 08 YouTube thumbnails ×3 | `Digital_Mockups/src/sanzeed-mockup--digital-youtube-channel-tablet.html` | `Digital_Mockups/sanzeed-mockup--digital-youtube-channel-tablet-3000w.jpg` (596 KB) · `…-1600w.jpg` (163 KB) |
| 025 | Presentation template · on a conference-room screen | 09 Presentation_Template slide 01 (PDF, 220 dpi) | `Digital_Mockups/src/sanzeed-mockup--digital-presentation-conference-screen.html` | `Digital_Mockups/sanzeed-mockup--digital-presentation-conference-screen-3000w.jpg` (538 KB) · `…-1600w.jpg` (116 KB) |
| 026 | Poster · A2 campaign poster on a gallery wall | 10 Posters campaign A2 (trim crop) | `Marketing_Mockups/src/sanzeed-mockup--marketing-poster-a2-gallery-wall.html` | `Marketing_Mockups/sanzeed-mockup--marketing-poster-a2-gallery-wall-3000w.jpg` (254 KB) · `…-1600w.jpg` (75 KB) |
| 027 | Brochure · A4 trifold standing, inside spread behind | 10 Brochures A4 trifold outside + inside (panels, trim crop) | `Marketing_Mockups/src/sanzeed-mockup--marketing-trifold-brochure-standing.html` | `Marketing_Mockups/sanzeed-mockup--marketing-trifold-brochure-standing-3000w.jpg` (401 KB) · `…-1600w.jpg` (107 KB) |
| 028 | Roll-up banner · at an event entrance | 10 Events exhibition roll-up 850 × 2000 mm (1:5) | `Marketing_Mockups/src/sanzeed-mockup--marketing-rollup-banner-entrance.html` | `Marketing_Mockups/sanzeed-mockup--marketing-rollup-banner-entrance-3000w.jpg` (600 KB) · `…-1600w.jpg` (130 KB) |
| 029 | Signage · door plate and wayfinding on a museum wall | 10 Signage door plate 300 × 100 + arrow plate (trim crop); 06 Prime Minister Museum corridor (approved image) | `Marketing_Mockups/src/sanzeed-mockup--marketing-door-plate-wayfinding-museum-wall.html` | `Marketing_Mockups/sanzeed-mockup--marketing-door-plate-wayfinding-museum-wall-3000w.jpg` (573 KB) · `…-1600w.jpg` (177 KB) |
| 030 | Signage · totem in a museum lobby | 10 Signage totem 600 × 1800 mm (1:10); 00/06 Prime Minister Museum lobby (case image) | `Marketing_Mockups/src/sanzeed-mockup--marketing-totem-lobby.html` | `Marketing_Mockups/sanzeed-mockup--marketing-totem-lobby-3000w.jpg` (574 KB) · `…-1600w.jpg` (177 KB) |
| 031 | Event backdrop · LED wall at the G20-style show | 10 Events backdrop 3000 × 2400 mm (1:10); 06 G20 LED Show (approved image) | `Marketing_Mockups/src/sanzeed-mockup--marketing-backdrop-g20-show.html` | `Marketing_Mockups/sanzeed-mockup--marketing-backdrop-g20-show-3000w.jpg` (680 KB) · `…-1600w.jpg` (215 KB) |
| 032 | Flyer · A5 flyer in a stylised hand | 10 Flyers A5 two-sided front (trim crop) | `Marketing_Mockups/src/sanzeed-mockup--marketing-flyer-in-hand.html` | `Marketing_Mockups/sanzeed-mockup--marketing-flyer-in-hand-3000w.jpg` (735 KB) · `…-1600w.jpg` (149 KB) |
| 033 | Social ad · 1080 × 1080 ad in a feed, on a phone | 10 Campaign_Templates ad 1080 × 1080 @ 2×; 08 Instagram profile 1024 (dark) | `Marketing_Mockups/src/sanzeed-mockup--marketing-social-ad-phone.html` | `Marketing_Mockups/sanzeed-mockup--marketing-social-ad-phone-3000w.jpg` (700 KB) · `…-1600w.jpg` (146 KB) |
| 034 | Lower third · over the Ram Katha Show, on a broadcast monitor | 11 Lower_Thirds name lower third (source, hold frame at 2.9 s, alpha); 00/06 Ram Katha Show stage (case image) | `Marketing_Mockups/src/sanzeed-mockup--marketing-lower-third-ram-katha.html` | `Marketing_Mockups/sanzeed-mockup--marketing-lower-third-ram-katha-3000w.jpg` (1.1 MB) · `…-1600w.jpg` (295 KB) |
| 035 | Logo reveal · final frame on a cinema screen | 11 Logo_Animations logo reveal, dark 1920 × 1080 (poster frame) | `Marketing_Mockups/src/sanzeed-mockup--marketing-logo-reveal-cinema-screen.html` | `Marketing_Mockups/sanzeed-mockup--marketing-logo-reveal-cinema-screen-3000w.jpg` (492 KB) · `…-1600w.jpg` (109 KB) |

## Known limits

* The approved photographs exist only at 960 × 540 / 1600 × 900, so the three photo composites and the frosted-door backdrop are
  upscaled 1.9–3.1× and are deliberately softened under the veil; for press use, re-run `make_plates.py` with higher-resolution originals.
* The scenes are rendered raster scenes, not layered PSD/Figma mockup files; the HTML sources are the layered, editable equivalent
  (every object is a positioned element with its own transform and shadow).
* `brand.css` sets `img { max-width: 100% }`, so the 1780 px photographs in the door-plate, totem and event-backdrop composites are
  capped at the 1500 px stage and stop short of the right edge (a dark band there). This predates the logo swap and was left as is;
  adding `max-width:none` to those `<img>` styles would restore the intended framing (re-check the sign perspective afterwards).
* Chromium paints very large CSS background images from a low-resolution decode, so plates are kept ≤ 3400 px on the long edge
  (the A2 poster plate is 1600 px wide, 1.5× what the scene shows).
