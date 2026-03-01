# MyAstraZeneca.co.uk — Visual Design & Layout Analysis

> Based on browser screenshots of 16 live pages taken February 2026
> These are all homepage/landing pages — gated subpage content was not accessible

---

## 1. Global Chrome (Header, Footer, Utility Bars)

### 1.1 Top Utility Bar (ever-present)

A thin bar at the very top of every page, full-width, light background:
- Left: "Prescribing Information [PRODUCT] (generic) United Kingdom" link + "Adverse Event Reporting" link
- These are magenta/dark text links on a white/light gray background
- Below it: a slightly darker bar with the HCP disclaimer: "This is a promotional website developed by AstraZeneca and intended for UK Healthcare Professionals only. Other UK residents please visit astrazeneca.co.uk"
- Font: small (~12-13px), sans-serif

**Some products have a colored top banner instead** — e.g. Forxiga has an orange/amber bar, Tezspire has a dark teal bar. These are product-branded accent bars.

### 1.2 Main Header/Navigation

- White background, full-width
- Left: **AstraZeneca logo** (gold/amber swirl icon + "AstraZeneca" wordmark in dark gray/black). The logo is roughly 150-180px wide.
- Center/Right: Main nav items as text links with dropdown chevrons:
  - **Products** (dropdown)
  - **Therapeutic Areas** (dropdown)
  - **About us** (dropdown)
  - **Contact us**
