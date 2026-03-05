import {
  renderBarChart, renderForestPlot, renderFlowDiagram, renderAccessibleTable,
} from '../trial-explorer/charts.js';

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

function el(tag, cls, html) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (html) node.innerHTML = html;
  return node;
}

function showLoading(container) {
  container.innerHTML = '';
  const skeleton = el('div', 'ct-skeleton');
  skeleton.innerHTML = '<div class="ct-skeleton-bar"></div><div class="ct-skeleton-bar"></div><div class="ct-skeleton-bar"></div><div class="ct-skeleton-bar"></div>';
  container.append(skeleton);
}

function showError(container, message) {
  container.innerHTML = '';
  container.append(el('div', 'ct-error', `<h3>Unable to Load Study</h3><p>${message}</p>`));
}

function formatStatus(status) {
  return (status || '').replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatDate(dateStr) {
  if (!dateStr) return '—';
  return dateStr;
}

// ─── HEADER ───

function buildHeader(data) {
  const { protocol: p } = data;
  const header = el('div', 'ct-header');
  const statusLabel = formatStatus(p.status.overallStatus);
  const phase = p.design.phases.filter((ph) => ph !== 'NA').join(', ');

  header.innerHTML = `
    <h2>${p.identification.officialTitle || p.identification.briefTitle}</h2>
    <div class="ct-header-meta">
      <span class="ct-status-badge" data-status="${p.status.overallStatus}">${statusLabel}</span>
      ${phase ? `<span class="ct-badge">${phase}</span>` : ''}
      ${p.design.enrollmentCount ? `<span class="ct-enrollment">n = ${p.design.enrollmentCount.toLocaleString()} (${p.design.enrollmentType.toLowerCase()})</span>` : ''}
      <span class="ct-nct-id">${p.identification.nctId}</span>
    </div>
  `;
  return header;
}

// ─── TABS ───

const TAB_DEFS = [
  { id: 'overview', label: 'Overview' },
  { id: 'eligibility', label: 'Eligibility' },
  { id: 'plan', label: 'Study Plan' },
  { id: 'outcomes', label: 'Study Endpoints' },
  { id: 'results', label: 'Results' },
  { id: 'locations', label: 'Locations' },
  { id: 'info', label: 'More Info' },
];

function buildTabs(data) {
  const tabBar = el('div', 'ct-tabs');
  tabBar.setAttribute('role', 'tablist');

  const panels = {};

  TAB_DEFS.forEach((def, i) => {
    // Hide Results tab if no results
    if (def.id === 'results' && !data.hasResults) return;

    const tab = el('button', 'ct-tab');
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
    tab.setAttribute('aria-controls', `ct-panel-${def.id}`);
    tab.id = `ct-tab-${def.id}`;
    tab.textContent = def.label;
    tab.type = 'button';

    const panel = el('div', 'ct-panel');
    panel.id = `ct-panel-${def.id}`;
    panel.setAttribute('role', 'tabpanel');
    panel.setAttribute('aria-labelledby', `ct-tab-${def.id}`);
    panel.setAttribute('aria-hidden', i === 0 ? 'false' : 'true');

    tab.addEventListener('click', () => {
      tabBar.querySelectorAll('.ct-tab').forEach((t) => t.setAttribute('aria-selected', 'false'));
      tab.setAttribute('aria-selected', 'true');
      Object.values(panels).forEach((p) => p.setAttribute('aria-hidden', 'true'));
      panel.setAttribute('aria-hidden', 'false');
    });

    tabBar.append(tab);
    panels[def.id] = panel;
  });

  return { tabBar, panels };
}

// ─── OVERVIEW PANEL ───

function buildOverviewPanel(data) {
  const p = data.protocol;
  const frag = document.createDocumentFragment();

  // Brief Summary
  if (p.description.briefSummary) {
    frag.append(el('h3', 'ct-subsection-title', 'Brief Summary'));
    frag.append(el('p', 'ct-description', p.description.briefSummary));
  }

  // Study Details grid
  frag.append(el('h3', 'ct-subsection-title', 'Study Details'));
  const grid = el('div', 'ct-info-grid');
  const rows = [
    ['Study Type', p.design.studyType ? formatStatus(p.design.studyType) : '—'],
    ['Phase', p.design.phases.filter((ph) => ph !== 'NA').join(', ') || 'Not Applicable'],
    ['Enrollment', p.design.enrollmentCount ? `${p.design.enrollmentCount.toLocaleString()} (${formatStatus(p.design.enrollmentType)})` : '—'],
    ['Allocation', p.design.allocation ? formatStatus(p.design.allocation) : '—'],
    ['Intervention Model', p.design.interventionModel ? formatStatus(p.design.interventionModel) : '—'],
    ['Masking', p.design.masking ? formatStatus(p.design.masking) : '—'],
    ['Primary Purpose', p.design.primaryPurpose ? formatStatus(p.design.primaryPurpose) : '—'],
  ];
  if (p.conditions.length) {
    rows.unshift(['Conditions', p.conditions.join(', ')]);
  }
  rows.forEach(([label, value]) => {
    grid.append(el('div', 'ct-info-label', label));
    grid.append(el('div', 'ct-info-value', value));
  });
  frag.append(grid);

  // Key Dates
  frag.append(el('h3', 'ct-subsection-title', 'Key Dates'));
  const dateGrid = el('div', 'ct-info-grid');
  [
    ['Status', formatStatus(p.status.overallStatus)],
    ['Start Date', `${formatDate(p.status.startDate)} (${formatStatus(p.status.startDateType || 'ACTUAL')})`],
    ['Primary Completion', `${formatDate(p.status.primaryCompletionDate)} (${formatStatus(p.status.primaryCompletionDateType || '')})`],
    ['Study Completion', `${formatDate(p.status.completionDate)} (${formatStatus(p.status.completionDateType || '')})`],
    ['First Posted', formatDate(p.status.studyFirstPostDate)],
    ['Last Update Posted', formatDate(p.status.lastUpdatePostDate)],
  ].forEach(([label, value]) => {
    dateGrid.append(el('div', 'ct-info-label', label));
    dateGrid.append(el('div', 'ct-info-value', value));
  });
  frag.append(dateGrid);

  // Detailed Description
  if (p.description.detailedDescription) {
    frag.append(el('h3', 'ct-subsection-title', 'Detailed Description'));
    frag.append(el('p', 'ct-description', p.description.detailedDescription));
  }

  return frag;
}

// ─── CRITERIA LIST HELPER ───

function buildCriteriaList(text, type) {
  const ol = el('ol', `ct-criteria-list ct-criteria-${type}`);
  const lines = text.split(/\n/).map((l) => l.trim()).filter(Boolean);
  lines.forEach((line) => {
    // Strip leading numbering like "1." or "- "
    const cleaned = line.replace(/^\d+[.)]\s*/, '').replace(/^[-•]\s*/, '');
    if (!cleaned) return;
    const li = document.createElement('li');
    li.textContent = cleaned;
    ol.append(li);
  });
  if (!ol.children.length) {
    // Fallback: render as plain text
    return el('div', 'ct-criteria', text);
  }
  return ol;
}

