(function () {
  const form = document.querySelector('[data-inquiry-form]');
  if (!form) return;

  const productIds = new Set([
    'psa-nitrogen-system',
    'integrated-mixing-cabinet',
    'mspv2-4000',
    'need-recommendation'
  ]);
  const steps = Array.from(form.querySelectorAll('[data-step]'));
  const progress = document.getElementById('inquiryProgress');
  const progressText = progress.querySelector('[data-progress-text]');
  const progressBar = progress.querySelector('[data-progress-bar]');
  const errors = document.getElementById('inquiryErrors');
  const failure = document.getElementById('inquiryFailure');
  const success = document.getElementById('inquirySuccess');
  const reference = success.querySelector('[data-inquiry-reference]');
  const product = form.elements.product;
  const recommendation = form.elements.recommendation_branch;
  const recommendationGroup = form.querySelector('[data-recommendation-only]');
  const psaBranch = form.querySelector('[data-branch="psa"]');
  const mixerBranch = form.querySelector('[data-branch="mixer"]');
  const mspGroup = form.querySelector('[data-msp-only]');
  const submitButton = form.querySelector('button[type="submit"]');
  const submitText = submitButton.textContent;
  let currentStep = 1;
  let submitting = false;

  function setControls(container, enabled) {
    container.hidden = !enabled;
    container.querySelectorAll('input, select, textarea').forEach(function (control) {
      control.disabled = !enabled;
      if (control.hasAttribute('data-required')) control.required = enabled;
      if (!enabled) control.setCustomValidity('');
    });
  }

  function activeBranches() {
    if (product.value === 'psa-nitrogen-system') return { psa: true, mixer: false };
    if (product.value === 'integrated-mixing-cabinet' || product.value === 'mspv2-4000') {
      return { psa: false, mixer: true };
    }
    if (product.value === 'need-recommendation') {
      return {
        psa: recommendation.value === 'psa' || recommendation.value === 'both',
        mixer: recommendation.value === 'mixer' || recommendation.value === 'both'
      };
    }
    return { psa: false, mixer: false };
  }

  function updateBranches() {
    const needsBranchChoice = product.value === 'need-recommendation';
    recommendationGroup.hidden = !needsBranchChoice;
    recommendation.disabled = !needsBranchChoice;
    recommendation.required = needsBranchChoice;

    const active = activeBranches();
    setControls(psaBranch, active.psa);
    setControls(mixerBranch, active.mixer);

    const needsControl = product.value === 'mspv2-4000';
    mspGroup.hidden = !needsControl;
    const control = form.elements.control_interface;
    control.disabled = !needsControl;
    control.required = needsControl;
  }

  function showErrors(message, target) {
    errors.textContent = message;
    errors.hidden = false;
    errors.focus();
    if (target) target.focus();
  }

  function clearErrors() {
    errors.hidden = true;
    errors.textContent = '';
  }

  function validateStep(stepNumber) {
    clearErrors();
    const fieldset = steps[stepNumber - 1];
    const controls = Array.from(fieldset.querySelectorAll('input, select, textarea')).filter(function (control) {
      return !control.disabled && control.type !== 'hidden';
    });
    const firstInvalid = controls.find(function (control) { return !control.checkValidity(); });
    if (firstInvalid) {
      showErrors(form.dataset.requiredMessage, firstInvalid);
      return false;
    }

    if (stepNumber === 2 && !psaBranch.hidden) {
      const retained = Array.from(form.querySelectorAll('input[name="retained_modules"]:not(:disabled)'));
      if (!retained.some(function (control) { return control.checked; })) {
        showErrors(form.dataset.requiredMessage, retained[0]);
        return false;
      }
    }
    return true;
  }

  function setStep(stepNumber) {
    currentStep = Math.max(1, Math.min(3, stepNumber));
    steps.forEach(function (fieldset, index) {
      fieldset.hidden = index + 1 !== currentStep;
    });
    const template = progress.dataset.template || 'Step {current} of 3';
    progressText.textContent = template.replace('{current}', String(currentStep));
    progressBar.style.width = `${currentStep / 3 * 100}%`;
    clearErrors();
    if (currentStep === 3) updateReview();
    steps[currentStep - 1].querySelector('legend').focus();
  }

  function value(name) {
    return String(form.elements[name]?.value || '').trim();
  }

  function selectedText(name) {
    const control = form.elements[name];
    return control && control.selectedIndex >= 0 ? control.options[control.selectedIndex].text : '';
  }

  function updateReview() {
    const review = document.getElementById('inquiryReview');
    review.replaceChildren();
    [
      [form.querySelector('label[for="product"]').textContent.replace('*', '').trim(), selectedText('product')],
      [form.querySelector('label[for="company"]').textContent.replace('*', '').trim(), value('company')],
      [form.querySelector('label[for="country"]').textContent.replace('*', '').trim(), value('country')]
    ].forEach(function (entry) {
      if (!entry[1]) return;
      const term = document.createElement('dt');
      const description = document.createElement('dd');
      term.textContent = entry[0];
      description.textContent = entry[1];
      review.append(term, description);
    });
  }

  function buildPayload() {
    const active = activeBranches();
    const payload = {
      product: value('product'),
      locale: document.documentElement.lang.split('-')[0].toLowerCase(),
      contact: {
        name: value('name'),
        company: value('company'),
        country: value('country'),
        email: value('email'),
        phone: value('phone'),
        preferred_channel: value('preferred_channel'),
        consent: form.elements.consent.checked
      },
      common: { customer_type: value('customer_type') },
      psa: null,
      mixer: null,
      message: value('message'),
      website: value('website')
    };

    if (active.psa) {
      payload.psa = {
        target_flow: value('target_flow'),
        purity: value('purity'),
        output_pressure: value('output_pressure'),
        laser_count: value('laser_count'),
        laser_power: value('psa_laser_power'),
        operating_hours: value('operating_hours'),
        retained_modules: Array.from(form.querySelectorAll('input[name="retained_modules"]:checked')).map(function (control) { return control.value; }),
        installation_space: value('installation_space')
      };
    }

    if (active.mixer) {
      payload.mixer = {
        laser_brand: value('laser_brand'),
        laser_power: value('mixer_laser_power'),
        material: value('material'),
        thickness: value('thickness'),
        current_gas: value('current_gas'),
        nitrogen_source: value('nitrogen_source'),
        nitrogen_inlet_pressure: value('nitrogen_inlet_pressure'),
        oxygen_source: value('oxygen_source'),
        oxygen_inlet_pressure: value('oxygen_inlet_pressure'),
        required_flow: value('required_flow'),
        installation_preference: value('installation_preference')
      };
      if (product.value === 'mspv2-4000') payload.mixer.control_interface = value('control_interface');
    }
    return payload;
  }

  form.addEventListener('click', function (event) {
    const next = event.target.closest('[data-next]');
    const back = event.target.closest('[data-back]');
    if (next) {
      if (validateStep(currentStep)) setStep(currentStep + 1);
    } else if (back) {
      setStep(currentStep - 1);
    }
  });

  product.addEventListener('change', updateBranches);
  recommendation.addEventListener('change', updateBranches);

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (submitting || !validateStep(3)) return;
    submitting = true;
    submitButton.disabled = true;
    submitButton.textContent = form.dataset.sending;
    failure.hidden = true;
    clearErrors();

    try {
      const response = await fetch('/api/inquiry', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(buildPayload())
      });
      const result = await response.json();
      if (result.ok) {
        form.hidden = true;
        progress.hidden = true;
        reference.textContent = result.reference;
        success.hidden = false;
        success.focus();
        if (typeof window.trackLead === 'function') trackLead('Contact Form');
        return;
      }
      failure.hidden = false;
      failure.focus();
    } catch {
      failure.hidden = false;
      failure.focus();
    } finally {
      submitting = false;
      submitButton.disabled = false;
      submitButton.textContent = submitText;
    }
  });

  const requestedProduct = new URLSearchParams(window.location.search).get('product');
  if (productIds.has(requestedProduct)) product.value = requestedProduct;
  updateBranches();
  setStep(1);
})();
