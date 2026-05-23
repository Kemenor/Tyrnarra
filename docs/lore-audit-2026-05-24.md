# Lore audit — 2026-05-24

One-shot consistency sweep across the canon (lore + docs + published HTML). Five parallel passes: dates/numerics, names/etymologies, cosmology/gods/planes, geography/kingdoms/settlements, HTML/lore alignment.

**Result:** canon is in very good shape. Three concrete fixes warranted, one stale doc reference, one optional clarifying tweak. No GM-tier leakage, no broken links, no roster contradictions.

---

## Fix these

### 1. Yorimichi's retirement line conflates *age* with *year*
**Where:** [`lore/glossary.md:275`](../lore/glossary.md)

> "Former Crimson Heart through several late-Adventurer-Era crises; retired **at age circa 2522 MR**. Now a master Catjomin Sake brewer at Kawaakari … 7 tails, ~140."

She is ~140 now in 2532 MR and retired ~10 years ago per [`lore/cultures.md`](../lore/cultures.md) ("a decade back"), so she retired *in* 2522 MR, *at age* ~130. The wording reads as if 2522 MR were her age. Suggested rewrite:

> "retired in 2522 MR at age ~130"

### 2. Five stale Millhaven landmark references
Millhaven is canonically "removed during a restructure" and tracked as a re-introduction thread ([`docs/open-threads.md:201–204`](open-threads.md)). But five files still use it as a live landmark to anchor *other* sub-regions:

- [`lore/geography.md:26`](../lore/geography.md) — *"Millhaven is on its southern shore"* (Midarra)
- [`lore/geography.md:299`](../lore/geography.md) — *"west of Millhaven"* (Rika Tikur)
- [`lore/glossary.md:148`](../lore/glossary.md) — *"west of Millhaven"* (Rika Tikur etymology)
- [`lore/glossary.md:557`](../lore/glossary.md) — *"Millhaven is on its southern shore"* (Midarra)
- [`talan/domains/brauogi/brauogi.html:58`](../talan/domains/brauogi/brauogi.html) — *"west of Millhaven"* (Brauogi subregion card)

The HTML page actually publishes the orphan reference to readers. Two clean resolutions:

- **Re-introduce Millhaven** (close the open-threads thread) — then the references become valid again.
- **Reanchor** the five descriptions to a different Brauogi landmark for now, and let the Millhaven re-introduction land separately.

The brauogi.html mention is the one with publication exposure; the four lore-file mentions only affect future drafting.

### 3. Stale "Lioaru → The Hollow" pointer in open-threads
**Where:** [`docs/open-threads.md:143`](open-threads.md), in the *Hollow of Ten Thousand Threads — Operational details* gate.

> "[`lore/geography.md`](../lore/geography.md) — *Lioaru → The Hollow*"

The Hollow is consistently sited in **Myrkono → Shadow Steppes** everywhere else (lore, secret-history, glossary, site-inventory, both relevant HTML pages). This single doc pointer is the only "Lioaru" reference for the Hollow in the repo. Suggested fix: change the pointer to `Myrkono → Shadow Steppes → The Hollow`.

---

## Optional polish

### Primordial Six preamble vs nine-primordial roster
[`lore/gods.md:19`](../lore/gods.md) describes the Primordial Six as the six who shaped Prelife's *elemental* forces (darkness/void, air, fire, earth, water, light), while the detailed roster at [`gods.md:285–304`](../lore/gods.md) lists **nine** Layer-1/Layer-2 primordials including Positive/Negative Energy and the Wellspring-Soul (Iturima), plus the sibling-plane Wood/Metal pair (Zurzar, Burdinzar).

These are not in contradiction — the *Primordial Six* are six Grand Gods of the Bound Thirteen; the *nine primordials* are the elemental beings of the Prelife/Life sibling planes (distinct tier, distinct roster). But the wording at line 19 could mislead a reader into matching the Six to the elemental seven. A one-clause parenthetical clarifying that the Six are Grand Gods (not the same set as the elemental primordials) would close the seam.

---

## What was checked and came back clean

- **Era boundaries and date arithmetic** (timeline, current year 2532 MR, Crimson Rain hinge, Dark/Adventurer transitions) — consistent across all files.
- **Calune → Unaru rename** (2026-05-22) and **Inari → Hahane retirement** — zero stale references remain in lore or HTML.
- **Roster integrity** — 13 Bound Gods, 7 Vice Demons, 14 Virtue Devils (stubs intentional), 7 Wardstones / 9 Generals, 9 Heartcourt pillars (7 seated), 7 Layer-1 Primordials + Zurzar/Burdinzar.
- **Vice Demon backstories** match across `bolverk.md`, `non-bound-gods.html`, glossary, registrar.
- **Crimson Rain account** — Tani's killers correctly attributed to the Storveldi class everywhere; "Week" naming preserved as in-world compression; Cronus role consistent.
- **Compact compliance** — no Bound-god direct-action violations, no claim that the Thirteen can observe Wellspring-direct activity.
- **Domain ↔ god ↔ god-city** table consistent across geography.md, glossary.md, grand-gods.html, pf2e-registrar.html, talan.html, and every domain page.
- **Sortalde east / Red Empire west** of Hafra — consistent.
- **GM-tier sealing** — Storveldi-Denbora, Golden Empire, Elden, Thousand Kingdom, the-binding all properly seal their reveals inside `⚿ GM Secret` boxes; no leakage in open prose.
- **HTML structural** — every published page has a sidebar entry, every sidebar entry has a file, every spot-checked link resolves, Style A/B applied per CLAUDE.md, card conventions (` →` for clickable / `Tap ▾` for expandable) followed.
- **TBD markers** — the small number of inline TBDs in HTML are all accounted for in `open-threads.md`.

---

## Suggested order of attack

1. Decide Millhaven (re-introduce vs reanchor) — biggest blast radius, only one with HTML exposure.
2. One-line Yorimichi glossary fix.
3. One-line open-threads pointer fix.
4. (Optional) Primordial Six preamble parenthetical.
