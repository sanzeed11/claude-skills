#!/usr/bin/env bash
# render-all.sh — regenerates every social-media export from the HTML templates in this folder
# with the brand kit's render.js (Chromium), then runs post_process.py (profile images, grid preview, JPGs)
# and build_pptx.py (the six PPTX versions + their LibreOffice proofs).
#   bash render-all.sh            # everything
#   bash render-all.sh instagram  # one platform (instagram | facebook | linkedin | youtube | x | pinterest | post | pptx)
set -euo pipefail
cd "$(dirname "$0")"
R="../../15_SOURCE_FILES/Project_Files/brand-kit/render.js"
G="document.documentElement.classList.add('show-guides')"      # turns the safe-zone / crop guides on
IMG="../../../00_ORIGINAL_ASSETS_BACKUP/images/img"              # relative to the template files
only="${1:-all}"
want() { [ "$only" = all ] || [ "$only" = "$1" ]; }
r() { # r <template.html> <out> <width> <height> [extra render.js args]
  node "$R" --in "$1" --out "$2" --width "$3" --height "$4" --scale 1 --wait 500 "${@:5}" >/dev/null && echo "  wrote $2"; }

if want instagram; then echo "Instagram"; T=instagram; O=../Instagram
  for t in project quote stat announcement; do r $T/ig-post-$t.html $O/sanzeed-ig-post--$t-1080x1080.png 1080 1080; done
  for t in project method about;           do r $T/ig-portrait-$t.html $O/sanzeed-ig-portrait--$t-1080x1350.png 1080 1350; done
  for t in project quote cta method;       do r $T/ig-story-$t.html $O/Stories/sanzeed-ig-story--$t-1080x1920.png 1080 1920; done
  r $T/ig-story-project.html $O/Stories/sanzeed-ig-story--project--safe-zone-guide-1080x1920.png 1080 1920 --js "$G"
  for c in work museums shows method about films press contact; do r $T/ig-highlight-covers.html $O/Highlight_Covers/sanzeed-ig-highlight--$c-1080x1920.png 1080 1920 --selector "#cover-$c"; done
  for t in project talk; do r $T/ig-reel-cover-$t.html $O/Reels/sanzeed-ig-reel-cover--$t-1080x1920.png 1080 1920
                            r $T/ig-reel-cover-$t.html $O/Reels/sanzeed-ig-reel-cover--$t--crop-guide-1080x1920.png 1080 1920 --js "$G"; done
  # five more square posts from the same templates (other confirmed projects) for the 3×3 grid preview
  r $T/ig-post-project.html $O/sanzeed-ig-post--project--buddha-park-1080x1080.png 1080 1080 --js "apply({image:'$IMG/case/buddha-park-06.webp', image_focal:'50% 55%', headline:'A garden of gestures.', title:'Buddha Park', place:'Uttarakhand', site:'sanzeed.com/work/buddha-park'})"
  r $T/ig-post-project.html $O/sanzeed-ig-post--project--yuge-yugeen-bharat-1080x1080.png 1080 1080 --js "apply({image:'$IMG/yuge-yugin-bharat-museum.webp', image_focal:'50% 58%', eyebrow:'Museum & Cultural Exhibition Planning', headline:'Galleries planned as a route, not a floor plan.', title:'Yuge Yugeen Bharat Museum', place:'New Delhi', site:'sanzeed.com/#galleries'})"
  r $T/ig-post-project.html $O/sanzeed-ig-post--project--india-pavilion-1080x1080.png 1080 1080 --js "apply({image:'$IMG/india-pavilion-expo-2025.webp', image_focal:'68% 40%', eyebrow:'Spatial Experience & Environmental Branding', headline:'Brands you can stand inside.', title:'India Pavilion Expo 2025', place:'Concept', site:'sanzeed.com/#galleries'})"
  r $T/ig-post-announcement.html $O/sanzeed-ig-post--announcement--g20-tree-show-1080x1080.png 1080 1080 --js "apply({image:'$IMG/g20-tree-show.webp', image_focal:'50% 45%', headline:'Shows where light and timing do the talking.', lit_last_word:false, title:'G20 Tree Show', place:'New Delhi', line:'Event Production & Brand Activation', site:'sanzeed.com/#galleries'})"
  r $T/ig-post-quote.html $O/sanzeed-ig-post--quote--whole-room-1080x1080.png 1080 1080 --js "apply({quote:'I lead the whole room — story, space, graphics, media and the team that builds it.', eyebrow:'About'})"
