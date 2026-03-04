#!/usr/bin/env node
/**
 * Crawl myastrazeneca.co.uk for reference images and classify by tier.
 *
 * Downloads images to brand/reference-images/tier{1,2,3,4}/ and writes
 * a manifest.json for human review and reclassification.
 *
 * Usage: node tools/crawl-az-references.mjs
 *
 * Reuses overlay-handling patterns from analysis/az-reference-screenshots/capture.mjs
 */

import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
import https from 'https';
import http from 'http';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_DIR = path.resolve(__dirname, '..');
const OUTPUT_DIR = path.join(PROJECT_DIR, 'brand', 'reference-images');
const MANIFEST_PATH = path.join(OUTPUT_DIR, 'manifest.json');

const BASE_URL = 'https://www.myastrazeneca.co.uk';

// Pages to crawl, grouped by expected tier classification
const PAGES = [
  // Homepage — cards are typically tier1 (double-exposure), hero lifestyle is tier2
  { url: '/', context: 'homepage', defaultTier: 'tier1' },
  // Therapy area pages — heroes are tier1 double-exposure
  { url: '/respiratory', context: 'therapy-respiratory', defaultTier: 'tier1' },
  { url: '/cardiovascular', context: 'therapy-cardiovascular', defaultTier: 'tier1' },
  { url: '/oncology', context: 'therapy-oncology', defaultTier: 'tier4' },
  // Product pages — heroes are tier2 lifestyle, product images are tier3
  { url: '/forxiga', context: 'product-forxiga', defaultTier: 'tier2' },
  { url: '/symbicort', context: 'product-symbicort', defaultTier: 'tier2' },
  { url: '/tezspire', context: 'product-tezspire', defaultTier: 'tier4' },
  { url: '/wainzua', context: 'product-wainzua', defaultTier: 'tier2' },
  { url: '/tagrisso', context: 'product-tagrisso', defaultTier: 'tier4' },
];

// Minimum image dimensions to filter out icons, logos, and tiny decorative images
const MIN_WIDTH = 200;
const MIN_HEIGHT = 150;

// Target: 3-5 images per tier, ~15-20 total
const MAX_PER_TIER = 6;

async function nukeOverlays(page) {
  // Phase 1: Click cookie consent
  await page.evaluate(() => {
    const consentPatterns = [
      'accept all', 'accept cookies', 'accept all cookies',
      'i accept', 'i agree', 'got it', 'ok', 'allow all',
      'agree and proceed', 'agree & proceed', 'agree',
    ];
    const buttons = document.querySelectorAll(
      'button, a[role="button"], [class*="consent"] a, [class*="cookie"] button, [class*="cookie"] a',
    );
    for (const btn of buttons) {
      const text = btn.textContent.trim().toLowerCase();
      if (consentPatterns.some((p) => text.includes(p))) {
        btn.click();
        break;
      }
    }
  });
  await page.waitForTimeout(1500);

  // Phase 2: Click HCP gate if present
  await page.evaluate(() => {
    const gatePatterns = [
      'i am a healthcare professional', 'i am a uk healthcare professional',
      'yes, i am', 'enter site', 'continue',
    ];
    for (const btn of document.querySelectorAll('button, a, [role="button"]')) {
      const text = btn.textContent.trim().toLowerCase();
      if (gatePatterns.some((p) => text.includes(p))) {
        btn.click();
        break;
      }
    }
  });
  await page.waitForTimeout(1500);

  // Phase 3: Remove overlays
  await page.evaluate(() => {
    const overlaySelectors = [
      '[class*="cookie"]', '[class*="consent"]', '[class*="gdpr"]',
      '[class*="overlay"]:not(nav):not(header)', '[class*="modal-backdrop"]',
      '[id*="cookie"]', '[id*="consent"]', '[id*="gdpr"]',
      '.onetrust-consent-sdk', '#CybotCookiebotDialog',
      '.cc-window', '.cookie-banner', '.privacy-banner',
    ];
    for (const selector of overlaySelectors) {
      for (const el of document.querySelectorAll(selector)) {
        el.remove();
      }
    }

    for (const el of document.querySelectorAll('*')) {
      const style = window.getComputedStyle(el);
      const zIndex = parseInt(style.zIndex) || 0;
      if ((style.position === 'fixed' || style.position === 'sticky') && zIndex > 9999) {
        if (!el.closest('nav') && !el.closest('header') && el.tagName !== 'NAV' && el.tagName !== 'HEADER') {
          el.remove();
        }
      }
    }

    document.body.style.overflow = 'auto';
    document.documentElement.style.overflow = 'auto';
  });
  await page.waitForTimeout(500);
}

