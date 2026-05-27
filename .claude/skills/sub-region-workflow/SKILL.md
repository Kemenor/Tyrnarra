---
name: sub-region-workflow
description: Use this skill whenever working on a Talanese sub-region (kingdom, free city, theocracy, mendicant order, guild-state, merchant republic, federated free-towns, march, clan-confederation, nomadic confederacy, or any polity smaller than a continent) within the Tyrnarra worldbuilding project. Trigger on phrases like "flesh out [name]", "let's design [polity]", "new sub-region in [domain]", "what should [domain]'s [feature] be", "promote [name] to its own page", "build the page for [name]", "we have a label on the map but no canon for X", working with TBD sub-region entries in docs/open-threads.md, drafting bullets in lore/geography/<region>.md sub-region sections, or any session that takes a label-on-the-map to fully fleshed canon. Also use when the user references the Baerfrost, Air Monastery / Wyndwalken, or Fellibylur exemplars as patterns to follow. The skill enforces a strict seven-phase workflow with surface-before-writing pauses, the kingdoms-inherit-names rule, the Basque/Icelandic/English naming-stratum check, the collision check on reserved names (Compact, Order), the lore-pre-read step, and the lore-first / surface-before-HTML protocol from CLAUDE.md. Do not use for cosmology or pantheon work, quest design unconnected to founding or refounding a polity, NPC dossiers in already-established sub-regions, or HTML edits to pages that already exist for unrelated reasons.
---

# Sub-region workflow

## What this skill is for

Taking a sub-region from "label on the map" (a one-liner stub in `lore/geography/<region>.md`, a TBD entry in `docs/open-threads.md`, or a freshly named region on a hand-drawn map) to fully fleshed canon, and optionally to a dedicated HTML page, inside a single session, with the user's voice setting direction at every phase boundary.

This applies to anything that needs its own polity-shape and signature institution(s) and stops short of a continent: kingdoms, factions-as-polities, orders, theocracies, confederations, free cities, mendicant brotherhoods, guild-states. The exemplars are the three Vindul sub-regions promoted on **2026-05-24**: **Baerfrost** (Hunt-League), **Air Monastery / Wyndwalken** (Kashrishi cartographers), **Fellibylur** (Stormpact merchant kingdom). Reading those three side by side is the fastest way to learn the rhythm.

## On invocation, before anything else

Read these in order. Skipping is the single largest source of rework.

1. **`CLAUDE.md`** if not already in context. The naming rule, the lore-first protocol, the affirmative-prose rule, the no-em-dashes rule, the surface-before-writing rule.
2. **The lore files for the target domain**, per the Phase 0 checklist below.
3. **Grep the project for the sub-region name.** Other pages may cross-reference it and constrain the design.

If any canon contradicts what you were about to draft, the canon wins. Surface the conflict in chat before adapting.

## The seven phases at a glance

| Phase | What happens | Phase boundary discipline |
|---|---|---|
| **0. Read the canon** | Domain lore + glossary + bestiary + open-threads + parent HTML + project grep | Do not start Phase 1 until done |
| **1. Spitball options** | Generate 4-6 structurally distinct political shapes with founding-era, ancestry-anchor, and cross-canon hook for each. End with a recommended pick | Chat only. No file writes |
| **2. User picks + refines** | User picks one or combines two. Axis-confirmation only. Ask one or two clarifying questions on placement, neighbors, ancestry-anchor, naming-axis preference | **Axis-confirmation is not a green light to draft prose.** Do not start Phase 4 yet |
| **3. Naming pass** | Offer 3-5 candidates per name slot with full etymology. Recommend one. Apply collision-check before suggesting. Wait for user pick | Chat only |
| **4. Surface the prose draft** | Draft the `geography/<region>.md` bullet, glossary entries, faction subsection, bestiary updates. Surface in chat. Flag every derivation that went beyond the user's explicit picks | **Do not commit to files yet.** Surface first |
| **5. Commit lore** | On explicit "commit" / "go ahead" / "publish to lore", apply edits in parallel to `lore/geography/<region>.md`, `lore/glossary.md`, `lore/ancestries.md`, `docs/open-threads.md` | Lore is now canon. **Do not touch HTML.** |
| **6. HTML mirror** | On an explicit publish signal, upgrade the parent domain HTML card and update cross-page links | Stay within the minimum mirror unless the user signals promotion |
| **7. Promote to dedicated page** | On an explicit "promote" signal, build `talan/domains/<domain>/<slug>/<slug>.html` using `talan/domains/vindul/haizetsua/haizetsua.html` as template. Wire `assets/site-nav.js`, the parent domain card, `docs/site-inventory.md`, cross-page links. Fold any agent-committed canon back to glossary.md | For multi-page promotion, see *Parallelization* below |

