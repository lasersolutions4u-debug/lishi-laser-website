// LISHI LASER - Website JavaScript

// Mobile Navigation Toggle
const mobileToggle = document.getElementById('mobileToggle');
const nav = document.getElementById('nav');

if (mobileToggle && nav) {
  mobileToggle.addEventListener('click', () => {
    nav.classList.toggle('open');
    mobileToggle.textContent = nav.classList.contains('open') ? '✕' : '☰';
  });

  // Close mobile nav when clicking a link
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      mobileToggle.textContent = '☰';
    });
  });
}

// Scroll Animations (Fade In)
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
  observer.observe(el);
});

// Active Navigation Link + Header Shrink
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav a[href^="#"]');
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
  let current = '';

  sections.forEach(section => {
    const sectionTop = section.offsetTop - 100;
    if (window.scrollY >= sectionTop) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${current}`) {
      link.classList.add('active');
    }
  });

  // Header shrink effect
  if (header) {
    header.classList.toggle('shrunk', window.scrollY > 60);
  }
});

// Smooth Scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;

    const target = document.querySelector(targetId);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Form Submission (Web3Forms)
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    const btn = this.querySelector('button[type="submit"]');
    btn.textContent = 'Sending...';
    btn.disabled = true;
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Trigger fade-in for hero section immediately
  document.querySelectorAll('.hero .fade-in').forEach(el => {
    el.classList.add('visible');
  });

  // Initialize ROI calculator if present
  if (document.getElementById('thicknessSlider')) {
    initRoiCalculator();
  }
});

// Animate presence stats on scroll into view
(function() {
  const statEls = document.querySelectorAll('.global-presence .stat-num[data-target]');
  if (!statEls.length) return;

  const animateStat = (el) => {
    const target = parseFloat(el.dataset.target);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    const duration = 1400;
    const start = performance.now();
    function tick(now) {
      const p = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - p, 3);
      const val = Math.round(target * ease);
      el.textContent = prefix + val + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  };

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateStat(entry.target);
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });

  statEls.forEach(el => io.observe(el));
})();

// Language Switcher
const langBtn = document.getElementById('langBtn');
const langDropdown = document.getElementById('langDropdown');

if (langBtn && langDropdown) {
  langBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    langDropdown.classList.toggle('show');
  });

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if (!langDropdown.contains(e.target)) {
      langDropdown.classList.remove('show');
    }
  });

  // Close when pressing Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      langDropdown.classList.remove('show');
    }
  });
}

// ROI Calculator
function initRoiCalculator() {
  // Cutting speed data (m/min) from official parameters (upper bound of Excel ranges)
  const cuttingData = {
    12: { 6: 13, 8: 10, 10: 6.5, 12: 4, 16: 3 },
    20: { 2: 22, 4: 20, 6: 18, 8: 16, 10: 12, 12: 10, 16: 6, 20: 3.2, 25: 2.75 },
    30: { 8: 16, 10: 15, 12: 12, 16: 8, 20: 5.5, 25: 3.2, 30: 3 },
    60: { 25: 7.5, 30: 5.5, 35: 4.4, 40: 3.4 }
  };

  // O2 cutting speeds (m/min) for comparison
  const o2Speed = {
    12: { 6: 2.5, 8: 2.5, 10: 2, 12: 1.8, 16: 1.6 },
    20: { 2: 8, 4: 6, 6: 3, 8: 2.4, 10: 2.1, 12: 1.9, 16: 1.55, 20: 1.3, 25: 1 },
    30: { 8: 3, 10: 2.5, 12: 2, 16: 1.5, 20: 1.2, 25: 0.9, 30: 0.7 },
    60: { 25: 1.5, 30: 1, 35: 0.7, 40: 0.5 }
  };

  const maxThickness = { 12: 16, 20: 25, 30: 30, 60: 40 };
  const minThickness = { 12: 6, 20: 2, 30: 8, 60: 25 };

  let currentPower = 12;

  const thicknessSlider = document.getElementById('thicknessSlider');
  const thicknessValue = document.getElementById('thicknessValue');
  const hoursSlider = document.getElementById('hoursSlider');
  const hoursValue = document.getElementById('hoursValue');
  const utilizationSlider = document.getElementById('utilizationSlider');
  const utilizationValue = document.getElementById('utilizationValue');
  const powerWarning = document.getElementById('powerWarning');
  const currentSpeedEl = document.getElementById('currentSpeed');
  const lishiSpeedEl = document.getElementById('lishiSpeed');
  const annualProfitEl = document.getElementById('annualProfit');
  const gasSavingsEl = document.getElementById('gasSavings');
  const currentBarEl = document.getElementById('currentBar');
  const lishiBarEl = document.getElementById('lishiBar');
  const profitPerMeterInput = document.getElementById('profitPerMeter');
  const monthlyN2CostInput = document.getElementById('monthlyN2Cost');

  document.querySelectorAll('.power-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.power-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentPower = parseInt(btn.dataset.power);
      updateSliderRange();
      calculate();
    });
  });

  function updateSliderRange() {
    const min = minThickness[currentPower];
    const max = maxThickness[currentPower];
    thicknessSlider.min = min;
    thicknessSlider.max = max;
    if (thicknessSlider.value < min) thicknessSlider.value = min;
    if (thicknessSlider.value > max) thicknessSlider.value = max;
    thicknessValue.textContent = thicknessSlider.value + ' mm';
    updateSliderFill(thicknessSlider);
  }

  function updateSliderFill(slider) {
    const pct = ((slider.value - slider.min) / (slider.max - slider.min)) * 100;
    slider.style.setProperty('--slider-pct', pct + '%');
  }

  thicknessSlider.addEventListener('input', () => {
    const thickness = parseInt(thicknessSlider.value);
    thicknessValue.textContent = thickness + ' mm';
    updateSliderFill(thicknessSlider);
    checkPowerWarning(thickness);
    calculate();
  });

  hoursSlider.addEventListener('input', () => {
    hoursValue.textContent = hoursSlider.value + ' hrs';
    updateSliderFill(hoursSlider);
    calculate();
  });

  utilizationSlider.addEventListener('input', () => {
    utilizationValue.textContent = utilizationSlider.value + ' %';
    updateSliderFill(utilizationSlider);
    calculate();
  });

  profitPerMeterInput.addEventListener('input', calculate);
  monthlyN2CostInput.addEventListener('input', calculate);

  function checkPowerWarning(thickness) {
    const max = maxThickness[currentPower];
    if (thickness > max) {
      powerWarning.textContent = 'For thickness over ' + max + 'mm with ' + currentPower + 'kW, we recommend 20kW+ for optimal mixed gas performance.';
      powerWarning.classList.add('show');
    } else {
      powerWarning.classList.remove('show');
    }
  }

  function getSpeed(speedData, power, thickness) {
    const powerData = speedData[power];
    if (!powerData) return 0;
    const thicknesses = Object.keys(powerData).map(Number).sort((a, b) => a - b);
    let closest = thicknesses[0];
    for (let t of thicknesses) {
      if (t <= thickness) closest = t;
      else break;
    }
    return powerData[closest] || 0;
  }

  function animateNumber(element, targetValue, prefix = '$', duration = 500) {
    const start = parseFloat(element.textContent.replace(/[^0-9.-]/g, '')) || 0;
    const startTime = performance.now();
    const endValue = parseFloat(targetValue);

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = start + (endValue - start) * easeOut;
      element.textContent = prefix + Math.round(current).toLocaleString();
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    requestAnimationFrame(update);
  }

  function calculate() {
    const thickness = parseInt(thicknessSlider.value);
    const hours = parseInt(hoursSlider.value);
    const utilization = (parseInt(utilizationSlider.value) || 60) / 100;
    const profitPerMeter = parseFloat(profitPerMeterInput.value) || 1;
    const monthlyN2Cost = parseFloat(monthlyN2CostInput.value) || 0;

    const currentSpeed = getSpeed(o2Speed, currentPower, thickness);
    const lishiSpeed = getSpeed(cuttingData, currentPower, thickness);

    currentSpeedEl.textContent = currentSpeed > 0 ? currentSpeed.toFixed(1) : '--';
    lishiSpeedEl.textContent = lishiSpeed > 0 ? lishiSpeed.toFixed(1) : '--';

    // Update speed bars
    if (currentBarEl && lishiBarEl) {
      const maxSpeed = Math.max(currentSpeed, lishiSpeed, 1);
      currentBarEl.style.width = (currentSpeed / maxSpeed * 100) + '%';
      lishiBarEl.style.width = (lishiSpeed / maxSpeed * 100) + '%';
    }

    if (lishiSpeed > 0 && currentSpeed > 0) {
      const workDays = 264;
      const speedDiff = lishiSpeed - currentSpeed;
      const annualBeamOnMinutes = hours * 60 * workDays * utilization;
      const annualMeters = speedDiff * annualBeamOnMinutes;
      const annualProfitIncrease = annualMeters * profitPerMeter;
      const annualGasSavings = monthlyN2Cost * 12 * 0.33;

      const oldAnnual = parseFloat(annualProfitEl.textContent.replace(/[^0-9.-]/g, '')) || 0;
      if (Math.abs(annualProfitIncrease - oldAnnual) > 100) {
        animateNumber(annualProfitEl, annualProfitIncrease, '$');
        animateNumber(gasSavingsEl, annualGasSavings, '$');
        annualProfitEl.classList.add('profit-animate');
        setTimeout(() => annualProfitEl.classList.remove('profit-animate'), 300);
      }
    } else {
      annualProfitEl.textContent = '$0';
      gasSavingsEl.textContent = '$0';
    }
  }

  // Initialize
  updateSliderRange();
  updateSliderFill(hoursSlider);
  updateSliderFill(utilizationSlider);
  calculate();
}

// Lead capture form submission (global)
function submitLead() {
  const email = document.getElementById('leadEmail').value.trim();
  const phone = document.getElementById('leadPhone').value.trim();
  const msgEl = document.getElementById('roiLeadMsg');

  function showMsg(type, html) {
    if (!msgEl) return;
    msgEl.className = 'roi-lead-msg show ' + type;
    msgEl.innerHTML = html;
    if (type === 'success') {
      setTimeout(function(){ msgEl.className = 'roi-lead-msg'; }, 8000);
    }
  }

  if (!email) {
    showMsg('error', 'Please enter your email address.');
    return;
  }

  var activePower = (document.querySelector('.power-btn.active') || {}).dataset?.power || 'N/A';
  var thickness = (document.getElementById('thicknessSlider') || {}).value || 'N/A';
  var annualProfit = (document.getElementById('annualProfit') || {}).textContent || 'N/A';
  var gasSavings = (document.getElementById('gasSavings') || {}).textContent || 'N/A';

  var formData = new FormData();
  formData.append('access_key', '2352c2d3-9578-4f1e-aa56-611e2ad355d1');
  formData.append('subject', 'ROI Calculator Lead - gasmixtech.com');
  formData.append('email', email);
  formData.append('phone', phone);
  formData.append('message',
    'ROI Calculator inquiry from ' + email +
    (phone ? ' | WhatsApp: ' + phone : '') +
    ' | Machine: ' + activePower + 'kW' +
    ' | Thickness: ' + thickness + 'mm' +
    ' | Est. Annual Profit: ' + annualProfit +
    ' | Est. Gas Savings: ' + gasSavings
  );

  var btn = document.querySelector('.roi-submit');
  var origText = btn.textContent;
  btn.textContent = 'Sending...';
  btn.disabled = true;

  fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    body: formData
  })
  .then(function(response) { return response.json(); })
  .then(function(data) {
    btn.textContent = origText;
    btn.disabled = false;
    if (data.success) {
      document.getElementById('leadEmail').value = '';
      document.getElementById('leadPhone').value = '';
      showMsg('success', '&#10003; Thank you! We\'ll send your custom parameter table within 24 hours.');
    } else {
      showMsg('error', 'Submission failed. Please email us directly at <a href=\"mailto:sales@gasmixtech.com\">sales@gasmixtech.com</a> or <a href=\"https://wa.me/525572080065\">WhatsApp +86 186 1558 4520</a>.');
    }
  })
  .catch(function() {
    btn.textContent = origText;
    btn.disabled = false;
    showMsg('error', 'Network error. Please email us at <a href=\"mailto:sales@gasmixtech.com\">sales@gasmixtech.com</a> or <a href=\"https://wa.me/525572080065\">WhatsApp +86 186 1558 4520</a>.');
  });
}
