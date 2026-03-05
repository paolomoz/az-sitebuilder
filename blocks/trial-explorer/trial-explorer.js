import {
  renderBarChart, renderForestPlot, renderFlowDiagram, renderAccessibleTable,
} from './charts.js';

const WORKER_URLS = {
  local: 'http://localhost:8787',
  prod: 'https://trial-explorer.paolo-moz.workers.dev',
};

function getWorkerUrl() {
  const { hostname } = window.location;
  return hostname === 'localhost' || hostname === '127.0.0.1'
    ? WORKER_URLS.local
    : WORKER_URLS.prod;
}

function readBlockConfig(block) {
  const config = {};
  [...block.children].forEach((row) => {
    const key = row.children[0]?.textContent?.trim().toLowerCase().replace(/\s+/g, '-');
    const val = row.children[1]?.textContent?.trim();
    if (key && val) config[key] = val;
  });
  return config;
}

function showLoading(block) {
  block.innerHTML = '';
  const skeleton = document.createElement('div');
  skeleton.className = 'te-skeleton';
  skeleton.innerHTML = `
    <div class="te-skeleton-bar"></div>
    <div class="te-skeleton-bar"></div>
    <div class="te-skeleton-bar"></div>
    <div class="te-skeleton-bar"></div>
  `;
  block.append(skeleton);
}

function showError(block, message) {
  block.innerHTML = '';
  const error = document.createElement('div');
  error.className = 'te-error';
  error.innerHTML = `
    <h3>Unable to Load Trial Data</h3>
    <p>${message}</p>
  `;
  block.append(error);
}

function buildHeader(data, config) {
  const header = document.createElement('div');
  header.className = 'te-header';

  const title = config['trial-name'] || data.briefTitle;
  header.innerHTML = `
    <h2>${title}</h2>
    <div class="te-header-meta">
      ${data.phase ? `<span class="te-badge">${data.phase}</span>` : ''}
      ${data.enrollment ? `<span class="te-enrollment">n = ${data.enrollment.toLocaleString()}</span>` : ''}
      <span class="te-nct-id">${data.nctId}</span>
    </div>
  `;
  return header;
}

function buildFilters(data, onFilter) {
  const container = document.createElement('div');
  container.className = 'te-filters';

  // Endpoint type filter (Primary / Secondary / All)
  const types = [...new Set(data.outcomes.map((o) => o.type))].filter(Boolean);
  if (types.length > 1) {
    const group = document.createElement('div');
    group.className = 'te-filter-group';
    group.setAttribute('role', 'tablist');
    group.setAttribute('aria-label', 'Endpoint type');
    group.innerHTML = '<span class="te-filter-label">Endpoint</span>';

    ['All', ...types].forEach((t, i) => {
      const pill = document.createElement('button');
      pill.className = 'te-pill';
      pill.setAttribute('role', 'tab');
      pill.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
      const labels = { PRIMARY: 'Primary', SECONDARY: 'Secondary' };
      pill.textContent = labels[t] || t;
      pill.dataset.filterType = 'endpoint';
      pill.dataset.filterValue = t;
      pill.addEventListener('click', () => {
        group.querySelectorAll('.te-pill').forEach((p) => p.setAttribute('aria-selected', 'false'));
        pill.setAttribute('aria-selected', 'true');
        onFilter();
      });
      group.append(pill);
    });
    container.append(group);
  }

  return container;
}

function getActiveFilters(block) {
  const filters = {};
  block.querySelectorAll('.te-pill[aria-selected="true"]').forEach((pill) => {
    filters[pill.dataset.filterType] = pill.dataset.filterValue;
  });
  return filters;
}

function filterOutcomes(outcomes, filters) {
  let filtered = outcomes;
  if (filters.endpoint && filters.endpoint !== 'All') {
    filtered = filtered.filter((o) => o.type === filters.endpoint);
  }
  return filtered;
}

