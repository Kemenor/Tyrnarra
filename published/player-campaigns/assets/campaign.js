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

     Portraits:    <img class="person-face" data-scene="…" data-scene-label="…">
                   inside a .person-card. Clicking it (or Enter / Space) opens
                   the data-scene picture full-size, NOT a bigger copy of the
                   avatar: the face is already on the card, the in-scene shot
                   is the thing worth revealing. Without data-scene it falls
                   back to opening the avatar itself. Esc, the close button or
                   a click on the overlay dismisses it.

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

    /* ── Portrait lightbox ── */
    if (e.target.closest('.pc-lightbox')) { closeLightbox(); return; }
    var face = e.target.closest('.person-face');
    if (face) { openLightbox(face); return; }

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

  /* ── Lightbox: a cast portrait opens full-size ──
     One overlay, built on first use. The avatars are made focusable here
     rather than in page markup, so a portrait opens from the keyboard too. */
  var lbox = null, lbOpener = null;

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { closeLightbox(); return; }
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var t = e.target;
    if (t && t.closest && t.closest('.person-face')) { e.preventDefault(); openLightbox(t); }
  });

  function buildLightbox() {
    if (lbox) return lbox;
    lbox = document.createElement('div');
    lbox.className = 'pc-lightbox';
    lbox.setAttribute('role', 'dialog');
    lbox.setAttribute('aria-modal', 'true');
    lbox.hidden = true;
    lbox.innerHTML = '<button class="pc-lightbox-close" aria-label="Close portrait">\u2715</button>'
                   + '<figure><img alt=""><figcaption></figcaption></figure>';
    document.body.appendChild(lbox);
    return lbox;
  }

  function openLightbox(img) {
    var box = buildLightbox();
    var card = img.closest('.person-card');
    var nameEl = card ? card.querySelector('.person-name') : null;
    var name = nameEl ? nameEl.textContent : (img.alt || '');
    // The avatar is the doorway to the in-scene picture, which is the shot a
    // player never otherwise sees: the card already shows the face. An avatar
    // with no scene wired falls back to opening itself.
    var scene = img.getAttribute('data-scene');
    var label = img.getAttribute('data-scene-label');
    var big = box.querySelector('img');
    big.src = scene || img.currentSrc || img.src;
    big.alt = scene && label ? name + ', ' + label.toLowerCase() : (img.alt || '');
    box.querySelector('figcaption').innerHTML = esc(name)
      + (scene && label ? ' <span class="pc-lightbox-where">' + esc(label) + '</span>' : '');
    box.setAttribute('aria-label', big.alt || 'Portrait');
    lbOpener = img;
    box.hidden = false;
    document.body.classList.add('pc-lightbox-open');
    box.querySelector('.pc-lightbox-close').focus();
  }

  function closeLightbox() {
    if (!lbox || lbox.hidden) return;
    lbox.hidden = true;
    document.body.classList.remove('pc-lightbox-open');
    if (lbOpener) { lbOpener.focus(); lbOpener = null; }
  }

  /* Seed aria-expanded so assistive tech reads correct state at load. */
  function initAria() {
    var btns = document.querySelectorAll('.quest-head, .reveal-toggle');
    for (var i = 0; i < btns.length; i++) {
      if (!btns[i].hasAttribute('aria-expanded')) btns[i].setAttribute('aria-expanded', 'false');
    }
    var faces = document.querySelectorAll('.person-face');
    for (var j = 0; j < faces.length; j++) {
      faces[j].tabIndex = 0;
      faces[j].setAttribute('role', 'button');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAria);
  } else {
    initAria();
  }
})();
