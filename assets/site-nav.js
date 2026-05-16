/* ───────────────────────────────────────────────────────────────
   site-nav.js — persistent sidebar menu
   Loaded by every published page (typically with `defer`).

   Single source of truth for the menu structure:
   - top-level sections in NAV_SECTIONS (cosmology, talan, factions)
   - the 13 domains in DOMAINS, with their sub-region/settlement children

   To add or rename a page in the sidebar, edit those arrays below.

   The page declares its location with <body data-page="<slug>">.
   The accordion auto-expands the domain whose child matches the
   current data-page on load. Domain rows are click-to-expand:
   click the chevron to toggle, click the name to navigate.
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ── Domain & sub-region structure ─────────────────────────────
  var DOMAINS = [
    { slug: 'vindul',   label: 'Vindul · Wind',       href: '/talan/domains/vindul/vindul.html',     children: [] },
    { slug: 'lautara',  label: 'Lautara · Commerce',  href: '/talan/domains/lautara/lautara.html',   children: [
      { slug: 'emarrea', label: 'Emarrea · Kitsune Kingdom', href: '/talan/domains/lautara/emarrea.html' }
    ]},
    { slug: 'myrkono',  label: 'Myrkono · Darkness',  href: '/talan/domains/myrkono/myrkono.html',   children: [
      { slug: 'myrria',  label: 'Myrria · City of Second Chances', href: '/talan/domains/myrkono/myrria/myrria.html' }
    ]},
    { slug: 'floteyn',  label: 'Floteyn · Water',     href: '/talan/domains/floteyn/floteyn.html',   children: [] },
    { slug: 'sumendar', label: 'Sumendar · Fire',     href: '/talan/domains/sumendar/sumendar.html', children: [] },
    { slug: 'lioaru',   label: 'Lioaru · Time',       href: '/talan/domains/lioaru/lioaru.html',     children: [] },
    { slug: 'brauogi',  label: 'Brauogi · Earth',     href: '/talan/domains/brauogi/brauogi.html',   children: [] },
    { slug: 'ezkudon',  label: 'Ezkudon · Knowledge', href: '/talan/domains/ezkudon/ezkudon.html',   children: [] },
    { slug: 'egulon',   label: 'Egulon · Light',      href: '/talan/domains/egulon/egulon.html',     children: [] },
    { slug: 'zuzental', label: 'Zuzental · Law',      href: '/talan/domains/zuzental/zuzental.html', children: [] },
    { slug: 'nashavel', label: 'Nashavel · Chaos',    href: '/talan/domains/nashavel/nashavel.html', children: [] },
    { slug: 'ehizahar', label: 'Ehizahar · Hunt',     href: '/talan/domains/ehizahar/ehizahar.html', children: [
      { slug: 'fenurra', label: 'Fenurra · The Flame-Source', href: '/talan/domains/ehizahar/fenurra.html' }
    ]},
    { slug: 'askamira', label: 'Askamira · Freedom',  href: '/talan/domains/askamira/askamira.html', children: [] }
  ];

  // ── Determine which domain (if any) should auto-expand ──────
  // Expands when the current page is either the domain itself
  // or one of its nested children. Missing the chevron is then
  // not a punishment — you can still see what's underneath.
  function findExpandedDomainSlug(currentPage) {
    if (!currentPage) return null;
    for (var i = 0; i < DOMAINS.length; i++) {
      var d = DOMAINS[i];
      if (d.slug === currentPage) return d.slug;
      for (var j = 0; j < d.children.length; j++) {
        if (d.children[j].slug === currentPage) return d.slug;
      }
    }
    return null;
  }

  // ── HTML builders ─────────────────────────────────────────────
  function buildDomainRow(d, expandSlug) {
    var hasChildren = d.children && d.children.length > 0;
    var isExpanded  = hasChildren && d.slug === expandSlug;
    var liClass     = 'nav-domain' + (hasChildren ? ' has-children' : '') + (isExpanded ? ' expanded' : '');

    var chevron = hasChildren
      ? '<button class="nav-expand" data-domain="' + d.slug + '" aria-label="Toggle ' + d.label + ' sub-regions" aria-expanded="' + (isExpanded ? 'true' : 'false') + '" type="button">▸</button>'
      : '';

    var sublist = '';
    if (hasChildren) {
      var items = d.children.map(function (c) {
        return '<li><a href="' + c.href + '" data-page="' + c.slug + '">' + c.label + '</a></li>';
      }).join('');
      sublist = '<ul class="nav-sublist">' + items + '</ul>';
    }

    return (
      '<li class="' + liClass + '">' +
        '<div class="nav-domain-row">' +
          '<a href="' + d.href + '" data-page="' + d.slug + '">' + d.label + '</a>' +
          chevron +
        '</div>' +
        sublist +
      '</li>'
    );
  }

  function buildNavHtml(currentPage) {
    var expandSlug = findExpandedDomainSlug(currentPage);
    var domainItems = DOMAINS.map(function (d) { return buildDomainRow(d, expandSlug); }).join('\n');

    return [
      '<button class="nav-toggle" id="navToggle" aria-label="Open navigation" type="button">≡ Menu</button>',
      '<div class="nav-scrim" id="navScrim"></div>',
      '<aside class="site-nav" id="siteNav" aria-label="Site navigation">',
      '  <a href="/index.html" class="site-nav-title">Tyrnarra</a>',

      '  <div class="nav-section">',
      '    <div class="nav-section-label">World &amp; Cosmos</div>',
      '    <ul class="nav-list">',
      '      <li><a href="/index.html"         data-page="cosmology">Cosmology</a></li>',
      '      <li><a href="/grand-gods.html"    data-page="gods">The 13 Bound Gods</a></li>',
      '      <li><a href="/magic.html"         data-page="magic">Magic &amp; Faith</a></li>',
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <div class="nav-section-label">Talan</div>',
      '    <ul class="nav-list">',
      '      <li><a href="/talan/talan.html"       data-page="talan">Continent Overview</a></li>',
      '      <li><a href="/talan/history.html"     data-page="history">History &amp; Eras</a></li>',
      '      <li><a href="/talan/the-binding.html" data-page="the-binding">The Binding</a></li>',
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <div class="nav-section-label">Domains</div>',
      '    <ul class="nav-list">',
           domainItems,
      '    </ul>',
      '  </div>',

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
  }

  // ── Wire-up ───────────────────────────────────────────────────
  function init() {
    var currentPage = document.body.getAttribute('data-page');
    document.body.insertAdjacentHTML('afterbegin', buildNavHtml(currentPage));

    var nav    = document.getElementById('siteNav');
    var toggle = document.getElementById('navToggle');
    var scrim  = document.getElementById('navScrim');
    if (!nav || !toggle) return;

    // Highlight current page (matches both top-level links and sub-region children)
    if (currentPage) {
      var link = nav.querySelector('a[data-page="' + currentPage + '"]');
      if (link) link.classList.add('is-current');
    }

    // Sidebar open/close
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

    // Accordion: click chevron to expand/collapse the domain row
    nav.querySelectorAll('.nav-expand').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var li = btn.closest('.nav-domain');
        if (!li) return;
        var expanded = li.classList.toggle('expanded');
        btn.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
