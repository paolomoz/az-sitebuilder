/**
 * Transform ClinicalTrials.gov API v2 response into flat chart-friendly JSON.
 */

function extractGroups(resultsSection) {
  const baseline = resultsSection?.baselineCharacteristicsModule;
  if (!baseline?.groups) return [];
  return baseline.groups.map((g) => ({
    id: g.id,
    title: g.title,
    description: g.description || '',
  }));
}

function extractOutcomes(resultsSection) {
  const outcomes = resultsSection?.outcomeMeasuresModule?.outcomeMeasures;
  if (!outcomes) return [];

  return outcomes.map((om) => {
    const measurements = [];
    if (om.groups && om.classes) {
      om.classes.forEach((cls) => {
        if (!cls.categories) return;
        cls.categories.forEach((cat) => {
          if (!cat.measurements) return;
          cat.measurements.forEach((m) => {
            measurements.push({
              groupId: m.groupId,
              value: parseFloat(m.value) || 0,
              lower: m.lowerLimit != null ? parseFloat(m.lowerLimit) : null,
              upper: m.upperLimit != null ? parseFloat(m.upperLimit) : null,
              classTitle: cls.title || '',
            });
          });
        });
      });
    }

    const analyses = [];
    if (om.analyses) {
      om.analyses.forEach((a) => {
        const est = a.groupIds?.length >= 2 ? {
          pValue: a.pValue != null ? parseFloat(a.pValue) : null,
          estimateType: a.paramType || a.statisticalMethod || '',
          estimateValue: a.estimateValue != null ? parseFloat(a.estimateValue) : null,
          ciLower: a.ciLowerLimit != null ? parseFloat(a.ciLowerLimit) : null,
          ciUpper: a.ciUpperLimit != null ? parseFloat(a.ciUpperLimit) : null,
          ciPercent: a.ciNumSides === '2-Sided' ? (a.ciPctValue || 95) : (a.ciPctValue || 95),
          groupIds: a.groupIds,
          description: a.nonInferiorityComment || a.paramDescription || '',
        } : null;
        if (est) analyses.push(est);
      });
    }

    return {
      title: om.title || '',
      type: om.type || '',
      description: om.description || '',
      timeFrame: om.timeFrame || '',
      unitOfMeasure: om.unitOfMeasure || '',
      paramType: om.paramType || '',
      dispersionType: om.dispersionType || '',
      measurements,
      analyses,
    };
  });
}

function extractParticipantFlow(resultsSection) {
  const flow = resultsSection?.participantFlowModule;
  if (!flow) return null;

  const groups = (flow.groups || []).map((g) => ({
    id: g.id,
    title: g.title,
    description: g.description || '',
  }));

  const periods = (flow.periods || []).map((p) => ({
    title: p.title || '',
    milestones: (p.milestones || []).map((m) => ({
      type: m.type || '',
      achievements: (m.achievements || []).map((a) => ({
        groupId: a.groupId,
        count: parseInt(a.numSubjects, 10) || 0,
      })),
    })),
    dropWithdraws: (p.dropWithdraws || []).map((d) => ({
      type: d.type || '',
      reasons: (d.reasons || []).map((r) => ({
        groupId: r.groupId,
        count: parseInt(r.numSubjects, 10) || 0,
      })),
    })),
  }));

  return { groups, periods };
}

function extractBaseline(resultsSection) {
  const baseline = resultsSection?.baselineCharacteristicsModule;
  if (!baseline?.measures) return [];

  return baseline.measures.map((m) => {
    const rows = [];
    if (m.classes) {
      m.classes.forEach((cls) => {
        if (!cls.categories) return;
        cls.categories.forEach((cat) => {
          const values = {};
          if (cat.measurements) {
            cat.measurements.forEach((meas) => {
              values[meas.groupId] = meas.value;
            });
          }
          rows.push({
            classTitle: cls.title || '',
            categoryTitle: cat.title || '',
            values,
          });
        });
      });
    }
    return {
      title: m.title || '',
      paramType: m.paramType || '',
      unitOfMeasure: m.unitOfMeasure || '',
      rows,
    };
  });
}

// eslint-disable-next-line import/prefer-default-export
export function transformTrial(apiResponse) {
  const study = apiResponse;
  const resultsSection = study?.resultsSection;
  const protocol = study?.protocolSection;

  if (!resultsSection) {
    return { error: 'No results section available for this trial' };
  }

  const identification = protocol?.identificationModule || {};
  const design = protocol?.designModule || {};
  const enrollment = design?.enrollmentInfo;

  return {
    nctId: identification.nctId || '',
    briefTitle: identification.briefTitle || '',
    officialTitle: identification.officialTitle || '',
    phase: (design.phases || []).join(', ') || '',
    enrollment: enrollment ? parseInt(enrollment.count, 10) || 0 : 0,
    enrollmentType: enrollment?.type || '',
    groups: extractGroups(resultsSection),
    outcomes: extractOutcomes(resultsSection),
    participantFlow: extractParticipantFlow(resultsSection),
    baseline: extractBaseline(resultsSection),
  };
}
