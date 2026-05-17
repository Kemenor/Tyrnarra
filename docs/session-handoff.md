# Session Handoff — 2026-05-17

A snapshot for the next Claude session picking up Tyrnarra work. The canonical tracking files (below) are the source of truth; this file is the **session-level context** that doesn't fit elsewhere.

---

## Where the project is right now

**WorldAnvil → lore migration: COMPLETE.** The `worldanvil-export/` and `tools/` folders are no longer in the repo (recoverable from git history). All canon lives in `lore/`.

**Lore → HTML publishing: TIERS 1–4 SUBSTANTIALLY COMPLETE.** Tier 5 (TBD-stub pages) and Tier 6 (incremental story-driven content) are the active forward fronts. The only remaining structural Tier-4-or-earlier item is **`bestiary.html`** (Tier 4 step 10 — overview page for 50+ ancestries).

**Current authoritative state lives in four files** — read them in this order:

1. [`lore/`](../lore/) — the canon (world-notes, geography, factions, bestiary, cultures, glossary, timeline, unplaced). Lore wins on conflict with any HTML page.
2. [`docs/open-threads.md`](open-threads.md) — every TBD / unresolved / future-development thread, organised by topic.
3. [`docs/site-inventory.md`](site-inventory.md) — what's published vs stub on the HTML side. Comprehensive.
4. [`docs/worldanvil-migration.md`](worldanvil-migration.md) — historical migration log + active HTML Publishing Status Tracker at the bottom. The tracker is the publishing punch list with most rows now struck through.

---

## What was done across the recent sessions (2026-05-16 → 2026-05-17)

### Lore-side closure (earlier sessions, 2026-05-16/17)

1. **Migration audit** — walked all 233 WA export files; 10 discrepancies resolved.
2. **Named Non-Bound Gods** — Bikiargi (Twins/Moon), Zaharsuge (Eldest/Wyrmkin), Epairima (Judge of Souls), Betibizi (Undeath; Storveldi-Denbora-survivor + integration-procedure holder). Sun god is a forward thread.
3. **"Domains Outside the Thirteen"** 14-domain source mapping (now published on `magic.html`).
4. **Base ancestry rework** — 44 PF2e remaster ancestries + 8 new placements + Tyrnarra-canon retained.
5. **Tian Xia placement pass** — created **Sortalde** / **Tao Hua Yuan**, the seven-petal continent. All six ancestries placed. Theology: no walking gods, Layer-3 pantheon (unnamed; future thread).
6. **Magitech canon** — Arcanotech (dominant) / Occultech (rarer) / Divitech (almost non-existent) / Primotech (legendary). Transport tiers documented (Magitrains / ships / airships / cloudships).

### HTML publishing — TIERS 1 → 4 (this session run)

**Tier 1** — `the-binding.html`, `grand-gods.html`, and five domain pages (brauogi/lautara/lioaru/sumendar plus the Cronus tile on talan.html).

**Tier 2** — four pages all shipped:
- `crossroads.html` + Spider's Silk Inn — Lautara sub-region
- `red-empire.html` — new `/off-continent/` section created
- `lost-kingdom.html` — Lioaru deep dive with comprehensive GM Secret
- Bundle: `order-of-steam.html` + `house-eisenhart.html` — Sumendar sub-region with sub-page

**Tier 3** — all four touches shipped:
- `adventurers-guild.html` — full rewrite (branch hierarchy, rank ladder, Bank, Post, Lavisburg, Seraphel, Godshall)
- `magic.html` — rewrite adding Magitech section, Mortal Ascent Ladder + GM Secret, Domains-Outside-the-Thirteen table
- `talan.html` — Continental Rail Network full section, Other Continents three-card section
- `history.html` — Gods' Era three-tier expandables (Old Race + Storveldi); Week of Crimson Rain secret harmonised

**Tier 4 (partial)** — pair shipped:
- `sortalde.html` — full continent page in `/off-continent/`
- `emerald-isles.html` — paired Talan-side cloudship landing point with the Bridgelands canon
- *Remaining*: `bestiary.html` overview (Tier 4 step 10).

### Smaller corrections shipped this session (worth knowing)

- **Sortalde embassies relocated** from Merkavar/Crossroads (inland — wrong) to the **Emerald Isles' Bridgelands** (the kingdom's NE outer-rim islands on the Hafra/Cloud-Sea boundary). Lore + HTML both consistent.
- **Train Pirates "Sortalde-route specialists" canon retraction** — cloudship route, not rail. Removed from lore and HTML.
- **Train Pirates + Conductor's Station** added to `factions.html` as a *Bandit Categories & Hazards* section to resolve broken cross-links from talan.html and order-of-steam.html.
- **Hooks sections removed** from `sortalde.html` and `house-eisenhart.html` — per user preference: **published HTML is lore documentation, not campaign-starter material.** This is a durable rule going forward — see `CLAUDE.md` and `feedback_no_campaign_hooks_in_html.md`. World-flavour expandables (Crossroads tavern rumours, Lost Kingdom Popular Belief) are different and stay.

---

## What's next

### Tier 4 — final structural piece

10. **`bestiary.html`** — overview page for 50+ ancestries. Options: per-domain sections, alphabetical, or both. Sortalde ancestries already published on the Sortalde continent page; this would be the Talan-side bestiary surface. Bigger build than most Tier 2/3 work.

### Tier 5 — publishable with TBD (user is fine with TBD-stub pages)

