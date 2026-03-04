# AZ Image Style Brief

> Machine-readable companion: `brand/az-image-style-config.sh`
> Source: `brand/az-brand-voice.md` Section 4, validated against myastrazeneca.co.uk imagery.

---

## Tier System Overview

| Tier | Name | Use Case | Style |
|------|------|----------|-------|
| 1 | Double-Exposure Artistic | Homepage heroes, therapy area cards | Human silhouette filled with scientific/natural imagery |
| 2 | Warm Lifestyle Photography | Product heroes, patient benefit sections | Natural-light photos of patients in everyday settings |
| 3 | Product & Device Photography | Dosing pages, device guides | Clean product shots on white/light backgrounds |
| 4 | Dramatic/Abstract Hero | Oncology heroes, severe disease products | Bold CGI, aurora borealis, dramatic landscapes |

When no tier is specified, the generic fallback applies (the existing photorealistic pharmaceutical style).

---

## Tier 1: Double-Exposure Artistic Portraits

### Prompt Template

```
Double exposure portrait, [subject description] silhouette filled with [scientific/natural imagery],
clean white background, editorial pharmaceutical style, vibrant [therapy colour],
high contrast between silhouette edge and interior imagery,
magazine-cover quality, no text overlay
```

### Seed Phrases (validated)

- "Double exposure portrait, human silhouette filled with"
- "editorial pharmaceutical style"
- "clean white background, high contrast"
- "magazine-cover quality"

### Negative Prompt

```
generic stock photography, smiling at camera, lab coat, stethoscope, hospital background,
clinical setting, text overlay, watermark, low resolution, blurry, cartoonish,
overly saturated, neon colours, dark background, busy background
```

### Composition Rules

| Aspect Ratio | Composition |
|--------------|-------------|
| 16:9 (hero) | Subject in left or centre third, silhouette from shoulders up, interior imagery fills full silhouette |
| 4:3 (card) | Tighter crop, head and shoulders only, interior imagery more concentrated |
| 1:1 (square) | Centred portrait, generous white space around silhouette edges |

### Therapy-to-Imagery Colour Map

| Therapy Area | Interior Imagery | Colour Palette |
|-------------|-------------------|----------------|
| Respiratory | Lungs as branching trees, airways, botanical forms | Teal #0A7E8C, Emerald #2E7D32 |
| Cardiovascular | Heart vessels, blood cells, circulatory patterns | Red #C62828, Coral #E57373, Amber #E88A00 |
| Oncology | Cellular structures, DNA helices, molecular bonds | Magenta #830051, Purple #6A1B9A, Teal #1A5276 |
| Immunology | Antibodies, immune cells, shield motifs | Gold #EFAB00, Teal #00827F |
| Rare Disease | Neural pathways, nerve fibres, constellation patterns | Forest Green #2E7D32, Gold #EFAB00 |

---

## Tier 2: Warm Lifestyle Photography

### Prompt Template

```
Warm natural-light photograph, [age] [ethnicity] [gender] patient,
[activity] in [everyday setting], [product brand colour] warmth,
editorial pharmaceutical lifestyle photography, positive but natural expression,
shallow depth of field, golden-hour quality lighting
```

### Seed Phrases (validated)

- "Warm natural-light photograph"
- "editorial pharmaceutical lifestyle"
- "positive but natural expression"
- "golden-hour quality lighting"
- "shallow depth of field"

### Negative Prompt

```
hospital, clinic, medical equipment, fluorescent lighting, lab coat, stethoscope,
medical gown, sterile environment, sad expression, suffering, distress,
overly staged pose, stock photography feel, isolated on white, studio backdrop,
dark or moody lighting, harsh shadows
```

### Composition Rules

| Aspect Ratio | Composition |
|--------------|-------------|
| 16:9 (hero) | Environmental portrait, subject off-centre with setting visible, wide establishing shot |
| 4:3 (card) | Medium shot, subject fills ~60% of frame, setting visible as context |
| 1:1 (square) | Close-up or medium close-up, subject centred, soft background bokeh |

### Subject & Setting Guidelines

- **Ages**: Reflect the patient population for the product (e.g., 60s-70s for cardiovascular, 30s-50s for asthma, children for paediatric vaccines)
- **Diversity**: Vary ethnicity, gender, and body type across a page's image set
- **Settings**: Home, garden, park, café, community — never hospital or clinic
- **Activities**: Walking, reading, gardening, cooking, playing with grandchildren — active and engaged
- **Clothing**: Casual everyday wear — never medical gowns or formal suits

