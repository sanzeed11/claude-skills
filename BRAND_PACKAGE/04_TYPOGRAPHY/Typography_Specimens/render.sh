#!/usr/bin/env bash
# render.sh — rebuild the specimen HTML from build_specimens.py, then render every sheet to PDF (A4) and PNG (2×).
# Usage: ./render.sh            (run from anywhere; paths are resolved from this file)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KIT="$HERE/../../15_SOURCE_FILES/Project_Files/brand-kit"
cd "$HERE/src" && python3 build_specimens.py
for html in "$HERE"/src/sanzeed-type-*.html; do
  name="$(basename "$html" .html)"
  node "$KIT/render.js" --in "$html" --out "$HERE/$name.pdf" --pdf --size 210x297
  pages=$(pdfinfo "$HERE/$name.pdf" | awk '/^Pages:/ {print $2}')
  if [ "$pages" = "1" ]; then
    node "$KIT/render.js" --in "$html" --out "$HERE/$name.png" --selector ".page" --width 794 --height 1123 --scale 2
  else
    # one PNG per page: render the PDF pages at 192 dpi (= 2× of 96 dpi CSS px)
    pdftoppm -r 192 -png "$HERE/$name.pdf" "$HERE/$name-p"
    for p in "$HERE/$name-p"-*.png; do n=$(echo "$p" | sed -E 's/.*-p-0*([0-9]+)\.png/\1/'); mv "$p" "$HERE/$name-$n.png"; done
  fi
done
ls -la "$HERE"/*.pdf "$HERE"/*.png
