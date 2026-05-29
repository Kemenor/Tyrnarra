---
name: sub-region-workflow
description: Use this skill whenever working on a Talanese sub-region (kingdom, free city, theocracy, mendicant order, guild-state, merchant republic, federated free-towns, march, clan-confederation, nomadic confederacy, or any polity smaller than a continent) within the Tyrnarra worldbuilding project. Trigger on phrases like "flesh out [name]", "let's design [polity]", "new sub-region in [domain]", "what should [domain]'s [feature] be", "promote [name] to its own page", "build the page for [name]", "we have a label on the map but no canon for X", working with TBD sub-region entries in docs/open-threads.md, drafting bullets in lore/geography/<region>.md sub-region sections, or any session that takes a label-on-the-map to fully fleshed canon. Also use when the user references the Emarrea, Baerfrost, Air Monastery / Wyndwalken, or Fellibylur exemplars as patterns to follow, or the Lautara resketch (Itsasalda mountain-Halflings, Azkataria philosopher-market, Atarialda welcome-threshold) as the seed pattern. The skill enforces an eight-phase workflow that opens with a seed-questions dialogue and a seed-generation pass (not a political-shape menu), with surface-before-writing pauses, the kingdoms-inherit-names rule, the Basque/Icelandic/English naming-stratum check, the collision check on reserved names (Compact, Order), the ancestry-is-not-culture rule, the specificity test, the lore-pre-read step, and the lore-first / surface-before-HTML protocol from CLAUDE.md. Do not use for cosmology or pantheon work, quest design unconnected to founding or refounding a polity, NPC dossiers in already-established sub-regions, or HTML edits to pages that already exist for unrelated reasons.
---

# Sub-region workflow

## What this skill is for

Taking a sub-region from "label on the map" (a one-liner stub in `lore/geography/<region>.md`, a TBD entry in `docs/open-threads.md`, or a freshly named region on a hand-drawn map) to fully fleshed canon, and optionally to a dedicated HTML page, inside a single session, with the user's voice setting direction at every phase boundary.

This applies to anything that needs its own polity-shape and signature institution(s) and stops short of a continent: kingdoms, factions-as-polities, orders, theocracies, confederations, free cities, mendicant brotherhoods, guild-states. The exemplars are **Emarrea** (the gold standard: Kitsune essence → foxfire → illusion → spectacle → drama → Heart Court; the polity is built outward from a specific image, not slotted into an archetype), the three Vindul sub-regions promoted on **2026-05-24** (**Baerfrost** Hunt-League, **Air Monastery / Wyndwalken** Kashrishi cartographers, **Fellibylur** Stormpact merchant kingdom), and the **Lautara resketch of 2026-05-28** (Itsasalda mountain-Halflings as glacial permanence against constant churn; Azkataria philosopher-market where Vishkanya craft meets Ezkudon scholarship; Atarialda welcome-threshold where Halflings carry the hearth with them). Reading those side by side is the fastest way to learn the rhythm.

## Why this skill was rewritten on 2026-05-28

The first version of this skill led Phase 1 with "what political shape fits this domain?" and "what ancestry lives here?" The result, by the user's verdict after Lautara: every sub-region came out as a template with slots filled in. Halflings did routing in every kingdom. Vishkanya did administration. Kitsune did brokering. Ancestry-label was being used as a substitute for culture, and political shape was being chosen before the place had a soul.

The fix is in Phases 1 and 2. **Phase 1** is now a 3-5 question dialogue with the user about what flows through this place, what presses on it, and what a traveler would remember. **Phase 2** generates **seeds**, not political shapes. A seed is an image, a contradiction, a behavior, or a collision of forces — the specific thing this place is, that no other place is. Political form and ancestry role emerge *from* the seed; they are not picked from a list and then justified.

The Emarrea methodology — build outward from "what makes Kitsune Kitsune *here*" through foxfire and illusion to the Heart Court — is the model. The archetype back-pocket (clan-confederation, merchant republic, theocracy, etc.) is a sanity-check *after* the seed, not a menu before it.

## On invocation, before anything else

Read these in order. Skipping is the single largest source of rework.

