# Tyrnarra: Worldbuilding Project

This repo is a personal worldbuilding project for the setting **Tyrnarra**. The deliverable is a static HTML site published via GitHub Pages from the **`published/`** folder (served as the site root by a GitHub Actions workflow; the `/published/` prefix is stripped at deploy, so the worldbuilding site is live under `/setting/…`). Pages are hand-crafted HTML; **shared chrome lives in `/setting/assets/`** (sidebar nav, Style A and Style B base CSS) and is referenced via `<link>` and `<script defer src>` tags. Page-specific styling and unique content stay inline in the page itself.

For getting the site running locally, see [`README.md`](README.md). For what's currently published vs. stub, see [`docs/site-inventory.md`](docs/site-inventory.md). For how the persistent sidebar works, see [`docs/sidebar-nav.md`](docs/sidebar-nav.md). For the session-spanning workflows that take content from idea to published page, see the workflow skills (`sub-region-workflow`, `god-city-workflow`, `quest-workflow`, `virtue-devil-workflow`, plus the `pf2e-encounter` / `pf2e-loot` / `grill-me-lore` helpers) under [`.claude/skills/`](.claude/skills/). For the in-repo **campaign layers** (the GM-only `/gm-notes/` table material and the player-facing, published `/player-campaigns/` companion), see [`docs/campaign-layer.md`](docs/campaign-layer.md).

---

## The naming convention (most important rule)

**For anything new you create**, follow this convention strictly:

- **Old or ancient things** (ruins, kingdoms, geographic features, deity names, anything pre-modern or "of the world itself") are named by:
  1. Translating a meaningful word or phrase into **Basque** or **Icelandic**
  2. Then slightly altering it to represent linguistic drift over time

  Example: *"Ehizahar"* (Hunt domain of Hinka) comes from Basque *"ehiza"* (hunt) + *"zahar"* (ancient), naturally eroded to its current form. Drift can happen anywhere in the word, not just the end.

- **New or modern things** (recently founded institutions, contemporary city-states, modern organizations) are named **plainly in English** but they may have drifted lightly.

  Examples: *"Free City"* → *"Frae City"*, *"Order of Steam"*, *"The Wayward Compass"*, *"Clearwater Exchange"*.

**When you coin a new name, always show your work**: note the source language, the literal meaning, and the drift step. Save it in `lore/glossary.md` so the etymology is preserved.

**Existing names predate this rule.** Don't try to retrofit names that are already in the HTML pages (Forseti, Cronus, etc.). Just follow the rule going forward.

**Regional cultural registers are a third stratum, not exceptions.** The Basque/Icelandic-with-drift rule covers the deep-old layer and the English-with-drift rule covers the modern layer; alongside both, every region has its own naming register a mortal born there will follow (Fenurran Latinate, Kotokoe-kitsune, Sortalde dynastic, Haizetsua-Tengu, etc.). A name in a regional register is not a rule-exception and does not need meta-flagging in lore as "pre-rule" or "predates the convention". It is simply a name from where its bearer was born.

**Kingdoms inherit names, not continuity.** A kingdom's *name* belongs to the old-and-ancient stratum (Basque/Icelandic with drift), but the *polity carrying that name* is almost never that old. **No Talanese kingdom predates 1 MR**; few are older than the Dark Era; most modern kingdoms were founded, refounded, or substantially redrawn during the Dark Era (1321 MR – 2135 MR) or in the immediate post-Dark-Era reconstruction, and they routinely *re-claimed* the older Lost-Era kingdom-names that had occupied the same ground centuries earlier. When you coin a new kingdom or write a founding date, default to a Dark-Era or early-Adventurer-Era founding unless the page makes the older-claim a deliberate story feature. Full canon: [`lore/timeline.md`](lore/timeline.md), *Kingdom continuity across the eras*.

---

## File layout

