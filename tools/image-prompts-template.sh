#!/bin/bash
# Image prompts template for a new site
# Copy this to sites/{sitename}/image-prompts.sh and customize
# Each call to generate_image adds to the TOTAL/SUCCESS/FAIL counters
# The generate_image function and counters are provided by tools/generate-images.sh

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-example.jpeg"
generate_image "hero-example.jpeg" \
  "Wide 16:9 hero image. Description of the scene..." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-example.jpeg"
generate_image "card-example.jpeg" \
  "4:3 aspect ratio. Description of the card image..." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
