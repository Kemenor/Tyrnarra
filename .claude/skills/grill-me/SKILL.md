---
name: grill-me
description: Interview the user relentlessly about a Tyrnarra lore draft, seed, or design until specificity is reached and same-iness has been eliminated. Walk down each branch of the lore design tree (geography → seed → sibling-contrast → politics → daily life → faith → ancestry → naming → chronicler-tier check), resolving dependencies one at a time. For each question, provide a recommended answer drawn from the canon and the seed so far. Ask one question at a time. If a question can be answered by reading a lore file (lore/geography/<region>.md, lore/glossary.md, lore/ancestries.md, lore/cosmology.md, lore/gods.md, lore/factions.md, lore/timeline.md, docs/open-threads.md) or an existing HTML page, read the file instead of asking. Use when the user says "grill me", "stress-test this", "what's thin about this", "this feels generic", "deepen this", "push on this", "audit my draft", or invokes /grill-me. Also useful mid-sub-region-workflow when a Phase 2 seed feels under-specified, a Phase 5 prose draft has generic patches, or a sub-region card reads as same-y compared to its siblings. Do not use during Phase 0 of any workflow (read the canon first; you cannot grill on top of canon you haven't read) or for procedural-only work (naming-only passes, HTML wiring, sidebar updates).
---

# Grill me

## What this skill is for

Interview the user relentlessly about a Tyrnarra lore draft or design until specificity is reached and same-iness has been eliminated. Walks down the lore design tree (geography → seed → sibling-contrast → politics → daily life → faith → ancestry → naming → chronicler-tier check) one branch at a time, applying the specificity test, the ancestry-is-not-culture rule, and the chronicler-vs-GM-tier discipline at every step.

Useful at any point inside `sub-region-workflow` where a section feels generic, and equally on factions, NPCs, named institutions, named events, religious orders, magical traditions, or any other lore element that has the bones of an idea but hasn't earned the specificity test yet.

## How to grill

- **Ask one question at a time.** Never two.
- **Provide a recommended answer with every question.** Drawn from the canon and the seed so far. The user can say "yes", "no, actually...", or "I hadn't thought about that". Recommendations make the grill faster, not slower.
- **If a question can be answered by reading a lore file, read the file instead of asking.** The lore files are the source of truth; the user is the source of *what isn't written yet*. Never grill the user on canon that's already on disk.
- **Walk the design tree in order.** Don't bounce around. Geography constrains economy constrains culture constrains politics constrains daily life. Resolve upstream before downstream.
- **After each answer, look for the next thing that isn't specific.** If everything currently surfaced passes the specificity test, name the next layer of depth and ask.
- **End when the user says enough, or when every question you'd ask is now answerable by the canon as it stands.**

## The grilling axes (the lore design tree)

Always proceed in this order. If a branch is already covered by canon, say so and move to the next.

1. **Geography and flow.** What does this place sit between? What flows through it (sea, rail, road, river)? What presses on it from outside (a neighboring domain, an off-continent power, the Cloud Sea)? What's the terrain doing to the people here?
2. **The seed.** What is the one image, contradiction, behavior, or collision that makes this place itself? Apply the **specificity test**: could this exist anywhere else in the setting? If yes, push harder. The Emarrea standard is the bar: foxfire → illusion → spectacle → drama → Heartcourt.
3. **The sibling contrast.** Name the closest sibling sub-region or comparable element. How is this place distinct? If a traveler walked from one to the other, what would change in the air, in the gestures, in the food, in how disputes resolve?
4. **Politics and power.** How do disputes actually resolve? Who is honored? Who is feared? Who is invisible? Where does authority come from: birth, demonstrated competence, the right to perform a specific ritual, the largest table, the best argument?
5. **Daily life.** What does a Tuesday morning look like for an ordinary person here? The sound, the smell, the gesture, the first thing they do when they wake. If the answer is "the same as anywhere else", the seed isn't load-bearing yet; go back to axis 2.
6. **Faith.** What does the chronicler see at a temple, a roadside shrine, a household altar? Separately: what's actually true that the chronicler doesn't know? Keep open-prose and GM-tier in two columns when grilling so the leak-risk is visible.
7. **Ancestry — only if relevant.** If an ancestry anchors here, what about **THIS place** changes how this ancestry lives? Don't accept the one-line lore as the answer. Push for what being from *here* adds on top of being of *this people*. The Itsasalda-vs-Atarialda Halfling contrast (the dock that never moves vs. the hearth that travels) is the model.
8. **Naming.** For every coined name: stratum (old-Basque/Icelandic-drift vs. modern-English-drift vs. regional register), literal meaning, drift step, collision check (*Compact* reserved for the Bound Thirteen; *Order* heavy traffic; *Republic* / *League* / *Council* / *Court* / *Hall* / *House* open).
9. **Founding era.** Default: Adventurer-Era or late-Dark-Era per the Kingdoms-Inherit-Names rule. If older, what is the story-reason for the older claim?
10. **The chronicler-tier check.** Read the surfaced prose back. Anything a chronicler couldn't earn by reading the chronicles goes inside a `⚿ GM Secret` expandable. Name what should move.

## Grilling principles

- **Specificity over completeness.** Better deep on three things than shallow on ten.
- **Recommend, don't interrogate.** Every question carries a recommended answer. Open-ended *"what do you think?"* questions are the failure mode; replace with *"I'd guess X because Y — does that land?"*.
- **Read the canon first.** If a question is answerable from `lore/geography/<region>.md`, `glossary.md`, `ancestries.md`, or another lore file, read the file and incorporate the answer rather than asking the user.
- **Apply the specificity test relentlessly.** *"Could this exist anywhere else in Tyrnarra?"* is the recurring test. If yes, the answer is generic; push harder.
- **Catch ancestry-as-label.** If the user (or the draft) says "Halflings live here", ask what about *this* place changes how Halflings live here. Same ancestry in two different sub-regions must produce two different cultures.
- **One axis at a time.** Don't ask about politics and faith in the same question. Resolve geography before economy; economy before culture; culture before politics; politics before daily life. Naming and the chronicler-tier check come last.
- **Concrete over abstract.** When the user gives an abstract answer ("a proud people", "deep tradition", "they value learning"), the follow-up asks for *one concrete sensory detail* that proves it. The smell, the gesture, the named object.
- **No em-dashes; affirmative prose.** Apply CLAUDE.md's prose rules to the grilling output, not just to committed lore. The grill itself models the voice.

## What a good grill looks like (a fragment)

> **Me:** Geography first. Itsasalda is the maritime gateway for half the continent — Brauogi grain, Myrkono wool, Floteyn timber, Order of Steam freight, Nashavel traders dodging Zuzental. That's the flow. My guess at the consequence: nothing stays. Everything is in motion. The people who run the docks don't get to know the people who use them, because by the time you'd learn their names they're on the next tide. Does that track, or is there a slower current under the throughput I'm missing?
>
> **User:** Tracks. And the slower current is the locals — the ones who *did* stay. They watch.
>
> **Me:** Good. That gets us to the seed. The mountain-Halflings on the dock stool, watching weather. Specificity test: could this be any port in Tyrnarra? I don't think so — Floteyn ports are timber-hauler towns, Vindul ports are Storm-rider towns, Bolverk has no comparable maritime layer. The Halflings-who-decided-to-stop is what makes it Itsasalda. Sibling contrast next: Atarialda Halflings carry the hearth with them; Itsasalda Halflings *are* the hearth. Same ancestry, opposite expression. Confirmed?

That's the rhythm. One axis. One recommendation. One question. Wait for the answer. Move to the next axis.

## When to use this skill

- The user invokes `/grill-me`, says "grill me", or asks to be stress-tested on a draft.
- **Mid-`sub-region-workflow`, inside a phase:**
  - **Phase 2 (Generate seeds):** grill the seed before locking it. The specificity test is the central grill move.
  - **Phase 3 (User picks + refines):** the clarifying questions phase *is* a grill, lightly held.
  - **Phase 5 (Surface the prose draft):** grill the draft before commit. Push every abstract phrase for a concrete one; every generic *"the people of X are proud"* for a specific behavior; every ancestry-as-label for what *this* place adds.
- Reviewing a faction, NPC, named event, religious order, or magical tradition that the user feels lukewarm about.
- Auditing an existing HTML page that reads as same-y compared to its siblings.
- After the user reads back their own draft and notices something feels thin but can't name what.

## When NOT to use it

- **During Phase 0 of any workflow.** Read the canon first; you cannot grill on top of canon you haven't read.
- **When the user is committed to a specific draft and wants polishing, not deepening.** Grilling assumes the design is in motion.
- **For purely procedural work** (naming-only passes, HTML wiring, sidebar updates, em-dash sweeps).

## Compatibility with sub-region-workflow

Grilling is a depth-tool *within* a `sub-region-workflow` phase. It does not replace the phase discipline:

- It does not skip phases.
- It does not bypass the surface-before-writing rule. A grill is chat, not commit.
- It does not bypass the canon-read. If grilling surfaces a question the canon already answers, the answer is in the canon, not the user.

When the grill is done, return to the workflow phase you were in. If the grill produced changes to a Phase 2 seed or a Phase 5 prose draft, re-surface the updated version before moving forward.