The site is hierarchical: **Tyrnarra → Talan → Domains → Sub-Regions/Kingdoms → Settlements.** The folder tree mirrors the world. The whole worldbuilding site ships from `published/setting/` and is served at `/setting/…`: world-level (cosmic) content under `/setting/cosmology/`, continent-level content under `/setting/talan/`. The schematic below shows the *pattern*; for the actual file roster + publish status, see [`docs/site-inventory.md`](docs/site-inventory.md).

```
/                                      ← repo root (NOT served; only published/ ships to the web)

  published/                           ← GitHub Pages serves THIS folder as the site root
    index.html                         ← root redirect → /setting/
    CNAME · robots.txt · favicon* · site.webmanifest   ← served-root files

    setting/                           ← the worldbuilding site (served at /setting/…)
      index.html                       ← cosmology / world primer (the homepage the / redirect targets)
      cosmology/                       ← world-level (cosmic) Style A pages
        grand-gods.html, gods.html, gods-law.html, magic.html,
        bolverk.html, primordials.html, layer-3-gods.html, pf2e-registrar.html
      talan/                           ← continent-level content (Style B)
        talan.html                     ← continent overview
        history.html, ancestries.html, …   ← other continent-level pages
        domains/                       ← the 13 god domains
          <domain>/<domain>.html       ← e.g. vindul/vindul.html, domain entry page
          <domain>/<sub-region>.html   ← optional: promoted sub-region with its own page
          <domain>/<settlement>/       ← settlement folder, when content warrants
            <settlement>.html          ← folder's main page, same name as the folder
            <sub-location>.html        ← location within the settlement
                                         (quests + GM/table material live in /gm-notes/, NOT here)
        factions/                      ← independent organisations
        historical/                    ← fallen civilisations
        the-binding/                   ← Nine Generals dungeons
      off-continent/                   ← non-Talan continents & powers
      assets/                          ← shared chrome (loaded by every setting page)
        site-nav.css / site-nav.js     ← sidebar (single source of truth for menu)
        site-interactions.js           ← shared toggle handlers (Popular Belief ◈, GM Secret ⚿, era cards)
        site-starfield.js              ← generates the cosmic-page starfield (Style A only)
        style-a.css                    ← Style A base, /setting/cosmology/ pages
        style-b.css                    ← Style B base, every page under /setting/talan/ and /setting/off-continent/

    gm-notes/                          ← GM / table material (served at /gm-notes/, unlinked from sidebar)
      assets/                          ← gm.css / gm.js / gm-nav.css / gm-nav.js (shared GM chrome)
      tools/map-area-editor.html       ← the one browser tool kept published (draw clickable map areas → JSON)
      <campaign>/                      ← per-campaign hub: GM town notes, location dossiers, quests
        assets/maps/                   ← downsized web map copies (committed); _full/ = full-res, gitignored (paid art stays local)

    player-campaigns/                  ← player companion (served at /player-campaigns/; its own pc-nav menu)

  tools/                               ← PRIVATE GM build tooling (NOT served)
    encounterBuilder/                  ← PF2e encounter + loot builders (pf2e-encounter / pf2e-loot skills)
    imageGen/                          ← NPC art generation, local ComfyUI/FLUX.2, Claude-operated (npc_art.py + npc-art skill)
    foundryExport/                     ← quest spec → paste-and-run Foundry VTT import macro (+ token bake / Forge upload)
    map-library/                       ← reusable map catalogues (+ local-only _full/ source art)
    token-frames/                      ← shared Foundry token-frame library
    keys/                              ← gitignored API keys (Forge), copied from Proton Drive

  lore/                                ← worldbuilding canon (NOT served; full roster in site-inventory)
    cosmology.md · gods.md · factions.md · ancestries.md · glossary.md · timeline.md
    geography/                          ← per-place canon: one <domain>.md per god domain, plus
                                          _continent.md · _off-continent.md · bolverk.md, and
                                          deep-culture sub-region files (e.g. lautara/emarrea.md)
    (the topic → file map is the "Where new content goes" table below)

  docs/                                ← site documentation (NOT served)
    site-inventory.md                  ← canonical roster of every page + publish status
    sidebar-nav.md                     ← architecture notes on shared sidebar + assets
    open-threads.md                    ← gate-tracked canon work (Needs writing / fleshing / publishing)
    accessibility.md                   ← WCAG 2.1 AA contract: contrast palette, focus styles, ARIA
    card-conventions.md                ← clickable-card pattern: whole-card-link + ` →`, no inner anchors
    campaign-layer.md                  ← architecture of the campaign layers (GM /gm-notes/ + player /player-campaigns/)
    ancestry-conventions.md            ← how to write a Tyrnarra ancestry (feeling-first; from the 2026 rebalance)
    god-city-seeds.md                  ← locked seeds + build roster of the thirteen god-cities (pass complete)

  .github/workflows/pages.yml          ← deploy: upload published/ → GitHub Pages (Actions)
  CLAUDE.md · README.md · .gitignore · serve.bat / serve.sh
```