- Nav font: ~16px, medium weight, dark gray (#363b3b)
- Active/hover: magenta (#830051)
- Below the main nav: **Breadcrumb** trail — e.g. "AstraZeneca UK ► Forxiga" in small text

### 1.3 Product Sub-Navigation

Product pages have a **horizontal tab bar** below the breadcrumb:
- Tabs are text links separated by spacing, not visually boxed
- Examples: "Home | Efficacy and clinical trials | Safety profile | Dosing and administration | Mechanism of action | Resources"
- Active tab appears to have a magenta underline or bold treatment
- Font: ~14-15px, regular weight
- This bar is specific to each product and varies in items

### 1.4 Footer

Consistent across all pages, two sections:

**Adverse Event Reporting Box:**
- Centered, bordered box (light gray border, rounded corners)
- Bold text: "Adverse events should be reported..."
- Contains MHRA Yellow Card link + AZ contact link + phone number (0800 783 0033)

**Main Footer:**
- Light gray background (#f5f5f5 or similar)
- 3-column layout:
  - Left: AZ logo (gold swirl + wordmark), mission text about HCPs, "intended for doctors, nurses, and pharmacists in the UK"
  - Center: "Terms of use", "Privacy Policy" links
  - Right: "Cookie Policy", "Contact Us" links
- Below: Social icons (LinkedIn, X/Twitter) on left, "©2024 AstraZeneca. GB-XXXXX | Month Year" on right
- Font: small (~14px), gray text

---

## 2. Page Types Observed

### 2.1 Homepage (myastrazeneca.co.uk)

**Layout:**
1. Utility bars + Header
2. Large hero area — white background, left-aligned:
   - "Welcome to" (small gray text)
   - "MyAstraZeneca." (very large serif heading, dark gray/black)
3. "How can we help you today?" (large serif heading)
4. **3-column image card grid** — each card is a large square photo with a magenta CTA bar at the bottom:
   - "Review progression in Respiratory"
   - "Learn more about Cardiovascular"
   - "Explore our work in Oncology"
   - Images: abstract artistic/medical imagery (double exposure portraits with scientific visuals)
5. **Second row of 3 cards** — same pattern:
   - "Understand our work in Renal"
   - "Learn about our Childhood Flu Vaccine"
   - "See the latest in Metabolic"
6. Prescribing Information section (list of product PI links)
7. Contact us section
8. AE reporting box
9. Footer

**Key observations:**
- No hero image/banner — just text on white
- Cards use **photography with artistic double-exposure effects** (human silhouettes filled with scientific/medical imagery)
- CTA bars on cards are **magenta with white text**, rounded corners
- Very clean, spacious layout with generous whitespace
- The homepage is NOT product-focused — it's therapy-area focused

### 2.2 Therapy Area Pages (Respiratory, Cardiovascular, Oncology)

These follow a **consistent text-heavy template:**

1. Utility bars + Header + Breadcrumb
2. **Hero section**: Large serif heading on white background + optional hero image on right
   - Respiratory: "Transforming respiratory conditions in the UK" + blue-toned scientific illustration
   - Cardiovascular: "Cardiovascular disease: a growing concern" + pink-toned anatomical illustration
   - Oncology: "Oncology" + pink-toned portrait illustration
3. Introductory paragraph (body text, sans-serif, ~16px)
4. **"Our [therapy] focus areas"** heading
   - Sub-heading with brief description
   - **Accordion items** — disease areas listed as expandable rows with ">" chevrons:
     - e.g. "COPD >" and "Asthma >" for Respiratory
     - e.g. "Heart failure >" and "Heart failure and hyperkalaemia >" for Cardiovascular
     - For Oncology: "Breast cancer >", "Gastrointestinal (GI) cancers >", "Gynaecological and Genitourinary cancers >", "Lung cancers >"
5. **"The scale of the challenge"** — epidemiological data section (long-form text)
6. **"Our commitment to helping HCPs improve patient outcomes"** — bullet points of commitments
7. Oncology adds: **"Other focus areas"** with bullet list (Haematology, Ovarian cancer, Prostate cancer)
8. **"Research and innovation"** section (Cardiovascular)
9. Prescribing Information section
10. Abbreviations and References (expandable with ">")
11. AE reporting box
12. Footer

**Key observations:**
- These are long-form content pages, mostly text
- Accordion pattern used for navigation into sub-areas
- Hero images are **artistic illustrations, not photos** — double-exposure style
- Very generous whitespace between sections
- Headings use a **serif font** (appears to be a thin/light serif, similar to the design system's Lexia)
- Section headings are large (~36-46px), dark gray or black

### 2.3 Product Landing Pages — TWO distinct templates observed

#### Template A: "Rich/Visual Product Page" (Forxiga, Symbicort, Trixeo, Bevespi, Lokelma, Wainzua, Fluenz)

These are **content-rich, highly visual pages** with product-specific branding:

**Forxiga (dapagliflozin):**
1. **Product-branded top accent bar** (amber/orange)
2. Header + breadcrumb + **product sub-nav tabs** ("Welcome to Forxiga | Type 2 Diabetes | Chronic Kidney Disease | Heart Failure | Safety")
3. Product logo/wordmark + "dapagliflozin" in branded style
4. Hero: Large serif heading "Discover the cardiorenal protective benefits of Forxiga (dapagliflozin)" + large photo of a smiling patient (warm, lifestyle photography)
5. "About dapagliflozin" text section
6. **Alert/callout box** — teal/green icon + bold text about dosing (rounded border, icon-led)
7. **"Dapagliflozin is indicated for:"** — 3-column card grid:
   - Each card: heading, body text, magenta "Learn more" CTA button
   - Cards for: Type 2 Diabetes, Chronic Kidney Disease, Heart Failure
8. **"Safety profile"** — icon-led section (shield icon) with CTA
9. Abbreviations and References
10. AE box + Footer

**Symbicort:**
1. **Amber/gold accent brand bar**
2. Product hero with "Symbicort® (budesonide/formoterol) Turbohaler" + lifestyle imagery (jogger)
3. Sub-nav: "Discover Symbicort | Reliever Therapy | Resources | Dosing & Side Effects"
4. **3 product image cards** showing different Symbicort variants (with product packaging photos)
5. "Drug Information" section
6. **Large infographic** — circular diagram showing preventer/reliever therapy
7. Indication section
8. AE + Footer

**Trixeo / Bevespi:**
1. **Teal/mint accent brand color**
2. Product hero with device imagery
3. **Technical product sections**: combination details, device illustrations
4. **Dosing infographics** — "2 INHALATIONS + 2 INHALATIONS" with large typography
5. **Efficacy data callouts** — large percentage numbers (24%, 13%) with downward arrows in colored circles
6. **Resources section** with image card linking to expert content
7. **Contact section** with person photo

**Lokelma:**
1. **Teal/dark green accent**
2. Product hero with illustration (medicine sachet diagram)
3. **3-column icon grid** — teal circular icons with white symbols
4. **Video/content cards** — teal circular play button icons
5. "How it works" section with icons
6. **Safety profile** section
7. **FAQ accordion** section
8. **3-column resource cards** — icon + title + CTA

**Wainzua:**
1. **Green accent brand color**
2. Product hero with patient lifestyle photo (person in park)
3. **Benefit cards** — 3-column with green circular icons
4. **Data presentation** — bullet points with supporting text
5. **Accordion sections** for reimbursement
6. **Contact section** with CTA form

**Fluenz:**
1. **Light blue accent brand color**
2. Hero with "Flu protection without the injection" + child/parent photo
3. **Info cards** — importance of vaccination, eligibility
4. **Resource carousel** — horizontally scrollable cards with arrows
5. **CTA cards** — "Get in touch", "Sign up for more information"

#### Template B: "Indication Selector" (Imfinzi, Lynparza)

These multi-indication products use a **simpler, selector-based layout:**

**Imfinzi (durvalumab):**
1. Header + breadcrumb (AstraZeneca UK ► Lung Cancer)
2. Sub-nav: "Home | Efficacy and clinical trials | Safety profile | Dosing and administration | Mechanism of action | Resources"
3. Product wordmark "IMFINZI" with brand logo
4. **"Select Indication"** heading
5. **3-column indication cards** — each with:
   - Heading (indication name)
   - Body text (brief description)
   - **Magenta "Learn more" button** (filled)
   - Background image (landscape/nature photography — mountains, seas)
   - Cards: "Unresectable stage III Non-Small Cell lung cancer — PACIFIC", "Resectable IIA to IIIB Non-Small Cell lung cancer — AEGEAN", "Extensive Stage Small Cell lung cancer — CASPIAN"
6. PI reference link
7. Approval code
8. AE box + Footer

**Lynparza (olaparib):** — appears to be gated/empty content on landing (only sub-nav + AE + footer visible)

#### Template C: "Data-Forward Product Page" (Tezspire)

**Tezspire** has a unique, highly data-driven layout:

1. **Dark teal/navy branded accent bar** at top
2. Product logo "TEZSPIRE ▼" with black triangle
3. Hero: dramatic fire/aurora imagery with "Rise above the complexity with TEZSPIRE® (tezepelumab)"
4. "See full SmPC" link
5. **Key data headline** — "TEZSPIRE significantly reduces exacerbations in a broad population..." (key words in magenta bold)
6. **2-column data display:**
   - Left: "Navigator" — "56%" with downward arrow, supporting statistical text
   - Right: "Pathway" — "71%" with downward arrow, supporting statistical text
   - Each with magenta "GET EFFICACY DATA" CTA buttons
7. **Second data section** — "TEZSPIRE treats across phenotypes and irrespective of key clinical biomarker levels" with key words in magenta
8. "EXPLORE DATA" CTA
9. AE + Footer

---

## 3. Visual Design System

### 3.1 Color Usage

**Global brand colors:**
- **AZ Gold/Amber**: The AZ logo swirl is a warm gold (#EFAB00 area). Used in logo only at the global level.
- **Dark gray/near-black**: Primary text (#1B1B1B or #363b3b)
- **Magenta/Deep pink** (#830051 or #d0006f): Primary CTA color, link hover, active states
- **White**: Primary background

**Product-specific accent colors** (each product has its own brand color):
| Product | Accent Color | Usage |
|---|---|---|
| Forxiga | Amber/Orange | Top bar, highlights |
| Symbicort | Gold/Amber | Top bar, accents |
| Tezspire | Dark Teal/Navy | Top bar, data backgrounds |
| Trixeo | Mint/Teal | Backgrounds, icons, highlights |
| Bevespi | Pink/Rose | Backgrounds, accents |
| Lokelma | Dark Teal/Green | Icons, backgrounds, accents |
| Wainzua | Forest Green | Icons, accents, CTA |
| Fluenz | Light Blue/Sky | Backgrounds, accents |
| Imfinzi | Blue (AZ corporate) | Sub-nav, accents |
| Lynparza | Purple/Magenta | (from AZ primary) |
| Tagrisso | Blue | Header accents |

### 3.2 Typography

**Headings:** A **thin-weight serif** typeface (Lexia VF / LexiaThin). Characteristics:
- Very thin strokes with slight serif terminals
- Used for all major headings (H1, H2)
- Large sizes: H1 appears ~48-56px, H2 ~36-42px
- Color: dark gray/black (#1B1B1B) for most, occasionally product-accent colored
- Line height: tight (~1.1-1.2)

**Body text:** Clean sans-serif (Inter / Helvetica Neue family):
- Size: ~16px
- Color: #363b3b (dark gray)
- Line height: ~1.6
- Regular weight (400)

**Product names in text:** Bold weight, sometimes in product accent color
**Data/statistics:** Large display numerals (~72-96px), often with colored accent (magenta arrows)
**CTA button text:** ~14-16px, medium weight, white on magenta or product color

### 3.3 Imagery Style

Three distinct imagery approaches observed:

1. **Double-exposure artistic portraits**: Used on homepage and therapy area heroes. Human silhouettes filled with scientific/medical imagery (molecules, anatomy, cells). These are the most distinctive AZ visual element — abstract, premium, editorial feel.

2. **Lifestyle patient photography**: Used on product pages. Warm, natural-lit photos of diverse patients in everyday settings (walking outdoors, smiling). Not clinical — aspirational and positive.

3. **Dramatic/abstract hero imagery**: Used on data-forward products like Tezspire (aurora/fire imagery). Bold, attention-grabbing.

4. **Product photography**: Clean shots of inhalers, pens, packaging on neutral backgrounds. Used for device-focused products (Symbicort, Trixeo, Bevespi, Wainzua).

5. **Icon systems**: Circular icons with white symbols on colored backgrounds (teal, green). Used for feature/benefit grids. Flat/minimal style.

### 3.4 Spacing & Layout

- **Max content width**: ~1200px, centered
- **Section spacing**: Very generous — ~60-80px between major sections
- **Card grids**: 3-column on desktop, gutters ~24-30px
- **Card styling**: White background, subtle shadow or no border, rounded corners (8px)
- **CTA buttons**: Rounded corners (4-6px), padding ~12px 24px
- **Magenta CTA bars on cards**: Full-width within card, rounded bottom corners

---

## 4. Component Patterns

### 4.1 Card Patterns

**Image Card (Homepage)**:
- Square/landscape image filling top of card
- Magenta bar at bottom with white text + ">" arrow
- No visible border — image + CTA bar only

**Indication Card (Imfinzi)**:
- Background landscape photo
- White heading text overlay
- Body text (white or dark depending on image)
- Magenta "Learn more" button (filled, rounded)

**Product Variant Card (Symbicort)**:
- Product photo centered
- Heading below
- Brief description
- Magenta text link CTA

**Benefit/Feature Card (Lokelma, Wainzua)**:
- Circular colored icon at top (large, ~80px)
- Heading below
- Brief description text
- No CTA button (the card itself may be clickable)

**Resource Card (Fluenz)**:
- Image/thumbnail
- Title
- Brief description
- CTA button or link

### 4.2 Data Display Patterns

**Large Statistic Callout (Tezspire)**:
- Large percentage number (~72px, bold)
- Downward arrow icon (in product accent color)
- Supporting statistical text (CI, p-value)
- Trial name as heading above
- CTA button below

**Dosing Infographic (Trixeo, Bevespi)**:
- Large "2 INHALATIONS" text with plus sign
- "at the same time" / "twice a day" descriptor
- Visual emphasis through typography size contrast

### 4.3 Accordion Pattern

Used extensively on therapy area pages:
- Full-width row
- Left: heading text
- Right: ">" chevron
- Border-bottom separator
- Expands to show content below on click

### 4.4 Alert/Callout Box

- Bordered box (rounded corners, ~8px)
- Left icon (teal/product color)
- Bold heading + body text
- Used for important clinical information (dosing notes, safety info)

### 4.5 Contact Section

- Two-column layout
- Left: "Contact us" heading + description text
- Right: CTA button or form link
- Sometimes includes person photo (representative/medical contact)

---

## 5. Page Section Ordering (Canonical)

Based on observing all 16 pages, the canonical section ordering is:

1. **Product PI + AE Reporting utility bar** (thin, top of page)
2. **HCP disclaimer bar** (thin, below utility bar)
3. **Main header** (logo + nav)
4. **Breadcrumb**
5. **Product sub-navigation** (product pages only)
6. **Hero section** (heading + optional image/illustration)
7. **Main content** (varies by page type)
8. **Prescribing Information** (links to PI documents)
9. **Abbreviations and References** (expandable)
10. **Approval code + Date of Preparation** (e.g., "GB-64326 | DOP: February 2025")
11. **Adverse Event Reporting box** (bordered, centered)
12. **Footer** (3-column: mission text, legal links, social icons)

---

## 6. Key Design Principles Observed

1. **Each product is a mini-brand**: Products have their own accent color, imagery style, and personality. The AZ global chrome (header/footer) unifies them, but product pages feel distinct.

2. **Typography-led hierarchy**: The thin serif heading font creates a premium, editorial feel. It's the dominant visual element — not images or color.

3. **White space is a feature**: Extremely generous spacing. Pages breathe. No visual clutter.

4. **Data when it matters, story when it doesn't**: Therapy area pages are narrative (long-form text about disease burden). Product pages are data-forward (large statistics, trial results). The template matches the content purpose.

5. **Minimal UI chrome**: No heavy borders, no drop shadows, no gradients on containers. Cards are flat or very subtly elevated. The design is reductive — only essential visual elements.

6. **Imagery is editorial, not stock**: The double-exposure portraits and dramatic hero images feel curated and art-directed, not generic stock photography. This is a premium pharma brand, not a clinical resource.

7. **Regulatory elements are omnipresent but understated**: PI links, AE reporting, approval codes appear on every page but are visually secondary — smaller text, lighter styling, positioned at the bottom.

---

## 7. Mapping to Our EDS Block Library

| AZ Pattern | EDS Block | Notes |
|---|---|---|
| Hero with heading + image | `hero-teaser` | Product-branded hero sections |
| Therapy area accordion | `accordion` | Focus area navigation |
| 3-column image cards | `cards-teaser` | Homepage therapy cards, product indication cards |
| 2-column text + image | `columns-teaser` | Resources, contact sections |
| Section heading + subtitle | `title` | Section dividers |
| Introductory text | `introduction` | Disease context, product descriptions |
| Data display (large stats) | Custom / `columns` | May need styling for large numerals |
| Product sub-nav | Custom / Section metadata | Horizontal tab navigation |
| PI section | Default content | Text list of PI links |
| AE reporting box | Default content with section styling | Bordered centered box |
| Benefit icon grid | `cards-teaser` variant | Circular icons + text cards |
| Alert/callout box | Default content with section styling | Bordered box with icon |
| Contact section | `columns-teaser` | 2-column with CTA |
| Resource carousel | `carousel-teaser` | Horizontally scrollable cards |
| Embedded video/media | `embed` | Video content |
| Data tables | `table-data` | Clinical trial data |

---

## 8. Brand Voice Quick Reference

Based on actual copy observed on pages:

**Homepage tone**: Warm, inviting, supportive
- "Welcome to MyAstraZeneca."
- "How can we help you today?"

**Therapy area tone**: Authoritative, evidence-driven, urgent
- "Cardiovascular disease: a growing concern"
- "The scale of the challenge"
- "Our commitment to helping HCPs improve patient outcomes"

**Product tone**: Precise, clinical, data-focused
- "Discover the cardiorenal protective benefits of Forxiga"
- "TEZSPIRE significantly reduces exacerbations"
- "Rise above the complexity with TEZSPIRE®"

**CTA patterns observed**:
- "Review progression in [area]"
- "Learn more about [topic]"
- "Explore our work in [area]"
- "GET EFFICACY DATA"
- "EXPLORE DATA"
- "Find out more"
- "Learn more"

---

## Sources

All analysis based on Playwright browser screenshots taken 27 February 2026 from:
- https://www.myastrazeneca.co.uk/ (homepage)
- https://www.myastrazeneca.co.uk/respiratory.html
- https://www.myastrazeneca.co.uk/cardiovascular.html
- https://www.myastrazeneca.co.uk/oncology.html
- https://www.myastrazeneca.co.uk/forxiga.html
- https://www.myastrazeneca.co.uk/symbicort.html
- https://www.myastrazeneca.co.uk/tezspire.html
- https://www.myastrazeneca.co.uk/trixeo.html
- https://www.myastrazeneca.co.uk/bevespi.html
- https://www.myastrazeneca.co.uk/tagrisso/lung-cancer.html
- https://www.myastrazeneca.co.uk/imfinzi/lung-cancer.html
- https://www.myastrazeneca.co.uk/lynparza.html
- https://www.myastrazeneca.co.uk/lokelma.html
- https://www.myastrazeneca.co.uk/fluenz.html
- https://www.myastrazeneca.co.uk/wainzua.html
- https://www.myastrazeneca.co.uk/about-us.html

Screenshots stored in: `analysis/screenshots/`
