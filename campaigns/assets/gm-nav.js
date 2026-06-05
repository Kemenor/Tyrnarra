/* ───────────────────────────────────────────────────────────────
   gm-nav.js: left-side menu for the campaign / GM layer.
   Loaded with `defer` by every page under /campaigns/.

   Single source of truth for the GM menu is TREE below.
   Each page declares its location with <body data-page="<slug>">;
   on load the drawer auto-expands the ancestor chain of that slug.

   Tree shape (any depth): { slug, label, href|null, children:[…] }
   An entry with href:null renders as a non-link group label.
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ── Favicon + manifest (shared with the public site) ─────────
  // The GM layer carries its own menu, so it does not load
  // site-nav.js; mirror its favicon injection here so campaign
  // pages get the full icon set, not just the root /favicon.ico
  // baseline. Files live at the site root.
  (function injectFavicon() {
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
  })();

  var TREE = [
    { slug: 'furrious-five', label: 'The Furrious Five', href: '/campaigns/furrious-five/index.html', children: [
      { slug: 'millhaven-gm', label: 'Millhaven · GM Notes', href: '/campaigns/furrious-five/millhaven-gm.html', children: [
        { slug: 'wayward-compass-gm', label: 'The Wayward Compass', href: '/campaigns/furrious-five/wayward-compass-gm.html', children: [] },
        { slug: 'low-span-gm',        label: 'The Low Span',        href: '/campaigns/furrious-five/low-span-gm.html',       children: [] }
      ]},
      { slug: 'quests', label: 'Quests', href: null, children: [
        { slug: 'quest-veldtmark',  label: 'The Veldtmark Invitation', href: '/campaigns/furrious-five/quest-veldtmark.html',   children: [] },
        { slug: 'quest-venomqueen', label: 'Below the Quiet Docks',    href: '/campaigns/furrious-five/quest-venomqueen.html',  children: [] }
      ]}
    ]},
    { slug: 'tools', label: 'Tools', href: null, children: [
      { slug: 'map-area-editor', label: 'Map Area Editor', href: '/campaigns/tools/map-area-editor.html', children: [] }
    ]}
  ];

  var current = document.body.getAttribute('data-page') || '';

  // Find the ancestor-chain of slugs leading to `current`.
  var openChain = {};
  (function find(nodes, chain) {
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var next = chain.concat(n.slug);
      if (n.slug === current) { next.forEach(function (s) { openChain[s] = true; }); return true; }
      if (n.children && n.children.length && find(n.children, next)) {
        next.forEach(function (s) { openChain[s] = true; });
        return true;
      }
    }
    return false;
  })(TREE, []);

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function buildList(nodes, depth) {
    var ul = el('ul', depth === 1 ? 'gm-nav-list' : 'gm-nav-sublist');
    nodes.forEach(function (n) {
      var li = el('li', 'gm-nav-item');
      li.setAttribute('data-depth', depth);
      var hasKids = n.children && n.children.length;
      if (openChain[n.slug]) li.classList.add('expanded');

      var row = el('div', 'gm-nav-row');
      if (n.href) {
        var a = el('a', null, n.label);
        a.setAttribute('href', n.href);
        if (n.slug === current) a.classList.add('is-current');
        row.appendChild(a);
      } else {
        row.appendChild(el('span', 'gm-nav-grouplabel', n.label));
      }
      if (hasKids) {
        var btn = el('button', 'gm-nav-expand', '▸');
        btn.setAttribute('aria-label', 'Toggle ' + n.label);
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          li.classList.toggle('expanded');
        });
        row.appendChild(btn);
      }
      li.appendChild(row);
      if (hasKids) li.appendChild(buildList(n.children, depth + 1));
      ul.appendChild(li);
    });
    return ul;
  }

  // ── Toggle button ──
  var toggle = el('button', 'gm-nav-toggle', '☰ Menu');
  toggle.setAttribute('aria-label', 'Open campaign menu');

  // ── Drawer ──
  var nav = el('nav', 'gm-nav');
  var title = el('a', 'gm-nav-title', 'Campaign Layer');
  title.setAttribute('href', '/campaigns/index.html');
  if (current === 'campaigns-home') title.classList.add('is-current');
  nav.appendChild(title);
  nav.appendChild(el('div', 'gm-nav-sub', 'Behind the Screen'));
  nav.appendChild(buildList(TREE, 1));

  var foot = el('div', 'gm-nav-foot');
  var back = el('a', null, '← Player Site');
  back.setAttribute('href', '/index.html');
  foot.appendChild(back);
  nav.appendChild(foot);

  // ── Scrim ──
  var scrim = el('div', 'gm-nav-scrim');

  function open() { nav.classList.add('open'); scrim.classList.add('open'); }
  function close() { nav.classList.remove('open'); scrim.classList.remove('open'); }
  toggle.addEventListener('click', function () { nav.classList.contains('open') ? close() : open(); });
  scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  document.body.appendChild(toggle);
  document.body.appendChild(scrim);
  document.body.appendChild(nav);
})();
