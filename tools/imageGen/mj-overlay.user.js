// ==UserScript==
// @name         Tyrnarra NPC helper for Midjourney
// @namespace    tyrnarra
// @version      1.0
// @description  Serve <slug>.set.json prompts into the Midjourney prompt bar, and save chosen images back into the spec's folder under the right name.
// @match        https://www.midjourney.com/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @connect      localhost
// @run-at       document-idle
// ==/UserScript==

/*
 * The GM drives Midjourney; this only removes the tedium around it. It fills
 * the prompt bar and it saves images. It never presses generate, never clicks
 * --oref, never navigates. Those stay manual on purpose: they are the judgment
 * steps, and unattended clicking is what a ToS-forbidden bot looks like.
 *
 * Needs mj_server.py running (python3 tools/imageGen/mj_server.py).
 *
 * Flow it supports:
 *   1. pick an NPC, click the anchor shot -> prompt bar filled -> you press enter
 *   2. click --oref on the grid image you like (Midjourney's own button)
 *   3. click the next shot -> prompt bar filled -> enter
 *   4. click the small down-arrow on any image -> saved as <file>.<real ext>
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

  // ------------------------------------------------------------------- saving
  // Derive the ORIGINAL from the job link rather than scraping the <img>: the
  // rendered src is a 640px webp thumbnail (0_0_640_N.webp), while
  // /<uuid>/0_<index>.png is the full-resolution image.
  function fullResFrom(anchor) {
    const m = anchor.getAttribute('href').match(/\/jobs\/([0-9a-f-]+)\?index=(\d+)/i);
    return m ? `https://cdn.midjourney.com/${m[1]}/0_${m[2]}.png` : null;
  }

  // The BYTES have to be read here, in the page. cdn.midjourney.com serves a
  // page fetch but answers a server-side one with 403, so mj_server cannot
  // download the image itself; it is handed the bytes base64.
  // Note the bare fetch(url): adding credentials:'include' turns a working
  // cross-origin read into "Failed to fetch", because the CDN does not allow
  // credentialed requests. Do not add it.
  async function blobToB64(blob) {
    const buf = new Uint8Array(await blob.arrayBuffer());
    let s = '';
    for (let i = 0; i < buf.length; i += 0x8000) {        // chunked: a 2 MB
      s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
    }                                                     // spread would blow
    return btoa(s);                                       // the call stack
  }

  async function saveImage(anchor) {
    if (!state.slug || !state.shot) { toast('pick an NPC and a shot first', true); return; }
    const url = fullResFrom(anchor);
    if (!url) { toast('could not read the job id', true); return; }
    toast(`saving as ${state.shot}...`);
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error('CDN returned ' + res.status);
      const data = await blobToB64(await res.blob());
      const r = await api('POST', '/save', { slug: state.slug, shot: state.shot, data });
      if (r.error) throw new Error(r.error);
      toast('saved ' + r.name);
    } catch (e) { toast(e.message, true); }
  }

  // Each grid image gets a small save button. A MutationObserver because the
  // feed is virtualised: rows mount and unmount as you scroll, so a one-shot
  // pass over the DOM decorates only what happened to be on screen at load.
  const seen = new WeakSet();
  function decorate() {
    document.querySelectorAll('a[href^="/jobs/"]').forEach(a => {
      if (seen.has(a) || !a.querySelector('img')) return;
      seen.add(a);
      const btn = document.createElement('button');
      btn.textContent = '⤓';
      btn.title = 'Save into the NPC spec folder';
      btn.style.cssText = 'position:absolute;right:6px;bottom:6px;z-index:40;' +
        'width:26px;height:26px;border-radius:6px;border:1px solid #0008;' +
        'background:#000a;color:#fff;font-size:14px;line-height:1;cursor:pointer;' +
        'opacity:.75';
      btn.onmouseenter = () => btn.style.opacity = '1';
      btn.onmouseleave = () => btn.style.opacity = '.75';
      btn.onclick = e => { e.preventDefault(); e.stopPropagation(); saveImage(a); };
      const host = a.parentElement || a;
      if (getComputedStyle(host).position === 'static') host.style.position = 'relative';
      host.appendChild(btn);
    });
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
        Click a shot to fill the prompt bar. Use Midjourney's own
        <i>--oref</i> button on your chosen anchor before the ref shots.
        Then ⤓ on an image saves it as the selected shot, full-res, into the spec's folder.
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
      b.innerHTML = `<b>${s.key}</b> <span style="opacity:.55">${tag} · ${s.ar}</span>`;
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
    decorate();
    new MutationObserver(decorate).observe(document.body,
      { childList: true, subtree: true });
  })();
})();
