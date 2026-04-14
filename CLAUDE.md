# AZ Sitebuilder

Multi-site AEM Edge Delivery Services project for AstraZeneca drug launch HCP websites.
One shared codebase (blocks, styles, scripts) serving multiple sites via URL-prefixed subfolders.

See @AGENTS.md for EDS fundamentals. See `blocks/BLOCK-REFERENCE.md` for block HTML markup structures.

## Architecture

```
az-sitebuilder/
├── blocks/           # Shared AZ design system (18 blocks)
├── styles/           # Shared AZ brand styles
├── scripts/          # Shared scripts (multi-site nav auto-detection)
├── fonts/            # AZ brand fonts (Roboto family)
├── icons/            # Shared icons (AZ logo, search)
├── tools/            # Multi-site aware CLI tools
├── brand/            # AZ brand guidelines (voice, visual analysis)
├── sites/            # Per-site config (briefing, image prompts)
│   └── {sitename}/
│       ├── briefing.md
│       └── image-prompts.sh
├── drafts/           # Per-site local content (mirrors DA structure)
│   └── {sitename}/
│       ├── index.plain.html
│       ├── nav.plain.html
│       ├── footer.plain.html
│       └── *.plain.html
├── images/           # Generated images (not committed)
│   └── {sitename}/
├── fstab.yaml        # DA content source: /paolomoz/az-sitebuilder/
└── .env              # API keys (not committed)
```

## Multi-Site Navigation

Header and footer blocks auto-detect the site prefix from the URL path.
When at `/{sitename}/efficacy`, nav loads from `/{sitename}/nav` and footer from `/{sitename}/footer`.
All links in nav and footer must use `/{sitename}/` prefix. Logo and search icon must use CDN URLs.

### Nav Template (`drafts/{sitename}/nav.plain.html`)

<!-- Top-bar URLs below are AZ-wide defaults. If the briefing specifies different URLs, use those instead. -->

```html
<div>
  <p><a href="https://www.astrazeneca.co.uk/contact-us.html">Contact Us</a> | <a href="https://login.astrazeneca.com">AZ Employee Login</a></p>
  <div class="section-metadata">
    <div>
      <div>Style</div>
      <div>top</div>
    </div>
  </div>
</div>
<hr>
<div>
  <p><a href="/{sitename}/"><img src="https://{sitename}-images.pages.dev/astrazeneca-logo.png" alt="AstraZeneca" width="216" height="52"></a></p>
</div>
<hr>
<div>
  <ul>
    <li><a href="/{sitename}/{page-slug}">Page Name</a></li>
    <!-- one <li> per nav page from the briefing; nest <ul> for dropdowns -->
  </ul>
</div>
<hr>
<div>
  <p><a href="/{sitename}/"><img src="https://{sitename}-images.pages.dev/search.svg" alt="Search"></a></p>
  <p><strong><a href="/{sitename}/">Login</a></strong></p>
</div>
```

### Footer Template (`drafts/{sitename}/footer.plain.html`)

<!-- If the briefing specifies different footer text (copyright, trademark, URLs), use the briefing's text verbatim. -->

```html
<div>
  <p><a href="/{sitename}/"><img src="https://{sitename}-images.pages.dev/astrazeneca-logo.png" alt="AstraZeneca"></a></p>
  <p>{approval-code} | DOP: {date-of-preparation}</p>
  <p>{copyright-line-from-briefing}</p>
</div>
<hr>
<div>
  <!-- one <p> per nav page -->
  <p><a href="/{sitename}/{page-slug}">Page Name</a></p>
</div>
<hr>
<div>
  <p><a href="https://yellowcard.mhra.gov.uk/">Report Adverse Event</a></p>
  <p><a href="https://contactazmedical.astrazeneca.com/">Medical Information</a></p>
  <p><a href="https://www.astrazeneca.co.uk/our-company/privacy-notice.html">Privacy Policy</a></p>
  <p><a href="https://www.astrazeneca.co.uk/our-company/terms-of-use.html">Terms of Use</a></p>
  <p><a href="https://www.astrazeneca.co.uk/accessibility.html">Accessibility</a></p>
</div>
<hr>
<div>
  <p>Date of Preparation: {date-of-preparation}</p>
</div>
```

## DA Integration

- DA org: `paolomoz`, repo: `az-sitebuilder`
- Content URL: `https://da.live/#/paolomoz/az-sitebuilder/{sitename}`
- Each site is a subfolder in DA: `/paolomoz/az-sitebuilder/velostra/`, `/paolomoz/az-sitebuilder/clareon/`, etc.
- Credentials in `.env` (see `.env.example`)

## Tools (all require site name as first arg)

```bash
# Upload site drafts to DA
./tools/upload-to-da.sh velostra

# Trigger AEM preview CDN refresh
./tools/preview-all.sh velostra

# Generate AI images (reads sites/{sitename}/image-prompts.sh)
./tools/generate-images.sh velostra

# Deploy images to Cloudflare Pages CDN
./tools/deploy-images.sh velostra

# Take screenshots of local dev server
node tools/screenshot-local.js velostra
```

