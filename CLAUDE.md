# Tyrnarra — Worldbuilding Project

This repo is a personal worldbuilding project for the setting **Tyrnarra**. The deliverable is a static HTML site published via GitHub Pages. Pages are hand-crafted HTML; **shared chrome lives in `/assets/`** (sidebar nav, Style A and Style B base CSS) and is referenced via `<link>` and `<script defer src>` tags. Page-specific styling and unique content stay inline in the page itself.

For getting the site running locally, see [`README.md`](README.md). For what's currently published vs. stub, see [`docs/site-inventory.md`](docs/site-inventory.md). For how the persistent sidebar works, see [`docs/sidebar-nav.md`](docs/sidebar-nav.md).

---

## The naming convention (most important rule)

**For anything new you create**, follow this convention strictly:

- **Old or ancient things** — ruins, kingdoms, geographic features, deity names, anything pre-modern or "of the world itself" — are named by:
  1. Translating a meaningful word or phrase into **Basque** or **Icelandic**
  2. Then slightly altering it to represent linguistic drift over time

  Example: *"Ehizahar"* (Hunt domain of Hinka) comes from Basque *"ehiza"* (hunt) + *"zahar"* (ancient), naturally eroded to its current form. Drift can happen anywhere in the word, not just the end.

- **New or modern things** — recently founded institutions, contemporary city-states, modern organizations — are named **plainly in English** but they may have drifted lightly.

  Examples: *"Free City"* → *"Frae City"*, *"Order of Steam"*, *"The Wayward Compass"*, *"Clearwater Exchange"*.

**When you coin a new name, always show your work**: note the source language, the literal meaning, and the drift step. Save it in `lore/glossary.md` so the etymology is preserved.

**Existing names predate this rule** — don't try to retrofit names that are already in the HTML pages (Forseti, Cronus, etc.). Just follow the rule going forward.

---

## File layout

The site is hierarchical: **Tyrnarra → Talan → Domains → Sub-Regions/Kingdoms → Settlements.** The folder tree mirrors the world. World-level (cosmic) content lives at root; continent-level content lives under `/talan/`.

```
/                                      ← GitHub Pages serves from here
  index.html                           ← landing = world primer (cosmology)
  grand-gods.html                      ← the 13 bound gods (world-level)
  magic.html                           ← Magic & Faith — Four Schools, daily life, faith

  talan/                               ← continent-level content
    talan.html                         ← continent overview (three seas, all 13 domains)
    history.html                       ← Eras / timeline
    domains/                           ← the 13 god domains
      <domain>/<domain>.html           ← e.g. vindul/vindul.html — domain entry page
      <domain>/<sub-region>.html       ← optional: promoted sub-region with its own page
      <domain>/<settlement>/           ← settlement folder, when content warrants
        <settlement>.html
        <sub-location>.html            ← location within the settlement
        Quests/                        ← quests nest under their location
          quest-<slug>.html
    factions/                          ← independent organisations
      factions.html                    ← faction overview / taxonomy
      adventurers-guild.html
      mercenary-guild.html
      god-churches.html
      remnants.html

  assets/                              ← shared chrome (loaded by every page)
    site-nav.css                       ← sidebar styling
    site-nav.js                        ← sidebar markup + behaviour (single source of truth for menu)
    style-a.css                        ← Style A base — used by world-level pages (/, gods, magic)
    style-b.css                        ← Style B base — used by every page under /talan/

  lore/                                ← worldbuilding canon (NOT published)
    cosmology.md                       ← how the world works — Wellspring, planar layers, magic, magitech, calendar
    gods.md                            ← who the gods are — the Thirteen, non-bound gods, city-states, cleric domains
    secret-history.md                  ← what really happened — Crimson Rain, Storveldi Denbora, Elden, Wardstones, Nine
    geography.md                       ← domain etymologies + sub-regions
    factions.md                        ← faction taxonomy + entries
    cultures.md                        ← peoples, traditions, politics, craft
    bestiary.md                        ← playable ancestries + otherworldly beings
    glossary.md                        ← coined names + etymologies
    timeline.md                        ← eras + dates

  docs/                                ← site documentation (NOT published)
    site-inventory.md                  ← what's published vs. stub
    sidebar-nav.md                     ← architecture notes on the shared sidebar

  CLAUDE.md                            ← this file
  README.md
  CNAME
  serve.bat / serve.sh                 ← local dev server helpers
```