1. **`CLAUDE.md`** if not already in context. The naming rule, the lore-first protocol, the affirmative-prose rule, the no-em-dashes rule, the surface-before-writing rule.
2. **The lore files for the target domain**, per the Phase 0 checklist below.
3. **Grep the project for the sub-region name.** Other pages may cross-reference it and constrain the design.

If any canon contradicts what you were about to draft, the canon wins. Surface the conflict in chat before adapting.

## The eight phases at a glance

| Phase | What happens | Phase boundary discipline |
|---|---|---|
| **0. Read the canon** | Domain lore + bordering-domain lore + glossary + ancestries + open-threads + parent HTML + project grep | Do not start Phase 1 until done |
| **1. Seed questions** | Ask the user 3-5 targeted questions about geography, flow, atmosphere, and the traveler's-impression of the place. Surface the answers back as a summary before generating | Chat only. No writes. |
| **2. Generate seeds** | Generate **2-3 distinct seeds**. Each is an image, a contradiction, a behavior, or a collision of forces; each must pass the specificity test ("could this place exist anywhere else? if yes, not specific enough"); each names what political form and ancestry role *naturally emerge*. End with a recommended pick. | Chat only. No writes. |
| **3. User picks + refines** | User picks one or combines two. Axis-confirmation only. Ask one or two clarifying questions on placement, neighbors, ancestry-anchor, naming-axis | **Axis-confirmation is not a green light to draft prose.** Do not start Phase 5 yet |
| **4. Naming pass** | Offer 3-5 candidates per name slot with full etymology. Recommend one. Apply collision-check before suggesting. Wait for user pick | Chat only |
| **5. Surface the prose draft** | Draft the `geography/<region>.md` bullet, glossary entries, faction subsection, bestiary updates. Surface in chat. Flag every derivation that went beyond the user's explicit picks | **Do not commit to files yet.** Surface first |
| **6. Commit lore** | On explicit "commit" / "go ahead" / "publish to lore", apply edits in parallel to `lore/geography/<region>.md`, `lore/glossary.md`, `lore/ancestries.md`, `docs/open-threads.md` | Lore is now canon. **Do not touch HTML.** |
| **7. HTML publish (mirror + optional promotion)** | On an explicit publish signal: upgrade the parent domain HTML card, update cross-page links (ancestries, registrar, prose mentions). On an explicit "promote" signal in the same phase: build `talan/domains/<domain>/<slug>/<slug>.html`, wire `assets/site-nav.js`, the parent domain card, `docs/site-inventory.md`, fold any agent-committed canon back to glossary.md | For multi-page promotion, see *Parallelization* below |

The phase boundaries are review checkpoints. Pause at each one even under broad "work through it" framing. Reading is fine within a phase; writes trigger the boundary.

---

## Phase 0: Read the canon

Per CLAUDE.md's pre-read rule, read the relevant lore end-to-end before drafting. For a sub-region in domain X:

1. **`lore/geography/<region>.md`** for domain X, end-to-end (terrain, neighbors, existing sub-region bullets, the god-city). Also read **`lore/geography/<bordering-region>.md`** for each bordering domain named in the file's `**Borders:**` line, since neighbours' canon constrains the sub-region's edges. **`lore/geography/_continent.md`** if the sub-region touches a sea, an off-continent power, or the rail network.
2. **`lore/glossary.md`** — sub-regions block for the domain; Faction proper nouns if any anchor institutions exist
3. **`lore/ancestries.md`** — any ancestry already anchored to this sub-region, or candidate ancestries that could be. **Read the full ancestry entry for any ancestry you might place here.** A one-liner lore note ("Halflings are the traveling folk") is not the ancestry; it's a seed for one. Read the full entry so you know what else there is.
4. **`docs/open-threads.md`** — search the target name; flesh-out spec may already be partially drafted
5. **The parent domain's HTML** (`talan/domains/<domain>/<domain>.html`) — see how the existing card frames it
6. **The sibling sub-regions** in the same domain — read their full bullets in `geography/<region>.md` and skim their HTML if promoted. The new sub-region must feel distinct from its siblings; reading them surfaces the same-iness risk early.
7. **Grep the project** for the sub-region name; other pages may cross-reference it and constrain the design

Skipping this step is the #1 source of rework. The Lautara resketch happened because the first-pass design didn't sit the sibling sub-regions side-by-side and notice they were all reading as variants of one template.

