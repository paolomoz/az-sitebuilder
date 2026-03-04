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

function isAccessGranted() {
  // Let Lighthouse / PageSpeed Insights / bots through to measure the real site
  if (navigator.webdriver || /Lighthouse|PTST|HeadlessChrome/i.test(navigator.userAgent)) return true;

  const GATE_KEY = 'az-access';
  const GATE_TTL = 24 * 60 * 60 * 1000; // 24 hours
  try {
    const stored = JSON.parse(localStorage.getItem(GATE_KEY));
    if (stored && stored.t && (Date.now() - stored.t < GATE_TTL)) return true;
  } catch { /* invalid entry */ }
  return false;
}

function showAccessGate() {
  return new Promise((resolve) => {
    document.body.innerHTML = '';
    const overlay = document.createElement('div');
    overlay.style.cssText = 'display:flex;align-items:center;justify-content:center;min-height:100vh;font-family:sans-serif;';
    overlay.innerHTML = `<form style="text-align:center">
      <p style="color:#830051;font-size:1.2rem;margin-bottom:1rem">Enter access code</p>
      <input type="password" autofocus style="padding:8px 12px;font-size:1rem;border:1px solid #ccc;border-radius:4px;width:200px">
      <button type="submit" style="margin-left:8px;padding:8px 16px;font-size:1rem;background:#d0006f;color:#fff;border:none;border-radius:4px;cursor:pointer">Go</button>
      <p class="gate-error" style="color:#c00;margin-top:0.5rem;min-height:1.4em"></p>
    </form>`;
    document.body.appendChild(overlay);
    document.body.classList.add('appear');

    overlay.querySelector('form').addEventListener('submit', (e) => {
      e.preventDefault();
      const val = overlay.querySelector('input').value;
      if (val === 'az26') {
        localStorage.setItem('az-access', JSON.stringify({ t: Date.now() }));
        overlay.remove();
        resolve(true);
      } else {
        overlay.querySelector('.gate-error').textContent = 'Incorrect code';
      }
    });
  });
}

async function loadPage() {
  if (!isAccessGranted()) {
    await showAccessGate();
    // reload to get fresh DOM from backend
    window.location.reload();
    return;
  }
  await loadEager(document);
  await loadLazy(document);
  loadDelayed();
}

// Check if running in Universal Editor mode and load UE-specific instrumentation
if (/\.(stage-ue|ue)\.da\.live$/.test(window.location.hostname)) {
  await import(`${window.hlx.codeBasePath}/ue/scripts/ue.js`).then(({ default: ue }) => ue());
}

loadPage();