## Dev Server

```bash
npm install
npx @adobe/aem-cli up --no-open --html-folder drafts
# Pages available at http://localhost:3000/{sitename}/
# e.g. http://localhost:3000/velostra/efficacy
```

## Available Blocks

accordion, action-bar, cards-teaser, carousel-teaser, columns-teaser,
embed, footer, fragment, header, hero-teaser, image, introduction, table-data,
tabs-large, title

## Brand Guidelines

- Visual analysis: `brand/myastrazeneca-analysis.md`
- Brand voice & imagery: `brand/az-brand-voice.md`
- Consult these when writing copy, selecting imagery, or making design decisions.

## AZ Brand Quick Reference

- Primary: AZ Magenta #830051
- Secondary: AZ Gold #EFAB00
- CTA buttons: Pink #d0006f (hover: #a30058)
- Headings: Roboto Condensed Bold, color #830051
- Body: Roboto Regular, color #363b3b
- Light sections: #f8f8f8, Highlight sections: #f4eef2 with #830051 border-top

## Workflow for Creating a New Site

1. **Create briefing**: Write `sites/{sitename}/briefing.md` with product info, page content, block types
2. **Generate images**: Create `sites/{sitename}/image-prompts.sh`, run `./tools/generate-images.sh {sitename}`
3. **Deploy images to CDN**: `./tools/deploy-images.sh {sitename}` → `https://{sitename}-images.pages.dev/`
4. **Create drafts**: Write `drafts/{sitename}/*.plain.html` using CDN image URLs
5. **Test locally**: `npx @adobe/aem-cli up --html-folder drafts` → `http://localhost:3000/{sitename}/`
6. **Upload to DA**: `./tools/upload-to-da.sh {sitename}`
7. **Preview on AEM CDN**: `./tools/preview-all.sh {sitename}`
8. **Screenshot & QA**: `node tools/screenshot-local.js {sitename}`

## Skill Source Code

When asked to "update the skill" or "fix the skill", edit the **source files** at `/Users/paolo/claude/skills/skills/`. Never edit the local plugin cache at `~/.claude/plugins/cache/` — that is updated manually by the user via `/plugins update`.

- **eds-website-builder**: `/Users/paolo/claude/skills/skills/eds-website-builder/SKILL.md`
- **briefing-critique**: `/Users/paolo/claude/skills/skills/briefing-critique/SKILL.md`
- **eds-website-builder-ema**: `.claude/skills/eds-website-builder-ema/SKILL.md` — project-local variant for Experience Catalyst (aemcoder.adobe.io). Uses `content/` instead of `drafts/` and omits DA upload / preview execution (handled by the ExCat UI). Edit in place; do not sync from the user-level `eds-website-builder`.

## Lessons Learned (from Zenvara & Clareon builds)

### Content & Blocks
- Use **columns-teaser** (not table-data) for side-by-side content with headings/CTAs — better visual hierarchy
- Use **cards-teaser** for 3-column card grids with images + text + CTAs
- Use **introduction** block for section lead-in text with key stat emphasis
- Use **section-metadata** `Style: highlight` for key stat callout sections, `Style: light` for alternating backgrounds
- Keep accordion for dense reference content (prescribing info, trial design details)
- Every page needs the **accordion** for prescribing information / important safety info at the bottom

### Image Generation
- Model: `gemini-3-pro-image-preview` (NOT gemini-2.0-flash-exp, that 404s)
- If images fail with `finishReason: "OTHER"` (content safety filter), retry with less medical/anatomical language
- Always deploy to CDN before referencing in drafts — DA converts local paths to `about:error`
- Use `https://{sitename}-images.pages.dev/` as CDN base URL

### DA & Preview
- DA normalizes repo names to lowercase
- All `<img>` tags in DA content MUST use public CDN URLs, never local paths
- DA rejects external image URLs from third-party domains (even well-known ones like `myastrazeneca.co.uk`) — they become `about:error`. Always download the asset, deploy to the site's Cloudflare Pages CDN, and reference via `{sitename}-images.pages.dev/`
- Before DA upload, verify: `grep -rn 'src="/' drafts/{sitename}/ --include='*.html'` should return nothing
- The AEM Code Sync GitHub App must be installed on the repo

### Navigation
- Single-product sites: flat top-level nav, no dropdowns (one dropdown with all pages adds a click with no benefit)
- All nav/footer links must be prefixed with `/{sitename}/` for multi-site routing
- Nav structure: top bar (Contact, Login, Language) | logo | page links | search + login CTA

### Accordion / Prescribing Information
- Generate the accordion (PI + AE Reporting + References) once as a standalone HTML block
- Copy that exact HTML identically into every page — do not re-generate per page
- This prevents formatting drift (e.g. inconsistent `<strong>` wrapping)
- When using parallel page generation, include the accordion HTML in the shared context bundle

