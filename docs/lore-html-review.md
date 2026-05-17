# Lore ↔ HTML Review

A coverage pass: does the HTML mirror the lore, and is there critical canon on either side that the other is missing?

**Method.** Read each top-tier HTML page (index, magic, talan, grand-gods, history, the-binding, bestiary) plus a representative sample of domain and sub-region pages; grep the full HTML tree for the specific facts most recently edited in lore; flag both directions of drift. The lore-first protocol is the standard: where the two disagree, the lore is canon and the HTML is stale.

Triage tiers:
- **High** — concrete contradictions, factual staleness from recent lore canon changes, meta-pollution on HTML mirroring the same pattern we just cleaned in lore.
- **Medium** — Pass D negative-recast prose that hasn't propagated to HTML yet, and named lore canon that no HTML page surfaces.
- **Low** — minor stylistic drift, optional design choices (e.g. whether a GM truth surfaces in one place or many).

---

## § High — fix-now

### 1. Cloud Sea canon update never propagated to HTML

Pass D rewrote the Cloud Sea canon: **sharp visible boundary** (not gradual), **lethal to cross without a cloudship** (vapor will not support weight, ordinary hulls sink fast, swimmers drown because the cloud reads as solid until they try to grip it). Three pages still carry the old "gradual boundary / slowly sink" framing.

- **[index.html:240](index.html:240)** — *"…each day and night sinking into, and rising from, the Cloud Sea's horizon."* OK.
- **[index.html:244](index.html:244)** — *"Ships that are not built for its surface slowly sink without trace."* **STALE.** Should reflect the lethal-and-fast framing: ordinary hulls sink fast with the crew; swimmers drown.
- **[talan.html:72](talan/talan.html:72)** (Hafra card) — *"the boundary is gradual — sailors know when they have crossed it, though they cannot point to where."* **STALE — directly contradicted by new canon.** Should read: sharp visible boundary, recognisable kilometres out, where water ends and cloud begins.
- **[talan.html:77](talan/talan.html:77)** (Cloud Sea card) — *"Conventional ships that attempt to cross it sink slowly and silently, pulled under by something that does not behave like ordinary water."* **STALE.** Should align with the new canon: vapor will not support weight; hulls sink fast; swimmers drown.

Recommended action: rewrite the three card bodies to mirror `cosmology.md → The Cloud Sea` and `geography.md → Hafra / The Cloud Sea`. Keep the existing prose voice; just swap the lethality framing.

### 2. "No Man's Land" still in use for the Brauogi / Ezkudon border

