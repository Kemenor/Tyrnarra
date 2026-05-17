# Lore Review — Cleanup Pass

A scrubbing pass across `lore/*.md` looking for two things:

1. **Negative wording** — sentences that tell the reader what the world *isn't*. Lore files should record what *is*. The exception is necessary cover-vs-truth framing (public belief vs GM truth), where negation is load-bearing.
2. **Consistency** — places where two files disagree, or where one file contradicts itself.

Triage tiers:
- **High** — fix-now problems (factual contradictions, meta-instructions to Claude inside lore, outdated entries).
- **Medium** — negative framing that recasts cleanly to positive without losing meaning; TBD placeholders that should move to `docs/open-threads.md`.
- **Low** — stylistic negatives that are load-bearing or rhetorically appropriate (e.g. cover-story framing) and can be left alone.

---

## § Resolved so far

- **Pass A (meta-pollution)** — §1 done. Frae City "Do not describe…" + "Neutral Ground" section + Komo "earlier drafts" parenthetical + Maw Below/Blightfather use-instruction + `geography.md` Frae City "NOT neutral ground" — all rewritten or deleted.
- **Pass B (concrete corrections)** — §2 Hungerseed glossary entry updated to match `bestiary.md` canon. §3 *Distiratsua* → *Distiratsue* fixed in `geography.md:351`. §4 Brauogi/Ezkudon *No Man's Land* renamed to **The Wildreach**; glossary entry added. §6 Sun god bullet extracted into its own entry under *Named Non-Bound Gods*. §7 Twin Suns description dropped (the moon-alignment gloss was wrong); name retained; phenomenon-of-origin filed to `docs/open-threads.md` as a new *Needs writing* item.
- **§5 Blightfather rule** — decision: **Maw Below, Blightfather, and Corrupted God are interchangeable in published prose; lore reference favours *Corrupted God*.** Swept the lore files (`secret-history.md`, `geography.md`, `factions.md`) — all GM-tier prose now reads *Corrupted God*. The Lorant in-world quote in `secret-history.md:219` keeps both folk titles (it's a mortal-voiced document). Glossary entries for *Maw Below* and *Blightfather* updated to record the policy.
- **Pass G (`unplaced.md` trim)** — §12 done. *Recently placed* changelog removed (the record lives in git); the file is now a minimal routing-buffer stub with the *(Currently empty.)* marker. Ready for new unplaced lore when it arrives.
- **Pass E (TBDs → open-threads)** — §9 + §11 done.
  - Geography sub-region `(details TBD)` annotations cleaned: Fellibylur and Balatur Erui pulled one-line glosses in from `glossary.md`; Red Dominion, Haraour Eliza, Earth Realm, Argia Esfera, Namur Republic, Order of Law, Kaosadaemi Principality, Star Island each got a one-line positive descriptor. Deep flavour-passes stay tracked in `docs/open-threads.md` § *Sub-region details*.
  - `secret-history.md` — three TBD-annotation sentences deleted (Araphel's "order of the others joining" line; Devourer's "more detail to be defined later" bullet; Corrupted God's "what it would truly take to end it is not yet defined" trailing clause). Underlying canon (Cannot be permanently killed by conventional means) retained.
  - `bestiary.md` — two changelog/status-note blocks deleted (top-of-file 2026-05-17 status note + Ancestries section reconciliation blockquote); Virtue Demons *Open thread* paragraph deleted (tracked); Sin Devils *Status: Placeholder* paragraph rewritten as a one-line canon statement (seven sins, seven lords; three domains mapped, four open).
  - `cultures.md` — entire Fenurran *Open threads & TBD* section deleted (every item tracked in `docs/open-threads.md`; the two *RESOLVED* strikethroughs went with it since the canon lives in the *The schism* prose already). Kitsune *Open threads & TBD* subsection same treatment.
  - `docs/open-threads.md` — Fellibylur's stale "(Floteyn)" tag fixed to "(Vindul — high lone peak, Storm-Fell / Blizzard Peak)"; the four kitsune-thread *Where* pointers repointed from the deleted subsection to *The Kitsune* section.
- **Pass D (negative recasts)** — §8 done per the user's line-by-line decisions.
  - **Fixed:** `cosmology.md` Gods' Law-as-physics opener; airships-always-Magitech (both occurrences); two-rail-networks-operate-independently; Conductor's Station haunts-both-networks framing; Cloud Sea paragraph rewritten with the new boundary canon (sharp visible boundary, vapor will not support weight, ordinary hulls sink, swimmers drown). `gods.md` Sortalde veil-mediated clerical life; Thirteen treat origins as theirs alone; Council gathers on call. `geography.md` cloudships serve Cloud Sea crossing only; Hafra/Cloud Sea boundary recast as sharp visible line + lethality canon (parallel to the cosmology rewrite). `bestiary.md` Automatons as a distinct ancestry the Empire stopped short of Android-quality; Dragons alien-arrivals truth *reachable to anyone who looks*; Ardande/Talos planar lineages parallel to the bound thirteen (dropped the negative cascade); Aiuvarin/Dromaar as mortal-ancestry mixes; Dhampir hospitality recast as cultural courtesy; bound-gods section retitled *passes outside bloodline* with each god's expression positively framed (Iro=celestial Nephilim, Enki=mind, Jianna=ledger, Cronus=choice). `timeline.md` Thirteen accepted, rest withdrew.
  - **Kept (load-bearing, per user):** `cosmology.md:85` Grand God tier closed; `factions.md:134–141` Mercenary Guild absence-of-record; `factions.md:232` Fodder as punishment; `cultures.md:33` Fenurran Speaker's Mantle; `cultures.md:201` Fenurrans join causes.
- **Pass F (PF2e bookkeeping)** — §10 done. New file **`lore/pf2e-notes.md`** consolidates the system-side meta: roster vs the standard 44 (renames, additions, removals, access tags), Drow Talan-specific framing, Sortalde Tian Xia placements, versatile-heritage Remaster reshuffle (Nephilim absorbs Aasimar+Tiefling, Ardande/Talos planar mapping, Suli generic geniekin), cleric-domain framing (Thirteen / Outside the Thirteen / GM ruling), per-god favoured weapons as mechanical canon. Lore files stripped of PF2e-meta phrasings: `bestiary.md` (Tyrnarra-canon-addition parentheticals on Dragons/Rabbitfolk/Slimes, the Kholo/Tripkee rename notes, "despite the PF2e stereotype" Drow framing, "Mostly unchanged from PF2e canon" Gnome/Poppet tags, "Post-Remaster" heading, "the pf2e remaster reshuffled…" intro, Nephilim PF2e-Remaster opener, "after the remaster reshuffle" heading); `secret-history.md` (Kusarigama PF2e-mechanical clarifier softened, bare `(PF2e)` tags on Android/Automaton dropped); `gods.md` (Domains Outside the Thirteen lead recast in-world, GM-ruling guidance moved to `pf2e-notes.md`); `glossary.md` (Versatile heritage section trimmed of remaster-history framing, cross-refs added to `pf2e-notes.md`).

---

## § High — fix-now

### 1. Meta-instructions to Claude living inside lore files

These are not lore. They are author-side instructions about *how to write the lore*. They pollute the canon and should be removed or rewritten as positive in-world statements.

- **`gods.md:73`** — *"Do not describe Frae City as 'the only neutral ground' — it is Cronus's home, not neutral territory."*
- **`gods.md:75–78`** — entire **"Neutral Ground"** section. Pure negation of a prior claim ("No single city on Talan is universally recognised as neutral ground… Frae City is *not* neutral ground"). Replace with one short positive sentence somewhere appropriate (probably under the Cronus entry, or under Frae City in `geography.md`): *"Frae City is Cronus's home, founded during the Week of Crimson Rain as the base of mortal resistance, and remains the natural ground for the Council of Thirteen because Cronus hosts it."* Then delete the whole section.
- **`gods.md:119`** — *"(Earlier drafts depicted him as a Lizardfolk; this is incorrect — he is a Kobold everywhere in canon.)"* Delete the parenthetical. Komo is a Kobold. The line ends with the depiction, full stop.
- **`secret-history.md:224`** — *"The names **Maw Below** and **Blightfather** are folk titles for the Corrupted God. Use them in mortal-voiced text (sermons, chronicles, peasant rumour); avoid them in GM-truth contexts."* The voice/register guidance is meta-craft, not lore. Reframe as a one-line in-world statement: *"In mortal sermons and chronicles the Corrupted God is named **Maw Below** or **Blightfather**; scholars who know the truth use neither."* (And then enforce the rule — see issue #5 below.)
- **`geography.md:435`** — Frae City line: *"NOT neutral ground — Cronus's home."* Same problem as above. Just say: *"Cronus's home, founded during the Week of Crimson Rain as the base of mortal resistance."*

### 2. Outdated glossary entry — Hungerseed

- **`glossary.md:349`**: *"Hungerseed → half-Oni; **TBD** pending Tian Xia ancestries pass."*
- The Tian Xia pass *has been done* — `bestiary.md:341` gives full Hungerseed canon (Oni as bound spirits of Sortalde, concentrated on Lingdao). Update the glossary entry to match.

### 3. Spelling inconsistency — Harro Distiratsue / Distiratsua

- **`geography.md:299`** (Brauogi sub-regions): *"Harro Distiratsue"* ✓
- **`geography.md:331`** (Egulon sub-regions): *"Harro Distiratsue"* ✓
- **`geography.md:351`** (Emerald Isles → Southern Isle closest neighbours): *"Harro **Distiratsua**"* ✗
- **`glossary.md:126`**: *"Harro **Distiratsue**"* ✓ (with the explicit drift note *-tsu > -tsue*).

Canonical spelling is **Distiratsue**. Fix the one stray *Distiratsua* in `geography.md:351`.

### 4. Two distinct places both named "No Man's Land"

This is a real geographic ambiguity. Two unrelated unclaimed territories carry the same name across the same file:

- **`geography.md:232`** (Sumendar): *"**No Man's Land** — unclaimed territory belonging to no kingdom. Houses Eldara, Komo's city-state."*
- **`geography.md:300`** (Brauogi) and **`geography.md:314`** (Ezkudon): the *other* No Man's Land — *"shared with Ezkudon/Brauogi. Unclaimed territory on the border between the two domains. The wild-touched live here."*

A reader skimming Brauogi → "No Man's Land" naturally assumes the Eldara one. The two are unrelated.

**Recommendation:** rename one of them. Either:
- Give the Sumendar one a proper Basque/Icelandic name (it is the Komo-city-state territory, so it predates the rule and warrants an old name); or
- Give the Brauogi/Ezkudon one a more specific descriptor (e.g. *"the Wildreach"* / *"the Wild-Touched Marches"*, then coin a Basque/Icelandic equivalent).

Whichever you pick, log the coinage in `glossary.md` with etymology, and update both sides of the cross-reference.

### 5. Meta-rule about "Blightfather" / "Maw Below" is contradicted by usage

`secret-history.md:224` says avoid the folk titles in GM-truth contexts. But:

- **`geography.md:150`** (Vermin Queen card, GM-tier description): *"…spider-swarm corruption seeding lesser nests across the plains… the **Blightfather**'s power…"*
- **`geography.md:190`** (Hollow of Ten Thousand Threads → Threats): *"threads carry the **Blightfather**'s power"*
- **`glossary.md:364`** lists Blightfather as a folk title only, with the same "not a personal deity" gloss.

Either:
- Drop the rule (treat *Blightfather* as the canon-wide name for the Corrupted God's reach into the world, used freely); or
- Enforce the rule and rewrite the Hollow / Vermin Queen descriptions to say *"the Corrupted God's power"* in the GM-tier prose.

Pick one and apply across files.

### 6. Glossary "Sun god" entry attached to the wrong bullet

- **`glossary.md:321`** — the line *"**Sun god** — paired-mate to Bikiargi by symmetry but not yet named or detailed; open thread."* is appended to the end of the **Betibizi** bullet. It is a separate concept (the open thread covered in `gods.md` *Open thread — The Sun*) and reads as if it were part of Betibizi's lore.

Move it to its own bullet under *Named Non-Bound Gods*, or drop it entirely from the glossary (it lives in `gods.md` and `docs/open-threads.md` already).

### 7. Twin Suns name vs description mismatch

- **`geography.md:129`**: *"**Twin Suns** — named for a hilltop phenomenon where both moons are visible alongside the sun on clear days."*

The *name* is "Twin Suns" (two suns) but the *description* is "two moons + the sun" (three bodies, not two). Either:
- Rename it (e.g. *"Three-Light"*, *"Tri-Lume"*, then coin); or
- Reword the gloss to fit the name — perhaps the two moons appear *sun-like* in a specific alignment, producing the *illusion of twin suns*.

Whichever you pick, the gloss and the name need to agree.

---

## § Medium — recast negatives, move TBDs to open-threads

### 8. Negative phrasings that should recast as positive

These all carry the same shape: *"X is not Y"* / *"there is no X"*. Each can be rewritten as a positive statement of what *is* true without loss of meaning.

| File · line | Current (negative) | Suggested (positive) |
|---|---|---|
| `cosmology.md:41` | *"It is **not a rule — it is physics.**"* | *"The Gods' Law operates as physics: a god entering the Material Plane is subject to it the way matter is subject to gravity."* |
| `cosmology.md:85` | *"**Impossible by any normal mechanism.** … **There is no replicable path** for any other being to reach Grand God."* | *"Grand God status is fixed: the twelve originals plus Cronus, whose ascent was anchored by the Gods' Law's one-time mechanism. The tier is closed."* |
| `cosmology.md:173, 178` | *"**There are no non-magical airships** — flight requires the magic."* (duplicated) | *"Flight on Tyrnarra is a Magitech property: every airship integrates either Arcanotech rune-lift or an Occultech-bound air elemental as its lift principle."* |
| `cosmology.md:197` | *"**The two are not directly connected.** No through-rail crosses Basogur Jungle."* | *"The northern and southern networks operate independently. Basogur Jungle bisects the east-central waist of Talan; rail stops at its edges on both sides."* |
| `cosmology.md:206` | *"there is no Northern or Southern bias. The Lost and Found does not appear to distinguish between the two"* | *"The Conductor's Station haunts both networks equally. Crews on both halves keep the same warding rituals and tell the same stories."* |
| `gods.md:39` | *"**No bound gods reside there.** All Sortalde clerical work channels through an unnamed Layer-3 pantheon… Sortalde mortals have never seen a god walk among them — religion there is invocation across the veil, never personal audition."* | *"Sortalde's clerical life is veil-mediated throughout. Every grant runs through Layer-3-resident gods — dynasty-spirits, ancestor-judges, place-gods — and reaches the worshipper across the veil. The pantheon is Sortalde-internal and named in the eastern register."* (Then the open-thread about specific names goes to `docs/open-threads.md`.) |
| `gods.md:48` | *"**None of the 13 have explained their own origins.** … Gods do not answer these questions."* | *"The Thirteen treat their own origins as theirs alone. Scholars study them constantly; the gods deflect every question."* |
| `gods.md:72–73` | *"There is **no fixed schedule**; the Council gathers only when something demands the full body in person."* | *"The Council gathers when something demands the full body in person — irregularly, at Cronus's hosting, in Frae City."* |
| `geography.md:20` | *"**Cloudships** are *not* used for routine north-south travel — they're rare specialist Cloud-Sea-crossing craft."* | *"Cloudships serve the Cloud Sea crossing; routine north-south traffic uses ships across Midarra, airships over Basogur, or the overland loop."* |
| `geography.md:34` | *"**No hard boundary** — sailors know when they've crossed over."* | *"The boundary between Hafra and the Cloud Sea is sailor-knowledge: a particular thickening of the air, a shift in the water's weight underfoot, the colour going pale."* |
| `factions.md:134–141` | The Mercenary Guild's structure: *"No official presence… No legal registration, no public charter… Does not exist in remote villages… Nothing on paper. Nothing with a sign."* | *"The Guild operates by absence-of-record: every chapter is informal, deniable, off the books. Town-level chapters work from back rooms; city chapters from quieter ones."* |
| `factions.md:232` | *"**Fodder** — *not* a caste but a punishment."* | *"**Fodder** — a punishment, sitting outside the caste ladder."* |
| `bestiary.md:56` | *"they are not Androids. The differences are deep and the Empire's scholars could not close them."* | *"Automatons are capable — formidable — but a different ancestry. The Empire's scholars approached the Elden's craft and stopped short."* |
| `bestiary.md:96` | *"it is not common knowledge but is not GM-secret either"* | *"The 'alien arrivals' truth is buried in dragon-internal religion and Gods'-Era scholarly archives — reachable to anyone who looks."* |
| `bestiary.md:316–324` | Wood/Metal heritages framed by what they're *not* (*"not divine blood," "neither plane belongs to a bound god," "Talos are not Araphel-aligned," "live without a god-claimant"*). | Lead with the planar origin and the cultural-clustering reality. *"Ardande carry the Feyworld's living-growth element; they cluster wherever their kin are welcomed, by cultural gravity. Talos carry the Shadowplane's eternal-structure element; their communities form around craft and structure."* |
| `bestiary.md:333` | *"These are genetic, not metaphysical — no divine, planar, or otherworldly lineage."* | *"Aiuvarin and Dromaar are mortal-ancestry mixes. Their place in the world is shaped by the politics of the two parent ancestries."* |
| `bestiary.md:339` | *"undead-touched, not god-touched. Vampires are an independent lineage on Talan (not a bound-god creation)… The acceptance is cultural, not doctrinal — Dhampir are not Araphel's by blood."* | *"Dhampir descend from vampires — an independent undead-touched lineage on Talan. Myrkono extends cultural hospitality under Araphel's *new faces / second chances* doctrine; the welcome is social, the lineage stays its own."* |
| `bestiary.md:344–351` | *"Bound gods without heritages"* whole section frames four gods by what they *lack*. | Recast section heading: *"Bound gods whose touch is not bloodline-borne."* Then for each: *"Iro's blessing manifests as celestial Nephilim, included in the universal heritage… Enki's touch manifests as scholarly aptitude rather than physical change… Jianna's blessing accumulates in trade fortune… Cronus's worshippers are made by choice (see secret-history.md — *Cronus — The Secret*)."* |
| `cultures.md:33` | *"there are no kings or queens. There are no permanent generals. There is only the Speaker's Mantle…"* | *"Leadership rests in the Speaker's Mantle — a rotating token held by whichever tribe has most recently proven competent enough to mediate the others."* |
| `cultures.md:201` | *"Fenurrans do not follow orders. They join causes."* | *"Fenurrans join causes. A flawed plan collapses under scrutiny; a sound plan grows stronger with every voice."* |
| `timeline.md:45` | *"More gods could have stayed, but virtually none were willing to be bound."* | *"Thirteen accepted the binding. The rest withdrew to the other planes."* |

### 9. TBD/process notes inside lore — move to `docs/open-threads.md`

These are author-side bookkeeping. The lore should state what *is* canon; the open-thread tracking lives in `docs/open-threads.md`.

- **`geography.md`** — every `(details TBD)` should become either: (a) a one-line positive description of what *is* known, with the deep TBDs moved to open-threads, or (b) deleted from the sub-region list entirely if literally nothing is known beyond the name (in which case the glossary etymology entry carries the placeholder). Specific lines:
  - `:108` Fellibylur — `glossary.md:83` already has the etymology + character. Pull the one-line gloss in.
  - `:206` Balatur Erui — same; `glossary.md:98` has it.
  - `:229` Red Dominion · `:231` Haraour Eliza · `:297` Earth Realm · `:333` Argia Esfera · `:384` Namur Republic · `:385` Order of Law · `:400` Kaosadaemi Principality — these are pure TBD stubs. They all appear in `docs/open-threads.md` § *Needs fleshing out* — geography sub-region small placement-and-flavour passes. Decide: either give each a one-line positive descriptor here, or drop them from the bullet list and rely on the open-threads entry.
- **`secret-history.md:19`** — *"The order of the others joining is not yet defined — to be developed."* The open thread *Order Grand Gods joined Cronus in the Week of Crimson Rain* tracks this in open-threads. Delete the line from secret-history.
- **`secret-history.md:200`** — *"More detail on origin, nature, and current state to be defined later."* (Devourer entry). Same — open-threads tracks *The Devourer — ending mechanism*. Delete.
- **`secret-history.md:211`** — *"What it would truly take to end it is not yet defined."* Same. Open-threads has it.
- **`cultures.md:283–289`** — entire *Open threads & TBD* section for Fenurrans. Either:
  - Move every line to `docs/open-threads.md` and delete the section from cultures.md, OR
  - Convert the resolved ones (Divine Faith, theocratic prince) to plain prose that asserts the canon, and move the remaining open ones to open-threads.
- **`cultures.md:392–397`** — entire *Open threads & TBD* section for Kitsune. Same treatment.
- **`bestiary.md:5`** and **`bestiary.md:39`** — multi-line *Status note* paragraphs describing the 2026-05-16/17 base ancestry rework and the Tian Xia placement pass. This is changelog/process content, not lore. Move to a CHANGELOG section if you want a record, or just delete — git history is the real record.
- **`bestiary.md:403`** — Sin Devils *Status: Placeholder.* paragraph. Open-threads has this thread. Delete and let the table speak for itself (its TBD column already says it).
- **`bestiary.md:385`** — *Open thread* note about virtue-demon catalogue. Open-threads tracks. Move/delete.

### 10. PF2e-bookkeeping meta-notes

Several lines explain Tyrnarra's relationship to PF2e mechanics in the voice of a designer, not the world.

- **`bestiary.md:86`** — *"Tyrnarra-canon addition (not part of the standard 44 PF2e remaster roster — Tyrnarra's Dragons are a unique alien lineage, distinct from PF2e's Dragonet ancestry…)"*
- **`bestiary.md:185`** (Rabbitfolk) and **`bestiary.md:199`** (Slimes) — same *"Tyrnarra-canon addition (not part of the standard 44 PF2e remaster roster)"* note.
- **`bestiary.md:109`** — *"Surface-dwelling, despite the PF2e stereotype: Drow on Talan are children of shadow, not children of the underdark."* PF2e-stereotype framing is meta.
- **`bestiary.md:289`** — Nephilim *"absorbs the old Aasimar/Tiefling split"* — explains remaster history.
- **`bestiary.md:151, 215`** — *(Renamed from Gnoll in the PF2e remaster — Tyrnarra adopts the new name.)*

Decision: either move all PF2e-bookkeeping into one *"Note on PF2e mechanics"* section at the top of `bestiary.md` (one place, one paragraph), or drop the notes entirely and let the canon speak. The world doesn't know it descends from PF2e tables.

### 11. cultures.md resolved-thread strikethroughs

- **`cultures.md:285–286`** — *"~~The Divine Faith~~ — RESOLVED 2026-05-16…"* and *"~~The theocratic prince~~ — RESOLVED 2026-05-16…"*

This is the open-threads.md pattern bleeding into lore. The resolution should already be reflected in the body of `cultures.md` (and it is — *The schism* section at lines 35–39 has the canon). The strikethrough entries are residue. Delete them.

### 12. `lore/unplaced.md`

The file currently contains: *"(Currently empty.)"* and a *Recently placed* changelog. The whole file is a routing buffer for content awaiting placement. With nothing currently unplaced, two options:

- Keep it as a minimal stub (current state) so contributors know where to drop new lore that doesn't fit elsewhere.
- Delete the *Recently placed* changelog (it's git history) and leave the file truly empty save for a header sentence.

Either is fine. Recommended: trim the changelog, keep the file as a routing buffer.

---

## § Low — load-bearing negatives that should stay

These are negative-shaped phrasings that *carry* the information rather than just denying. Leave them.

- **Cover vs. truth framing** — `bestiary.md:342` (Reflection public framing as *"ritual mishap, cosmic blip, or magical duplication; no parent lineage"* — this *is* the public cover); `secret-history.md` Sage Lorant *Age of Corruption* mortal myth (*"It is mostly wrong"* — necessary to flag the gap between mortal belief and GM truth); `glossary.md:354` *"'Elden blood' — the persistent Azarketi inherited claim. **Wrong.**"* (the wrongness *is* the lore — it's the multimillennial transmitted lie).
- **GM-truth secrets** — `secret-history.md:283, 288, 311` (*"The Grand Gods do not know how he did it… No living Reflection knows what they are… The Adventurers Guild does not know this either"*). These are the structural negatives that make the Golden Emperor campaign frame work. The world hangs on what nobody knows.
- **In-world unknowns as canon** — `bestiary.md:90` (*"What specifically was lost — what divine or biological mechanism was severed — is not known. That this fact is unknown is the central strife of Dragon civilisation."*) The unknownness is the lore.
- **Necessary disambiguation** — `bestiary.md:117–121` (Blackened Lands fleshwarps vs Menagerie-made fleshwarps); `bestiary.md:73–77` (two centaur populations); `factions.md:310` (same). Useful and load-bearing.
- **The Devourer / Corrupted God's killability** — `secret-history.md:211` *"Cannot be permanently killed by conventional means."* This is canon about the world's hardest problem; the negative is the substance.

---

## § Suggested order of work

1. **Pass A — meta-pollution (§1).** Delete or rewrite the seven meta-instructions to Claude. Lowest-risk, highest-readability gain.
2. **Pass B — concrete corrections (§2, §3, §4, §6, §7).** Hungerseed entry, Distiratsue spelling, two "No Man's Lands" disambiguation, glossary Sun-god bullet placement, Twin Suns name/desc fit.
3. **Pass C — Blightfather rule (§5).** Decide and apply across files.
4. **Pass D — negative recast (§8).** Mechanical rewrites; ~20 lines across the corpus.
5. **Pass E — TBDs migration (§9, §11).** Move bookkeeping from lore into `docs/open-threads.md`; trim resolved-thread residue.
6. **Pass F — PF2e bookkeeping (§10).** Consolidate or drop.
7. **Pass G — `unplaced.md` (§12).** Trim or leave.

Passes A–C are surgical edits. Passes D–F are the meaningful prose-cleanup work. Pass G is a five-minute decision.

---

**Files touched if all passes are applied:**

- `lore/cosmology.md` — D
- `lore/gods.md` — A, D
- `lore/secret-history.md` — A, C, E
- `lore/geography.md` — A, B, C, D, E
- `lore/factions.md` — D
- `lore/bestiary.md` — D, E, F
- `lore/cultures.md` — D, E
- `lore/timeline.md` — D, E
- `lore/glossary.md` — B
- `lore/unplaced.md` — G
- `docs/open-threads.md` — receives migrated TBDs from E
