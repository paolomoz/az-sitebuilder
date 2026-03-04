# ELUVION (eluvionimab) — Site Briefing

## Drug Profile

- **Brand name:** ELUVION
- **Generic name:** eluvionimab
- **Class:** [Drug class — e.g. First-in-class selective monoclonal antibody / small molecule inhibitor]
- **Indication:** [Exact SmPC indication language — e.g. "Treatment of adult patients with [Target Disease] who have [qualifying criteria]"]
- **Brand colour:** Sapphire Blue #1A5B8C
- **Approval:** MHRA approved, [Month Year]

## Mechanism of Action

[Describe the mechanism factually. Example structure below — replace with real data.]

Eluvionimab is a [drug class] that [mechanism]. By [action on target], eluvionimab:

- [Effect 1 on disease pathway]
- [Effect 2 on disease pathway]
- [Effect 3 on disease pathway]
- [Effect 4 — differentiation from existing therapies]

[One paragraph explaining why this mechanism is differentiated from existing approaches.]

## Dosing

- **Formulation:** [e.g. 100 mg/mL solution for injection in a pre-filled syringe]
- **Recommended dose:** [e.g. 100 mg intravenous infusion every 3 weeks]
- **Administration:** [Route, setting, duration]
- **Loading dose:** [If applicable]
- **Storage:** [Temperature requirements]
- **Dose adjustments:** [Body weight, renal/hepatic impairment, age]

## Clinical Programme: [PROGRAMME NAME]

### [TRIAL-1] (Phase III, pivotal — [Primary objective])

- **Design:** Randomised, double-blind, placebo-controlled, multicentre, [duration]
- **Population:** [N] adults with [disease criteria], [key inclusion criteria]
- **Primary endpoint:** [Endpoint name] at [timepoint]
- **Key results:**
  - [Primary endpoint]: **[ELUVION result] vs [comparator result]** ([magnitude of effect]; [rate ratio/hazard ratio], 95% CI: [range]; P[value])
  - [Key secondary 1]: **[result]** (P[value])
  - [Key secondary 2]: **[result]** (P[value])
  - [Key secondary 3]: **[result]**

### [TRIAL-2] (Phase III, pivotal — [Primary objective])

- **Design:** Randomised, double-blind, [comparator]-controlled, multicentre, [duration]
- **Population:** [N] adults with [disease criteria]
- **Primary endpoint:** [Endpoint name] at [timepoint]
- **Key results:**
  - [Primary endpoint]: **[result]** ([statistic]; P[value])
  - [Key secondary 1]: **[result]** (P[value])
  - [Key secondary 2]: **[result]** (P[value])

## Safety Profile (Pooled data, n=[total])

### Most common adverse events (&ge;3%)

| Adverse Event | ELUVION (n=[N]) | Placebo (n=[N]) |
|---|---|---|
| [AE 1] | [%] | [%] |
| [AE 2] | [%] | [%] |
| [AE 3] | [%] | [%] |
| [AE 4] | [%] | [%] |
| [AE 5] | [%] | [%] |

### Key safety findings

- **Serious adverse events:** [%] vs [%] placebo
- **Treatment discontinuation due to AEs:** [%] vs [%]
- **Infections:** [Summary of infection rates and notable findings]
- **[Other notable AE]:** [Details]
- **Immunogenicity:** [Anti-drug antibody rates and clinical impact]

### Special populations

- **Pregnancy:** [SmPC language]
- **Breastfeeding:** [SmPC language]
- **Elderly (&ge;65 years):** [Dose adjustment requirements and data limitations]
- **Renal/hepatic impairment:** [Dose adjustment requirements]

---

## Page Content

**IMPORTANT:** All copy below is final approved copy from the product and marketing team. It must be used exactly as written when generating site pages. Map the copy to the most appropriate block types but do not modify any text, headings, or link labels. Image alt text may be adapted to the generated images.

**Navigation pages:** Home, Efficacy Data, Safety, Dosing, Mechanism of Action, Resources

