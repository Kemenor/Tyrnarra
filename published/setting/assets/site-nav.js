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

  // ── Favicon + manifest (single source of truth) ──────────────
  // The favicon pack lives at site root; these tags are injected
  // here so every page that loads the sidebar gets them from one
  // place. A bare /favicon.ico at root is auto-requested by the
  // browser as a no-JS baseline; this upgrades to the SVG / Apple
  // touch icon / PWA manifest and sets the tab theme colour.
  function injectFavicon() {
    var head = document.head || document.getElementsByTagName('head')[0];
    if (!head || head.querySelector('link[rel~="icon"]')) return; // already wired
    var links = [
      { rel: 'icon', href: '/favicon.ico', sizes: 'any' },
      { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32.png' },
      { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16.png' },
      { rel: 'apple-touch-icon', href: '/favicon-180.png' },
      { rel: 'manifest', href: '/site.webmanifest' }
    ];
    links.forEach(function (spec) {
      var el = document.createElement('link');
      Object.keys(spec).forEach(function (k) { el.setAttribute(k, spec[k]); });
      head.appendChild(el);
    });
    if (!head.querySelector('meta[name="theme-color"]')) {
      var meta = document.createElement('meta');
      meta.setAttribute('name', 'theme-color');
      meta.setAttribute('content', '#101C3A');
      head.appendChild(meta);
    }
  }
  injectFavicon();

  // ── Talan-level pages (collapsible) ───────────────────────────
  // Note: the Talan section header itself links to the Continent
  // Overview, so that page is not repeated here.
  var TALAN_PAGES = [
    { slug: 'maps',        label: 'Maps of Talan',      href: '/setting/talan/maps.html',        children: [] },
    { slug: 'history',     label: 'History &amp; Eras', href: '/setting/talan/history.html',     children: [] },
    { slug: 'the-binding', label: 'The Binding',        href: '/setting/talan/the-binding.html', children: [
      { slug: 'hollow-of-ten-thousand-threads', label: 'Hollow of Ten Thousand Threads', href: '/setting/talan/the-binding/hollow-of-ten-thousand-threads.html', children: [] }
    ]},
    { slug: 'ancestries',  label: 'Ancestries',                href: '/setting/talan/ancestries.html',           children: [] },
    { slug: 'historical',  label: 'Historical · The Fallen',   href: '/setting/talan/historical/historical.html', children: [
      { slug: 'golden-empire',     label: 'The Golden Empire',     href: '/setting/talan/historical/golden-empire.html',     children: [] },
      { slug: 'storveldi-denbora', label: 'The Storveldi Denbora', href: '/setting/talan/historical/storveldi-denbora.html', children: [] },
      { slug: 'elden',             label: 'The Elden',             href: '/setting/talan/historical/elden.html',             children: [] }
    ]}
  ];

  // ── Domain & sub-region structure ─────────────────────────────
  // Children may nest to whatever depth the world requires.
  // Practical ceiling is ~5 levels before labels start to wrap.
  var DOMAINS = [
    { slug: 'vindul',   label: 'Vindul · Wind',       href: '/setting/talan/domains/vindul/vindul.html',     children: [
      { slug: 'baerfrost',     label: 'Baerfrost &middot; Hunt-League',     href: '/setting/talan/domains/vindul/baerfrost/baerfrost.html',         children: [] },
      { slug: 'air-monastery', label: 'Air Monastery &middot; Wyndwalken',  href: '/setting/talan/domains/vindul/air-monastery/air-monastery.html', children: [] },
      { slug: 'fellibylur',    label: 'Fellibylur &middot; Stormpact',      href: '/setting/talan/domains/vindul/fellibylur/fellibylur.html',       children: [] },
      { slug: 'haizava',       label: 'Haizava &middot; the Shifting City', href: '/setting/talan/domains/vindul/haizava/haizava.html',             children: [] },
      { slug: 'haizetsua',     label: 'Haizetsua &middot; Tengu Island',    href: '/setting/talan/domains/vindul/haizetsua/haizetsua.html',         children: [] }
    ]},
    { slug: 'lautara',  label: 'Lautara · Commerce',  href: '/setting/talan/domains/lautara/lautara.html',   children: [
      { slug: 'merkavar', label: 'Merkavar · the Market City', href: '/setting/talan/domains/lautara/merkavar/merkavar.html', children: [] },
      { slug: 'azkataria', label: 'Azkataria · Philosopher-Market', href: '/setting/talan/domains/lautara/azkataria/azkataria.html', children: [] },
      { slug: 'dreaming-cape', label: 'The Dreaming Cape · Twin Lantern', href: '/setting/talan/domains/lautara/dreaming-cape/dreaming-cape.html', children: [
        { slug: 'millhaven', label: 'Millhaven · River-Border Town', href: '/setting/talan/domains/lautara/millhaven/millhaven.html', children: [
          { slug: 'wayward-compass', label: 'The Wayward Compass', href: '/setting/talan/domains/lautara/millhaven/wayward-compass.html', children: [] }
        ] }
      ] },
      { slug: 'rika-tikur', label: 'Rika Tikur · the Plutocracy', href: '/setting/talan/domains/lautara/rika-tikur/rika-tikur.html', children: [] },
      { slug: 'itsasalda', label: 'Itsasalda · The Vordsbench', href: '/setting/talan/domains/lautara/itsasalda/itsasalda.html', children: [
        { slug: 'millhaven', label: 'Millhaven · River-Border Town', href: '/setting/talan/domains/lautara/millhaven/millhaven.html', children: [
          { slug: 'wayward-compass', label: 'The Wayward Compass', href: '/setting/talan/domains/lautara/millhaven/wayward-compass.html', children: [] }
        ] }
      ] },
      { slug: 'atarialda', label: 'Atarialda · Hearth-Halflings', href: '/setting/talan/domains/lautara/atarialda/atarialda.html', children: [] },
      { slug: 'emarrea', label: 'Emarrea · Kitsune Kingdom', href: '/setting/talan/domains/lautara/emarrea/emarrea.html', children: [
        { slug: 'heartcourt', label: 'The Heartcourt', href: '/setting/talan/domains/lautara/emarrea/heartcourt.html', children: [] }
      ]}
    ]},
    { slug: 'myrkono',  label: 'Myrkono · Darkness',  href: '/setting/talan/domains/myrkono/myrkono.html',   children: [
      { slug: 'ilun-tasun', label: 'Ilun Tasun · the Kept Lamp', href: '/setting/talan/domains/myrkono/ilun-tasun/ilun-tasun.html', children: [] },
      { slug: 'itzasoa', label: 'Itzasoa · the Woven Wood', href: '/setting/talan/domains/myrkono/itzasoa/itzasoa.html', children: [] },
      { slug: 'izarelai', label: 'Izarelai · the Star Plain', href: '/setting/talan/domains/myrkono/izarelai/izarelai.html', children: [] },
      { slug: 'myrria', label: 'Myrria · City of Second Chances', href: '/setting/talan/domains/myrkono/myrria/myrria.html', children: [] },
      { slug: 'three-pines', label: 'Three Pines · the Forest That Sails', href: '/setting/talan/domains/myrkono/three-pines/three-pines.html', children: [] },
      { slug: 'tvisol', label: 'Tvisol · the Kingdom of the Two Suns', href: '/setting/talan/domains/brauogi/tvisol/tvisol.html', children: [] }
    ]},
    { slug: 'floteyn',  label: 'Floteyn · Water',     href: '/setting/talan/domains/floteyn/floteyn.html',   children: [
      { slug: 'uravel', label: 'Uravel &middot; the Floating Isles', href: '/setting/talan/domains/floteyn/uravel/uravel.html', children: [] }
    ]},
    { slug: 'sumendar', label: 'Sumendar · Fire',     href: '/setting/talan/domains/sumendar/sumendar.html', children: [
      { slug: 'eldara',         label: 'Eldara &middot; the Forge City', href: '/setting/talan/domains/sumendar/eldara/eldara.html', children: [] },
      { slug: 'order-of-steam', label: 'Order of Steam · Industrial Kingdom', href: '/setting/talan/domains/sumendar/order-of-steam/order-of-steam.html', children: [
        { slug: 'house-eisenhart', label: 'House Eisenhart', href: '/setting/talan/domains/sumendar/order-of-steam/house-eisenhart.html', children: [] }
      ]},
      { slug: 'dragons-reach', label: 'Dragon\'s Reach · Dragon Capital', href: '/setting/talan/domains/sumendar/dragons-reach.html', children: [] }
    ]},
    { slug: 'lioaru',   label: 'Lioaru · Time',       href: '/setting/talan/domains/lioaru/lioaru.html',     children: [
      { slug: 'valreka',      label: 'Valreka &middot; the Whale-Borne City', href: '/setting/talan/domains/lioaru/valreka/valreka.html', children: [] },
      { slug: 'lost-kingdom', label: 'Lost Kingdom · Blackened Lands', href: '/setting/talan/domains/lioaru/lost-kingdom.html', children: [] }
    ]},
    { slug: 'brauogi',  label: 'Brauogi · Earth',     href: '/setting/talan/domains/brauogi/brauogi.html',   children: [
      { slug: 'lurrath', label: 'Lurrath &middot; the Steadfast City', href: '/setting/talan/domains/brauogi/lurrath/lurrath.html', children: [] },
      { slug: 'sugeiturri', label: 'Sugeiturri &middot; the Source-Country', href: '/setting/talan/domains/brauogi/sugeiturri/sugeiturri.html', children: [] },
      { slug: 'haldmark', label: 'Haldmark &middot; the Kept March', href: '/setting/talan/domains/brauogi/haldmark/haldmark.html', children: [] },
      { slug: 'greenward', label: 'Greenward &middot; the Furrowsworn', href: '/setting/talan/domains/brauogi/greenward/greenward.html', children: [] },
      { slug: 'tvisol', label: 'Tvisol &middot; the Kingdom of the Two Suns', href: '/setting/talan/domains/brauogi/tvisol/tvisol.html', children: [] }
    ]},
    { slug: 'ezkudon',  label: 'Ezkudon · Knowledge', href: '/setting/talan/domains/ezkudon/ezkudon.html',   children: [
      { slug: 'thekkavar',     label: 'Thekkavar &middot; the City of Learning', href: '/setting/talan/domains/ezkudon/thekkavar/thekkavar.html', children: [] }
    ] },
    { slug: 'egulon',   label: 'Egulon · Light',      href: '/setting/talan/domains/egulon/egulon.html',     children: [
      { slug: 'ljosarn', label: 'Ljosarn &middot; the Everbright City', href: '/setting/talan/domains/egulon/ljosarn/ljosarn.html', children: [] }
    ]},
    { slug: 'zuzental', label: 'Zuzental · Law',      href: '/setting/talan/domains/zuzental/zuzental.html', children: [
      { slug: 'lograth',          label: 'Lograth · The Judgment City',        href: '/setting/talan/domains/zuzental/lograth/lograth.html',  children: [] },
      { slug: 'thousand-kingdom', label: 'Thousand Kingdom · Forseti\'s Realm', href: '/setting/talan/domains/zuzental/thousand-kingdom.html', children: [] },
      { slug: 'emerald-isles',    label: 'Emerald Isles · Island Kingdom',     href: '/setting/talan/domains/zuzental/emerald-isles.html',    children: [] },
      { slug: 'legea-empire',     label: 'Legea Empire · Demigod Theocracy',   href: '/setting/talan/domains/zuzental/legea-empire.html',     children: [] },
      { slug: 'crossroads',       label: 'Crossroads · Southern Tri-Domain Nexus', href: '/setting/talan/domains/zuzental/crossroads.html',  children: [] }
    ]},
    { slug: 'nashavel', label: 'Nashavel · Chaos',    href: '/setting/talan/domains/nashavel/nashavel.html', children: [
      { slug: 'nahaskel', label: 'Nahaskel &middot; the Unmapped City', href: '/setting/talan/domains/nashavel/nahaskel/nahaskel.html', children: [] }
    ]},
    { slug: 'ehizahar', label: 'Ehizahar · Hunt',     href: '/setting/talan/domains/ehizahar/ehizahar.html', children: [
      { slug: 'veidrath', label: 'Veidrath &middot; the Hunting City', href: '/setting/talan/domains/ehizahar/veidrath/veidrath.html', children: [] },
      { slug: 'fenurra', label: 'Fenurra · The Flame-Source', href: '/setting/talan/domains/ehizahar/fenurra.html', children: [] }
    ]},
    { slug: 'askamira', label: 'Askamira · Freedom',  href: '/setting/talan/domains/askamira/askamira.html', children: [
      { slug: 'frae-city',     label: 'Frae City &middot; the Unchained City', href: '/setting/talan/domains/askamira/frae-city/frae-city.html', children: [] }
    ] }
  ];

  // ── World & Cosmos section (collapsible) ──────────────────────
  // The section header links to the Cosmology landing (index.html),
  // so that page is not repeated as a leaf here.
  var WORLD_PAGES = [
    { slug: 'gods-hub', label: 'Gods &amp; Powerful Beings', href: '/setting/cosmology/gods.html', children: [
      { slug: 'primordials',  label: 'The Primordials &middot; Prelife',   href: '/setting/cosmology/primordials.html',  children: [] },
      { slug: 'gods',         label: 'The 13 Bound Gods &middot; Material', href: '/setting/cosmology/grand-gods.html',   children: [] },
      { slug: 'layer-3-gods', label: 'Layer-3 Gods &middot; Postlife',     href: '/setting/cosmology/layer-3-gods.html', children: [
        { slug: 'bolverk',    label: 'Bolverk &middot; the Megacity in Abyss', href: '/setting/cosmology/bolverk.html', children: [] }
      ]}
    ]},
    { slug: 'gods-law',       label: 'The Gods&rsquo; Law',         href: '/setting/cosmology/gods-law.html',       children: [] },
    { slug: 'magic',          label: 'Magic &amp; Faith',           href: '/setting/cosmology/magic.html',          children: [] },
    { slug: 'pf2e-registrar', label: 'PF2e Registrar',              href: '/setting/cosmology/pf2e-registrar.html', children: [] }
  ];

  // ── Factions section (collapsible) ────────────────────────────
  // Header links to the Factions hub, so it is not repeated here.
  var FACTION_PAGES = [
    { slug: 'adventurers-guild', label: 'Adventurers Guild',      href: '/setting/talan/factions/adventurers-guild.html', children: [] },
    { slug: 'mercenary-guild',   label: 'Mercenary Guild',        href: '/setting/talan/factions/mercenary-guild.html',   children: [] },
    { slug: 'voroir-daua',       label: 'The Voroir Daua',        href: '/setting/talan/factions/voroir-daua.html',       children: [] },
    { slug: 'god-churches',      label: 'God Churches',           href: '/setting/talan/factions/god-churches.html',      children: [] },
    { slug: 'remnants',          label: 'Remnants of Corruption', href: '/setting/talan/factions/remnants.html',          children: [] }
  ];

  // ── Off-Continent section (collapsible) ───────────────────────
  // Header links to the Off-Continent hub, so it is not repeated here.
  var OFFCONTINENT_PAGES = [
    { slug: 'sortalde',   label: 'Sortalde · Petal Continent', href: '/setting/off-continent/sortalde.html',   children: [] },
    { slug: 'red-empire', label: 'The Red Empire',             href: '/setting/off-continent/red-empire.html', children: [] }
  ];

  // The player-facing Campaigns layer (/player-campaigns/) carries its
  // OWN menu (pc-nav.js) and is reached via the foot button below, so it
  // is NOT a section in this setting menu. The GM-only /gm-notes/ tree
  // is likewise deliberately absent from any player-facing nav.

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
    var worldExpanded  = buildExpandedSet(WORLD_PAGES,        currentPage);
    var factionExpanded= buildExpandedSet(FACTION_PAGES,      currentPage);
    var offExpanded    = buildExpandedSet(OFFCONTINENT_PAGES, currentPage);
    var talanItems     = TALAN_PAGES.map(function (d) { return buildAccordionRow(d, talanExpanded,  1); }).join('\n');
    var domainItems    = DOMAINS.map(    function (d) { return buildAccordionRow(d, domainExpanded, 1); }).join('\n');
    var worldItems     = WORLD_PAGES.map(function (d) { return buildAccordionRow(d, worldExpanded,  1); }).join('\n');
    var factionItems   = FACTION_PAGES.map(function (d) { return buildAccordionRow(d, factionExpanded, 1); }).join('\n');
    var offItems       = OFFCONTINENT_PAGES.map(function (d) { return buildAccordionRow(d, offExpanded, 1); }).join('\n');

    return [
      '<button class="nav-toggle" id="navToggle" aria-label="Open navigation" type="button">≡ Menu</button>',
      '<div class="nav-scrim" id="navScrim"></div>',
      '<aside class="site-nav" id="siteNav" aria-label="Site navigation">',
      '  <a href="/setting/index.html" class="site-nav-title">Tyrnarra</a>',

      // Scrollable middle: title (above) and foot (below) stay pinned.
      '  <div class="nav-scroll">',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/setting/index.html" data-page="cosmology">World &amp; Cosmos</a>',
      '    <ul class="nav-list">',
           worldItems,
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/setting/talan/talan.html" data-page="talan">Talan</a>',
      '    <ul class="nav-list">',
           talanItems,
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/setting/talan/domains/domains.html" data-page="domains-hub">Domains</a>',
      '    <ul class="nav-list">',
           domainItems,
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/setting/talan/factions/factions.html" data-page="factions">Factions</a>',
      '    <ul class="nav-list">',
           factionItems,
      '    </ul>',
      '  </div>',

      '  <div class="nav-section">',
      '    <a class="nav-section-label nav-section-link" href="/setting/off-continent/off-continent.html" data-page="off-continent-hub">Off-Continent</a>',
      '    <ul class="nav-list">',
           offItems,
      '    </ul>',
      '  </div>',

      '  </div>', // close .nav-scroll
      '  <div class="nav-foot">',
      '    <a class="nav-foot-link" href="/player-campaigns/index.html">Player Campaigns &rarr;</a>',
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