### Briefing vs Template Precedence
- When an MLR-approved briefing specifies footer/nav content (URLs, copyright text, approval codes), use the briefing's text verbatim — do not fall back to CLAUDE.md template defaults
- The templates in this file provide structure; the briefing provides content
- After generating nav and footer, verify every link target against the briefing's nav/footer sections
- Common miss: regulatory links (Privacy, Terms, Accessibility) left as placeholders when the briefing specifies real URLs

### Hero Text Contrast
Three fixes required for readable hero text over background images:
1. Gradient overlay via `::before` pseudo-element
2. Content row z-index higher than overlay
3. Text cell explicitly positioned above the `<picture>` element
See `blocks/hero-teaser/hero-teaser.css` for the implementation.

## Image Style Tiers

The image generation pipeline supports 4 brand-aligned tiers plus a generic fallback. Pass the tier as the optional 3rd argument to `generate_image` in `image-prompts.sh` files.

| Tier | Name | When to Use | Style |
|------|------|-------------|-------|
| `tier1` | Double-Exposure Artistic | Homepage heroes, therapy area cards | Human silhouette filled with scientific/natural imagery |
| `tier2` | Warm Lifestyle Photography | Product heroes, patient benefit sections | Natural-light photos of patients in everyday settings |
| `tier3` | Product & Device Photography | Dosing pages, device guides | Clean product shots on white/light backgrounds |
| `tier4` | Dramatic/Abstract Hero | Oncology heroes, severe disease products | Bold CGI, aurora borealis, dramatic landscapes |
| (omit) | Generic | Default when no tier specified | Photorealistic pharmaceutical style (backwards compatible) |

**Usage in image-prompts.sh:**
```bash
generate_image "hero-home.jpeg" "Woman silhouette filled with teal lung imagery" "tier1"
generate_image "hero-product.jpeg" "Man walking in a park, golden light" "tier2"
generate_image "card-device.jpeg" "Pre-filled pen, white background" "tier3"
generate_image "hero-onc.jpeg" "Aurora borealis, dark teal to warm gold" "tier4"
generate_image "card-generic.jpeg" "Description..." # no tier = generic fallback
```

**Config files:**
- Style brief: `brand/az-image-style-brief.md`
- Machine-readable config (sourced by `generate-images.sh`): `brand/az-image-style-config.sh`
- Reference images for style grounding: `brand/reference-images/tier{1,2,3,4}/`
- Crawler: `node tools/crawl-az-references.mjs` (populates reference images, writes manifest for human review)

## Design Context

### Users
UK Healthcare Professionals (doctors, nurses, pharmacists) visiting product-specific HCP portals during clinical decision-making. They need fast access to efficacy data, safety profiles, dosing information, and prescribing resources. Context is professional, time-pressured, and evidence-driven.

### Brand Personality
**Clinically authoritative, supportively warm, editorially premium.** AstraZeneca positions itself as a trusted scientific partner standing alongside HCPs — never a vendor, never casual, never patronising.

### Aesthetic Direction
- **Visual tone**: Premium editorial pharmaceutical — clean, spacious, typography-led
- **Reference site**: myastrazeneca.co.uk (live screenshots in `analysis/az-reference-screenshots/`)
- **Reference analysis**: `brand/myastrazeneca-analysis.md` (16-page visual audit)
- **Theme**: Light mode only, white primary background
- **Typography**: The live site uses a thin-weight serif (Lexia) for headings; our block library uses Roboto Condensed Bold — this is a deliberate simplification but headings should remain prominent and use AZ Magenta (#830051)
- **Imagery**: Double-exposure artistic portraits (Tier 1), warm lifestyle photography (Tier 2), product/device shots (Tier 3), dramatic oncology imagery (Tier 4). See `brand/az-brand-voice.md` Section 4.
- **Anti-references**: Generic stock photography, consumer health websites, clinical/sterile aesthetics, dark mode

### Design Principles
1. **White space is a feature**: Generous spacing between sections (48-80px). Pages breathe. No visual clutter.
2. **Typography drives hierarchy**: Headings are the dominant visual element — large, prominent, AZ Magenta. Data and statistics use bold emphasis.
3. **Minimal UI chrome**: No heavy borders, no drop shadows on containers, no gradients on backgrounds. Cards are flat or very subtly elevated. The design is reductive.
4. **Data when it matters, story when it doesn't**: Disease context pages are narrative. Product efficacy pages are data-forward with large statistics and trial tables.
5. **Regulatory elements are omnipresent but understated**: PI, AE reporting, approval codes appear on every page in smaller, lighter styling at the bottom.
6. **Each product is a mini-brand**: Products have their own accent colour that influences imagery and highlights, unified by the AZ global chrome (header/footer) and magenta CTAs.