### Page 1: Home (index.plain.html)

#### Section 1 — Hero
**Block:** hero-teaser
**Image:** hero-home.jpeg (16:9, 1440&times;810)
**Image prompt:** "Wide 16:9 hero image. Double exposure portrait of a [patient demographic appropriate to disease] in profile, silhouette filled with abstract [disease-relevant scientific imagery] in sapphire blue and white tones. Clean white background. Editorial pharmaceutical style, aspirational, calm. No text."

```
ELUVION (eluvionimab)
[Benefit-led headline using SmPC indication language — e.g. "A new approach to [Target Disease] in adult patients with [qualifying criteria]"].&sup1;
[Explore the [PROGRAMME] data](/eluvion/efficacy-data)
```

#### Section 2 — Key data carousel
**Block:** carousel-teaser

Slide 1:
- **Image:** card-efficacy.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Abstract representation of [disease-relevant improvement] in sapphire blue and white, with golden light accents. Clean pharmaceutical editorial style, no text."

```
[Key statistic — e.g. "XX% improvement in [primary endpoint] at [timepoint]"]
In [TRIAL-1], ELUVION [achieved/demonstrated] [primary result] compared with [comparator] in [patient population] (rate ratio [X.XX]; 95% CI: [range]; P<[value]).&sup1;
[View [PROGRAMME] efficacy data](/eluvion/efficacy-data)
```

Slide 2:
- **Image:** card-safety.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Warm photograph of a healthcare professional and patient in a consultation, sapphire blue colour accents in the background. Editorial medical style, natural light."

```
[Safety headline — e.g. "A well-characterised safety profile"]
[Key safety finding — e.g. "Serious adverse events occurred in X% of ELUVION-treated patients compared with Y% in the placebo group"].&sup1;
[Review the safety profile](/eluvion/safety)
```

Slide 3:
- **Image:** card-dosing.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Clean product-style photograph of [device/formulation] against a white background with subtle sapphire blue gradient. Sharp detail, pharmaceutical product photography."

```
[Dosing headline — e.g. "Simple [frequency] dosing"]
[Key dosing information from SmPC — e.g. "ELUVION [dose] [route] every [interval]. [Key convenience feature]"].&sup1;
[See dosing and administration](/eluvion/dosing)
```

#### Section 3 — Disease context
**Block:** introduction
**Section metadata:** Style: light

```
[Target Disease]: [evidence-led framing headline — e.g. "a persistent challenge in [therapy area]"]
[2-3 sentences of epidemiological context with UK-specific statistics and superscript reference numbers. Use NHS/NICE/MHRA sources. Frame the unmet need factually, without dramatisation.]&sup1; &sup2;
```

#### Section 4 — Mechanism teaser
**Block:** columns-teaser
**Section metadata:** Style: highlight

- **Image:** moa-preview.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Scientific illustration showing [target/pathway] with [drug mechanism of action]. Sapphire blue and white colour palette with warm amber accents. Clean editorial pharmaceutical illustration."

```
[Mechanism headline — e.g. "Targeting [pathway] at [level]"]
[2-3 sentences explaining the mechanism factually. Reference how this translates to clinical outcomes.]&sup1;
[Explore how ELUVION works](/eluvion/mechanism-of-action)
```

#### Section 5 — Prescribing information accordion
**Block:** accordion

```
Prescribing Information | ELUVION (eluvionimab) Prescribing Information. Please refer to the full Summary of Product Characteristics (SmPC) before prescribing. ELUVION [formulation details]. Each [unit] contains [dose] eluvionimab. Indication: [SmPC indication language]. Posology: [Dosing regimen]. Contraindications: Hypersensitivity to the active substance or any excipient.
Adverse Event Reporting | Adverse events should be reported. Reporting forms and information can be found at www.mhra.gov.uk/yellowcard or search for MHRA Yellow Card in the Google Play or Apple App Store. Adverse events should also be reported to AstraZeneca by visiting https://contactazmedical.astrazeneca.com/ or by calling 0800 783 0033.
References | 1. ELUVION (eluvionimab) Summary of Product Characteristics. AstraZeneca UK Ltd. 2. [Epidemiology reference]. 3. [MOA reference]. 4. [TRIAL-1 publication]. 5. [TRIAL-2 publication].
```

