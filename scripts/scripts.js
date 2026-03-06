import {
  loadHeader,
  loadFooter,
  decorateIcons,
  decorateSections,
  decorateBlocks,
  decorateTemplateAndTheme,
  waitForFirstImage,
  loadSection,
  loadSections,
  loadCSS,
} from './aem.js';

/**
 * load fonts.css and set a session storage flag
 */
async function loadFonts() {
  await loadCSS(`${window.hlx.codeBasePath}/styles/fonts.css`);
  try {
    if (!window.location.hostname.includes('localhost')) sessionStorage.setItem('fonts-loaded', 'true');
  } catch (e) {
    // do nothing
  }
}

/**
 * Builds all synthetic blocks in a container element.
 * @param {Element} main The container element
 */
function buildAutoBlocks(main) {
  try {
    // auto load `*/fragments/*` references
    const fragments = [...main.querySelectorAll('a[href*="/fragments/"]')].filter((f) => !f.closest('.fragment'));
    if (fragments.length > 0) {
      // eslint-disable-next-line import/no-cycle
      import('../blocks/fragment/fragment.js').then(({ loadFragment }) => {
        fragments.forEach(async (fragment) => {
          try {
            const { pathname } = new URL(fragment.href);
            const frag = await loadFragment(pathname);
            fragment.parentElement.replaceWith(...frag.children);
          } catch (error) {
            // eslint-disable-next-line no-console
            console.error('Fragment loading failed', error);
          }
        });
      });
    }
  } catch (error) {
    // eslint-disable-next-line no-console
    console.error('Auto Blocking failed', error);
  }
}

/**
 * Decorates formatted links to style them as buttons.
 * @param {HTMLElement} main The main container element
 */
function decorateButtons(main) {
  main.querySelectorAll('p a[href]').forEach((a) => {
    a.title = a.title || a.textContent;
    const p = a.closest('p');
    const text = a.textContent.trim();

    // quick structural checks
    if (a.querySelector('img') || p.textContent.trim() !== text) return;

    // skip URL display links
    try {
      if (new URL(a.href).href === new URL(text, window.location).href) return;
    } catch { /* continue */ }

    // require authored formatting for buttonization
    const strong = a.closest('strong');
    const em = a.closest('em');
    if (!strong && !em) return;

    p.className = 'button-wrapper';
    a.className = 'button';
    if (strong && em) { // high-impact call-to-action
      a.classList.add('accent');
      const outer = strong.contains(em) ? strong : em;
      outer.replaceWith(a);
    } else if (strong) {
      a.classList.add('primary');
      strong.replaceWith(a);
    } else {
      a.classList.add('secondary');
      em.replaceWith(a);
    }
  });
}

/**
 * Decorates the main element.
 * @param {Element} main The main element
 */
// eslint-disable-next-line import/prefer-default-export
export function decorateMain(main) {
  decorateIcons(main);
  buildAutoBlocks(main);
  decorateSections(main);

  // Process and remove document-level metadata block before block decoration
  // to prevent it from being loaded as a visual block (404 on blocks/metadata/)
  main.querySelectorAll('.metadata').forEach((metaBlock) => {
    metaBlock.querySelectorAll(':scope > div').forEach((row) => {
      const key = row.children[0]?.textContent?.trim().toLowerCase();
      const value = row.children[1]?.textContent?.trim();
      if (key && value && !document.head.querySelector(`meta[name="${key}"]`)) {
        const meta = document.createElement('meta');
        meta.name = key;
        meta.content = value;
        document.head.appendChild(meta);
      }
    });
    metaBlock.closest('.section')?.remove();
  });

  decorateBlocks(main);
  decorateButtons(main);
}

/**
 * Loads everything needed to get to LCP.
 * @param {Element} doc The container element
 */
async function loadEager(doc) {
  document.documentElement.lang = 'en';
  decorateTemplateAndTheme();
  const main = doc.querySelector('main');
  if (main) {
    decorateMain(main);
    await loadSection(main.querySelector('.section'), waitForFirstImage);
    document.body.classList.add('appear');
  }

  try {
    /* if desktop (proxy for fast connection) or fonts already loaded, load fonts.css */
    if (window.innerWidth >= 900 || sessionStorage.getItem('fonts-loaded')) {
      loadFonts();
    }
  } catch (e) {
    // do nothing
  }
}

/**
 * Loads everything that doesn't need to be delayed.
 * @param {Element} doc The container element
 */
async function loadLazy(doc) {
  loadHeader(doc.querySelector('header'));

  const main = doc.querySelector('main');
  await loadSections(main);

  const { hash } = window.location;
  const element = hash ? doc.getElementById(hash.substring(1)) : false;
  if (hash && element) element.scrollIntoView();

  loadFooter(doc.querySelector('footer'));

  loadCSS(`${window.hlx.codeBasePath}/styles/lazy-styles.css`);
  loadFonts();
}

/**
 * Loads everything that happens a lot later,
 * without impacting the user experience.
 */
function loadDelayed() {
  // eslint-disable-next-line import/no-cycle
  window.setTimeout(() => import('./delayed.js'), 3000);
  // load anything that can be postponed to the latest here
}

const ACCESS_GATE_ENABLED = true;

function checkAccessGate() {
  if (!ACCESS_GATE_ENABLED) return;
  // Let bots / Lighthouse / PageSpeed through
  if (navigator.webdriver || /bot|crawl|spider|Lighthouse|PTST|HeadlessChrome/i.test(navigator.userAgent)) return;

  const key = 'az-access';
  try {
    const s = JSON.parse(localStorage.getItem(key));
    if (s && Date.now() - s.t < 86400000) return; // 24h
  } catch { /* ask again */ }

  // eslint-disable-next-line no-alert
  if (prompt('Enter access code:') !== 'az26') {
    document.body.innerHTML = '<p style="text-align:center;margin-top:40vh;font-family:sans-serif;color:#830051">Access denied.</p>';
    throw new Error('access denied');
  }
  localStorage.setItem(key, JSON.stringify({ t: Date.now() }));
}

async function loadPage() {
  checkAccessGate();
  await loadEager(document);
  await loadLazy(document);
  loadDelayed();
}

// Check if running in Universal Editor mode and load UE-specific instrumentation
if (/\.(stage-ue|ue)\.da\.live$/.test(window.location.hostname)) {
  await import(`${window.hlx.codeBasePath}/ue/scripts/ue.js`).then(({ default: ue }) => ue());
}

loadPage();
