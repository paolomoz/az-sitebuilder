#!/bin/bash
# AZ Image Style Config — Machine-readable tier prefixes and negative prompts
# Sourced by tools/generate-images.sh
# Bash 3.2 compatible (no associative arrays)
# See brand/az-image-style-brief.md for full documentation

# --- Tier 1: Double-Exposure Artistic Portraits ---
TIER1_PREFIX="Double exposure portrait, editorial pharmaceutical style, human silhouette filled with scientific or natural imagery, clean white background, vibrant therapy-area colours, high contrast between silhouette edge and interior imagery, magazine-cover quality, no text overlay."
TIER1_NEGATIVE="generic stock photography, smiling at camera, lab coat, stethoscope, hospital background, clinical setting, text overlay, watermark, low resolution, blurry, cartoonish, overly saturated, neon colours, dark background, busy background"

# --- Tier 2: Warm Lifestyle Photography ---
TIER2_PREFIX="Warm natural-light photograph, editorial pharmaceutical lifestyle photography, positive but natural expression, shallow depth of field, golden-hour quality lighting, everyday setting, no medical equipment visible."
TIER2_NEGATIVE="hospital, clinic, medical equipment, fluorescent lighting, lab coat, stethoscope, medical gown, sterile environment, sad expression, suffering, distress, overly staged pose, stock photography feel, isolated on white, studio backdrop, dark or moody lighting, harsh shadows"

# --- Tier 3: Product & Device Photography ---
TIER3_PREFIX="Clean pharmaceutical product photograph, white or very light neutral background, sharp detail, professional studio lighting, instructional quality, no text overlay."
TIER3_NEGATIVE="lifestyle setting, people's faces, busy background, coloured backdrop, shadows on background, dust, scratches, low resolution, blurry product, artistic filter, vintage look, dramatic lighting, dark background"

# --- Tier 4: Dramatic/Abstract Hero Imagery ---
TIER4_PREFIX="Dramatic and aspirational image, cinematic quality, high dynamic range, communicating breakthrough and transformation, bold colour transitions, no text overlay."
TIER4_NEGATIVE="generic stock, calm pastoral scene, everyday setting, people, clinical or sterile aesthetic, low contrast, washed out colours, horror or foreboding mood, destructive imagery, consumer health website style, cartoon, illustration"

# --- Generic Fallback (no tier specified) ---
GENERIC_PREFIX="Photorealistic pharmaceutical visual, extremely high quality, 8K detail, professional studio lighting. AstraZeneca brand aesthetic: clean, warm, clinically authoritative. Soft natural light, subtle depth of field."
GENERIC_NEGATIVE=""