fi
if want facebook; then echo "Facebook"; T=facebook; O=../Facebook
  r $T/fb-cover.html $O/sanzeed-fb-cover-1640x624.png 1640 624
  r $T/fb-cover.html $O/sanzeed-fb-cover--safe-zone-guide-1640x624.png 1640 624 --js "$G"
  for t in project quote; do r $T/fb-post-$t.html $O/sanzeed-fb-post--$t-1200x630.png 1200 630; done
  r $T/fb-event-cover.html $O/sanzeed-fb-event-cover-1920x1005.png 1920 1005
fi
if want linkedin; then echo "LinkedIn"; T=linkedin; O=../LinkedIn
  r $T/li-banner-personal.html $O/sanzeed-li-banner--personal-1584x396.png 1584 396
  r $T/li-banner-personal.html $O/sanzeed-li-banner--personal--avatar-guide-1584x396.png 1584 396 --js "$G"
  r $T/li-banner-company.html $O/sanzeed-li-banner--company-1128x191.png 1128 191
  for t in insight project stat timeline; do r $T/li-post-$t.html $O/sanzeed-li-post--$t-1200x627.png 1200 627; done
  for t in project quote; do r $T/li-post-square-$t.html $O/sanzeed-li-post--$t-1080x1080.png 1080 1080; done
  for i in 1 2 3 4 5; do r $T/li-carousel-pm-museum.html $O/Carousel/sanzeed-li-carousel--prime-minister-museum--page-$i-1080x1350.png 1080 1350 --selector "#p$i"; done
  node "$R" --in $T/li-carousel-pm-museum.html --out $O/Carousel/sanzeed-li-carousel--prime-minister-museum-1080x1350.pdf --pdf --size 285.75x357.19 --wait 800 >/dev/null && echo "  wrote $O/Carousel/sanzeed-li-carousel--prime-minister-museum-1080x1350.pdf"
fi
if want youtube; then echo "YouTube"; T=youtube; O=../YouTube
  r $T/yt-banner.html $O/sanzeed-yt-banner-2560x1440.png 2560 1440 --wait 700
  r $T/yt-banner.html $O/sanzeed-yt-banner--safe-area-guide-2560x1440.png 2560 1440 --wait 700 --js "$G"
  for t in project talk process; do r $T/yt-thumb-$t.html $O/sanzeed-yt-thumbnail--$t-1280x720.png 1280 720; done
  r $T/yt-endscreen.html $O/sanzeed-yt-end-screen-1920x1080.png 1920 1080
  r $T/yt-endscreen.html $O/sanzeed-yt-end-screen--element-zones-guide-1920x1080.png 1920 1080 --js "$G"
fi
if want x; then echo "X"; T=x; O=../X
  r $T/x-header.html $O/sanzeed-x-header-1500x500.png 1500 500
  r $T/x-header.html $O/sanzeed-x-header--avatar-guide-1500x500.png 1500 500 --js "$G"
  for t in project quote stat; do r $T/x-post-$t.html $O/sanzeed-x-post--$t-1600x900.png 1600 900; done
fi
if want pinterest; then echo "Pinterest"; T=pinterest; O=../Pinterest
  for t in project quote method; do r $T/pin-$t.html $O/sanzeed-pin--$t-1000x1500.png 1000 1500; done
fi
if want post; then echo "Post-processing (profile images, grid preview, JPG q90)"; python3 post_process.py; fi
if want pptx; then echo "PPTX versions + LibreOffice proofs"; python3 build_pptx.py; fi
echo "done."
