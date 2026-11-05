# X — Sanzeed social identity

Profile image, header (with the avatar-overlap guide) and three 16:9 post images.

Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.

## Upload notes

- Header: 1500×500, ≤ 5 MB. The avatar overlaps the bottom-left (about 400×200 at this scale): the copy sits right of x = 520 (see the `--avatar-guide` render). Upload the JPG if the PNG is over the limit.
- Post images: 1600×900 (16:9) shows uncropped in the timeline; ≤ 5 MB.
- Profile image: 400×400, ≤ 2 MB, shown as a circle.

Platform sizes change: check the platform's help page before uploading (brand kit §8).

## Files

| File | Format · pixels | Size | Use | Editable from |
|---|---|---|---|---|
| `sanzeed-x-profile--dark-400x400.png` | PNG · 400×400 px · sRGB | 5 KB | Profile image, dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-x-profile--light-400x400.png` | PNG · 400×400 px · sRGB | 5 KB | Profile image, light tile | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-x-header-1500x500.png` | PNG · 1500×500 px · sRGB | 906 KB | Header (PNG) | `Editable_Templates/x/x-header.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh x`. |
| `sanzeed-x-header-1500x500.jpg` | JPG · 1500×500 px · sRGB | 157 KB | Header (JPG q90) | written by `post_process.py` |
| `sanzeed-x-header--avatar-guide-1500x500.png` | PNG · 1500×500 px · sRGB | 928 KB | Header with the avatar overlap drawn (reference only) | same template with the guide class |
| `sanzeed-x-post--project-1600x900.png` | PNG · 1600×900 px · sRGB | 818 KB | Post image — project (Albert Hall Projection Show) | `Editable_Templates/x/x-post-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh x`. |
| `sanzeed-x-post--quote-1600x900.png` | PNG · 1600×900 px · sRGB | 559 KB | Post image — statement ("Galleries planned as a route, not a floor plan.") | `Editable_Templates/x/x-post-quote.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh x`. |
| `sanzeed-x-post--stat-1600x900.png` | PNG · 1600×900 px · sRGB | 462 KB | Post image — stat, the four proof figures | `Editable_Templates/x/x-post-stat.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh x`. |

**8 files · 3.8 MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh x` (then `… post` for the profile images, grid and JPGs).