The phase boundaries are review checkpoints. Pause at each one even under broad "work through it" framing. Reading is fine within a phase; writes trigger the boundary.

---

## Phase 0: Read the canon

Per CLAUDE.md's pre-read rule, read the relevant lore end-to-end before drafting. For a sub-region in domain X:

1. **`lore/geography/<region>.md`** for domain X, end-to-end (terrain, neighbors, existing sub-region bullets, the god-city). Also read **`lore/geography/<bordering-region>.md`** for each bordering domain named in the file's `**Borders:**` line, since neighbours' canon constrains the sub-region's edges. **`lore/geography/_continent.md`** if the sub-region touches a sea, an off-continent power, or the rail network.
2. **`lore/glossary.md`** — sub-regions block for the domain; Faction proper nouns if any anchor institutions exist
3. **`lore/ancestries.md`** — any ancestry already anchored to this sub-region, or candidate ancestries that could be
4. **`docs/open-threads.md`** — search the target name; flesh-out spec may already be partially drafted
5. **The parent domain's HTML** (`talan/domains/<domain>/<domain>.html`) — see how the existing card frames it
6. **Grep the project** for the sub-region name; other pages may cross-reference it and constrain the design

Skipping this step is the #1 source of rework. Fellibylur required three rounds of map-correction because the canon-check on neighbors was shallow.

---

## Phase 1: Spitball options (chat only, no commits)

Generate **4-6 distinct political shapes**. Each:
- 2-3 sentence pitch
- Structurally distinct from the others (not five flavours of monarchy)
- Tagged with implicit ancestry-anchor, faith-flavor, founding era
- Notes a cross-canon hook (what locked canon the option rhymes with)

### Archetype back-pocket

- **Clan-confederation** (no central crown; council of chieftains)
- **Hereditary monarchy / jarldom** (one ruling line)
- **Merchant republic** (chartered council of merchant-houses)
- **Theocracy** (god-tied or order-tied rule)
- **March / border-state** (militarised, hereditary aristocracy on a dangerous border)
- **Mendicant order** (rule = abbot/chapter; population = the order itself)
- **Mercantile guild-state** (the guild *is* the polity)
- **Federated free-towns** (Hanseatic; loose alliance of autonomous towns)
- **Rotating meritocracy** (annual or term-limited rule by demonstrated merit)
- **Nomadic confederacy** (mounted clans, seasonal gathering at a fixed site)
- **Two-tier hybrid** (coast + interior; settled + nomadic; secular + sacred under a single charter)

### Per-option notes to include