**`lore/` vs. `docs/`**: `lore/` is the source of truth for what's *true in the world*. When an HTML page disagrees with a lore file, the lore wins. `docs/` is the source of truth for *how the site is built*. They have different update rhythms: canon evolves with the world; docs drift with the code.

### Layer-to-folder mapping

| World layer | Folder | Example |
|---|---|---|
| World (Tyrnarra) | `/setting/` + `/setting/cosmology/` | `index.html` at `/setting/index.html`; `grand-gods.html`, `magic.html` at `/setting/cosmology/…` |
| Continent (Talan) | `/setting/talan/` | `talan.html`, `history.html` |
| Region (god domain) | `/setting/talan/domains/<domain>/` | `/setting/talan/domains/vindul/vindul.html` |
| Sub-region / Kingdom | section in domain page, or own file when promoted | `Thousand Kingdom` lives inside `zuzental.html` until it earns its own file |
| Settlement | folder under its domain | `/setting/talan/domains/lautara/millhaven/millhaven.html` |
| Sub-location of settlement | sibling file in settlement folder | `/setting/talan/domains/lautara/millhaven/wayward-compass.html` |
| Quest / GM table material | GM campaign layer (GM-only, served at `/gm-notes/`, unlinked from the sidebar) | `/gm-notes/<campaign>/quest-<slug>/quest-<slug>.html` (own folder, folder-named page) |
| Player campaign companion | player campaign layer (player-facing, published, its own `pc-nav` menu) | `/player-campaigns/<campaign>/<page>.html` |
| Faction (independent org) | `/setting/talan/factions/` | `/setting/talan/factions/adventurers-guild.html` |
| God church | umbrella `god-churches.html`; promoted to its own file when content warrants | `/setting/talan/factions/god-churches.html` |

### Conventions

- **Folder slugs** are lowercase ASCII with hyphens. Diacritics are stripped from slugs but kept in display titles.
- **Each settlement gets its own folder under its domain.** The folder's main page is named the same as the folder (`millhaven/millhaven.html`).
- **Sub-regions** start as sections inside the domain page. When one earns enough content, promote it to its own file in the domain folder (e.g. `zuzental/thousand-kingdom.html`). Don't create empty stub files for sub-regions that don't exist yet.
- **Kingdoms vs. sub-regions:** "sub-region" is the umbrella; some sub-regions are kingdoms (Thousand Kingdom, Order of Steam), others are geographic (Baerfrost), cultural (Tahu Tangata), or border territories (Haldmark). All live in the same place in the folder tree; the political type is a property, not a folder.
- **Always use absolute paths in links** (starting with `/`). The sidebar uses absolute paths and so does cross-linking between pages.
- **Dark mode only.** All pages assume a dark background.
- **Mobile responsive.** Pages use `@media (max-width: 600px)` breakpoints; match this.
- **Accent colours must clear 3:1 contrast** against `--bg`. New `--domain-accent` values (and any colour used as a card stripe, border, or load-bearing graphic) need to pass the graphic-contrast floor; moody-dark is fine, invisible isn't. See [`docs/accessibility.md`](docs/accessibility.md) for the contrast check (`node tools/contrast.mjs '#hex'`) and the rest of the WCAG 2.1 AA contract (focus styles, aria-expanded on toggles, glyph + label not colour alone).
- **Cards declare their interaction in the title row.** Clickable cards (whole card is an `<a>`) carry a trailing ` →` in the title. Expandable cards (in-place reveal) carry a small bordered `Tap ▾` pill (`.expand-hint`) in their header. Plain `<div>` cards carry neither. Inner anchors inside a clickable card's body are forbidden (use plain `<b>` instead). Full spec, reference implementations, and pitfalls in [`docs/card-conventions.md`](docs/card-conventions.md).
- **No build step.** Open in a local server, it just works. (See README.md for the local server.)
- **Tone in copy:** specific over generic. Small concrete details (the smell, the named NPCs, the inside-joke aside) over abstract worldbuilding.