// ─── ELIGIBILITY PANEL ───

function buildEligibilityPanel(data) {
  const p = data.protocol;
  const frag = document.createDocumentFragment();

  // Quick facts
  const grid = el('div', 'ct-info-grid');
  [
    ['Sex', p.eligibility.sex ? formatStatus(p.eligibility.sex) : '—'],
    ['Age Groups', p.eligibility.stdAges.map(formatStatus).join(', ') || '—'],
    ['Minimum Age', p.eligibility.minimumAge || 'N/A'],
    ['Maximum Age', p.eligibility.maximumAge || 'N/A'],
    ['Accepts Healthy Volunteers', p.eligibility.healthyVolunteers ? 'Yes' : 'No'],
  ].forEach(([label, value]) => {
    grid.append(el('div', 'ct-info-label', label));
    grid.append(el('div', 'ct-info-value', value));
  });
  frag.append(grid);

  // Criteria — parse into Inclusion / Exclusion sections
  if (p.eligibility.criteria) {
    const raw = p.eligibility.criteria;
    const inclIdx = raw.search(/inclusion\s+criteria/i);
    const exclIdx = raw.search(/exclusion\s+criteria/i);

    if (inclIdx >= 0 && exclIdx > inclIdx) {
      const inclText = raw.substring(inclIdx, exclIdx).trim();
      const exclText = raw.substring(exclIdx).trim();

      frag.append(el('h3', 'ct-subsection-title', 'Inclusion Criteria'));
      frag.append(buildCriteriaList(
        inclText.replace(/^inclusion\s+criteria:?\s*/i, ''),
        'inclusion',
      ));
      frag.append(el('h3', 'ct-subsection-title', 'Exclusion Criteria'));
      frag.append(buildCriteriaList(
        exclText.replace(/^exclusion\s+criteria:?\s*/i, ''),
        'exclusion',
      ));
    } else {
      frag.append(el('h3', 'ct-subsection-title', 'Eligibility Criteria'));
      frag.append(el('div', 'ct-criteria', raw));
    }
  }

  return frag;
}

// ─── STUDY PLAN PANEL ───

