// ==UserScript==
// @name         Tyrnarra NPC helper for Midjourney
// @namespace    tyrnarra
// @version      1.6
// @description  Serve <slug>.set.json prompts into the Midjourney prompt bar, and save the open image into the spec's folder.
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
 * Save-back lives in the PANEL, not on the image. A first version drew a
 * button on every grid thumbnail and it sat on top of the zoom view; the panel
 * is out of the way and needs no per-image decoration, so no MutationObserver
 * and no fighting the virtualised feed. It reads whichever image is open:
 * clicking a thumbnail pushes /jobs/<uuid>?index=N, so the URL is the source of
 * truth for "which image".
 *
 * Needs mj_server.py running (python3 tools/imageGen/mj_server.py).
 *
 * Flow it supports (V8.2):
 *   1. pick an NPC, click the anchor shot -> prompt bar filled -> you press enter
 *   2. on the grid image you like: Quick Edit, which attaches it to the prompt
 *      with the role "Attach to prompt"
 *   3. click the next shot -> prompt bar filled -> enter
 *   4. click the image you want, then "save as ..." in the panel
 *
 * Do NOT use Omni Reference (--oref) on V8.2. It still appears on older jobs
 * and it still works, but a prompt carrying --oref renders in V7: the anchor
 * would come back as 8.2 and the ref shots as 7, and nothing in the UI says so.
 * The Edit Model ("Attach to prompt", up to 4 images) replaced it.
 */

