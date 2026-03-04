// add delayed functionality here

// Critique highlight overlay — activated only via ?critique-section or ?critique-target params
(() => {
  const params = new URLSearchParams(window.location.search);
  const sectionIdx = params.get('critique-section');
  const critiqueTarget = params.get('critique-target');
  if (!sectionIdx && !critiqueTarget) return;

  let target;
  if (critiqueTarget === 'header') {
    target = document.querySelector('header');
  } else if (critiqueTarget === 'footer') {
    target = document.querySelector('footer');
  } else if (sectionIdx) {
    const sections = document.querySelectorAll('main > .section');
    target = sections[parseInt(sectionIdx, 10) - 1];
  }
  if (!target) return;

  const label = params.get('critique-label') || '';
  target.style.outline = '3px solid #c0392b';
  target.style.outlineOffset = '-3px';
  target.style.background = 'rgba(192,57,43,0.06)';
  target.style.position = 'relative';
  if (label) {
    const tag = document.createElement('div');
    tag.textContent = label;
    Object.assign(tag.style, {
      position: 'absolute', top: '0', right: '0', background: '#c0392b', color: '#fff',
      fontSize: '12px', fontFamily: 'system-ui, sans-serif', fontWeight: '600',
      padding: '4px 10px', borderRadius: '0 0 0 6px', zIndex: '9999',
    });
    target.appendChild(tag);
  }
  target.scrollIntoView({ behavior: 'smooth', block: 'center' });
})();
