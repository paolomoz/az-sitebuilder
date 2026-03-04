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
STYLE_CONFIG="$PROJECT_DIR/brand/az-image-style-config.sh"
REF_IMAGES_DIR="$PROJECT_DIR/brand/reference-images"

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

# Load tier-aware style config if available, otherwise use generic fallback
if [ -f "$STYLE_CONFIG" ]; then
  source "$STYLE_CONFIG"
  echo "Loaded brand style config from $STYLE_CONFIG"
else
  GENERIC_PREFIX="Photorealistic pharmaceutical visual, extremely high quality, 8K detail, professional studio lighting. AstraZeneca brand aesthetic: clean, warm, clinically authoritative. Soft natural light, subtle depth of field."
  GENERIC_NEGATIVE=""
  echo "No brand style config found, using generic prefix"
fi

# Resolve tier prefix and negative prompt for a given tier argument.
# Uses validated eval indirection (bash 3.2 compatible, no associative arrays).
# Falls back to GENERIC_* when tier is empty or unrecognised.
get_tier_prefix() {
  local tier="$1"
  if [ -n "$tier" ]; then
    # Validate tier is 1-4
    case "$tier" in
      tier1|tier2|tier3|tier4)
        local tier_num="${tier#tier}"
        local var_name="TIER${tier_num}_PREFIX"
        eval "local val=\"\${${var_name}:-}\""
        if [ -n "$val" ]; then
          echo "$val"
          return
        fi
        ;;
    esac
  fi
  echo "${GENERIC_PREFIX:-}"
}

get_tier_negative() {
  local tier="$1"
  if [ -n "$tier" ]; then
    case "$tier" in
      tier1|tier2|tier3|tier4)
        local tier_num="${tier#tier}"
        local var_name="TIER${tier_num}_NEGATIVE"
        eval "local val=\"\${${var_name}:-}\""
        if [ -n "$val" ]; then
          echo "$val"
          return
        fi
        ;;
    esac
  fi
  echo "${GENERIC_NEGATIVE:-}"
}

# Pick a random reference image from brand/reference-images/{tier}/ if available.
# Uses POSIX-compatible random selection (macOS sort lacks -R).
pick_reference_image() {
  local tier="$1"
  if [ -z "$tier" ] || [ ! -d "$REF_IMAGES_DIR/$tier" ]; then
    echo ""
    return
  fi

  # List image files (jpg, jpeg, png, webp) in the tier directory
  local images=()
  while IFS= read -r f; do
    images+=("$f")
  done < <(find "$REF_IMAGES_DIR/$tier" -maxdepth 1 -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.webp" \) 2>/dev/null)

  local count=${#images[@]}
  if [ "$count" -eq 0 ]; then
    echo ""
    return
  fi

  # POSIX-compatible random index using $RANDOM (available in bash 3.2)
  local idx=$(( RANDOM % count ))
  echo "${images[$idx]}"
}

# Base64-encode a reference image and return its MIME type
encode_reference_image() {
  local img_path="$1"
  local ext="${img_path##*.}"
  local mime_type
  case "$ext" in
    jpg|jpeg) mime_type="image/jpeg" ;;
    png)      mime_type="image/png" ;;
    webp)     mime_type="image/webp" ;;
    *)        mime_type="image/jpeg" ;;
  esac

  local b64_data
  b64_data=$(base64 < "$img_path" | tr -d '\n')
  echo "${mime_type}|${b64_data}"
}

generate_image() {
  local filename="$1"
  local prompt="$2"
  local tier="${3:-}"
  local output_path="$IMG_DIR/$filename"

  if [ -f "$output_path" ]; then
    echo "  SKIP: $filename (exists)"
    return 0
  fi

  # Select tier-specific or generic prefix/negative
  local style_prefix
  style_prefix=$(get_tier_prefix "$tier")
  local negative_prompt
  negative_prompt=$(get_tier_negative "$tier")

  local full_prompt="$style_prefix $prompt"
  if [ -n "$negative_prompt" ]; then
    full_prompt="$full_prompt. Avoid: $negative_prompt."
  fi

  # Check for reference image grounding
  local ref_image_path=""
  local payload=""

  if [ -n "$tier" ]; then
    ref_image_path=$(pick_reference_image "$tier")
  fi

  if [ -n "$ref_image_path" ]; then
    # Multi-modal payload: reference image + text prompt
    local encoded
    encoded=$(encode_reference_image "$ref_image_path")
    local mime_type="${encoded%%|*}"
    local b64_data="${encoded#*|}"
    local ref_name
    ref_name=$(basename "$ref_image_path")

    local style_instruction="Generate an image matching the visual style of this reference."
    local combined_prompt="$style_instruction $full_prompt"

    # Write base64 data to temp file to avoid shell quoting issues with large strings
    local b64_tmpfile
    b64_tmpfile=$(mktemp)
    echo "$b64_data" > "$b64_tmpfile"

    payload=$(echo "$combined_prompt" | python3 -c "
import json, sys
prompt_text = sys.stdin.read().strip()
with open('$b64_tmpfile', 'r') as f:
    b64 = f.read().strip()
payload = {
    'contents': [{
        'parts': [
            {'inlineData': {'mimeType': '$mime_type', 'data': b64}},
            {'text': prompt_text}
        ]
    }],
    'generationConfig': {'responseModalities': ['TEXT', 'IMAGE']}
}
print(json.dumps(payload))
")
    rm -f "$b64_tmpfile"
    echo "  REF: $ref_name ($tier)"
  else
    # Text-only payload
    local json_prompt
    json_prompt=$(echo "$full_prompt" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))")
    payload="{\"contents\":[{\"parts\":[{\"text\":$json_prompt}]}],\"generationConfig\":{\"responseModalities\":[\"TEXT\",\"IMAGE\"]}}"
  fi

  if [ -n "$tier" ]; then
    echo "  TIER: $tier"
  fi

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
