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

// Active Navigation Link
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav a[href^="#"]');

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

// Form Submission (for Formspree)
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  contactForm.addEventListener('submit', function(e) {
    // Let Formspree handle it naturally
    // Just add visual feedback
    const btn = this.querySelector('button[type="submit"]');
    btn.textContent = 'Sending...';
    btn.disabled = true;
  });
}

// Video play functionality placeholder
function playVideo(element) {
  const videoId = element.dataset.video;
  // Video modal could be implemented here
  // For now, show an alert or redirect to YouTube if video URL is known
  console.log('Play video:', videoId);
}

// Counter animation for hero stats
function animateCounters() {
  const counters = document.querySelectorAll('.hero-stat-value');
  counters.forEach(counter => {
    const text = counter.textContent;
    if (text.includes('×') || text.includes('%') || text.includes('−')) {
      // Keep as-is for special characters
      return;
    }
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Trigger fade-in for hero section immediately
  document.querySelectorAll('.hero .fade-in').forEach(el => {
    el.classList.add('visible');
  });
});
