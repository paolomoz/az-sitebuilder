// eslint-disable-next-line import/no-unresolved
import { toClassName, decorateBlock, loadBlock } from '../../scripts/aem.js';

/**
 * Detects repeating card patterns (picture-only p followed by body paragraphs)
 * in flat panel content and reconstructs them into a cards-teaser block.
 * Needed because the AEM backend flattens nested block divs in table cells.
 */
function assembleCards(panel) {
  const content = panel.lastElementChild;
  if (!content) return null;

  const children = [...content.children];
  const cards = [];
  let currentCard = null;
  const beforeCards = [];
  const afterCards = [];
  let foundFirstCard = false;
  let finishedCards = false;

  children.forEach((el) => {
    const isPictureOnly = el.tagName === 'P'
      && el.children.length === 1
      && el.firstElementChild
      && el.firstElementChild.tagName === 'PICTURE';

    if (isPictureOnly && !finishedCards) {
      if (currentCard) cards.push(currentCard);
      foundFirstCard = true;
      currentCard = { image: el, body: [] };
    } else if (currentCard && el.tagName === 'P') {
      currentCard.body.push(el);
    } else if (foundFirstCard) {
      if (currentCard) {
        cards.push(currentCard);
        currentCard = null;
      }
      finishedCards = true;
      afterCards.push(el);
    } else {
      beforeCards.push(el);
    }
  });
  if (currentCard) cards.push(currentCard);

  // Only assemble cards if there's a heading before the card pattern,
  // to avoid converting icon-list content (e.g. stage icons) into cards.
  const hasHeadingBefore = beforeCards.some((el) => /^H[1-6]$/.test(el.tagName));
  if (cards.length < 2 || !hasHeadingBefore) return null;

  const cardsBlock = document.createElement('div');
  cardsBlock.className = 'cards-teaser';
  cards.forEach((card) => {
    const row = document.createElement('div');
    const imageDiv = document.createElement('div');
    imageDiv.append(card.image.querySelector('picture'));
    const bodyDiv = document.createElement('div');
    card.body.forEach((el) => bodyDiv.append(el));
    row.append(imageDiv, bodyDiv);
    cardsBlock.append(row);
  });

  content.replaceChildren(...beforeCards, cardsBlock, ...afterCards);
  return cardsBlock;
}

export default async function decorate(block) {
  // build tablist
  const tablist = document.createElement('div');
  tablist.className = 'tabs-large-list';
  tablist.setAttribute('role', 'tablist');

  // decorate tabs and tabpanels
  const tabs = [...block.children].map((child) => child.firstElementChild);
  tabs.forEach((tab, i) => {
    const id = toClassName(tab.textContent);

    // decorate tabpanel
    const tabpanel = block.children[i];
    tabpanel.className = 'tabs-large-panel';
    tabpanel.id = `tabpanel-${id}`;
    tabpanel.setAttribute('aria-hidden', !!i);
    tabpanel.setAttribute('aria-labelledby', `tab-${id}`);
    tabpanel.setAttribute('role', 'tabpanel');

    // build tab button
    const button = document.createElement('button');
    button.className = 'tabs-large-tab';
    button.id = `tab-${id}`;

    button.innerHTML = tab.innerHTML;

    button.setAttribute('aria-controls', `tabpanel-${id}`);
    button.setAttribute('aria-selected', !i);
    button.setAttribute('role', 'tab');
    button.setAttribute('type', 'button');
    button.addEventListener('click', () => {
      block.querySelectorAll('[role=tabpanel]').forEach((panel) => {
        panel.setAttribute('aria-hidden', true);
      });
      tablist.querySelectorAll('button').forEach((btn) => {
        btn.setAttribute('aria-selected', false);
      });
      tabpanel.setAttribute('aria-hidden', false);
      button.setAttribute('aria-selected', true);
    });
    tablist.append(button);
    tab.remove();
  });

  block.prepend(tablist);

  // add divider bar after tab list
  const divider = document.createElement('div');
  divider.className = 'tabs-large-divider';
  tablist.after(divider);

  // assemble card patterns from flat content into cards-teaser blocks
  block.querySelectorAll('.tabs-large-panel').forEach((panel) => assembleCards(panel));

  // decorate and load nested blocks within tab panels
  const nestedBlocks = [...block.querySelectorAll('.tabs-large-panel div[class]')];
  await nestedBlocks.reduce(async (promise, nestedBlock) => {
    await promise;
    const blockName = nestedBlock.classList[0];
    if (blockName && !blockName.startsWith('tabs-large')) {
      const wrapper = document.createElement('div');
      nestedBlock.before(wrapper);
      wrapper.append(nestedBlock);
      decorateBlock(nestedBlock);
      await loadBlock(nestedBlock);
    }
  }, Promise.resolve());
}
