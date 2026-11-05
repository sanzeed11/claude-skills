# Campaign templates — “Carry the light across.”

All copy is from `01_BRAND_STRATEGY` (confirmed from sanzeed.com); imagery is the client's own project visuals from `00_ORIGINAL_ASSETS_BACKUP`; logos from `02_LOGO_SYSTEM`; type Fraunces 300 / Inter Tight 600 / Inter 400 via `brand.css`. Bracketed fields such as `[Date]` are the only placeholders and must be filled by Sanzeed.

Three campaign lines, each as a key visual in 16:9, 1:1 and 9:16; a digital ad set at IAB sizes; promotional web banners in dark and light.

**Composition rule (every piece):** black field (or Plaster for the light banners) · one lit object or one lit room inside a rounded “room” plate with a hairline · headline in Fraunces 300, sentence case, ending with a full stop — the stop is the single gold point · wall-label caption (Title · Place) · primary wordmark top-left (full-colour-dark on dark, full-colour-light on light) · `sanzeed.com` in the footer.

| Line | Image | Wall label |
|---|---|---|
| Carry the light across. | the point-of-light object (`_shared/img/hero-object--dark-2400.jpg`, from `poster-dark.webp`) | Between two points of light · sanzeed.com |
| Experiential design you can walk into. | Prime Minister Museum, the tricolour corridor (`case/prime-minister-museum-03`) | Prime Minister Museum · New Delhi |
| Tell me about the room. | the portrait, 4:5 crop | Sanzeed Mirza · New Delhi |

**Exports.** Key visuals: PNG at 2× (3840×2160 / 2160×2160 / 2160×3840) + JPG at 1× (q88). Ads: PNG at 2× (`@2x`) + JPG at exact IAB pixels. Banners: PNG at 2× + JPG at 1×. 9:16 keeps text inside the centre-safe 1080×1420 band.

**How to edit.** Every export has an HTML source in `src/`. Change the copy or swap the `<img>` in the HTML (paths are relative to `BRAND_PACKAGE`), then re-render, e.g.

```
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-key-visual--carry-the-light-16x9.html --out sanzeed-key-visual--carry-the-light-16x9-3840x2160.png --width 1920 --height 1080 --scale 2
node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-ad--300x250.html --out sanzeed-ad--300x250@2x.png --width 300 --height 250 --scale 2
```
To regenerate the whole set from the templates: `python3 _shared/build/build_campaign.py`.

## Files

| File | Spec | Size |
|---|---|---|
| `README.md` | Markdown | 7 KB |
| `sanzeed-ad--1080x1080.jpg` | 1080×1080 px | 79 KB |
| `sanzeed-ad--1080x1080@2x.png` | 2160×2160 px | 546 KB |
| `sanzeed-ad--160x600.jpg` | 160×600 px | 16 KB |
| `sanzeed-ad--160x600@2x.png` | 320×1200 px | 102 KB |
| `sanzeed-ad--300x250.jpg` | 300×250 px | 14 KB |
| `sanzeed-ad--300x250@2x.png` | 600×500 px | 78 KB |
| `sanzeed-ad--300x600.jpg` | 300×600 px | 28 KB |
| `sanzeed-ad--300x600@2x.png` | 600×1200 px | 159 KB |
| `sanzeed-ad--320x50.jpg` | 320×50 px | 3 KB |
| `sanzeed-ad--320x50@2x.png` | 640×100 px | 9 KB |
| `sanzeed-ad--728x90.jpg` | 728×90 px | 10 KB |
| `sanzeed-ad--728x90@2x.png` | 1456×180 px | 24 KB |
| `sanzeed-ad--970x250.jpg` | 970×250 px | 25 KB |
| `sanzeed-ad--970x250@2x.png` | 1940×500 px | 146 KB |
| `sanzeed-key-visual--carry-the-light-16x9-1920x1080.jpg` | 1920×1080 px | 96 KB |
| `sanzeed-key-visual--carry-the-light-16x9-3840x2160.png` | 3840×2160 px | 906 KB |
| `sanzeed-key-visual--carry-the-light-1x1-1080x1080.jpg` | 1080×1080 px | 78 KB |
| `sanzeed-key-visual--carry-the-light-1x1-2160x2160.png` | 2160×2160 px | 1.0 MB |
| `sanzeed-key-visual--carry-the-light-9x16-1080x1920.jpg` | 1080×1920 px | 126 KB |
| `sanzeed-key-visual--carry-the-light-9x16-2160x3840.png` | 2160×3840 px | 1.9 MB |
| `sanzeed-key-visual--tell-me-16x9-1920x1080.jpg` | 1920×1080 px | 174 KB |
| `sanzeed-key-visual--tell-me-16x9-3840x2160.png` | 3840×2160 px | 2.4 MB |
| `sanzeed-key-visual--tell-me-1x1-1080x1080.jpg` | 1080×1080 px | 130 KB |
| `sanzeed-key-visual--tell-me-1x1-2160x2160.png` | 2160×2160 px | 2.0 MB |
| `sanzeed-key-visual--tell-me-9x16-1080x1920.jpg` | 1080×1920 px | 173 KB |
| `sanzeed-key-visual--tell-me-9x16-2160x3840.png` | 2160×3840 px | 2.5 MB |
| `sanzeed-key-visual--walk-into-16x9-1920x1080.jpg` | 1920×1080 px | 127 KB |
| `sanzeed-key-visual--walk-into-16x9-3840x2160.png` | 3840×2160 px | 1.0 MB |
| `sanzeed-key-visual--walk-into-1x1-1080x1080.jpg` | 1080×1080 px | 108 KB |
| `sanzeed-key-visual--walk-into-1x1-2160x2160.png` | 2160×2160 px | 1.1 MB |
| `sanzeed-key-visual--walk-into-9x16-1080x1920.jpg` | 1080×1920 px | 141 KB |
| `sanzeed-key-visual--walk-into-9x16-2160x3840.png` | 2160×3840 px | 1.5 MB |
| `sanzeed-web-banner--dark-1440x500.jpg` | 1440×500 px | 64 KB |
| `sanzeed-web-banner--dark-1440x500@2x.png` | 2880×1000 px | 511 KB |
| `sanzeed-web-banner--dark-1920x600.jpg` | 1920×600 px | 84 KB |
| `sanzeed-web-banner--dark-1920x600@2x.png` | 3840×1200 px | 754 KB |
| `sanzeed-web-banner--light-1440x500.jpg` | 1440×500 px | 59 KB |
| `sanzeed-web-banner--light-1440x500@2x.png` | 2880×1000 px | 271 KB |
| `sanzeed-web-banner--light-1920x600.jpg` | 1920×600 px | 76 KB |
| `sanzeed-web-banner--light-1920x600@2x.png` | 3840×1200 px | 346 KB |
| `src/sanzeed-ad--1080x1080.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-ad--160x600.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-ad--300x250.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-ad--300x600.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-ad--320x50.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-ad--728x90.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-ad--970x250.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-key-visual--carry-the-light-16x9.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--carry-the-light-1x1.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--carry-the-light-9x16.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--tell-me-16x9.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--tell-me-1x1.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--tell-me-9x16.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--walk-into-16x9.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--walk-into-1x1.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-key-visual--walk-into-9x16.html` | HTML source (brand.css + collateral.css) | 4 KB |
| `src/sanzeed-web-banner--dark-1440x500.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-web-banner--dark-1920x600.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-web-banner--light-1440x500.html` | HTML source (brand.css + collateral.css) | 2 KB |
| `src/sanzeed-web-banner--light-1920x600.html` | HTML source (brand.css + collateral.css) | 2 KB |
