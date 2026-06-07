#!/bin/bash
# resize.sh - Resize the Talan maps for web display.
#
# Generates two reduced variants of each map in /assets/maps/:
#   display/  (2400px max width, quality 85) - for inline page display
#   thumbs/   (800px max width, quality 80)  - for previews / index thumbnails
#
# The originals stay untouched. Use whichever variant suits the page;
# the originals are kept for click-through to full-size.
#
# Requires ImageMagick: https://imagemagick.org
#
# Run: bash ./resize.sh  (or chmod +x ./resize.sh && ./resize.sh)

set -e

# Resolve paths relative to this script's location
MAPS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DISPLAY_DIR="$MAPS_DIR/display"
THUMBS_DIR="$MAPS_DIR/thumbs"

# Check for ImageMagick (newer 'magick' binary or older 'convert')
if command -v magick &> /dev/null; then
    MAGICK="magick"
elif command -v convert &> /dev/null; then
    MAGICK="convert"
else
    echo "ERROR: ImageMagick is required but not found on PATH." >&2
    echo "Install from: https://imagemagick.org" >&2
    exit 1
fi

# Ensure output directories exist
mkdir -p "$DISPLAY_DIR" "$THUMBS_DIR"

# Maps to process
MAPS=("terrain.webp" "kingdoms.webp" "domains.webp")

echo "Resizing Talan maps..."
echo

for map in "${MAPS[@]}"; do
    input="$MAPS_DIR/$map"
    if [ ! -f "$input" ]; then
        echo "  SKIP $map (not found)"
        continue
    fi

    base="${map%.*}"
    display_out="$DISPLAY_DIR/$base.webp"
    thumb_out="$THUMBS_DIR/$base.webp"

    orig_size=$(du -h "$input" | cut -f1)
    echo "  $map ($orig_size)"

    # Display version: 2400px max width, quality 85
    $MAGICK "$input" -resize '2400x>' -quality 85 -define webp:method=6 "$display_out"
    display_size=$(du -h "$display_out" | cut -f1)
    echo "    -> display/$base.webp ($display_size)"

    # Thumb version: 800px max width, quality 80
    $MAGICK "$input" -resize '800x>' -quality 80 -define webp:method=6 "$thumb_out"
    thumb_size=$(du -h "$thumb_out" | cut -f1)
    echo "    -> thumbs/$base.webp ($thumb_size)"
done

echo
echo "Done."
