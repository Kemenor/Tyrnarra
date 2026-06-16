---
name: virtue-devil-workflow
description: Use this skill whenever designing an individual Virtue Devil of Bolverk (one of the fourteen seat-holders of the ordered ziggurat side) within the Tyrnarra worldbuilding project. Trigger on phrases like "design the [Virtue] Devil", "write the Justice Devil", "flesh out the [virtue] line", "next devil", "give the Courage Devil a holder", "fill a stub card on bolverk.html", working with the Virtue Devils table in lore/geography/bolverk.md, the virtueDevils stub block on bolverk.html, or any session that takes a virtue-line stub from name-on-a-card to fully published entry. The canonical fourteen virtue lines are Courage, Wisdom, Justice, Honesty, Hope, Faith, Loyalty, Compassion, Curiosity, Hospitality, Honor, Mercy, Magnanimity, Creativity; mention of any of their excess/deficiency faces (Recklessness, Cowardice, Cynicism, Folly, Vengefulness, Permissiveness, Indiscretion, Deceit, Delusion, Despair, Fanaticism, Apostasy, Servility, Treachery, Sentimentality, Callousness, Obsession, Apathy, Sycophancy, Xenophobia, Vainglory, Perfidy, Appeasement, Implacability, Vanity, Pettiness, Hubris, Sterility) also triggers. The skill enforces an eight-phase workflow adapted from sub-region-workflow: canon pre-read, seed questions, seed generation under the could-this-hold-any-other-line specificity test, naming pass with first-devil pattern locks, surface-before-writing pauses, the consistency ledger (timing + reciprocal cross-references, the lesson of the Vice Demon consistency pass), and the lore-first / surface-before-HTML protocol from CLAUDE.md. The seven finished Vice Demon entries in lore/geography/bolverk.md are the quality bar and structural template. Do not use for Vice Demon edits, Bolverk city geography, Independents, sub-region or kingdom design (use sub-region-workflow), or the Bound Thirteen.
---

# Virtue-devil workflow

## What this skill is for

Taking a Virtue Devil from "virtue line on a stub card" (a row in the canonical-fourteen table in `lore/geography/bolverk.md`, a placeholder card in the `virtueDevils` block of `published/setting/cosmology/bolverk.html`) to a fully fleshed seat-holder with the same depth as the seven Vice Demons, and optionally to a published card, inside a single session, with the user's voice setting direction at every phase boundary.

The quality bar is the Vice Demon roster. Each of the seven is a complete character study: an origin life, a corruption arc, a seat-taking that *enacts the vice*, a form whose gimmick *is* the vice, a spire that dramatises it, a Talan-side method, a reputation web, a load-bearing GM Secret, a bespoke structural weakness, and PF2e mechanics. Read Veislur (the innkeeper whose framing never broke) and Lostar (the engineer of desire who has never wanted) side by side before designing any devil; they teach what "the character could hold no other seat" feels like.

## Why this skill exists

Two lessons feed it.

First, the sub-region-workflow lesson: designs led by archetype-and-slot produce templates with the labels swapped. A devil designed as "the [Virtue] Devil, who corrupts [virtue]" is the demon-side equivalent of "a merchant republic of Halflings". The seed comes first; the seat emerges from it.

Second, the Vice Demon consistency-pass lesson (2026-06-03): the seven demons were written one after another, and a later pass had to repair rank contradictions (Reidar mislabelled second-oldest), era/age arithmetic (Veislur's 650-vs-720 years and a misattributed Adventurer-Era arrival), a double-running clock (Ofunda's seventy-vs-forty-five years), and a sheaf of one-sided cross-references. This skill bakes the fixes in at design time: every devil carries explicit seat-taking dates checked against `lore/timeline.md` and the current year, every cross-reference is written on *both* entries in the same pass, and a running ledger keeps the fourteen ordered and distinct.

## How devils differ from demons (the design constraints)

These are canon in `lore/geography/bolverk.md` and every entry must hold them:

| Axis | Vice Demons (the seven) | Virtue Devils (the fourteen) |
|---|---|---|
| Theology | *Embody* a vice; foundational | *Corrupt* a virtue; parasitic on the virtue line |
| Internal structure | One vice, pure | **Both extremes within one being**: excess-face and deficiency-face, seated on the false-mean between |
| Governance | Anarchic, kill-and-replace, no leader | **Council of Fourteen**, consensus-bound ritual debate, no leader |
| Architecture | Independent spires, as far apart as rivalries demand | Vertically-split ziggurats in a tetradecagram around the Council Hall |
| Seat turnover | Seats change when a stronger holder walks in | Seats are individually killable but **rarely change** |
| Recruitment on Talan | Proliferate around mortals who *choose* a vice | Proliferate around mortals who have already *half-corrupted* a virtue |
| Redemption | Possible in principle; the contrary virtue still runs through them | Possible in principle; **every devil retains the seed of the virtue it perverts** |

Three craft consequences:

- **The false-mean discipline.** A devil written as only its excess or only its deficiency is a demon-shaped design and gets rewritten. The devil reads the mortal and tips whichever way will damage more; the entry must show both faces working, and show the devil *looking, from a distance, like the virtue itself*.
- **The virtue must be real.** Parasitic corruption needs a genuine virtue to feed on. Somewhere in the entry (usually the GM Secret or the weakness) the retained seed of the true virtue must be visible. This is also where the Enki-aligned exorcist canon bites: the corruption fails when the true mean is restored, so each devil's weakness should be a specific, story-usable expression of its virtue's true mean.
- **Tenure skews ancient.** Because devil seats rarely change, most of the fourteen should be long-tenured; recent seat-changes are notable events with Council-level consequences, used sparingly (the inverse of the Vice side, where Ofunda's forty-five years is unremarkable).

## On invocation, before anything else

1. **`CLAUDE.md`** if not already in context: naming rule, lore-first protocol, affirmative prose, no em-dashes, mortals-not-humans, surface-before-writing.
2. **`lore/geography/bolverk.md` end-to-end.** Mandatory per `docs/site-inventory.md` ("read before drafting any infernal seat"). The Virtue Devils section, the canonical-fourteen table, the Demon/Devil distinction, the soul-claim mechanic, *and all seven Vice Demon entries*, which are both template and cross-reference surface.
3. **Grep the project for the virtue name and both face names.** Existing hooks constrain the design (see *Existing hooks* below); a face name like Vengefulness may already be committed canon.

If any canon contradicts what you were about to draft, the canon wins. Surface the conflict in chat before adapting.

## The eight phases at a glance

| Phase | What happens | Phase boundary discipline |
|---|---|---|
| **0. Read the canon** | bolverk.md end-to-end + cosmology (Gods' Law scope, soul-routing) + timeline + glossary + registrar + the stub card + project grep + the ledger | Do not start Phase 1 until done |
| **1. Seed questions** | Ask the user 3-5 targeted questions about the corruption, the two faces, the origin class, the visitor's image, and the Council posture | Chat only. No writes. |
| **2. Generate seeds** | 2-3 distinct seeds, each a person-shaped image or contradiction; each passes the could-this-hold-any-other-line test; each names what origin, faces, and Council role *emerge*. Diversity-check against the ledger. End with a recommended pick | Chat only. No writes. |
| **3. User picks + refines** | Axis-confirmation only. One or two clarifying questions on era, origin, face-preference, hooks | **Axis-confirmation is not a green light to draft prose** |
| **4. Naming pass** | 3-5 candidates per name slot with full etymology; collision-check; first-devil pattern locks if this is the first | Chat only |
| **5. Surface the prose draft** | Draft the full bolverk.md entry, glossary entries, registrar row, ledger update. Grill it (see *Grilling the devil*). Flag every derivation beyond the user's picks | **Do not commit to files yet** |
| **6. Commit lore** | On explicit go: bolverk.md entry + named-so-far line, glossary.md, open-threads.md, ledger | Lore is now canon. **Do not touch HTML** |
| **7. HTML publish** | On explicit publish signal: replace the stub card in `published/setting/cosmology/bolverk.html` with a full card, update `published/setting/cosmology/pf2e-registrar.html`, `docs/site-inventory.md`, and any cross-page mentions | Generator already renders seated-vs-stub cards; replace the line's stub with a full card; see Phase 7 |

The phase boundaries are review checkpoints. Pause at each one even under broad "work through it" framing. Reading is fine within a phase; writes trigger the boundary.

---

## Phase 0: Read the canon

1. **`lore/geography/bolverk.md`** end-to-end. The Virtue Devils section is the frame; the seven Vice Demon entries are the template and the relationship surface; the soul-claim table governs how a devil's bargains tag souls (Ofunda arrived *pre-tagged* by a devil's mark; that is the harvest mechanic working).
2. **`lore/cosmology.md`**, the Gods' Law sections: the Layer-1/3-residency clause is what lets Bolverk's seat-holders reach Talan only through whispers, bargains, and mortal mediation. A devil's Talan-side method must fit inside it.
3. **`lore/timeline.md`**: era anchors for the origin life and the seat-taking date. Current year 2532 MR; eras from Creation to Adventurer. Every date in the entry must reconcile against this file.
4. **`lore/glossary.md`**: the Vice Demon names block (naming precedent), plus any prior devil entries.
5. **`published/setting/cosmology/pf2e-registrar.html`**: the within-pantheon no-sharing rule, the Bound 13's 46 domains, the demons' 25, the cross-pantheon co-grant pattern, the pending domains (several carry non-devil candidate grantors; Swarm sits with the Vermin Queen, Undeath with Betibizi), and the two never-assigned lines (Dragon, Moon).
6. **`published/setting/cosmology/bolverk.html`**: the `viceDemons` card schema (the publish target shape) and the `virtueDevils` stub block (what gets replaced).
7. **`docs/open-threads.md`**: the Vice Demon politics thread and any devil-related entries.
8. **The consistency ledger** (see below): the already-written devils side by side, plus the demon roster, for same-iness and timing.
9. **Grep the project** for the virtue name and both face names.

---

## Phase 1: Seed questions (chat only)

Read what the canon has settled and don't ask those. Pick 3-5 from these categories, tailored to the virtue line:

- **The corruption question.** What does this virtue look like one step before it breaks? Who on Talan is half-corrupting it right now: which professions, which institutions, which kinds of mortal? (The devil's congregation defines the devil.)
- **The two-faces question.** Which face leads in your mind for this holder, excess or deficiency, and what does the quiet face look like when it finally shows? (Both must exist; the question is temperament, the canon allows per-target tipping either way.)
- **The origin-class question.** What was this devil before the seat: mortal soul, fallen divine, devilborn of the ziggurat side, original holder, something stranger? Check the ledger: the demon side deliberately varies its origin classes (fallen Nephilim demi-god, dead frontier god, Outer being, Dark-Era innkeeper, Adventurer-Era pirate lord, mortal merchant's daughter, demonborn); the fourteen should spread at least as wide, and should skew long-tenured.
- **The visitor's image.** A petitioner climbs the ziggurat: what is the one thing they remember? The texture, the sound, the wrongness that looked like rightness.
- **The hooks question.** Which committed canon already touches this line? (Justice: Ofunda's debt. Honesty, Honor, Loyalty: Lostar's apprentices. See *Existing hooks*.)
- **The Council question.** What is this devil at the table of Fourteen: the slow voice, the procedural blade, the swing seat, the one who has spoken twice in a century? And where do they stand on the standing truce between the banks (the publicly-known peace)? **Do NOT position them on the uncalled Ofunda debt.** That debt is known to exactly two beings in creation, the debtor (Ofunda) and the keeper (Jafnar); no other demon or devil knows it exists. Only Jafnar's and Ofunda's own entries may reference it. (See *Existing hooks* and *Hard rules*.)

Surface the answers back as a 4-6 sentence summary before generating seeds.

---

## Phase 2: Generate seeds (chat only)

Generate **2-3 distinct seeds**. A devil-seed is a person-shaped image or contradiction from which the whole entry unfolds: the origin, the faces, the ziggurat, the method, the secret.

### What a devil-seed is

- An **image** (an innkeeper at his stove, feeding a village that cannot ask what is in the pot)
- A **contradiction** (lust embodied who has never wanted; a hoarder whose hoard is one entry short of total)
- A **corruption arc in miniature** (a god of the unbroken line who held it into pointlessness and turned)
- A **bargain-shape** (a creditor who grants exactly what is owed by right, and owns you by the framing)

### What a devil-seed is NOT

- The virtue line restated ("the Courage Devil corrupts courage")
- An excess/deficiency pair with adjectives attached
- A monster design (horns, fire, a big sword) with the virtue painted on
- A Council job description

### The specificity test, devil edition

Each seed must pass all three:

1. **Could this character hold any other virtue line?** If yes, the seed is not specific enough. The demon-side bar: Veislur's meal-takeover could belong to no seat except Gluttony; Nirfel's gifted cache to none except Greed.
2. **Does the seed produce both faces?** The excess and the deficiency must both be visible in the character, with the false-mean between them. If the seed only yields one face, it is half a devil.
3. **Does the retained virtue-seed survive in it?** Somewhere in the character the true virtue must still be findable; that is what parasitic corruption means, and it is where the secret and the weakness will live.

### Per-seed contents

- **A 2-3 sentence pitch** leading with the image or contradiction. Mechanics do not appear in the pitch.
- **"What follows from this"**: one short paragraph naming the origin class and era, the leading face, the ziggurat's individual character, the Talan-side method, and the Council posture, all emerging from the seed.
- **The seat-story sketch.** How they came to hold the seat. The demon precedent: every takeover *enacts the vice* (a gift for Greed, a meal for Gluttony, engineered yearning for Lust, a watched weakness for Envy). A devil's seat-story should enact the virtue's corruption. Remember tenure skews ancient; "inherited at the founding and never challenged" is a legitimate devil answer in a way it is rarely a demon answer.
- **Cross-canon hook**: how this rhymes with or binds to committed canon.
- **The specificity result**: one line confirming the test and naming what would have to change to hang this character on a different line. If the answer is "the virtue's name", the seed has failed; rewrite.
- **Ledger check**: origin class, era, gender, register, and secret-shape compared against the existing holders (both rosters). Two devils with the same secret-shape (e.g. two "never felt the thing they embody" inversions) is same-iness; the demon side already owns that shape via Lostar.

End with a recommended pick.

---

## Phase 3: User picks + refines (axis-confirmation, NOT a green light)

User picks one, combines two, or inverts one. Ask one or two clarifying questions: era of the origin life, which hooks to honor now versus leave open, leading face, any cross-reference targets among the demons or seated devils. Do not draft prose yet.

---

## Phase 4: Naming pass (chat only)

Offer 3-5 candidates per name slot with full etymology, recommend one, wait for the user pick. Record everything in `lore/glossary.md` at commit time.

### Name slots

- **Seat-name** (the name the city uses, parallel to Drambur/Nirfel/Lostar/Ofunda/Veislur/Reidar/Lethar).
- **Former name**, if the origin life had one: era- and culture-appropriate register (the Henrick Brodd / Mara Goldwake / Atezar / Klumpa pattern; a Gods'-Era figure drifts Basque/Icelandic, a Dark-Era mortal takes lightly drifted English, a regional-register mortal takes their region's register).
- **Ziggurat by-name**, if the building earns one (the Long Inn / the Vault / the Library pattern).

### First-devil pattern locks

The first devil designed locks three patterns for all fourteen. Decide them deliberately, with the user, and record the decisions in the glossary:

1. **Seat-name derivation.** The demon precedent is a drifted Icelandic word for the vice. Recommended devil parallel: a drifted Icelandic or Basque word for the **virtue** (the devil sits on the false-mean and wears the virtue's face; the name should too). Confirm or replace this rule at the first naming pass; apply it consistently afterward.
2. **Favored-weapon rule.** The demons each carry one distinct PF2e **Advanced-category** weapon, and the fourteen follow the same rule: one Advanced weapon per holder, distinct across all twenty-one seat-holders citywide, thematically locked to the line. The ordered side tends to a formal/courtly register, but it stays **Advanced**. **Verify the category against the bestiary data, never from memory** (it has been mis-recalled repeatedly, e.g. Bladed Scarf and Flyssa are Martial, not Advanced): query `tools/encounterBuilder/items.db`, e.g. `python -c "import sqlite3; [print(r) for r in sqlite3.connect('tools/encounterBuilder/items.db').execute(\"SELECT name,grp FROM items WHERE item_type='weapon' AND category='advanced' ORDER BY grp,name\")]"` for the full candidate list, or filter by `name` to check one weapon. **Taken so far:** Aldori Dueling Sword, Flying Talon, Bladed Hoop, Visap, Karambit, Spirit Thresher, Dwarven Dorn-Dergar (the seven demons); Hook Sword (Jafnar), Bladed Diabolo (Sannar), Spiral Rapier (Drengar). **Lone exception on record:** Vondar's Khakkara (the ringed mendicant healer-staff; spelled **Khakkhara** in items.db and on AoN, where it is Martial) is kept by author's call because no Advanced weapon fits a healer's staff. Do not "correct" it, and add no new exceptions without the same justification.
3. **Domain allocation sketch.** Before the first devil's grants are locked, pencil a light 14-row allocation across all virtue lines (3-5 domains each, no duplicates within the fourteen, cross-pantheon co-grants with the Bound 13 and the demons allowed and expected). Greedy per-devil picking will strand later lines; the sketch is a pencil-tier draft, revisable, but it must exist. Respect the registrar's pending notes (several open domains have non-devil candidate grantors) and the never-assigned pair (Dragon, Moon) unless the user opts in.

### Collision check

*Compact* is reserved (the Gods' Law). *Order* is heavy traffic. **Muiral** is retired but unbound: the name may return if it genuinely fits a line, and only then. Check every coined name against the glossary before suggesting it.

---

## Phase 5: Surface the prose draft for review

Draft the full entry and surface it in chat. **Do not commit yet.** Flag every derivation that went beyond the user's explicit picks.

### The complete devil entry (the template, mirroring the Vice Demon entries)

A `### [Seat-name]: the [Virtue] Virtue Devil` section in `lore/geography/bolverk.md` containing, in order:

1. **Origin / former life.** Origin class, era, the life before the seat (or the founding, for an original holder). Dates reconciled against `lore/timeline.md`.
2. **The corruption arc.** The virtue genuinely held, then half-corrupted, then tipped. The arc must show the virtue real before it broke; a devil that was never virtuous is a demon wearing the wrong coat.
3. **The seat-taking.** How they came to the seat, enacting the line. State the tenure explicitly (years or era-anchor) and slot it into the ledger ordering as you write.
4. **Form.** A physical gimmick that *is* the false-mean: the body should be able to show excess-face, deficiency-face, and the deceptive mean, the way Drambur cannot appear smaller and Ofunda is always one detail short.
5. **The ziggurat.** The shared architecture (excess-face upper tier, deficiency-face lower tier, the holder seated on the false-mean between) individualised by this holder, the way each demon's spire individualises anarchy.
6. **Method on Talan.** Who they cultivate (mortals who have half-corrupted the virtue), what the bargain-shape is, how the tipping works per target, and how the marks tag souls for the Tunsund (the pre-tagged routing is the harvest). The Enki-exorcist counter applies; the entry can acknowledge what the exorcists know of this line.
7. **Seat at the Council of Fourteen.** Devil-specific, with no demon equivalent: their voice in consensus debate, their alliances and oppositions among the fourteen, their stance on the détente. **Do not give a non-Jafnar devil any position on the uncalled Ofunda debt:** the debt is known to exactly two beings, the debtor (Ofunda) and the keeper (Jafnar), and no other seat knows it exists (see *Hard rules* and *Existing hooks*).
8. **Reputation.** Among the fourteen and across the Tunsund. Every named relationship is written reciprocally (see the ledger).
9. **⚿ GM Secret.** The load-bearing inner truth, usually touching the retained seed of the true virtue. The demon-side pattern: the secret is the wound at the center (the framing that never broke, the cache she lost, the want she has never felt).
10. **Secret weakness.** The structural opening, bespoke and story-usable, normally an expression of the line's *true mean* restored (the devil-side counterpart of the Salute of the Last Door and the presented lost cache).
11. **Domains & Favored Weapon.** PF2e grants per the allocation sketch, with one-line justifications per domain; the favored weapon per the locked rule.

Plus, in the same draft: **glossary entries** (seat-name, former name, ziggurat by-name, each with source language, literal meaning, drift step), the **registrar row** updates (pencil), the **named-so-far line** update in bolverk.md, and the **ledger** update.

### Voice and tier

Bolverk canon is GM-leaning by nature, but the discipline still applies: the entry's open sections are what Bolverk itself could know; the `⚿ GM Secret:` heading marks what even Bolverk does not. No em-dashes. Affirmative prose. Mortals, not humans. Concrete sensory detail over abstraction (the smell of the ziggurat's third tier, the sound the Council door makes, the gesture the devil's petitioners learn).

---

## Phase 6: Commit lore (on explicit go)

| File | What goes there |
|---|---|
| `lore/geography/bolverk.md` | The full devil entry under *Virtue Devils: the Fourteen*; update the **Named Virtue Devils so far** line; reciprocal cross-reference lines added to any demon or devil entry named in Reputation |
| `lore/glossary.md` | Seat-name, former-name, and ziggurat etymologies; the first-devil pattern locks if newly decided |
| `docs/open-threads.md` | Open or update a Virtue Devils rolling thread (mirror of the Vice Demons thread): who is seated, what each entry left open, the allocation sketch's pencil state |

Lore is now canon. **Do not touch HTML** without an explicit publish signal (*publish*, *render the card*, *make it live*, *put it on the site*, *mirror to HTML*).

---

## Phase 7: HTML publish (on explicit publish signal)

1. **`published/setting/cosmology/bolverk.html`**: replace the virtue line's stub card with a full card using the same field schema as the `viceDemons` entries (name, line, location, orb emoji, accent + orbBg + orbGlow, heldSince, domain, weapon, etymology, summary, the labelled sections, reputation with `#anchor` links, secretTitle / secretLabel / secret). **Structural note:** the `virtueDevils` block already renders seated devils as full cards while unseated lines keep their stubs; that generator was established at Jafnar's publish, so the rework is done. For each new devil, supply the full card fields for its line, leave the other lines as stubs, and verify the remaining stub cards still render.
2. **Anchors and reciprocity**: if the new card references a demon (or vice versa), add the reciprocal sentence to the other card in the same pass, with `#anchor` links both ways.
3. **`published/setting/cosmology/pf2e-registrar.html`**: move the devil's domains from pending to granted; record cross-pantheon co-grants in the *Granted by* column; update the summary counts.
4. **`docs/site-inventory.md`**: update the `published/setting/cosmology/bolverk.html` entry's Virtue Devils description (stub count down, seated count up, named entry summarised).
5. **heldSince discipline**: the card's `heldSince` field states tenure *and* rank context only if the rank is arithmetically true against the ledger (the Reidar second-oldest error is the cautionary tale).

---

## Grilling the devil (grill-me integration)

Use the `grill-me` skill before Phase 5 commits to prose, and again on the surfaced draft if any section reads thin. One question at a time, each with a recommended answer drawn from canon; read the lore file instead of asking when the answer is on disk. The devil-adapted grilling axes, in order:

1. **The line.** What does this virtue look like the day before it breaks? Concrete mortal, concrete moment.
2. **The seed.** Could this character hold any other line? Push until the answer is no.
3. **The two faces.** Show me the excess working on one mortal and the deficiency on another. If only one face has scenes, the false-mean is decorative.
4. **The sibling contrast.** Name the nearest neighbor: the demon or devil this one most resembles in secret-shape, origin, or method. What separates them? (Lostar owns "never felt the thing embodied"; Veislur owns "the framing never broke"; Ofunda owns the watcher; do not reissue these.)
5. **The bargain.** What exactly does a mortal receive, what exactly does it cost, and what does the mark on the soul do at the Tunsund?
6. **The Council.** How does this devil vote, and where does it stand on the standing truce between the banks? (Do NOT ask about the uncalled Ofunda debt: only Jafnar and Ofunda know it exists. If and only if you are grilling the Justice Devil himself, ask why he has not called it.)
7. **The retained seed.** Where does the true virtue still live in them? If nowhere, the design has drifted demon-side.
8. **The weakness.** Is it bespoke, structural, and usable at a table? "Restore the true mean" is the mechanism; the entry needs the *specific* form it takes for this devil.
9. **Naming.** Stratum, literal meaning, drift step, collision check, pattern-lock conformity.
10. **The timing check.** Seat-taking date against timeline.md, tenure against 2532 MR, rank claims against the ledger.

---

## The consistency ledger

Maintain a running ledger as devils accumulate, updated at every Phase 6 commit (a section in the Virtue Devils open-thread entry is the natural home). It holds:

- **Tenure ordering**, youngest to oldest, with seat-taking anchors. The demon-side reference ledger: Ofunda (~45 yrs) → Nirfel (~140) → Lostar (~400) → Veislur (~720, Dark Era death) → Reidar (shortly after the Gods' Law was sealed; third-oldest) → Drambur (close of the Gods' Era; second-oldest) → Lethar (original holder, predates Bolverk). The fourteen get the same ledger, and any rank language in prose ("second-oldest of the fourteen") must be arithmetically true against it.
- **Cross-reference map.** Every relationship is written on both entries in the same pass. One-sided references are permitted only as deliberate characterisation (the Drambur-ignores-what-unsettles-him pattern) and are flagged as deliberate in the ledger.
- **Diversity ledger.** Origin classes, eras, leading faces, secret-shapes, weapon picks, and registers used so far, demon and devil sides both, so same-iness is caught at Phase 2 rather than after publication.

---

## Existing hooks already in canon (honor these; do not contradict them)

- **The Justice Devil and Ofunda's debt.** Committed canon: Ofunda's catalysing bargain was with the **Justice Devil's Vengefulness face** ("grants on the framing of what is owed by right"); the mark survived her death and ascension; she has refused the debt since arriving seventy years ago, the forty-five seated years of which make the refusal heresy (a Vice Demon owing a Virtue Devil breaks the unwritten parity); calling the debt publicly hands the Council of Fourteen a casus belli; he has not called it; he could twist the thread to feed information or favours through her instead of cutting it. **The debt is secret: it is known to exactly two beings in creation, the debtor (Ofunda) and the keeper (Jafnar). No other demon or devil knows it exists, and no seat other than these two may know, reference, or act on it.** **Designing the Justice Devil means answering, in character, why he has not called it.** The restraint is load-bearing for the whole city and must come out of the corruption itself, both faces considered (Vengefulness waits for the moment of maximum owing; Permissiveness lets the debt ride).
- **Lostar feeds four lines.** Her successful apprentices drift into **Deceit** (Honesty-deficiency), **Vainglory** (Honor-excess), **Perfidy** (Honor-deficiency), and **Treachery** (Loyalty-deficiency) in their later careers; "the Virtue Devils across the Tunsund quietly benefit." The Honesty, Honor, and Loyalty devils each receive this supply; their entries should know it, and whether they know *where it comes from* is a design choice per devil.
- **The détente watchers.** The Virtue Devils watch **Reidar** more carefully than any other Vice Demon (the breaking point if the détente fails) and watch **Lethar** with the same care inverted (the proof it holds). Each devil's Council section can position itself against this watch.
- **The shared city.** Border deals happen on the neutral strip between flood-cycles; councils-to-councils negotiation is rare; lower-tier demons and devils deal pragmatically at the channel-bank constantly. The feudal-tithe model runs on the devil side exactly as on the demon side.
- **The fourteen-line table is locked.** Courage, Wisdom, Justice, Honesty, Hope, Faith, Loyalty, Compassion, Curiosity, Hospitality, Honor, Mercy, Magnanimity, Creativity, with their excess/deficiency faces as tabled in bolverk.md. New lines and renamed faces are out of scope; Modesty stays retired with Muiral.

---

## Hard rules (non-negotiable; violating drafts get rewritten)

- **The false-mean discipline.** Both faces present and working; the devil tips per target; the seated shape looks like virtue from a distance.
- **The retained seed.** The true virtue is findable somewhere in every entry; redemption stays possible in principle.
- **The seat-story enacts the line.** The way they hold or took the seat is the corruption in miniature.
- **The specificity test.** Could this character hold any other virtue line? If yes, rework before commit.
- **Tenure skews ancient; rank claims must be arithmetically true** against the ledger and `lore/timeline.md` (current year 2532 MR).
- **Reciprocal cross-references in the same pass.** A relationship written on one entry only is a bug unless ledger-flagged as deliberate characterisation.
- **Pantheon mechanics.** No domain duplicates within the fourteen; cross-pantheon co-grants welcome; one distinct favored weapon per holder per the locked rule; the allocation sketch exists before the first grants lock.
- **Naming stratum + collision check + glossary etymology** for every coined name; first-devil pattern locks recorded.
- **No em-dashes. Affirmative prose. Mortals, not humans.** En-dashes for numeric ranges only.
- **Lore-first; surface-before-writing; HTML only on an explicit publish signal.**

---

## Common pitfalls

- **Designing a demon with a virtue's name on it.** If the character embodies a single failure-mode purely, it is demon-shaped. The devil holds two failure modes and a false mean.
- **The virtue painted on a monster.** Horns-and-menace first, virtue rationalised after. Seed first; the body comes out of the false-mean.
- **Reissuing a demon's secret-shape.** Lostar owns the never-felt-it inversion, Nirfel the single missing entry, Veislur the unbroken framing, Drambur the scoured name, Reidar the Law-dependent banishment, Lethar the doctrinal stillness, Ofunda the watcher's catalogue. Fourteen more seats need fourteen more shapes.
- **Greedy domain picking.** Three devils in, the thematically obvious domains are gone and the Hope Devil is granting leftovers. The allocation sketch exists to prevent this.
- **Unreciprocated relationships.** The Vice Demon consistency pass existed because of these. Write both sides in the same pass.
- **Untethered dates.** "Centuries ago" that contradicts the era math, ranks that contradict the ledger, an arrival-era that confuses the soul's fall with a later discovery (the Veislur error). Reconcile every date against timeline.md before surfacing.
- **Forgetting the Council.** A devil entry without a Council posture is half an entry; the ordered side's politics is consensus, and every seat has a voice in it, even a silent one.
- **Breaking the Justice restraint, or leaking the secret.** The Ofunda debt is known to exactly two beings: the debtor (Ofunda) and the keeper (Jafnar). **Any devil other than Jafnar who knows the debt exists, references it, or acts on it breaks hard canon** (*"known to two beings in creation"*, stated in both Ofunda's and Jafnar's entries). A non-Jafnar devil's Council stance is about the standing truce, never the debt. Any entry that makes the uncalled debt incoherent, or calls it casually, also breaks the city's standing tension.
- **GM-tier leaking into open card text.** The secret fields exist; use them.
- **Touching HTML without a publish signal.** Stay in lore by default.

---

## Worked reference (read these in order)

1. **Veislur** and **Lostar** entries in `lore/geography/bolverk.md`: the bar for character-could-hold-no-other-seat and for secrets that are wounds, not trivia.
2. **Ofunda's** entry: the bargain-with-a-devil mechanics from the mortal side, the pre-tagged routing, and the debt the Justice Devil holds; the single richest devil-side hook in canon.
3. **Reidar** and **Drambur** entries: era-anchored ancient tenure done correctly (post-consistency-pass), including how rank language is phrased against the ledger.
4. **The Virtue Devils section** of bolverk.md: the false-mean architecture, the Council, the tipping mechanic, the exorcist counter, the locked table of fourteen.
5. **The `viceDemons` block** in `published/setting/cosmology/bolverk.html`: the publish-target card schema, anchor-link reciprocity, and the heldSince phrasing conventions.