async function autoScroll(page) {
  await page.evaluate(async () => {
    const scrollHeight = document.body.scrollHeight;
    const viewportHeight = window.innerHeight;
    let currentPosition = 0;
    let scrolls = 0;
    while (currentPosition < scrollHeight && scrolls < 30) {
      window.scrollTo(0, currentPosition);
      currentPosition += viewportHeight;
      scrolls += 1;
      await new Promise((r) => setTimeout(r, 300));
    }
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise((r) => setTimeout(r, 500));
  });
}

/**
 * Extract image elements from the page with metadata for classification.
 */
async function extractImages(page) {
  return page.evaluate(({ minW, minH }) => {
    const images = [];
    for (const img of document.querySelectorAll('img')) {
      const rect = img.getBoundingClientRect();
      const src = img.src || img.getAttribute('data-src') || '';
      const alt = img.alt || '';

      // Skip tiny images, icons, logos, and data URIs
      if (rect.width < minW || rect.height < minH) continue;
      if (!src || src.startsWith('data:')) continue;
      if (alt.toLowerCase().includes('logo') || alt.toLowerCase().includes('icon')) continue;
      if (src.includes('logo') || src.includes('icon') || src.includes('favicon')) continue;

      // Determine position context for classification
      const isHero = rect.top < 600 && rect.width > 800;
      const isCard = rect.width < 500 && rect.height < 400;
      const parentClasses = (img.closest('section') || img.parentElement)?.className || '';

      images.push({
        src,
        alt,
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        isHero,
        isCard,
        parentClasses,
        pageY: Math.round(rect.top + window.scrollY),
      });
    }
    return images;
  }, { minW: MIN_WIDTH, minH: MIN_HEIGHT });
}

/**
 * Classify an image into a tier based on page context and image characteristics.
 * This is approximate — human review via manifest.json is expected.
 */
function classifyImage(img, pageInfo) {
  const { alt, isHero, isCard, parentClasses } = img;
  const { context, defaultTier } = pageInfo;
  const altLower = (alt || '').toLowerCase();
  const classesLower = (parentClasses || '').toLowerCase();

  // Product/device images: clean product shots
  if (altLower.includes('inhaler') || altLower.includes('pen') || altLower.includes('device')
    || altLower.includes('turbohaler') || altLower.includes('sachet')
    || altLower.includes('packaging') || altLower.includes('product')) {
    return 'tier3';
  }

  // Oncology/dramatic contexts
  if (context.includes('oncology') || context.includes('tezspire') || context.includes('tagrisso')) {
    if (isHero) return 'tier4';
  }

  // Homepage cards are typically double-exposure artistic
  if (context === 'homepage' && isCard) return 'tier1';

  // Therapy area heroes are typically double-exposure
  if (context.startsWith('therapy-') && isHero) return 'tier1';

  // Product page heroes are typically lifestyle
  if (context.startsWith('product-') && isHero) return 'tier2';

  // Lifestyle-looking images (people in settings)
  if (altLower.includes('patient') || altLower.includes('person')
    || altLower.includes('walking') || altLower.includes('smiling')
    || classesLower.includes('lifestyle')) {
    return 'tier2';
  }

  // Fall back to page default
  return defaultTier;
}

/**
 * Download a file from a URL to a local path.
 */
function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(destPath);
    protocol.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (response) => {
      if (response.statusCode === 301 || response.statusCode === 302) {
        const redirectUrl = response.headers.location;
        if (redirectUrl) {
          downloadFile(redirectUrl, destPath).then(resolve).catch(reject);
          return;
        }
      }
      if (response.statusCode !== 200) {
        reject(new Error(`HTTP ${response.statusCode} for ${url}`));
        return;
      }
      response.pipe(file);
      file.on('finish', () => { file.close(); resolve(); });
      file.on('error', (err) => { fs.unlink(destPath, () => {}); reject(err); });
    }).on('error', (err) => { fs.unlink(destPath, () => {}); reject(err); });
  });
}

