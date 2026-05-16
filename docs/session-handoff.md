# Session Handoff — 2026-05-17

A snapshot for the next Claude session picking up Tyrnarra work. The canonical tracking files (below) are the source of truth; this file is the **session-level context** that doesn't fit elsewhere.

---

## Where the project is right now

**WorldAnvil → lore migration: COMPLETE.** The `worldanvil-export/` and `tools/` folders have been deleted from the repo (recoverable from git history). All canon now lives in `lore/`.

**Lore → HTML publishing: IN PROGRESS.** Tier 1 of the publishing pass just landed. Tier 2 is next.

**Current authoritative state lives in three files** — read all three before picking up work:

1. [`lore/`](../lore/) — the canon (world-notes, geography, factions, bestiary, cultures, glossary, timeline, unplaced). Lore wins on conflict with any HTML page.
2. [`docs/open-threads.md`](open-threads.md) — every TBD / unresolved / future-development thread, organised by topic with status + what's decided + what's open + where it lives. **Read this any time the user mentions an unresolved canon question.**
3. [`docs/site-inventory.md`](site-inventory.md) — what's published vs stub on the HTML side. **Read this any time the user mentions publishing or HTML pages.**
4. [`docs/worldanvil-migration.md`](worldanvil-migration.md) — historical migration log + **active HTML Publishing Status Tracker** at the bottom. The tracker is the publishing punch list.

---

## What was done this session (2026-05-16 → 2026-05-17)

The session spanned two days of dense work, organised as a sequence of phases each ending with a user check-in.

### Lore-side closure

