/**
 * Pure SVG chart rendering for clinical trial data.
 * No external dependencies — uses document.createElementNS for all SVG.
 */

const SVG_NS = 'http://www.w3.org/2000/svg';

// Color palette for treatment arms — uses CSS custom properties at runtime
const GROUP_COLORS = [
  'var(--te-color-treatment)',
  'var(--te-color-control)',
  'var(--te-color-alt)',
  'var(--te-color-alt2)',
];

function svgEl(tag, attrs = {}) {
  const el = document.createElementNS(SVG_NS, tag);
  Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}

function textEl(x, y, text, attrs = {}) {
  const el = svgEl('text', {
    x, y, 'font-family': "'Roboto', sans-serif", 'font-size': '12', fill: '#363b3b', ...attrs,
  });
  el.textContent = text;
  return el;
}

/**
 * Horizontal grouped bar chart with CI whisker lines.
 * Each outcome measurement row becomes a bar, grouped by treatment arm.
 */
export function renderBarChart(outcome, groups) {
  const { measurements, unitOfMeasure } = outcome;
  if (!measurements.length) return null;

  // Group measurements by classTitle (or single group if no classes)
  const classes = [];
  const classMap = new Map();
  measurements.forEach((m) => {
    const key = m.classTitle || '_default';
    if (!classMap.has(key)) {
      classMap.set(key, []);
      classes.push(key);
    }
    classMap.get(key).push(m);
  });

  const groupIds = groups.map((g) => g.id);
  const barHeight = 22;
  const barGap = 4;
  const groupGap = 20;
  const labelWidth = 160;
  const chartLeft = labelWidth + 10;
  const chartRight = 40; // space for value label
  const width = 600;
  const chartWidth = width - chartLeft - chartRight;

  // Find max value for scale
  const allValues = measurements.map((m) => {
    const upper = m.upper != null ? m.upper : m.value;
    return Math.max(m.value, upper);
  });
  const maxVal = Math.max(...allValues, 1) * 1.15;

  const rowsPerClass = groupIds.length;
  const classHeight = rowsPerClass * (barHeight + barGap) + groupGap;
  const totalHeight = classes.length * classHeight + 40; // 40 for axis

  const svg = svgEl('svg', {
    viewBox: `0 0 ${width} ${totalHeight}`,
    role: 'img',
    'aria-label': `Bar chart: ${outcome.title}`,
    class: 'te-bar-chart',
  });

  // Grid lines
  const gridSteps = 5;
  for (let i = 0; i <= gridSteps; i += 1) {
    const x = chartLeft + (i / gridSteps) * chartWidth;
    svg.append(svgEl('line', {
      x1: x, y1: 0, x2: x, y2: totalHeight - 40, stroke: 'var(--te-color-grid)', 'stroke-width': '1',
    }));
    const val = ((i / gridSteps) * maxVal).toFixed(1);
    svg.append(textEl(x, totalHeight - 22, val, { 'text-anchor': 'middle', 'font-size': '11', fill: '#999' }));
  }

  // Axis label
  if (unitOfMeasure) {
    svg.append(textEl(chartLeft + chartWidth / 2, totalHeight - 6, unitOfMeasure, {
      'text-anchor': 'middle', 'font-size': '11', fill: '#999',
    }));
  }

  classes.forEach((classKey, ci) => {
    const classMeasurements = classMap.get(classKey);
    const yBase = ci * classHeight + 10;

    // Class label
    if (classKey !== '_default') {
      svg.append(textEl(0, yBase + 4, classKey, {
        'font-size': '12', 'font-weight': 'bold', fill: 'var(--te-heading-color)',
      }));
    }

    groupIds.forEach((gid, gi) => {
      const m = classMeasurements.find((ms) => ms.groupId === gid);
      if (!m) return;

      const y = yBase + (classKey !== '_default' ? 16 : 0) + gi * (barHeight + barGap);
      const barW = Math.max((m.value / maxVal) * chartWidth, 2);
      const color = GROUP_COLORS[gi % GROUP_COLORS.length];

      // Bar
      const bar = svgEl('rect', {
        x: chartLeft,
        y,
        width: barW,
        height: barHeight,
        fill: color,
        rx: '2',
        class: 'te-bar',
      });
      svg.append(bar);

      // CI whisker
      if (m.lower != null && m.upper != null) {
        const ciX1 = chartLeft + (m.lower / maxVal) * chartWidth;
        const ciX2 = chartLeft + (m.upper / maxVal) * chartWidth;
        const ciY = y + barHeight / 2;
        svg.append(svgEl('line', {
          x1: ciX1, y1: ciY, x2: ciX2, y2: ciY, stroke: 'var(--te-color-ci-line)', 'stroke-width': '2',
        }));
        // Whisker caps
        svg.append(svgEl('line', {
          x1: ciX1, y1: ciY - 5, x2: ciX1, y2: ciY + 5, stroke: 'var(--te-color-ci-line)', 'stroke-width': '2',
        }));
        svg.append(svgEl('line', {
          x1: ciX2, y1: ciY - 5, x2: ciX2, y2: ciY + 5, stroke: 'var(--te-color-ci-line)', 'stroke-width': '2',
        }));
      }

      // Value label
      svg.append(textEl(chartLeft + barW + 6, y + barHeight / 2 + 4, m.value.toString(), {
        'font-size': '12', 'font-weight': 'bold',
      }));
    });
  });

  return svg;
}

