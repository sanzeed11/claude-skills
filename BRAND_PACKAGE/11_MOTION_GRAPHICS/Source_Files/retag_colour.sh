#!/usr/bin/env bash
# retag_colour.sh — stamp BT.709 colour metadata (primaries, transfer, matrix, limited range) on every MP4 (H.264) and
# WebM (VP9) in the deliverable folders without re-encoding (bitstream filters; lossless). render.sh now sets the tags at
# encode time; this pass exists for files encoded before that and as a check. Usage: ./retag_colour.sh
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$HERE/.."
n=0
for f in Logo_Animations/*.mp4 Intros_Outros/*.mp4 Social_Animations/*.mp4 Lower_Thirds/*.mp4 Website_Loader/*.mp4; do
  [ -f "$f" ] || continue
  ffmpeg -y -loglevel error -i "$f" -c copy -bsf:v "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0" -movflags +faststart "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f"; n=$((n+1))
done
for f in Logo_Animations/*.webm Intros_Outros/*.webm Lower_Thirds/*.webm; do
  [ -f "$f" ] || continue
  ffmpeg -y -loglevel error -i "$f" -c copy -bsf:v "vp9_metadata=color_space=bt709:color_range=tv" "$f.tmp.webm" && mv "$f.tmp.webm" "$f"; n=$((n+1))
done
echo "re-tagged $n files"; ffprobe -v quiet -select_streams v:0 -show_entries stream=color_space,color_transfer,color_primaries,color_range -of csv=p=0 Logo_Animations/sanzeed-logo-reveal--dark-1920x1080.mp4
