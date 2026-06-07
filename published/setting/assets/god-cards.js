/* ───────────────────────────────────────────────────────────────
   god-cards.js: shared Style-A god-card builders

   The render engine for the expandable "god / being" cards used by the
   Non-Bound Gods page, the Bolverk infernal-hierarchy page, and any
   future per-plane page (Feyworld Season Courts, Shadowplane, the
   Layer-3 planes, etc.). A page supplies its own data array and a grid
   container, then calls these builders inside a DOMContentLoaded handler
   (this file is loaded with `defer`, so the functions are defined before
   DOMContentLoaded fires).

   The card SHELL styling lives in style-a.css (.god-card, .god-orb,
   .card-expanded, .god-stats, …). The GM-Secret toggle (toggleSecret)
   lives in site-interactions.js. Include all three on any page that
   renders these cards:

     <link rel="stylesheet" href="/setting/assets/style-a.css">
     <script defer src="/setting/assets/site-interactions.js"></script>
     <script defer src="/setting/assets/god-cards.js"></script>

   Two card shapes:
     buildBeingCard(being, gridId)  — non-bound gods / primordials /
                                      Layer-3 residents / virtue-devil stubs
     buildDemonCard(d, gridId)      — Vice Demons / seated Virtue Devils
                                      (richer: vice/spire/fall sections)
   ─────────────────────────────────────────────────────────────── */

function buildBeingCard(being, gridId) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  const card = document.createElement('div');
  card.className = 'god-card';
  if (being.id) {
    card.id = being.id;
  } else {
    card.id = being.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }
  card.style.setProperty('--accent', being.accent);

  card.innerHTML = `
    <div class="card-top">
      <div class="god-orb" style="--orb-bg:${being.orbBg};--orb-glow:${being.orbGlow};background:${being.orbBg};box-shadow:0 0 16px ${being.orbGlow}">${being.orb}</div>
      <div class="god-title">
        <div class="god-name">${being.name}</div>
        <div class="god-domain-primary" style="color:${being.accent}">${being.primary}</div>
        <div class="god-city">${being.tier} · ${being.city}</div>
      </div>
      <div class="expand-hint">Tap ▾</div>
    </div>
    <div class="card-summary">${being.summary}</div>
    <div class="card-expanded">
      <div class="exp-section">
        <div class="exp-label">At a Glance</div>
        <div class="god-stats">
          <div class="stat-row"><div class="stat-label">Aspects</div><div class="stat-val">${being.aspects}</div></div>
          <div class="stat-row"><div class="stat-label">Worshippers</div><div class="stat-val">${being.worshippers}</div></div>
          <div class="stat-row"><div class="stat-label">Etymology</div><div class="stat-val">${being.etymology}</div></div>
        </div>
      </div>
      <div class="exp-section">
        <div class="exp-label">Nature &amp; Position</div>
        <div class="exp-text">${being.nature}</div>
      </div>
      <div class="exp-section">
        <div class="exp-label">Of Note</div>
        <div class="exp-text" style="color:var(--text-dim);font-style:italic">${being.note}</div>
      </div>
      ${being.secret ? `
      <div class="secret-section">
        <button class="secret-toggle" onclick="toggleSecret(event, this)">⚿ &nbsp; GM Secret · Click to Reveal</button>
        <div class="secret-content">
          <div class="secret-label">⚿ &nbsp; Secret · Known to Very Few</div>
          <div class="secret-text">${being.secret}</div>
        </div>
      </div>` : ''}
    </div>
  `;

  card.addEventListener('click', (e) => {
    // Don't collapse when clicking inside the expanded content
    if (card.classList.contains('expanded') && e.target.closest('.card-expanded')) return;
    const isExpanded = card.classList.contains('expanded');
    document.querySelectorAll('.god-card.expanded').forEach(c => c.classList.remove('expanded'));
    if (!isExpanded) {
      card.classList.add('expanded');
      setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50);
    }
  });

  grid.appendChild(card);
}