/**
 * Generate a safe filename from a URL.
 */
function safeFilename(url, index) {
  try {
    const parsed = new URL(url);
    const basename = path.basename(parsed.pathname);
    // Keep original extension if valid
    const ext = path.extname(basename);
    const validExts = ['.jpg', '.jpeg', '.png', '.webp', '.gif'];
    if (validExts.includes(ext.toLowerCase())) {
      return `${index}-${basename}`;
    }
    return `${index}-image.jpg`;
  } catch {
    return `${index}-image.jpg`;
  }
}

async function main() {
  console.log('=== AZ Reference Image Crawler ===');
  console.log(`Source: ${BASE_URL}`);
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log('');

  // Create tier directories
  for (const tier of ['tier1', 'tier2', 'tier3', 'tier4']) {
    fs.mkdirSync(path.join(OUTPUT_DIR, tier), { recursive: true });
  }

  const manifest = {
    source: BASE_URL,
    crawledAt: new Date().toISOString(),
    images: [],
  };

  // Track counts per tier
  const tierCounts = { tier1: 0, tier2: 0, tier3: 0, tier4: 0 };

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    reducedMotion: 'reduce',
  });

  // Track downloaded URLs to avoid duplicates across pages
  const downloadedUrls = new Set();
  let imageIndex = 0;

  for (const pageInfo of PAGES) {
    const fullUrl = `${BASE_URL}${pageInfo.url}`;
    console.log(`--- ${pageInfo.context} (${fullUrl}) ---`);

    const page = await context.newPage();
    try {
      await page.goto(fullUrl, { waitUntil: 'networkidle', timeout: 30000 });
      await nukeOverlays(page);
      await autoScroll(page);
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.waitForTimeout(500);

      const images = await extractImages(page);
      console.log(`  Found ${images.length} candidate images`);

      for (const img of images) {
        // Skip duplicates
        if (downloadedUrls.has(img.src)) continue;

        // Classify
        const tier = classifyImage(img, pageInfo);

        // Respect per-tier cap
        if (tierCounts[tier] >= MAX_PER_TIER) continue;

        // Download
        imageIndex += 1;
        const filename = safeFilename(img.src, imageIndex);
        const destPath = path.join(OUTPUT_DIR, tier, filename);

        try {
          await downloadFile(img.src, destPath);
          const stats = fs.statSync(destPath);

          // Skip tiny files (likely broken downloads)
          if (stats.size < 5000) {
            fs.unlinkSync(destPath);
            console.log(`  SKIP: ${filename} (too small: ${stats.size} bytes)`);
            continue;
          }

          downloadedUrls.add(img.src);
          tierCounts[tier] += 1;

          manifest.images.push({
            filename,
            tier,
            sourceUrl: img.src,
            alt: img.alt,
            pageContext: pageInfo.context,
            dimensions: `${img.naturalWidth}x${img.naturalHeight}`,
            filePath: path.relative(PROJECT_DIR, destPath),
          });

          console.log(`  OK: ${tier}/${filename} (${stats.size} bytes)`);
        } catch (err) {
          console.log(`  FAIL: ${filename} — ${err.message}`);
        }
      }
    } catch (err) {
      console.error(`  PAGE FAIL: ${err.message}`);
    }

    await page.close();
  }

  await browser.close();

  // Write manifest
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2));
  console.log('');
  console.log('=== Summary ===');
  console.log(`Tier 1 (double-exposure): ${tierCounts.tier1} images`);
  console.log(`Tier 2 (lifestyle):       ${tierCounts.tier2} images`);
  console.log(`Tier 3 (product/device):  ${tierCounts.tier3} images`);
  console.log(`Tier 4 (dramatic/abstract): ${tierCounts.tier4} images`);
  console.log(`Total: ${manifest.images.length} images`);
  console.log(`Manifest: ${MANIFEST_PATH}`);
  console.log('');
  console.log('Next steps:');
  console.log('  1. Review manifest.json — reclassify any misplaced images');
  console.log('  2. Move files between tier{1,2,3,4}/ directories as needed');
  console.log('  3. Delete any unsuitable images');
  console.log('  4. Run generate-images.sh with tier args to use references');
}

main().catch(console.error);
