#!/usr/bin/env python3
"""write_readmes.py — writes README.md in every platform folder (spec table with measured pixels and file sizes,
intended use, upload notes, source template + command). Run from this folder after render-all.sh."""
import pathlib, os
from PIL import Image
from pypdf import PdfReader
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent
EDIT = "Edit the `DATA` block at the top of the source HTML, then run `bash Editable_Templates/render-all.sh {p}`."
PROF = "Copied from `02_LOGO_SYSTEM/Social_Profile` (the symbol tile, S. centred); regenerate there with `export_logo.py`, then `bash Editable_Templates/render-all.sh post`."

def spec(path):
    p = ROOT / path
    if not p.exists(): return None
    kb = os.path.getsize(p) / 1024; size = f"{kb:,.0f} KB" if kb < 1024 else f"{kb/1024:.1f} MB"
    if p.suffix == '.pdf':
        r = PdfReader(p); b = r.pages[0].mediabox; return f"PDF · {len(r.pages)} pages · {float(b.width)/72*96:.0f}×{float(b.height)/72*96:.0f} px (CSS @page)", size
    im = Image.open(p); return f"{p.suffix[1:].upper()} · {im.width}×{im.height} px · sRGB", size

PLATFORMS = {
 'Instagram': dict(intro="Profile image, feed posts (1:1 and 4:5), stories, highlight covers, reel covers and a grid preview. Dark gallery by default; the 4:5 project post is the light *label* variant.",
  notes=["Profile: upload the 1024 master; Instagram crops it to a circle and shows 320 px — the S. tile sits centred so nothing is lost.",
         "Feed: 4:5 (1080×1350) is the largest the feed shows; 1:1 posts display at 1:1 in the grid. Upload PNG; Instagram recompresses to JPG itself.",
         "Stories / reels: keep text inside the 1080×1420 centre band (250 px free top and bottom for the UI) — every story template does, see the `--safe-zone-guide` render.",
         "Highlight covers: upload the 1080×1920 file as a story (archive it) and pick it as the cover; the profile shows the centre circle, where the icon is.",
         "Reel covers: use **Profile grid → Edit cover** and keep the default centre crop — the `--crop-guide` renders show the 4:5 feed crop and the 1:1 grid crop."],
  files=[
   ('sanzeed-ig-profile--dark-320x320.png','Profile image (display size), dark — default',PROF),
   ('sanzeed-ig-profile--light-320x320.png','Profile image, light tile (if a light avatar is wanted)',PROF),
   ('sanzeed-ig-profile--dark-1024x1024.png','Profile upload master, dark — upload this one',PROF),
   ('sanzeed-ig-profile--light-1024x1024.png','Profile upload master, light',PROF),
   ('sanzeed-ig-post--project-1080x1080.png','Square post — project with wall label (Prime Minister Museum)','`Editable_Templates/instagram/ig-post-project.html` · '+EDIT),
   ('sanzeed-ig-post--project--buddha-park-1080x1080.png','Square post — project variant (Buddha Park)','same template, other data: see the `--js "apply({…})"` line in `render-all.sh`'),
   ('sanzeed-ig-post--project--yuge-yugeen-bharat-1080x1080.png','Square post — project variant (Yuge Yugeen Bharat Museum)','same template, other data in `render-all.sh`'),
   ('sanzeed-ig-post--project--india-pavilion-1080x1080.png','Square post — project variant (India Pavilion Expo 2025, concept)','same template, other data in `render-all.sh`'),
   ('sanzeed-ig-post--quote-1080x1080.png','Square post — quote (Fraunces italic on the lamp)','`Editable_Templates/instagram/ig-post-quote.html` · '+EDIT),
   ('sanzeed-ig-post--quote--whole-room-1080x1080.png','Square post — quote variant ("I lead the whole room…")','same template, other data in `render-all.sh`'),
   ('sanzeed-ig-post--stat-1080x1080.png','Square post — stat "90 projects, one continuous craft."','`Editable_Templates/instagram/ig-post-stat.html` · '+EDIT),
   ('sanzeed-ig-post--announcement-1080x1080.png','Square post — "Now showing" announcement (Ram Katha Show)','`Editable_Templates/instagram/ig-post-announcement.html` · '+EDIT),
   ('sanzeed-ig-post--announcement--g20-tree-show-1080x1080.png','Square post — announcement variant (G20 Tree Show)','same template, other data in `render-all.sh`'),
   ('sanzeed-ig-portrait--project-1080x1350.png','Portrait post — project, light label variant (Buddha Park)','`Editable_Templates/instagram/ig-portrait-project.html` · '+EDIT),
   ('sanzeed-ig-portrait--method-1080x1350.png','Portrait post — method step (Step 02 Direct)','`Editable_Templates/instagram/ig-portrait-method.html` · '+EDIT+' Set `step` 1–4 to light the right point on the route.'),
   ('sanzeed-ig-portrait--about-1080x1350.png','Portrait post — about, with the approved portrait','`Editable_Templates/instagram/ig-portrait-about.html` · '+EDIT),
   ('sanzeed-ig-grid-preview--3x3-1632x1632.png','Grid preview — nine posts as the profile will show them','built by `Editable_Templates/post_process.py` from the nine square renders'),
   ('Stories/sanzeed-ig-story--project-1080x1920.png','Story — project (picture in a 5:4 room, label below)','`Editable_Templates/instagram/ig-story-project.html` · '+EDIT),
   ('Stories/sanzeed-ig-story--project--safe-zone-guide-1080x1920.png','Story — the same with the 1080×1420 centre-safe band drawn (reference only, do not upload)','same template rendered with `--js "document.documentElement.classList.add(\'show-guides\')"`'),
   ('Stories/sanzeed-ig-story--quote-1080x1920.png','Story — quote','`Editable_Templates/instagram/ig-story-quote.html` · '+EDIT),
   ('Stories/sanzeed-ig-story--cta-1080x1920.png','Story — "Tell me about the room." call (add the link sticker over the button)','`Editable_Templates/instagram/ig-story-cta.html` · '+EDIT),
   ('Stories/sanzeed-ig-story--method-1080x1920.png','Story — method step (Step 01 Discover)','`Editable_Templates/instagram/ig-story-method.html` · '+EDIT),
   ('Highlight_Covers/sanzeed-ig-highlight--work-1080x1920.png','Highlight cover — Work (doorway icon)','`Editable_Templates/instagram/ig-highlight-covers.html` (all eight icons in one file, drawn on the 24-unit monoline grid) · '+EDIT),
   ('Highlight_Covers/sanzeed-ig-highlight--museums-1080x1920.png','Highlight cover — Museums','same file, `COVERS` row "museums"'),
   ('Highlight_Covers/sanzeed-ig-highlight--shows-1080x1920.png','Highlight cover — Shows (projection cone)','same file, row "shows"'),
   ('Highlight_Covers/sanzeed-ig-highlight--method-1080x1920.png','Highlight cover — Method (the route)','same file, row "method"'),
   ('Highlight_Covers/sanzeed-ig-highlight--about-1080x1920.png','Highlight cover — About','same file, row "about"'),
   ('Highlight_Covers/sanzeed-ig-highlight--films-1080x1920.png','Highlight cover — Films (clapper)','same file, row "films"'),
   ('Highlight_Covers/sanzeed-ig-highlight--press-1080x1920.png','Highlight cover — Press (page, the point as its full stop)','same file, row "press"'),
   ('Highlight_Covers/sanzeed-ig-highlight--contact-1080x1920.png','Highlight cover — Contact (speech bubble)','same file, row "contact"'),
   ('Reels/sanzeed-ig-reel-cover--project-1080x1920.png','Reel cover — project film (Ram Katha Show)','`Editable_Templates/instagram/ig-reel-cover-project.html` · '+EDIT),
   ('Reels/sanzeed-ig-reel-cover--project--crop-guide-1080x1920.png','Reel cover — with the 1080×1350 feed crop and 1080×1080 grid crop drawn (reference only)','same template with the guide class'),
   ('Reels/sanzeed-ig-reel-cover--talk-1080x1920.png','Reel cover — talk / method','`Editable_Templates/instagram/ig-reel-cover-talk.html` · '+EDIT),
   ('Reels/sanzeed-ig-reel-cover--talk--crop-guide-1080x1920.png','Reel cover — talk, crop guide (reference only)','same template with the guide class'),
  ]),
 'Facebook': dict(intro="Page profile image, page cover (with its centre-safe guide), two post images and an event cover.",
  notes=["Profile: upload the 720 file; it shows at 170 px on desktop and 128 px on phones, cropped to a circle.",
         "Cover: desktop shows 820×312, phones crop the sides to the centre 1250×463 — all copy sits inside that band (see the `--safe-zone-guide` render). Facebook loads sRGB JPGs under 100 KB fastest: the `.jpg` (q90) is beside the PNG.",
         "Event cover: 1920×1005; some feeds crop it to 16:9, so the copy stays left-centre. The sample is filled with the Prime Minister Museum; replace title / place / `[Date and time]` per event.",
         "Post images: 1200×630 is also the link-preview size; the feed shows them at 1.91:1."],
  files=[
   ('sanzeed-fb-profile--dark-320x320.png','Profile image (display size), dark — default',PROF),
   ('sanzeed-fb-profile--light-320x320.png','Profile image, light tile',PROF),
   ('sanzeed-fb-profile--dark-720x720.png','Profile upload master, dark — upload this one',PROF),
   ('sanzeed-fb-profile--light-720x720.png','Profile upload master, light',PROF),
   ('sanzeed-fb-cover-1640x624.png','Page cover (PNG)','`Editable_Templates/facebook/fb-cover.html` · '+EDIT),
   ('sanzeed-fb-cover-1640x624.jpg','Page cover (JPG q90, the one to upload)','written by `post_process.py` from the PNG'),
   ('sanzeed-fb-cover--safe-zone-guide-1640x624.png','Page cover with the 1250×463 centre-safe area drawn (reference only)','same template with the guide class'),
   ('sanzeed-fb-post--project-1200x630.png','Post image — project (Yuge Yugeen Bharat Museum)','`Editable_Templates/facebook/fb-post-project.html` · '+EDIT),
   ('sanzeed-fb-post--quote-1200x630.png','Post image — quote','`Editable_Templates/facebook/fb-post-quote.html` · '+EDIT),
   ('sanzeed-fb-event-cover-1920x1005.png','Event cover (PNG)','`Editable_Templates/facebook/fb-event-cover.html` · '+EDIT),
   ('sanzeed-fb-event-cover-1920x1005.jpg','Event cover (JPG q90)','written by `post_process.py`'),
  ]),
 'LinkedIn': dict(intro="Personal profile image and banner (with the avatar-overlap guide), company logo and banner, six post images and the five-page document carousel for the Prime Minister Museum case study.",
  notes=["Personal banner: 1584×396, ≤ 8 MB. On desktop the profile photo overlaps the bottom-left; the copy sits right of x = 520 and the bottom-left 440×220 is empty (see the `--avatar-guide` render).",
         "Company banner: 1128×191; the company logo overlaps the bottom-left on desktop, so the wordmark sits left-centre and the line right.",
         "Post images: 1200×627 (1.91:1) or 1080×1080; LinkedIn shows the square larger in the feed.",
         "Document carousel: upload `Carousel/…pdf` as a *Document* post (PDF, ≤ 100 MB, ≤ 300 pages); LinkedIn renders each page as a swipeable card. The page PNGs are previews and can be posted as an image carousel instead.",
         "Profile image: 400×400 minimum; the company logo 300×300."],
  files=[
   ('sanzeed-li-profile--dark-400x400.png','Personal profile image, dark — default',PROF),
   ('sanzeed-li-profile--light-400x400.png','Personal profile image, light tile',PROF),
   ('sanzeed-li-company-logo--dark-300x300.png','Company page logo, dark — default',PROF),
   ('sanzeed-li-company-logo--light-300x300.png','Company page logo, light',PROF),
   ('sanzeed-li-banner--personal-1584x396.png','Personal banner (PNG)','`Editable_Templates/linkedin/li-banner-personal.html` · '+EDIT),
   ('sanzeed-li-banner--personal-1584x396.jpg','Personal banner (JPG q90)','written by `post_process.py`'),
   ('sanzeed-li-banner--personal--avatar-guide-1584x396.png','Personal banner with the avatar overlap drawn (reference only)','same template with the guide class'),
   ('sanzeed-li-banner--company-1128x191.png','Company banner (PNG)','`Editable_Templates/linkedin/li-banner-company.html` · '+EDIT),
   ('sanzeed-li-banner--company-1128x191.jpg','Company banner (JPG q90)','written by `post_process.py`'),
   ('sanzeed-li-post--insight-1200x627.png','Post — insight, light label variant (one observation, one image)','`Editable_Templates/linkedin/li-post-insight.html` · '+EDIT),
   ('sanzeed-li-post--project-1200x627.png','Post — project (Army Museum Abu Dhabi)','`Editable_Templates/linkedin/li-post-project.html` · '+EDIT),
   ('sanzeed-li-post--stat-1200x627.png','Post — stat, the four proof figures','`Editable_Templates/linkedin/li-post-stat.html` · '+EDIT),
   ('sanzeed-li-post--timeline-1200x627.png','Post — timeline "Fifteen years, one through-line." (2011 → 2026)','`Editable_Templates/linkedin/li-post-timeline.html` · '+EDIT),
   ('sanzeed-li-post--project-1080x1080.png','Square post — project (India Pavilion Expo 2025, concept)','`Editable_Templates/linkedin/li-post-square-project.html` · '+EDIT),
   ('sanzeed-li-post--quote-1080x1080.png','Square post — quote ("All seven, every time.")','`Editable_Templates/linkedin/li-post-square-quote.html` · '+EDIT),
   ('Carousel/sanzeed-li-carousel--prime-minister-museum-1080x1350.pdf','Document carousel — Prime Minister Museum case study, 5 pages (cover · the brief · the idea · the walk & what visitors do · the call)','`Editable_Templates/linkedin/li-carousel-pm-museum.html` · '+EDIT+' The PDF is rendered by `render.js --pdf` (CSS `@page` 1080×1350 px).'),
   ('Carousel/sanzeed-li-carousel--prime-minister-museum--page-1-1080x1350.png','Carousel page 1 — cover','same template, `--selector "#p1"`'),
   ('Carousel/sanzeed-li-carousel--prime-minister-museum--page-2-1080x1350.png','Carousel page 2 — the brief','same template, `--selector "#p2"`'),
   ('Carousel/sanzeed-li-carousel--prime-minister-museum--page-3-1080x1350.png','Carousel page 3 — the idea','same template, `--selector "#p3"`'),
   ('Carousel/sanzeed-li-carousel--prime-minister-museum--page-4-1080x1350.png','Carousel page 4 — the walk · what visitors do','same template, `--selector "#p4"`'),
   ('Carousel/sanzeed-li-carousel--prime-minister-museum--page-5-1080x1350.png','Carousel page 5 — the call','same template, `--selector "#p5"`'),
  ]),
 'YouTube': dict(intro="Channel profile image, channel banner (with the device safe-area guide), three thumbnails and the end-screen background with its element zones.",
  notes=["Banner: 2560×1440, ≤ 6 MB. TV shows all of it, desktop the centre 2560×423, tablets 1855×423, phones 1546×423 — the wordmark, line and name sit inside that smallest area (see the `--safe-area-guide` render). Upload the JPG if the PNG is refused for size.",
         "Thumbnails: 1280×720, ≤ 2 MB, JPG or PNG. The copy is set large (96–100 px) so it reads at 200 px wide; the bottom-right is clear for the duration badge.",
         "End screen: use the 1920×1080 background as the last 5–20 s of the film and place the elements in YouTube Studio on the three rooms — video 96,340 (672×378), subscribe 862,429 (196×196), video/playlist 1152,340 (672×378) — see the `--element-zones-guide` render.",
         "Profile image: 800×800, shown as a circle."],
  files=[
   ('sanzeed-yt-profile--dark-800x800.png','Channel profile image, dark — default',PROF),
   ('sanzeed-yt-profile--light-800x800.png','Channel profile image, light tile',PROF),
   ('sanzeed-yt-banner-2560x1440.png','Channel banner (PNG)','`Editable_Templates/youtube/yt-banner.html` · '+EDIT),
   ('sanzeed-yt-banner-2560x1440.jpg','Channel banner (JPG q90)','written by `post_process.py`'),
   ('sanzeed-yt-banner--safe-area-guide-2560x1440.png','Channel banner with the TV / desktop / tablet / phone areas drawn (reference only)','same template with the guide class'),
   ('sanzeed-yt-thumbnail--project-1280x720.png','Thumbnail — project film (Ram Katha Show)','`Editable_Templates/youtube/yt-thumb-project.html` · '+EDIT),
   ('sanzeed-yt-thumbnail--project-1280x720.jpg','Thumbnail — project film (JPG q90)','written by `post_process.py`'),
   ('sanzeed-yt-thumbnail--talk-1280x720.png','Thumbnail — talk / explainer, with the approved portrait plate','`Editable_Templates/youtube/yt-thumb-talk.html` · '+EDIT),
   ('sanzeed-yt-thumbnail--talk-1280x720.jpg','Thumbnail — talk (JPG q90)','written by `post_process.py`'),
   ('sanzeed-yt-thumbnail--process-1280x720.png','Thumbnail — process ("The script comes first.")','`Editable_Templates/youtube/yt-thumb-process.html` · '+EDIT),
   ('sanzeed-yt-thumbnail--process-1280x720.jpg','Thumbnail — process (JPG q90)','written by `post_process.py`'),
   ('sanzeed-yt-end-screen-1920x1080.png','End-screen background with the three rooms (PNG)','`Editable_Templates/youtube/yt-endscreen.html` · '+EDIT),
   ('sanzeed-yt-end-screen-1920x1080.jpg','End-screen background (JPG q90)','written by `post_process.py`'),
   ('sanzeed-yt-end-screen--element-zones-guide-1920x1080.png','End screen with the element zones and their pixel boxes drawn (reference only)','same template with the guide class'),
  ]),
 'X': dict(intro="Profile image, header (with the avatar-overlap guide) and three 16:9 post images.",
  notes=["Header: 1500×500, ≤ 5 MB. The avatar overlaps the bottom-left (about 400×200 at this scale): the copy sits right of x = 520 (see the `--avatar-guide` render). Upload the JPG if the PNG is over the limit.",
         "Post images: 1600×900 (16:9) shows uncropped in the timeline; ≤ 5 MB.",
         "Profile image: 400×400, ≤ 2 MB, shown as a circle."],
  files=[
   ('sanzeed-x-profile--dark-400x400.png','Profile image, dark — default',PROF),
   ('sanzeed-x-profile--light-400x400.png','Profile image, light tile',PROF),
   ('sanzeed-x-header-1500x500.png','Header (PNG)','`Editable_Templates/x/x-header.html` · '+EDIT),
   ('sanzeed-x-header-1500x500.jpg','Header (JPG q90)','written by `post_process.py`'),
   ('sanzeed-x-header--avatar-guide-1500x500.png','Header with the avatar overlap drawn (reference only)','same template with the guide class'),
   ('sanzeed-x-post--project-1600x900.png','Post image — project (Albert Hall Projection Show)','`Editable_Templates/x/x-post-project.html` · '+EDIT),
   ('sanzeed-x-post--quote-1600x900.png','Post image — statement ("Galleries planned as a route, not a floor plan.")','`Editable_Templates/x/x-post-quote.html` · '+EDIT),
   ('sanzeed-x-post--stat-1600x900.png','Post image — stat, the four proof figures','`Editable_Templates/x/x-post-stat.html` · '+EDIT),
  ]),
 'Pinterest': dict(intro="Profile image and three 2:3 pins (project, quote, method — the method pin is the light label variant).",
  notes=["Pins: 1000×1500 (2:3) is the size Pinterest shows without cropping; ≤ 20 MB, PNG or JPG. Put the project title, place and sanzeed.com link in the pin description as well.",
         "Profile image: upload the 600 file; it displays at 165 px, cropped to a circle."],
  files=[
   ('sanzeed-pin-profile--dark-165x165.png','Profile image (display size), dark — default',PROF),
   ('sanzeed-pin-profile--light-165x165.png','Profile image, light tile',PROF),
   ('sanzeed-pin-profile--dark-600x600.png','Profile upload master, dark — upload this one',PROF),
   ('sanzeed-pin-profile--light-600x600.png','Profile upload master, light',PROF),
   ('sanzeed-pin--project-1000x1500.png','Pin — project (Prime Minister Museum, picture in a room)','`Editable_Templates/pinterest/pin-project.html` · '+EDIT),
   ('sanzeed-pin--quote-1000x1500.png','Pin — quote ("The script comes first.")','`Editable_Templates/pinterest/pin-quote.html` · '+EDIT),
   ('sanzeed-pin--method-1000x1500.png','Pin — method, light label variant (the four steps as a route)','`Editable_Templates/pinterest/pin-method.html` · '+EDIT),
  ]),
}
for name, d in PLATFORMS.items():
    rows, total, n = [], 0, 0
    for f, use, src in d['files']:
        s = spec(f'{name}/{f}')
        if s is None: print('  MISSING', name, f); continue
        rows.append(f"| `{f}` | {s[0]} | {s[1]} | {use} | {src.replace('{p}', name.lower())} |"); total += os.path.getsize(ROOT / name / f); n += 1
    md = [f"# {name} — Sanzeed social identity", "", d['intro'], "",
          "Dark gallery by default (Gallery Black / Night ground, Gallery White type, one Lamp Gold accent), the `full-colour-dark` wordmark with its clear space, Fraunces 300 headlines in sentence case ending with a full stop, Inter Tight 600 eyebrows and wall-label titles, Inter 400 body. Every picture is one of the client's own project images and carries its wall label (Title · Place). Nothing here is hand-retouched: edit the source, re-render.", "",
          "## Upload notes", ""] + [f"- {x}" for x in d['notes']] + ["", "Platform sizes change: check the platform's help page before uploading (brand kit §8).", "",
          "## Files", "", "| File | Format · pixels | Size | Use | Editable from |", "|---|---|---|---|---|"] + rows + ["", f"**{n} files · {total/1024/1024:.1f} MB.** Regenerate everything with `bash ../Editable_Templates/render-all.sh {name.lower()}` (then `… post` for the profile images, grid and JPGs).", ""]
    (ROOT / name / 'README.md').write_text("\n".join(md)); print('  wrote', name + '/README.md', n, 'files')