Pass B renamed the Brauogi/Ezkudon shared sub-region to **The Wildreach** (the Sumendar Komo-city-state territory kept the *No Man's Land* name to disambiguate). Two pages still use the old name for the Brauogi side:

- **[brauogi.html:86](talan/domains/brauogi/brauogi.html:86)** — sub-region card titled *"No Man's Land"*. Should be *"The Wildreach"*.
- **[ezkudon.html:54](talan/domains/ezkudon/ezkudon.html:54)** — sub-region card titled *"No Man's Land"*. Should be *"The Wildreach"*.

The Sumendar references at **[sumendar.html:48, :74](talan/domains/sumendar/sumendar.html:48)** are correct (that's the Komo-city-state *No Man's Land*, distinct from the Wildreach).

### 3. Distiratsua spelling holdout

The canonical spelling is **Distiratsue** (per glossary.md drift note: *-tsu > -tsue*). One HTML location still has the old *Distiratsua*:

- **[emerald-isles.html:103](talan/domains/zuzental/emerald-isles.html:103)** — Southern Isle's mainland-neighbours line lists *"Harro Distiratsua"*. Fix.

(`brauogi.html`, `egulon.html`, and `domains.html` all use the correct *Distiratsue*.)

### 4. Frae City meta-instruction still on askamira.html

The same parenthetical we stripped from lore (Pass A) is still on the HTML:

- **[askamira.html:46](talan/domains/askamira/askamira.html:46)** — *"The Free City (NOT neutral ground — Cronus's home)"*.

Recast positively, matching the lore: *"The Free City — Cronus's home, founded during the Week of Crimson Rain as the base of mortal resistance."* The other Frae City references across the site (talan.html, factions.html, domains.html, crossroads.html) already frame it correctly.

### 5. Twin Suns wrong description still live

Pass B (§7) dropped the wrong moon-alignment description from lore (the name *Twin Suns* refers to a still-TBD phenomenon, not the sun-plus-moons gloss). One HTML location still carries the wrong description:

- **[lautara.html:81](talan/domains/lautara/lautara.html:81)** — Twin Suns sub-region card body reads *"On clear days both moons are visible alongside the sun."* **STALE.**

For the interim: drop that sentence; replace with the Soul Tree adjacency only, or a brief *"named for a phenomenon native to the sub-region — origin in canon-work."* Once we coin the actual phenomenon (per the open thread), drop it in here.

---

## § Medium — Pass D recasts not yet on HTML

Pass D rewrote ~16 negative-shaped statements across the lore. The recasts haven't propagated to the corresponding HTML prose. None of these are factual contradictions; they're prose drift between two surfaces of the same canon. Listed by file:

### bestiary.html

- **[bestiary.html:154](talan/bestiary.html:154)** — Drow line: *"Surface-dwelling children of shadow — not the underdark stereotype. Talan's underdark is the Darklands, and they are not Araphel's."* → lore now reads: *"Surface-dwelling: Drow on Talan are children of shadow. The underdark on Talan is the Darklands, the Corrupted God's territory; the Drow live above it."* Drop the "stereotype" framing.
- **[bestiary.html:389](talan/bestiary.html:389)** — Ardande/Talos callout: *"Both lineages live without a god-claimant"* and the negative cascade about Vesuna/Araphel/Forseti. → lore now reframes positively: *"Ardande carry the Feyworld's living-growth element… Talos carry the Shadowplane's eternal-structure element… planar lineages parallel to the bound thirteen, gathering by cultural gravity / trade."*
- **[bestiary.html:401](talan/bestiary.html:401)** — Mortal-mixes prose: *"These are genetic, not metaphysical — no divine, planar, or otherworldly lineage."* → lore now reads: *"mortal-ancestry mixes — genetic lineages, with their place in the world shaped by the mortal politics of the two parent ancestries."*
- **[bestiary.html:408](talan/bestiary.html:408)** — Dhampir row: *"Undead-touched, not god-touched."* → lore now drops the "not god-touched" comparative.
- **[bestiary.html:417](talan/bestiary.html:417)** — *"Four bound gods without exclusive heritages"* callout, full text: *"After the remaster reshuffle… no exclusive heritage. … never had one. … never had one."* → lore now retitled *"Bound gods whose touch passes outside bloodline"* with positive per-god framings (Iro=celestial Nephilim, Enki=mind, Jianna=ledger, Cronus=choice).

### magic.html

- **[magic.html:142](magic.html:142)** — *"airships are always Magitech — there are no non-magical airships"*. → lore now reads: *"Flight is a Magitech property: every airship integrates either Arcanotech rune-array lift or an Occultech-bound air elemental as its lift principle."*

### history.html

- **[history.html:116](talan/history.html:116)** (Week of Crimson Rain body) — *"More gods could have stayed, but virtually none were willing to be bound. The vast majority withdrew to the other planes."* → lore now reads: *"Thirteen accepted the binding and remained on the Material Plane; the rest withdrew to the other planes."*

### grand-gods.html

- **[grand-gods.html:102](grand-gods.html:102)** (Conclave Council note) — *"There is no fixed schedule."* → lore now reads: *"The Council gathers irregularly, on call, when something demands the full body in person."* Minor stylistic. The rest of the conclave note is well-framed (Cronus hosts, Frae City as the natural ground, Cronus is always already there).

### sortalde.html

- **[sortalde.html:212](off-continent/sortalde.html:212)** — *"Sortalde has no walking gods. The Thirteen Bound all maintain their sancta on Talan…"* → lore now reads: *"Sortalde's clerical life is veil-mediated throughout. Every grant runs through a Layer-3-resident pantheon… Religion on Sortalde is invocation, not personal audition — the gods stay on their side, the worshippers stay on theirs."* Same canon, more positive framing.

---

## § Medium — Lore canon not surfaced on the HTML side

### 6. Named Non-Bound Gods — Bikiargi and Epairima are absent from the site

`gods.md` defines four Named Non-Bound Gods (Layer 3 residents whose portfolios appear in Talanese clerical practice):

| God | Tier | HTML coverage |
|---|---|---|
| **Betibizi** (Undeath) | Minor God | Well covered: history.html (Storveldi Denbora secret), magic.html (integration-procedure GM Secret), lost-kingdom.html, bestiary.html (Skeleton entry). ✓ |
| **Zaharsuge** (Wyrmkin) | Minor God | Covered: dragons-reach.html, bestiary.html (Dragonet entry), lioaru.html (indirect). ✓ |
| **Bikiargi** (Moon, Twins) | Major God | **Not on any HTML page.** Worshipped by sailors, navigators, witches, lovers, the Iron Tide's astronomers, midwives. Currently invisible to site visitors. |
| **Epairima** (Judge of Souls) | Minor God | **Not on any HTML page.** Her court routes unclaimed souls at Dauria, invoked in mortal funerary rites. Currently invisible to site visitors. |

Recommended placement: either extend [grand-gods.html](grand-gods.html) with a *Named Non-Bound Gods* section (analogous to the *Council of Thirteen* conclave box at the bottom) covering all four with short blurbs and a pointer to fuller treatment; **or** add the Named Non-Bound Gods to [magic.html](magic.html) under the *Faith & the Gods* group, where the "13 & Beyond" info card already gestures at non-bound gods without naming them.

(The **Sun god / Solyra** is an active open thread — not yet ready for HTML placement. Skip until canon decides.)

### 7. Reflection's GM truth lives on history.html but doesn't reach bestiary.html

[bestiary.html:411](talan/bestiary.html:411) Reflection row has only the public-cover framing (*"Magical accident · Wellspring blip — no parent lineage… Reflections are made, sometimes intentionally, often not"*). The Stillpool / Wellspring-direct / conscious-pull / Lost-Era-leak GM truth lives on [history.html:151](talan/history.html:151) under the Lost Era card.

This is plausibly intentional design (the GM truth lives "one click deep" on history, the bestiary just lists the surface cover). The Azarketi entry on bestiary.html has a parallel ⚿ GM Secret expandable, and Reflection deserves one for parity. Worth a low-priority add: a brief *⚿ GM Secret — The Real Story* on the Reflection row pointing to history.html's Lost Era secret, with one paragraph summarising Stillpools and the conscious-pull mechanism for the Emperor's case.

---

## § Low — minor drift, optional

### 8. Per-god GM Secrets — 12 of 13 still empty on grand-gods.html

Only Cronus's `secret:` field is populated. The other twelve gods carry empty placeholders. This is already tracked in [open-threads.md → Per-god GM Secrets](open-threads.md). Surfacing it here just so the lore↔HTML pass mentions it: no Pass D fix is needed; the work is "write the secrets," which is canon-work, not propagation-work.

### 9. PF2e remaster history phrasing on bestiary.html

[bestiary.html:342](talan/bestiary.html:342) and L417 carry the *"PF2e Remaster reshuffled the versatile heritage roster"* / *"After the remaster reshuffle"* framings. Pass F (lore-side) consolidated these into `pf2e-notes.md` and stripped the meta-history phrasings from lore. The HTML can keep them (it's the player-facing surface, and the user explicitly noted PF2e is the game system in play). Listed here for visibility only — no action needed.

### 10. "Blightfather" / "Maw Below" in published prose

User's policy (set in Pass B/§5): *Maw Below*, *Blightfather*, and *Corrupted God* are **interchangeable in published prose**; lore reference favours *Corrupted God*. HTML usage of *Blightfather* on [the-binding.html:62, :167](talan/the-binding.html:62), the Sage Lorant quote on [history.html:209](talan/history.html:209), and similar surface-level prose is **policy-compliant**. No action.

---

## § Direction check — HTML canon missing from lore

Spot-checks across the major HTML pages and a sample of domain/sub-region pages did not surface meaningful HTML-only canon. The pattern is consistent: HTML pages elaborate lore canon with sensory and presentation detail (district names, dish names, sigil descriptions, callout copy) that is either also captured in lore or is presentation-layer texture. The lore is consistently the source of truth.

One area I did not exhaustively verify: **per-god clergy details, rites, and atmospheric notes on grand-gods.html** (e.g. Sarrum's dawn-vigil reading the dead's names in Lurrath, Shuun's clergy sitting wordlessly with anyone who asks). These read as natural elaborations of `gods.md` but a careful pass might surface specific rites in HTML that aren't in lore. If you want a deeper sweep on that direction, flag it as a separate task — the rest of the site appears clean.

---

## § Suggested order of work

1. **Pass H — fix-now (§1–5).** Five concrete edits across five HTML pages. Lowest-risk, highest-correctness gain.
2. **Pass I — negative-recast propagation (§6.* under Medium).** Mirror the Pass D positive framings from lore into bestiary.html, magic.html, history.html, grand-gods.html, sortalde.html. Prose-level edits, mechanical.
3. **Pass J — Named Non-Bound Gods placement (§7).** Decide whether Bikiargi and Epairima land on grand-gods.html (own section), magic.html (under Faith & the Gods), or somewhere else entirely. One-time canon decision + one new HTML section.
4. **Pass K — Reflection GM Secret on bestiary.html (§8).** Optional. One expandable to add.
5. **Skip:** per-god GM Secrets (canon-work tracked in open-threads), PF2e-meta on bestiary (intentional player surface), Blightfather/Maw Below (policy-compliant).

---

**Files that would be touched:**

- High: `index.html`, `talan/talan.html`, `talan/domains/brauogi/brauogi.html`, `talan/domains/ezkudon/ezkudon.html`, `talan/domains/zuzental/emerald-isles.html`, `talan/domains/askamira/askamira.html`, `talan/domains/lautara/lautara.html`
- Medium prose recasts: `talan/bestiary.html`, `magic.html`, `talan/history.html`, `grand-gods.html`, `off-continent/sortalde.html`
- New placement (named non-bound gods): `grand-gods.html` or `magic.html`
- Optional: `talan/bestiary.html` (Reflection GM toggle)