---

## Persistent sidebar navigation

Every **setting** page references the shared worldbuilding sidebar by including two tags in `<head>`:

```html
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
```

The page declares its location for the highlight via `<body data-page="vindul">`.

To add or rename a page in the sidebar, edit `/setting/assets/site-nav.js`: one file, one place. Full architecture (data arrays, section-header pattern, accordion behaviour) in [`docs/sidebar-nav.md`](docs/sidebar-nav.md).

The campaign layers carry their **own** menus, not this one: `/gm-notes/` uses `gm-nav.*` and `/player-campaigns/` uses `pc-nav.*`, each its own source-of-truth tree (see [`docs/campaign-layer.md`](docs/campaign-layer.md)).

---

## Two page styles (worldbuilding pages)

Worldbuilding pages under `/setting/` use one of two visual modes. New setting pages should pick one and match it closely; don't invent a third without asking. (The campaign layers carry their own chrome, not Style A/B: `/gm-notes/` uses `gm.css` and `/player-campaigns/` uses the themeable `campaign.css`; see [`docs/campaign-layer.md`](docs/campaign-layer.md).)

### Style A: Cosmic / World-level
Used for: the landing/cosmology, the 13 gods, magic; anything world-scale or mythic.

- **Source:** `/setting/assets/style-a.css`. Page-specific tweaks (orb effects, soul bars) stay inline in the page itself.
- **Fonts:** Cinzel Decorative (page titles), Cinzel (labels, small caps), Crimson Pro (body)
- **Palette:** deep void (`--bg: #06060a`), purple/blue ambient gradients, gold accents (`--gold: #c8a84a`, `--gold-bright: #f0d080`), parchment text (`--text: #c8c4d8`), per-god accent colours
- **Signature elements:** animated starfield, god orbs that gently float, group dividers with sub-labels, expandable god cards with red `⚿ GM Secret` pills, planar-layer expandables
- **References:** `/setting/index.html` (cosmology landing), `/setting/cosmology/grand-gods.html` (the pantheon), `/setting/cosmology/magic.html`

### Style B: Grounded / Continent + Settlement-level
Used for: continent primer, domain pages, faction pages, town primers, district guides, NPC rosters, off-continent powers, anything ground-level and lived-in. Every page under `/setting/talan/` and `/setting/off-continent/` uses Style B.

- **Source:** `/setting/assets/style-b.css`. Pages set a custom `--domain-accent` in a small inline `<style>` when they want one.
- **Fonts:** Uncial Antiqua (page titles), Crimson Pro (body), Cinzel (labels/small caps)
- **Palette:** warm dark (`--bg: #0f0c08`), gold accents (`--gold: #c8900a`, `--gold-bright: #f0b020`), parchment text (`--text: #d0c8a8`), per-domain accent colour driven by the location's character
- **Signature elements:** parchment noise overlay, ornament dividers (`✦ · ✦ · ✦`), "At a Glance" facts panel, god-city callout boxes, sub-region grid cards, timeline + era cards, amber `◈` Popular Belief + red `⚿` GM Secret expandables
- **References:** `/setting/talan/talan.html` (continent overview), any of `/setting/talan/domains/<domain>/<domain>.html` (domain page), `/setting/talan/factions/adventurers-guild.html` (faction page)

