#!/bin/bash
# Generate site images using Gemini 3 Pro image generation
# Usage: ./tools/generate-images.sh <sitename>
# Reads prompts from a PROMPTS array defined in sites/{sitename}/image-prompts.sh
# Outputs to images/{sitename}/

set -uo pipefail

SITE_NAME="${1:-}"
if [ -z "$SITE_NAME" ]; then
  echo "Usage: ./tools/generate-images.sh <sitename>"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
IMG_DIR="$PROJECT_DIR/images/$SITE_NAME"
PROMPTS_FILE="$PROJECT_DIR/sites/$SITE_NAME/image-prompts.sh"

if [ ! -f "$PROMPTS_FILE" ]; then
  echo "ERROR: No image prompts file found at $PROMPTS_FILE"
  echo "Create this file with generate_image calls. See tools/image-prompts-template.sh"
  exit 1
fi

mkdir -p "$IMG_DIR"

# Load API key from .env
GOOGLE_API_KEY=$(grep "^GOOGLE_API_KEY" "$PROJECT_DIR/.env" | sed 's/GOOGLE_API_KEY=//' | tr -d '"')
if [ -z "$GOOGLE_API_KEY" ]; then
  echo "ERROR: GOOGLE_API_KEY not found in .env"
  exit 1
fi

API_URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GOOGLE_API_KEY"

STYLE_PREFIX="Photorealistic pharmaceutical visual, extremely high quality, 8K detail, professional studio lighting. AstraZeneca brand aesthetic: clean, warm, clinically authoritative. Soft natural light, subtle depth of field."

generate_image() {
  local filename="$1"
  local prompt="$2"
  local output_path="$IMG_DIR/$filename"

  if [ -f "$output_path" ]; then
    echo "  SKIP: $filename (exists)"
    return 0
  fi

  local full_prompt="$STYLE_PREFIX $prompt"
  local json_prompt
  json_prompt=$(echo "$full_prompt" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")

  local payload="{\"contents\":[{\"parts\":[{\"text\":$json_prompt}]}],\"generationConfig\":{\"responseModalities\":[\"TEXT\",\"IMAGE\"]}}"

  local response
  response=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    --max-time 120)

  local image_data
  image_data=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for part in data.get('candidates', [{}])[0].get('content', {}).get('parts', []):
        if 'inlineData' in part:
            print(part['inlineData']['data'])
            break
    else:
        print('NO_IMAGE', file=sys.stderr)
except Exception as e:
    print(f'ERROR: {e}', file=sys.stderr)
" 2>/dev/null)

  if [ -n "$image_data" ] && [ "$image_data" != "" ]; then
    echo "$image_data" | base64 -d > "$output_path"
    local size
    size=$(wc -c < "$output_path" | tr -d ' ')
    if [ "$size" -gt 1000 ]; then
      echo "  OK: $filename (${size} bytes)"
      return 0
    else
      rm -f "$output_path"
      echo "  FAIL: $filename (too small: ${size} bytes)"
      return 1
    fi
  else
    echo "  FAIL: $filename (no image in response)"
    echo "$response" | head -c 200
    echo ""
    return 1
  fi
}

echo "=== Generating images for site: $SITE_NAME ==="
echo "Output: $IMG_DIR"
echo ""

TOTAL=0
SUCCESS=0
FAIL=0

# Source the site-specific prompts file (it calls generate_image)
source "$PROMPTS_FILE"

echo ""
echo "=== Summary ==="
echo "Total: $TOTAL | Success: $SUCCESS | Failed: $FAIL"
echo "Images saved to: $IMG_DIR"