1. **Migration audit** — walked all 233 WA export files; 10 discrepancies surfaced, all resolved. Results in `docs/migration-review.md`.
2. **Named Non-Bound Gods canonised** — Bikiargi (Twins / Moon), Zaharsuge (Eldest / Wyrmkin), Epairima (Judge of Souls), Betibizi (Undeath; Storveldi Denbora ruling-class survivor + integration-procedure holder). Sun god noted as forward thread.
3. **"Domains Outside the Thirteen" 14-domain source mapping** added (Abomination → Muiral; Plague → Corrupted God; Decay/Swarm/Naga/Nightmares → four Generals of Corruption; Tyranny/Destruction/Indulgence → three named Sin Devils; Pain/Toil/Sorrow/Delirium → four virtue-demons).
4. **Base ancestry rework** — 44 standard PF2e remaster ancestries placed; Gnoll→Kholo, Grippli→Tripkee renamed; 8 new ancestries placed (Athamaru, Awakened Animal, Centaur, Dragonet — Zaharsuge's living lineage, Jotunborn, Merfolk, Minotaur, Surki). Tyrnarra-canon kept: Dragons, Dragonkin, Slimes, Rabbitfolk.
5. **Tian Xia placement pass** — created **Sortalde** (external Talanese name) / **Tao Hua Yuan** (internal name), the Eastern petal-archipelago across Hafra. Shape: 7 petals (Wandao/Xidao/Niudao = outer; Yingdao/Lingdao/Lundao = inner; Heting = central Concord seat). All 6 Tian Xia ancestries placed on petals. Hungerseed resolved (Oni are bound spirits of Lingdao). Kitsune confirmed *not* descended from Sortalde — parallel naming is coincidental. Theology: no walking gods on Sortalde, Layer-3 pantheon (unnamed, future thread).
6. **Magitech canon** — Magitech is the umbrella for applied magic-engineering, with four sub-traditions per school: **Arcanotech** (dominant), **Occultech** (rarer; chaos-resilient), **Divitech** (almost non-existent; ceremonial), **Primotech** (essentially non-existent; legendary). Modern Magitech descends from **post-Crimson-Rain Elden-ruin discoveries** (UHTC = Elden — that open thread closed). Transport tiers documented: **Magitrains** on land (common, two-half network with Basogur as the rail-blocker between northern and southern halves), **Ships** on water (normal wooden by count, Magitech for the wealth upgrade — Occultech for chaos-water work), **Airships** in the sky (always Magitech; Arcanotech standard or Occultech with bound air elemental; only premium way over Basogur), **Cloudships** for the Cloud Sea (very rare; **always dual-school** — typically Arcanotech+Occultech, rarer Arcanotech+Divitech, legendary Arcanotech+Primotech like *Eyrasunda*).
7. **Cleanups** — Balaena placed in Floteyn → Floating Isles of Shuun; Conductor's Station promoted to canon hazard of the Magitrain network (haunts both halves equally); Train Pirates entry added to factions.md.
8. **Doc hygiene** — created `docs/open-threads.md` as the punch list; restructured `docs/worldanvil-migration.md` to clearly separate the (complete) WA-side migration from the (active) HTML publishing; updated CLAUDE.md with migration state. Deleted `worldanvil-export/` and `tools/`.

### HTML publishing — Tier 1 landed

The publishing audit produced a tiered priority list (see `docs/worldanvil-migration.md` HTML tracker for the live state). Tier 1 = lowest friction, highest visible impact. All complete:

- **`the-binding.html`** — added GM Secret expandable revealing the Corrupted God = Elden truth + 4 General domain-grants (Vermin Queen → Swarm, Rot-Tyrant → Decay, Whisperer in Dreams → Nightmares, Maw Serpent → Naga). Toggle JS wired in.
- **`grand-gods.html`** — Vesuna gained Free Will, Hinka gained Violent Death (per-god cleric domain lists).
- **`brauogi.html`** — Minotaur added as third dominant Earth-domain ancestry; Magitrain southern-network line added to At a Glance.
- **`lautara.html`** — Emarrea sub-region card now links to its existing page (was stale TBD); Crossroads sub-region card added (Spider's Silk Inn + Sortalde embassies mentioned); Magitrain northern-hub line added.
- **`lioaru.html`** — Lost Kingdom card expanded with public Blackened Lands canon (Skeleton/Fleshwarp origin); GM Secret expandable revealing Storveldi/Betibizi truth; Magitrain limits noted.
- **`sumendar.html`** — Order of Steam reframed as Magitech industrial heart with Elden-tech excavation origin and House Eisenhart; Dragon's Reach two-recovery-projects friction; Magitech + Magitrain lines added.

---

## What's next

### Tier 2 — next publishing batch (recommended order)

1. **Crossroads dedicated page** at `talan/domains/lautara/crossroads.html` + **Spider's Silk Inn** content. The Lautara sub-region card already references both; this promotes them properly. **Add sidebar nav entry** in `assets/site-nav.js` under Lautara children.
2. **Red Empire faction page** at `talan/factions/red-empire.html` — fully written in lore (`factions.md` → Off-Continent Powers), clean new build. Add sidebar nav.
3. **Lost Kingdom dedicated page** at `talan/domains/lioaru/lost-kingdom.html` with GM Secret for the Storveldi truth. (Lioaru domain page already covers the public-facing summary + GM Secret; the dedicated page is the deep dive.)
4. **House Eisenhart page** under factions or as a sub-page of Order of Steam (TBD).

### Tier 3 — substantial rewrites

5. **Adventurers Guild rewrite** at `talan/factions/adventurers-guild.html` — major expansion to incorporate the rank ladder (Bronze→Starsteel), branch hierarchy, Bank, Post, Grand Assembly, Lord Albrecht Lavisburg, Seraphel Duskbane. Currently has the original short writeup.
6. **`magic.html` rewrite** — add Mortal Ascent Ladder, Domains Outside the Thirteen, Magitech canon section.
7. **`talan.html` updates** — Other Continents framing (Sortalde + Red Empire continent), Continental Rail Network note.
8. **`history.html` updates** — Storveldi Denbora GM Secret on Gods' Era card.

### Tier 4 — big new builds

9. **Sortalde continent** — new page at `talan/sortalde.html` or `talan/sortalde/sortalde.html`. Covers 7 petals + 6 ancestries + Concord + theology + Hafra crossing. Decide whether to use Style B with Sortalde-specific accent colour. **Add sidebar nav entry as a peer to Talan, or as a separate top section.**
10. **`bestiary.html`** — overview page for 50+ ancestries. Could be per-domain sections, alphabetical, or both.

### Tier 5 — publishable with TBD (per user)

11. **Legea Empire page** — Divine Faith. God name + demigod ruler + theocratic prince all TBD. User said they're fine with TBD pages.
12. Individual Nine Generals dungeon pages — placements TBD for 7 of 8.

### Tier 6 — incremental, story-driven

- Per-god GM Secrets (12 of 13 placeholder on `grand-gods.html`; Cronus's is the only one fully written).
- Three-tier UI on remaining 6 history eras.
- Other god city-state pages (Haizava, Merkavar, Uravel, Eldara, Denbora, Lurrath, Thekkavar, Ljosarn, Lograth, Nahaskel, Veidrath, Frae City).
- Millhaven settlement (Brauogi).
- Order of Steam, Thousand Kingdom, Dragon's Reach — promoted sub-region/settlement pages.

---

## How we've been working — patterns to maintain

These are session-level rhythms, not formal rules. They've been working — keep them up unless the user redirects.

1. **Check in between phases.** A phase is a coherent chunk of work (one HTML page, one big lore restructure, one ancestry pass). After each phase: short summary, list of what landed, pointer to next, then wait for user. **Don't run two phases together without an explicit "yes continue."** Memory file: `feedback_check_in_between_phases.md`.
2. **Strong defaults + crisp redirects.** The user gives directional answers and expects strong picks rather than open-ended questions. When proposing options, offer 2–4 with a clear pick and reasoning. They redirect if they disagree. Don't over-batch questions — 3–4 max in an AskUserQuestion call; if more are needed, do them in two rounds.
3. **Lore-first protocol.** All worldbuilding lands in `lore/` first; HTML only with explicit publish signal. The lore migration is closed, so this mostly affects new canon coined during HTML work (etymologies, named NPCs) — capture to glossary.md / relevant lore file BEFORE the HTML uses it.
4. **GM Secret discipline.** Recent canon includes major GM-truth pieces. Public-facing HTML body must NOT leak them. Use the `.secret-era-toggle` / `.secret-era-content` pattern (red ⚿ pill); content reveals on click. Toggle JS goes at the bottom of the page if not already present. The Storveldi-Denbora-killed-Tani, Cronus-was-mortal, Elden=Corrupted-God, Betibizi-Origin, and Integration-Procedure facts are all GM-only.
5. **Sidebar nav.** Every new page needs an entry in `/assets/site-nav.js` `DOMAINS` array (sub-regions/settlements under domains) or `NAV_HTML` arrays (top-level/factions). Easy to forget. Add immediately when a new page lands.
6. **Migration doc + site-inventory updates.** When a publishing pass lands, strike through completed rows in `docs/worldanvil-migration.md` HTML tracker and add to `docs/site-inventory.md`. Both are how future sessions know what's done.

---

## Open canon questions ranked by publishing impact

Forward-worldbuilding gaps that would show up in HTML if their target page publishes today. User said they're OK with TBD-stub pages, so these are NOT blockers — but worth knowing per page:

- **Sortalde Layer-3 pantheon** — would render as "(unnamed; future thread)" on a Sortalde page.
- **Divine Faith pantheon** — god/demigod/prince names all TBD; would render as "TBD" on a Legea Empire page.
- **8 Nine Generals dungeons** — placement TBD for 7. The-binding.html already handles this (only Vermin Queen has a Located tag).
- **Sub-region etymologies** — ~10 sub-regions with "etymology TBD" tags. Visible on domain pages and the glossary.
- **Sin-Devil names + 4 missing domain mappings** (Envy/Greed/Lust/Sloth) — visible as "(unnamed) — TBD" in any future devils/demons page.
- **Sun god** — short "open thread" subsection in world-notes; would render as TBD on a Named Non-Bound Gods page.

Full list with status: [`docs/open-threads.md`](open-threads.md).

---

## Memory state

The persistent memory directory at `~/.claude/projects/C--Users-Thoma-Documents-Tyrnarra/memory/` has one file:

- `feedback_check_in_between_phases.md` — captures the between-phases-check rhythm and the strong-defaults/crisp-redirects preference.

`MEMORY.md` indexes it.

---

## Final note

The user prefers **terse, scannable summaries** over verbose explanations. Use sentence fragments where they read clean; complete sentences where they don't. Match the tone of past responses in this repo's docs files. Markdown links so files are clickable.

If you're uncertain about scope, ask — but pick a default first. Don't ratify exhaustively.
