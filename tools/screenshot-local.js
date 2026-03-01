import { chromium } from 'playwright';
import { mkdirSync, readdirSync, statSync } from 'fs';
import { join, basename } from 'path';

const BASE = 'http://localhost:3000';
const siteName = process.argv[2];

if (!siteName) {
  console.error('Usage: node tools/screenshot-local.js <sitename>');
  console.error('Example: node tools/screenshot-local.js velostra');
  process.exit(1);
}

// Auto-discover pages from drafts/{sitename}/ directory
const draftsDir = join(process.cwd(), 'drafts', siteName);
const PAGES = readdirSync(draftsDir)
  .filter((f) => f.endsWith('.plain.html') && f !== 'nav.plain.html' && f !== 'footer.plain.html')
  .map((f) => {
    const name = basename(f, '.plain.html');
    return {
      name: name === 'index' ? 'home' : name,
      path: `/${siteName}/${name === 'index' ? '' : name}`,
    };
  });

const DIR = `analysis/${siteName}-screenshots`;

async function main() {
  mkdirSync(DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });

  for (const { name, path } of PAGES) {
    const page = await context.newPage();
    try {
      console.log(`Capturing: ${name} (${BASE}${path})`);
      await page.goto(`${BASE}${path}`, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(3000);
      await page.screenshot({ path: `${DIR}/${name}.png`, fullPage: true });
      console.log(`  OK: ${name}`);
    } catch (err) {
      console.error(`  FAIL: ${name} - ${err.message}`);
    } finally {
      await page.close();
    }
  }

  await browser.close();
  console.log(`\nDone. Screenshots saved to ${DIR}`);
}

main().catch(console.error);