#### Page Metadata
```
Title | Eluvion (eluvionimab) | HCP Resources | AstraZeneca UK
Description | ELUVION (eluvionimab) is [drug class summary]. Explore [PROGRAMME] clinical data, safety profile, and dosing information for UK healthcare professionals.
Approval Code | GB-XXXXX | DOP: [Month Year]
```

---

### Page 2: Efficacy Data (efficacy-data.plain.html)

#### Section 1 — Hero
**Block:** hero-teaser
**Image:** hero-efficacy.jpeg (16:9, 1440&times;810)
**Image prompt:** "Wide 16:9 hero image. Double exposure portrait of a [patient demographic] looking forward with confidence, silhouette filled with abstract data visualisation elements — declining curves, data points in sapphire blue and gold. Clean white background. Editorial pharmaceutical style."

```
Clinically meaningful improvements across the [PROGRAMME] programme
ELUVION demonstrated [summary of key outcomes across trials].&sup1; &sup2;
```

#### Section 2 — Programme overview
**Block:** introduction
**Section metadata:** Style: light

```
The [PROGRAMME] clinical programme
[PROGRAMME] was a comprehensive Phase III programme evaluating eluvionimab in [total patient number] patients with [disease] across [number] pivotal, randomised, [comparator]-controlled trials: [TRIAL-1] ([primary objective]) and [TRIAL-2] ([primary objective]).&sup1; &sup2;
```

#### Section 3 — Trial data tabs
**Block:** tabs-large

Tab 1 — [TRIAL-1]: [Primary objective]:
- **Image:** trial1-results.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Bold typographic data visualisation showing [key statistic]% in large sapphire blue numerals against a clean white background, with an abstract [improvement/reduction] motif. Modern pharmaceutical data presentation."

```
[TRIAL-1]: [headline result — e.g. "XX% reduction in [endpoint] over [duration]"]
[Detailed result paragraph with full statistical context: treatment difference, rate ratio/hazard ratio, 95% CI, P-value. Include key secondary endpoints with statistics.]&sup1;

| Endpoint | ELUVION (n=[N]) | [Comparator] (n=[N]) | Treatment difference |
| [Primary endpoint] | [result] | [result] | [effect size]; [statistic] ([CI]); P[value] |
| [Secondary endpoint 1] | [result] | [result] | [difference]; P[value] |
| [Secondary endpoint 2] | — | — | [statistic] ([CI]); P[value] |
| [Secondary endpoint 3] | [result] | [result] | P[value] |

[Download the [TRIAL-1] study summary](/eluvion/resources)
```

Tab 2 — [TRIAL-2]: [Primary objective]:
- **Image:** trial2-results.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Bold typographic data visualisation showing [key statistic]% in large sapphire blue numerals against a clean white background. Modern pharmaceutical data presentation."

```
[TRIAL-2]: [headline result]
[Detailed result paragraph with statistics.]&sup2;

| Endpoint | ELUVION (n=[N]) | [Comparator] (n=[N]) | Treatment difference |
| [Primary endpoint] | [result] | [result] | P[value] |
| [Secondary endpoint 1] | [result] | [result] | P[value] |
| [Secondary endpoint 2] | [result] | [result] | [difference]; P[value] |

[Download the [TRIAL-2] study summary](/eluvion/resources)
```

#### Section 4 — Prescribing information accordion
**Block:** accordion

(Same accordion content as Home page)

#### Page Metadata
```
Title | [PROGRAMME] Data | Eluvion (eluvionimab) | AstraZeneca UK
Description | Explore the [PROGRAMME] clinical programme: pivotal Phase III trial data for ELUVION (eluvionimab) in [Target Disease].
```

