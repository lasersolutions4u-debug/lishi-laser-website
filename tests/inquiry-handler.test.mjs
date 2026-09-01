import test from 'node:test';
import assert from 'node:assert/strict';

import { handleInquiryRequest } from '../functions/lib/inquiry-handler.mjs';

function validPayload() {
  return {
    product: 'integrated-mixing-cabinet',
    locale: 'en',
    contact: {
      name: 'Avery Chen',
      company: 'Example Metalworks Ltd.',
      country: 'Canada',
      email: 'avery@example.com',
      phone: '+1 555 010 2030',
      preferred_channel: 'email',
      consent: true,
    },
    common: { customer_type: 'end_user' },
    psa: null,
    mixer: {
      laser_brand: 'Example Laser',
      laser_power: '12 kW',
      material: 'carbon_steel',
      thickness: '6-20 mm',
      current_gas: 'nitrogen',
      nitrogen_source: 'psa',
      nitrogen_inlet_pressure: '30 bar',
      oxygen_source: 'cylinder',
      oxygen_inlet_pressure: '12 bar',
      required_flow: '35 Nm3/h',
      installation_preference: 'cabinet',
    },
    message: 'Please review this fictional application.',
    website: '',
  };
}

function requestFor(payload = validPayload(), overrides = {}) {
  const body = typeof payload === 'string' ? payload : JSON.stringify(payload);
  const headers = {
    'content-type': 'application/json',
    'content-length': String(Buffer.byteLength(body)),
    origin: 'https://gasmixtech.com',
    ...overrides.headers,
  };
  return new Request(overrides.url ?? 'https://gasmixtech.com/api/inquiry', {
    method: overrides.method ?? 'POST',
    headers,
    body: (overrides.method ?? 'POST') === 'GET' ? undefined : body,
  });
}

function successfulEnv(calls) {
  return {
    INQUIRY_MAILER: {
      async fetch(request) {
        calls.push(await request.json());
        return Response.json({ ok: true });
      },
    },
  };
}

test('allows only POST and advertises the allowed method', async () => {
  const response = await handleInquiryRequest({ request: requestFor('', { method: 'GET' }), env: {} });
  assert.equal(response.status, 405);
  assert.equal(response.headers.get('allow'), 'POST');
});

test('requires application/json and a bounded declared body length', async () => {
  const wrongType = requestFor(validPayload(), { headers: { 'content-type': 'text/plain' } });
  assert.equal((await handleInquiryRequest({ request: wrongType, env: {} })).status, 415);

  const missingLength = requestFor(validPayload(), { headers: { 'content-length': '' } });
  assert.equal((await handleInquiryRequest({ request: missingLength, env: {} })).status, 413);

  const tooLarge = requestFor('{}', { headers: { 'content-length': String(32 * 1024 + 1) } });
  assert.equal((await handleInquiryRequest({ request: tooLarge, env: {} })).status, 413);
});

test('rejects a parsed body above 32 KiB even if the header lies', async () => {
  const payload = JSON.stringify({ message: 'x'.repeat(33 * 1024) });
  const response = await handleInquiryRequest({
    request: requestFor(payload, { headers: { 'content-length': '100' } }),
    env: {},
  });
  assert.equal(response.status, 413);
});

test('requires same-origin requests and gates localhost override explicitly', async () => {
  const foreign = requestFor(validPayload(), { headers: { origin: 'https://example.invalid' } });
  assert.equal((await handleInquiryRequest({ request: foreign, env: {} })).status, 403);

  const local = requestFor(validPayload(), { headers: { origin: 'http://localhost:8123' } });
  assert.equal((await handleInquiryRequest({ request: local, env: {} })).status, 403);

  const calls = [];
  const response = await handleInquiryRequest({
    request: local,
    env: { ...successfulEnv(calls), ALLOW_LOCAL_ORIGIN: 'true' },
  });
  assert.equal(response.status, 200);
  assert.equal(calls.length, 1);
});

test('returns field-only validation errors without echoing customer values', async () => {
  const payload = validPayload();
  payload.contact.email = 'private-invalid-value';
  const response = await handleInquiryRequest({ request: requestFor(payload), env: successfulEnv([]) });
  const body = await response.json();
  assert.equal(response.status, 400);
  assert.equal(body.ok, false);
  assert.equal(body.code, 'validation_error');
  assert.ok(body.fields['contact.email']);
  assert.equal(JSON.stringify(body).includes('private-invalid-value'), false);
});

test('accepts honeypot submissions without delivering or revealing the trap', async () => {
  const payload = validPayload();
  payload.website = 'https://robot.example.invalid';
  const calls = [];
  const response = await handleInquiryRequest({ request: requestFor(payload), env: successfulEnv(calls) });
  const body = await response.json();
  assert.equal(response.status, 200);
  assert.equal(body.ok, true);
  assert.match(body.reference, /^[0-9a-f-]{36}$/);
  assert.equal(calls.length, 0);
  assert.equal(JSON.stringify(body).includes('website'), false);
});

test('requires the private Service Binding', async () => {
  const response = await handleInquiryRequest({ request: requestFor(), env: {} });
  assert.deepEqual(await response.json(), { ok: false, code: 'delivery_unavailable' });
  assert.equal(response.status, 503);
});

test('forwards only canonical data with a random reference and server timestamp', async () => {
  const payload = validPayload();
  payload.untrusted = 'drop me';
  payload.contact.untrusted = 'drop me';
  const calls = [];
  const response = await handleInquiryRequest({ request: requestFor(payload), env: successfulEnv(calls) });
  const body = await response.json();

  assert.equal(response.status, 200);
  assert.equal(body.ok, true);
  assert.match(body.reference, /^[0-9a-f-]{36}$/);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].reference, body.reference);
  assert.match(calls[0].received_at, /^\d{4}-\d{2}-\d{2}T/);
  assert.equal('untrusted' in calls[0], false);
  assert.equal('untrusted' in calls[0].contact, false);
});

test('maps private Worker errors to a fixed delivery response without CORS wildcard', async () => {
  const env = {
    INQUIRY_MAILER: { async fetch() { return new Response('private provider details', { status: 502 }); } },
  };
  const response = await handleInquiryRequest({ request: requestFor(), env });
  assert.equal(response.status, 503);
  assert.deepEqual(await response.json(), { ok: false, code: 'delivery_unavailable' });
  assert.equal(response.headers.get('access-control-allow-origin'), null);
});
