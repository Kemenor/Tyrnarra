# Sidebar Navigation — Reference Snippet

Every published HTML page should include this sidebar so the menu is consistent site-wide. Paste the three blocks (CSS, HTML, JS) into the page. The page sets `data-page="<slug>"` on its `<body>` tag — the sidebar uses that to highlight the current entry.

The sidebar uses fallback CSS variables, so it works against both Style A (cosmic) and Style B (grounded) without changes.

---

## 1. CSS (inside the page's `<style>` block)

```css
/* ── SITE NAV ── */
.nav-toggle {
  position: fixed; top: 14px; left: 14px; z-index: 200;
  background: rgba(15, 12, 8, 0.85);
  color: var(--gold-bright, var(--gold, #c8a84b));
  border: 1px solid rgba(200, 168, 75, 0.35);
  font-family: 'Cormorant SC', 'Cinzel', serif;
  font-size: 1.1rem; letter-spacing: 0.1em;
  padding: 6px 12px; border-radius: 2px;
  cursor: pointer;
  backdrop-filter: blur(4px);
}
.nav-toggle:hover { background: rgba(40, 28, 12, 0.95); }

.site-nav {
  position: fixed; top: 0; left: 0; bottom: 0;
  width: 280px;
  background: rgba(8, 10, 18, 0.96);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(200, 168, 75, 0.18);
  padding: 64px 20px 30px;
  overflow-y: auto;
  z-index: 190;
  font-family: 'Cormorant Garamond', 'Crimson Pro', Georgia, serif;
  transform: translateX(-100%);
  transition: transform 0.28s ease;
}
.site-nav.open { transform: translateX(0); box-shadow: 4px 0 32px rgba(0,0,0,0.6); }

.site-nav-title {
  display: block;
  font-family: 'Cormorant SC', 'Cinzel', serif;
  font-size: 1.3rem; letter-spacing: 0.22em;
  color: var(--gold-bright, var(--gold, #c8a84b));
  text-decoration: none; text-align: center;
  margin-bottom: 26px; padding-bottom: 14px;
  border-bottom: 1px solid rgba(200, 168, 75, 0.18);
}

.nav-section { margin-bottom: 22px; }
.nav-section-label {
  font-family: 'Cormorant SC', 'Cinzel', serif;
  font-size: 0.62rem; letter-spacing: 0.32em;
  color: var(--gold-dim, #8a6e28);
  margin-bottom: 8px; text-transform: uppercase;
}
.nav-list { list-style: none; padding: 0; margin: 0; }
.nav-list a {
  display: block; padding: 4px 10px;
  color: var(--text-dim, #8a8070);
  text-decoration: none;
  font-size: 0.95rem;
  border-left: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s, background 0.15s;
}
.nav-list a:hover {
  color: var(--text, #d0c8a8);
  border-left-color: rgba(200, 168, 75, 0.4);
  background: rgba(200, 168, 75, 0.05);
}
.nav-list a.is-current {
  color: var(--gold-bright, var(--gold, #c8a84b));
  border-left-color: var(--gold, #c8a84b);
  background: rgba(200, 168, 75, 0.08);
}

.nav-scrim {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 180;
  opacity: 0; pointer-events: none;
  transition: opacity 0.2s;
}
.nav-scrim.open { opacity: 1; pointer-events: auto; }

@media (max-width: 600px) {
  .site-nav { width: 86vw; }
}
```

---

## 2. HTML (immediately after `<body>`)

