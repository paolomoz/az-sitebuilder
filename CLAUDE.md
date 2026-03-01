# AZ Sitebuilder

Multi-site AEM Edge Delivery Services project for AstraZeneca drug launch HCP websites.
One shared codebase (blocks, styles, scripts) serving multiple sites via URL-prefixed subfolders.

See @AGENTS.md for EDS fundamentals.

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

Each site's nav.plain.html and footer.plain.html must use **prefixed links**:
```html
<!-- In drafts/velostra/nav.plain.html -->
<a href="/velostra/efficacy">Efficacy</a>
<!-- NOT just /efficacy -->
```

The brand logo link should also point to the site root:
```html
<a href="/velostra/"><img src="https://velostra-images.pages.dev/astrazeneca-logo.svg" alt="AstraZeneca"></a>
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

accordion, action-bar, cards, cards-teaser, carousel-teaser, columns, columns-teaser,
embed, footer, fragment, header, hero, hero-teaser, image, introduction, table-data,
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
- Before DA upload, verify: `grep -rn 'src="/' drafts/{sitename}/ --include='*.html'` should return nothing
- The AEM Code Sync GitHub App must be installed on the repo

### Navigation
- Single-product sites: flat top-level nav, no dropdowns (one dropdown with all pages adds a click with no benefit)
- All nav/footer links must be prefixed with `/{sitename}/` for multi-site routing
- Nav structure: top bar (Contact, Login, Language) | logo | page links | search + login CTA

### Hero Text Contrast
Three fixes required for readable hero text over background images:
1. Gradient overlay via `::before` pseudo-element
2. Content row z-index higher than overlay
3. Text cell explicitly positioned above the `<picture>` element
See `blocks/hero-teaser/hero-teaser.css` for the implementation.