---

### Page 3: Safety (safety.plain.html)

#### Section 1 — Page header (no hero image)
**Block:** title

```
Safety profile of ELUVION
The safety of ELUVION was evaluated in [N] patients with [disease] across the [PROGRAMME] programme, with a median exposure of [duration].&sup1; &sup2;
```

#### Section 2 — Safety overview
**Block:** introduction
**Section metadata:** Style: light

```
[Safety headline — e.g. "A well-characterised safety profile"]
[2-3 sentences summarising key safety findings: SAE rates, discontinuation rates, infection rates, with comparator data. All referenced.]&sup1; &sup2;
```

#### Section 3 — Adverse events table
**Block:** table-data

```
| Adverse Event | ELUVION (n=[N]) | Placebo (n=[N]) |
| [AE 1] | [%] | [%] |
| [AE 2] | [%] | [%] |
| [AE 3] | [%] | [%] |
| [AE 4] | [%] | [%] |
| [AE 5] | [%] | [%] |
| Serious adverse events | [%] | [%] |
| Discontinuation due to AEs | [%] | [%] |
```

#### Section 4 — Safety considerations cards
**Block:** cards-teaser

Card 1:
- **Image:** safety-card1.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Clean flat illustration of a [relevant safety icon] in sapphire blue and white. Modern pharmaceutical instructional style, clean white background."

```
[Safety topic 1 heading]
[Factual description of the safety consideration, incidence rates, clinical significance, and management guidance. Referenced.]&sup1;
```

Card 2:
- **Image:** safety-card2.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Clean flat illustration of a [relevant safety icon] in sapphire blue and white. Modern pharmaceutical instructional style, clean white background."

```
[Safety topic 2 heading]
[Factual description with incidence rates and management recommendations. Referenced.]&sup1;
```

Card 3:
- **Image:** safety-card3.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Clean flat illustration of a [relevant safety icon] in sapphire blue and amber on white. Modern pharmaceutical instructional style."

```
[Safety topic 3 heading]
[Factual description with management guidance. Referenced.]&sup1;
```

#### Section 5 — Special populations
**Block:** columns-teaser
**Section metadata:** Style: highlight
**Image:** special-populations.jpeg (4:3, 800&times;600)
**Image prompt:** "4:3 aspect ratio. Warm photograph of an older adult in a comfortable everyday setting — garden, living room, or park bench. Natural light, warm golden tones with sapphire blue accent. Editorial pharmaceutical lifestyle, calm and dignified."

```
Special populations
Pregnancy: [SmPC language for pregnancy, verbatim].&sup1;
Elderly patients: [SmPC language for elderly, verbatim].&sup1;
[Additional populations as applicable — adolescents, renal/hepatic impairment].&sup1;
```

#### Section 6 — Prescribing information accordion
**Block:** accordion

(Same accordion content as Home page)

#### Page Metadata
```
Title | Safety | Eluvion (eluvionimab) | AstraZeneca UK
Description | Review the safety profile of ELUVION (eluvionimab) from the [PROGRAMME] programme, including adverse events, special populations, and key safety considerations.
```

---

### Page 4: Dosing (dosing.plain.html)

#### Section 1 — Hero
**Block:** hero-teaser
**Image:** hero-dosing.jpeg (16:9, 1440&times;810)
**Image prompt:** "Wide 16:9 hero image. Clean, bright photograph of [device/formulation] in context — [e.g. pre-filled syringe on a clean surface, infusion setup]. Light background with sapphire blue and white tones. Modern pharmaceutical product photography, clean and reassuring, natural light."

```
[Dosing headline — e.g. "Simple [frequency] [administration route]"]
[Key dosing summary from SmPC — dose, route, frequency, key convenience features. Referenced.]&sup1;
```

#### Section 2 — Administration steps
**Block:** cards-teaser

