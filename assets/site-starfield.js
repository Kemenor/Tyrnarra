/* ───────────────────────────────────────────────────────────────
   site-starfield.js: generates the ambient star field for the
   Style A "cosmic" pages. Looks for the canonical placeholder:

     <div class="starfield" id="starfield" data-stars="180"></div>

   data-stars is optional (default 180). If the placeholder is
   absent, the script no-ops, so it is safe to include on any page.

   The .star + .starfield CSS and the starPulse keyframe live in
   /assets/style-a.css.
   ─────────────────────────────────────────────────────────────── */

(function () {
  'use strict';
  var sf = document.getElementById('starfield');
  if (!sf) return;
  var count = parseInt(sf.getAttribute('data-stars'), 10);
  if (!count || count < 1) count = 180;
  for (var i = 0; i < count; i++) {
    var s = document.createElement('div');
    s.className = 'star';
    var size = Math.random() * 2 + 0.5;
    s.style.cssText =
      'width:' + size + 'px;height:' + size + 'px;' +
      'top:' + (Math.random() * 100) + '%;left:' + (Math.random() * 100) + '%;' +
      '--d:' + (Math.random() * 4 + 2) + 's;' +
      '--delay:-' + (Math.random() * 6) + 's;';
    sf.appendChild(s);
  }
})();
