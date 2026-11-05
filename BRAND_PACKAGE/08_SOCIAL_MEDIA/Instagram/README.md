# Instagram — Sanzeed social identity

Profile image, feed posts (1:1 and 4:5), stories, highlight covers, reel covers and a grid preview. Dark gallery by default; the 4:5 project post is the light *label* variant.

Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.

## Upload notes

- Profile: upload the 1024 master; Instagram crops it to a circle and shows 320 px — the S. tile sits centred so nothing is lost.
- Feed: 4:5 (1080×1350) is the largest the feed shows; 1:1 posts display at 1:1 in the grid. Upload PNG; Instagram recompresses to JPG itself.
- Stories / reels: keep text inside the 1080×1420 centre band (250 px free top and bottom for the UI) — every story template does, see the `--safe-zone-guide` render.
- Highlight covers: upload the 1080×1920 file as a story (archive it) and pick it as the cover; the profile shows the centre circle, where the icon is.
- Reel covers: use **Profile grid → Edit cover** and keep the default centre crop — the `--crop-guide` renders show the 4:5 feed crop and the 1:1 grid crop.

Platform sizes change: check the platform's help page before uploading (brand kit §8).

## Files

| File | Format · pixels | Size | Use | Editable from |
|---|---|---|---|---|
| `sanzeed-ig-profile--dark-320x320.png` | PNG · 320×320 px · sRGB | 4 KB | Profile image (display size), dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-ig-profile--light-320x320.png` | PNG · 320×320 px · sRGB | 4 KB | Profile image, light tile (if a light avatar is wanted) | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-ig-profile--dark-1024x1024.png` | PNG · 1024×1024 px · sRGB | 16 KB | Profile upload master, dark — upload this one | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-ig-profile--light-1024x1024.png` | PNG · 1024×1024 px · sRGB | 15 KB | Profile upload master, light | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-ig-post--project-1080x1080.png` | PNG · 1080×1080 px · sRGB | 855 KB | Square post — project with wall label (Prime Minister Museum) | `Editable_Templates/instagram/ig-post-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `sanzeed-ig-post--project--buddha-park-1080x1080.png` | PNG · 1080×1080 px · sRGB | 1.3 MB | Square post — project variant (Buddha Park) | same template, other data: see the `--js "apply({…})"` line in `render-all.sh` |
| `sanzeed-ig-post--project--yuge-yugeen-bharat-1080x1080.png` | PNG · 1080×1080 px · sRGB | 1.2 MB | Square post — project variant (Yuge Yugeen Bharat Museum) | same template, other data in `render-all.sh` |
| `sanzeed-ig-post--project--india-pavilion-1080x1080.png` | PNG · 1080×1080 px · sRGB | 1.1 MB | Square post — project variant (India Pavilion Expo 2025, concept) | same template, other data in `render-all.sh` |
| `sanzeed-ig-post--quote-1080x1080.png` | PNG · 1080×1080 px · sRGB | 491 KB | Square post — quote (Fraunces italic on the lamp) | `Editable_Templates/instagram/ig-post-quote.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `sanzeed-ig-post--quote--whole-room-1080x1080.png` | PNG · 1080×1080 px · sRGB | 462 KB | Square post — quote variant ("I lead the whole room…") | same template, other data in `render-all.sh` |
| `sanzeed-ig-post--stat-1080x1080.png` | PNG · 1080×1080 px · sRGB | 395 KB | Square post — stat "90 projects, one continuous craft." | `Editable_Templates/instagram/ig-post-stat.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `sanzeed-ig-post--announcement-1080x1080.png` | PNG · 1080×1080 px · sRGB | 942 KB | Square post — "Now showing" announcement (Ram Katha Show) | `Editable_Templates/instagram/ig-post-announcement.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `sanzeed-ig-post--announcement--g20-tree-show-1080x1080.png` | PNG · 1080×1080 px · sRGB | 851 KB | Square post — announcement variant (G20 Tree Show) | same template, other data in `render-all.sh` |
| `sanzeed-ig-portrait--project-1080x1350.png` | PNG · 1080×1350 px · sRGB | 934 KB | Portrait post — project, light label variant (Buddha Park) | `Editable_Templates/instagram/ig-portrait-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `sanzeed-ig-portrait--method-1080x1350.png` | PNG · 1080×1350 px · sRGB | 69 KB | Portrait post — method step (Step 02 Direct) | `Editable_Templates/instagram/ig-portrait-method.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. Set `step` 1–4 to light the right point on the route. |
| `sanzeed-ig-portrait--about-1080x1350.png` | PNG · 1080×1350 px · sRGB | 1.3 MB | Portrait post — about, with the approved portrait | `Editable_Templates/instagram/ig-portrait-about.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `sanzeed-ig-grid-preview--3x3-1632x1632.png` | PNG · 1632×1632 px · sRGB | 2.2 MB | Grid preview — nine posts as the profile will show them | built by `Editable_Templates/post_process.py` from the nine square renders |
| `Stories/sanzeed-ig-story--project-1080x1920.png` | PNG · 1080×1920 px · sRGB | 1.2 MB | Story — project (picture in a 5:4 room, label below) | `Editable_Templates/instagram/ig-story-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Stories/sanzeed-ig-story--project--safe-zone-guide-1080x1920.png` | PNG · 1080×1920 px · sRGB | 1.2 MB | Story — the same with the 1080×1420 centre-safe band drawn (reference only, do not upload) | same template rendered with `--js "document.documentElement.classList.add('show-guides')"` |
| `Stories/sanzeed-ig-story--quote-1080x1920.png` | PNG · 1080×1920 px · sRGB | 777 KB | Story — quote | `Editable_Templates/instagram/ig-story-quote.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Stories/sanzeed-ig-story--cta-1080x1920.png` | PNG · 1080×1920 px · sRGB | 655 KB | Story — "Tell me about the room." call (add the link sticker over the button) | `Editable_Templates/instagram/ig-story-cta.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Stories/sanzeed-ig-story--method-1080x1920.png` | PNG · 1080×1920 px · sRGB | 82 KB | Story — method step (Step 01 Discover) | `Editable_Templates/instagram/ig-story-method.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Highlight_Covers/sanzeed-ig-highlight--work-1080x1920.png` | PNG · 1080×1920 px · sRGB | 32 KB | Highlight cover — Work (doorway icon) | `Editable_Templates/instagram/ig-highlight-covers.html` (all eight icons in one file, drawn on the 24-unit monoline grid) · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Highlight_Covers/sanzeed-ig-highlight--museums-1080x1920.png` | PNG · 1080×1920 px · sRGB | 35 KB | Highlight cover — Museums | same file, `COVERS` row "museums" |
| `Highlight_Covers/sanzeed-ig-highlight--shows-1080x1920.png` | PNG · 1080×1920 px · sRGB | 34 KB | Highlight cover — Shows (projection cone) | same file, row "shows" |
| `Highlight_Covers/sanzeed-ig-highlight--method-1080x1920.png` | PNG · 1080×1920 px · sRGB | 32 KB | Highlight cover — Method (the route) | same file, row "method" |
| `Highlight_Covers/sanzeed-ig-highlight--about-1080x1920.png` | PNG · 1080×1920 px · sRGB | 37 KB | Highlight cover — About | same file, row "about" |
| `Highlight_Covers/sanzeed-ig-highlight--films-1080x1920.png` | PNG · 1080×1920 px · sRGB | 29 KB | Highlight cover — Films (clapper) | same file, row "films" |
| `Highlight_Covers/sanzeed-ig-highlight--press-1080x1920.png` | PNG · 1080×1920 px · sRGB | 30 KB | Highlight cover — Press (page, the point as its full stop) | same file, row "press" |
| `Highlight_Covers/sanzeed-ig-highlight--contact-1080x1920.png` | PNG · 1080×1920 px · sRGB | 30 KB | Highlight cover — Contact (speech bubble) | same file, row "contact" |
| `Reels/sanzeed-ig-reel-cover--project-1080x1920.png` | PNG · 1080×1920 px · sRGB | 1.3 MB | Reel cover — project film (Ram Katha Show) | `Editable_Templates/instagram/ig-reel-cover-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Reels/sanzeed-ig-reel-cover--project--crop-guide-1080x1920.png` | PNG · 1080×1920 px · sRGB | 1.3 MB | Reel cover — with the 1080×1350 feed crop and 1080×1080 grid crop drawn (reference only) | same template with the guide class |
| `Reels/sanzeed-ig-reel-cover--talk-1080x1920.png` | PNG · 1080×1920 px · sRGB | 901 KB | Reel cover — talk / method | `Editable_Templates/instagram/ig-reel-cover-talk.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh instagram`. |
| `Reels/sanzeed-ig-reel-cover--talk--crop-guide-1080x1920.png` | PNG · 1080×1920 px · sRGB | 913 KB | Reel cover — talk, crop guide (reference only) | same template with the guide class |

**34 files · 20.4 MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh instagram` (then `… post` for the profile images, grid and JPGs).
