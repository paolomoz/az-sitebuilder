import { transformTrial } from './transform.js';

const ALLOWED_ORIGINS = [
  'http://localhost:3000',
  /^https:\/\/.*\.aem\.page$/,
  /^https:\/\/.*\.aem\.live$/,
];

function isAllowedOrigin(origin) {
  if (!origin) return false;
  return ALLOWED_ORIGINS.some((allowed) => {
    if (typeof allowed === 'string') return allowed === origin;
    return allowed.test(origin);
  });
}

function corsHeaders(origin) {
  const headers = {
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
  if (isAllowedOrigin(origin)) {
    headers['Access-Control-Allow-Origin'] = origin;
  }
  return headers;
}

function jsonResponse(data, status = 200, origin = '') {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    // Route: GET /api/trial/:nctId
    const match = url.pathname.match(/^\/api\/trial\/(NCT\d+)$/i);
    if (!match) {
      return jsonResponse({ error: 'Not found. Use /api/trial/NCTxxxxxxxx' }, 404, origin);
    }

    const nctId = match[1].toUpperCase();

    // Check cache first
    const cache = caches.default;
    const cacheKey = new Request(`https://trial-cache/${nctId}`, { method: 'GET' });
    const cached = await cache.match(cacheKey);
    if (cached) {
      // Re-add CORS headers for the current origin
      const body = await cached.text();
      return new Response(body, {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'X-Cache': 'HIT',
          ...corsHeaders(origin),
        },
      });
    }

    // Fetch from ClinicalTrials.gov API v2
    const ctgovBase = env.CTGOV_BASE || 'https://clinicaltrials.gov/api/v2';
    const apiUrl = `${ctgovBase}/studies/${nctId}?fields=protocolSection.identificationModule,protocolSection.designModule,resultsSection`;

    let apiResponse;
    try {
      apiResponse = await fetch(apiUrl, {
        headers: { Accept: 'application/json' },
      });
    } catch (err) {
      return jsonResponse({ error: `Failed to fetch from ClinicalTrials.gov: ${err.message}` }, 502, origin);
    }

    if (!apiResponse.ok) {
      const status = apiResponse.status === 404 ? 404 : 502;
      return jsonResponse(
        { error: `ClinicalTrials.gov returned ${apiResponse.status} for ${nctId}` },
        status,
        origin,
      );
    }

    let study;
    try {
      study = await apiResponse.json();
    } catch {
      return jsonResponse({ error: 'Invalid JSON from ClinicalTrials.gov' }, 502, origin);
    }

    const transformed = transformTrial(study);
    if (transformed.error) {
      return jsonResponse(transformed, 404, origin);
    }

    // Cache for 30 days (trial results are immutable)
    const responseBody = JSON.stringify(transformed);
    const cacheResponse = new Response(responseBody, {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=2592000',
      },
    });
    await cache.put(cacheKey, cacheResponse);

    return new Response(responseBody, {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'X-Cache': 'MISS',
        ...corsHeaders(origin),
      },
    });
  },
};