**`lore/` vs. `docs/`**: `lore/` is the source of truth for what's *true in the world* — when an HTML page disagrees with a lore file, the lore wins. `docs/` is the source of truth for *how the site is built*. They have different update rhythms: canon evolves with the world; docs drift with the code.

### Layer-to-folder mapping

| World layer | Folder | Example |
|---|---|---|
| World (Tyrnarra) | root | `index.html` (cosmology), `grand-gods.html`, `magic.html` |
| Continent (Talan) | `/talan/` | `talan.html`, `history.html` |
| Region (god domain) | `/talan/domains/<domain>/` | `/talan/domains/vindul/vindul.html` |
| Sub-region / Kingdom | section in domain page, or own file when promoted | `Thousand Kingdom` lives inside `zuzental.html` until it earns its own file |
| Settlement | folder under its domain | `/talan/domains/brauogi/millhaven/millhaven.html` |
| Sub-location of settlement | sibling file in settlement folder | `/talan/domains/brauogi/millhaven/lowspan.html` |
| Quest | `Quests/` inside settlement folder | `/talan/domains/brauogi/millhaven/Quests/quest-x.html` |
| Faction (independent org) | `/talan/factions/` | `/talan/factions/adventurers-guild.html` |
| God church | umbrella `god-churches.html`; promoted to its own file when content warrants | `/talan/factions/god-churches.html` |

### Conventions

- **Folder slugs** are lowercase ASCII with hyphens. Diacritics are stripped from slugs but kept in display titles.
- **Each settlement gets its own folder under its domain.** The folder's main page is named the same as the folder (`millhaven/millhaven.html`).
- **Sub-regions** start as sections inside the domain page. When one earns enough content, promote it to its own file in the domain folder (e.g. `zuzental/thousand-kingdom.html`). Don't create empty stub files for sub-regions that don't exist yet.
- **Kingdoms vs. sub-regions:** "sub-region" is the umbrella; some sub-regions are kingdoms (Thousand Kingdom, Order of Steam), others are geographic (Baerfrost), cultural (Tahu Tangata), or border territories (Azkamour). All live in the same place in the folder tree — the political type is a property, not a folder.
- **Always use absolute paths in links** (starting with `/`). The sidebar uses absolute paths and so does cross-linking between pages.
- **Dark mode only.** All pages assume a dark background.
- **Mobile responsive.** Pages use `@media (max-width: 600px)` breakpoints — match this.
- **No build step.** Open in a local server, it just works. (See README.md for the local server.)
- **Tone in copy:** specific over generic. Small concrete details (the smell, the named NPCs, the inside-joke aside) over abstract worldbuilding.

---

## Persistent sidebar navigation

Every page references the shared sidebar by including two tags in `<head>`:

```html
<link rel="stylesheet" href="/assets/site-nav.css">
<script defer src="/assets/site-nav.js"></script>
```

The page declares its location for the highlight via `<body data-page="vindul">`.

To add or rename a page in the sidebar, edit `/assets/site-nav.js` (the `NAV_HTML` array) — one file, one place. Full architecture in [`docs/sidebar-nav.md`](docs/sidebar-nav.md).

---

## Two page styles

The existing pages establish two visual modes. New pages should pick one and match it closely — don't invent a third style without asking.

### Style A — Cosmic / World-level
Used for: the landing/cosmology, the 13 gods, magic — anything world-scale or mythic.