```html
<button class="nav-toggle" id="navToggle" aria-label="Open navigation" type="button">≡ Menu</button>
<div class="nav-scrim" id="navScrim"></div>

<aside class="site-nav" id="siteNav" aria-label="Site navigation">
  <a href="/index.html" class="site-nav-title">Tyrnarra</a>

  <div class="nav-section">
    <div class="nav-section-label">World &amp; Cosmos</div>
    <ul class="nav-list">
      <li><a href="/tyrnarra-primer.html" data-page="cosmology">Cosmology</a></li>
      <li><a href="/tyrnarra-gods.html"   data-page="gods">The 13 Bound Gods</a></li>
    </ul>
  </div>

  <div class="nav-section">
    <div class="nav-section-label">Talan</div>
    <ul class="nav-list">
      <li><a href="/talan/talan.html"   data-page="talan">Continent Overview</a></li>
      <li><a href="/talan/history.html" data-page="history">History &amp; Eras</a></li>
      <li><a href="/talan/magic.html"   data-page="magic">Magic — Four Schools</a></li>
    </ul>
  </div>

  <div class="nav-section">
    <div class="nav-section-label">Domains</div>
    <ul class="nav-list">
      <li><a href="/talan/domains/vindul/vindul.html"     data-page="vindul">Vindul · Wind</a></li>
      <li><a href="/talan/domains/lautara/lautara.html"   data-page="lautara">Lautara · Commerce</a></li>
      <li><a href="/talan/domains/myrkono/myrkono.html"   data-page="myrkono">Myrkono · Darkness</a></li>
      <li><a href="/talan/domains/floteyn/floteyn.html"   data-page="floteyn">Floteyn · Water</a></li>
      <li><a href="/talan/domains/sumendar/sumendar.html" data-page="sumendar">Sumendar · Fire</a></li>
      <li><a href="/talan/domains/lioaru/lioaru.html"     data-page="lioaru">Lioaru · Time</a></li>
      <li><a href="/talan/domains/brauogi/brauogi.html"   data-page="brauogi">Brauogi · Earth</a></li>
      <li><a href="/talan/domains/ezkudon/ezkudon.html"   data-page="ezkudon">Ezkudon · Knowledge</a></li>
      <li><a href="/talan/domains/egulon/egulon.html"     data-page="egulon">Egulon · Light</a></li>
      <li><a href="/talan/domains/zuzental/zuzental.html" data-page="zuzental">Zuzental · Law</a></li>
      <li><a href="/talan/domains/nashavel/nashavel.html" data-page="nashavel">Nashavel · Chaos</a></li>
      <li><a href="/talan/domains/ehizahar/ehizahar.html" data-page="ehizahar">Ehizahar · Hunt</a></li>
      <li><a href="/talan/domains/askamira/askamira.html" data-page="askamira">Askamira · Freedom</a></li>
    </ul>
  </div>

  <div class="nav-section">
    <div class="nav-section-label">Factions</div>
    <ul class="nav-list">
      <li><a href="/talan/factions/factions.html"          data-page="factions">All Factions</a></li>
      <li><a href="/talan/factions/adventurers-guild.html" data-page="adventurers-guild">Adventurers Guild</a></li>
      <li><a href="/talan/factions/mercenary-guild.html"   data-page="mercenary-guild">Mercenary Guild</a></li>
      <li><a href="/talan/factions/god-churches.html"      data-page="god-churches">God Churches</a></li>
      <li><a href="/talan/factions/remnants.html"          data-page="remnants">Remnants of Corruption</a></li>
    </ul>
  </div>
</aside>
```

---

## 3. JS (at the end of `<body>`, before `</body>`)

```js
(function() {
  var nav = document.getElementById('siteNav');
  var toggle = document.getElementById('navToggle');
  var scrim = document.getElementById('navScrim');
  if (!nav || !toggle) return;

  // Highlight current page from body[data-page]
  var current = document.body.getAttribute('data-page');
  if (current) {
    var link = nav.querySelector('a[data-page="' + current + '"]');
    if (link) link.classList.add('is-current');
  }

  function open()  { nav.classList.add('open');    if (scrim) scrim.classList.add('open'); }
  function close() { nav.classList.remove('open'); if (scrim) scrim.classList.remove('open'); }

  toggle.addEventListener('click', function(e) { e.stopPropagation(); nav.classList.contains('open') ? close() : open(); });
  if (scrim) scrim.addEventListener('click', close);
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape') close(); });
})();
```

---

## How to add the sidebar to a new page

1. Set `<body data-page="<slug>">` where `<slug>` matches one of the `data-page` attributes in the nav HTML above. If your page isn't in the nav (yet), just omit `data-page`.
2. Paste the CSS block inside the page's existing `<style>` (anywhere — the cascade handles it).
3. Paste the HTML block immediately after `<body>`.
4. Paste the JS block at the end of `<body>`, before `</body>`.

---

## When to extend the nav

When a new top-level page is added (a new domain, a new faction, a new world-level reference), update this file *and* the snippet inlined into every page. Until we have a build step, this means find-and-replace across pages. Acceptable while the site is small; revisit if it gets painful.
