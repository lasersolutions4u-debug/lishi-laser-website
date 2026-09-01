import { escapeHtml, validateInquiry } from '../../../functions/lib/inquiry-schema.mjs';

const SALES_ADDRESS = 'sales@gasmixtech.com';
const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const EXPECTED_KEYS = {
  top: ['product', 'locale', 'contact', 'common', 'psa', 'mixer', 'message', 'reference', 'received_at'],
  contact: ['name', 'company', 'country', 'email', 'phone', 'preferred_channel', 'consent'],
  common: ['customer_type'],
  psa: ['target_flow', 'purity', 'output_pressure', 'laser_count', 'laser_power', 'operating_hours', 'retained_modules', 'installation_space'],
  mixer: ['laser_brand', 'laser_power', 'material', 'thickness', 'current_gas', 'nitrogen_source', 'nitrogen_inlet_pressure', 'oxygen_source', 'oxygen_inlet_pressure', 'required_flow', 'installation_preference'],
};

function json(body, status) {
  return Response.json(body, {
    status,
    headers: { 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' },
  });
}

function hasExactKeys(value, expected) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const actual = Object.keys(value).sort();
  return actual.length === expected.length && actual.every((key, index) => key === [...expected].sort()[index]);
}

function canonicalPayload(input) {
  if (!hasExactKeys(input, EXPECTED_KEYS.top)) return null;
  if (!hasExactKeys(input.contact, EXPECTED_KEYS.contact)) return null;
  if (!hasExactKeys(input.common, EXPECTED_KEYS.common)) return null;
  if (input.psa !== null && !hasExactKeys(input.psa, EXPECTED_KEYS.psa)) return null;
  if (input.mixer !== null) {
    const mixerKeys = input.product === 'mspv2-4000'
      ? [...EXPECTED_KEYS.mixer, 'control_interface']
      : EXPECTED_KEYS.mixer;
    if (!hasExactKeys(input.mixer, mixerKeys)) return null;
  }
  if (!UUID_V4.test(input.reference)) return null;
  if (typeof input.received_at !== 'string' || Number.isNaN(Date.parse(input.received_at))) return null;

  const validation = validateInquiry({
    product: input.product,
    locale: input.locale,
    contact: input.contact,
    common: input.common,
    psa: input.psa,
    mixer: input.mixer,
    message: input.message,
    website: '',
  });
  if (!validation.ok) return null;
  return { ...validation.value, reference: input.reference, received_at: input.received_at };
}

function label(key) {
  return key.replaceAll('_', ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function rows(payload) {
  const entries = [
    ['Reference', payload.reference],
    ['Received At', payload.received_at],
    ['Product', payload.product],
    ['Locale', payload.locale],
    ...Object.entries(payload.contact).filter(([key]) => key !== 'consent').map(([key, value]) => [label(key), value]),
    ...Object.entries(payload.common).map(([key, value]) => [label(key), value]),
  ];
  if (payload.psa) entries.push(...Object.entries(payload.psa).map(([key, value]) => [label(key), value]));
  if (payload.mixer) entries.push(...Object.entries(payload.mixer).map(([key, value]) => [label(key), value]));
  entries.push(['Message', payload.message]);
  return entries.map(([key, value]) => [key, Array.isArray(value) ? value.join(', ') : String(value)]);
}

function buildEmail(payload) {
  const contentRows = rows(payload);
  const safeSubjectPart = (value) => String(value).replace(/[\r\n]/g, ' ').trim();
  return {
    to: SALES_ADDRESS,
    from: SALES_ADDRESS,
    replyTo: payload.contact.email,
    subject: `[Website inquiry] ${safeSubjectPart(payload.product)} | ${safeSubjectPart(payload.contact.country)} | ${safeSubjectPart(payload.reference)}`,
    text: contentRows.map(([key, value]) => `${key}: ${value}`).join('\n'),
    html: `<!doctype html><html><body><h1>Website inquiry</h1><table>${contentRows.map(([key, value]) => `<tr><th align="left" valign="top">${escapeHtml(key)}</th><td>${escapeHtml(value).replaceAll('\n', '<br>')}</td></tr>`).join('')}</table></body></html>`,
  };
}

export async function handleMailerRequest(request, env = {}) {
  const url = new URL(request.url);
  if (url.pathname !== '/send') return json({ ok: false, code: 'not_found' }, 404);
  if (request.method !== 'POST') return json({ ok: false, code: 'method_not_allowed' }, 405);
  if (!(request.headers.get('content-type') || '').toLowerCase().startsWith('application/json')) {
    return json({ ok: false, code: 'invalid_payload' }, 400);
  }

  let input;
  try {
    input = await request.json();
  } catch {
    return json({ ok: false, code: 'invalid_payload' }, 400);
  }
  const payload = canonicalPayload(input);
  if (!payload) return json({ ok: false, code: 'invalid_payload' }, 400);
  if (!env.EMAIL || typeof env.EMAIL.send !== 'function') {
    return json({ ok: false, code: 'delivery_failed' }, 503);
  }

  try {
    await env.EMAIL.send(buildEmail(payload));
  } catch {
    return json({ ok: false, code: 'delivery_failed' }, 502);
  }
  return json({ ok: true }, 200);
}

export default {
  fetch: handleMailerRequest,
};

