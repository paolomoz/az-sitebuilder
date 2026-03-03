# Block HTML Markup Reference

Expected `.plain.html` structure for each block. Use these patterns when creating site draft files.

## accordion
```html
<div class="accordion">
  <div>
    <div>Label text</div>
    <div>Body content (paragraphs, lists, links)</div>
  </div>
  <!-- repeat rows for more items -->
</div>
```
Each row = one item. First cell = summary label, second cell = expandable body. Renders as `<details>/<summary>`.

## cards-teaser
```html
<div class="cards-teaser">
  <div>
    <div><picture>...<img src="..." alt="..."></picture></div>
    <div>
      <p><strong>Card heading</strong></p>
      <p>Body text</p>
      <p><a href="#">CTA link</a></p>
    </div>
  </div>
  <!-- repeat rows for more cards -->
</div>
```
Each row = one card. First cell = image, second cell = body. Standalone links become buttons.

## carousel-teaser
```html
<div class="carousel-teaser">
  <div>
    <div><picture>...<img src="..." alt="..."></picture></div>
    <div>
      <p><strong>Slide heading</strong></p>
      <p>Slide content</p>
      <p><a href="#">CTA</a></p>
    </div>
  </div>
  <!-- 2+ rows enable carousel with dots and arrows; 1 row = static -->
</div>
```
Each row = one slide. First cell = image, second cell = content. Needs 2+ rows for carousel controls.

## columns-teaser
```html
<div class="columns-teaser">
  <div>
    <div><picture>...<img src="..." alt="..."></picture></div>
    <div>
      <h2>Heading</h2>
      <p>Body text</p>
      <p><strong><a href="#">CTA</a></strong></p>
    </div>
  </div>
</div>
```
Image + content side-by-side. Wrap CTA in `<strong>` for primary button styling.

## hero-teaser
```html
<div class="hero-teaser">
  <div>
    <div><picture>...<img src="..." alt="..."></picture></div>
  </div>
  <div>
    <div>
      <h1>Headline</h1>
      <p>Description text</p>
      <p><strong><a href="#">CTA</a></strong></p>
    </div>
  </div>
</div>
```
First row = background image. Second row = text overlay. Text gets gradient contrast via CSS.

## introduction
```html
<div class="introduction">
  <div>
    <div>
      <h2>Section heading</h2>
      <p>Lead-in text with optional key stat emphasis.</p>
    </div>
  </div>
</div>
```
CSS-only block. Pair with `section-metadata Style: light` for background.

## table-data
```html
<div class="table-data">
  <div>
    <div>Header 1</div>
    <div>Header 2</div>
    <div>Header 3</div>
  </div>
  <div>
    <div>Cell</div>
    <div>Cell</div>
    <div>Cell</div>
  </div>
  <!-- repeat rows -->
</div>
```
First row = table header (`<th>`). Remaining rows = data (`<td>`). Renders as semantic `<table>`.

## tabs-large
```html
<div class="tabs-large">
  <div>
    <div>Tab 1 Label</div>
    <div>
      <h3>Panel heading</h3>
      <p>Panel content</p>
      <!-- can contain nested blocks like table-data -->
    </div>
  </div>
  <div>
    <div>Tab 2 Label</div>
    <div>Panel content</div>
  </div>
</div>
```
Each row = one tab. First cell = tab button label (extracted). Second cell = panel content. Supports nested blocks (`div[class]`) inside panels — they get auto-decorated.

## title
```html
<div class="title">
  <div>
    <div>
      <h1>Page title</h1>
      <p>Optional subtitle</p>
    </div>
  </div>
</div>
```
CSS-only, no JS. Centered heading block — use instead of hero-teaser when no hero image is needed.

## Section Metadata (not a block — used within sections)
```html
<div class="section-metadata">
  <div>
    <div>Style</div>
    <div>light</div>  <!-- or: highlight -->
  </div>
</div>
```
Place at the end of a section (before `<hr>`). `light` = #f8f8f8 background, `highlight` = #f4eef2 with magenta border-top.

## Page Metadata (not a block — one per page, at the end)
```html
<div class="metadata">
  <div>
    <div>Title</div>
    <div>Page Title | Site Name</div>
  </div>
  <div>
    <div>Description</div>
    <div>Meta description text.</div>
  </div>
</div>
```
Place as the last section of the page.

## Less Common Blocks

**action-bar** — Row 1: metadata text. Row 2: action buttons (Like, Save, Share). Icons auto-generated.

**embed** — Cell with YouTube/Vimeo/Twitter URL. Optional picture cell as play button overlay.

**fragment** — Cell with `<a href="/path/to/fragment">` loads external content inline.

**image** — Wrapper for standalone `<picture>`. Maintains 16:9 aspect ratio.
