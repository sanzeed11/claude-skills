# Facebook — Sanzeed social identity

Page profile image, page cover (with its centre-safe guide), two post images and an event cover.

Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.

## Upload notes

- Profile: upload the 720 file; it shows at 170 px on desktop and 128 px on phones, cropped to a circle.
- Cover: desktop shows 820×312, phones crop the sides to the centre 1250×463 — all copy sits inside that band (see the `--safe-zone-guide` render). Facebook loads sRGB JPGs under 100 KB fastest: the `.jpg` (q90) is beside the PNG.
- Event cover: 1920×1005; some feeds crop it to 16:9, so the copy stays left-centre. The sample is filled with the Prime Minister Museum; replace title / place / `[Date and time]` per event.
- Post images: 1200×630 is also the link-preview size; the feed shows them at 1.91:1.

Platform sizes change: check the platform's help page before uploading (brand kit §8).

## Files

| File | Format · pixels | Size | Use | Editable from |
|---|---|---|---|---|
| `sanzeed-fb-profile--dark-320x320.png` | PNG · 320×320 px · sRGB | 4 KB | Profile image (display size), dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-fb-profile--light-320x320.png` | PNG · 320×320 px · sRGB | 4 KB | Profile image, light tile | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-fb-profile--dark-720x720.png` | PNG · 720×720 px · sRGB | 18 KB | Profile upload master, dark — upload this one | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-fb-profile--light-720x720.png` | PNG · 720×720 px · sRGB | 18 KB | Profile upload master, light | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-fb-cover-1640x624.png` | PNG · 1640×624 px · sRGB | 674 KB | Page cover (PNG) | `Editable_Templates/facebook/fb-cover.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh facebook`. |
| `sanzeed-fb-cover-1640x624.jpg` | JPG · 1640×624 px · sRGB | 77 KB | Page cover (JPG q90, the one to upload) | written by `post_process.py` from the PNG |
| `sanzeed-fb-cover--safe-zone-guide-1640x624.png` | PNG · 1640×624 px · sRGB | 603 KB | Page cover with the 1250×463 centre-safe area drawn (reference only) | same template with the guide class |
| `sanzeed-fb-post--project-1200x630.png` | PNG · 1200×630 px · sRGB | 866 KB | Post image — project (Yuge Yugeen Bharat Museum) | `Editable_Templates/facebook/fb-post-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh facebook`. |
| `sanzeed-fb-post--quote-1200x630.png` | PNG · 1200×630 px · sRGB | 311 KB | Post image — quote | `Editable_Templates/facebook/fb-post-quote.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh facebook`. |
| `sanzeed-fb-event-cover-1920x1005.png` | PNG · 1920×1005 px · sRGB | 1.4 MB | Event cover (PNG) | `Editable_Templates/facebook/fb-event-cover.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh facebook`. |
| `sanzeed-fb-event-cover-1920x1005.jpg` | JPG · 1920×1005 px · sRGB | 196 KB | Event cover (JPG q90) | written by `post_process.py` |

**11 files · 4.1 MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh facebook` (then `… post` for the profile images, grid and JPGs).