---

## Phase 1: Seed questions (chat only)

Before generating any seeds, ask the user 3-5 questions to get the texture only they can provide. Without this step, seeds default to demographic labels and political archetypes, which is exactly what the rewrite is here to prevent.

### How to choose the questions

Read what the canon has already settled and **don't ask those**. The questions are for the gaps — the parts of "what is this place" that the lore files don't yet answer. Pick 3-5 from the categories below; tailor the wording to the specific sub-region.

### Question categories

- **Geography and flow.** What does this place sit *between*? What flows through it? What presses on it from outside? Does the rail go through it; does sea trade dock here; is it on a corridor from a neighboring domain? *(Example: "Itsasalda is the port of Merkavar — half the continent's sea trade lands here. That's its flow. What does that do to the feel of the place?")*
- **The traveler's impression.** If you close your eyes and imagine being there, what's the one thing you'd remember? Not the politics, the texture — the smell, the sound, the gesture, the image you'd describe to someone who's never been. *(Example: "An old Halfling woman on the same dock stool she has sat on every morning for fifty years, watching a Brauogi grain ship unload with the expression of someone watching weather.")*
- **Contradiction or tension.** Is there an unlikely combination at the heart of this place? A people that shouldn't be where they are; a value held in a setting that resists it; two cultures that collided and didn't separate? *(Example: Atarialda — the wanderers are the most rooted. The campfire laugh is the dining-room laugh.)*
- **The neighbor question.** How is this place different from its closest sibling sub-region? If a traveler walked from one to the other, what would change? *(Example: "Itsasalda is the dock that never moves; Atarialda is the threshold where the hearth meets every traveler. Different welcomes, different rhythms.")*
- **Ancestry as seed, not identity.** *Only if an ancestry might anchor here, and only as a follow-up to one of the questions above.* What about *this place* changes how this ancestry lives? What does being from *here* add on top of being of this people? *(Example: Halflings are travelers everywhere — but the Itsasalda mountain-Halflings are the ones who stopped, and stopping changed what travel means to them.)*

### Surface the answers back

After the user answers, write a 4-6 sentence summary of what the answers tell you about the place: the flow, the image, the tension, the inherited canon. Surface this summary in chat before moving to Phase 2. The user may correct or refine before you generate seeds.

---

## Phase 2: Generate seeds (chat only, no commits)

Generate **2-3 distinct seeds**. A seed is the specific thing this place *is*, that no other place is. Politics, ancestry role, and signature institution all emerge from the seed; they are not slotted in.

### What a seed is

- An **image** (a Halfling on a dock stool watching a grain ship unload)
- A **contradiction** (the wanderers are the most rooted; the welcome travels with you)
- A **behavior** (the campfire laugh is the dining-room laugh)
- A **collision of forces** (Vishkanya craft meets Ezkudon scholarship at a coffee table; the result is fluid democracy by argument)
- A **flow-derived character** (Itsasalda lives on the throughput of half a continent; nothing stays, everything passes; the locals are the ones who decided not to)

### What a seed is NOT

- A political archetype with ancestry slotted in ("a merchant republic dominated by Halflings")
- An ancestry label as identity ("Halflings live here")
- A demographic distribution
- A founding-era + faith descriptor combo
- An adjective for the domain ("Commerce-flavored welcoming kingdom")

### The specificity test

Each seed must pass all three:

1. **Could this place exist anywhere else in the setting?** If yes, the seed isn't specific enough. *(Example: "merchant republic with Halflings" fails — could be any domain. "the dock that never moves while half a continent's trade passes through" passes — it requires Itsasalda's exact geography.)*
2. **Does the seed tell you both what someone would REMEMBER and how the locals LIVE?** If only one, it's too shallow.
3. **Does political form and ancestry role emerge naturally from the seed, or are you having to invent them on top?** If invented on top, the seed isn't load-bearing.

### Per-seed contents

For each of the 2-3 seeds, write:

- **A 2-3 sentence pitch** that leads with the image / contradiction / behavior / collision. Politics does not appear in the pitch.
- **"What follows from this"** — one short paragraph naming the political form, ancestry role, signature institution, and one concrete sensory detail that all emerge naturally from the seed. *(Example, Atarialda: "The hearth-rule. Hospitality is a near-sacred obligation; refusing someone a seat is a civic wrong. Governance is the council of those who keep the best tables; stay-at-home families and traveling families are equals with complementary roles. Population is mixed by accumulation — strangers who got fed kept coming back.")*
- **Cross-canon hook** — how this rhymes with locked canon (Halflings' "they got faster" with trains; Lautara's Commerce-domain texture; the trade corridor from Egulon and Zuzental).
- **The specificity test result** — one line confirming the seed passes the test and naming what would have to change to put this place elsewhere. If the answer is "the kingdom's name", the seed has failed; rewrite.

### Don't lead with the archetype menu

The archetype back-pocket below is a sanity-check *after* the seed is chosen, not a starting list. If you find yourself reaching for the menu in Phase 2, the canon-read or the seed-questions weren't deep enough. Go back.

### End with a recommended pick

Note which of the 2-3 you'd lean toward and why. The user can pick one, combine two, or invert one.

### Archetype back-pocket (for after the seed, not before)

These are political shapes the setting has used. When the seed is chosen and you're working out what governance actually looks like, recognise which archetype the seed has produced and lean on the precedent.

- **Clan-confederation** (no central crown; council of chieftains) — Baerfrost shape
- **Hereditary monarchy / jarldom** (one ruling line)
- **Merchant republic** (chartered council of merchant-houses)
- **Theocracy** (god-tied or order-tied rule)
- **March / border-state** (militarised, hereditary aristocracy on a dangerous border)
- **Mendicant order** (rule = abbot/chapter; population = the order itself) — Wyndwalken shape
- **Mercantile guild-state** (the guild *is* the polity)
- **Federated free-towns** (Hanseatic; loose alliance of autonomous towns)
- **Rotating meritocracy** (annual or term-limited rule by demonstrated merit)
- **Nomadic confederacy** (mounted clans, seasonal gathering at a fixed site)
- **Two-tier hybrid** (coast + interior; settled + nomadic; secular + sacred under a single charter) — Fellibylur shape
- **Hearth-council / hospitality-rule** (governance grounded in a near-sacred civic value, council seats earned by exemplifying it) — Atarialda shape
- **Court-of-spectacle** (rule by demonstrated artistry; politics performed as drama) — Emarrea Heart Court shape

### Founding-era and ancestry notes per seed

- **Founding-era reading.** Default: Adventurer-Era or late-Dark-Era founding per the Kingdoms-Inherit-Names rule. Older claims should be a deliberate feature, not the default.
- **Ancestry-anchor implication.** Check the canon for ancestries already claimed elsewhere before suggesting a new anchor. Crucially: **don't reduce the ancestry to its one-line lore.** If Halflings are "the traveling folk", that is a seed for *one* aspect of one *possible* Halfling-anchored sub-region. The mountain-Halflings of Itsasalda are travelers who *stopped*. The hearth-Halflings of Atarialda *carry the hearth with them*. Same ancestry, different lives, because being from *here* shapes them.

---

## Phase 3: User picks + refines (axis-confirmation, NOT a green light)

User picks one (or combines two). Often they refine the framing significantly, sometimes invert it. **Do not start drafting prose yet.** Per the user's surface-before-writing rule, axis-confirmation is not a green light.

This phase is for follow-up questions: geographic placement, neighbors, ancestry-anchor, naming-axis preferences. Ask one or two clarifying questions in chat, get the answers, then move to naming.

If the user provides a map image with hand-drawn borders, treat the geographic corrections as authoritative over any prior canon. Note the canon-mismatches you'll need to fix at commit time.

---

## Phase 4: Naming pass (chat only)

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

## Phase 5: Surface the prose draft for review

Once direction and names are settled, draft the actual prose. **Surface in chat. Do not commit yet.**

### Standard draft contents