function buildStudyPlanPanel(data) {
  const p = data.protocol;
  const frag = document.createDocumentFragment();

  // Arms
  if (p.arms.length) {
    frag.append(el('h3', 'ct-subsection-title', 'Arms'));
    const wrap = el('div', 'ct-table-wrap');
    const table = el('table', 'ct-table');
    table.innerHTML = `
      <thead><tr><th>Arm</th><th>Type</th><th>Description</th></tr></thead>
      <tbody>${p.arms.map((a) => `<tr><td><strong>${a.label}</strong></td><td>${formatStatus(a.type)}</td><td>${a.description}</td></tr>`).join('')}</tbody>
    `;
    wrap.append(table);
    frag.append(wrap);
  }

  // Interventions
  if (p.interventions.length) {
    frag.append(el('h3', 'ct-subsection-title', 'Interventions'));
    const wrap = el('div', 'ct-table-wrap');
    const table = el('table', 'ct-table');
    table.innerHTML = `
      <thead><tr><th>Intervention</th><th>Type</th><th>Description</th><th>Assigned Arms</th></tr></thead>
      <tbody>${p.interventions.map((iv) => `<tr><td><strong>${iv.name}</strong></td><td>${formatStatus(iv.type)}</td><td>${iv.description}</td><td>${iv.armGroupLabels.join(', ')}</td></tr>`).join('')}</tbody>
    `;
    wrap.append(table);
    frag.append(wrap);
  }

  return frag;
}

// ─── OUTCOME MEASURES PANEL (planned) ───

function buildOutcomesPanel(data) {
  const p = data.protocol;
  const frag = document.createDocumentFragment();

  function renderOutcomeGroup(title, outcomes, badgeClass) {
    if (!outcomes.length) return;
    frag.append(el('h3', 'ct-subsection-title', `${title} (${outcomes.length})`));
    outcomes.forEach((o) => {
      const card = el('div', 'ct-outcome-card');
      card.innerHTML = `
        <span class="ct-outcome-type-badge ${badgeClass}">${title.replace(' Outcomes', '')}</span>
        <h4>${o.measure}</h4>
        ${o.description ? `<p>${o.description}</p>` : ''}
        ${o.timeFrame ? `<p class="ct-outcome-timeframe">Time frame: ${o.timeFrame}</p>` : ''}
      `;
      frag.append(card);
    });
  }

  renderOutcomeGroup('Primary Outcomes', p.plannedOutcomes.primary, 'primary');
  renderOutcomeGroup('Secondary Outcomes', p.plannedOutcomes.secondary, 'secondary');
  renderOutcomeGroup('Other Outcomes', p.plannedOutcomes.other, 'other');

  const { primary, secondary, other } = p.plannedOutcomes;
  if (!primary.length && !secondary.length && !other.length) {
    frag.append(el('p', 'ct-no-results', 'No outcome measures specified.'));
  }

  return frag;
}

// ─── RESULTS PANEL ───

function buildLegend(groups) {
  const legend = el('div', 'ct-legend');
  const colors = ['var(--ct-color-treatment)', 'var(--ct-color-control)', 'var(--ct-color-alt)', 'var(--ct-color-alt2)'];
  groups.forEach((g, i) => {
    const item = el('div', 'ct-legend-item');
    item.innerHTML = `<span class="ct-legend-swatch" style="background:${colors[i % colors.length]}"></span><span>${g.title}</span>`;
    legend.append(item);
  });
  return legend;
}

function buildStatsPanel(outcomes) {
  const panel = el('div', 'ct-stats');
  panel.innerHTML = '<h3>Key Statistics</h3>';
  const grid = el('div', 'ct-stat-grid');

  const allAnalyses = outcomes.flatMap((o) => o.analyses || []);
  if (!allAnalyses.length) {
    grid.innerHTML = '<p style="font-size:13px;color:#666;">No statistical analyses available.</p>';
    panel.append(grid);
    return panel;
  }

  allAnalyses.forEach((a) => {
    if (a.estimateValue != null) {
      const item = el('div', 'ct-stat-item');
      const isSig = a.pValue != null && a.pValue < 0.05;
      item.innerHTML = `<span class="ct-stat-label">${a.estimateType || 'Estimate'}</span><span class="ct-stat-value${isSig ? ' ct-significant' : ''}">${a.estimateValue.toFixed(2)}</span>`;
      grid.append(item);
    }
    if (a.pValue != null) {
      const item = el('div', 'ct-stat-item');
      const isSig = a.pValue < 0.05;
      item.innerHTML = `<span class="ct-stat-label">p-value</span><span class="ct-stat-value${isSig ? ' ct-significant' : ''}">${a.pValue < 0.001 ? '<0.001' : a.pValue.toFixed(4)}</span>`;
      grid.append(item);
    }
    if (a.ciLower != null && a.ciUpper != null) {
      const item = el('div', 'ct-stat-item');
      item.innerHTML = `<span class="ct-stat-label">${a.ciPercent || 95}% CI</span><span class="ct-stat-value" style="font-size:18px;">${a.ciLower.toFixed(2)} – ${a.ciUpper.toFixed(2)}</span>`;
      grid.append(item);
    }
  });

  panel.append(grid);
  return panel;
}

