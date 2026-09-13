// ==UserScript==
// @name         Tyrnarra NPC helper for Midjourney
// @namespace    tyrnarra
// @version      1.2
// @description  Serve <slug>.set.json prompts into the Midjourney prompt bar.
// @match        https://www.midjourney.com/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// ==/UserScript==

/*
 * The GM drives Midjourney; this only removes the tedium around it. It fills
 * the prompt bar, and nothing else. It never presses generate, never clicks
 * --oref, never navigates. Those stay manual on purpose: they are the judgment
 * steps, and unattended clicking is what a ToS-forbidden bot looks like.
 *
 * Save-back was built and then REMOVED (2026-09-13): a button drawn on each
 * grid image sat on top of the zoom view. The mechanism worked and is in git
 * (and mj_server's /save endpoint is still live), so re-wiring it to a control
 * that does not overlap the image is a small job, not a rebuild. What it needs:
 * the full-res image is cdn.midjourney.com/<uuid>/0_<index>.png, derived from
 * the job link; the bytes must be fetched IN THE PAGE with a bare fetch (the
 * CDN 403s a server-side fetch, and credentials:'include' breaks CORS) and
 * posted to /save base64.
 *
 * Needs mj_server.py running (python3 tools/imageGen/mj_server.py).
 *
 * Flow it supports (V8.2):
 *   1. pick an NPC, click the anchor shot -> prompt bar filled -> you press enter
 *   2. on the grid image you like: Quick Edit, which attaches it to the prompt
 *      with the role "Attach to prompt"
 *   3. click the next shot -> prompt bar filled -> enter
 *
 * Do NOT use Omni Reference (--oref) on V8.2. It still appears on older jobs
 * and it still works, but a prompt carrying --oref renders in V7: the anchor
 * would come back as 8.2 and the ref shots as 7, and nothing in the UI says so.
 * The Edit Model ("Attach to prompt", up to 4 images) replaced it.
 */

