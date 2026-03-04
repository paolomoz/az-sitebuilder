#!/bin/bash
# Image prompts for Treluxia (trelimovab) — Anti-TSLP monoclonal antibody for Severe Asthma
# Brand colour: Deep Teal #006B77
# Accent colour: Sky Blue #4DADD9

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a confident woman in her 40s breathing deeply with eyes closed, silhouette filled with abstract flowing air currents and lung alveoli imagery in deep teal and sky blue tones, subtle golden light rays representing clear airways. White background. Editorial pharmaceutical style, aspirational and liberating. No text." "tier1" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a middle-aged South Asian man looking forward with determination, silhouette filled with abstract descending bar chart data and molecular antibody structures in deep teal and sky blue tones. Clean white background. Editorial pharmaceutical style, data-driven and authoritative. No text." "tier1" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-dosing.jpeg"
generate_image "hero-dosing.jpeg" \
  "Wide 16:9 hero image. Warm lifestyle photograph of a woman in her 30s sitting comfortably at home, looking relaxed and confident. Bright modern living room with natural light, deep teal accent cushion visible. Warm and reassuring, suggesting ease of self-care. Editorial pharmaceutical lifestyle photography. No text." "tier2" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-moa.jpeg"
generate_image "hero-moa.jpeg" \
  "Wide 16:9 hero image. Abstract scientific illustration of a branching network of inflammatory pathways being blocked at their origin point by a glowing teal antibody molecule. Pathways rendered as flowing streams in warm orange and red that fade to calm blue as they are neutralised. Deep teal and sky blue palette against dark background. Dramatic, modern CGI pharmaceutical style. No text." "tier4" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-exacerbations.jpeg"
generate_image "card-exacerbations.jpeg" \
  "4:3 aspect ratio. Abstract medical illustration of a descending exacerbation frequency curve rendered as a flowing teal ribbon dramatically dropping against a sky blue gradient background. Modern pharmaceutical editorial style, clean and optimistic. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-lung-function.jpeg"
generate_image "card-lung-function.jpeg" \
  "4:3 aspect ratio. Abstract medical illustration of healthy lungs with clear bronchial airways glowing in sky blue, surrounded by flowing air currents in teal and white. Clean modern pharmaceutical illustration style on white background. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-ocs.jpeg"
generate_image "card-ocs.jpeg" \
  "4:3 aspect ratio. Warm photograph of a woman's hand putting away a bottle of steroid tablets into a medicine cabinet, symbolising freedom from daily oral steroids. Soft morning light, modern bathroom setting with teal accent tile. Editorial pharmaceutical lifestyle photography. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- SAFETY CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Safety card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-isr.jpeg"
generate_image "card-isr.jpeg" \
  "4:3 aspect ratio. Clean flat medical illustration of an injection syringe with a small checkmark icon, rendered in deep teal outline on white background, with a subtle calming wave pattern. Modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-anaphylaxis.jpeg"
generate_image "card-anaphylaxis.jpeg" \
  "4:3 aspect ratio. Clean flat medical illustration of a shield icon with a medical cross, rendered in deep teal and sky blue on white background, suggesting safety monitoring and protection. Modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-infections.jpeg"
generate_image "card-infections.jpeg" \
  "4:3 aspect ratio. Clean flat medical illustration of an immune cell with antibody molecules surrounding it in deep teal outline on white background, with a subtle balanced scale overlay suggesting maintained immune function. Modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- RESOURCE CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Resource card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-prescribing-guide.jpeg"
generate_image "card-prescribing-guide.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a clinical document with a deep teal header bar and a checkmark icon. White background, minimal modern pharmaceutical style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-patient-materials.jpeg"
generate_image "card-patient-materials.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient information booklet with a teal cover lying open beside an asthma inhaler on a clean kitchen table. Soft morning light, inviting and accessible. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-clinical-data.jpeg"
generate_image "card-clinical-data.jpeg" \
  "4:3 aspect ratio. Modern flat illustration of a document showing bar charts and data graphs in deep teal and sky blue, with a download arrow icon. Clean white background, pharmaceutical editorial style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Content / column images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-moa-preview.jpeg"
generate_image "columns-moa-preview.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing TSLP cytokine molecules being neutralised by teal-coloured antibody proteins at the top of an inflammatory cascade, with downstream pathways (eosinophils, mast cells, T cells) fading as they lose activation signal. Deep teal and sky blue palette on white background. Modern pharmaceutical illustration. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-tslp-pathway.jpeg"
generate_image "columns-tslp-pathway.jpeg" \
  "4:3 aspect ratio. Scientific illustration of airway epithelial cells releasing TSLP cytokines upward, which activate dendritic cells and innate lymphoid cells below, triggering branching inflammatory cascades shown as flowing warm-coloured streams. Deep teal and warm orange palette. Modern pharmaceutical editorial illustration. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-mechanism.jpeg"
generate_image "columns-mechanism.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a large teal antibody molecule binding to and blocking a TSLP protein, preventing it from reaching the TSLP receptor on an immune cell surface. Clean molecular detail, deep teal and sky blue palette on light background. Modern pharmaceutical scientific illustration. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-positioning.jpeg"
generate_image "columns-positioning.jpeg" \
  "4:3 aspect ratio. Infographic-style illustration showing a treatment pathway staircase from left to right: inhaler at bottom, additional controllers in middle, biologic injection at top highlighted in teal. Clean modern pharmaceutical editorial style on white background. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-dosing.jpeg"
generate_image "columns-dosing.jpeg" \
  "4:3 aspect ratio. Clean product photograph of a pre-filled syringe pen device in teal and white packaging, resting on a clean white surface with soft natural light. Modern pharmaceutical product photography. No text." "tier3" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-admin.jpeg"
generate_image "columns-admin.jpeg" \
  "4:3 aspect ratio. Warm lifestyle photograph of a female healthcare professional demonstrating subcutaneous injection technique to a patient in a bright modern clinic. Natural light, professional and reassuring. Deep teal accent in the healthcare professional's lanyard. No text." "tier2" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-ocs-management.jpeg"
generate_image "columns-ocs-management.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a calendar with monthly injection markers highlighted in deep teal, with steroid tablet icons progressively shrinking over time, symbolising OCS dose reduction. White background, modern pharmaceutical instructional style. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-special-pops.jpeg"
generate_image "columns-special-pops.jpeg" \
  "4:3 aspect ratio. Warm photograph of diverse group of people of different ages — a teenager, a middle-aged woman, and an older man — all looking healthy and active outdoors in a park. Natural golden light, deep teal clothing accent. Editorial pharmaceutical lifestyle photography, inclusive and dignified. No text." "tier2" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-contact.jpeg"
generate_image "columns-contact.jpeg" \
  "4:3 aspect ratio. Warm photograph of a healthcare professional on a phone call at a modern desk, with a laptop open showing medical information. Bright office setting with deep teal accent wall. Professional and approachable. No text." "tier2" && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- TAB IMAGES (4:3, 800x600) ---
echo ""
echo "--- Tab images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tab-luminos1.jpeg"
generate_image "tab-luminos1.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing a large 56 percentage figure in deep teal against a clean white background, with an abstract descending exacerbation rate curve below in teal and sky blue. Modern pharmaceutical data presentation style. No text other than the number." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tab-luminos-ocs.jpeg"
generate_image "tab-luminos-ocs.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing 75% in deep teal font with a downward arrow icon, symbolising OCS dose reduction. Below, a small cluster of steroid tablets fading to transparency. Clean white background, modern pharmaceutical data presentation. No text other than the number." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