function buildLegend(groups) {
  const legend = document.createElement('div');
  legend.className = 'te-legend';
  const colors = ['var(--te-color-treatment)', 'var(--te-color-control)', 'var(--te-color-alt)', 'var(--te-color-alt2)'];

  groups.forEach((g, i) => {
    const item = document.createElement('div');
    item.className = 'te-legend-item';
    item.innerHTML = `<span class="te-legend-swatch" style="background:${colors[i % colors.length]}"></span><span>${g.title}</span>`;
    legend.append(item);
  });
  return legend;
}

function buildStatsPanel(outcomes) {
  const panel = document.createElement('div');
  panel.className = 'te-stats';
  panel.innerHTML = '<h3>Key Statistics</h3>';

  const grid = document.createElement('div');
  grid.className = 'te-stat-grid';

  // Collect all analyses from filtered outcomes
  const allAnalyses = outcomes.flatMap((o) => o.analyses || []);
  if (!allAnalyses.length) {
    grid.innerHTML = '<p style="font-size:13px;color:#666;">No statistical analyses available for selected endpoints.</p>';
    panel.append(grid);
    return panel;
  }

  allAnalyses.forEach((a) => {
    if (a.estimateValue != null) {
      const item = document.createElement('div');
      item.className = 'te-stat-item';
      const isSignificant = a.pValue != null && a.pValue < 0.05;
      item.innerHTML = `
        <span class="te-stat-label">${a.estimateType || 'Estimate'}</span>
        <span class="te-stat-value${isSignificant ? ' te-significant' : ''}">${a.estimateValue.toFixed(2)}</span>
      `;
      grid.append(item);
    }

    if (a.pValue != null) {
      const item = document.createElement('div');
      item.className = 'te-stat-item';
      const isSignificant = a.pValue < 0.05;
      item.innerHTML = `
        <span class="te-stat-label">p-value</span>
        <span class="te-stat-value${isSignificant ? ' te-significant' : ''}">${a.pValue < 0.001 ? '<0.001' : a.pValue.toFixed(4)}</span>
      `;
      grid.append(item);
    }

    if (a.ciLower != null && a.ciUpper != null) {
      const item = document.createElement('div');
      item.className = 'te-stat-item';
      item.innerHTML = `
        <span class="te-stat-label">${a.ciPercent || 95}% CI</span>
        <span class="te-stat-value" style="font-size:20px;">${a.ciLower.toFixed(2)} – ${a.ciUpper.toFixed(2)}</span>
      `;
      grid.append(item);
    }
  });

  panel.append(grid);
  return panel;
}

function buildCharts(data, filteredOutcomes, chartArea) {
  chartArea.innerHTML = '';

  // Legend
  chartArea.append(buildLegend(data.groups));

  // Forest plot if we have analyses
  const allAnalyses = filteredOutcomes.flatMap((o) => o.analyses || []);
  if (allAnalyses.length) {
    const title = document.createElement('h3');
    title.className = 'te-chart-title';
    title.textContent = 'Treatment Effect (Forest Plot)';
    chartArea.append(title);

    const forest = renderForestPlot(allAnalyses, data.groups);
    if (forest) chartArea.append(forest);
  }

  // Bar charts for each outcome
  filteredOutcomes.forEach((outcome) => {
    if (!outcome.measurements.length) return;

    const title = document.createElement('h3');
    title.className = 'te-chart-title';
    title.textContent = outcome.title;
    chartArea.append(title);

    if (outcome.timeFrame) {
      const subtitle = document.createElement('p');
      subtitle.className = 'te-chart-subtitle';
      subtitle.textContent = `Time frame: ${outcome.timeFrame}`;
      chartArea.append(subtitle);
    }

    const chart = renderBarChart(outcome, data.groups);
    if (chart) chartArea.append(chart);

    // Accessible table
    chartArea.append(renderAccessibleTable(outcome, data.groups));
  });
}

