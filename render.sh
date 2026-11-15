#!/usr/bin/env bash
# Renders the 108.75 s, 1080x1920, 30 fps portfolio reel.
# Usage: ./render.sh [out.mp4]      (optional: FRAMES=90 ./render.sh test.mp4 for a short test)
set -euo pipefail
cd "$(dirname "$0")"
OUT="${1:-Eniola_Portfolio_Reel_9x16.mp4}"
FRAMES="${FRAMES:-3263}"          # 108.75 s x 30 fps = 3262.5 -> 3263 frames
rm -rf frames && mkdir -p frames
python3 capg.py frames 0 "$FRAMES" frames           # headless Chromium: render(t) -> screenshot per frame
python3 audio3.py                                    # synthesises raw3.wav (48 kHz stereo) from code
ffmpeg -y -framerate 30 -i frames/f_%04d.jpg -i raw3.wav \
  -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
echo "wrote $OUT"
