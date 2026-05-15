/* ───────────────────────────────────────────────────────────────
   site-nav.js — persistent sidebar menu
   Loaded by every published page (typically with `defer`).

   Single source of truth for the menu structure: to add or rename
   a page in the sidebar, edit the NAV_HTML template below.

   The page declares its location with <body data-page="<slug>">.
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ── Menu HTML ─────────────────────────────────────────────────
  // Edit here to change what appears in the sidebar.
  var NAV_HTML = [
    '<button class="nav-toggle" id="navToggle" aria-label="Open navigation" type="button">≡ Menu</button>',
    '<div class="nav-scrim" id="navScrim"></div>',
    '<aside class="site-nav" id="siteNav" aria-label="Site navigation">',
    '  <a href="/index.html" class="site-nav-title">Tyrnarra</a>',
    '',
    '  <div class="nav-section">',
    '    <div class="nav-section-label">World &amp; Cosmos</div>',
    '    <ul class="nav-list">',
    '      <li><a href="/index.html"         data-page="cosmology">Cosmology</a></li>',
    '      <li><a href="/grand-gods.html" data-page="gods">The 13 Bound Gods</a></li>',
    '      <li><a href="/magic.html"         data-page="magic">Magic &amp; Faith</a></li>',
    '    </ul>',
    '  </div>',
    '',
    '  <div class="nav-section">',
    '    <div class="nav-section-label">Talan</div>',
    '    <ul class="nav-list">',
    '      <li><a href="/talan/talan.html"   data-page="talan">Continent Overview</a></li>',
    '      <li><a href="/talan/history.html" data-page="history">History &amp; Eras</a></li>',
    '    </ul>',
    '  </div>',
    '',
    '  <div class="nav-section">',
    '    <div class="nav-section-label">Domains</div>',
    '    <ul class="nav-list">',
    '      <li><a href="/talan/domains/vindul/vindul.html"     data-page="vindul">Vindul · Wind</a></li>',
    '      <li><a href="/talan/domains/lautara/lautara.html"   data-page="lautara">Lautara · Commerce</a></li>',
    '      <li><a href="/talan/domains/myrkono/myrkono.html"   data-page="myrkono">Myrkono · Darkness</a></li>',
    '      <li><a href="/talan/domains/floteyn/floteyn.html"   data-page="floteyn">Floteyn · Water</a></li>',
    '      <li><a href="/talan/domains/sumendar/sumendar.html" data-page="sumendar">Sumendar · Fire</a></li>',
    '      <li><a href="/talan/domains/lioaru/lioaru.html"     data-page="lioaru">Lioaru · Time</a></li>',
    '      <li><a href="/talan/domains/brauogi/brauogi.html"   data-page="brauogi">Brauogi · Earth</a></li>',
    '      <li><a href="/talan/domains/ezkudon/ezkudon.html"   data-page="ezkudon">Ezkudon · Knowledge</a></li>',
    '      <li><a href="/talan/domains/egulon/egulon.html"     data-page="egulon">Egulon · Light</a></li>',
    '      <li><a href="/talan/domains/zuzental/zuzental.html" data-page="zuzental">Zuzental · Law</a></li>',
    '      <li><a href="/talan/domains/nashavel/nashavel.html" data-page="nashavel">Nashavel · Chaos</a></li>',
    '      <li><a href="/talan/domains/ehizahar/ehizahar.html" data-page="ehizahar">Ehizahar · Hunt</a></li>',
    '      <li><a href="/talan/domains/askamira/askamira.html" data-page="askamira">Askamira · Freedom</a></li>',
    '    </ul>',
    '  </div>',
    '',
    '  <div class="nav-section">',
    '    <div class="nav-section-label">Factions</div>',
    '    <ul class="nav-list">',
    '      <li><a href="/talan/factions/factions.html"          data-page="factions">All Factions</a></li>',
    '      <li><a href="/talan/factions/adventurers-guild.html" data-page="adventurers-guild">Adventurers Guild</a></li>',
    '      <li><a href="/talan/factions/mercenary-guild.html"   data-page="mercenary-guild">Mercenary Guild</a></li>',
    '      <li><a href="/talan/factions/god-churches.html"      data-page="god-churches">God Churches</a></li>',
    '      <li><a href="/talan/factions/remnants.html"          data-page="remnants">Remnants of Corruption</a></li>',
    '    </ul>',
    '  </div>',
    '</aside>'
  ].join('\n');

  // ── Wire-up ───────────────────────────────────────────────────
  function init() {
    // Inject the markup at the very start of <body> so the toggle
    // is on top and the sidebar slides over content.
    document.body.insertAdjacentHTML('afterbegin', NAV_HTML);

    var nav = document.getElementById('siteNav');
    var toggle = document.getElementById('navToggle');
    var scrim = document.getElementById('navScrim');
    if (!nav || !toggle) return;

    // Highlight current page
    var current = document.body.getAttribute('data-page');
    if (current) {
      var link = nav.querySelector('a[data-page="' + current + '"]');
      if (link) link.classList.add('is-current');
    }

    function open()  { nav.classList.add('open');    if (scrim) scrim.classList.add('open'); }
    function close() { nav.classList.remove('open'); if (scrim) scrim.classList.remove('open'); }

    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      nav.classList.contains('open') ? close() : open();
    });
    if (scrim) scrim.addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
