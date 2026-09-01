import { validateInquiry } from './inquiry-schema.mjs';

const MAX_BODY_BYTES = 32 * 1024;
const LOCAL_ORIGIN = /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/;

function json(body, status, extraHeaders = {}) {
  return Response.json(body, {
    status,
    headers: {
      'cache-control': 'no-store',
      'x-content-type-options': 'nosniff',
      ...extraHeaders,
    },
  });
}

function deliveryUnavailable() {
  return json({ ok: false, code: 'delivery_unavailable' }, 503);
}

function originAllowed(request, env) {
  const origin = request.headers.get('origin');
  if (!origin) return false;
  if (origin === new URL(request.url).origin) return true;
  return env?.ALLOW_LOCAL_ORIGIN === 'true' && LOCAL_ORIGIN.test(origin);
}

async function callMailer(binding, payload) {
  const signal = typeof AbortSignal.timeout === 'function'
    ? AbortSignal.timeout(4000)
    : undefined;
  const response = await binding.fetch(new Request('https://inquiry-mailer.internal/send', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload),
    signal,
  }));
  if (!response.ok) return false;
  try {
    const result = await response.json();
    return result?.ok === true;
  } catch {
    return false;
  }
}

export async function handleInquiryRequest(context) {
  const { request, env = {} } = context;
  if (request.method !== 'POST') {
    return json({ ok: false, code: 'method_not_allowed' }, 405, { allow: 'POST' });
  }

  const contentType = request.headers.get('content-type') || '';
  if (!contentType.toLowerCase().startsWith('application/json')) {
    return json({ ok: false, code: 'unsupported_media_type' }, 415);
  }

  const declaredLength = Number(request.headers.get('content-length'));
  if (!Number.isInteger(declaredLength) || declaredLength <= 0 || declaredLength > MAX_BODY_BYTES) {
    return json({ ok: false, code: 'try_again_later' }, 413);
  }

  if (!originAllowed(request, env)) {
    return json({ ok: false, code: 'try_again_later' }, 403);
  }

  let rawBody;
  try {
    rawBody = await request.text();
  } catch {
    return json({ ok: false, code: 'validation_error', fields: { payload: 'invalid' } }, 400);
  }
  if (new TextEncoder().encode(rawBody).byteLength > MAX_BODY_BYTES) {
    return json({ ok: false, code: 'try_again_later' }, 413);
  }

  let input;
  try {
    input = JSON.parse(rawBody);
  } catch {
    return json({ ok: false, code: 'validation_error', fields: { payload: 'invalid' } }, 400);
  }

  const reference = crypto.randomUUID();
  if (typeof input?.website === 'string' && input.website.trim()) {
    return json({ ok: true, reference }, 200);
  }

  const validation = validateInquiry(input);
  if (!validation.ok) {
    return json({ ok: false, code: 'validation_error', fields: validation.fields }, 400);
  }

  if (!env.INQUIRY_MAILER || typeof env.INQUIRY_MAILER.fetch !== 'function') {
    return deliveryUnavailable();
  }

  const internalPayload = {
    ...validation.value,
    reference,
    received_at: new Date().toISOString(),
  };

  try {
    if (!await callMailer(env.INQUIRY_MAILER, internalPayload)) return deliveryUnavailable();
  } catch {
    return deliveryUnavailable();
  }

  return json({ ok: true, reference }, 200);
}

