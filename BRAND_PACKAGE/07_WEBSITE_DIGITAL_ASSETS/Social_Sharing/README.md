# Social_Sharing — generic share images and the link-preview mock

One message in three aspect ratios for posting the site itself (launch post, profile link, story), and a mock of how the Open Graph card appears in feeds and chats.

## Files

| File | Use | Spec | Source |
|---|---|---|---|
| `sanzeed-share--16x9-1920x1080.png` / `.jpg` | landscape post, YouTube community, presentation end card | 1920×1080 (exact platform pixels), wordmark + master line left, orbit monoline right, lamp | `src/share-16x9.html` |
| `sanzeed-share--1x1-1080x1080.png` / `.jpg` | Instagram / LinkedIn square post | 1080×1080 | `src/share-1x1.html` |
| `sanzeed-share--9x16-1080x1920.png` / `.jpg` | story / reel cover / WhatsApp status | 1080×1920, all text inside the 1080×1420 centre-safe band (250 px top and bottom are platform UI) | `src/share-9x16.html` |
| `sanzeed-link-preview--mock-1600x900.png` | shows `../Open_Graph/sanzeed-og--default-1200x630.png` inside three generic card shapes: a professional-network feed card, a summary-large-image card and a chat bubble. No platform logos or trade dress — text labels only | 3200×1800 (2×) | `src/link-preview.html` |
| `src/share.css` | layout for the three ratios | | |
| `build_share.sh` | renders all four with `render.js`, writes the JPGs (q90) | `bash build_share.sh` | |

JPG for platforms that cap size; PNG otherwise. The 9:16 file is also the right asset for an Instagram highlight cover (the centre circle shows the wordmark and line).

To change the copy, edit the three HTML files (they share `share.css`) and rebuild. The orbit illustration and the wordmark are the same inline SVGs used across the package (the wordmark — the approved refined original, three points — is re-inlined from `02_LOGO_SYSTEM/SVG` by `../sync_logo.py`, which `build_share.sh` runs first); the point on the ring is the one gold accent beside the wordmark's own points.