/**
 * Forest plot — the pharma stakeholder crowd-pleaser.
 * Diamond at HR estimate, horizontal CI line, vertical reference at 1.0.
 */
// eslint-disable-next-line no-unused-vars
export function renderForestPlot(analyses, groups) {
  if (!analyses.length) return null;

  const width = 600;
  const rowHeight = 50;
  const labelWidth = 200;
  const chartLeft = labelWidth + 10;
  const chartRight = 60;
  const chartWidth = width - chartLeft - chartRight;
  const headerHeight = 30;
  const totalHeight = headerHeight + analyses.length * rowHeight + 30;

  // Log scale: find range
  const allVals = analyses.flatMap(
    (a) => [a.ciLower, a.ciUpper, a.estimateValue].filter((v) => v != null && v > 0),
  );
  const logMin = Math.log(Math.min(...allVals, 0.1));
  const logMax = Math.log(Math.max(...allVals, 10));
  const logRange = logMax - logMin || 1;

  function toX(val) {
    if (!val || val <= 0) return chartLeft;
    return chartLeft + ((Math.log(val) - logMin) / logRange) * chartWidth;
  }

  const svg = svgEl('svg', {
    viewBox: `0 0 ${width} ${totalHeight}`,
    role: 'img',
    'aria-label': 'Forest plot of treatment effect estimates',
    class: 'te-forest-plot',
  });

  // Header labels
  svg.append(textEl(chartLeft, 16, 'Favours Treatment', { 'font-size': '10', fill: '#999' }));
  svg.append(textEl(chartLeft + chartWidth, 16, 'Favours Control', { 'font-size': '10', fill: '#999', 'text-anchor': 'end' }));

  // Reference line at HR=1.0
  const refX = toX(1.0);
  svg.append(svgEl('line', {
    x1: refX,
    y1: headerHeight,
    x2: refX,
    y2: totalHeight - 20,
    stroke: 'var(--te-color-reference-line)',
    'stroke-width': '1',
    'stroke-dasharray': '4,3',
  }));
  svg.append(textEl(refX, totalHeight - 8, '1.0', { 'text-anchor': 'middle', 'font-size': '11', fill: '#999' }));

  // Log scale ticks
  [0.1, 0.25, 0.5, 1.0, 2.0, 4.0, 10.0].forEach((v) => {
    const x = toX(v);
    if (x >= chartLeft && x <= chartLeft + chartWidth) {
      svg.append(svgEl('line', {
        x1: x, y1: totalHeight - 24, x2: x, y2: totalHeight - 20, stroke: '#999', 'stroke-width': '1',
      }));
      if (v !== 1.0) {
        svg.append(textEl(x, totalHeight - 8, v.toString(), { 'text-anchor': 'middle', 'font-size': '10', fill: '#999' }));
      }
    }
  });

  analyses.forEach((a, i) => {
    const y = headerHeight + i * rowHeight + rowHeight / 2;

    // Label
    const label = a.estimateType || `Analysis ${i + 1}`;
    svg.append(textEl(0, y + 4, label, { 'font-size': '12', 'font-weight': 'bold' }));

    if (a.pValue != null) {
      svg.append(textEl(0, y + 18, `p = ${a.pValue}`, { 'font-size': '11', fill: '#666' }));
    }

    // CI line
    if (a.ciLower != null && a.ciUpper != null) {
      svg.append(svgEl('line', {
        x1: toX(a.ciLower),
        y1: y,
        x2: toX(a.ciUpper),
        y2: y,
        stroke: 'var(--te-color-treatment)',
        'stroke-width': '2',
      }));
    }

    // Diamond at estimate
    if (a.estimateValue != null && a.estimateValue > 0) {
      const cx = toX(a.estimateValue);
      const dSize = 8;
      const diamond = svgEl('polygon', {
        points: `${cx},${y - dSize} ${cx + dSize},${y} ${cx},${y + dSize} ${cx - dSize},${y}`,
        fill: 'var(--te-color-treatment)',
      });
      svg.append(diamond);

      // Value annotation
      svg.append(textEl(cx, y - dSize - 4, a.estimateValue.toFixed(2), {
        'text-anchor': 'middle', 'font-size': '11', 'font-weight': 'bold', fill: 'var(--te-color-treatment)',
      }));
    }
  });

  return svg;
}