Card 1:
- **Image:** step-1.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. [Image appropriate to step 1 — e.g. physician reviewing patient eligibility, clinical setting with sapphire blue accents, natural light, professional editorial medical photography.]"

```
Step 1: [Step heading — e.g. "Assess eligibility"]
[Detailed step description from SmPC — eligibility criteria, pre-treatment screening, baseline assessments. Referenced.]&sup1;
```

Card 2:
- **Image:** step-2.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. [Image appropriate to step 2 — e.g. treatment initiation, dose preparation, patient training. Sapphire blue accents, natural light.]"

```
Step 2: [Step heading — e.g. "Initiate treatment"]
[Detailed step description — dose, route, duration, monitoring requirements. Referenced.]&sup1;
```

Card 3:
- **Image:** step-3.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. [Image appropriate to step 3 — e.g. ongoing monitoring, follow-up scheduling. Sapphire blue accents, warm natural setting.]"

```
Step 3: [Step heading — e.g. "Monitor and follow up"]
[Detailed step description — monitoring schedule, dose adjustments, when to discontinue. Referenced.]&sup1;
[Access patient support materials](/eluvion/resources)
```

#### Section 3 — Dosing overview
**Block:** introduction
**Section metadata:** Style: light

```
[Dosing convenience headline]
[1-2 sentences highlighting key dosing advantages — no loading dose, fixed dosing, no weight adjustment, etc. Referenced.]&sup1;
```

#### Section 4 — Storage and handling
**Block:** columns-teaser
**Section metadata:** Style: highlight
**Image:** storage.jpeg (4:3, 800&times;600)
**Image prompt:** "4:3 aspect ratio. Clean product photograph showing [formulation/device] with storage context — original packaging, appropriate temperature indicator. Sapphire blue and white colour palette. Modern pharmaceutical instructional style."

```
Storage and handling
[Verbatim SmPC storage instructions — temperature, light protection, shelf life, in-use stability. Referenced.]&sup1;
[Preparation instructions if applicable — reconstitution, dilution, inspection.]&sup1;
```

#### Section 5 — Prescribing information accordion
**Block:** accordion

(Same accordion content as Home page)

#### Page Metadata
```
Title | Dosing | Eluvion (eluvionimab) | AstraZeneca UK
Description | ELUVION (eluvionimab) dosing and administration guide: [key dosing summary] for healthcare professionals.
```

---

### Page 5: Mechanism of Action (mechanism-of-action.plain.html)

#### Section 1 — Hero
**Block:** hero-teaser
**Image:** hero-moa.jpeg (16:9, 1440&times;810)
**Image prompt:** "Wide 16:9 hero image. Abstract scientific illustration of [target pathway/mechanism] with [drug action]. Sapphire blue and deep teal colour palette with warm amber accents. Dark background with luminous sapphire elements. Editorial pharmaceutical CGI style."

```
[MOA headline — e.g. "Targeting [pathway]: [mechanistic summary]"]
[1-2 sentences describing the mechanism at a high level, linking to clinical relevance. Referenced.]&sup1;
```

#### Section 2 — Disease pathway
**Block:** columns-teaser
**Image:** pathway-disease.jpeg (4:3, 800&times;600)
**Image prompt:** "4:3 aspect ratio. Scientific illustration of [disease pathway step 1 — e.g. target overexpression, pathway activation]. Sapphire blue and white colour palette with warm amber accents for disease-state elements. Clean pharmaceutical illustration style."

```
[Disease pathway heading — e.g. "The role of [target] in [disease]"]
[2-3 sentences explaining the pathological role of the target in the disease. Evidence-led, referenced. No emotive language.]&sup1; &sup3;
```

#### Section 3 — Cascade/pathway detail
**Block:** columns-teaser
**Section metadata:** Style: highlight
**Image:** pathway-cascade.jpeg (4:3, 800&times;600)
**Image prompt:** "4:3 aspect ratio. Scientific illustration showing [downstream effects of target] — [disease manifestations]. Sapphire blue base with amber pathways. Modern pharmaceutical illustration, editorial quality."