function buildResultsOutcomesSubPanel(data) {
  const frag = document.createDocumentFragment();
  if (!data.outcomes?.length) {
    frag.append(el('p', 'ct-no-results', 'No outcome measure results posted.'));
    return frag;
  }

  // Filter tabs: Primary / Secondary / All
  const types = [...new Set(data.outcomes.map((o) => o.type))].filter(Boolean);
  let activeFilter = 'All';

  const filterBar = el('div', 'ct-results-sub-tabs');
  const chartArea = el('div', 'ct-chart-area');
  const statsContainer = el('div');

  function renderCharts() {
    const filtered = activeFilter === 'All' ? data.outcomes : data.outcomes.filter((o) => o.type === activeFilter);
    chartArea.innerHTML = '';
    chartArea.append(buildLegend(data.groups));

    const allAnalyses = filtered.flatMap((o) => o.analyses || []);
    if (allAnalyses.length) {
      chartArea.append(el('h4', 'ct-chart-title', 'Treatment Effect (Forest Plot)'));
      const forest = renderForestPlot(allAnalyses, data.groups);
      if (forest) chartArea.append(forest);
    }

    filtered.forEach((outcome) => {
      if (!outcome.measurements.length) return;
      chartArea.append(el('h4', 'ct-chart-title', outcome.title));
      if (outcome.timeFrame) {
        chartArea.append(el('p', 'ct-chart-subtitle', `Time frame: ${outcome.timeFrame}`));
      }
      const chart = renderBarChart(outcome, data.groups);
      if (chart) chartArea.append(chart);
      chartArea.append(renderAccessibleTable(outcome, data.groups));
    });

    statsContainer.innerHTML = '';
    statsContainer.append(buildStatsPanel(filtered));
  }

  if (types.length > 1) {
    const labels = { PRIMARY: 'Primary', SECONDARY: 'Secondary' };
    ['All', ...types].forEach((t, i) => {
      const btn = el('button', 'ct-results-sub-tab');
      btn.textContent = labels[t] || t;
      btn.type = 'button';
      btn.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
      btn.addEventListener('click', () => {
        filterBar.querySelectorAll('.ct-results-sub-tab').forEach((b) => b.setAttribute('aria-selected', 'false'));
        btn.setAttribute('aria-selected', 'true');
        activeFilter = t;
        renderCharts();
      });
      filterBar.append(btn);
    });
    frag.append(filterBar);
  }

  const layout = el('div', 'ct-results-layout');
  layout.append(chartArea);
  layout.append(statsContainer);
  frag.append(layout);

  renderCharts();
  return frag;
}

function buildResultsFlowSubPanel(data) {
  const frag = document.createDocumentFragment();
  if (!data.participantFlow) {
    frag.append(el('p', 'ct-no-results', 'No participant flow data posted.'));
    return frag;
  }

  const container = el('div', 'ct-flow');
  const flow = renderFlowDiagram(data.participantFlow, data.groups);
  if (flow) container.append(flow);

  // Drop/withdraw reasons table
  const period = data.participantFlow.periods?.[0];
  if (period?.dropWithdraws?.length) {
    container.append(el('h4', 'ct-chart-title', 'Drop/Withdraw Reasons'));
    const wrap = el('div', 'ct-table-wrap');
    const table = el('table', 'ct-table');
    const groups = data.participantFlow.groups || data.groups;
    table.innerHTML = `
      <thead><tr><th>Reason</th>${groups.map((g) => `<th>${g.title}</th>`).join('')}</tr></thead>
      <tbody>${period.dropWithdraws.map((d) => {
    const counts = Object.fromEntries((d.reasons || []).map((r) => [r.groupId, r.count]));
    return `<tr><td>${d.type}</td>${groups.map((g) => `<td class="ct-cell-num">${counts[g.id] ?? '—'}</td>`).join('')}</tr>`;
  }).join('')}</tbody>
    `;
    wrap.append(table);
    container.append(wrap);
  }

  frag.append(container);
  return frag;
}

