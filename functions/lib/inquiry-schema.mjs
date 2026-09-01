export const PRODUCT_IDS = [
  'psa-nitrogen-system',
  'integrated-mixing-cabinet',
  'mspv2-4000',
  'need-recommendation',
];

export const LOCALES = ['en', 'zh', 'es', 'ko', 'ja', 'pt', 'pl'];

const CUSTOMER_TYPES = ['end_user', 'factory', 'integrator', 'project_owner', 'other'];
const CHANNELS = ['email', 'phone', 'whatsapp'];
const MATERIALS = ['carbon_steel', 'stainless_steel', 'aluminum', 'mixed', 'other'];
const GAS_TYPES = ['oxygen', 'nitrogen', 'air', 'mixed', 'unknown'];
const INSTALLATION_PREFERENCES = ['cabinet', 'valve', 'unsure'];
const CONTROL_INTERFACES = ['analog', 'modbus', 'plc-custom', 'unsure'];
const RETAINED_MODULES = [
  'air-compressor',
  'dryer',
  'filters',
  'air-buffer-tank',
  'nitrogen-storage',
  'booster',
  'none',
];

const FORBIDDEN_KEYS = /^(attachment|attachments|file|files|blob|base64)$/i;
const CONTROL_CHARACTERS = /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const LIMITS = {
  short: 120,
  medium: 300,
  message: 5000,
};

function isPlainObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function containsForbiddenValue(value) {
  if (!isPlainObject(value)) return false;
  for (const [key, child] of Object.entries(value)) {
    if (FORBIDDEN_KEYS.test(key)) return true;
    if (isPlainObject(child) && containsForbiddenValue(child)) return true;
  }
  return false;
}

function normalizeString(value, { multiline = false } = {}) {
  if (typeof value !== 'string') return null;
  if (CONTROL_CHARACTERS.test(value)) return null;
  if (!multiline && /[\r\n]/.test(value)) return null;
  if (multiline) {
    return value
      .replace(/\r\n?/g, '\n')
      .split('\n')
      .map((line) => line.trim().replace(/[ \t]+/g, ' '))
      .join('\n')
      .trim();
  }
  return value.trim().replace(/\s+/g, ' ');
}

function readString(source, key, fields, path, options = {}) {
  const value = normalizeString(source?.[key], options);
  const max = options.max ?? LIMITS.short;
  if (value === null || (options.required && !value) || value.length > max) {
    fields[path] = 'invalid';
    return '';
  }
  if (options.allowed && value && !options.allowed.includes(value)) {
    fields[path] = 'invalid';
    return '';
  }
  if (options.email && value && !EMAIL_PATTERN.test(value)) {
    fields[path] = 'invalid';
    return '';
  }
  return value;
}

function readStringArray(source, key, fields, path, allowed) {
  const value = source?.[key];
  if (!Array.isArray(value) || value.length === 0 || value.length > allowed.length) {
    fields[path] = 'invalid';
    return [];
  }
  const normalized = [];
  for (const item of value) {
    const clean = normalizeString(item);
    if (!clean || !allowed.includes(clean) || normalized.includes(clean)) {
      fields[path] = 'invalid';
      return [];
    }
    normalized.push(clean);
  }
  return normalized;
}

function validateContact(source, fields) {
  if (!isPlainObject(source)) {
    fields.contact = 'invalid';
    source = {};
  }
  const contact = {
    name: readString(source, 'name', fields, 'contact.name', { required: true }),
    company: readString(source, 'company', fields, 'contact.company', { required: true, max: LIMITS.medium }),
    country: readString(source, 'country', fields, 'contact.country', { required: true }),
    email: readString(source, 'email', fields, 'contact.email', { required: true, email: true, max: LIMITS.medium }),
    phone: readString(source, 'phone', fields, 'contact.phone', { max: LIMITS.medium }),
    preferred_channel: readString(source, 'preferred_channel', fields, 'contact.preferred_channel', {
      required: true,
      allowed: CHANNELS,
    }),
    consent: source?.consent === true,
  };
  if (!contact.consent) fields['contact.consent'] = 'required';
  if (['phone', 'whatsapp'].includes(contact.preferred_channel) && !contact.phone) {
    fields['contact.phone'] = 'required';
  }
  return contact;
}

function validateCommon(source, fields) {
  if (!isPlainObject(source)) {
    fields.common = 'invalid';
    source = {};
  }
  return {
    customer_type: readString(source, 'customer_type', fields, 'common.customer_type', {
      required: true,
      allowed: CUSTOMER_TYPES,
    }),
  };
}

