/* ───────────────────────────────────────────────────────────────
   campaign.js: shared interactions for the player-facing campaign
   layer (/player-campaigns/). Loaded with `defer`.

   All behaviour is click-delegated, so pages only need the right
   classes / data-attributes (no inline onclick required):

     Quest board:  <div class="quest-pin">
                      <button class="quest-head" aria-expanded="false" aria-controls="id">…</button>
                      <div class="quest-detail" id="id">…</div>
                    </div>

     Room map:     <div class="room-cell" data-room="key">…</div>   (clickable)
                   <div class="room-cell locked">…</div>            (no data-room: inert)
                   <div id="roomDetail"></div>                       detail target
                   room data on window.CAMPAIGN_ROOMS[key]:
                     { name, floor, tags:[], read, desc, details:[] }

     Reveal:       <div class="reveal">
                      <button class="reveal-toggle">◈ …</button>
                      <div class="reveal-body">…</div>
                    </div>
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  function esc(s) { return String(s == null ? '' : s); }

  function renderRoom(r) {
    var read = r.read
      ? '<div class="rc-read"><div class="rc-read-label">As You Walk In</div><div class="rc-read-text">' + esc(r.read) + '</div></div>'
      : '';
    var desc = r.desc ? '<div class="rc-desc">' + esc(r.desc) + '</div>' : '';
    var details = (r.details || []).map(function (d) { return '<li>' + esc(d) + '</li>'; }).join('');
    var list = details ? '<ul class="rc-list">' + details + '</ul>' : '';
    return '<div class="room-card">'
         + '<div class="rc-name">' + esc(r.name) + '</div>'
         + '<div class="rc-floor">' + esc(r.floor || '') + '</div>'
         + read + desc + list
         + '</div>';
  }

  document.addEventListener('click', function (e) {

    /* ── Quest board: expand a pinned notice ── */
    var head = e.target.closest('.quest-head');
    if (head) {
      var pin = head.closest('.quest-pin');
      if (pin) {
        var open = pin.classList.toggle('open');
        head.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
      return;
    }

    /* ── Reveal (rumour / popular belief) ── */
    var rt = e.target.closest('.reveal-toggle');
    if (rt) {
      var box = rt.closest('.reveal');
      if (box) {
        var rOpen = box.classList.toggle('open');
        rt.setAttribute('aria-expanded', rOpen ? 'true' : 'false');
      }
      return;
    }

    /* ── Room map: render a room's detail ── */
    var cell = e.target.closest('.room-cell');
    if (cell && cell.dataset.room && window.CAMPAIGN_ROOMS) {
      var data = window.CAMPAIGN_ROOMS[cell.dataset.room];
      var target = document.getElementById('roomDetail');
      if (data && target) {
        var prev = document.querySelector('.room-cell.active');
        if (prev) prev.classList.remove('active');
        cell.classList.add('active');
        target.innerHTML = renderRoom(data);
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      return;
    }
  });

  /* Seed aria-expanded so assistive tech reads correct state at load. */
  function initAria() {
    var btns = document.querySelectorAll('.quest-head, .reveal-toggle');
    for (var i = 0; i < btns.length; i++) {
      if (!btns[i].hasAttribute('aria-expanded')) btns[i].setAttribute('aria-expanded', 'false');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAria);
  } else {
    initAria();
  }
})();
