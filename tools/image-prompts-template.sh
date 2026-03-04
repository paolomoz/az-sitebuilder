#!/bin/bash
# Image prompts template for a new site
# Copy this to sites/{sitename}/image-prompts.sh and customize
# Each call to generate_image adds to the TOTAL/SUCCESS/FAIL counters
# The generate_image function and counters are provided by tools/generate-images.sh
#
# generate_image takes 2 required args and 1 optional:
#   generate_image "filename.jpeg" "prompt text" ["tier"]
#
# Tier values (optional 3rd arg):
#   tier1 — Double-exposure artistic portraits (homepage heroes, therapy area cards)
#   tier2 — Warm lifestyle photography (product heroes, patient benefit sections)
#   tier3 — Product & device photography (dosing pages, device guides)
#   tier4 — Dramatic/abstract hero imagery (oncology, severe disease products)
#   (omit) — Generic photorealistic pharmaceutical style (backwards compatible)
#
# When a tier is specified:
#   - The tier-specific style prefix replaces the generic one
#   - Negative prompts are appended automatically
#   - If brand/reference-images/{tier}/ contains images, one is randomly selected
#     and sent as a multi-modal style reference to the Gemini API
#
# See brand/az-image-style-brief.md for full tier documentation.

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

# Tier 1 example: Double-exposure artistic portrait
TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Woman in her 40s breathing freely, silhouette filled with teal botanical lung imagery — branching airways resembling tree branches. White background." \
  "tier1" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# Tier 2 example: Warm lifestyle photograph
TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-product.jpeg"
generate_image "hero-product.jpeg" \
  "Wide 16:9 hero image. Man in his 60s walking confidently in a park, golden afternoon light, warm amber tones." \
  "tier2" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# Tier 4 example: Dramatic/abstract hero
TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-oncology.jpeg"
generate_image "hero-oncology.jpeg" \
  "Wide 16:9 hero image. Aurora borealis over dark mountains, dark teal transitioning to warm orange and gold. Sense of transcendence." \
  "tier4" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Card images ---"

# No tier example: Generic pharmaceutical style (backwards compatible)
TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-example.jpeg"
generate_image "card-example.jpeg" \
  "4:3 aspect ratio. Description of the card image..." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# Tier 3 example: Product/device photography
TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-device.jpeg"
generate_image "card-device.jpeg" \
  "4:3 aspect ratio. Pre-filled autoinjector pen shown from a three-quarter angle, white background, teal accent." \
  "tier3" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
