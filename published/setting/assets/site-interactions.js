/* ───────────────────────────────────────────────────────────────
   site-interactions.js: shared click handlers for page widgets
   Loaded by any page that uses the three-tier knowledge UI or
   the era-card accordion. Safe to include even when a page uses
   none of these: each function is invoked from inline onclick=,
   so unused handlers cost nothing.

   Exposes (on window):
     - toggleSecret(e, btn)       red GM Secret (Style A pages)
     - toggleEra(el)              era-card open/close (history page)
     - toggleEraLegend(e, btn)    amber Popular Belief
     - toggleEraSecret(e, btn)    red GM Secret (Style B pages)

   The legend and secret toggles share one mechanism: store the
   button's original label on first click, swap to "Hide …" while
   open, restore on close. The original-label snapshot means the
   page's inline HTML: including any per-page wording variants
   like "◈ Hide" vs "◈ Hide Popular Belief": is preserved without
   the JS needing to know about it.
   ─────────────────────────────────────────────────────────────── */

(function (g) {
  'use strict';

  function snapshot(btn) {
    if (!btn.getAttribute('data-original')) {
      btn.setAttribute('data-original', btn.innerHTML);
    }
  }

  function toggleReveal(btn, defaultOpenLabel) {
    snapshot(btn);
    var content = btn.nextElementSibling;
    if (!content) return false;
    var revealed = content.classList.toggle('revealed');
    var openLabel = btn.getAttribute('data-hide-label') || defaultOpenLabel;
    btn.innerHTML = revealed ? openLabel : btn.getAttribute('data-original');
    /* Announce state to screen readers (WCAG 4.1.2 Name, Role, Value). */
    btn.setAttribute('aria-expanded', revealed ? 'true' : 'false');
    return revealed;
  }

  /* Seed aria-expanded="false" on every reveal-toggle at load time, so
     assistive tech reads correct state before the first interaction.
     Also marks the paired content as a region for navigation. */
  function initAria() {
    var selectors = '.secret-toggle, .secret-era-toggle, .legend-era-toggle';
    var btns = document.querySelectorAll(selectors);
    for (var i = 0; i < btns.length; i++) {
      if (!btns[i].hasAttribute('aria-expanded')) {
        btns[i].setAttribute('aria-expanded', 'false');
      }
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAria);
  } else {
    initAria();
  }

  /* Default open-state labels can be overridden per-button via
     data-hide-label="…": useful where a shorter "Hide" reads
     better than the full default. */

  g.toggleSecret = function (e, btn) {
    if (e && e.stopPropagation) e.stopPropagation();
    toggleReveal(btn, '⚿ &nbsp; Hide Secret');
  };

  g.toggleEraSecret = function (e, btn) {
    if (e && e.stopPropagation) e.stopPropagation();
    toggleReveal(btn, '⚿ &nbsp; Hide Secret');
  };

  g.toggleEraLegend = function (e, btn) {
    if (e && e.stopPropagation) e.stopPropagation();
    toggleReveal(btn, '◈ &nbsp; Hide Popular Belief');
  };

  g.toggleEra = function (el) {
    el.classList.toggle('open');
  };
})(window);