- Founding-era reading. Default: Adventurer-Era or late-Dark-Era founding per the Kingdoms-Inherit-Names rule. Older claims should be a deliberate feature, not the default.
- Ancestry-anchor implication. Vindul has Kashrishi, Tengu, Jotunborn, Strix; check which are claimed elsewhere before suggesting a new anchor.
- Cross-canon hook. How does this option talk to existing locked canon (the Gods' Law, Wardstones, neighboring sub-regions, named factions)?

End with a recommended pick and a note that the user can combine options.

---

## Phase 2: User picks + refines (axis-confirmation, NOT a green light)

User picks one (or combines two). Often they refine the framing significantly, sometimes invert it. **Do not start drafting prose yet.** Per the user's surface-before-writing rule, axis-confirmation is not a green light.

This phase is for follow-up questions: geographic placement, neighbors, ancestry-anchor, naming-axis preferences. Ask one or two clarifying questions in chat, get the answers, then move to naming.

If the user provides a map image with hand-drawn borders, treat the geographic corrections as authoritative over any prior canon. Note the canon-mismatches you'll need to fix at commit time.

---

## Phase 3: Naming pass (chat only)

If the sub-region or its institutions need new names, **offer 3-5 candidates per name slot with full etymology, recommend one, wait for the user pick.**

### The naming-stratum rule (from CLAUDE.md)

- **Old / ancient / geographic** → Basque or Icelandic, slightly drifted. Examples: *Fellibylur*, *Vindboorg*, *Hartzar Erruta*.
- **Modern / institutional / contemporary** → English, lightly drifted. Examples: *Frae City*, *Order of Steam*, *Wyndwalken*, *Stormpact*, *Brasswatch*.
- **Regional cultural register** if the region has one (Fenurran Latinate, Kotokoe-kitsune, Sortalde dynastic, Haizetsua-Tengu). These are not exceptions; they're the third stratum.

### Drift mechanisms to apply (modern stratum)

- Vowel shift (i → y, ai → ae, ou → ow)
- Consonant erosion (-ed → -t, -ing → -en)
- Compound contraction (mountain → mount)
- Archaic suffixes (-en past-participle as in *oxen*; -augh as in *thought*; -worn as Old-English *-sworn*)
- Loss of silent letters

### Critical: collision-check before committing

- *Compact* is reserved for the **Compact of the Bound Thirteen** (the Gods' Law). Never reuse for a constitutional agreement; we used *Stormpact* for Fellibylur instead.
- *Order* is heavy traffic (*Order of Steam*, *Voroir Daua*). Distinct, but check before coining.
- *Republic* and *League* are open. *Hanseatic*-feel names work cleanly.
- *Council*, *Court*, *Hall*, *House* are open and common.

### Always record etymology in `glossary.md` at commit time

Source language, literal meaning, drift step. The glossary is the source of truth for derivation.

---

## Phase 4: Surface the prose draft for review

Once direction and names are settled, draft the actual prose. **Surface in chat. Do not commit yet.**

### Standard draft contents

- **A single extended bullet for `lore/geography/<region>.md`** under the domain's *Sub-regions* list. Model on the Haizetsua bullet pattern: one rich paragraph (or a small handful of paragraphs) packing geography, polity, institutions, signature export, tension, and faith. No em-dashes. Affirmative prose. Chronicler-tier voice (in-world scholar).
- **Etymology entries for `lore/glossary.md`** (sub-region entry under *Sub-regions → <Domain>*, nested under parent if it's a place-within-a-place like *Hartzar Erruta* under *Air Monastery*).
- **Faction subsection for `lore/glossary.md`** if institutions are coined (modeled on the Voroir Daua or Wyndwalken patterns).
- **Bestiary updates** if an ancestry is being anchored, moved, or freshly placed (table cell + per-ancestry entry + cross-references in related entries).

### Flag every derivation that goes beyond the user's explicit picks

If you inferred something from canon ("Kashrishi are secular per bestiary, so the order is secular-contemplative not religious-monastic"), state it explicitly in the surface message so the user can correct before commit.

---

## Phase 5: Commit lore (on explicit go)

User green-lights with "commit" / "go ahead" / "publish to lore" / similar. Apply edits in parallel:

| File | What goes there |
|---|---|
| `lore/geography/<region>.md` | The full sub-region bullet, replacing the prior one-liner |
| `lore/glossary.md` | Sub-region etymology entry (nested under *Sub-regions → <Domain>* block); new Faction proper nouns subsection if institutions were coined |
| `lore/ancestries.md` | Ancestry-anchor table updates; full ancestry-entry rewrite if the ancestry moved or is newly Common; cross-reference cleanup in related ancestry entries |
| `docs/open-threads.md` | Close or update the sub-region's open-thread entry. Mark "Closed." inline. If any sub-canon remains open, enumerate what's still TBD. |

Lore is now canon. **Do not touch HTML** without an explicit publish signal. Phrasings that count: *publish to HTML*, *render the page*, *make it live*, *put it on the site*, *commit to HTML*, *mirror to HTML*.

---

## Phase 6: HTML mirror (on explicit publish signal)

Minimum mirror when canon changes:

1. **Parent domain HTML card** (`talan/domains/<domain>/<domain>.html`): upgrade the sub-region card from a one-liner `<div>` to a richer card with the new description and updated tags. If the sub-region is being promoted to a dedicated page (Phase 7), make the card a clickable `<a class="subregion-card">` with trailing ` →` in the title per `docs/card-conventions.md`.
2. **Cross-page links** if the ancestry-anchor changed:
   - `pf2e-registrar.html` ancestry rows (wrap the sub-region in `<a>` inside the location parenthetical)
   - `talan/ancestries.html` table row (same)
   - **Per-domain card body on `ancestries.html`: text mention only**; card-conventions forbid inner anchors inside clickable cards.
3. **Other HTML pages that mention the sub-region**: grep for the name and update prose where needed (commonly the domain-page, sibling sub-region pages, or a TBD note that's now resolvable).

Lore stays canonical; HTML is reflection.

---

## Phase 7: Promote to dedicated page (on explicit "promote" signal)

Per CLAUDE.md: "Don't create empty stub files for sub-regions that don't exist yet." Once a sub-region has full lore canon (`geography/<region>.md` bullet + glossary entries + factions referenced), it has earned promotion.

### Build the page

- Path: `talan/domains/<domain>/<slug>/<slug>.html`
- Template: copy the structure of **`talan/domains/vindul/haizetsua/haizetsua.html`**. Gold-standard Style B sub-region page.
- Standard structure:
  - `<head>` with Style B CSS link, `site-nav.js`, custom `<style>` with per-page `--domain-accent` (verify ≥3:1 contrast against `#0f0c08` via `docs/accessibility.md`'s PowerShell snippet)
  - `<body data-page="<slug>">`
  - Breadcrumb (absolute paths)
  - Header with title, subtitle, evocative flavor-line
  - **At-a-Glance facts panel** (etymology, position, terrain, character pills, people, tongue, faith, rule)
  - **God's-city-style callout** for the capital or mother-house
  - **5-8 themed sections**, each with a divider and section-heading
  - **Signature feature panels** (`.feature-panel`) for the kingdom's distinctive crafts or institutions
  - **Card grids** where appropriate (clans, departments, named artifacts, named bells, named seasons)
  - **Optional amber `◈ Popular Belief` and red `⚿ GM Secret` expandables**. Load `/assets/site-interactions.js` if used. Folk-belief boxes work well for tavern-tales about the institution; GM secrets are reserved for canon the chronicler couldn't reasonably know.
  - **Open in the Chronicle Record** list at the bottom (remaining TBDs in chronicler voice)

### Style and convention rules

- **No em-dashes anywhere**. En-dashes for numeric ranges only.
- **Affirmative prose**. Avoid "not X but Y" framings; if the negation is the clearest framing for a fact with no affirmative form, fine, but verify.
- **Chronicler-tier in open prose**; GM-tier inside `⚿ GM Secret` expandables only. If a chronicler reading the open prose would learn something the lore files mark as GM-only, it's leaking.
- **Concrete sensory detail** (the smell of brass and salt at a port-tower, the gesture a Stormrider makes to read a cloud-front, the sound of iron tokens in a vote-bowl) over abstract worldbuilding.
- **All links absolute paths** starting with `/`.
- **Card conventions** per `docs/card-conventions.md`: clickable card = ` →` in title; expandable card = `Tap ▾` pill; plain `<div>` carries neither.

### Wire it in

1. **`assets/site-nav.js`** — add the new page to the `DOMAINS` tree under its domain, with a descriptive label (`'Baerfrost · Hunt-League'`, `'Air Monastery · Wyndwalken'`). Order alphabetically or by canonical sub-region listing.
2. **Parent domain HTML** — upgrade the sub-region card to clickable (Haizetsua pattern: `<a class="subregion-card" href="...">` with `→` in the title and a "Promoted" tag).
3. **`docs/site-inventory.md`** — add an entry to the Promoted sub-regions section describing the new page's structure. Model on the Haizetsua entry (the most detailed precedent).
4. **Cross-page links** — same as Phase 6.

### Fold agent-committed canon back to glossary

When a page-building agent invents canon-additive content (new place-names, governance details, named artifacts, named subdivisions), **fold those back to `lore/glossary.md`** so the canon stays consistent across files. Update `docs/open-threads.md` if any TBDs are newly resolved. Examples from the 2026-05-24 pass:

- **Hartzar Erruta** (Air Monastery mother-house) committed by the agent → nested under *Air Monastery* in glossary sub-regions, full Basque etymology recorded.
- **Brasswatch** + named subsidiary Skybell ports + named Skybells + the Hightable + storm-season calendar (all Fellibylur) committed by the agent → folded into the *Fellibylur* faction subsection.
- **Abbot-for-life + five-department Chapter** (Wyndwalken governance) committed by the agent → folded into the Wyndwalken faction subsection.

---

## Parallelization for multi-page promotion

When promoting two or more sub-regions at once, **spawn one general-purpose agent per page in parallel** with the Agent tool. Each agent gets:

- **Canon source pointers** — the lore source files for its target (`geography/<region>.md` bullet + glossary entries + bestiary if relevant)
- **Template pointer** — `talan/domains/vindul/haizetsua/haizetsua.html` as the model
- **Convention pointers** — `CLAUDE.md`, `docs/card-conventions.md`, `docs/accessibility.md`, `docs/sidebar-nav.md`
- **Explicit guidance** on the page's `--domain-accent` (suggest 2-3 hex options + tell the agent to verify contrast against `#0f0c08`)
- **The fixed style rules**: commit no em-dashes, write affirmative prose, stay chronicler-tier in open prose, all links absolute
- **A short-form report-back spec** (under 200 words: accent + contrast + section count + committed canon-additive choices + whether they wrote Popular-Belief / GM-Secret boxes)

Wait for all agents to complete. Each will report its committed canon-additive choices. Fold those back to glossary.md in a single batch after all agents have reported.

---

## Hard rules (non-negotiable, surface-violating drafts get rewritten)

- **No em-dashes anywhere.** En-dashes for numeric ranges only (e.g. `1321 MR – 2135 MR`). The 2026-05-24 sweep removed 1,786 em-dashes; do not re-introduce any.
- **Affirmative prose.** No "Not X" or "Not X but Y" openings. Exception: when a true negation is the clearest framing for a fact with no affirmative form (*"his cult kept no records"*).
- **Chronicler-tier in open prose; GM-tier inside `⚿ GM Secret` expandables only.** If a chronicler reading the open prose would learn something the lore files mark as GM-only, it is leaking; move it inside a secret box.
- **Kingdoms inherit names, not continuity.** No Talanese kingdom predates 1 MR; few are older than the Dark Era. Default new polities to Adventurer-Era or late-Dark-Era founding unless the older claim is a deliberate story feature.
- **Naming stratum + collision check** before committing any new name (full detail in Phase 3).
- **Pre-read before designing.** If the user could reasonably point at the draft and say *"that contradicts what's in `<file>`,"* you should have read `<file>` first.
- **Lore-first by default.** Brainstorm goes to lore files, not HTML, until an explicit publish signal.

---

## Common pitfalls

- **Skipping the canon-check.** Map labels and lore-file canon can disagree. Always grep the project for the sub-region name before drafting.
- **Naming collisions.** Check *Compact* (reserved), *Order* (heavy traffic), and any institution name that sounds generic. Stormpact > Compact for Fellibylur was a forced rename mid-session.
- **Damaging neighboring canon.** Moving an ancestry (Strix from Floteyn to Vindul) means cleaning up cross-references in *other* ancestries' entries (Athamaru, Tripkee). Always grep the project for the ancestry name and read each hit before editing.
- **Em-dashes leaking in.** Especially in long extended bullets. The sweep on 2026-05-24 removed 1,786 em-dashes across the project; don't re-introduce any.
- **Inner anchors in clickable cards.** `docs/card-conventions.md` forbids them. Per-domain card bodies on `ancestries.html` get text-only mentions; table cells and prose paragraphs can use anchors freely.
- **GM-tier content in open prose.** If a fact wasn't earnable by an in-world scholar, it goes in a `⚿ GM Secret` expandable. The chronicler does not know.
- **Touching HTML without a publish signal.** Stay in lore by default. Only publish when the user says so explicitly.

---

## Working principles (reminder, from CLAUDE.md)

- **Lore-first protocol.** Brainstorm goes to lore files, not HTML, until an explicit publish signal.
- **Surface phase boundaries rather than chaining them.** Pause at: spitball → user picks → naming → prose draft → commit → publish → promote.
- **Pre-read the canon.** Read the relevant lore file end-to-end before designing on top of it.
- **Surface before writing.** For Tyrnarra lore writes, surface actual prose for review before committing. Axis-confirmation is not a green light.
- **Affirmative prose.** No "Not X" or "Not X but Y" openings unless the negation is the clearest framing.
- **No em-dashes.** En-dashes for numeric ranges only.
- **Kingdoms inherit names, not continuity.** Default new polities to Adventurer-Era or late-Dark-Era founding unless the older claim is a deliberate story feature.

---

## Worked examples (read these in order)

The three Vindul sub-regions promoted on 2026-05-24:

- **Baerfrost** (clan-confederation under rotating meritocracy). `lore/geography/vindul.md` *Baerfrost*; `lore/glossary.md` sub-regions block; `talan/domains/vindul/baerfrost/baerfrost.html`.
- **Air Monastery / The Wyndwalken** (mendicant order with fixed mother-house). `lore/geography/vindul.md` *Air Monastery*; `lore/glossary.md` sub-regions + *The Wyndwalken (Air Monastery cartographer order)*; `talan/domains/vindul/air-monastery/air-monastery.html`.
- **Fellibylur** (chartered merchant kingdom, parallel coast/interior seats). `lore/geography/vindul.md` *Fellibylur*; `lore/glossary.md` sub-regions + *Fellibylur (storm-people merchant kingdom of Vindul)*; `talan/domains/vindul/fellibylur/fellibylur.html`.

Read the prose in `lore/geography/vindul.md` + the etymology entries in `lore/glossary.md` + the HTML at `talan/domains/vindul/<slug>/<slug>.html` for each. That is the shape every new sub-region is aiming at.
