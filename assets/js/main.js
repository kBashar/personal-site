/* ============================================================
   main.js — Nav toggle + dark mode
   ============================================================ */

(function () {
  'use strict';

  // ── Nav toggle (mobile) ─────────────────────────────────────
  const toggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      const isOpen = navLinks.classList.toggle('open');
      toggle.classList.toggle('open', isOpen);
      toggle.setAttribute('aria-expanded', String(isOpen));
    });

    // Close nav when a link is clicked
    navLinks.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        navLinks.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Close nav on outside click
    document.addEventListener('click', function (e) {
      if (!toggle.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        toggle.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Dark mode toggle ────────────────────────────────────────
  const themeBtn = document.getElementById('theme-toggle');
  const root = document.documentElement;

  var sunSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
  var moonSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

  // Load saved preference or default to system preference
  const saved = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial = saved || (prefersDark ? 'dark' : 'light');

  applyTheme(initial);

  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      const current = root.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('theme', next);
    });
  }

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (themeBtn) {
      themeBtn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
      themeBtn.innerHTML = theme === 'dark' ? moonSvg : sunSvg;
    }
  }

  // ── Active nav link highlight ───────────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(function (link) {
    const href = link.getAttribute('href');
    if (!href) return;
    // Match exact or sub-path (for blog/*)
    const normalized = href.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
    const currentNorm = currentPath.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
    if (currentNorm === normalized || (normalized !== '/' && currentNorm.startsWith(normalized))) {
      link.classList.add('active');
    }
  });

})();