function buildBaselineTable(data) {
  if (!data.baseline?.length) return null;

  const container = document.createElement('div');
  container.className = 'te-baseline';
  container.innerHTML = '<h3>Baseline Characteristics</h3>';

  const table = document.createElement('table');
  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = `<th>Characteristic</th>${data.groups.map((g) => `<th>${g.title}</th>`).join('')}`;
  thead.append(headerRow);
  table.append(thead);

  const tbody = document.createElement('tbody');
  data.baseline.forEach((measure) => {
    if (!measure.rows.length) return;
    // Measure header row
    if (measure.rows.length > 1 || measure.rows[0].classTitle) {
      const mRow = document.createElement('tr');
      mRow.innerHTML = `<td colspan="${data.groups.length + 1}"><strong>${measure.title}</strong> (${measure.unitOfMeasure || measure.paramType})</td>`;
      tbody.append(mRow);
    }

    measure.rows.forEach((row) => {
      const tr = document.createElement('tr');
      const label = row.classTitle || row.categoryTitle || measure.title;
      tr.innerHTML = `<td>${label}</td>${data.groups.map((g) => `<td>${row.values[g.id] ?? '–'}</td>`).join('')}`;
      tbody.append(tr);
    });
  });

  table.append(tbody);
  container.append(table);
  return container;
}

function buildFlowSection(data) {
  if (!data.participantFlow) return null;

  const container = document.createElement('div');
  container.className = 'te-flow';
  container.innerHTML = '<h3>Participant Flow</h3>';

  const flow = renderFlowDiagram(data.participantFlow, data.groups);
  if (flow) container.append(flow);
  return container;
}

function renderTrial(block, data, config) {
  block.innerHTML = '';

  // Header
  block.append(buildHeader(data, config));

  // Filters
  const chartArea = document.createElement('div');
  chartArea.className = 'te-chart-area';

  const statsContainer = document.createElement('div');

  function updateView() {
    const filters = getActiveFilters(block);
    const filtered = filterOutcomes(data.outcomes, filters);
    buildCharts(data, filtered, chartArea);

    // Stats panel
    const newStats = buildStatsPanel(filtered);
    statsContainer.innerHTML = '';
    statsContainer.append(newStats);
  }

  const filters = buildFilters(data, updateView);
  block.append(filters);

  // Main area (chart + stats side by side on desktop)
  const main = document.createElement('div');
  main.className = 'te-main';
  main.append(chartArea);
  main.append(statsContainer);
  block.append(main);

  // Initial render
  updateView();

  // Flow diagram
  const flow = buildFlowSection(data);
  if (flow) block.append(flow);

  // Baseline table
  const baseline = buildBaselineTable(data);
  if (baseline) block.append(baseline);
}

function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

function renderSearchCard(study) {
  const card = document.createElement('button');
  card.className = 'te-search-card';
  card.type = 'button';
  card.dataset.nctId = study.nctId;

  const conditions = study.conditions.slice(0, 3).join(', ');
  card.innerHTML = `
    <h3 class="te-search-card-title">${study.title}</h3>
    <div class="te-search-card-meta">
      ${study.phase ? `<span class="te-badge">${study.phase}</span>` : ''}
      ${study.enrollment ? `<span class="te-enrollment">n\u00a0=\u00a0${study.enrollment.toLocaleString()}</span>` : ''}
    </div>
    ${conditions ? `<p class="te-search-card-conditions">${conditions}</p>` : ''}
    ${study.sponsor ? `<p class="te-search-card-sponsor">${study.sponsor}</p>` : ''}
    <span class="te-search-card-nct">${study.nctId}</span>
  `;
  return card;
}

const SEARCH_SUGGESTIONS = ['osimertinib', 'lung cancer', 'dapagliflozin', 'AstraZeneca', 'breast cancer'];

function buildSuggestionChips(input) {
  const row = document.createElement('div');
  row.className = 'te-search-suggestions';
  const label = document.createElement('span');
  label.textContent = 'Try:';
  row.append(label);

  SEARCH_SUGGESTIONS.forEach((term) => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'te-suggestion-chip';
    chip.textContent = term;
    chip.addEventListener('click', () => {
      input.value = term;
      input.dispatchEvent(new Event('input'));
      input.focus();
    });
    row.append(chip);
  });
  return row;
}