- **Source:** `/assets/style-a.css`. Page-specific tweaks (orb effects, soul bars) stay inline in the page itself.
- **Fonts:** Cinzel Decorative (page titles), Cinzel (labels, small caps), Crimson Pro (body)
- **Palette:** deep void (`--bg: #06060a`), purple/blue ambient gradients, gold accents (`--gold: #c8a84a`, `--gold-bright: #f0d080`), parchment text (`--text: #c8c4d8`), per-god accent colours
- **Signature elements:** animated starfield, god orbs that gently float, group dividers with sub-labels, expandable god cards with red `⚿ GM Secret` pills, planar-layer expandables
- **References:** `index.html` (cosmology landing), `grand-gods.html` (the pantheon), `magic.html`

### Style B — Grounded / Continent + Settlement-level
Used for: continent primer, domain pages, faction pages, town primers, district guides, NPC rosters, anything ground-level and lived-in.

- **Source:** `/assets/style-b.css`. Pages set a custom `--domain-accent` in a small inline `<style>` when they want one.
- **Fonts:** Uncial Antiqua (page titles), Crimson Pro (body), Cinzel (labels/small caps)
- **Palette:** warm dark (`--bg: #0f0c08`), gold accents (`--gold: #c8900a`, `--gold-bright: #f0b020`), parchment text (`--text: #d0c8a8`), per-domain accent colour driven by the location's character
- **Signature elements:** parchment noise overlay, ornament dividers (`✦ · ✦ · ✦`), "At a Glance" facts panel, god-city callout boxes, sub-region grid cards, timeline + era cards, amber `◈` Popular Belief + red `⚿` GM Secret expandables
- **References:** `talan/talan.html` (continent overview), any of `talan/domains/<domain>/<domain>.html` (domain page), `talan/factions/adventurers-guild.html` (faction page)

---

## How we work together — drafting → publishing

**Lore-first protocol.** When the user is brainstorming new content — a kingdom, an NPC, a magic ritual, a faction, a god's secret — capture it into the right `lore/` markdown file, not directly into HTML. Lore files are the draft space and evolve freely. HTML pages are the published output: clean, polished, navigable.

**Stay in lore by default.** A new session starts in drafting mode. Claude should not generate or modify HTML pages until the user gives an explicit publish signal — phrasings like *"add this to the page"*, *"publish it"*, *"render the page"*, *"make it live"*, *"put it on the site"*, or similar. If the intent is ambiguous, ask before touching HTML.

**Pause between lore-write and HTML-publish — always, even with a publish signal.** When new content is being created (not just polishing existing canon), the lore-write and the HTML-mirror are two separate phases, and the user wants to review the lore before it's mirrored to HTML. Even when the original instruction was *"write out the history"* or *"publish this"* — when the lore is fresh content, write it into `lore/`, then **stop and surface what landed** so the user can correct details (timing, characters, public-vs-secret partition, canon implications) before the HTML lock-in. Mirroring to HTML before the lore is confirmed creates double-edit work when corrections come. The pause is mandatory; the user will say *"go ahead and publish"* to release it. Polish-only or wiring-only follow-ups (sidebar nav, site-inventory, open-threads closure) can chain after the HTML publish without a second pause.

**Published HTML is lore documentation, not a campaign starter.** Pages should read as reference material — what exists in the world, why, how, and who. **Do not add dedicated "Hooks" or "Adventure Seeds" sections** with campaign prompts ("a campaign that crosses the two…", "a Yaksha exile whose bond was broken could open…"). Campaign-side material belongs in private GM notes, not on the published site. World-flavour expandables — folkloric *Popular Belief* (amber ◈), in-world tavern rumours, *What People Say* speculation — are different and welcome: they characterise *the world*, not *what to do in it*.

