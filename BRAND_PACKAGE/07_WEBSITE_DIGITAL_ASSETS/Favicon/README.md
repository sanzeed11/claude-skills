# Favicon — the production set for sanzeed.com

A copy of `02_LOGO_SYSTEM/Favicon/` (generated there by the logo builder in `15_SOURCE_FILES/Project_Files/logo-builder/` from the symbol tile `sanzeed-symbol-tile--dark.svg`): the approved refined S + point (20 Nov 2026). Re-copied 20 Nov 2026 with `cp ../02_LOGO_SYSTEM/Favicon/* Favicon/` run from `07_WEBSITE_DIGITAL_ASSETS/`. Edit the logo source and regenerate in the logo system, then copy here; do not edit these files by hand.

| File | Spec | Tag / use |
|---|---|---|
| `favicon.ico` | ICO with 16 / 32 / 48 / 64 px layers | `<link rel="icon" href="/favicon.ico" sizes="48x48">` (legacy and Windows) |
| `favicon.svg` | symbol tile, Night rounded square, Gallery White S, gold point | `<link rel="icon" href="/favicon.svg" type="image/svg+xml">` (modern browsers, scales to any size) |
| `favicon-light.svg`, `favicon-light-64.png` | the light tile for sites that show a light tab bar | optional `media="(prefers-color-scheme: light)"` variant |
| `favicon-16.png` … `favicon-1024.png` | PNG at 16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512, 1024 | explicit `sizes` links where a platform asks for PNG |
| `apple-touch-icon.png` | 180×180, square (iOS rounds it) | `<link rel="apple-touch-icon" href="/apple-touch-icon.png">` |
| `android-chrome-192x192.png`, `android-chrome-512x512.png` | rounded tile, transparent corners | referenced from the manifest |
| `maskable-icon-512x512.png` | full-bleed Night, symbol inside the safe zone | manifest `purpose: "maskable"` |
| `safari-pinned-tab.svg` | single-colour symbol (black), recoloured by Safari | `<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#0D0D0F">` |
| `site.webmanifest` | name, short_name, icons, theme #0D0D0F | `<link rel="manifest" href="/site.webmanifest">` |
| `favicon-head-snippet.html` | the full `<head>` block, including the two `theme-color` metas for light and dark | paste into `<head>`, serve the files from the site root |

See `../App_Icons/` for iOS, Android, Windows and PWA icon sets at every platform size with their own mapping.