async function renderSearchMode(block) {
  const workerUrl = getWorkerUrl();
  block.innerHTML = '';

  const wrapper = document.createElement('div');
  wrapper.className = 'te-search';

  const input = document.createElement('input');
  input.type = 'search';
  input.className = 'te-search-input';
  input.placeholder = 'Search trials by drug, condition, or sponsor\u2026';
  input.setAttribute('aria-label', 'Search clinical trials');
  wrapper.append(input);

  wrapper.append(buildSuggestionChips(input));

  const status = document.createElement('div');
  status.className = 'te-search-status';
  status.setAttribute('aria-live', 'polite');
  wrapper.append(status);

  const grid = document.createElement('div');
  grid.className = 'te-search-grid';
  wrapper.append(grid);

  block.append(wrapper);

  let lastResults = null;

  async function doSearch(query) {
    if (!query) {
      grid.innerHTML = '';
      status.innerHTML = '';
      lastResults = null;
      return;
    }

    status.innerHTML = 'Searching\u2026';
    grid.innerHTML = '';

    try {
      const resp = await fetch(`${workerUrl}/api/search?q=${encodeURIComponent(query)}`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      lastResults = data;

      status.innerHTML = data.totalCount
        ? `<strong>${data.totalCount}</strong> trial${data.totalCount !== 1 ? 's' : ''} with results found`
        : '';

      if (!data.studies.length) {
        grid.innerHTML = '<p class="te-search-empty">No trials with posted results match your query.</p>';
        return;
      }

      data.studies.forEach((study) => {
        grid.append(renderSearchCard(study));
      });
    } catch (err) {
      status.innerHTML = '';
      grid.innerHTML = `<p class="te-search-empty">Search failed: ${err.message}</p>`;
    }
  }

  const debouncedSearch = debounce(doSearch, 300);
  input.addEventListener('input', () => debouncedSearch(input.value.trim()));

  grid.addEventListener('click', async (e) => {
    const card = e.target.closest('.te-search-card');
    if (!card) return;

    const { nctId } = card.dataset;
    const study = lastResults?.studies?.find((s) => s.nctId === nctId);
    const trialName = study?.title || nctId;
    const lastQuery = input.value;

    const backBtn = document.createElement('button');
    backBtn.type = 'button';
    backBtn.className = 'te-back-btn';
    backBtn.textContent = '\u2190 Back to results';

    backBtn.addEventListener('click', () => {
      renderSearchMode(block).then(() => {
        const newInput = block.querySelector('.te-search-input');
        if (newInput && lastQuery) {
          newInput.value = lastQuery;
          newInput.dispatchEvent(new Event('input'));
        }
      });
    });

    // Fade out search, show loading
    block.innerHTML = '';
    block.append(backBtn);
    showLoading(block);

    try {
      const resp = await fetch(`${workerUrl}/api/trial/${nctId}`);
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.error || `HTTP ${resp.status}`);
      }
      const data = await resp.json();
      if (data.error) {
        showError(block, data.error);
        block.prepend(backBtn);
        return;
      }
      const skeleton = block.querySelector('.te-skeleton');
      if (skeleton) skeleton.remove();
      renderTrial(block, data, { 'trial-name': trialName });
      block.prepend(backBtn);
    } catch (err) {
      showError(block, `Could not load trial ${nctId}: ${err.message}`);
      block.prepend(backBtn);
    }
  });

  input.focus();
}

export default async function decorate(block) {
  const config = readBlockConfig(block);
  const nctId = config['nct-id'];

  if (!nctId) {
    await renderSearchMode(block);
    return;
  }

  showLoading(block);

  const workerUrl = getWorkerUrl();

  try {
    const resp = await fetch(`${workerUrl}/api/trial/${nctId}`);
    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      throw new Error(errData.error || `HTTP ${resp.status}`);
    }
    const data = await resp.json();
    if (data.error) {
      showError(block, data.error);
      return;
    }
    renderTrial(block, data, config);
  } catch (err) {
    showError(block, `Could not load trial ${nctId}: ${err.message}`);
  }
}