function buildResultsBaselineSubPanel(data) {
  const frag = document.createDocumentFragment();
  if (!data.baseline?.length) {
    frag.append(el('p', 'ct-no-results', 'No baseline data posted.'));
    return frag;
  }

  const wrap = el('div', 'ct-baseline-table');
  const table = el('table', 'ct-table');
  const thead = el('thead');
  const headerRow = el('tr');
  headerRow.innerHTML = `<th>Characteristic</th>${data.groups.map((g) => `<th>${g.title}</th>`).join('')}`;
  thead.append(headerRow);
  table.append(thead);

  const tbody = el('tbody');
  data.baseline.forEach((measure) => {
    if (!measure.rows.length) return;
    if (measure.rows.length > 1 || measure.rows[0].classTitle) {
      const mRow = el('tr');
      mRow.innerHTML = `<td colspan="${data.groups.length + 1}"><strong>${measure.title}</strong> (${measure.unitOfMeasure || measure.paramType})</td>`;
      tbody.append(mRow);
    }
    measure.rows.forEach((row) => {
      const tr = el('tr');
      const label = row.classTitle || row.categoryTitle || measure.title;
      tr.innerHTML = `<td>${label}</td>${data.groups.map((g) => `<td class="ct-cell-num">${row.values[g.id] ?? '—'}</td>`).join('')}`;
      tbody.append(tr);
    });
  });

  table.append(tbody);
  wrap.append(table);
  frag.append(wrap);
  return frag;
}

function buildResultsAdverseEventsSubPanel(data) {
  const frag = document.createDocumentFragment();
  const ae = data.adverseEvents;
  if (!ae) {
    frag.append(el('p', 'ct-no-results', 'No adverse event data posted.'));
    return frag;
  }

  // Description and timeframe
  if (ae.description) {
    frag.append(el('p', 'ct-description', ae.description));
  }
  if (ae.timeFrame) {
    frag.append(el('p', null, `<strong>Time frame:</strong> ${ae.timeFrame}`));
  }

  // Summary cards
  const summary = el('div', 'ct-ae-summary');
  ae.groups.forEach((g) => {
    const card = el('div', 'ct-ae-summary-card');
    card.innerHTML = `
      <span class="ct-ae-label">${g.title}</span>
      <span class="ct-ae-count">${g.seriousNumAffected}</span>
      <span class="ct-ae-label">Serious / ${g.seriousNumAtRisk} at risk</span>
    `;
    summary.append(card);
  });
  frag.append(summary);

  // Events grouped by organ system
  function renderEventSection(title, events) {
    if (!events.length) return;
    frag.append(el('h3', 'ct-subsection-title', `${title} (${events.length} events)`));

    // Group by organ system
    const byOrgan = new Map();
    events.forEach((ev) => {
      const organ = ev.organSystem || 'Other';
      if (!byOrgan.has(organ)) byOrgan.set(organ, []);
      byOrgan.get(organ).push(ev);
    });

    byOrgan.forEach((organEvents, organName) => {
      const header = el('button', 'ct-ae-organ-header');
      header.type = 'button';
      header.setAttribute('aria-expanded', 'false');
      header.innerHTML = `<span>${organName} <span class="ct-ae-organ-count">(${organEvents.length})</span></span>`;

      const body = el('div', 'ct-ae-organ-body');
      body.setAttribute('aria-hidden', 'true');

      const wrap = el('div', 'ct-table-wrap');
      const table = el('table', 'ct-table');
      table.innerHTML = `
        <thead><tr><th>Term</th>${ae.groups.map((g) => `<th>${g.title}</th>`).join('')}</tr></thead>
        <tbody>${organEvents.map((ev) => {
    const statsByGroup = Object.fromEntries(ev.stats.map((s) => [s.groupId, s]));
    return `<tr><td>${ev.term}</td>${ae.groups.map((g) => {
      const s = statsByGroup[g.id];
      return `<td class="ct-cell-num">${s ? `${s.numAffected}/${s.numAtRisk}` : '—'}</td>`;
    }).join('')}</tr>`;
  }).join('')}</tbody>
      `;
      wrap.append(table);
      body.append(wrap);

      header.addEventListener('click', () => {
        const expanded = header.getAttribute('aria-expanded') === 'true';
        header.setAttribute('aria-expanded', String(!expanded));
        body.setAttribute('aria-hidden', String(expanded));
      });

      frag.append(header);
      frag.append(body);
    });
  }

  renderEventSection('Serious Adverse Events', ae.seriousEvents);
  renderEventSection('Other Adverse Events', ae.otherEvents);

  return frag;
}