```
[Cascade heading — e.g. "How [target dysregulation] drives [disease features]"]
[2-3 sentences explaining downstream effects of the target in disease pathology. Referenced.]&sup1; &sup3;
```

#### Section 4 — Drug mechanism
**Block:** columns-teaser
**Image:** drug-mechanism.jpeg (4:3, 800&times;600)
**Image prompt:** "4:3 aspect ratio. Scientific illustration showing [drug] interacting with [target] — blocking/inhibiting/neutralising. Clean composition showing the therapeutic effect. Sapphire blue and white, modern pharmaceutical editorial."

```
[Drug mechanism heading — e.g. "ELUVION: [mechanism description]"]
[2-3 sentences explaining how eluvionimab acts on the target, translating mechanism to clinical outcomes with data references.]&sup1; &sup4;
[View [PROGRAMME] clinical data](/eluvion/efficacy-data)
```

#### Section 5 — Why this target matters
**Block:** introduction
**Section metadata:** Style: light

```
[Target rationale heading — e.g. "Why [target] matters in [disease]"]
[1-2 sentences summarising the therapeutic rationale for targeting this pathway. Referenced.]&sup1; &sup3;
```

#### Section 6 — Prescribing information accordion
**Block:** accordion

(Same accordion content as Home page)

#### Page Metadata
```
Title | Mechanism of Action | Eluvion (eluvionimab) | AstraZeneca UK
Description | Understand the [target/pathway] and how ELUVION (eluvionimab) [mechanism summary] in [Target Disease].
```

---

### Page 6: Resources (resources.plain.html)

#### Section 1 — Page header (no hero image)
**Block:** title

```
Resources for you and your patients
Access prescribing information, patient support materials, and clinical summaries to support your patients treated with ELUVION.
```

#### Section 2 — Resource cards
**Block:** cards-teaser

Card 1:
- **Image:** resource-prescribing.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Clean flat illustration of a clinical document with a sapphire blue header and a checkmark icon. White background, minimal modern pharmaceutical style."

```
Prescribing information
Access the full Summary of Product Characteristics, patient information leaflet, and a dosing quick reference card for ELUVION.
[Access prescribing information](/eluvion/resources)
```

Card 2:
- **Image:** resource-patient.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Warm photograph of a patient information booklet open on a clean surface next to [device/formulation]. Sapphire blue cover, natural light, instructional feel."

```
Patient support materials
Download patient information guides, treatment diaries, and support resources to help your patients understand and manage their treatment with ELUVION.
[Download patient materials](/eluvion/resources)
```

Card 3:
- **Image:** resource-clinical.jpeg (4:3, 800&times;600)
- **Image prompt:** "4:3 aspect ratio. Modern illustration of a document with graphs and data visualisations in sapphire blue, surrounded by subtle clinical icons. Clean white background, flat pharmaceutical style."

```
[PROGRAMME] study summaries
Review concise summaries of the [TRIAL-1] and [TRIAL-2] pivotal trials, including study design, key endpoints, and headline results.
[Download study summaries](/eluvion/resources)
```

#### Section 3 — Supporting text
**Block:** introduction
**Section metadata:** Style: light

```
Supporting [disease] management in practice
From prescribing guides to clinical data summaries, we provide resources to help you integrate ELUVION into your [disease] management pathway and support your patients through treatment initiation and beyond.
```

#### Section 4 — Medical information contact
**Block:** columns-teaser
**Section metadata:** Style: highlight
**Image:** contact-medical.jpeg (4:3, 800&times;600)
**Image prompt:** "4:3 aspect ratio. Warm photograph of a medical information specialist at a modern desk with a laptop. Natural light, sapphire blue accents. Professional and approachable."