### Product Brand Colour Warmth

| Product | Colour Accent | Warmth Direction |
|---------|--------------|-----------------|
| Forxiga | Amber #E88A00 | Warm golden tones in lighting |
| Symbicort | Gold/Amber | Warm golden, outdoor activity |
| Wainzua | Forest Green #2E7D32 | Natural green environment |
| Fluenz | Sky Blue #4FC3F7 | Bright, cheerful, high-key |
| Lokelma | Dark Teal #00827F | Cool but friendly |

---

## Tier 3: Product & Device Photography

### Prompt Template

```
Clean pharmaceutical product photograph, [device/product description],
white or very light neutral background, sharp detail, professional studio lighting,
[product brand colour] accent, instructional quality, no text overlay
```

### Seed Phrases (validated)

- "Clean pharmaceutical product photograph"
- "white or very light neutral background"
- "sharp detail, professional studio lighting"
- "instructional quality"

### Negative Prompt

```
lifestyle setting, people's faces, busy background, coloured backdrop,
shadows on background, dust, scratches, low resolution, blurry product,
artistic filter, vintage look, dramatic lighting, dark background
```

### Composition Rules

| Aspect Ratio | Composition |
|--------------|-------------|
| 16:9 (hero) | Product centred with generous white space, packaging may be shown alongside |
| 4:3 (card) | Product fills ~70% of frame, single angle, clean isolation |
| 1:1 (square) | Product centred, may include hand for scale on device products |

### Product-Specific Notes

- **Inhalers** (Symbicort, Trixeo, Bevespi): Show from multiple angles, label visible, cap on/off views
- **Pre-filled pens** (Wainzua, biologics): Show in-hand for scale, demonstrate grip
- **Oral preparations** (Lokelma sachets): Show sachet + preparation steps
- **Packaging**: Include carton alongside device for context

---

## Tier 4: Dramatic/Abstract Hero Imagery

### Prompt Template

```
Dramatic [abstract/landscape/CGI] image, [specific visual description],
[product brand colour] palette transitioning to [complementary colour],
bold and aspirational, communicating breakthrough and transformation,
cinematic quality, high dynamic range, no text overlay
```

### Seed Phrases (validated)

- "Dramatic, bold and aspirational"
- "cinematic quality, high dynamic range"
- "communicating breakthrough and transformation"
- "dark background transitioning to"

### Negative Prompt

```
generic stock, calm pastoral scene, everyday setting, people,
clinical or sterile aesthetic, low contrast, washed out colours,
horror or foreboding mood, destructive imagery, violence, death,
consumer health website style, cartoon, illustration
```

### Composition Rules

| Aspect Ratio | Composition |
|--------------|-------------|
| 16:9 (hero) | Full-bleed dramatic backdrop, designed for text overlay in left or right third |
| 4:3 (card) | Concentrated drama, tighter composition of the key visual element |
| 1:1 (square) | Abstract pattern or celestial detail, works as background texture |

### Product-Specific Visual Direction

| Product | Visual Direction | Palette |
|---------|-----------------|---------|
| Tezspire | Aurora borealis, fire, dramatic sky — "rising above" | Dark teal #1A5276 → warm orange/gold #EFAB00 |
| Tagrisso | Lung anatomy imagery with purple/teal gradients | Purple #6A1B9A → teal #00827F |
| Imfinzi | Vast landscapes (mountains, seas, horizons) | AZ Blue #003DA5 → sky blue |
| Lynparza | Cellular/molecular structures with magenta glow | Magenta #830051 → deep purple |

---

## Generic Fallback (No Tier Specified)

When no tier is specified, images use the original photorealistic pharmaceutical style:

```
Photorealistic pharmaceutical visual, extremely high quality, 8K detail,
professional studio lighting. AstraZeneca brand aesthetic: clean, warm,
clinically authoritative. Soft natural light, subtle depth of field.
```

This maintains backwards compatibility with existing image-prompts.sh files that do not use tiers.

---

## Cross-Reference

- Brand voice & full imagery guidelines: `brand/az-brand-voice.md`
- Visual analysis of live site: `brand/myastrazeneca-analysis.md`
- Machine-readable config: `brand/az-image-style-config.sh`
- Image generation tool: `tools/generate-images.sh`
- Reference images for grounding: `brand/reference-images/tier{1,2,3,4}/`
