#!/bin/bash
# Image prompts for Revantha (revantholimab) — Dual PD-L1/TIGIT checkpoint inhibitor for NSCLC
# Brand colour: Sapphire Blue #1B4F8A

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a man in his 50s in three-quarter view, silhouette filled with abstract sapphire blue and gold cellular immunology imagery, T-cells, antibodies, immune checkpoint receptors. Clean white background transitioning to deep sapphire blue. Editorial pharmaceutical style, high contrast, aspirational. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a woman in her 60s in profile view, silhouette filled with abstract clinical data visualisations, Kaplan-Meier survival curves, statistical scatter plots, data points in sapphire blue and gold. Clean white background. Editorial pharmaceutical style, high contrast." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-safety.jpeg"
generate_image "hero-safety.jpeg" \
  "Wide 16:9 hero image. Warm natural-light photograph of a man in his 60s walking along a tree-lined path in an autumn park, wearing a warm jacket and looking content. Golden and sapphire blue tones, editorial pharmaceutical lifestyle photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-dosing.jpeg"
generate_image "hero-dosing.jpeg" \
  "Wide 16:9 hero image. Clean, modern photograph of an IV infusion setup in a bright clinical treatment room, with a comfortable reclining infusion chair and natural light from a large window. Sapphire blue accents in the decor. Professional medical photography, warm and reassuring." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-moa.jpeg"
generate_image "hero-moa.jpeg" \
  "Wide 16:9 hero image. Abstract scientific illustration of T-cells engaging with tumour cells in a deep sapphire blue and gold colour palette. Glowing immune checkpoint receptors, abstract tumour microenvironment, editorial pharmaceutical CGI style. Dark background with luminous sapphire blue elements." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-resources.jpeg"
generate_image "hero-resources.jpeg" \
  "Wide 16:9 hero image. Warm natural-light photograph of a female oncologist in her 40s wearing a white coat, sitting at a desk with a laptop, smiling while reviewing clinical materials. Modern hospital office, natural light from a window, sapphire blue accents in the decor. Editorial pharmaceutical lifestyle." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-efficacy.jpeg"
generate_image "card-efficacy.jpeg" \
  "4:3 aspect ratio. Abstract data visualisation in sapphire blue and white, rising curves suggesting survival data, clean modern pharmaceutical style, no text, no charts, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-safety.jpeg"
generate_image "card-safety.jpeg" \
  "4:3 aspect ratio. Warm photograph of a healthcare professional hands holding a tablet showing patient monitoring data, with a subtle sapphire blue colour accent. Editorial medical style, shallow depth of field." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-dosing.jpeg"
generate_image "card-dosing.jpeg" \
  "4:3 aspect ratio. Clean photograph of a modern IV infusion bag and line against a clinical white background, with subtle sapphire blue accents. Professional medical photography, sharp detail." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Content images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] moa-preview.jpeg"
generate_image "moa-preview.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a bispecific antibody bridging two different receptor targets on a T-cell surface. Sapphire blue and white colour palette with warm gold accents. Clean, editorial pharmaceutical style, abstract tumour microenvironment." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] ascend1-results.jpeg"
generate_image "ascend1-results.jpeg" \
  "4:3 aspect ratio. Bold data visualisation showing the number 22 months in large sapphire blue typography against a clean white background, with a subtle Kaplan-Meier survival curve element. Modern pharmaceutical data presentation, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] ascend2-results.jpeg"
generate_image "ascend2-results.jpeg" \
  "4:3 aspect ratio. Bold data visualisation showing the number 19 months in large sapphire blue typography against a clean white background, with subtle abstract lung silhouette in the background. Modern pharmaceutical data presentation, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] immune-monitoring.jpeg"
generate_image "immune-monitoring.jpeg" \
  "4:3 aspect ratio. Warm photograph of a healthcare professional hands reviewing laboratory results on a computer screen, with a subtle sapphire blue colour cast. Natural lighting, modern clinical setting, editorial medical style, no faces visible." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] patient-support.jpeg"
generate_image "patient-support.jpeg" \
  "4:3 aspect ratio. Warm photograph of a middle-aged couple sitting on a park bench together, the man leaning gently into the woman, autumn light filtering through trees. Sapphire blue scarf visible. Editorial pharmaceutical lifestyle, positive and hopeful." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] dosing-combination.jpeg"
generate_image "dosing-combination.jpeg" \
  "4:3 aspect ratio. Clean infographic-style illustration showing a simple treatment timeline with chemotherapy cycles transitioning to maintenance monotherapy, in sapphire blue and white on a clean white background. Modern pharmaceutical style, minimal design, abstract, no text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] infusion-room.jpeg"
generate_image "infusion-room.jpeg" \
  "4:3 aspect ratio. Warm photograph of a modern, comfortable infusion treatment room with a reclining chair, IV stand, and soft natural light. Sapphire blue cushions and warm wood tones. Professional medical photography, calm and reassuring." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hcp-preparation.jpeg"
generate_image "hcp-preparation.jpeg" \
  "4:3 aspect ratio. Warm photograph of a pharmacist or nurse preparing an IV infusion bag in a clean clinical environment, with sapphire blue accents. Natural lighting, professional and careful. Editorial pharmaceutical style, no faces visible." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] pdl1-pathway.jpeg"
generate_image "pdl1-pathway.jpeg" \
  "4:3 aspect ratio. Scientific illustration of the PD-1 PD-L1 checkpoint pathway between a T-cell and a tumour cell. Abstract receptor shapes on cell surfaces with ligand interaction. Deep sapphire blue background with glowing white and gold molecular elements. Clean, modern pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tigit-pathway.jpeg"
generate_image "tigit-pathway.jpeg" \
  "4:3 aspect ratio. Scientific illustration of the TIGIT checkpoint pathway on a T-cell surface interacting with CD155 on a tumour cell. Deep sapphire blue and warm gold colour palette. Abstract immunology, glowing molecular interactions. Clean, modern pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] bispecific-advantage.jpeg"
generate_image "bispecific-advantage.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a single bispecific antibody molecule simultaneously engaging two different immune checkpoint receptors on a T-cell. Clean split composition with sapphire blue on one side and gold on the other, merging in the centre. Modern pharmaceutical illustration, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-prescribing.jpeg"
generate_image "resource-prescribing.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a clinical document or SmPC with a sapphire blue-coloured header and checkmark icon. White background, minimal modern pharmaceutical style, flat design aesthetic." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-patient.jpeg"
generate_image "resource-patient.jpeg" \
  "4:3 aspect ratio. Warm photograph of printed patient education booklets and support materials fanned out on a clean white surface, with sapphire blue covers. Professional editorial photography, soft shadows, pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-education.jpeg"
generate_image "resource-education.jpeg" \
  "4:3 aspect ratio. Modern illustration of a laptop screen showing a video player with an immune checkpoint animation, surrounded by subtle sapphire blue geometric elements. Clean white background, flat modern pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] contact-support.jpeg"
generate_image "contact-support.jpeg" \
  "4:3 aspect ratio. Warm photograph of a customer service headset resting on a clean white desk with a laptop and clinical notes visible. Sapphire blue accents in accessories, natural light, professional but approachable. Editorial pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