```
Medical information and support
For medical information enquiries about ELUVION, please contact AstraZeneca Medical Information:
Telephone: 0800 783 0033
Email: medicalinformationuk@astrazeneca.com
Website: contactazmedical.astrazeneca.com
Our medical information team is available Monday to Friday, 9:00 AM to 5:00 PM.
```

#### Section 5 — Prescribing information accordion
**Block:** accordion

(Same accordion content as Home page)

#### Page Metadata
```
Title | Resources | Eluvion (eluvionimab) | AstraZeneca UK
Description | Access prescribing information, patient support materials, and [PROGRAMME] study summaries for ELUVION (eluvionimab) in [Target Disease].
```

---

## Nav and Footer

### Navigation
```
Top bar: Contact Us | AZ Employee Login
Logo: AstraZeneca (CDN)
Pages: Home, Efficacy Data, Safety, Dosing, Mechanism of Action, Resources
CTA: Login
```

### Footer
```
Logo: AstraZeneca (CDN)
Approval: GB-XXXXX | DOP: [Month Year]
Copyright: [Copyright line — e.g. "© 2026 AstraZeneca UK Limited. All rights reserved."]
Page links: Home, Efficacy Data, Safety, Dosing, Mechanism of Action, Resources
Regulatory links: Report Adverse Event, Medical Information, Privacy Policy, Terms of Use, Accessibility
Date of Preparation: [Month Year]
```

---

## Image Generation Summary

### Hero Images (16:9, 1440&times;810) — 4 heroes (Safety and Resources use title block)
1. hero-home.jpeg — Double exposure portrait, [patient demographic], [disease-relevant imagery], sapphire blue
2. hero-efficacy.jpeg — Double exposure portrait, [patient demographic], data visualisation elements, sapphire blue/gold
3. hero-dosing.jpeg — [Device/formulation] product photography, clean sapphire blue/white
4. hero-moa.jpeg — Abstract [pathway/target] illustration, dark sapphire blue/amber

### Carousel/Card Images (4:3, 800&times;600)
5. card-efficacy.jpeg — Abstract [disease improvement] representation, sapphire blue/gold
6. card-safety.jpeg — HCP and patient consultation, sapphire blue accent
7. card-dosing.jpeg — [Device/formulation] product photography, sapphire blue

### Content Images (4:3, 800&times;600)
8. moa-preview.jpeg — [Drug-target interaction] illustration, sapphire blue/amber
9. trial1-results.jpeg — Bold [key statistic]% data visualisation, sapphire blue
10. trial2-results.jpeg — Bold [key statistic]% data visualisation, sapphire blue
11. special-populations.jpeg — Older adult in everyday setting, warm gold/sapphire
12. storage.jpeg — [Formulation/device] with packaging, sapphire blue/white
13. pathway-disease.jpeg — [Disease pathway] scientific illustration, sapphire blue/amber
14. pathway-cascade.jpeg — [Downstream effects] illustration, sapphire blue/amber
15. drug-mechanism.jpeg — [Drug-target interaction] illustration, sapphire blue
16. contact-medical.jpeg — Medical information specialist, sapphire blue accents

### Safety Cards (4:3, 800&times;600)
17. safety-card1.jpeg — [Safety topic] flat illustration, sapphire blue
18. safety-card2.jpeg — [Safety topic] flat illustration, sapphire blue
19. safety-card3.jpeg — [Safety topic] flat illustration, sapphire blue/amber

### Dosing Cards (4:3, 800&times;600)
20. step-1.jpeg — [Eligibility assessment] clinical setting, sapphire blue
21. step-2.jpeg — [Treatment initiation] clinical/patient setting, sapphire blue
22. step-3.jpeg — [Monitoring/follow-up] warm setting, sapphire blue

### Resource Cards (4:3, 800&times;600)
23. resource-prescribing.jpeg — Clinical document illustration, flat sapphire blue
24. resource-patient.jpeg — Patient information booklet, sapphire blue
25. resource-clinical.jpeg — Document with data visualisations, flat sapphire blue
