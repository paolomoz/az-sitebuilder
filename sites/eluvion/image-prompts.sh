#!/bin/bash
# Image prompts for Eluvion (eluvionimab) — Selective HIF-2α inhibitor for advanced renal cell carcinoma
# Brand colour: Sapphire Blue #1A5B8C

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a man in his 60s looking forward with quiet determination, silhouette filled with abstract sapphire blue and indigo kidney vasculature imagery — branching renal arteries, glomerular structures, flowing blood vessels. White background transitioning to deep sapphire blue. Editorial pharmaceutical style, aspirational, dignified. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a woman in her 50s looking confidently forward, silhouette filled with abstract data visualisation elements — declining tumour growth curves, Kaplan-Meier survival traces, data points in sapphire blue and gold. Clean white background. Editorial pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-dosing.jpeg"
generate_image "hero-dosing.jpeg" \
  "Wide 16:9 hero image. Clean bright photograph of an IV infusion bag and modern infusion pump in a comfortable outpatient clinic setting with warm natural light. Sapphire blue and white tones. Modern pharmaceutical product photography, clean and reassuring." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-moa.jpeg"
generate_image "hero-moa.jpeg" \
  "Wide 16:9 hero image. Abstract scientific illustration of HIF-2alpha protein being blocked by a monoclonal antibody, preventing VEGF and angiogenesis signalling in tumour cells. Deep sapphire blue and midnight colour palette with warm amber signalling elements. Dark background with luminous sapphire blue molecular structures. Editorial pharmaceutical CGI style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CAROUSEL/CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Carousel/card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-efficacy.jpeg"
generate_image "card-efficacy.jpeg" \
  "4:3 aspect ratio. Abstract representation of tumour regression — shrinking cellular mass dissolving into sapphire blue light particles, clean white background with golden accents. Editorial pharmaceutical style, no text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-safety.jpeg"
generate_image "card-safety.jpeg" \
  "4:3 aspect ratio. Warm photograph of a healthcare professional and an older male patient reviewing treatment results together in a modern consultation room. Sapphire blue colour accents in background decor. Editorial medical style, natural light, collaborative mood." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-dosing.jpeg"
generate_image "card-dosing.jpeg" \
  "4:3 aspect ratio. Clean product-style photograph of a modern IV infusion setup — clear glass vial and infusion bag against a white background with subtle sapphire blue gradient. Sharp detail, pharmaceutical product photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTENT IMAGES (4:3, 800x600) ---
echo ""
echo "--- Content images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] moa-preview.jpeg"
generate_image "moa-preview.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing HIF-2alpha protein in a tumour cell being blocked by a monoclonal antibody, preventing downstream VEGF signalling and new blood vessel formation. Sapphire blue and white colour palette with warm amber accents for the blocked pathway. Clean editorial pharmaceutical illustration." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] trial1-results.jpeg"
generate_image "trial1-results.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing 42% in large sapphire blue numerals against a clean white background, with an abstract upward arrow motif suggesting improvement. Modern pharmaceutical data presentation, no other text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] trial2-results.jpeg"
generate_image "trial2-results.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing 32% in large sapphire blue numerals against a clean white background, with an abstract survival curve motif. Modern pharmaceutical data presentation, no other text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] special-populations.jpeg"
generate_image "special-populations.jpeg" \
  "4:3 aspect ratio. Warm photograph of an older man in his 70s sitting comfortably in a sunlit garden, reading a book peacefully. Natural light, warm golden tones with sapphire blue blanket accent. Editorial pharmaceutical lifestyle, calm and dignified." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] storage.jpeg"
generate_image "storage.jpeg" \
  "4:3 aspect ratio. Clean product photograph showing a pharmaceutical glass vial and infusion bag in original packaging, stored in a clean pharmacy refrigerator shelf. Sapphire blue and white colour palette. Modern pharmaceutical instructional style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] pathway-disease.jpeg"
generate_image "pathway-disease.jpeg" \
  "4:3 aspect ratio. Scientific illustration of kidney tumour cells in a hypoxic microenvironment, showing HIF-2alpha accumulating in the cell nucleus and activating VEGF gene transcription. Sapphire blue and white colour palette with warm amber accents for the hypoxia signals. Clean pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] pathway-cascade.jpeg"
generate_image "pathway-cascade.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing downstream effects of HIF-2alpha activation — new blood vessel formation around tumour, tumour cell proliferation, immune evasion. Sapphire blue base with amber branching pathways. Modern pharmaceutical illustration, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] drug-mechanism.jpeg"
generate_image "drug-mechanism.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a monoclonal antibody (sapphire blue) binding to and neutralising HIF-2alpha protein (amber) inside a tumour cell, blocking VEGF transcription. Clean composition showing the therapeutic blockade. Sapphire blue and white, modern pharmaceutical editorial." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] contact-medical.jpeg"
generate_image "contact-medical.jpeg" \
  "4:3 aspect ratio. Warm photograph of a medical information specialist at a modern desk with a laptop showing clinical data. Professional woman wearing a headset, natural light from window, sapphire blue accents in decor. Professional and approachable." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- SAFETY CARDS (4:3, 800x600) ---
echo ""
echo "--- Safety card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-hypertension.jpeg"
generate_image "safety-hypertension.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a blood pressure monitor icon with an upward arrow, in sapphire blue and white. Modern pharmaceutical instructional style, clean white background." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-hepatic.jpeg"
generate_image "safety-hepatic.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a liver with a monitoring checklist icon, in sapphire blue and amber on white. Modern pharmaceutical instructional style, clean white background." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] safety-proteinuria.jpeg"
generate_image "safety-proteinuria.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a kidney with a laboratory test tube icon, in sapphire blue and white. Modern pharmaceutical instructional style, clean white background." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- DOSING CARDS (4:3, 800x600) ---
echo ""
echo "--- Dosing card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] step-assess.jpeg"
generate_image "step-assess.jpeg" \
  "4:3 aspect ratio. Warm photograph of an oncologist reviewing CT scan images on a lightbox, with a patient file visible. Modern clinic setting, sapphire blue accents in decor, natural light. Professional editorial medical photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] step-initiate.jpeg"
generate_image "step-initiate.jpeg" \
  "4:3 aspect ratio. Warm photograph of an oncology nurse preparing an IV infusion in a comfortable outpatient infusion suite, sapphire blue scrubs. Natural light, clinical but warm. Professional editorial medical photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] step-monitor.jpeg"
generate_image "step-monitor.jpeg" \
  "4:3 aspect ratio. Warm photograph of an oncologist and patient in follow-up consultation, reviewing results on a screen together. Sapphire blue accents, natural light from window. Collaborative and reassuring." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- RESOURCE CARDS (4:3, 800x600) ---
echo ""
echo "--- Resource card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-prescribing.jpeg"
generate_image "resource-prescribing.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a clinical document with a sapphire blue header and a checkmark icon. White background, minimal modern pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-patient.jpeg"
generate_image "resource-patient.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient information booklet open on a clean surface next to a glass pharmaceutical vial. Sapphire blue cover, natural light, instructional feel." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] resource-clinical.jpeg"
generate_image "resource-clinical.jpeg" \
  "4:3 aspect ratio. Modern illustration of a document with graphs and survival curve visualisations in sapphire blue, surrounded by subtle clinical icons. Clean white background, flat pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
