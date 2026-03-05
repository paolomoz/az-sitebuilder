import { chromium } from 'playwright';

const url = 'https://main--az-sitebuilder--paolomoz.aem.page/demo/trial-explorer';
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

const consoleErrors = [];
page.on('console', msg => {
  if (msg.type() === 'error') consoleErrors.push(msg.text());
});

console.log('Navigating to', url);
await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
await page.waitForTimeout(5000);

await page.screenshot({ path: '/tmp/trial-explorer-full.png', fullPage: true });
console.log('Screenshot saved to /tmp/trial-explorer-full.png');

const blocks = await page.locator('.trial-explorer').all();
console.log(`\nFound ${blocks.length} trial-explorer block(s)`);

for (let i = 0; i < blocks.length; i++) {
  const text = await blocks[i].textContent();
  const hasError = text.includes('Unable to Load');
  const skeletons = await blocks[i].locator('.te-skeleton').count();
  const charts = await blocks[i].locator('svg').count();
  const headers = await blocks[i].locator('.te-header').count();
  const stats = await blocks[i].locator('.te-stats').count();
  console.log(`\nBlock ${i+1}:`);
  console.log(`  Error state: ${hasError}`);
  console.log(`  Loading skeleton: ${skeletons > 0}`);
  console.log(`  Header rendered: ${headers > 0}`);
  console.log(`  SVG charts: ${charts}`);
  console.log(`  Stats panel: ${stats > 0}`);
  console.log(`  Text: ${text.substring(0, 200)}`);
}

if (consoleErrors.length) {
  console.log('\nConsole errors:');
  consoleErrors.forEach(e => console.log(' ', e));
} else {
  console.log('\nNo console errors');
}

await browser.close();
