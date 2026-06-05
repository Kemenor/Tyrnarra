/* ───────────────────────────────────────────────────────────────
   gm.js: shared interactions for the campaign / GM layer.
   Loaded with `defer` by every page under /campaigns/.

   All behaviour is wired by delegation on click, so pages only need
   the right classes / data-attributes (no inline onclick required):

     Tabs:      <button class="gm-tab-btn" data-target="panel-id">…</button>
                <div class="gm-panel" id="panel-id">…</div>
                (first .gm-tab-btn / .gm-panel in a group start active)

     Secrets:   <div class="gm-secret">
                  <button class="gm-secret-toggle">⚿ …</button>
                  <div class="gm-secret-body">…</div>
                </div>

     NPC cards: <div class="npc-card"> … </div>   (whole card toggles .open)
     Levels:    <div class="level-card"><div class="level-header">…</div>…</div>
     Rooms:     <div class="room-cell" data-room="key">…</div>  +  a
                <div id="roomDetail"> target; room data on window.GM_ROOMS[key]

     Battlemap: <div class="map-wrap"> <img …>
                  <button class="map-hot" data-area="key" style="left/top/width/height %">
                    <span class="hot-num">1</span></button> …
                </div>
                <button class="map-toggle">Hide areas</button>
                <div class="map-detail" id="mapDetail">…</div>
                area notes on window.GM_MAP_AREAS[key] = { n: title, t: htmlNotes }
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  document.addEventListener('click', function (e) {
    // ── Tabs ──────────────────────────────────────────────
    var tab = e.target.closest('.gm-tab-btn');
    if (tab && tab.dataset.target) {
      var tabBar = tab.parentElement;
      tabBar.querySelectorAll('.gm-tab-btn').forEach(function (b) { b.classList.remove('active'); });
      tab.classList.add('active');
      var panel = document.getElementById(tab.dataset.target);
      if (panel) {
        var scope = panel.parentElement;
        scope.querySelectorAll(':scope > .gm-panel').forEach(function (p) { p.classList.remove('active'); });
        panel.classList.add('active');
      }
      return;
    }

    // ── Secret reveal ─────────────────────────────────────
    var sec = e.target.closest('.gm-secret-toggle');
    if (sec) {
      var box = sec.closest('.gm-secret');
      if (box) box.classList.toggle('open');
      return;
    }

    // ── Level cards ───────────────────────────────────────
    var lvl = e.target.closest('.level-header');
    if (lvl) {
      var card = lvl.closest('.level-card');
      if (card) card.classList.toggle('open');
      return;
    }

    // ── Room cells (floorplan detail panel) ───────────────
    var cell = e.target.closest('.room-cell');
    if (cell && cell.dataset.room && window.GM_ROOMS) {
      var data = window.GM_ROOMS[cell.dataset.room];
      var target = document.getElementById('roomDetail');
      if (data && target) {
        document.querySelectorAll('.room-cell.active').forEach(function (c) { c.classList.remove('active'); });
        cell.classList.add('active');
        target.innerHTML = renderRoom(data);
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      return;
    }

    // ── Battlemap hotspots (notes on window.GM_MAP_AREAS, target #mapDetail) ──
    var hot = e.target.closest('.map-hot');
    if (hot && hot.dataset.area && window.GM_MAP_AREAS) {
      var area = window.GM_MAP_AREAS[hot.dataset.area];
      var mdetail = document.getElementById('mapDetail');
      if (area && mdetail) {
        document.querySelectorAll('.map-hot.active').forEach(function (x) { x.classList.remove('active'); });
        hot.classList.add('active');
        mdetail.innerHTML = '<div class="section-title">' + (area.n || '') + '</div><div class="prose">' + (area.t || '') + '</div>';
        mdetail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      return;
    }

    // ── Battlemap "hide areas" toggle ─────────────────────────
    var mtoggle = e.target.closest('.map-toggle');
    if (mtoggle) {
      var mscope = mtoggle.closest('.section') || document;
      var mwrap = mscope.querySelector('.map-wrap');
      if (mwrap) {
        var hidden = mwrap.classList.toggle('hide-areas');
        mtoggle.textContent = hidden ? 'Show areas' : 'Hide areas';
      }
      return;
    }

    // ── NPC cards (expand) ────────────────────────────────
    var npc = e.target.closest('.npc-card');
    if (npc) {
      if (e.target.closest('a')) return; // let links work
      npc.classList.toggle('open');
    }
  });

  function esc(s) { return String(s == null ? '' : s); }

  function renderRoom(r) {
    var tags = (r.tags || []).map(function (t) { return '<span class="stat-pill">' + esc(t) + '</span>'; }).join(' ');
    var details = (r.details || []).map(function (d) { return '<li>' + esc(d) + '</li>'; }).join('');
    var read = r.readAloud ? '<div class="read-aloud"><div class="read-aloud-label">Read Aloud</div><div class="read-aloud-text">' + esc(r.readAloud) + '</div></div>' : '';
    var desc = r.desc ? '<div class="gm-note"><div class="gm-note-label">Description</div><div class="gm-note-text">' + esc(r.desc) + '</div></div>' : '';
    var list = details ? '<div class="exp-label">Notable Details</div><ul class="trait-list">' + details + '</ul>' : '';
    return '<div class="statblock-name">' + esc(r.name) + '</div>'
         + '<div class="statblock-meta">' + esc(r.floor || '') + '</div>'
         + (tags ? '<div class="pill-row" style="margin-bottom:12px">' + tags + '</div>' : '')
         + read + desc + list;
  }
})();
