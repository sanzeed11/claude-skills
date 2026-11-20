# Pinterest — Sanzeed social identity

Profile image and three 2:3 pins (project, quote, method — the method pin is the light label variant).

Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.

## Upload notes

- Pins: 1000×1500 (2:3) is the size Pinterest shows without cropping; ≤ 20 MB, PNG or JPG. Put the project title, place and sanzeed.com link in the pin description as well.
- Profile image: upload the 600 file; it displays at 165 px, cropped to a circle.

Platform sizes change: check the platform's help page before uploading (brand kit §8).

## Files

| File | Format · pixels | Size | Use | Editable from |
|---|---|---|---|---|
| `sanzeed-pin-profile--dark-165x165.png` | PNG · 165×165 px · sRGB | 3 KB | Profile image (display size), dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-pin-profile--light-165x165.png` | PNG · 165×165 px · sRGB | 3 KB | Profile image, light tile | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-pin-profile--dark-600x600.png` | PNG · 600×600 px · sRGB | 17 KB | Profile upload master, dark — upload this one | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-pin-profile--light-600x600.png` | PNG · 600×600 px · sRGB | 18 KB | Profile upload master, light | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-pin--project-1000x1500.png` | PNG · 1000×1500 px · sRGB | 668 KB | Pin — project (Prime Minister Museum, picture in a room) | `Editable_Templates/pinterest/pin-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh pinterest`. |
| `sanzeed-pin--quote-1000x1500.png` | PNG · 1000×1500 px · sRGB | 585 KB | Pin — quote ("The script comes first.") | `Editable_Templates/pinterest/pin-quote.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh pinterest`. |
| `sanzeed-pin--method-1000x1500.png` | PNG · 1000×1500 px · sRGB | 87 KB | Pin — method, light label variant (the four steps as a route) | `Editable_Templates/pinterest/pin-method.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh pinterest`. |

**7 files · 1.3 MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh pinterest` (then `… post` for the profile images, grid and JPGs).
