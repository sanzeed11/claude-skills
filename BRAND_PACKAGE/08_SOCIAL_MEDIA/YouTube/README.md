# YouTube — Sanzeed social identity

Channel profile image, channel banner (with the device safe-area guide), three thumbnails and the end-screen background with its element zones.

Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.

## Upload notes

- Banner: 2560×1440, ≤ 6 MB. TV shows all of it, desktop the centre 2560×423, tablets 1855×423, phones 1546×423 — the wordmark, line and name sit inside that smallest area (see the `--safe-area-guide` render). Upload the JPG if the PNG is refused for size.
- Thumbnails: 1280×720, ≤ 2 MB, JPG or PNG. The copy is set large (96–100 px) so it reads at 200 px wide; the bottom-right is clear for the duration badge.
- End screen: use the 1920×1080 background as the last 5–20 s of the film and place the elements in YouTube Studio on the three rooms — video 96,340 (672×378), subscribe 862,429 (196×196), video/playlist 1152,340 (672×378) — see the `--element-zones-guide` render.
- Profile image: 800×800, shown as a circle.

Platform sizes change: check the platform's help page before uploading (brand kit §8).

## Files

| File | Format · pixels | Size | Use | Editable from |
|---|---|---|---|---|
| `sanzeed-yt-profile--dark-800x800.png` | PNG · 800×800 px · sRGB | 11 KB | Channel profile image, dark — default | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-yt-profile--light-800x800.png` | PNG · 800×800 px · sRGB | 11 KB | Channel profile image, light tile | Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`. |
| `sanzeed-yt-banner-2560x1440.png` | PNG · 2560×1440 px · sRGB | 3.7 MB | Channel banner (PNG) | `Editable_Templates/youtube/yt-banner.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh youtube`. |
| `sanzeed-yt-banner-2560x1440.jpg` | JPG · 2560×1440 px · sRGB | 513 KB | Channel banner (JPG q90) | written by `post_process.py` |
| `sanzeed-yt-banner--safe-area-guide-2560x1440.png` | PNG · 2560×1440 px · sRGB | 3.7 MB | Channel banner with the TV / desktop / tablet / phone areas drawn (reference only) | same template with the guide class |
| `sanzeed-yt-thumbnail--project-1280x720.png` | PNG · 1280×720 px · sRGB | 1.1 MB | Thumbnail — project film (Ram Katha Show) | `Editable_Templates/youtube/yt-thumb-project.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh youtube`. |
| `sanzeed-yt-thumbnail--project-1280x720.jpg` | JPG · 1280×720 px · sRGB | 223 KB | Thumbnail — project film (JPG q90) | written by `post_process.py` |
| `sanzeed-yt-thumbnail--talk-1280x720.png` | PNG · 1280×720 px · sRGB | 830 KB | Thumbnail — talk / explainer, with the approved portrait plate | `Editable_Templates/youtube/yt-thumb-talk.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh youtube`. |
| `sanzeed-yt-thumbnail--talk-1280x720.jpg` | JPG · 1280×720 px · sRGB | 123 KB | Thumbnail — talk (JPG q90) | written by `post_process.py` |
| `sanzeed-yt-thumbnail--process-1280x720.png` | PNG · 1280×720 px · sRGB | 494 KB | Thumbnail — process ("The script comes first.") | `Editable_Templates/youtube/yt-thumb-process.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh youtube`. |
| `sanzeed-yt-thumbnail--process-1280x720.jpg` | JPG · 1280×720 px · sRGB | 91 KB | Thumbnail — process (JPG q90) | written by `post_process.py` |
| `sanzeed-yt-end-screen-1920x1080.png` | PNG · 1920×1080 px · sRGB | 564 KB | End-screen background with the three rooms (PNG) | `Editable_Templates/youtube/yt-endscreen.html` · Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh youtube`. |
| `sanzeed-yt-end-screen-1920x1080.jpg` | JPG · 1920×1080 px · sRGB | 80 KB | End-screen background (JPG q90) | written by `post_process.py` |
| `sanzeed-yt-end-screen--element-zones-guide-1920x1080.png` | PNG · 1920×1080 px · sRGB | 582 KB | End screen with the element zones and their pixel boxes drawn (reference only) | same template with the guide class |

**14 files · 11.9 MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh youtube` (then `… post` for the profile images, grid and JPGs).