function buildResultsSummary(data) {
  const allAnalyses = (data.outcomes || []).flatMap((o) => o.analyses || []);
  if (!allAnalyses.length) return null;

  const card = el('div', 'ct-results-summary');
  card.innerHTML = '<h3>Key Finding</h3>';
  const grid = el('div', 'ct-results-summary-grid');

  allAnalyses.slice(0, 1).forEach((a) => {
    if (a.estimateValue != null) {
      const item = el('div', 'ct-results-summary-item');
      const isSig = a.pValue != null && a.pValue < 0.05;
      item.innerHTML = `
        <span class="ct-rsum-label">${a.estimateType || 'Estimate'}</span>
        <span class="ct-rsum-value${isSig ? ' ct-significant' : ''}">${a.estimateValue.toFixed(2)}</span>
      `;
      grid.append(item);
    }
    if (a.ciLower != null && a.ciUpper != null) {
      const item = el('div', 'ct-results-summary-item');
      item.innerHTML = `
        <span class="ct-rsum-label">${a.ciPercent || 95}% CI</span>
        <span class="ct-rsum-value">${a.ciLower.toFixed(2)} – ${a.ciUpper.toFixed(2)}</span>
      `;
      grid.append(item);
    }
    if (a.pValue != null) {
      const item = el('div', 'ct-results-summary-item');
      const isSig = a.pValue < 0.05;
      item.innerHTML = `
        <span class="ct-rsum-label">p-value</span>
        <span class="ct-rsum-value${isSig ? ' ct-significant' : ''}">${a.pValue < 0.001 ? '<0.001' : a.pValue.toFixed(4)}</span>
      `;
      grid.append(item);
    }
  });

  card.append(grid);
  return card;
}

function buildResultsPanel(data) {
  const frag = document.createDocumentFragment();

  // Results Summary card
  const summary = buildResultsSummary(data);
  if (summary) frag.append(summary);

  // Sub-tabs within Results
  const subTabDefs = [
    { id: 'outcomes', label: 'Outcome Measures' },
    { id: 'flow', label: 'Participant Flow' },
    { id: 'baseline', label: 'Baseline' },
    { id: 'ae', label: 'Adverse Events' },
  ];

  const subTabBar = el('div', 'ct-results-sub-tabs');
  const subPanels = {};

  subTabDefs.forEach((def, i) => {
    const btn = el('button', 'ct-results-sub-tab');
    btn.textContent = def.label;
    btn.type = 'button';
    btn.setAttribute('aria-selected', i === 0 ? 'true' : 'false');

    const panel = el('div', 'ct-results-sub-panel');
    panel.setAttribute('aria-hidden', i === 0 ? 'false' : 'true');

    btn.addEventListener('click', () => {
      subTabBar.querySelectorAll('.ct-results-sub-tab').forEach((b) => b.setAttribute('aria-selected', 'false'));
      btn.setAttribute('aria-selected', 'true');
      Object.values(subPanels).forEach((p) => p.setAttribute('aria-hidden', 'true'));
      panel.setAttribute('aria-hidden', 'false');
    });

    subTabBar.append(btn);
    subPanels[def.id] = panel;
  });

  frag.append(subTabBar);

  // Populate sub-panels
  subPanels.outcomes.append(buildResultsOutcomesSubPanel(data));
  subPanels.flow.append(buildResultsFlowSubPanel(data));
  subPanels.baseline.append(buildResultsBaselineSubPanel(data));
  subPanels.ae.append(buildResultsAdverseEventsSubPanel(data));

  Object.values(subPanels).forEach((p) => frag.append(p));
  return frag;
}

// ─── LOCATIONS PANEL ───

function buildLocationsPanel(data) {
  const p = data.protocol;
  const frag = document.createDocumentFragment();

  // Officials
  if (p.contacts.officials.length) {
    frag.append(el('h3', 'ct-subsection-title', 'Study Officials'));
    const wrap = el('div', 'ct-table-wrap');
    const table = el('table', 'ct-table');
    table.innerHTML = `
      <thead><tr><th>Name</th><th>Role</th><th>Affiliation</th></tr></thead>
      <tbody>${p.contacts.officials.map((o) => `<tr><td>${o.name}</td><td>${formatStatus(o.role)}</td><td>${o.affiliation}</td></tr>`).join('')}</tbody>
    `;
    wrap.append(table);
    frag.append(wrap);
  }

  // Locations grouped by country
  if (p.contacts.locations.length) {
    const byCountry = new Map();
    p.contacts.locations.forEach((loc) => {
      const country = loc.country || 'Unknown';
      if (!byCountry.has(country)) byCountry.set(country, []);
      byCountry.get(country).push(loc);
    });

    const countryCount = byCountry.size;
    const locCount = p.contacts.locations.length;
    frag.append(el(
      'h3',
      'ct-subsection-title',
      `Study Locations (${locCount} across ${countryCount} ${countryCount === 1 ? 'country' : 'countries'})`,
    ));

    byCountry.forEach((locs, country) => {
      const header = el('button', 'ct-country-header');
      header.type = 'button';
      header.setAttribute('aria-expanded', countryCount === 1 ? 'true' : 'false');
      header.innerHTML = `<span>${country} <span class="ct-country-count">(${locs.length})</span></span>`;

      const body = el('div', 'ct-country-body');
      body.setAttribute('aria-hidden', countryCount === 1 ? 'false' : 'true');

      const grid = el('div', 'ct-locations-grid');
      locs.forEach((loc) => {
        const card = el('div', 'ct-location-card');
        const parts = [loc.city, loc.state, loc.zip].filter(Boolean).join(', ');
        card.innerHTML = `
          <div class="ct-location-facility">${loc.facility || 'Unnamed Facility'}</div>
          <div class="ct-location-address">${parts}</div>
        `;
        grid.append(card);
      });
      body.append(grid);

      header.addEventListener('click', () => {
        const expanded = header.getAttribute('aria-expanded') === 'true';
        header.setAttribute('aria-expanded', String(!expanded));
        body.setAttribute('aria-hidden', String(expanded));
      });

      frag.append(header);
      frag.append(body);
    });
  }

  if (!p.contacts.officials.length && !p.contacts.locations.length) {
    frag.append(el('p', 'ct-no-results', 'No contact or location information available.'));
  }

  return frag;
}

