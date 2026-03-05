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

export function transformSearch(apiResponse) {
  const studies = (apiResponse?.studies || []).map((s) => {
    const protocol = s?.protocolSection;
    const id = protocol?.identificationModule || {};
    const design = protocol?.designModule || {};
    const conditions = protocol?.conditionsModule?.conditions || [];
    const sponsor = protocol?.sponsorCollaboratorsModule?.leadSponsor?.name || '';
    const enrollment = design?.enrollmentInfo;
    return {
      nctId: id.nctId || '',
      title: id.briefTitle || '',
      phase: (design.phases || []).join(', ') || '',
      status: protocol?.statusModule?.overallStatus || '',
      conditions,
      sponsor,
      enrollment: enrollment ? parseInt(enrollment.count, 10) || 0 : 0,
    };
  });
  return {
    totalCount: apiResponse?.totalCount || studies.length,
    studies,
  };
}

function extractAdverseEvents(resultsSection) {
  const ae = resultsSection?.adverseEventsModule;
  if (!ae) return null;

  const groups = (ae.eventGroups || []).map((g) => ({
    id: g.id,
    title: g.title,
    description: g.description || '',
    deathsNumAffected: g.deathsNumAffected ?? 0,
    deathsNumAtRisk: g.deathsNumAtRisk ?? 0,
    seriousNumAffected: g.seriousNumAffected ?? 0,
    seriousNumAtRisk: g.seriousNumAtRisk ?? 0,
    otherNumAffected: g.otherNumAffected ?? 0,
    otherNumAtRisk: g.otherNumAtRisk ?? 0,
  }));

  function mapEvents(events) {
    if (!events) return [];
    return events.map((e) => ({
      term: e.term || '',
      organSystem: e.organSystem || '',
      stats: (e.stats || []).map((s) => ({
        groupId: s.groupId,
        numAffected: s.numAffected ?? 0,
        numAtRisk: s.numAtRisk ?? 0,
      })),
    }));
  }

  return {
    frequencyThreshold: ae.frequencyThreshold || '',
    timeFrame: ae.timeFrame || '',
    description: ae.description || '',
    groups,
    seriousEvents: mapEvents(ae.seriousEvents),
    otherEvents: mapEvents(ae.otherEvents),
  };
}

function extractProtocol(protocolSection) {
  const p = protocolSection || {};
  const id = p.identificationModule || {};
  const status = p.statusModule || {};
  const desc = p.descriptionModule || {};
  const design = p.designModule || {};
  const eligibility = p.eligibilityModule || {};
  const arms = p.armsInterventionsModule || {};
  const outcomes = p.outcomesModule || {};
  const contacts = p.contactsLocationsModule || {};
  const sponsor = p.sponsorCollaboratorsModule || {};
  const refs = p.referencesModule || {};
  const ipd = p.ipdSharingStatementModule || {};
  const oversight = p.oversightModule || {};
  const conditions = p.conditionsModule || {};

  return {
    identification: {
      nctId: id.nctId || '',
      briefTitle: id.briefTitle || '',
      officialTitle: id.officialTitle || '',
      orgStudyId: id.orgStudyIdInfo?.id || '',
      organization: id.organization?.fullName || '',
    },
    status: {
      overallStatus: status.overallStatus || '',
      startDate: status.startDateStruct?.date || '',
      startDateType: status.startDateStruct?.type || '',
      primaryCompletionDate: status.primaryCompletionDateStruct?.date || '',
      primaryCompletionDateType: status.primaryCompletionDateStruct?.type || '',
      completionDate: status.completionDateStruct?.date || '',
      completionDateType: status.completionDateStruct?.type || '',
      studyFirstPostDate: status.studyFirstPostDateStruct?.date || '',
      lastUpdatePostDate: status.lastUpdatePostDateStruct?.date || '',
      statusVerifiedDate: status.statusVerifiedDate || '',
    },
    description: {
      briefSummary: desc.briefSummary || '',
      detailedDescription: desc.detailedDescription || '',
    },
    conditions: conditions.conditions || [],
    keywords: conditions.keywords || [],
    design: {
      studyType: design.studyType || '',
      phases: design.phases || [],
      allocation: design.designInfo?.allocation || '',
      interventionModel: design.designInfo?.interventionModel || '',
      primaryPurpose: design.designInfo?.primaryPurpose || '',
      masking: design.designInfo?.maskingInfo?.masking || '',
      maskingDescription: design.designInfo?.maskingInfo?.description || '',
      enrollmentCount: design.enrollmentInfo?.count ?? 0,
      enrollmentType: design.enrollmentInfo?.type || '',
    },
    arms: (arms.armGroups || []).map((a) => ({
      label: a.label || '',
      type: a.type || '',
      description: a.description || '',
      interventionNames: a.interventionNames || [],
    })),
    interventions: (arms.interventions || []).map((iv) => ({
      type: iv.type || '',
      name: iv.name || '',
      description: iv.description || '',
      armGroupLabels: iv.armGroupLabels || [],
    })),
    eligibility: {
      criteria: eligibility.eligibilityCriteria || '',
      healthyVolunteers: eligibility.healthyVolunteers ?? false,
      sex: eligibility.sex || '',
      minimumAge: eligibility.minimumAge || '',
      maximumAge: eligibility.maximumAge || '',
      stdAges: eligibility.stdAges || [],
    },
    plannedOutcomes: {
      primary: (outcomes.primaryOutcomes || []).map((o) => ({
        measure: o.measure || '',
        description: o.description || '',
        timeFrame: o.timeFrame || '',
      })),
      secondary: (outcomes.secondaryOutcomes || []).map((o) => ({
        measure: o.measure || '',
        description: o.description || '',
        timeFrame: o.timeFrame || '',
      })),
      other: (outcomes.otherOutcomes || []).map((o) => ({
        measure: o.measure || '',
        description: o.description || '',
        timeFrame: o.timeFrame || '',
      })),
    },
    contacts: {
      officials: (contacts.overallOfficials || []).map((o) => ({
        name: o.name || '',
        affiliation: o.affiliation || '',
        role: o.role || '',
      })),
      locations: (contacts.locations || []).map((l) => ({
        facility: l.facility || '',
        city: l.city || '',
        state: l.state || '',
        zip: l.zip || '',
        country: l.country || '',
        lat: l.geoPoint?.lat ?? null,
        lon: l.geoPoint?.lon ?? null,
      })),
    },
    sponsor: {
      leadSponsor: sponsor.leadSponsor?.name || '',
      leadSponsorClass: sponsor.leadSponsor?.class || '',
      responsiblePartyType: sponsor.responsibleParty?.type || '',
      collaborators: (sponsor.collaborators || []).map((c) => ({
        name: c.name || '',
        class: c.class || '',
      })),
    },
    references: (refs.references || []).map((r) => ({
      pmid: r.pmid || '',
      type: r.type || '',
      citation: r.citation || '',
    })),
    ipdSharing: ipd.ipdSharing || '',
    oversightHasDmc: oversight.oversightHasDmc ?? false,
  };
}

export function transformStudy(apiResponse) {
  const study = apiResponse;
  const protocol = extractProtocol(study?.protocolSection);
  const resultsSection = study?.resultsSection;

  const result = {
    protocol,
    hasResults: !!resultsSection,
  };

  if (resultsSection) {
    result.groups = extractGroups(resultsSection);
    result.outcomes = extractOutcomes(resultsSection);
    result.participantFlow = extractParticipantFlow(resultsSection);
    result.baseline = extractBaseline(resultsSection);
    result.adverseEvents = extractAdverseEvents(resultsSection);
  }

  return result;
}

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
