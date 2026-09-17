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

   Also wires the place-map widget by delegation (no inline handlers):
   a click on .pm-cell[data-area] or .pm-hot[data-area] inside a
   .place-map renders window.PLACE_AREAS[<data-areas>][<data-area>]
   ({k, n, t}) into the map's .pm-detail, marks every cell sharing the
   key .active, and keeps aria-expanded / aria-controls in step. Clicking
   the active cell again closes the panel. Markup in style-b.css.

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

  /* ── Place-map ─────────────────────────────────────────────── */
  var pmSeq = 0;

  function pmAreas(map) {
    var src = g.PLACE_AREAS || {};
    var name = map.getAttribute('data-areas');
    return name ? src[name] : src;
  }

  function pmRender(map, btn) {
    var key = btn.getAttribute('data-area');
    var areas = pmAreas(map);
    var detail = map.querySelector('.pm-detail');
    if (!areas || !detail) return;
    if (!detail.id) detail.id = 'pm-detail-' + (++pmSeq);
    var wasActive = btn.classList.contains('active');
    var all = map.querySelectorAll('.pm-cell, .pm-hot');
    for (var i = 0; i < all.length; i++) {
      all[i].classList.remove('active');
      all[i].setAttribute('aria-expanded', 'false');
    }
    if (wasActive) { detail.innerHTML = ''; return; }
    var d = areas[key];
    if (!d) return;
    var same = map.querySelectorAll('[data-area="' + key + '"]');
    for (var j = 0; j < same.length; j++) {
      same[j].classList.add('active');
      same[j].setAttribute('aria-expanded', 'true');
    }
    detail.innerHTML = '<div class="pm-detail-inner">' +
      (d.k ? '<div class="pm-detail-kicker">' + d.k + '</div>' : '') +
      '<h3 class="pm-detail-name">' + d.n + '</h3>' +
      (d.t || '') + '</div>';
  }

  function pmInit() {
    var maps = document.querySelectorAll('.place-map');
    for (var m = 0; m < maps.length; m++) {
      var detail = maps[m].querySelector('.pm-detail');
      if (detail && !detail.id) detail.id = 'pm-detail-' + (++pmSeq);
      var cells = maps[m].querySelectorAll('.pm-cell[data-area], .pm-hot[data-area]');
      for (var c = 0; c < cells.length; c++) {
        cells[c].setAttribute('aria-expanded', 'false');
        if (detail) cells[c].setAttribute('aria-controls', detail.id);
      }
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', pmInit);
  } else {
    pmInit();
  }

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var btn = t.closest('.pm-cell[data-area], .pm-hot[data-area]');
    if (!btn) return;
    var map = btn.closest('.place-map');
    if (map) pmRender(map, btn);
  });
})(window);
