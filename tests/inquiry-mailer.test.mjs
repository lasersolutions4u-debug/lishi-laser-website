import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

import { handleMailerRequest } from '../workers/inquiry-mailer/src/index.mjs';

function canonicalPayload() {
  return {
    product: 'integrated-mixing-cabinet',
    locale: 'en',
    contact: {
      name: 'Avery <Chen>',
      company: 'Example & Sons Ltd.',
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
    message: 'Please review <this> fictional application.',
    reference: '123e4567-e89b-42d3-a456-426614174000',
    received_at: '2026-09-01T08:30:00.000Z',
  };
}

function requestFor(payload = canonicalPayload(), options = {}) {
  return new Request(options.url ?? 'https://inquiry-mailer.internal/send', {
    method: options.method ?? 'POST',
    headers: { 'content-type': 'application/json' },
    body: (options.method ?? 'POST') === 'GET' ? undefined : JSON.stringify(payload),
  });
}

function emailEnv(sent) {
  return {
    EMAIL: {
      async send(message) {
        sent.push(message);
        return { messageId: 'fictional-message-id' };
      },
    },
  };
}

test('allows only POST to the private /send endpoint', async () => {
  assert.equal((await handleMailerRequest(requestFor({}, { method: 'GET' }), {})).status, 405);
  assert.equal((await handleMailerRequest(requestFor({}, { url: 'https://inquiry-mailer.internal/other' }), {})).status, 404);
});

test('requires an exact canonical payload and rejects unknown fields', async () => {
  const missingReference = canonicalPayload();
  delete missingReference.reference;
  assert.equal((await handleMailerRequest(requestFor(missingReference), emailEnv([]))).status, 400);

  const unknown = canonicalPayload();
  unknown.untrusted = 'do not accept';
  const response = await handleMailerRequest(requestFor(unknown), emailEnv([]));
  assert.equal(response.status, 400);
  assert.equal((await response.text()).includes('do not accept'), false);
});

test('builds a CRLF-safe subject from product, country and reference only', async () => {
  const sent = [];
  const response = await handleMailerRequest(requestFor(), emailEnv(sent));
  assert.equal(response.status, 200);
  assert.equal(sent.length, 1);
  assert.equal(
    sent[0].subject,
    '[Website inquiry] integrated-mixing-cabinet | Canada | 123e4567-e89b-42d3-a456-426614174000',
  );
  assert.equal(/[\r\n]/.test(sent[0].subject), false);
});

test('sends escaped HTML, plain text and validated Reply-To without using customer From', async () => {
  const sent = [];
  await handleMailerRequest(requestFor(), emailEnv(sent));
  const message = sent[0];

  assert.equal(message.to, 'sales@gasmixtech.com');
  assert.equal(message.from, 'sales@gasmixtech.com');
  assert.equal(message.replyTo, 'avery@example.com');
  assert.match(message.text, /Avery <Chen>/);
  assert.match(message.text, /Example & Sons Ltd\./);
  assert.match(message.html, /Avery &lt;Chen&gt;/);
  assert.match(message.html, /Example &amp; Sons Ltd\./);
  assert.match(message.html, /Please review &lt;this&gt; fictional application\./);
  assert.equal(message.html.includes('Avery <Chen>'), false);
});

test('returns a fixed response and no customer data when the email binding fails', async () => {
  const env = { EMAIL: { async send() { throw Object.assign(new Error('private details'), { code: 'E_DELIVERY_FAILED' }); } } };
  const response = await handleMailerRequest(requestFor(), env);
  const text = await response.text();
  assert.equal(response.status, 502);
  assert.deepEqual(JSON.parse(text), { ok: false, code: 'delivery_failed' });
  assert.equal(text.includes('avery@example.com'), false);
  assert.equal(text.includes('private details'), false);
});

test('worker configuration is private and restricts sender and destination', async () => {
  const config = JSON.parse(await readFile(new URL('../workers/inquiry-mailer/wrangler.jsonc', import.meta.url), 'utf8'));
  assert.equal(config.workers_dev, false);
  assert.equal('routes' in config, false);
  assert.deepEqual(config.send_email, [{
    name: 'EMAIL',
    destination_address: 'sales@gasmixtech.com',
    allowed_sender_addresses: ['sales@gasmixtech.com'],
  }]);
});