// ─── MORE INFO PANEL ───

function buildInfoPanel(data) {
  const p = data.protocol;
  const frag = document.createDocumentFragment();

  // Sponsor & Collaborators
  frag.append(el('h3', 'ct-subsection-title', 'Sponsor & Collaborators'));
  const grid = el('div', 'ct-info-grid');
  const sponsorRows = [
    ['Lead Sponsor', p.sponsor.leadSponsor || '—'],
    ['Sponsor Type', formatStatus(p.sponsor.leadSponsorClass) || '—'],
    ['Responsible Party', formatStatus(p.sponsor.responsiblePartyType) || '—'],
  ];
  if (p.sponsor.collaborators.length) {
    sponsorRows.push(['Collaborators', p.sponsor.collaborators.map((c) => c.name).join(', ')]);
  }
  sponsorRows.push(['Data Monitoring Committee', p.oversightHasDmc ? 'Yes' : 'No']);
  sponsorRows.push(['IPD Sharing', p.ipdSharing || '—']);

  sponsorRows.forEach(([label, value]) => {
    grid.append(el('div', 'ct-info-label', label));
    grid.append(el('div', 'ct-info-value', value));
  });
  frag.append(grid);

  // Study IDs
  frag.append(el('h3', 'ct-subsection-title', 'Study Identifiers'));
  const idGrid = el('div', 'ct-info-grid');
  [
    ['NCT Number', p.identification.nctId],
    ['Organization Study ID', p.identification.orgStudyId || '—'],
    ['Organization', p.identification.organization || '—'],
  ].forEach(([label, value]) => {
    idGrid.append(el('div', 'ct-info-label', label));
    idGrid.append(el('div', 'ct-info-value', value));
  });
  frag.append(idGrid);

  // References
  if (p.references.length) {
    frag.append(el('h3', 'ct-subsection-title', `References (${p.references.length})`));
    p.references.forEach((ref) => {
      const refEl = el('div', 'ct-reference');
      refEl.innerHTML = `
        <span class="ct-reference-type">${ref.type}</span>
        ${ref.citation}
        ${ref.pmid ? ` <a class="ct-pmid-link" href="https://pubmed.ncbi.nlm.nih.gov/${ref.pmid}/" target="_blank" rel="noopener">PMID: ${ref.pmid}</a>` : ''}
      `;
      frag.append(refEl);
    });
  }

  // Keywords
  if (p.keywords?.length) {
    frag.append(el('h3', 'ct-subsection-title', 'Keywords'));
    frag.append(el('p', null, p.keywords.join(', ')));
  }

  return frag;
}

// ─── FULL STUDY RENDER ───

function renderStudy(block, data) {
  block.innerHTML = '';

  block.append(buildHeader(data));

  const { tabBar, panels } = buildTabs(data);
  block.append(tabBar);

  // Build each panel's content
  panels.overview?.append(buildOverviewPanel(data));
  panels.eligibility?.append(buildEligibilityPanel(data));
  panels.plan?.append(buildStudyPlanPanel(data));
  panels.outcomes?.append(buildOutcomesPanel(data));
  if (data.hasResults && panels.results) {
    panels.results.append(buildResultsPanel(data));
  }
  panels.locations?.append(buildLocationsPanel(data));
  panels.info?.append(buildInfoPanel(data));

  Object.values(panels).forEach((p) => block.append(p));
}

// ─── SEARCH MODE ───

function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

const SEARCH_SUGGESTIONS = ['osimertinib', 'lung cancer', 'dapagliflozin', 'heart failure', 'breast cancer'];

