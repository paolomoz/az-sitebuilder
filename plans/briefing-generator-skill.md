# Plan: Create `briefing-generator` Skill

## Context

The current workflow requires manually creating `sites/{sitename}/briefing.md` and `sites/{sitename}/image-prompts.sh` before using `eds-website-builder` to build a site. This new skill automates that step — taking raw product information (DOCX, PDF, or verbal) and producing both files, then running image generation and CDN deployment. This completes the end-to-end pipeline: **briefing-generator → eds-website-builder → briefing-critique**.

## Files to Create/Modify

| File | Action |
|------|--------|
| `/Users/paolo/claude/skills/skills/briefing-generator/SKILL.md` | **Create** — main skill definition |
| `/Users/paolo/claude/skills/.claude-plugin/marketplace.json` | **Edit** — register skill in `page-generation` category |
| `/Users/paolo/claude/skills/tests/trigger-prompts.json` | **Edit** — add trigger prompts and signals |

## Skill Design

### Inputs (any combination)
- DOCX file with product information (read natively by Claude Code)
- PDF SmPC or clinical paper (read natively, max 20 pages/request)
- Verbal description from user
- The `ARGUMENTS` passed from the skill invocation (sitename or drug name)

### Outputs
1. `sites/{sitename}/briefing.md` — complete MLR-style briefing (11 sections)
2. `sites/{sitename}/image-prompts.sh` — tier-aware image generation script
3. Generated images in `images/{sitename}/` (via `generate-images.sh`)
4. CDN deployment (via `deploy-images.sh`)

### 8-Step Workflow

**Step 1: Gather input & extract product data**
- Read provided files (DOCX/PDF)
- Parse: brand name, generic name, drug class, indication, MoA, clinical trials (with full stats), safety profile, dosing, references
- If critical fields are missing (brand name, generic name, drug class, indication), ask the user

**Step 2: Determine sitename & brand colour**
- Derive sitename: lowercase, alphanumeric (TRELUXIA → treluxia)
- If no brand colour specified, assign from therapy-area palette:
  - Respiratory: Deep Teal #006B77
  - Cardiovascular: Cerulean Blue #0072B2
  - Oncology: Sapphire Blue #1A5B8C
  - Diabetes: Mediterranean Blue #2E6BA4
  - Immunology: Teal #00827F
  - Default: Sapphire Blue #1A5B8C
- Create `sites/{sitename}/` directory

**Step 3: Determine page structure**
- Standard 6-page HCP site: Home, Efficacy/Data, Safety, Dosing, MoA, Resources
- Name efficacy page after clinical programme if one exists (e.g., `/treluxia/luminos-data`)
- Name MoA page as `how-{brandname}-works`

**Step 4: Generate `sites/{sitename}/briefing.md`**
- Follow exact Treluxia briefing format (11 sections)
- Section 9 (Page Content) includes complete per-section copy with block types, image specs, CDN URLs, CTAs, and page metadata
- Apply AZ brand voice from `brand/az-brand-voice.md`
- Include all clinical stats with rate ratios, CIs, p-values
- Reference superscripts on every factual claim
- Alternate section backgrounds (default → light → highlight) for visual rhythm
- Every page ends with accordion (PI + AE Reporting + References)

**Step 5: Generate `sites/{sitename}/image-prompts.sh`**
- Group by type: heroes (16:9), cards (4:3), columns (4:3), tabs (4:3)
- Assign tiers: tier1 (heroes with double-exposure), tier2 (lifestyle), tier3 (product shots), tier4 (dramatic MoA)
- Include brand colour in prompt descriptions
- Use counter pattern (TOTAL, SUCCESS, FAIL)
- End all prompts with "No text."

**Step 6: Run image generation**
```bash
./tools/generate-images.sh {sitename}
```

**Step 7: Deploy images to CDN**
```bash
./tools/deploy-images.sh {sitename}
```
Verify: `curl -sI https://{sitename}-images.pages.dev/astrazeneca-logo.png | head -1` → HTTP 200

**Step 8: Verify & report**
- Confirm both files exist and have correct structure
- Report image generation results (success/fail count)
- Report CDN status
- Tell user to run `eds-website-builder` next

### Block Selection Rules (embedded in skill)

| Context | Block | Section Style |
|---------|-------|---------------|
| Homepage hero | hero-teaser | — |
| Key benefit cards | cards-teaser (3 cards) | — |
| Disease context | introduction | light |
| MoA teaser | columns-teaser | highlight |
| Trial data (multiple trials) | tabs-large with nested table-data | — |
| Safety page header | title (no image) | — |
| AE table | table-data | light |
| Safety cards | cards-teaser | — |
| Special populations | columns-teaser | highlight |
| Dosing sections | columns-teaser | alternating light/highlight |
| Resource cards | cards-teaser | — |
| Medical contact | columns-teaser | highlight |
| Every page bottom | accordion (PI + AE + Refs) | — |

### Copy Generation Rules (embedded in skill)
- Every efficacy claim needs: rate ratio/HR, 95% CI, P-value
- Brand name ALL CAPS with ™ on first mention per page
- Generic name lowercase in parentheses on first mention
- Action-oriented CTAs: "Explore", "View", "Review", "Download"
- No contractions in clinical copy
- Page titles: `Context | BRAND (generic) | Detail | AstraZeneca UK`

### Missing Data Handling
- If clinical trial data is incomplete: generate structure with `[DATA TO BE PROVIDED]` markers
- Change opening instruction from "MLR-approved" to "Draft copy — pending review"
- All other fields: proceed with what's available, mark gaps

## Registration

### marketplace.json
Add to `page-generation` category's skills array:
```json
"./skills/briefing-generator"
```

### trigger-prompts.json
```json
"briefing-generator": {
  "description": "Generate complete website briefing and image prompts from product/drug information",
  "prompts": [
    "Generate a briefing for a new drug site",
    "Create a website briefing from this DOCX",
    "Set up a new site briefing from the SmPC",
    "Generate briefing and images for treluxia"
  ],
  "signals": ["briefing", "generate briefing", "create briefing", "new site brief", "SmPC", "DOCX brief", "drug profile"]
}
```

## Verification

1. Check skill file exists: `ls /Users/paolo/claude/skills/skills/briefing-generator/SKILL.md`
2. Check marketplace registration: `grep briefing-generator /Users/paolo/claude/skills/.claude-plugin/marketplace.json`
3. Check trigger prompts: `grep briefing-generator /Users/paolo/claude/skills/tests/trigger-prompts.json`
4. Dry-run test: invoke the skill with a known product to verify it produces valid briefing.md + image-prompts.sh structure (don't need to actually run image generation for the test)
