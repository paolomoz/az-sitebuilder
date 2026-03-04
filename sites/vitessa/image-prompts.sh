#!/bin/bash
# Image prompts for Vitessa (vitessamab) — Anti-IL-33 monoclonal antibody for severe eosinophilic asthma
# Brand colour: Verdant Teal #0A7E8C

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a woman in her 40s breathing freely with eyes closed, silhouette filled with abstract teal and emerald botanical lung imagery — branching airways resembling tree branches, clean alveoli structures. White background transitioning to verdant teal. Editorial pharmaceutical style, aspirational, calm. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a man in his 50s taking a deep breath outdoors, silhouette filled with abstract data visualisation elements — declining exacerbation curves, spirometry traces, data points in teal and gold. Clean white background. Editorial pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-dosing.jpeg"
generate_image "hero-dosing.jpeg" \
  "Wide 16:9 hero image. Clean, bright photograph of a pre-filled autoinjector pen held in a patient's hand against a light background with teal and white tones. Modern pharmaceutical product photography, clean and reassuring, natural light." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-moa.jpeg"
generate_image "hero-moa.jpeg" \
  "Wide 16:9 hero image. Abstract scientific illustration of airway epithelial cells releasing IL-33 alarmins upward, with a monoclonal antibody intercepting the signal. Deep teal and emerald colour palette with warm amber alarm signals. Dark background with luminous teal elements. Editorial pharmaceutical CGI style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CAROUSEL/CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Carousel/card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-efficacy.jpeg"
generate_image "card-efficacy.jpeg" \
  "4:3 aspect ratio. Abstract representation of airways opening — bronchial tree in teal and white with golden light breaking through, clean pharmaceutical editorial style, no text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-safety.jpeg"
generate_image "card-safety.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient and respiratory nurse reviewing an inhaler technique together, teal colour accent in the background. Editorial medical style, natural light." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-dosing.jpeg"
generate_image "card-dosing.jpeg" \
  "4:3 aspect ratio. Clean product-style photograph of a modern pre-filled autoinjector pen against a white background with subtle teal gradient. Sharp detail, pharmaceutical product photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Content images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] moa-preview.jpeg"
generate_image "moa-preview.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing IL-33 being released from damaged airway epithelial cells, with a monoclonal antibody intercepting it before it reaches ILC2 and Th2 cells below. Teal and white colour palette with warm amber accents. Clean editorial pharmaceutical illustration." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] clarity1-results.jpeg"
generate_image "clarity1-results.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing 68% in large teal numerals against a clean white background, with an abstract descending curve below suggesting exacerbation reduction. Modern pharmaceutical data presentation." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] clarity2-results.jpeg"
generate_image "clarity2-results.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing 58% in large teal numerals against a clean white background with a subtle abstract pill/tablet dissolving motif suggesting OCS elimination. Modern pharmaceutical data presentation." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] special-populations.jpeg"
generate_image "special-populations.jpeg" \
  "4:3 aspect ratio. Warm photograph of an older man in his 70s sitting comfortably in a garden chair, reading peacefully, with a teal blanket. Natural light, warm golden tones. Editorial pharmaceutical lifestyle, calm and dignified." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] pen-storage.jpeg"
generate_image "pen-storage.jpeg" \
  "4:3 aspect ratio. Clean product photograph showing a pre-filled pen stored in its original carton alongside a refrigerator, with a calendar showing monthly dosing. Teal and white colour palette. Modern pharmaceutical instructional style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] epithelial-damage.jpeg"
generate_image "epithelial-damage.jpeg" \
  "4:3 aspect ratio. Scientific illustration of airway epithelial cells under stress, releasing IL-33 molecules shown as amber and gold warning signals into the subepithelial space. Teal and white colour palette for the healthy tissue, warm amber for the alarmin signals. Clean pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] cascade-amplification.jpeg"
generate_image "cascade-amplification.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing the IL-33 ST2 signalling cascade branching into multiple inflammatory pathways — ILC2 activation, Th2 polarisation, eosinophil recruitment, mast cell degranulation. Teal base with amber branching pathways. Modern pharmaceutical illustration, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] vitessa-blockade.jpeg"
generate_image "vitessa-blockade.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a monoclonal antibody in teal binding to and neutralising IL-33 in amber before it can reach the ST2 receptor on an ILC2 cell. Clean composition showing the blocked signal with downstream pathways remaining inactive. Teal and white, modern pharmaceutical editorial." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] contact-support.jpeg"
generate_image "contact-support.jpeg" \
  "4:3 aspect ratio. Warm photograph of a medical information specialist wearing a headset at a modern desk, with a laptop showing clinical data. Natural light, teal accents. Professional and approachable." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- SAFETY CARDS (4:3, 800x600) ---
echo ""
echo "--- Safety card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-injection.jpeg"
generate_image "safety-injection.jpeg" \
  "4:3 aspect ratio. Close-up photograph of a mild injection site on the upper arm with a small adhesive bandage. Warm clinical lighting, clean and undramatic. Teal accent in background. Professional medical photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-zoster.jpeg"
generate_image "safety-zoster.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a vaccine vial with a shield icon, in teal and white. Modern pharmaceutical instructional style, clean white background." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-helminth.jpeg"
generate_image "safety-helminth.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a screening checklist with a magnifying glass icon, teal and amber on white. Modern pharmaceutical instructional style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- GETTING STARTED CARDS (4:3, 800x600) ---
echo ""
echo "--- Getting started card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] step-assess.jpeg"
generate_image "step-assess.jpeg" \
  "4:3 aspect ratio. Warm photograph of a respiratory physician reviewing blood test results on a screen, eosinophil count highlighted. Modern clinic, teal accents, natural light. Professional editorial medical photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] step-initiate.jpeg"
generate_image "step-initiate.jpeg" \
  "4:3 aspect ratio. Warm photograph of a respiratory nurse demonstrating a pre-filled pen to a patient in a consultation room. Teal decor accents, natural light, collaborative and encouraging." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] step-support.jpeg"
generate_image "step-support.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient confidently self-injecting at home in a comfortable setting, with a calendar on the wall showing monthly schedule. Teal accents, natural home environment, empowering." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- RESOURCE CARDS (4:3, 800x600) ---
echo ""
echo "--- Resource card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-prescribing.jpeg"
generate_image "resource-prescribing.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a clinical document with a teal header and a checkmark icon. White background, minimal modern pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-training.jpeg"
generate_image "resource-training.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient training booklet open next to a demo autoinjector pen on a clean surface. Teal-coloured cover, natural light, instructional feel." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-clinical.jpeg"
generate_image "resource-clinical.jpeg" \
  "4:3 aspect ratio. Modern illustration of a document with graphs and data visualisations in teal, surrounded by subtle clinical icons. Clean white background, flat pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