- **A single extended bullet for `lore/geography/<region>.md`** under the domain's *Sub-regions* list. Model on the Haizetsua bullet pattern: one rich paragraph (or a small handful of paragraphs) packing geography, polity, institutions, signature export, tension, and faith. **Lead with the seed.** The first sentence should evoke the image, contradiction, or behavior the seed was built on. The political form follows from there. No em-dashes. Affirmative prose. Chronicler-tier voice (in-world scholar).
- **Etymology entries for `lore/glossary.md`** (sub-region entry under *Sub-regions → <Domain>*, nested under parent if it's a place-within-a-place like *Hartzar Erruta* under *Air Monastery*).
- **Faction subsection for `lore/glossary.md`** if institutions are coined (modeled on the Voroir Daua or Wyndwalken patterns).
- **Bestiary updates** if an ancestry is being anchored, moved, or freshly placed (table cell + per-ancestry entry + cross-references in related entries). **Anchor the ancestry to its place-shaped version, not its generic lore.** "Halflings in Itsasalda" gets the mountain-Halfling specificity; "Halflings in Atarialda" gets the hearth-carrier specificity.

### Flag every derivation that goes beyond the user's explicit picks

If you inferred something from canon ("Kashrishi are secular per bestiary, so the order is secular-contemplative not religious-monastic"), state it explicitly in the surface message so the user can correct before commit.

---

## Phase 6: Commit lore (on explicit go)

User green-lights with "commit" / "go ahead" / "publish to lore" / similar. Apply edits in parallel:

| File | What goes there |
|---|---|
| `lore/geography/<region>.md` | The full sub-region bullet, replacing the prior one-liner |
| `lore/glossary.md` | Sub-region etymology entry (nested under *Sub-regions → <Domain>* block); new Faction proper nouns subsection if institutions were coined |
| `lore/ancestries.md` | Ancestry-anchor table updates; full ancestry-entry rewrite if the ancestry moved or is newly Common; cross-reference cleanup in related ancestry entries |
| `docs/open-threads.md` | Close or update the sub-region's open-thread entry. Mark "Closed." inline. If any sub-canon remains open, enumerate what's still TBD. |

Lore is now canon. **Do not touch HTML** without an explicit publish signal. Phrasings that count: *publish to HTML*, *render the page*, *make it live*, *put it on the site*, *commit to HTML*, *mirror to HTML*. *Promote* additionally means "give it a dedicated page" (the second half of Phase 7).

---

## Phase 7: HTML publish (on explicit publish signal)

This phase folds the old "minimum mirror" and "promote to dedicated page" steps. Both are HTML work and triggered by the same kind of explicit signal; the only difference is scope. A *publish* signal does the mirror; a *promote* signal does the mirror **and** the dedicated page.

### Part A: Minimum mirror (every publish signal)

1. **Parent domain HTML card** (`talan/domains/<domain>/<domain>.html`): upgrade the sub-region card from a one-liner `<div>` to a richer card with the new description and updated tags. If the sub-region is also being promoted (Part B below), make the card a clickable `<a class="subregion-card">` with trailing ` →` in the title per `docs/card-conventions.md`.
2. **Cross-page links** if the ancestry-anchor changed:
   - `pf2e-registrar.html` ancestry rows (wrap the sub-region in `<a>` inside the location parenthetical)
   - `talan/ancestries.html` table row (same)
   - **Per-domain card body on `ancestries.html`: text mention only**; card-conventions forbid inner anchors inside clickable cards.
3. **Other HTML pages that mention the sub-region**: grep for the name and update prose where needed (commonly the domain-page, sibling sub-region pages, or a TBD note that's now resolvable).

Lore stays canonical; HTML is reflection.

### Part B: Promote to dedicated page (only on explicit "promote" signal)

Per CLAUDE.md: "Don't create empty stub files for sub-regions that don't exist yet." Once a sub-region has full lore canon (`geography/<region>.md` bullet + glossary entries + factions referenced), it has earned promotion.

**Build the page:**

- Path: `talan/domains/<domain>/<slug>/<slug>.html`
- Template: copy the structure of **`talan/domains/vindul/haizetsua/haizetsua.html`**. Gold-standard Style B sub-region page.
- Standard structure:
  - `<head>` with Style B CSS link, `site-nav.js`, custom `<style>` with per-page `--domain-accent` (verify ≥3:1 contrast against `#0f0c08` via `docs/accessibility.md`'s PowerShell snippet)
  - `<body data-page="<slug>">`
  - Breadcrumb (absolute paths)
  - Header with title, subtitle, evocative flavor-line. **The flavor-line should evoke the seed**, not the political shape.
  - **At-a-Glance facts panel** (etymology, position, terrain, character pills, people, tongue, faith, rule)
  - **God's-city-style callout** for the capital or mother-house
  - **5-8 themed sections**, each with a divider and section-heading. The first themed section should expand the seed; don't lead with governance.
  - **Signature feature panels** (`.feature-panel`) for the kingdom's distinctive crafts or institutions
  - **Card grids** where appropriate (clans, departments, named artifacts, named bells, named seasons)
  - **Optional amber `◈ Popular Belief` and red `⚿ GM Secret` expandables**. Load `/assets/site-interactions.js` if used. Folk-belief boxes work well for tavern-tales about the institution; GM secrets are reserved for canon the chronicler couldn't reasonably know.
  - **Open in the Chronicle Record** list at the bottom (remaining TBDs in chronicler voice)

**Style and convention rules:**

- **No em-dashes anywhere**. En-dashes for numeric ranges only.
- **Affirmative prose**. Avoid "not X but Y" framings; if the negation is the clearest framing for a fact with no affirmative form, fine, but verify.
- **Chronicler-tier in open prose**; GM-tier inside `⚿ GM Secret` expandables only. If a chronicler reading the open prose would learn something the lore files mark as GM-only, it's leaking.
- **Concrete sensory detail** (the smell of brass and salt at a port-tower, the gesture a Stormrider makes to read a cloud-front, the sound of iron tokens in a vote-bowl) over abstract worldbuilding.
- **All links absolute paths** starting with `/`.
- **Card conventions** per `docs/card-conventions.md`: clickable card = ` →` in title; expandable card = `Tap ▾` pill; plain `<div>` carries neither.

**Wire it in:**

1. **`assets/site-nav.js`** — add the new page to the `DOMAINS` tree under its domain, with a descriptive label (`'Baerfrost · Hunt-League'`, `'Air Monastery · Wyndwalken'`). Order alphabetically or by canonical sub-region listing.
2. **Parent domain HTML** — upgrade the sub-region card to clickable (Haizetsua pattern: `<a class="subregion-card" href="...">` with `→` in the title and a "Promoted" tag).
3. **`docs/site-inventory.md`** — add an entry to the Promoted sub-regions section describing the new page's structure. Model on the Haizetsua entry (the most detailed precedent).
4. **Cross-page links** — same as Part A above.

**Fold agent-committed canon back to glossary:**

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
- **The seed and what it produces** — pass the seed text from Phase 2 verbatim and remind the agent that the page should evoke the seed in its flavor-line and lead themed section, not just describe the politics
- **A short-form report-back spec** (under 200 words: accent + contrast + section count + committed canon-additive choices + whether they wrote Popular-Belief / GM-Secret boxes)

Wait for all agents to complete. Each will report its committed canon-additive choices. Fold those back to glossary.md in a single batch after all agents have reported.

---

## Hard rules (non-negotiable, surface-violating drafts get rewritten)

- **Ancestry-as-label is not culture.** A people's one-line lore is a seed, not an identity. The same ancestry in two different places should live two different lives, because being from *here* shapes them. Halflings as "the traveling folk" is the seed; Itsasalda mountain-Halflings and Atarialda hearth-Halflings are two different cultures that share an ancestry. If your draft has the same ancestry doing the same thing in two sub-regions, the seed wasn't load-bearing — rewrite.
- **The specificity test.** Every seed and every committed sub-region must pass: could this place exist anywhere else in the setting? If yes, the seed isn't specific enough. Rework before commit.
- **No em-dashes anywhere.** En-dashes for numeric ranges only (e.g. `1321 MR – 2135 MR`). The 2026-05-24 sweep removed 1,786 em-dashes; do not re-introduce any.
- **Affirmative prose.** No "Not X" or "Not X but Y" openings. Exception: when a true negation is the clearest framing for a fact with no affirmative form (*"his cult kept no records"*).
- **Chronicler-tier in open prose; GM-tier inside `⚿ GM Secret` expandables only.** If a chronicler reading the open prose would learn something the lore files mark as GM-only, it is leaking; move it inside a secret box.
- **Kingdoms inherit names, not continuity.** No Talanese kingdom predates 1 MR; few are older than the Dark Era. Default new polities to Adventurer-Era or late-Dark-Era founding unless the older claim is a deliberate story feature.
- **Naming stratum + collision check** before committing any new name (full detail in Phase 4).
- **Pre-read before designing.** If the user could reasonably point at the draft and say *"that contradicts what's in `<file>`,"* you should have read `<file>` first.
- **Lore-first by default.** Brainstorm goes to lore files, not HTML, until an explicit publish signal.

---

## Common pitfalls

- **Leading Phase 2 with the archetype menu.** The menu is a sanity-check *after* the seed. If you find yourself opening with "a merchant republic of Halflings", the seed-questions weren't deep enough — go back to Phase 1.
- **Reducing the ancestry to its one-line lore.** "Halflings travel" is a seed, not an identity. A Halfling-anchored sub-region must answer "what about *this* place changes how Halflings live here?" before commit.
- **Same-iness across siblings.** If the new sub-region reads as a variant of a sibling in the same domain, the seed has failed the specificity test. Read the sibling bullets in Phase 0 to surface this risk early.
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
- **Surface phase boundaries rather than chaining them.** Pause at: seed-questions → seeds → user picks → naming → prose draft → commit → publish.
- **Pre-read the canon.** Read the relevant lore file end-to-end before designing on top of it.
- **Surface before writing.** For Tyrnarra lore writes, surface actual prose for review before committing. Axis-confirmation is not a green light.
- **Affirmative prose.** No "Not X" or "Not X but Y" openings unless the negation is the clearest framing.
- **No em-dashes.** En-dashes for numeric ranges only.
- **Kingdoms inherit names, not continuity.** Default new polities to Adventurer-Era or late-Dark-Era founding unless the older claim is a deliberate story feature.

---

## Worked examples (read these in order)

### The seed pattern (the gold standard and the resketch)

- **Emarrea** (Lautara). The original gold standard. Built outward from "what makes Kitsune Kitsune": foxfire → illusion → spectacle → drama → Heart Court. The political form (Heart Court, ranked by demonstrated artistry) is the *consequence* of the seed, not the starting point. `lore/geography/lautara/emarrea.md`.
- **Itsasalda** (Lautara, resketch 2026-05-28). Seed: the mountain-Halflings, the dock that never moves, glacial permanence against constant churn. The political form (port-council of those who stayed) follows. The ancestry-anchor is Halflings, but specifically the Halflings-who-stopped, and stopping changed what travel means to them.
- **Azkataria** (Lautara, resketch 2026-05-28). Seed: the philosopher-market. Vishkanya craft meets Ezkudon scholarship at a coffee table; the result is fluid democracy by argument. Politics is the coffee-house consensus; ancestry-anchor is Vishkanya, but specifically those formed by the Ezkudon corridor.
- **Atarialda** (Lautara, resketch 2026-05-28). Seed: the welcome threshold. Halflings who carry the hearth with them; always a seat at the table. The campfire laugh is the dining-room laugh. Politics is the hearth-council; ancestry-anchor is Halflings, but specifically the hearth-carriers, who live a completely different life from the Itsasalda dock-Halflings.

### The full-workflow precedents (Vindul 2026-05-24)

- **Baerfrost** (clan-confederation under rotating meritocracy). `lore/geography/vindul.md` *Baerfrost*; `lore/glossary.md` sub-regions block; `talan/domains/vindul/baerfrost/baerfrost.html`.
- **Air Monastery / The Wyndwalken** (mendicant order with fixed mother-house). `lore/geography/vindul.md` *Air Monastery*; `lore/glossary.md` sub-regions + *The Wyndwalken (Air Monastery cartographer order)*; `talan/domains/vindul/air-monastery/air-monastery.html`.
- **Fellibylur** (chartered merchant kingdom, parallel coast/interior seats). `lore/geography/vindul.md` *Fellibylur*; `lore/glossary.md` sub-regions + *Fellibylur (storm-people merchant kingdom of Vindul)*; `talan/domains/vindul/fellibylur/fellibylur.html`.

Read the prose in `lore/geography/<region>.md` + the etymology entries in `lore/glossary.md` + the HTML at `talan/domains/<domain>/<slug>/<slug>.html` for each. The Vindul three teach the full eight-phase rhythm; the Lautara resketch and Emarrea teach what a seed-led design feels like in the prose.
