import test from 'node:test';
import assert from 'node:assert/strict';

import {
  PRODUCT_IDS,
  LOCALES,
  escapeHtml,
  validateInquiry,
} from '../functions/lib/inquiry-schema.mjs';

const contact = {
  name: 'Avery Chen',
  company: 'Example Metalworks Ltd.',
  country: 'Canada',
  email: 'avery@example.com',
  phone: '+1 555 010 2030',
  preferred_channel: 'email',
  consent: true,
};

const common = {
  customer_type: 'end_user',
};

const psa = {
  target_flow: '45 Nm3/h',
  purity: '99.99%',
  output_pressure: '30 bar',
  laser_count: '1',
  laser_power: '6 kW',
  operating_hours: '10 hours/day',
  retained_modules: ['air-compressor', 'dryer'],
  installation_space: '12 m x 3 m',
};

const mixer = {
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
};

function validPayload(product = 'integrated-mixing-cabinet', locale = 'en') {
  const payload = {
    product,
    locale,
    contact: { ...contact },
    common: { ...common },
    psa: null,
    mixer: null,
    message: 'Please review this fictional cutting-gas application.',
    website: '',
  };

  if (product === 'psa-nitrogen-system') payload.psa = { ...psa };
  if (product === 'integrated-mixing-cabinet') payload.mixer = { ...mixer };
  if (product === 'mspv2-4000') {
    payload.mixer = { ...mixer, control_interface: 'modbus' };
  }
  if (product === 'need-recommendation') payload.mixer = { ...mixer };
  return payload;
}

test('accepts exactly the four stable product IDs', () => {
  assert.deepEqual(PRODUCT_IDS, [
    'psa-nitrogen-system',
    'integrated-mixing-cabinet',
    'mspv2-4000',
    'need-recommendation',
  ]);
  for (const product of PRODUCT_IDS) {
    assert.equal(validateInquiry(validPayload(product)).ok, true, product);
  }
  assert.equal(validateInquiry(validPayload('unknown-product')).ok, false);
});

test('accepts exactly the seven active locales', () => {
  assert.deepEqual(LOCALES, ['en', 'zh', 'es', 'ko', 'ja', 'pt', 'pl']);
  for (const locale of LOCALES) {
    assert.equal(validateInquiry(validPayload('integrated-mixing-cabinet', locale)).ok, true, locale);
  }
  assert.equal(validateInquiry(validPayload('integrated-mixing-cabinet', 'fr')).ok, false);
});

test('requires contact, customer type, preferred channel and consent', () => {
  for (const field of ['name', 'company', 'country', 'email', 'preferred_channel']) {
    const payload = validPayload();
    payload.contact[field] = '';
    const result = validateInquiry(payload);
    assert.equal(result.ok, false, field);
    assert.ok(result.fields[`contact.${field}`]);
  }

  const noCustomerType = validPayload();
  noCustomerType.common.customer_type = '';
  assert.ok(validateInquiry(noCustomerType).fields['common.customer_type']);

  const noConsent = validPayload();
  noConsent.contact.consent = false;
  assert.ok(validateInquiry(noConsent).fields['contact.consent']);
});

test('requires a complete PSA branch for the PSA product', () => {
  for (const field of Object.keys(psa)) {
    const payload = validPayload('psa-nitrogen-system');
    payload.psa[field] = Array.isArray(payload.psa[field]) ? [] : '';
    const result = validateInquiry(payload);
    assert.equal(result.ok, false, field);
    assert.ok(result.fields[`psa.${field}`]);
  }
});

test('requires a complete mixer branch and MSP control interface', () => {
  for (const field of Object.keys(mixer)) {
    const payload = validPayload('integrated-mixing-cabinet');
    payload.mixer[field] = '';
    const result = validateInquiry(payload);
    assert.equal(result.ok, false, field);
    assert.ok(result.fields[`mixer.${field}`]);
  }

  const msp = validPayload('mspv2-4000');
  msp.mixer.control_interface = '';
  assert.ok(validateInquiry(msp).fields['mixer.control_interface']);
});

test('recommendation requires at least one complete branch', () => {
  const empty = validPayload('need-recommendation');
  empty.mixer = null;
  assert.ok(validateInquiry(empty).fields.product);

  const both = validPayload('need-recommendation');
  both.psa = { ...psa };
  assert.equal(validateInquiry(both).ok, true);
});

test('normalizes whitespace, drops unknown keys and keeps international phone formatting', () => {
  const payload = validPayload();
  payload.contact.name = '  Avery   Chen  ';
  payload.contact.phone = ' +52 (55) 7208-0065 ext. 9 ';
  payload.ignored = 'must not be forwarded';
  payload.contact.ignored = 'must not be forwarded';

  const result = validateInquiry(payload);
  assert.equal(result.ok, true);
  assert.equal(result.value.contact.name, 'Avery Chen');
  assert.equal(result.value.contact.phone, '+52 (55) 7208-0065 ext. 9');
  assert.equal('ignored' in result.value, false);
  assert.equal('ignored' in result.value.contact, false);
});

test('rejects excessive strings, control characters and CRLF subject values', () => {
  const longMessage = validPayload();
  longMessage.message = 'x'.repeat(5001);
  assert.ok(validateInquiry(longMessage).fields.message);

  const control = validPayload();
  control.contact.company = 'Example\u0000Company';
  assert.ok(validateInquiry(control).fields['contact.company']);

  const crlf = validPayload();
  crlf.contact.country = 'Canada\r\nBcc: attacker@example.invalid';
  assert.ok(validateInquiry(crlf).fields['contact.country']);
});

test('rejects attachment-like keys, base64 payloads and unexpected nested values', () => {
  for (const [key, value] of [
    ['attachment', 'invoice.pdf'],
    ['file', 'data:application/pdf;base64,AAAA'],
    ['blob', 'AAAA'],
    ['base64', 'AAAA'],
  ]) {
    const payload = validPayload();
    payload[key] = value;
    assert.equal(validateInquiry(payload).ok, false, key);
  }

  const nested = validPayload();
  nested.contact.company = { value: 'Example Metalworks Ltd.' };
  assert.equal(validateInquiry(nested).ok, false);
});

test('escapes every HTML-significant character used in email output', () => {
  assert.equal(
    escapeHtml(`<script>alert('x') & \"y\"</script>`),
    '&lt;script&gt;alert(&#39;x&#39;) &amp; &quot;y&quot;&lt;/script&gt;',
  );
});
