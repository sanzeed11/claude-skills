#!/usr/bin/env bash
# render.sh — capture one animation with the brand kit's capture_frames.js (deterministic frame stepping),
# then encode to the delivery specs of 11_MOTION_GRAPHICS:
#   MP4  H.264 CRF 20 yuv420p, tagged BT.709 limited range (transparent sources are composited on black)
#   WebM VP9 CRF 30 (alpha when transparent)
#   MOV  ProRes 4444, fixed quantiser 9 (alpha when transparent). ProRes has a ~1 MB/s floor at 1080p and large soft
#        alpha gradients inflate it, so transparent sources carry no lamp wash — only the points glow.
#   GIF  long edge <= 960 px, 15 fps, 128 colours (transparent sources on black — GIF cannot hold soft alpha)
# and keep six key frames (Exports/Key_Frames/<Deliverable>/<name>/) plus a full-size poster of the last frame.
#
# usage: render.sh <source.html> <width> <height> <seconds> <out-dir> <out-base> <formats> [transparent] [gif-fps] [gif-width]
#   e.g. render.sh logo-reveal/index.html 1920 1080 4 ../Logo_Animations sanzeed-logo-reveal--dark-1920x1080 mp4,webm,gif
#        render.sh symbol-loop/index.html 1920 1080 3 ../Logo_Animations sanzeed-symbol-loop--alpha-1920x1080 mov,webm,mp4,gif transparent 20
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT="$HERE/../../15_SOURCE_FILES/Project_Files/brand-kit"
IN="$HERE/$1"; W="$2"; H="$3"; DUR="$4"; OUTDIR="$(cd "$HERE/$5" && pwd)"; BASE="$6"; FORMATS="$7"
TRANSPARENT="${8:-}"; GIFFPS="${9:-15}"; GIFW="${10:-960}"
TMP="${SZ_TMP:-/tmp/sz-motion}"; mkdir -p "$TMP" "$OUTDIR"
FR="$TMP/${BASE}_frames"
TFLAG=""; [ "$TRANSPARENT" = "transparent" ] && TFLAG="--transparent"

echo "== capture $BASE (${W}x${H}, ${DUR}s @30fps)"
node "$KIT/capture_frames.js" --in "$IN" --out "$TMP/$BASE" --width "$W" --height "$H" --fps 30 --duration "$DUR" --formats none --keepframes $TFLAG
INP=(-framerate 30 -i "$FR/f%05d.png")
ONBLACK="color=c=black:s=${W}x${H}:r=30[bg];[bg][0:v]overlay=shortest=1:format=auto,format=yuv420p"

for f in ${FORMATS//,/ }; do
  case "$f" in
    mp4)
      if [ -n "$TFLAG" ]; then
        ffmpeg -y -loglevel error "${INP[@]}" -filter_complex "$ONBLACK" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -movflags +faststart "$OUTDIR/$BASE.mp4"
      else
        ffmpeg -y -loglevel error "${INP[@]}" -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv -movflags +faststart "$OUTDIR/$BASE.mp4"
      fi ;;
    webm)
      PF=yuv420p; [ -n "$TFLAG" ] && PF=yuva420p
      ffmpeg -y -loglevel error "${INP[@]}" -c:v libvpx-vp9 -pix_fmt $PF -b:v 0 -crf 30 -row-mt 1 -deadline good -cpu-used 2 -auto-alt-ref 0 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv "$OUTDIR/$BASE.webm" ;;
    mov)
      PF=yuv444p10le; [ -n "$TFLAG" ] && PF=yuva444p10le
      ffmpeg -y -loglevel error "${INP[@]}" -c:v prores_ks -profile:v 4444 -pix_fmt $PF -qscale:v 9 -vendor apl0 "$OUTDIR/$BASE.mov" ;;
    gif)
      PAL="fps=${GIFFPS},scale='if(gt(iw,ih),min(${GIFW},iw),-2)':'if(gt(iw,ih),-2,min(${GIFW},ih))':flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=sierra2_4a:diff_mode=rectangle"
      if [ -n "$TFLAG" ]; then
        ffmpeg -y -loglevel error "${INP[@]}" -filter_complex "${ONBLACK},${PAL}" -loop 0 "$OUTDIR/$BASE.gif"
      else
        ffmpeg -y -loglevel error "${INP[@]}" -filter_complex "$PAL" -loop 0 "$OUTDIR/$BASE.gif"
      fi ;;
    *) echo "unknown format $f"; exit 1 ;;
  esac
done

# key frames (six, evenly spaced) + poster (last frame)
DELIV="$(basename "$OUTDIR")"; KF="$HERE/../Exports/Key_Frames/$DELIV/$BASE"; mkdir -p "$KF"; rm -f "$KF"/*
N=$(ls "$FR" | wc -l); LAST=$((N-1))
for i in 0 1 2 3 4 5; do
  IDX=$(( i * LAST / 5 )); SRC="$FR/f$(printf %05d $IDX).png"; T=$(python3 -c "print(f'{$IDX/30:.2f}')")
  if [ -n "$TFLAG" ]; then
    ffmpeg -y -loglevel error -i "$SRC" -vf "scale='min(960,iw)':-1" "$KF/${BASE}--t${T}s.png"
  else
    ffmpeg -y -loglevel error -i "$SRC" -vf "scale='min(960,iw)':-1" -q:v 3 "$KF/${BASE}--t${T}s.jpg"
  fi
done
if [ -n "$TFLAG" ]; then
  cp "$FR/f$(printf %05d $LAST).png" "$OUTDIR/$BASE--poster.png"
else
  ffmpeg -y -loglevel error -i "$FR/f$(printf %05d $LAST).png" -q:v 2 "$OUTDIR/$BASE--poster.jpg"
fi
rm -rf "$FR"
ls -la "$OUTDIR" | grep "$BASE" | awk '{printf "   %8.2f MB  %s\n", $5/1048576, $9}'