async function renderSearchMode(block) {
  const workerUrl = getWorkerUrl();
  block.innerHTML = '';

  const wrapper = el('div', 'ct-search');

  const input = document.createElement('input');
  input.type = 'search';
  input.className = 'ct-search-input';
  input.placeholder = 'Search clinical trials by drug, condition, or sponsor\u2026';
  input.setAttribute('aria-label', 'Search clinical trials');
  wrapper.append(input);

  // Suggestion chips
  const chips = el('div', 'ct-search-suggestions');
  chips.append(el('span', null, 'Try:'));
  SEARCH_SUGGESTIONS.forEach((term) => {
    const chip = el('button', 'ct-suggestion-chip', term);
    chip.type = 'button';
    chip.addEventListener('click', () => {
      input.value = term;
      input.dispatchEvent(new Event('input'));
      input.focus();
    });
    chips.append(chip);
  });
  wrapper.append(chips);

  const status = el('div', 'ct-search-status');
  status.setAttribute('aria-live', 'polite');
  wrapper.append(status);

  const grid = el('div', 'ct-search-grid');
  wrapper.append(grid);

  block.append(wrapper);

  let lastQuery = '';

  async function doSearch(query) {
    if (!query) {
      grid.innerHTML = '';
      status.innerHTML = '';
      return;
    }

    status.innerHTML = 'Searching\u2026';
    grid.innerHTML = '';

    try {
      const resp = await fetch(`${workerUrl}/api/search?q=${encodeURIComponent(query)}`);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const searchData = await resp.json();

      status.innerHTML = searchData.totalCount
        ? `<strong>${searchData.totalCount}</strong> trial${searchData.totalCount !== 1 ? 's' : ''} found`
        : '';

      if (!searchData.studies.length) {
        grid.innerHTML = '<p class="ct-search-empty">No trials match your query.</p>';
        return;
      }

      searchData.studies.forEach((study) => {
        const card = el('button', 'ct-search-card');
        card.type = 'button';
        card.dataset.nctId = study.nctId;
        const conditions = study.conditions.slice(0, 3).join(', ');
        const statusLabel = formatStatus(study.status || '');
        card.innerHTML = `
          <h3>${study.title}</h3>
          <div class="ct-search-card-meta">
            ${study.status ? `<span class="ct-status-badge" data-status="${study.status}">${statusLabel}</span>` : ''}
            ${study.phase ? `<span class="ct-badge">${study.phase}</span>` : ''}
            ${study.enrollment ? `<span class="ct-enrollment">n\u00a0=\u00a0${study.enrollment.toLocaleString()}</span>` : ''}
          </div>
          ${conditions ? `<p class="ct-search-card-conditions">${conditions}</p>` : ''}
          ${study.sponsor ? `<p class="ct-search-card-sponsor">${study.sponsor}</p>` : ''}
          <span class="ct-search-card-nct">${study.nctId}</span>
        `;
        grid.append(card);
      });
    } catch (err) {
      status.innerHTML = '';
      grid.innerHTML = `<p class="ct-search-empty">Search failed: ${err.message}</p>`;
    }
  }

  const debouncedSearch = debounce(doSearch, 300);
  input.addEventListener('input', () => {
    lastQuery = input.value.trim();
    debouncedSearch(lastQuery);
  });

  grid.addEventListener('click', async (e) => {
    const card = e.target.closest('.ct-search-card');
    if (!card) return;

    const { nctId } = card.dataset;
    const savedQuery = lastQuery;

    const backBtn = el('button', 'ct-back-btn', '\u2190 Back to results');
    backBtn.type = 'button';
    backBtn.addEventListener('click', () => {
      renderSearchMode(block).then(() => {
        const newInput = block.querySelector('.ct-search-input');
        if (newInput && savedQuery) {
          newInput.value = savedQuery;
          newInput.dispatchEvent(new Event('input'));
        }
      });
    });

    block.innerHTML = '';
    block.append(backBtn);
    showLoading(block);

    try {
      const resp = await fetch(`${workerUrl}/api/study/${nctId}`);
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.error || `HTTP ${resp.status}`);
      }
      const studyData = await resp.json();
      const skeleton = block.querySelector('.ct-skeleton');
      if (skeleton) skeleton.remove();
      renderStudy(block, studyData);
      block.prepend(backBtn);
    } catch (err) {
      showError(block, `Could not load study ${nctId}: ${err.message}`);
      block.prepend(backBtn);
    }
  });

  input.focus();
}

// ─── ENTRY POINT ───

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
    const resp = await fetch(`${workerUrl}/api/study/${nctId}`);
    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      throw new Error(errData.error || `HTTP ${resp.status}`);
    }
    const data = await resp.json();
    renderStudy(block, data, config);
  } catch (err) {
    showError(block, `Could not load study ${nctId}: ${err.message}`);
  }
}