---

## Chronicler's voice: what's public, what's behind the seal

Published **worldbuilding** (`/setting/`) pages are **player-facing**. Open prose reads as something an in-world chronicler of Talan would actually write, hedged where the chronicle-record is hedged, ignorant where mortals are ignorant. **GM-tier truth never goes in open prose**; it lives inside expandable boxes only. **The lore files mark GM-tier inline** with a `⚿ GM Secret:` heading prefix (the lore-side equivalent of the HTML expandable; same content, same visibility-discipline). HTML pages stratify the same content into expandable boxes. This applies to both Style A and Style B pages.

**Three tiers, three treatments:**

| Tier | Box | Contents |
|---|---|---|
| **Chronicler** | Open prose | What a scholar in-world could plausibly write: disputed scholarship, *"the chronicles say…"* framing, named-but-debated facts. |
| **Folk-belief** | Amber `◈ Popular Belief` expandable | Tavern-tales, sermons, traveller's accounts; what mortals *say*, including the parts that are wrong. |
| **GM-tier** | Red `⚿ GM Secret` expandable | The actual truth: mechanisms, identities, cosmological reality. Hidden until clicked. |

A useful gut check: **if a chronicler reading the open prose would learn something the lore files mark as GM-only, it's leaking.** Move it inside the secret box. The *Open in Canon* panel at the bottom of a page is open prose too. Keep it chronicler-tier; put GM-tier "open threads" inside the secret block they relate to.

**Use multiple secret boxes per page.** A single secret at the bottom of a long page is a wall of text. Split secrets by topic and place each one immediately after the open-prose section it answers; the reader gets *"the chronicles disagree about X"* in the prose, clicks, and sees *"what X actually was."* Four or five thematic boxes on a long page is fine.

**Theme secret boxes with the page's full visual vocabulary.** Cards, grids, pill rows, italic reveal-intros, side-by-side comparisons, codas: same scaffolding you'd use in open prose, just inside the box. If cards need a darker background to read against the secret-box tint, override `--card-bg` with a darker tinted value (e.g. `rgba(46,14,18,0.55)` for red-secret-tinted cards). Treat each secret as a structured reveal, not a paragraph.

**Reference implementations:**
- [`published/setting/talan/historical/storveldi-denbora.html`](published/setting/talan/historical/storveldi-denbora.html): four thematic GM Secret boxes, each with reveal-pills, themed cards (claim-vs-truth, three-tier court, three fragment-locations) and italic codas. The model for *multiple themed secrets per page*.
- [`published/setting/talan/historical/golden-empire.html`](published/setting/talan/historical/golden-empire.html): a single consolidated GM Secret box. The model for when *one continuous reveal arc* makes more sense than splitting.

---

## How we work together: drafting → publishing

**Read the canon before designing on top of it.** Before drafting anything new whose design *touches* an established canon event (Crimson Rain, Gods' Law forging, Tani's death, the Storveldi Denbora, the Elden / Corrupted God, the Mortal Ascent Ladder, Bolverk soul-routing, the Council, individual Grand Gods), **read the relevant lore file end-to-end first**, not a grep, not a skim. The roster of what each file covers is in [`docs/site-inventory.md`](docs/site-inventory.md), under *Lore files*. The test: if the user could reasonably point at the draft and say *"that contradicts what's in `<file>`,"* you should have read `<file>` first. Reading mid-design is a fix; reading before drafting is the rule.

**Write affirmatively.** Say what something *is*, not what it *isn't*. Don't open sentences with *"Not …"* or *"No …"*; avoid *"not X but Y"* constructions. If you're tempted to write *"not a Council god,"* the affirmative version (*"his own god, of his own pantheon"*) is always available and always better. Strip the negation and rewrite from what's actually true. **Sole exception:** when a true negation is the clearest framing for a fact that has no affirmative form (*"his cult kept no records"*, *"the Cloud Sea will not support weight"*). When in doubt, prefer the affirmative.