(function () {
  'use strict';

  const API = 'http://127.0.0.1:8765';
  const state = { slug: null, shot: null, data: null, style: 'none' };

  // ---------------------------------------------------------------- transport
  // GM_xmlhttpRequest rather than fetch. A plain fetch does work today, because
  // Chrome counts http://127.0.0.1 as a trustworthy origin and does not treat
  // it as mixed content (measured 2026-09-13), and mj_server sends permissive
  // CORS headers. GM_xmlhttpRequest is used anyway because it depends on
  // neither of those: it is outside the page's CORS and mixed-content rules
  // entirely, so a stricter Chrome or a tightened Midjourney CSP cannot break
  // the panel.
  function api(method, path, body) {
    return new Promise((resolve, reject) => {
      GM_xmlhttpRequest({
        method, url: API + path,
        headers: { 'Content-Type': 'application/json' },
        data: body ? JSON.stringify(body) : undefined,
        onload: r => {
          try { resolve(JSON.parse(r.responseText)); }
          catch (e) { reject(new Error('bad response: ' + r.responseText.slice(0, 120))); }
        },
        onerror: () => reject(new Error('mj_server unreachable - is it running?')),
      });
    });
  }

  // ------------------------------------------------------------------ prompt
  // The prompt bar is a React-controlled <textarea>. Assigning .value directly
  // updates the DOM but not React's internal state, so the text vanishes on the
  // next render and submitting sends an empty prompt. Going through the native
  // setter and dispatching an input event is what makes React accept it.
  function fillPrompt(text) {
    const ta = document.querySelector('textarea[placeholder*="imagine" i]')
            || document.querySelector('textarea');
    if (!ta) { toast('prompt bar not found', true); return; }
    const setter = Object.getOwnPropertyDescriptor(
      window.HTMLTextAreaElement.prototype, 'value').set;
    setter.call(ta, text);
    ta.dispatchEvent(new Event('input', { bubbles: true }));
    ta.focus();
  }

  // --------------------------------------------------------------------- panel
  const panel = document.createElement('div');
  panel.style.cssText = 'position:fixed;left:12px;bottom:12px;z-index:99999;' +
    'width:260px;background:#14110dee;color:#d0c8a8;border:1px solid #c8900a55;' +
    'border-radius:10px;font:12px/1.4 system-ui,sans-serif;padding:10px;' +
    'box-shadow:0 6px 24px #000a';
  panel.innerHTML = `
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:8px">
      <b style="color:#f0b020;letter-spacing:.04em">TYRNARRA</b>
      <span id="ty-status" style="margin-left:auto;opacity:.7">…</span>
      <button id="ty-min" style="background:none;border:0;color:inherit;cursor:pointer;font-size:14px">–</button>
    </div>
    <div id="ty-body">
      <select id="ty-slug" style="width:100%;margin-bottom:8px;background:#0f0c08;
        color:inherit;border:1px solid #c8900a44;border-radius:6px;padding:4px"></select>
      <div id="ty-shots" style="display:flex;flex-direction:column;gap:4px"></div>
      <label style="display:flex;align-items:center;gap:6px;margin-top:8px;opacity:.8">
        <input type="checkbox" id="ty-style"> add the house style sentence
      </label>
      <div style="margin-top:8px;opacity:.6;font-size:11px">
        Click a shot to fill the prompt bar. For the ref shots, first
        <b>Quick Edit</b> your chosen anchor so it attaches with the role
        <i>Attach to prompt</i>. Do not use <i>--oref</i>: it renders in V7.
        Saving is manual for now.
      </div>
    </div>`;
  document.body.appendChild(panel);
  const $ = id => panel.querySelector(id);

  $('#ty-min').onclick = () => {
    const b = $('#ty-body');
    b.style.display = b.style.display === 'none' ? '' : 'none';
    $('#ty-min').textContent = b.style.display === 'none' ? '+' : '–';
  };

  $('#ty-style').onchange = e => {
    // Off by default: the Midjourney personalization profile already carries
    // the house look, and the long style sentence competes with it.
    state.style = e.target.checked ? 'digital' : 'none';
    if (state.slug) loadSlug(state.slug);
  };

  let toastEl;
  function toast(msg, bad) {
    clearTimeout(toastEl && toastEl._t);
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.style.cssText = 'position:fixed;left:12px;bottom:200px;z-index:99999;' +
        'padding:6px 10px;border-radius:6px;font:12px system-ui;max-width:260px';
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.style.background = bad ? '#5a1a1aee' : '#1d2a16ee';
    toastEl.style.color = bad ? '#ffb4b4' : '#cfe8b8';
    toastEl.style.display = '';
    toastEl._t = setTimeout(() => toastEl.style.display = 'none', 4000);
  }

  function renderShots() {
    const box = $('#ty-shots');
    box.innerHTML = '';
    (state.data ? state.data.shots : []).forEach(s => {
      const b = document.createElement('button');
      const tag = s.key === state.data.anchor ? 'anchor' : s.mode;
      const warn = s.long ? ' style="color:#ff9c6e"' : ' style="opacity:.55"';
      b.innerHTML = `<b>${s.key}</b> <span${warn}>${tag} · ${s.ar} · ${s.words}w`
                  + `${s.long ? ' LONG' : ''}</span>`;
      b.style.cssText = 'text-align:left;background:#0f0c08;color:inherit;cursor:pointer;' +
        'border:1px solid ' + (state.shot === s.key ? '#f0b020' : '#c8900a33') +
        ';border-radius:6px;padding:5px 7px';
      b.onclick = () => { state.shot = s.key; fillPrompt(s.prompt); renderShots();
                          toast('prompt bar filled: ' + s.key); };
      box.appendChild(b);
    });
  }

  async function loadSlug(slug) {
    state.slug = slug; state.shot = null;
    state.data = await api('GET', '/prompts?slug=' + encodeURIComponent(slug)
                           + '&style=' + state.style);
    renderShots();
  }

  (async function init() {
    try {
      const specs = await api('GET', '/specs');
      $('#ty-status').textContent = specs.length + ' specs';
      const sel = $('#ty-slug');
      specs.forEach(s => sel.add(new Option(s.slug, s.slug)));
      sel.onchange = () => loadSlug(sel.value);
      if (specs.length) await loadSlug(specs[0].slug);
    } catch (e) {
      $('#ty-status').textContent = 'offline';
      toast(e.message, true);
    }
  })();
})();
