/* ───────────────────────────────────────────────────────────────
   site-nav.js: persistent sidebar menu
   Loaded by every published page (typically with `defer`).

   Single source of truth for the menu structure:
   - the Talan-level reference pages in TALAN_PAGES
   - the 13 domains in DOMAINS (with sub-region / settlement / location children)
   - the remaining fixed sections (World & Cosmos, Factions, Off-Continent)
     are string literals inside buildNavHtml()

   Tree shape (any depth: children may themselves have children):
     { slug, label, href, children: [ { slug, label, href, children: […] } ] }

   The page declares its location with <body data-page="<slug>">.
   On load, the sidebar walks the tree for that slug and auto-expands
   the full ancestor chain: every other branch stays collapsed.
   Click a chevron to expand/collapse a row; click the label to navigate.
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ── Talan-level pages (collapsible) ───────────────────────────
  // Note: the Talan section header itself links to the Continent
  // Overview, so that page is not repeated here.
  var TALAN_PAGES = [
    { slug: 'history',     label: 'History &amp; Eras', href: '/talan/history.html',     children: [] },
    { slug: 'the-binding', label: 'The Binding',        href: '/talan/the-binding.html', children: [
      { slug: 'hollow-of-ten-thousand-threads', label: 'Hollow of Ten Thousand Threads', href: '/talan/the-binding/hollow-of-ten-thousand-threads.html', children: [] }
    ]},
    { slug: 'ancestries',  label: 'Ancestries',                href: '/talan/ancestries.html',           children: [] },
    { slug: 'historical',  label: 'Historical · The Fallen',   href: '/talan/historical/historical.html', children: [
      { slug: 'golden-empire',     label: 'The Golden Empire',     href: '/talan/historical/golden-empire.html',     children: [] },
      { slug: 'storveldi-denbora', label: 'The Storveldi Denbora', href: '/talan/historical/storveldi-denbora.html', children: [] },
      { slug: 'elden',             label: 'The Elden',             href: '/talan/historical/elden.html',             children: [] }
    ]}
  ];

  // ── Domain & sub-region structure ─────────────────────────────
  // Children may nest to whatever depth the world requires.
  // Practical ceiling is ~5 levels before labels start to wrap.
  var DOMAINS = [
    { slug: 'vindul',   label: 'Vindul · Wind',       href: '/talan/domains/vindul/vindul.html',     children: [] },
    { slug: 'lautara',  label: 'Lautara · Commerce',  href: '/talan/domains/lautara/lautara.html',   children: [
      { slug: 'emarrea', label: 'Emarrea · Kitsune Kingdom', href: '/talan/domains/lautara/emarrea.html', children: [] }
    ]},
    { slug: 'myrkono',  label: 'Myrkono · Darkness',  href: '/talan/domains/myrkono/myrkono.html',   children: [
      { slug: 'myrria', label: 'Myrria · City of Second Chances', href: '/talan/domains/myrkono/myrria/myrria.html', children: [] }
    ]},
    { slug: 'floteyn',  label: 'Floteyn · Water',     href: '/talan/domains/floteyn/floteyn.html',   children: [] },
    { slug: 'sumendar', label: 'Sumendar · Fire',     href: '/talan/domains/sumendar/sumendar.html', children: [
      { slug: 'order-of-steam', label: 'Order of Steam · Industrial Kingdom', href: '/talan/domains/sumendar/order-of-steam/order-of-steam.html', children: [
        { slug: 'house-eisenhart', label: 'House Eisenhart', href: '/talan/domains/sumendar/order-of-steam/house-eisenhart.html', children: [] }
      ]},
      { slug: 'dragons-reach', label: 'Dragon\'s Reach · Dragon Capital', href: '/talan/domains/sumendar/dragons-reach.html', children: [] }
    ]},
    { slug: 'lioaru',   label: 'Lioaru · Time',       href: '/talan/domains/lioaru/lioaru.html',     children: [
      { slug: 'lost-kingdom', label: 'Lost Kingdom · Blackened Lands', href: '/talan/domains/lioaru/lost-kingdom.html', children: [] }
    ]},
    { slug: 'brauogi',  label: 'Brauogi · Earth',     href: '/talan/domains/brauogi/brauogi.html',   children: [] },
    { slug: 'ezkudon',  label: 'Ezkudon · Knowledge', href: '/talan/domains/ezkudon/ezkudon.html',   children: [] },
    { slug: 'egulon',   label: 'Egulon · Light',      href: '/talan/domains/egulon/egulon.html',     children: [] },
    { slug: 'zuzental', label: 'Zuzental · Law',      href: '/talan/domains/zuzental/zuzental.html', children: [
      { slug: 'lograth',          label: 'Lograth · The Judgment City',        href: '/talan/domains/zuzental/lograth/lograth.html',  children: [] },
      { slug: 'thousand-kingdom', label: 'Thousand Kingdom · Forseti\'s Realm', href: '/talan/domains/zuzental/thousand-kingdom.html', children: [] },
      { slug: 'emerald-isles',    label: 'Emerald Isles · Island Kingdom',     href: '/talan/domains/zuzental/emerald-isles.html',    children: [] },
      { slug: 'legea-empire',     label: 'Legea Empire · Demigod Theocracy',   href: '/talan/domains/zuzental/legea-empire.html',     children: [] },
      { slug: 'crossroads',       label: 'Crossroads · Southern Tri-Domain Nexus', href: '/talan/domains/zuzental/crossroads.html',  children: [] }
    ]},
    { slug: 'nashavel', label: 'Nashavel · Chaos',    href: '/talan/domains/nashavel/nashavel.html', children: [] },
    { slug: 'ehizahar', label: 'Ehizahar · Hunt',     href: '/talan/domains/ehizahar/ehizahar.html', children: [
      { slug: 'fenurra', label: 'Fenurra · The Flame-Source', href: '/talan/domains/ehizahar/fenurra.html', children: [] }
    ]},
    { slug: 'askamira', label: 'Askamira · Freedom',  href: '/talan/domains/askamira/askamira.html', children: [] }
  ];

  // ── Walk the tree for the current slug, return ancestor path ──
  // Returns an array of slugs from the root of the tree down to and
  // including the matched node. Used to decide which rows auto-expand.
  function findAncestorPath(arr, currentPage) {
    if (!currentPage || !arr) return null;
    for (var i = 0; i < arr.length; i++) {
      var node = arr[i];
      if (node.slug === currentPage) return [node.slug];
      if (node.children && node.children.length > 0) {
        var deeper = findAncestorPath(node.children, currentPage);
        if (deeper) return [node.slug].concat(deeper);
      }
    }
    return null;
  }

  function buildExpandedSet(arr, currentPage) {
    var path = findAncestorPath(arr, currentPage);
    var set  = Object.create(null);
    if (path) {
      for (var i = 0; i < path.length; i++) set[path[i]] = true;
    }
    return set;
  }

  // ── HTML builders ─────────────────────────────────────────────
  // Recursive accordion row. `depth` starts at 1 for top-level rows
  // inside a section's <ul class="nav-list"> and increments by one
  // for each level of nesting: CSS uses data-depth to step the
  // indent / font-size / dim per level.
  function buildAccordionRow(node, expandedSet, depth) {
    var hasChildren = node.children && node.children.length > 0;
    var isExpanded  = hasChildren && !!expandedSet[node.slug];
    var liClass     = 'nav-domain' + (hasChildren ? ' has-children' : '') + (isExpanded ? ' expanded' : '');

    var chevron = hasChildren
      ? '<button class="nav-expand" data-domain="' + node.slug + '" aria-label="Toggle ' + node.label + ' children" aria-expanded="' + (isExpanded ? 'true' : 'false') + '" type="button">▸</button>'
      : '';

    var sublist = '';
    if (hasChildren) {
      var items = node.children.map(function (c) {
        return buildAccordionRow(c, expandedSet, depth + 1);
      }).join('');
      sublist = '<ul class="nav-sublist">' + items + '</ul>';
    }

    return (
      '<li class="' + liClass + '" data-depth="' + depth + '">' +
        '<div class="nav-domain-row">' +
          '<a href="' + node.href + '" data-page="' + node.slug + '">' + node.label + '</a>' +
          chevron +
        '</div>' +
        sublist +
      '</li>'
    );
  }

  function buildNavHtml(currentPage) {
    var talanExpanded  = buildExpandedSet(TALAN_PAGES, currentPage);
    var domainExpanded = buildExpandedSet(DOMAINS,     currentPage);
    var talanItems     = TALAN_PAGES.map(function (d) { return buildAccordionRow(d, talanExpanded,  1); }).join('\n');
    var domainItems    = DOMAINS.map(    function (d) { return buildAccordionRow(d, domainExpanded, 1); }).join('\n');

    return [
      '<button class="nav-toggle" id="navToggle" aria-label="Open navigation" type="button">≡ Menu</button>',
      '<div class="nav-scrim" id="navScrim"></div>',
      '<aside class="site-nav" id="siteNav" aria-label="Site navigation">',
      '  <a href="/index.html" class="site-nav-title">Tyrnarra</a>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/index.html" data-page="cosmology">World &amp; Cosmos</a>',
      '    <ul class="nav-list">',
      '      <li><a href="/grand-gods.html"      data-page="gods">The 13 Bound Gods</a></li>',
      '      <li><a href="/non-bound-gods.html"  data-page="non-bound-gods">Non-Bound Gods &amp; Beings</a></li>',
      '      <li><a href="/gods-law.html"        data-page="gods-law">The Gods&rsquo; Law</a></li>',
      '      <li><a href="/magic.html"           data-page="magic">Magic &amp; Faith</a></li>',
      '      <li><a href="/pf2e-registrar.html"  data-page="pf2e-registrar">PF2e Registrar</a></li>',
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/talan/talan.html" data-page="talan">Talan</a>',
      '    <ul class="nav-list">',
           talanItems,
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/talan/domains/domains.html" data-page="domains-hub">Domains</a>',
      '    <ul class="nav-list">',
           domainItems,
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/talan/factions/factions.html" data-page="factions">Factions</a>',
      '    <ul class="nav-list">',
      '      <li><a href="/talan/factions/adventurers-guild.html" data-page="adventurers-guild">Adventurers Guild</a></li>',
      '      <li><a href="/talan/factions/mercenary-guild.html"   data-page="mercenary-guild">Mercenary Guild</a></li>',
      '      <li><a href="/talan/factions/god-churches.html"      data-page="god-churches">God Churches</a></li>',
      '      <li><a href="/talan/factions/remnants.html"          data-page="remnants">Remnants of Corruption</a></li>',
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/off-continent/off-continent.html" data-page="off-continent-hub">Off-Continent</a>',
      '    <ul class="nav-list">',
      '      <li><a href="/off-continent/sortalde.html"   data-page="sortalde">Sortalde · Petal Continent</a></li>',
      '      <li><a href="/off-continent/red-empire.html" data-page="red-empire">The Red Empire</a></li>',
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

    // Highlight current page (matches both top-level links and nested children at any depth)
    if (currentPage) {
      var link = nav.querySelector('a[data-page="' + currentPage + '"]');
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

    // Accordion: click chevron to expand/collapse the row at any depth
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