function validatePsa(source, fields) {
  if (!isPlainObject(source)) {
    fields.psa = 'required';
    source = {};
  }
  return {
    target_flow: readString(source, 'target_flow', fields, 'psa.target_flow', { required: true }),
    purity: readString(source, 'purity', fields, 'psa.purity', { required: true }),
    output_pressure: readString(source, 'output_pressure', fields, 'psa.output_pressure', { required: true }),
    laser_count: readString(source, 'laser_count', fields, 'psa.laser_count', { required: true }),
    laser_power: readString(source, 'laser_power', fields, 'psa.laser_power', { required: true }),
    operating_hours: readString(source, 'operating_hours', fields, 'psa.operating_hours', { required: true }),
    retained_modules: readStringArray(source, 'retained_modules', fields, 'psa.retained_modules', RETAINED_MODULES),
    installation_space: readString(source, 'installation_space', fields, 'psa.installation_space', {
      required: true,
      max: LIMITS.medium,
    }),
  };
}

function validateMixer(source, fields, requireControlInterface) {
  if (!isPlainObject(source)) {
    fields.mixer = 'required';
    source = {};
  }
  const result = {
    laser_brand: readString(source, 'laser_brand', fields, 'mixer.laser_brand', { required: true }),
    laser_power: readString(source, 'laser_power', fields, 'mixer.laser_power', { required: true }),
    material: readString(source, 'material', fields, 'mixer.material', { required: true, allowed: MATERIALS }),
    thickness: readString(source, 'thickness', fields, 'mixer.thickness', { required: true }),
    current_gas: readString(source, 'current_gas', fields, 'mixer.current_gas', { required: true, allowed: GAS_TYPES }),
    nitrogen_source: readString(source, 'nitrogen_source', fields, 'mixer.nitrogen_source', { required: true }),
    nitrogen_inlet_pressure: readString(source, 'nitrogen_inlet_pressure', fields, 'mixer.nitrogen_inlet_pressure', { required: true }),
    oxygen_source: readString(source, 'oxygen_source', fields, 'mixer.oxygen_source', { required: true }),
    oxygen_inlet_pressure: readString(source, 'oxygen_inlet_pressure', fields, 'mixer.oxygen_inlet_pressure', { required: true }),
    required_flow: readString(source, 'required_flow', fields, 'mixer.required_flow', { required: true }),
    installation_preference: readString(source, 'installation_preference', fields, 'mixer.installation_preference', {
      required: true,
      allowed: INSTALLATION_PREFERENCES,
    }),
  };
  if (requireControlInterface) {
    result.control_interface = readString(source, 'control_interface', fields, 'mixer.control_interface', {
      required: true,
      allowed: CONTROL_INTERFACES,
    });
  }
  return result;
}

export function validateInquiry(input) {
  const fields = {};
  if (!isPlainObject(input) || containsForbiddenValue(input)) {
    return { ok: false, fields: { payload: 'invalid' } };
  }

  const product = readString(input, 'product', fields, 'product', {
    required: true,
    allowed: PRODUCT_IDS,
  });
  const locale = readString(input, 'locale', fields, 'locale', {
    required: true,
    allowed: LOCALES,
  });
  const value = {
    product,
    locale,
    contact: validateContact(input.contact, fields),
    common: validateCommon(input.common, fields),
    psa: null,
    mixer: null,
    message: readString(input, 'message', fields, 'message', {
      required: true,
      multiline: true,
      max: LIMITS.message,
    }),
  };

  if (product === 'psa-nitrogen-system') {
    value.psa = validatePsa(input.psa, fields);
  } else if (product === 'integrated-mixing-cabinet') {
    value.mixer = validateMixer(input.mixer, fields, false);
  } else if (product === 'mspv2-4000') {
    value.mixer = validateMixer(input.mixer, fields, true);
  } else if (product === 'need-recommendation') {
    const hasPsa = isPlainObject(input.psa);
    const hasMixer = isPlainObject(input.mixer);
    if (!hasPsa && !hasMixer) fields.product = 'branch_required';
    if (hasPsa) value.psa = validatePsa(input.psa, fields);
    if (hasMixer) value.mixer = validateMixer(input.mixer, fields, Boolean(input.mixer?.control_interface));
  }

  if (Object.keys(fields).length) return { ok: false, fields };
  return { ok: true, value };
}

export function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}