(function () {
  'use strict';

  const API = 'http://127.0.0.1:8765';
  const MEM = 'tyrnarra-mj-selection';

  // Remember which NPC and shot were selected. Without this the panel falls
  // back to the first spec the server lists, and the server lists them by FILE
  // MODIFICATION TIME - so the default silently moves to whichever spec was
  // edited last. Reload the page mid-session and you can be pointed at a
  // different character while believing you are still on the old one, which is
  // exactly the kind of mistake that ends with one NPC's art saved under
  // another's name.
  const remember = () => {
    try { localStorage.setItem(MEM, JSON.stringify({ slug: state.slug, shot: state.shot })); }
    catch (e) { /* private window, or storage disabled: selection just will not persist */ }
  };
  const recall = () => {
    try { return JSON.parse(localStorage.getItem(MEM)) || {}; } catch (e) { return {}; }
  };
  const state = { slug: null, shot: null, data: null, style: 'none',
                specs: [], showDone: false };

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
  // Which image is open, from the URL. Clicking a thumbnail pushes
  // /jobs/<uuid>?index=N, so this is authoritative and costs no DOM scraping.
  function currentJob() {
    const m = location.pathname.match(/^\/jobs\/([0-9a-f-]+)/i);
    if (!m) return null;
    const idx = new URLSearchParams(location.search).get('index') || '0';
    return { id: m[1], index: idx };
  }

  // Full-res, derived from the job id: the rendered <img> is a 640px webp
  // thumbnail (0_0_640_N.webp), the original is /<uuid>/0_<index>.png.
  const fullResUrl = j => `https://cdn.midjourney.com/${j.id}/0_${j.index}.png`;

  async function blobToB64(blob) {
    const buf = new Uint8Array(await blob.arrayBuffer());
    let out = '';
    for (let i = 0; i < buf.length; i += 0x8000) {        // chunked: a spread
      out += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
    }                                                     // over 2 MB would
    return btoa(out);                                     // blow the stack
  }

  async function saveOpenImage() {
    const job = currentJob();
    if (!job) { toast('open an image first', true); return; }
    if (!state.shot) { toast('pick a shot first', true); return; }
    toast(`saving as ${state.shot}...`);
    try {
      // The bytes MUST be read here in the page: cdn.midjourney.com serves a
      // page fetch but answers a server-side one with 403. And the fetch must
      // be bare - credentials:'include' turns it into "Failed to fetch".
      const res = await fetch(fullResUrl(job));
      if (!res.ok) throw new Error('CDN returned ' + res.status);
      const data = await blobToB64(await res.blob());
      const r = await api('POST', '/save', { slug: state.slug, shot: state.shot, data });
      if (r.error) throw new Error(r.error);
      toast('saved ' + r.name);
      // Re-read so the shot gets its tick and, if that was the last one, the
      // set drops out of the list on its own.
      state.data = await api('GET', '/prompts?slug='
                             + encodeURIComponent(state.slug)
                             + '&style=' + state.style);
      renderShots();
      await refreshSpecs();
      if (state.data.done) toast(`${state.slug} complete`);
    } catch (e) { toast(e.message, true); }
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
      <button id="ty-save" style="width:100%;margin-top:8px;padding:6px;
        background:#0f0c08;color:inherit;border:1px solid #c8900a55;
        border-radius:6px;cursor:pointer">save</button>
      <label style="display:flex;align-items:center;gap:6px;margin-top:8px;opacity:.8">
        <input type="checkbox" id="ty-style"> add the house style sentence
      </label>
      <label style="display:flex;align-items:center;gap:6px;margin-top:4px;opacity:.8">
        <input type="checkbox" id="ty-done"> show finished sets
      </label>
      <div style="margin-top:8px;opacity:.6;font-size:11px">
        Click a shot to fill the prompt bar. For the ref shots, first
        <b>Quick Edit</b> your chosen anchor so it attaches with the role
        <i>Attach to prompt</i>. Do not use <i>--oref</i>: it renders in V7.
        Click the image you want, then <b>save</b>.
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

  $('#ty-save').onclick = saveOpenImage;

  $('#ty-done').onchange = e => { state.showDone = e.target.checked; fillSelect(); };

  // The site is a single-page app, so the URL changes without a load event.
  // Polling beats patching history.pushState: it also catches back/forward and
  // anything the app does internally, and twice a second is free.
  function refreshSaveButton() {
    const btn = $('#ty-save');
    const job = currentJob();
    const shot = state.data && state.data.shots.find(x => x.key === state.shot);
    const ready = !!(job && shot);
    btn.disabled = !ready;
    btn.style.opacity = ready ? '1' : '.45';
    btn.style.cursor = ready ? 'pointer' : 'default';
    btn.textContent = !job ? 'save (open an image)'
                    : !shot ? 'save (pick a shot)'
                    : `\u2913 save as ${shot.file}`;
  }
  setInterval(refreshSaveButton, 500);

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
      const tick = s.saved ? '<span style="color:#7fd17f">\u2713</span> ' : '';
      b.innerHTML = `${tick}<b>${s.key}</b> <span${warn}>${tag} · ${s.ar} · `
                  + `${s.words}w${s.long ? ' LONG' : ''}</span>`;
      b.style.cssText = 'text-align:left;background:#0f0c08;color:inherit;cursor:pointer;' +
        'border:1px solid ' + (state.shot === s.key ? '#f0b020' : '#c8900a33') +
        ';border-radius:6px;padding:5px 7px';
      b.onclick = () => { state.shot = s.key; fillPrompt(s.prompt); renderShots();
                          refreshSaveButton(); remember();
                          toast('prompt bar filled: ' + s.key); };
      box.appendChild(b);
    });
  }

  // A set with every shot on disk leaves the list. Derived from the files,
  // so it happens by itself the moment the last image is saved and reverses
  // itself if one is deleted; there is nothing to keep in sync by hand.
  function fillSelect() {
    const sel = $('#ty-slug');
    const show = state.specs.filter(x => state.showDone || !x.done
                                         || x.slug === state.slug);
    sel.innerHTML = '';
    show.forEach(x => sel.add(new Option(
      x.done ? `\u2713 ${x.slug}` : `${x.slug} (${x.saved}/${x.total})`, x.slug)));
    if (state.slug) sel.value = state.slug;
    const hidden = state.specs.filter(x => x.done).length;
    $('#ty-status').textContent = state.showDone
      ? `${state.specs.length} specs`
      : `${state.specs.length - hidden} open` + (hidden ? ` · ${hidden} done` : '');
  }

  async function refreshSpecs() {
    state.specs = await api('GET', '/specs');
    fillSelect();
  }

  async function loadSlug(slug, keepShot) {
    state.slug = slug;
    if (!keepShot) state.shot = null;
    remember();
    state.data = await api('GET', '/prompts?slug=' + encodeURIComponent(slug)
                           + '&style=' + state.style);
    renderShots();
  }

  (async function init() {
    try {
      // fillSelect owns the list and the counter, and reads state.specs, so
      // this has to fill that rather than the <select> directly. Populating
      // the element here instead left fillSelect looking at an empty array,
      // which blanked the dropdown it had just built and reported "0 open".
      state.specs = await api('GET', '/specs');
      const sel = $('#ty-slug');
      sel.onchange = () => loadSlug(sel.value);
      const want = recall();
      const known = state.specs.some(x => x.slug === want.slug);
      // Otherwise open on the first set with work left, rather than on a
      // finished one that the default filter is about to hide anyway.
      const first = state.specs.find(x => !x.done) || state.specs[0];
      const slug = known ? want.slug : (first && first.slug);
      if (slug) {
        state.slug = slug;
        fillSelect();
        await loadSlug(slug, known);
        // only restore the shot if it still exists in this spec
        if (known && want.shot && state.data.shots.some(x => x.key === want.shot)) {
          state.shot = want.shot;
          renderShots();
        }
        if (!known && want.slug) toast(`"${want.slug}" is gone; showing ${slug}`, true);
      }
      fillSelect();
    } catch (e) {
      $('#ty-status').textContent = 'offline';
      toast(e.message, true);
    }
  })();
})();
