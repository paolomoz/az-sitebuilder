#!/bin/bash
# Image prompts for Zenturis (zenturigliptin) — Oral GLP-1 receptor agonist for Type 2 Diabetes
# Brand colour: Mediterranean Blue #2E6BA4

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a middle-aged South Asian man looking confident and healthy, silhouette filled with abstract metabolic energy imagery — glucose molecules transforming into golden light, cellular mitochondria glowing blue. Mediterranean blue and warm gold palette. White background. Editorial pharmaceutical style, aspirational and warm. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a woman in her 50s looking thoughtfully forward, silhouette filled with abstract descending curve data visualisations and molecular structures in Mediterranean blue and gold tones. Clean white background. Editorial pharmaceutical style, data-driven and authoritative. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-efficacy.jpeg"
generate_image "card-efficacy.jpeg" \
  "4:3 aspect ratio. Abstract medical illustration of a descending glucose curve rendered as a flowing blue ribbon against a warm golden gradient background. Modern pharmaceutical editorial style, clean and optimistic. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-safety.jpeg"
generate_image "card-safety.jpeg" \
  "4:3 aspect ratio. Warm photograph of a female doctor reviewing patient health data on a tablet screen with a reassuring expression. Bright modern clinic setting with Mediterranean blue accent wall. Natural light, professional and caring. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-dosing.jpeg"
generate_image "card-dosing.jpeg" \
  "4:3 aspect ratio. Clean product photograph of a single round blue film-coated tablet resting on a white surface beside its blister pack. Soft natural light, subtle Mediterranean blue gradient in background. Modern pharmaceutical product photography. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Content images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-moa.jpeg"
generate_image "columns-moa.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a GLP-1 receptor on a pancreatic beta cell being activated by a small molecule agonist in Mediterranean blue, triggering insulin release shown as golden particles. Clean modern pharmaceutical illustration style with blue and gold palette. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tab-zenith1.jpeg"
generate_image "tab-zenith1.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing a large 1.4 percentage figure in Mediterranean blue against a clean white background, with an abstract descending HbA1c curve below in blue and gold. Modern pharmaceutical data presentation style. No text other than the number." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tab-zenith2.jpeg"
generate_image "tab-zenith2.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing two equal descending curves side by side — one in Mediterranean blue and one in teal — converging at the same endpoint, symbolising non-inferiority. Modern pharmaceutical data presentation on clean white background. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-cv.jpeg"
generate_image "columns-cv.jpeg" \
  "4:3 aspect ratio. Abstract medical illustration of a strong healthy heart with smooth coronary arteries, rendered in Mediterranean blue and warm gold tones. Clean pharmaceutical editorial style, optimistic and clinical. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- SAFETY CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Safety card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-gi.jpeg"
generate_image "card-gi.jpeg" \
  "4:3 aspect ratio. Clean flat medical illustration of a stomach and digestive system in Mediterranean blue outline on white background, with a gentle calming wave pattern suggesting tolerability. Modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-hepatic.jpeg"
generate_image "card-hepatic.jpeg" \
  "4:3 aspect ratio. Clean flat medical illustration of a liver organ in Mediterranean blue outline on white background, with a monitoring chart icon overlay suggesting regular testing. Modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-hypo.jpeg"
generate_image "card-hypo.jpeg" \
  "4:3 aspect ratio. Clean flat medical illustration of a blood glucose meter showing a stable reading, in Mediterranean blue and warm gold tones on white background. Modern pharmaceutical instructional style, reassuring. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-special-pops.jpeg"
generate_image "columns-special-pops.jpeg" \
  "4:3 aspect ratio. Warm photograph of an older couple in their 70s walking together in a sunny park, looking healthy and active. Natural golden light, Mediterranean blue clothing accent. Editorial pharmaceutical lifestyle photography, dignified and warm. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- DOSING CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Dosing images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-admin.jpeg"
generate_image "columns-admin.jpeg" \
  "4:3 aspect ratio. Clean product photograph of a single blue tablet being taken with a glass of water, morning light through a window. Bright, clean, simple pharmaceutical lifestyle photography. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-dose-adjust.jpeg"
generate_image "columns-dose-adjust.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a calendar with weekly dosing markers highlighted in Mediterranean blue, with a clock icon showing morning time. White background, modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- RESOURCE CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Resource card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-prescribing.jpeg"
generate_image "card-prescribing.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a clinical document with a Mediterranean blue header bar and a checkmark icon. White background, minimal modern pharmaceutical style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-patient-guide.jpeg"
generate_image "card-patient-guide.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient information booklet with a Mediterranean blue cover lying open next to a cup of tea on a kitchen table. Soft morning light, inviting and accessible. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-clinical-data.jpeg"
generate_image "card-clinical-data.jpeg" \
  "4:3 aspect ratio. Modern flat illustration of a document showing graphs and bar charts in Mediterranean blue and gold, with a download arrow icon. Clean white background, pharmaceutical editorial style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