**Surface phase boundaries for review — don't chain them.** On multi-step work (e.g. publishing several pages, restructuring multiple docs, a coherent lore restructure across several files), pause at the seam between phases and surface what landed + what's next, even when given a broad "work through it" instruction. A phase boundary is a review checkpoint, not a clarifying question — these pauses are wanted even under "work without stopping for clarifying questions" framing. Survey work and reading source files is fine within a phase; *writes* are what trigger the boundary.

**Where new content goes:**

| Topic | File |
|---|---|
| How the world works — Wellspring, belief mechanic, planar layers, magic schools, Magitech, Gods' Law mechanics, calendar | `lore/cosmology.md` |
| Who the gods are — the Thirteen, named non-bound gods, gods' city-states, Council, cleric domains | `lore/gods.md` |
| What really happened — Crimson Rain, Cronus's secret, Storveldi Denbora, Elden / Corrupted God, Wardstones, Nine Generals, Tani & Araphel deep-dives | `lore/secret-history.md` |
| Domains, sub-regions, kingdoms, settlements, terrain | `lore/geography.md` |
| Factions, guilds, churches, organisations | `lore/factions.md` |
| Peoples, traditions, politics, craft, warfare | `lore/cultures.md` |
| Playable ancestries (PF2e), heritages, otherworldly beings (virtue-demons, sin-devils, etc.) | `lore/bestiary.md` |
| New coined names + etymologies | `lore/glossary.md` (always — see naming rule) |
| Eras, historical events, dates | `lore/timeline.md` |
| Something entirely new that doesn't fit above | new file in `lore/` (e.g. `lore/spells.md`) |

When coining new names, always record the source language, literal meaning, and drift step in `glossary.md` *before* using the name elsewhere — the glossary is the source of truth for derivation.

**On the publish signal**, identify the target HTML page from the layer-to-folder mapping above, pick the matching style (A or B), and either edit the existing page or create a new one. After publishing, update `docs/site-inventory.md` to reflect any new or now-populated pages.

---

## Working across sessions (and via Cowork Dispatch)

This project is designed so a fresh Claude session — a new chat, a new Cowork session, or a task dispatched from your phone — can pick it up with no prior context. Everything Claude needs is in the repo:

1. **Read `CLAUDE.md` first** — naming rule, folder layout, style guide, drafting protocol.
2. **Read whichever `lore/` files are relevant** to the topic at hand.
3. **Skim `docs/site-inventory.md`** to know what's already published vs. stub.
4. **Check `docs/open-threads.md`** if the user references an ongoing canon question — it lists every TBD/unresolved thread with status and where it lives.

Don't rely on the user's in-session memory file for canon — that's a summary, not the source. The lore files win.

### Migration state (as of 2026-05-17)

- **WorldAnvil → lore migration: COMPLETE.** The `worldanvil-export/` folder has been retired from the repo. All canon now lives in `lore/`.
- **Lore → HTML publishing: COMPLETE.** All four migration phases (cosmology, geography, factions, bestiary) shipped to HTML. Remaining work is incremental Tier 5/6 worldbuilding tracked in [`docs/open-threads.md`](docs/open-threads.md) and [`docs/site-inventory.md`](docs/site-inventory.md)'s *Future Work* section. The user holds the publish signal; do not push new lore to HTML without an explicit go-ahead.

### Using Cowork Dispatch

Cowork's Dispatch feature lets you assign tasks to Claude from your phone (or another spot) and Claude executes them on the desktop. For Tyrnarra:

- The Tyrnarra folder must be selected as the Cowork workspace so the dispatched session can read and write the files.
- The Claude Desktop app must be installed, running, and the computer awake when the task fires.
- Dispatched tasks can be terse — e.g. *"In Tyrnarra, design a coastal city called Veldtmark in Brauogi"* — because Claude will read `CLAUDE.md` and the relevant lore files to learn the conventions and existing canon.
- The drafting protocol still applies: a dispatched session captures to `lore/` and doesn't render HTML unless the task includes the publish signal.
