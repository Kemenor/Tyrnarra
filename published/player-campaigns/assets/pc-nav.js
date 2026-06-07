/* ───────────────────────────────────────────────────────────────
   pc-nav.js: left-side menu for the PLAYER-facing campaign layer.
   Loaded with `defer` by every page under /player-campaigns/.

   This layer carries its OWN menu and does NOT load site-nav.js: the
   world/setting menu and the campaigns menu are separate. A foot
   button crosses back to the setting; the setting nav has the mirror
   button crossing here. (The GM /gm-notes/ layer is deliberately NOT
   linked from any player-facing menu.)

   Single source of truth for the campaigns menu is TREE below.
   Each page declares its location with <body data-page="<slug>">;
   on load the drawer auto-expands the ancestor chain of that slug.

   Tree shape (any depth): { slug, label, href|null, children:[…] }
   An entry with href:null renders as a non-link group label.
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  // ── Favicon + manifest (shared with the public site) ─────────
  // This layer carries its own menu, so it does not load site-nav.js;
  // mirror its favicon injection here so campaign pages get the full
  // icon set, not just the root /favicon.ico baseline. Files live at
  // the site root.
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
    { slug: 'ff-hub', label: 'The Furrious Five', href: '/player-campaigns/furrious-five/furrious-five.html', children: [
      { slug: 'ff-wayward-compass', label: 'Wayward Compass · Quest Board', href: '/player-campaigns/furrious-five/wayward-compass.html', children: [] },
      { slug: 'ff-millhaven',       label: 'Millhaven',                      href: '/player-campaigns/furrious-five/millhaven.html',       children: [] },
      { slug: 'ff-low-span',        label: 'The Low Span',                   href: '/player-campaigns/furrious-five/low-span.html',        children: [] }
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
    var ul = el('ul', depth === 1 ? 'pc-nav-list' : 'pc-nav-sublist');
    nodes.forEach(function (n) {
      var li = el('li', 'pc-nav-item');
      li.setAttribute('data-depth', depth);
      var hasKids = n.children && n.children.length;
      if (openChain[n.slug]) li.classList.add('expanded');

      var row = el('div', 'pc-nav-row');
      if (n.href) {
        var a = el('a', null, n.label);
        a.setAttribute('href', n.href);
        if (n.slug === current) a.classList.add('is-current');
        row.appendChild(a);
      } else {
        row.appendChild(el('span', 'pc-nav-grouplabel', n.label));
      }
      if (hasKids) {
        var btn = el('button', 'pc-nav-expand', '▸');
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
  var toggle = el('button', 'pc-nav-toggle', '☰ Campaigns');
  toggle.setAttribute('aria-label', 'Open campaigns menu');

  // ── Drawer ──
  var nav = el('nav', 'pc-nav');
  var title = el('a', 'pc-nav-title', 'Campaigns');
  title.setAttribute('href', '/player-campaigns/index.html');
  if (current === 'campaigns') title.classList.add('is-current');
  nav.appendChild(title);

  // Scrollable middle: title (above) and foot (below) stay pinned.
  var scroll = el('div', 'pc-nav-scroll');
  scroll.appendChild(el('div', 'pc-nav-sub', 'Player Companions'));
  scroll.appendChild(buildList(TREE, 1));
  nav.appendChild(scroll);

  var foot = el('div', 'pc-nav-foot');
  var back = el('a', null, '← The World · Setting');
  back.setAttribute('href', '/setting/index.html');
  foot.appendChild(back);
  nav.appendChild(foot);

  // ── Scrim ──
  var scrim = el('div', 'pc-nav-scrim');

  function open() { nav.classList.add('open'); scrim.classList.add('open'); }
  function close() { nav.classList.remove('open'); scrim.classList.remove('open'); }
  toggle.addEventListener('click', function () { nav.classList.contains('open') ? close() : open(); });
  scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  document.body.appendChild(toggle);
  document.body.appendChild(scrim);
  document.body.appendChild(nav);
})();