11. **Legea Empire page** — Divine Faith / Zuzental sub-region. God identity, demigod ruler, theocratic prince all TBD.
12. **Individual Nine Generals dungeon pages** — placements TBD for 7 of 8 (only Vermin Queen's Hollow is sited).

### Tier 6 — incremental, story-driven (the long backlog)

- **Per-god GM Secrets** — 12 of 13 placeholder text on `grand-gods.html` (Cronus is done).
- **Three-tier UI on remaining eras** — Lost, Golden, Dark, Adventurer (Creation is intentionally open). Pattern matches Gods' Era / Crimson Rain / Elden Era.
- **Other god city-state pages** — Haizava, Merkavar, Uravel, Eldara, Denbora, Lurrath, Thekkavar, Ljosarn, Lograth, Nahaskel, Veidrath, Frae City. Pattern: folder under domain (Myrria pattern).
- **Settlements**: Millhaven (Brauogi).
- **Sub-region promotion (remaining major)**: Thousand Kingdom, Dragon's Reach, River Duchies.
- **Per-faction promotions**:
  - **Bandit Categories** — likely deserves its own page once more categories land (highway raiders, Midarra river pirates / Twin Cities, ruin-strippers, slavers). Tracked in `open-threads.md` → *Site structure → Factions page reorganisation*.
  - **Conductor's Station** — same. Phenomenon more than bandit category; could move to its own page or a future `/hazards/` folder.
- **Emerald Isles capital name** — flagged TBD in `open-threads.md`.

---

## How we've been working — patterns to maintain

These are session-level rhythms. They've been working — keep them up unless redirected.

1. **Check in between phases.** A phase ≈ one HTML page or one coherent lore restructure. After each: short summary + what landed + next + wait. **Don't run two phases together without an explicit "yes continue."** Memory: `feedback_check_in_between_phases.md`.
2. **Strong defaults + crisp redirects.** Offer 2–4 options with a clear recommendation and reasoning. User redirects if they disagree. 3–4 questions max per AskUserQuestion call.
3. **Lore-first protocol.** New canon coined during HTML work (etymologies, named NPCs, kingdom expansions) goes to `lore/glossary.md` / `lore/geography.md` / etc. BEFORE the HTML uses it. Drafting protocol is still in effect for new canon even during the publishing pass.
4. **GM Secret discipline.** Major GM-truth facts (Cronus-was-mortal, Elden=Corrupted-God, Storveldi-killed-Tani, Betibizi-origin, Integration-Procedure) stay behind red ⚿ `secret-era-toggle` expandables. Public-facing body must not leak them.
5. **Lore documents, not campaign starters.** Published HTML is lore reference. **No dedicated "Hooks" sections** with adventure prompts in the published pages — that material belongs in GM-side notes elsewhere. World-flavour expandables (folkloric Popular Belief, in-world rumours) are different and welcome. Memory: `feedback_no_campaign_hooks_in_html.md`. Project convention: `CLAUDE.md`.
6. **Sidebar nav.** Every new page needs an entry in `/assets/site-nav.js` (`DOMAINS` for children under domains; `NAV_HTML` arrays for top-level sections). Easy to forget — add immediately when a page lands.
7. **Tracker updates.** When a page lands: strike through completed rows in `worldanvil-migration.md` HTML tracker; add to `site-inventory.md`. Both are how future sessions know what's done.

---

## Open canon questions ranked by publishing impact

Forward-worldbuilding gaps. User said TBD-stubs are fine, so these are not blockers — but worth knowing per page:

- **Emerald Isles capital name** — currently renders as *"the kingdom's capital (name TBD)"* on `emerald-isles.html`. Small naming call.
- **Sortalde Layer-3 pantheon** — flagged on `sortalde.html` as "unnamed; future thread." Doesn't break anything; a naming pass would close out the Eastern continent's religious texture.
- **Divine Faith pantheon** — god/demigod/prince names all TBD; would render as "TBD" on any future Legea Empire page.
- **8 Nine Generals dungeons** — placement TBD for 7. `the-binding.html` already handles this (only Vermin Queen has a Located tag).
- **Sub-region etymologies** — ~10 sub-regions with "etymology TBD" tags. Visible on domain pages and glossary.
- **Sin-Devil names + 4 missing domain mappings** (Envy/Greed/Lust/Sloth) — visible as "(unnamed) — TBD" in any future devils/demons page.
- **Sun god** — short open thread; would render as TBD on a Named Non-Bound Gods page.

Full list with status: [`docs/open-threads.md`](open-threads.md).

---

## Important recent canon corrections (don't undo)

The user caught and corrected several things mid-session. **Do not reintroduce these:**

- **Sortalde + rail conflation is wrong.** Sortalde freight arrives via cloudship and lands on the Bridgelands. No Magitrain line or Sortalde-route train freight on any page. Train Pirates have no "Sortalde-route specialist" category.
- **Sortalde embassies are NOT in Merkavar or Crossroads** (those are inland). They are on the **Emerald Isles' Bridgelands** — the NE outer-rim islands of the Zuzental island kingdom, partially in Hafra/partially in Cloud Sea, connected by spanning Magitech bridges.
- **No "Hooks" sections** on lore-documentation pages. Folkloric expandables (Popular Belief / tavern rumour / "what people say") are fine; campaign-starter prompts are not.

---

## Memory state

The persistent memory directory at `~/.claude/projects/C--Users-Thomas-Documents-Tyrnarra/memory/` has:

- `feedback_check_in_between_phases.md` — the between-phases-check rhythm and strong-defaults preference.
- `feedback_no_campaign_hooks_in_html.md` — published HTML is lore documentation, not campaign starters; no dedicated Hooks sections.

`MEMORY.md` indexes them.

---

## Final note

The user prefers **terse, scannable summaries** over verbose explanations. Match the tone of past responses in this repo's docs files. Markdown links so files are clickable.

If you're uncertain about scope, ask — but pick a default first. Don't ratify exhaustively.