/**
 * Participant flow diagram — horizontal funnel showing enrollment through completion.
 */
export function renderFlowDiagram(participantFlow, groups) {
  if (!participantFlow?.periods?.length) return null;

  const period = participantFlow.periods[0]; // Usually just "Overall Study"
  if (!period.milestones?.length) return null;

  const flowGroups = participantFlow.groups || groups;
  const width = 600;
  const boxWidth = 140;
  const boxHeight = 60;
  const arrowWidth = 40;
  const stageY = 30;
  const groupRowHeight = 28;

  // Extract milestone data
  const milestones = period.milestones.map((m) => ({
    label: m.type,
    counts: Object.fromEntries((m.achievements || []).map((a) => [a.groupId, a.count])),
  }));

  const totalWidth = milestones.length * (boxWidth + arrowWidth) - arrowWidth;
  const totalHeight = stageY + boxHeight + 10 + flowGroups.length * groupRowHeight + 20;

  const svg = svgEl('svg', {
    viewBox: `0 0 ${Math.max(totalWidth, width)} ${totalHeight}`,
    role: 'img',
    'aria-label': 'Participant flow diagram',
    class: 'te-flow-diagram',
  });

  milestones.forEach((ms, mi) => {
    const x = mi * (boxWidth + arrowWidth);

    // Stage box
    svg.append(svgEl('rect', {
      x,
      y: stageY,
      width: boxWidth,
      height: boxHeight,
      fill: mi === 0 ? 'var(--te-color-treatment)' : 'var(--te-pill-inactive-bg)',
      rx: '6',
    }));

    // Stage label
    svg.append(textEl(x + boxWidth / 2, stageY + 24, ms.label, {
      'text-anchor': 'middle',
      'font-size': '13',
      'font-weight': 'bold',
      fill: mi === 0 ? '#fff' : 'var(--te-body-color)',
    }));

    // Group counts inside box
    flowGroups.forEach((g, gi) => {
      const count = ms.counts[g.id] ?? '–';
      svg.append(textEl(x + boxWidth / 2, stageY + 42 + gi * 14, `${g.title}: ${count}`, {
        'text-anchor': 'middle',
        'font-size': '10',
        fill: mi === 0 ? 'rgba(255,255,255,0.8)' : '#666',
      }));
    });

    // Arrow to next
    if (mi < milestones.length - 1) {
      const arrowX = x + boxWidth;
      const arrowY = stageY + boxHeight / 2;
      svg.append(svgEl('line', {
        x1: arrowX + 4,
        y1: arrowY,
        x2: arrowX + arrowWidth - 4,
        y2: arrowY,
        stroke: 'var(--te-color-control)',
        'stroke-width': '2',
      }));
      // Arrowhead
      svg.append(svgEl('polygon', {
        points: `${arrowX + arrowWidth - 4},${arrowY} ${arrowX + arrowWidth - 12},${arrowY - 5} ${arrowX + arrowWidth - 12},${arrowY + 5}`,
        fill: 'var(--te-color-control)',
      }));
    }
  });

  return svg;
}

/**
 * Build a hidden accessible data table for screen readers.
 */
export function renderAccessibleTable(outcome, groups) {
  const table = document.createElement('table');
  table.className = 'te-sr-only';
  table.setAttribute('role', 'table');
  table.setAttribute('aria-label', outcome.title);

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  headerRow.innerHTML = `<th>Category</th>${groups.map((g) => `<th>${g.title}</th>`).join('')}`;
  thead.append(headerRow);
  table.append(thead);

  const tbody = document.createElement('tbody');
  const classMap = new Map();
  outcome.measurements.forEach((m) => {
    const key = m.classTitle || 'Result';
    if (!classMap.has(key)) classMap.set(key, new Map());
    classMap.get(key).set(m.groupId, m.value);
  });

  classMap.forEach((values, classTitle) => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${classTitle}</td>${groups.map((g) => `<td>${values.get(g.id) ?? '–'}</td>`).join('')}`;
    tbody.append(row);
  });

  table.append(tbody);
  return table;
}
