#!/bin/bash
# Image prompts for Novapril (novaprylimab) — Dual BAFF/APRIL inhibitor for SLE
# Brand colour: Deep Teal #007B8A

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a woman in her 30s in profile view, silhouette filled with abstract teal and white cellular biology imagery, B-cells, antibodies, molecular structures. Clean white background transitioning to deep teal. Editorial pharmaceutical style, high contrast, aspirational. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a middle-aged man in three-quarter view, silhouette filled with abstract clinical data visualisations, flowing graphs, statistical curves, scattered data points in teal and gold. Clean white background. Editorial pharmaceutical style, high contrast." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-safety.jpeg"
generate_image "hero-safety.jpeg" \
  "Wide 16:9 hero image. Warm natural-light photograph of a woman in her 40s walking peacefully through a sunlit park with green trees and dappled light. She wears casual clothing and has a calm, content expression. Warm teal and green tones, editorial pharmaceutical lifestyle photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-dosing.jpeg"
generate_image "hero-dosing.jpeg" \
  "Wide 16:9 hero image. Clean, modern product photograph of a pharmaceutical pre-filled autoinjector pen lying at an angle on a white surface with subtle teal gradient accents and soft shadows. Professional medical device photography, sharp detail, white and teal colour palette." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-moa.jpeg"
generate_image "hero-moa.jpeg" \
  "Wide 16:9 hero image. Abstract scientific illustration of molecular antibody structures interacting with cell-surface receptors in a deep teal and gold colour palette. Glowing molecular bonds, abstract cellular landscape, editorial pharmaceutical CGI style. Dark background with luminous teal elements." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-resources.jpeg"
generate_image "hero-resources.jpeg" \
  "Wide 16:9 hero image. Warm natural-light photograph of a healthcare professional, a woman in her 40s wearing a white coat, sitting at a desk with a laptop, smiling while reviewing materials. Modern clinic office, natural light from a window, teal accents in the decor. Editorial pharmaceutical lifestyle." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-efficacy.jpeg"
generate_image "card-efficacy.jpeg" \
  "4:3 aspect ratio. Abstract data visualisation in deep teal and white, flowing curves suggesting clinical trial response rates, clean modern pharmaceutical style, no text, no charts, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-safety.jpeg"
generate_image "card-safety.jpeg" \
  "4:3 aspect ratio. Close-up warm-toned photograph of a stethoscope resting on a wooden desk in natural light, with a subtle teal colour accent. Editorial medical style, shallow depth of field, no people visible." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-dosing.jpeg"
generate_image "card-dosing.jpeg" \
  "4:3 aspect ratio. Clean product photograph of a modern pharmaceutical pre-filled autoinjector pen on a pristine white background, with subtle teal accents on the device. Professional medical device photography, sharp detail." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Content images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] moa-preview.jpeg"
generate_image "moa-preview.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing dual antibody binding to two different molecular targets on a B-cell surface. Deep teal and white colour palette with warm gold accents. Clean, editorial pharmaceutical style, abstract cellular environment." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] luminos1-results.jpeg"
generate_image "luminos1-results.jpeg" \
  "4:3 aspect ratio. Bold data visualisation showing the number 61 percent in large teal typography against a clean white background, with a subtle upward arrow and faint clinical chart elements. Modern pharmaceutical data presentation, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] luminos2-results.jpeg"
generate_image "luminos2-results.jpeg" \
  "4:3 aspect ratio. Bold data visualisation showing the number 45 percent in large teal typography against a clean white background, with subtle abstract kidney or renal shapes in the background. Modern pharmaceutical data presentation, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-monitoring.jpeg"
generate_image "safety-monitoring.jpeg" \
  "4:3 aspect ratio. Warm photograph of a healthcare professional hands reviewing patient notes on a tablet device, with a subtle teal colour cast. Natural lighting, wooden desk surface, editorial medical style, no faces visible." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] patient-care.jpeg"
generate_image "patient-care.jpeg" \
  "4:3 aspect ratio. Warm photograph of an older woman in her 60s smiling gently while sitting in a sunlit living room, holding a cup of tea. Natural warm light, teal cushion visible in background. Editorial pharmaceutical lifestyle, positive and content expression." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] dosing-schedule.jpeg"
generate_image "dosing-schedule.jpeg" \
  "4:3 aspect ratio. Clean infographic-style illustration showing a simple calendar timeline with dots marking treatment doses in teal, on a clean white background. Modern pharmaceutical style, minimal design, abstract, no text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] injection-device.jpeg"
generate_image "injection-device.jpeg" \
  "4:3 aspect ratio. Close-up photograph of hands holding a modern pre-filled autoinjector pen demonstrating subcutaneous injection technique against a neutral background. Clean, clinical but warm lighting, teal accent on the device. Professional medical photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hcp-consultation.jpeg"
generate_image "hcp-consultation.jpeg" \
  "4:3 aspect ratio. Warm photograph of a doctor and patient in a consultation room, having a supportive conversation across a desk. Natural lighting, modern office setting, diverse representation. Teal accents in decor. Editorial pharmaceutical lifestyle." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] baff-pathway.jpeg"
generate_image "baff-pathway.jpeg" \
  "4:3 aspect ratio. Scientific illustration of a molecular signalling pathway on a cell surface. Abstract receptor shapes on a cell membrane with ligand molecules approaching. Deep teal background with glowing white and gold molecular elements. Clean, modern pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] april-pathway.jpeg"
generate_image "april-pathway.jpeg" \
  "4:3 aspect ratio. Scientific illustration of molecular receptors on a cell surface with ligand molecules binding. Deep teal and warm gold colour palette. Abstract cellular biology, glowing molecular bonds. Clean, modern pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] dual-inhibition.jpeg"
generate_image "dual-inhibition.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a single antibody molecule binding to two different molecular targets simultaneously. Clean split composition with teal on one side and gold on the other, merging in the centre. Modern pharmaceutical illustration, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-prescribing.jpeg"
generate_image "resource-prescribing.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a medical document or prescription form with a teal-coloured header and checkmark icon. White background, minimal modern pharmaceutical style, flat design aesthetic." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-patient.jpeg"
generate_image "resource-patient.jpeg" \
  "4:3 aspect ratio. Warm photograph of printed patient education booklets and leaflets fanned out on a clean white surface, with teal-coloured covers. Professional editorial photography, soft shadows, pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-education.jpeg"
generate_image "resource-education.jpeg" \
  "4:3 aspect ratio. Modern illustration of a laptop screen showing a video player with a molecular animation, surrounded by subtle teal geometric elements. Clean white background, flat modern pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] contact-support.jpeg"
generate_image "contact-support.jpeg" \
  "4:3 aspect ratio. Warm photograph of a customer service headset resting on a clean white desk with a laptop and notepad visible. Teal accents in accessories, natural light, professional but approachable. Editorial pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
