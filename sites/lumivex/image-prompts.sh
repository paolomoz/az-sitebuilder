#!/bin/bash
# Image prompts for Lumivex (lumvecitinib) — Selective TYK2 inhibitor for moderate-to-severe plaque psoriasis
# Brand colour: Luminous Amber #D4851F

# --- HERO IMAGES (16:9, 1440x810) ---
echo "--- Hero images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-home.jpeg"
generate_image "hero-home.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a confident woman in her 30s with radiant, healthy skin, silhouette filled with abstract amber and golden cellular renewal imagery — healthy skin layers, luminous keratinocytes, warm light radiating outward. Clean white background transitioning to warm amber. Editorial pharmaceutical style, aspirational, hopeful. No text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-efficacy.jpeg"
generate_image "hero-efficacy.jpeg" \
  "Wide 16:9 hero image. Double exposure portrait of a man in his 40s looking forward with calm confidence, silhouette filled with abstract data visualisation elements — ascending PASI response curves, percentage markers, data points in amber and gold on white. Clean white background. Editorial pharmaceutical style, evidence-driven." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] hero-moa.jpeg"
generate_image "hero-moa.jpeg" \
  "Wide 16:9 hero image. Abstract scientific illustration of the TYK2 signalling pathway being selectively blocked — a glowing amber molecule binding to the pseudokinase domain of a receptor, with downstream inflammatory cascades dimming. Deep amber and gold colour palette with cool grey pathway elements. Dark background with luminous amber molecular elements. Editorial pharmaceutical CGI style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CAROUSEL/CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Carousel/card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-efficacy.jpeg"
generate_image "card-efficacy.jpeg" \
  "4:3 aspect ratio. Abstract representation of skin renewal — healthy dermis layers in warm amber and gold, with luminous clear skin cells replacing inflamed tissue. Clean pharmaceutical editorial style, no text." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-safety.jpeg"
generate_image "card-safety.jpeg" \
  "4:3 aspect ratio. Warm photograph of a dermatologist reviewing skin assessment results with a patient in a modern consultation room, amber colour accents in the decor. Editorial medical style, natural light, collaborative." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-dosing.jpeg"
generate_image "card-dosing.jpeg" \
  "4:3 aspect ratio. Clean product-style photograph of a modern film-coated tablet next to its blister pack against a white background with subtle warm amber gradient. Sharp detail, pharmaceutical product photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- MOA TEASER (4:3, 800x600) ---
echo ""
echo "--- MOA teaser ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-moa.jpeg"
generate_image "columns-moa.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a TYK2 receptor with its pseudokinase domain highlighted in amber, with a selective inhibitor molecule approaching the allosteric binding site. Clean pharmaceutical illustration, amber and gold palette, white background." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- EFFICACY TAB IMAGES (4:3, 800x600) ---
echo ""
echo "--- Efficacy tab images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tab-luminance1.jpeg"
generate_image "tab-luminance1.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing 72% in large amber numerals against a clean white background, with an abstract ascending response curve suggesting skin clearance improvement. Modern pharmaceutical data presentation, warm amber and gold tones." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tab-luminance2.jpeg"
generate_image "tab-luminance2.jpeg" \
  "4:3 aspect ratio. Bold typographic data visualisation showing a head-to-head comparison bar chart in amber versus grey, with the amber bar clearly superior. Clean white background. Modern pharmaceutical data presentation, warm amber and gold tones." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-longterm.jpeg"
generate_image "columns-longterm.jpeg" \
  "4:3 aspect ratio. Data visualisation showing a sustained response curve over 3 years with a warm amber trend line maintaining a high plateau. Clean pharmaceutical style, white background with subtle grid lines." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- SAFETY CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Safety card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-infections.jpeg"
