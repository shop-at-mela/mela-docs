#!/usr/bin/env bash
# Render a Mela card template to PNG via headless Chrome (no window opens).
#
#   ./render.sh <template.html> <out.png> [square|story|pin]
#
# Ratios:  square 1080x1080 (IG feed, default) | story 1080x1920 | pin 1000x1500
# Add MELA_SCALE=2 for retina-crisp output at 2x pixels (e.g. 2160x2160).
set -euo pipefail

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
html="${1:?usage: render.sh <template.html> <out.png> [square|story|pin]}"
out="${2:?usage: render.sh <template.html> <out.png> [square|story|pin]}"
ratio="${3:-square}"
scale="${MELA_SCALE:-1}"

case "$ratio" in
  square) size="1080,1080" ;;
  story)  size="1080,1920" ;;
  pin)    size="1000,1500" ;;
  *) echo "unknown ratio: $ratio (use square|story|pin)" >&2; exit 1 ;;
esac

abs="$(cd "$(dirname "$html")" && pwd)/$(basename "$html")"

"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --force-device-scale-factor="$scale" \
  --screenshot="$out" --window-size="$size" \
  --default-background-color=00000000 \
  "$abs" 2>/dev/null

echo "wrote $out  ($ratio ${size}, scale ${scale}x)"
