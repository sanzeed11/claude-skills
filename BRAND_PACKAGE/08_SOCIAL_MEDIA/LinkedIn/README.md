# LinkedIn — Sanzeed social identity

Personal profile image and banner (with the avatar-overlap guide), company logo and banner, six post images and the five-page document carousel for the Prime Minister Museum case study.

Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.

## Upload notes

- Personal banner: 1584×396, ≤ 8 MB. On desktop the profile photo overlaps the bottom-left; the copy sits right of x = 520 and the bottom-left 440×220 is empty (see the `--avatar-guide` render).
- Company banner: 1128×191; the company logo overlaps the bottom-left on desktop, so the wordmark sits left-centre and the line right.
- Post images: 1200×627 (1.91:1) or 1080×1080; LinkedIn shows the square larger in the feed.
- Document carousel: upload `Carousel/…pdf` as a *Document* post (PDF, ≤ 100 MB, ≤ 300 pages); LinkedIn renders each page as a swipeable card. The page PNGs are previews and can be posted as an image carousel instead.
- Profile image: 400×400 minimum; the company logo 300×300.

Platform sizes change: check the platform's help page before uploading (brand kit §8).

## Files

| File | Format · pixels | Size | Use | Editable from |
|---|---|---|---|---|
| `sanzeed-li-profile--dark-400x400.png` | PNG · 400×400 px · sRGB | 5 KB | Personal profile image, dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-li-profile--light-400x400.png` | PNG · 400×400 px · sRGB | 5 KB | Personal profile image, light tile | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-li-company-logo--dark-300x300.png` | PNG · 300×300 px · sRGB | 7 KB | Company page logo, dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-li-company-logo--light-300x300.png` | PNG · 300×300 px · sRGB | 7 KB | Company page logo, light | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-li-banner--personal-1584x396.png` | PNG · 1584×396 px · sRGB | 422 KB | Personal banner (PNG) | `Editable_Templates/linkedin/li-banner-personal.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-banner--personal-1584x396.jpg` | JPG · 1584×396 px · sRGB | 57 KB | Personal banner (JPG q90) | written by `post_process.py` |
| `sanzeed-li-banner--personal--avatar-guide-1584x396.png` | PNG · 1584×396 px · sRGB | 452 KB | Personal banner with the avatar overlap drawn (reference only) | same template with the guide class |
| `sanzeed-li-banner--company-1128x191.png` | PNG · 1128×191 px · sRGB | 96 KB | Company banner (PNG) | `Editable_Templates/linkedin/li-banner-company.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-banner--company-1128x191.jpg` | JPG · 1128×191 px · sRGB | 23 KB | Company banner (JPG q90) | written by `post_process.py` |
| `sanzeed-li-post--insight-1200x627.png` | PNG · 1200×627 px · sRGB | 227 KB | Post — insight, light label variant (one observation, one image) | `Editable_Templates/linkedin/li-post-insight.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-post--project-1200x627.png` | PNG · 1200×627 px · sRGB | 854 KB | Post — project (Army Museum Abu Dhabi) | `Editable_Templates/linkedin/li-post-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-post--stat-1200x627.png` | PNG · 1200×627 px · sRGB | 256 KB | Post — stat, the four proof figures | `Editable_Templates/linkedin/li-post-stat.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-post--timeline-1200x627.png` | PNG · 1200×627 px · sRGB | 42 KB | Post — timeline "Fifteen years, one through-line." (2011 → 2026) | `Editable_Templates/linkedin/li-post-timeline.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-post--project-1080x1080.png` | PNG · 1080×1080 px · sRGB | 1.1 MB | Square post — project (India Pavilion Expo 2025, concept) | `Editable_Templates/linkedin/li-post-square-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `sanzeed-li-post--quote-1080x1080.png` | PNG · 1080×1080 px · sRGB | 478 KB | Square post — quote ("All seven, every time.") | `Editable_Templates/linkedin/li-post-square-quote.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. |
| `Carousel/sanzeed-li-carousel--prime-minister-museum-1080x1350.pdf` | PDF · 5 pages · 1080×1351 px (CSS @page) | 9.3 MB | Document carousel — Prime Minister Museum case study, 5 pages (cover · the brief · the idea · the walk & what visitors do · the call) | `Editable_Templates/linkedin/li-carousel-pm-museum.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh linkedin`. The PDF is rendered by `render.js --pdf` (CSS `@page` 1080×1350 px). |
| `Carousel/sanzeed-li-carousel--prime-minister-museum--page-1-1080x1350.png` | PNG · 1080×1350 px · sRGB | 486 KB | Carousel page 1 — cover | same template, `--selector "#p1"` |
| `Carousel/sanzeed-li-carousel--prime-minister-museum--page-2-1080x1350.png` | PNG · 1080×1350 px · sRGB | 660 KB | Carousel page 2 — the brief | same template, `--selector "#p2"` |
| `Carousel/sanzeed-li-carousel--prime-minister-museum--page-3-1080x1350.png` | PNG · 1080×1350 px · sRGB | 350 KB | Carousel page 3 — the idea | same template, `--selector "#p3"` |
| `Carousel/sanzeed-li-carousel--prime-minister-museum--page-4-1080x1350.png` | PNG · 1080×1350 px · sRGB | 473 KB | Carousel page 4 — the walk · what visitors do | same template, `--selector "#p4"` |
| `Carousel/sanzeed-li-carousel--prime-minister-museum--page-5-1080x1350.png` | PNG · 1080×1350 px · sRGB | 503 KB | Carousel page 5 — the call | same template, `--selector "#p5"` |

**21 files · 15.7 MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh linkedin` (then `… post` for the profile images, grid and JPGs).