**Avoid em-dashes.** Don't use em-dashes in new prose, lore files, or HTML. They're a tell of AI drafting and they pile up fast. Reach for a period, a semicolon, a colon, parentheses, or a comma first; if none of those work, rewrite the sentence. En-dashes are fine for numeric ranges (e.g. *1321 MR – 2135 MR*).

**Mortals, not humans.** Talan has more than a dozen ancestries; *Human* is one specific people (Zuzental's, beside the Elves), not the word for people-in-general. When you mean persons generically, write *mortals*, *folk*, *people*, *no one*, *anyone*, never *humans* or *mankind*. The generic-human reflex is strong and easy to fall into; catch it in revision.

**Ancestries are a feeling, not a job.** An entry in `lore/ancestries.md` says what a people *is*: the temperament, the disposition (Kholo "keep their own"; Minotaurs "outlast"; Dragonets "the old blood"). A vocation, a culture, or a settlement-history baked into the feeling (the herder-clans, the miners, Fetchling's old "many serve Araphel") is stale lore that belongs to *a place*, not the species; the same feeling wears a different life in every region it appears in. When you build on an anchor ancestry, first verify its entry is feeling-only, and strip any baked-in vocation down into the region that carries it. Older entries commonly still hold one, so expect to fix more than one anchor in a domain. (Heritage and cosmology, like the Dragonet Wyrmkin line, are *what the people is* and stay.)

**Lore-first protocol.** Brainstormed content (a kingdom, an NPC, a ritual, a faction, a god's secret) goes into the right `lore/` markdown file, not directly into HTML. Lore files are the draft space; HTML pages are the published output.

**Stay in lore by default.** A new session starts in drafting mode. Don't generate or modify HTML pages until the user gives an explicit publish signal: phrasings like *"add this to the page"*, *"publish it"*, *"render the page"*, *"make it live"*, *"put it on the site"*. If the intent is ambiguous, ask.

**Always pause between lore-write and HTML-publish, even with a publish signal.** When the content is *new* (not polishing existing canon), the lore-write and HTML-mirror are two phases. Even if the original instruction was *"write out the history"* or *"publish this"*: write the lore, then **stop and surface what landed** so the user can correct details (timing, characters, public-vs-secret partition, canon implications) before HTML lock-in. The user will say *"go ahead and publish"* to release it. Polish-only or wiring-only follow-ups (sidebar nav, site-inventory, open-threads) can chain after the HTML publish without a second pause.

**Published worldbuilding HTML is reference material, not a campaign starter.** **Do not add "Hooks" or "Adventure Seeds" sections** with campaign prompts ("a campaign that crosses the two…", "a Yaksha exile whose bond was broken could open…") to `/setting/` pages. Campaign-side material lives in the in-repo **campaign layers** instead: GM-tier material (quests, stat blocks, read-aloud boxes, adventure hooks, GM-tier location detail) in the GM-only, sidebar-unlinked `/gm-notes/<campaign>/`; the player-facing companion (town/location handouts, the interactive quest board, with all GM-tier content stripped) in the published `/player-campaigns/<campaign>/`. The *Furrious Five* layer (present in both) is the reference implementation; see [`docs/campaign-layer.md`](docs/campaign-layer.md) for the architecture (the GM/player split, the GM chrome, the clickable-battlemap pattern + the `map-area-editor` tool, and the rule that paid full-res maps stay local-only in `maps/_full/`). World-flavour expandables are welcome on worldbuilding pages: folkloric *Popular Belief* (amber ◈), in-world tavern rumours, *What People Say* speculation. They characterise *the world*, not *what to do in it*. A `PostToolUse` guard hook (`.claude/hooks/gm-notes-link-guard.mjs`, registered in `.claude/settings.json`) backstops the split: it warns whenever an edit leaves an actual link to `/gm-notes/` in a `/setting/` or `/player-campaigns/` file (prose or comment mentions are fine); it only flags, never blocks.

**Surface phase boundaries rather than chaining them.** On multi-step work (publishing several pages, restructuring multiple docs, a coherent lore restructure across files), pause at the seam between phases and surface what landed + what's next, even under a broad "work through it" instruction. Phase boundaries are review checkpoints, not clarifying questions; they're wanted under "work without stopping for clarifying questions" framing too. Reading is fine within a phase; *writes* trigger the boundary.

**The GM-Vetted badge.** A page the GM has personally read through and corrected carries a **GM-Vetted** badge at the top of the page, under the title (so players see at a glance that the page is current): an HTML comment `<!-- gm-vetted: YYYY-MM-DD ... -->` plus a `<div class="gm-vetted">` pill (styled in `/setting/assets/site-nav.css`). The badge is the visible mark that a human signed off on that page's prose. **Only the GM grants it** (when he says a page is vetted); never add or re-add a badge on your own initiative. A `PostToolUse` hook (`.claude/hooks/gm-vetted-check.mjs`, registered in `.claude/settings.json`) fires whenever a vetted `.html` page is edited and reminds you to **judge whether the edit was more than minor**. If it was a real prose, structural, or canon change, **strip the badge** (delete both the comment line and the `gm-vetted` div) so the page no longer claims a sign-off it no longer has; if it was trivial (typo, single word, whitespace, one punctuation swap), leave the badge in place. The hook only flags; the minor-vs-major call is yours, and stripping is the conservative default when unsure. **The badge is about prose/canon, not chrome:** adding or restyling pure-navigation furniture that doesn't touch the page's lore (a shared `.see-also` "Continue Reading" panel, an `.open-canon` re-wrap, a sidebar/cross-link change) is **not** a badge-stripping edit; leave the badge in place.

**Where new content goes:**

| Topic | File |
|---|---|
| How the world works: Wellspring, belief mechanic, planar layers, magic schools, Magitech, Gods' Law mechanics, calendar | `lore/cosmology.md` |
| Who the gods are: the Thirteen, named non-bound gods, gods' city-states, Council, cleric domains | `lore/gods.md` |
| What really happened (GM-tier secrets) | **No central file.** Each secret lives with the canon it shadows, marked with a `⚿ GM Secret:` heading prefix. Examples: Cronus's mortal origin and Tani's death/rebirth in `gods.md` (per-god sheets); the Week of Crimson Rain True Account, the Storveldi Denbora, the Elden / Wyrmkin, and the Lost/Golden/Dark-Era real-histories in `timeline.md` (per-era sub-sections); the Seven Wardstones in `geography/myrkono.md`; the Dreaming Cape Real History in `geography/lautara.md`; the Nine Generals in `factions.md` (under *Remnants of Corruption*); the Devourer and the Corrupted God's true identity in `cosmology.md`. The `⚿ GM Secret:` heading prefix is the lore-side equivalent of the HTML `⚿ GM Secret` expandable: same content, same visibility-discipline. |
| Domains, sub-regions, kingdoms, settlements, terrain | `lore/geography/<region>.md` (one file per god domain) + `lore/geography/_continent.md` (Talan-continental frame, seas, rail, domain index) + `lore/geography/_off-continent.md` (Sortalde + Red Empire) + `lore/geography/bolverk.md` (the megacity in Abyss). Each domain file declares its land borders at the top; when designing on top of a domain, read its file *and* the files of its bordering domains. |
| Factions, guilds, churches, organisations | `lore/factions.md` — but only for **cross-domain** organisations (Adventurers' Guild, Mercenary Guild, Voroir Daua, Remnants of Corruption, etc.). Region-bound institutions (state religions of single polities, noble houses of single kingdoms, named taverns) live in the relevant `lore/geography/<region>.md` file, not here. |
| Peoples, traditions, politics, craft, warfare | Deep-culture peoples live with their place: **Fenurrans** in `lore/geography/ehizahar/fenurra.md`, **Kitsune** in `lore/geography/lautara/emarrea.md`, **Tengu** in `lore/geography/vindul/haizetsua.md`, **Sortalde peoples** in `lore/geography/_off-continent.md`. Pan-Talan canon (the common tongue, cross-cultural patterns) lives in `lore/geography/_continent.md` (*Languages* section). |
| Playable ancestries (PF2e), heritages, lifespan, domain distribution | `lore/ancestries.md` (deep-culture peoples carry one-line stubs that point to their `lore/geography/<domain>/<sub-region>.md` file) |
| Bolverk (the megacity in Abyss), Vice Demons, Virtue Devils, the Tunsund, soul-routing from Dauria, individual demon/devil seat-holders | `lore/geography/bolverk.md` (Bolverk is a place; its city geography and the factions inside it live in the geography folder) |
| New coined names + etymologies | `lore/glossary.md` (always; see naming rule) |
| Eras, historical events, dates | `lore/timeline.md` |
| Something entirely new that doesn't fit above | new file in `lore/` (e.g. `lore/spells.md`) |

When coining new names, always record the source language, literal meaning, and drift step in `glossary.md` *before* using the name elsewhere; the glossary is the source of truth for derivation.

**On the publish signal**, identify the target HTML page from the layer-to-folder mapping above, pick the matching style (A or B), and either edit the existing page or create a new one. After publishing, update `docs/site-inventory.md` to reflect any new or now-populated pages.

**Commit and push per completed phase.** When a lore-write phase is complete and surfaced, or an HTML-publish phase is complete (the page edited or created, plus its wiring: sidebar nav, `docs/site-inventory.md`, `docs/open-threads.md`), commit that work with a descriptive message and push. Commit at the phase boundary, not per file edit, and hold off on committing mid-phase or un-reviewed drafts. The lore-write and the HTML-publish are separate phases (see the pause rule above), so they are separate commits. **Stage only the files this session touched since its last commit.** Multiple Claude sessions routinely run in this one working tree at the same time, so `git add -A`, `git add .`, and `git commit -a` are forbidden: they sweep another session's in-progress edits into your commit and push them half-finished under your message. Always stage explicit paths you created or changed this session (e.g. `git add lore/geography/vindul.md published/setting/talan/domains/vindul/vindul.html`); run `git status` first and confirm every staged file is one you actually touched. If `git status` shows modified files you did not edit, leave them unstaged: they belong to a concurrent session. Write a real message naming what landed (`Add Itsasalda Vordsbench canon`, `Publish Frae City god-city page`), not a generic one. This is the project's standing authorization to commit and push straight to `main` for these phases: no need to ask each time, and no need to branch first (a push to `main` triggers the GitHub Actions deploy of `published/`). A `PostToolUse` reminder hook (`.claude/hooks/git-commit-reminder.mjs`, registered in `.claude/settings.json`) nudges you after any `lore/` or `.html` edit; it only reminds and never runs git. You run the commit and the push yourself, with judgment about whether the phase is truly done.

---

## Working across sessions

This project is designed so a fresh Claude session can pick it up with no prior context. Everything Claude needs is in the repo:

1. **Read `CLAUDE.md` first**: naming rule, folder layout, style guide, drafting protocol (including the pre-read rule and the affirmative-prose rule).
2. **Skim `docs/site-inventory.md`** to know what's already published, what's stub, and (in the *Lore files* section at the top) which `lore/` file covers which topics. The pre-read rule routes through this table.
3. **Read the relevant `lore/` files end-to-end** before drafting content that touches their canon; the *Lore files* section tells you which.
4. **Check `docs/open-threads.md`** if the user references an ongoing canon question; it lists every TBD/unresolved thread with status and where it lives.
5. **For GM table / quest work**, read [`docs/campaign-layer.md`](docs/campaign-layer.md) and drive the relevant workflow skill (`quest-workflow`, `pf2e-encounter`, `pf2e-loot`); that material lives in the campaign layers, never on the worldbuilding pages.

Don't rely on the user's in-session memory file for canon; that's a summary, not the source. The lore files win.