// ── Honour an inbound #fragment after deferred card render ─────
// Cards inject on DOMContentLoaded (the builders load via `defer`),
// which is after the browser's initial scroll-to-fragment attempt,
// so a cross-page link like voroir-daua.html → layer-3-gods.html#epairima
// lands at the top of the page on cold navigation. Re-scroll once the
// cards exist. Runs on `load`, after every page's build calls have fired.
window.addEventListener('load', function () {
  if (!location.hash) return;
  var el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (el) el.scrollIntoView();
});

function buildDemonCard(d, gridId) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  const card = document.createElement('div');
  card.className = 'god-card';
  card.id = d.name.toLowerCase();
  card.style.setProperty('--accent', d.accent);

  const sectionIf = (label, text) => text ? `<div class="exp-section"><div class="exp-label">${label}</div><div class="exp-text">${text}</div></div>` : '';
  const placeholderNote = !d.mortalLife ? `<div class="exp-section"><div class="exp-text" style="color:var(--text-dim);font-style:italic">Full canon for this holder is in progress and will appear here as it is designed.</div></div>` : '';

  card.innerHTML = `
    <div class="card-top">
      <div class="god-orb" style="--orb-bg:${d.orbBg};--orb-glow:${d.orbGlow};background:${d.orbBg};box-shadow:0 0 16px ${d.orbGlow}">${d.orb}</div>
      <div class="god-title">
        <div class="god-name">${d.name}</div>
        <div class="god-domain-primary" style="color:${d.accent}">${d.primary}</div>
        <div class="god-city">${d.location}</div>
      </div>
      <div class="expand-hint">Tap ▾</div>
    </div>
    <div class="card-summary">${d.summary}</div>
    <div class="card-expanded">
      <div class="exp-section">
        <div class="exp-label">At a Glance</div>
        <div class="god-stats">
          <div class="stat-row"><div class="stat-label">${d.lineLabel || 'Vice'}</div><div class="stat-val">${d.vice}</div></div>
          <div class="stat-row"><div class="stat-label">Held since</div><div class="stat-val">${d.heldSince}</div></div>
          <div class="stat-row"><div class="stat-label">Name etymology</div><div class="stat-val">${d.etymology}</div></div>
          <div class="stat-row"><div class="stat-label">PF2e Domain</div><div class="stat-val">${d.domain}</div></div>
          <div class="stat-row"><div class="stat-label">Favored Weapon</div><div class="stat-val">${d.weapon}</div></div>
        </div>
      </div>
      ${sectionIf(d.mortalLifeLabel || 'Mortal Life', d.mortalLife)}
      ${sectionIf(d.theFallLabel || 'The Fall &amp; Ascension', d.theFall)}
      ${sectionIf('Form', d.form)}
      ${sectionIf(d.spireLabel || 'The Spire', d.spire)}
      ${sectionIf('Method on Talan', d.method)}
      ${sectionIf(d.reputationLabel || 'Reputation Among the Seven', d.reputation)}
      ${placeholderNote}
      ${d.secret ? `
      <div class="secret-section">
        <button class="secret-toggle" onclick="toggleSecret(event, this)">⚿ &nbsp; GM Secret · ${d.secretTitle || 'Click to Reveal'}</button>
        <div class="secret-content">
          <div class="secret-label">⚿ &nbsp; ${d.secretLabel || 'Secret · Known to Very Few'}</div>
          <div class="secret-text">${d.secret}</div>
        </div>
      </div>` : ''}
    </div>
  `;

  card.addEventListener('click', (e) => {
    if (card.classList.contains('expanded') && e.target.closest('.card-expanded')) return;
    const isExpanded = card.classList.contains('expanded');
    document.querySelectorAll('.god-card.expanded').forEach(c => c.classList.remove('expanded'));
    if (!isExpanded) {
      card.classList.add('expanded');
      setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50);
    }
  });

  grid.appendChild(card);
}