generate_image "card-infections.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a protective shield with a medical cross and a checklist, in amber and white. Modern pharmaceutical instructional style, clean white background. Represents infection monitoring." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-selectivity.jpeg"
generate_image "card-selectivity.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing selective targeting — one specific receptor highlighted in amber while three similar receptors in grey remain unaffected. Clean pharmaceutical illustration, minimal, precise." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-longterm-safety.jpeg"
generate_image "card-longterm-safety.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a calendar spanning 3 years with a checkmark and a steady heartbeat line across, in amber and white. Modern pharmaceutical style, represents long-term safety data." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- SAFETY SPECIAL POPULATIONS (4:3, 800x600) ---
echo ""
echo "--- Special populations ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-special-pops.jpeg"
generate_image "columns-special-pops.jpeg" \
  "4:3 aspect ratio. Warm photograph of an older man in his 70s relaxing comfortably in a garden, reading a book with clear, healthy forearms visible. Natural light, warm golden tones. Editorial pharmaceutical lifestyle, calm and dignified. Amber accent in background." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- DOSING IMAGES (4:3, 800x600) ---
echo ""
echo "--- Dosing images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-admin.jpeg"
generate_image "columns-admin.jpeg" \
  "4:3 aspect ratio. Clean product photograph showing a film-coated tablet being taken with a glass of water, morning sunlight streaming in, breakfast setting visible in soft focus. Warm amber and gold tones, pharmaceutical lifestyle photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] columns-monitoring.jpeg"
generate_image "columns-monitoring.jpeg" \
  "4:3 aspect ratio. Warm photograph of a dermatologist examining a patient's skin with a dermatoscope in a modern clinic. Natural light, amber warm tones. Professional and reassuring. Editorial medical photography." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- MOA PAGE IMAGES (4:3, 800x600) ---
echo ""
echo "--- Mechanism of action images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] psoriatic-inflammation.jpeg"
generate_image "psoriatic-inflammation.jpeg" \
  "4:3 aspect ratio. Scientific illustration of psoriatic skin in cross-section showing thickened epidermis with excessive keratinocyte proliferation, inflammatory T-cells infiltrating the dermis, and dilated blood vessels. Red and amber inflammation signals contrasting with grey normal tissue. Clean pharmaceutical illustration style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] tyk2-il23-cascade.jpeg"
generate_image "tyk2-il23-cascade.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing the IL-23/TYK2 signalling cascade — IL-23 binding to its receptor activating TYK2, which phosphorylates STAT3, driving Th17 cell differentiation and IL-17 production. Amber pathway arrows on clean white background. Modern pharmaceutical illustration, editorial quality." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] lumivex-blockade.jpeg"
generate_image "lumivex-blockade.jpeg" \
  "4:3 aspect ratio. Scientific illustration showing a selective inhibitor molecule in luminous amber binding to the pseudokinase JH2 domain of TYK2, preventing signal transduction while nearby JAK1 JAK2 JAK3 receptors remain fully active. Clean composition showing selective blockade. Amber and white, modern pharmaceutical editorial." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- RESOURCE CARD IMAGES (4:3, 800x600) ---
echo ""
echo "--- Resource card images ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-prescribing.jpeg"
generate_image "card-prescribing.jpeg" \
  "4:3 aspect ratio. Clean flat illustration of a clinical document with a warm amber header and a checkmark icon. White background, minimal modern pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-patient-guide.jpeg"
generate_image "card-patient-guide.jpeg" \
  "4:3 aspect ratio. Warm photograph of a patient information booklet with an amber-coloured cover, sitting on a clean desk next to a tablet device showing skin images. Natural light, instructional feel." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

TOTAL=$((TOTAL+1))
echo "[$TOTAL] card-clinical-data.jpeg"
generate_image "card-clinical-data.jpeg" \
  "4:3 aspect ratio. Modern illustration of a document with response curves and bar charts in amber, surrounded by subtle dermatology icons. Clean white background, flat pharmaceutical style." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))

# --- CONTACT IMAGE (4:3, 800x600) ---
echo ""
echo "--- Contact image ---"

TOTAL=$((TOTAL+1))
echo "[$TOTAL] contact-support.jpeg"
generate_image "contact-support.jpeg" \
  "4:3 aspect ratio. Warm photograph of a medical information specialist wearing a headset at a modern desk, with a laptop showing dermatology resources. Natural light, amber accents. Professional and approachable." && SUCCESS=$((SUCCESS+1)) || FAIL=$((FAIL+1))
