---
name: sub-region-workflow
description: Use this skill whenever working on a Talanese sub-region (kingdom, free city, theocracy, mendicant order, guild-state, merchant republic, federated free-towns, march, clan-confederation, nomadic confederacy, anarchy, or any polity smaller than a continent) within the Tyrnarra worldbuilding project. Trigger on phrases like "flesh out [name]", "let's design [polity]", "new sub-region in [domain]", "what should [domain]'s [feature] be", "promote [name] to its own page", "build the page for [name]", "we have a label on the map but no canon for X", "let's do [region] next", working with TBD sub-region entries in docs/open-threads.md, drafting entries in lore/geography/<region>.md, or any session that takes a label-on-the-map to fully fleshed, published canon. Also use for a full pass on an already-built region, and when the user references the exemplars (Emarrea, the Lautara resketch, the Vindul three, Breidey, or the 2026-09 Zuzental and Sumendar builds). Do not use for cosmology or pantheon work, the thirteen god-cities (god-city-workflow), quest design (quest-workflow), NPC dossiers in established regions, or HTML edits to pages that already exist for unrelated reasons.
---

# Sub-region workflow

Takes a sub-region from a label on the map (or a thin existing entry) to full lore canon and a published page, in thirteen phases. Each phase has one topic, a fixed list of what must be done, and a fixed output.

## Ground rules

1. **A phase closes only when the user says it is good.** Discuss each phase until then; do not move on under a broad "go on" unless the user closes it.
2. **Every phase ends with a checklist readback**: list the phase's *What must be done* items and mark each done, answered-by-the-user, or deliberately left (with the user's say-so). A skipped item shows up here, not three regions later.
3. **Nothing is written to lore before Phase 11**, except an in-world document the user has co-written and accepted (Phase 3), committed and pushed on acceptance. Maintain the non-canon decision record in `docs/pencilled/<region>.md` throughout the build as described below; recording a proposal never approves it or makes it canon.
4. **All canon can change, deliberately and on the user's yes.** Dates, transport, a General's dungeon, an ancestry's home, an earmark: each is a **canon move**, named, approved, and listed with the files it touches (Phase 4). **Silent contradiction is the only thing forbidden.**
5. **Read before designing on canon** (Phase 0, point 7): if the user could point at a proposal and say "that contradicts `<file>`", `<file>` should have been read first.
6. **Surface before writing; lore before HTML.** Prose is reviewed as a draft file (Phase 10) before it becomes canon (Phase 11); HTML waits for an explicit publish signal (Phase 12).
7. **Candidate rounds are 1–3, scaled to importance, recommendation first** (seeds, images, governments, names, beliefs, secrets): three options for what carries the region, a single recommendation for side matters, alternatives on request.
8. **Plain answers are allowed.** A phase question may have an ordinary answer (the people feed themselves; the clothes are unremarkable). Answer for plausibility first, using every neighbour and not only the famous one; never invent a dependency or a drama to feed the tension.
9. **The project rules apply throughout:** `CLAUDE.md` (naming strata, affirmative prose, no em-dashes, *mortals* not *humans*, chronicler tier in open prose, the GM badges, commit discipline) and `docs/region-prose.md` (the region-entry contract; Breidey is the exemplar).

## Working record and revisions

After the Phase 0 readback is approved, create or update `docs/pencilled/<region>.md`, headed **Working record: not canon**. Preserve existing pencil material. Keep a concise record of the current phase and its approval status, approved decisions by phase, rejected options with the reason, unanswered or deliberately deferred questions, and approved canon moves with their affected files. Summarise rejected options; preserve full alternatives when the user asks. Keep private story uses in a separate, clearly labelled **Private story uses: never publish to `/setting/`** section. Link the draft file once it exists.

Update this record as decisions change and at each phase checkpoint, without requiring a separate request to take notes. Commit and push the record at approved phase boundaries with explicit paths, alongside any accepted document. Unreviewed draft prose waits for draft approval. On resuming, read the record and relevant current canon first; a pending proposal or an existing draft is never evidence of approval.

**Approved decisions can be reopened.** Later government, economy, or history work may change the seed or traveller's image. Identify the affected decisions and dependent prose, explain the proposed change, and ask the user to approve that change. Mark those items reopened in the record, preserving the earlier decision until its replacement is approved. Recheck the affected phase items and canon moves; keep unrelated approvals and continue from the appropriate phase instead of restarting the whole build. An already committed document changes only through an explicitly approved revision, respecting GM-Written rules. Nothing dependent on an unresolved revision proceeds to canon or publication.

## The phases at a glance

| # | Phase | Output |
|---|---|---|
| 0 | Canon read | A readback: stub or rework, constraints, map facts, siblings, conflicts, ancestry fixes, badges |
| 1 | Seed questions | A summary of the user's answers |
| 2 | Seeds | The chosen seed, recorded with the options considered |
| 3 | Traveller's image | The image, its speaker, year, form, and placement |
| 4 | Place, peoples and history | A settled-facts list, dates and canon moves included |
| 5 | Government | The chosen government, with the three test results |
| 6 | Economy | The settled economy |
| 7 | Daily life | The settled daily life |
| 8 | Naming | A name table with etymologies |
| 9 | Tension and reveal | The tension, the belief, the secret(s), the section weights |
| 10 | Draft | The approved draft file and derivations list |
| 11 | Commit lore | A lore commit and summary |
| 12 | Publish | A publish commit and summary |

---

## Phase 0: Canon read

**Topic:** know everything the canon already says about this place and its surroundings before proposing anything.

**What must be done:**
1. **The domain file** (`lore/geography/<domain>.md`), end to end: borders, seas, terrain, peoples, god-city, every sub-region entry.
2. **Every bordering domain's file**, end to end, for the neighbours this region touches.
3. **The region's own traces:** a project-wide search for the name (lore, docs, published), plus the git history of any dropped stub (what it said before the drop).
4. **The map:** the region's shape, size, and neighbours (`wdmap geography` or `tools/wonderdraft/map-snapshot.json`), the icons inside it (capital, temple, towns), and the terrain in export crops of `published/setting/assets/maps/`. Record the area in square miles (one full-resolution pixel is a quarter of a square mile). The map shows **landmarks, not land cover** (`_continent.md`, *Scale*).
5. **Sibling regions:** their full entries, noting which are **built** and which are **stubs**. A stub is a placeholder, not canon to design around.
6. **Anchor ancestries:** the full entry of every ancestry anchored in the domain, checked for **feeling-only**; any vocation, culture, or settlement history baked into an entry is flagged for moving into a place (Appendix A).
7. **Canon the design will touch:** any event, faction, or cosmology the region might involve (a General of the Nine, a god, the Gods' Law, the timeline) has its file read end to end *before* proposing.
8. **Tracking docs:** the region's entries in `docs/open-threads.md`, `docs/deepening-ideas.md`, `docs/map-todo.md`, and `docs/pencilled/`.
9. **Pages to be touched:** checked for GM-Vetted or GM-Written badges.

**Output:** a readback in chat before any writes: stub or rework (and what a dropped stub said); fixed constraints; map facts (area, neighbours, icons, terrain); the sibling census (built versus stub, existing images and institutions); canon conflicts and stale lines; ancestry entries needing a feeling-only fix; GM badges on pages this build touches. After approval, initialise the working record.

**Closes when:** the user has seen the readback and says it is good.

---

## Phase 1: Seed questions

**Topic:** draw out what only the user knows about this place, the texture the canon does not hold yet, before any seed is proposed.

**What must be done:**
1. **Ask 3–5 questions**, only about what the Phase 0 readback left open; never ask what the canon already answers. Choose from:
   - **Flow:** what does it sit between, what passes through it, what presses on it from outside?
   - **Contradiction:** an unlikely combination at its heart, a value held against its setting?
   - **The sibling question:** how must it differ from its closest built sibling; what would change for a traveller crossing from one to the other?
   - **The domain's aspect:** how does the god's portfolio show here, without becoming the region's literal climate?
   - **The ancestry question:** only if a people anchors here, and only as a follow-up: what does being from *here* add to being of this people?
2. **Offer a prompt with each question**, clearly marked as a prompt, so the user has something to push against.
3. **Welcome the user's own ideas.** A seed idea the user brings (the Namur dictatorship came this way) is an answer, tested in Phase 2 alongside the others.
4. **Leave to later phases:** the traveller's image (3), government (5), economy (6), daily life (7). Asked now, they produce guesses.

**Output:** a 4–6 sentence summary in chat of what the answers say about the place: the flow, the pressure, the contradiction, the user's ideas. The user corrects it before any seed is made. **The summary is written even when the user's own idea answers the questions**: it fixes the neighbours and sibling contrasts as context, which otherwise drop out (the Namur dry run).

**Closes when:** the user confirms the summary.

---

## Phase 2: Seeds

**Topic:** find what makes this place specific to its setting; government, economy, and people grow from it. Its identity comes from the combination and local consequences, and may include shared customs, borrowed institutions, and ordinary features.

**What must be done:**
1. **Generate 2–3 seeds.** A seed is an **image**, a **contradiction**, a **behaviour**, or a **collision of forces**; never a political archetype with an ancestry slotted in, a demographic label, or an adjective for the domain. **A seed may be political when the politics is the contradiction** (Namur: a free people sworn to obey one). **When the user brings the idea, the seeds may be its shapes**: variants of the user's idea laid side by side, then combined with the other open axes if needed (the Namur grid).
2. **Per seed:**
   - **The pitch**, 2–3 sentences, leading with the image or contradiction. No politics in the pitch unless the politics is the contradiction.
   - **What follows:** the political direction, the peoples' part, the signature institution, and one concrete sensory detail that grow from the seed. The government is a first sketch only (Phase 5 settles it).
   - **The cross-canon hook:** what it rhymes with in locked canon.
   - **The specificity test** in one line: could this place exist anywhere else in the setting; what would have to change to move it? If "only the name", the seed fails and is rewritten.
3. **Sameness check against the setting.** Hold each seed against the built regions *across the whole setting*, not only the domain's siblings. Rework a seed whose identity merely duplicates another place. Shared customs, related images, and borrowed institutions are welcome where they fit; explain their local meaning and check any claimed historical connection against canon. Overlaps often surface only here, and often from the user, who knows the setting best; that is expected, not a failure of Phase 0. The check is authoring: its comparisons go in the working record, never onto the page (see Phase 5).
4. **The user's own ideas** from Phase 1 are tested the same way, alongside.
5. **Recommend one.** The user picks, combines, inverts, or asks for the combinations laid side by side (the Namur grid: two shapes against three Generals).
6. **Record the choice.** Update the working record with the chosen seed and a short account of the alternatives and why they were rejected or combined. Keep full alternative pitches if the user requests them.

**Output:** the chosen seed **as one sentence** (it becomes the page's flavour line: *a republic that keeps its word, including the one that made it a dictatorship*); the updated working record.

**Closes when:** the user has picked the seed and says it is good.

---

## Phase 3: Traveller's image

**Topic:** the one thing a visitor would carry home: the seed seen from the road, from outside.

**What must be done:**
1. **Offer 2–3 candidates**, each a single concrete thing: a sound, a gesture, a view, a public act (the knot-cutting on the Drukha quay; the line of fires seen from the Eldara train; the sword laid on the slab). Ground each in the seed and in canon already fixed.
2. **Compare names and images with built places**, including **kin rites** in other regions (Namur's Oath-Day beside Lograth's Re-Swearing). Shared rites and imagery may connect places; check whether the scene conveys this region's circumstances rather than merely copying another scene. Avoid confusing names, and do not invent a unique rite just to fill this slot. Reopen the image if later phases change what a traveller would see.
3. **Recommend one.**
4. **Settle the speaker:** who sees it, from a register whose naming rules exist (so the name follows them); why they are there; the year; the form (a single quote, a letter, a journal entry).
5. **Give the speaker personality.** Settle one or two traits with the user (a passion, a habit, an impulse, a way of seeing) and let them show in the text itself, not only in the attribution. Joana Fontebaixa, the Leitor in the Tahu Tangata letter, has a passion for fire: she cannot pass one, gets off the train on impulse, and folds a pinch of the field's ash into her apology to her master.
6. **Settle where it lands:** the top of the section it belongs to. If it grows into a longer document, it becomes its own in-world file (`lore/geography/<domain>/<region>-<form>.md`, with a voice block), published whole as a log card, excerpts quoted at section heads.
7. **Write it together if the user wants.** The user may draft and ask for corrections (Renier's journal was written this way): corrections keep the user's words and mark every addition. A co-written document is committed and pushed as soon as the user accepts it, with placeholders marked for the naming pass.

**Output:** the chosen image, its speaker and year, its form, its placement; if co-written, the accepted in-world file committed.

**Closes when:** the user says it is good.

---

## Phase 4: Place, peoples and history

**Topic:** fix where things are, who lives there, how many, and what happened when, so everything after builds on settled facts.

**What must be done:**
1. **Site the key features on the map:** the capital, the signature place (monastery, gate, lair, hall), anything the seed needs. Features the map draws are fixed; features added below its resolution are free, and each one that would show at map scale is noted for map-todo.
2. **Neighbours:** one line per bordering region on the relationship (trade, friction, treaty, war, indifference). "Light for now" is a valid answer, recorded as such.
3. **Peoples, by the ancestry-distribution model** (Appendix A): is one ancestry the anchor here at full expression; which others live here and in what proportion; or is it unsorted, defined by an institution or faith? Feeling-only fixes from Phase 0 are settled here (which region the stripped vocation moves to).
4. **Founding era,** by the naming strata (`_continent.md`, *Naming strata across the eras*): when the place and its polity were named. Default a Dark-Era or Adventurer-Era founding (*Kingdoms inherit names*); an older founding is a deliberate story choice.
5. **Dated history:** a short timeline of the events the region needs, each checked against `lore/timeline.md` and the canon read in Phase 0 (era boundaries; the Nine Dungeons erupted 2524 MR and did not exist before; the present is 2532 MR). No date goes forward without the check.
6. **Population, by the density rule** (`_continent.md`, *Population density*): area times tier (held heartland 20–40 per square mile, wild country 2–10); the capital holds 1–3% of the country.
7. **Canon moves:** every change to built or earmarked canon the design needs (moving a General, ending a domain's dungeon-free status, a new transport link, retiring an old stub's idea). Each needs the user's explicit yes, with its files listed.

**Output:** a settled-facts list in chat: sites; neighbour lines; peoples and proportions; founding era; dated history; population and capital size; canon moves approved, with files.

**Closes when:** the user says it is good.

---

## Phase 5: Government

**Topic:** who actually rules, why they are fit to, why the ruled accept it, and what it costs. The government grows *from* the seed's world and *contains* the seed; it is never the seed generalized into rule (Appendix E, *Making the government be the seed*).

**What must be done:**
1. **Census first:** hold each candidate against the forms already on Talan (Appendix B) and name its nearest existing polity. Talan is heavy on councils and assemblies; a new one says what sets it apart. **The census and sameness notes stay off the page** (GM ruling, 2026-10-02): record them in the working record; the region's prose describes its own government and never argues why it differs from another region's (the Tahu Tangata draft's paragraph setting its diarchy against Tvisol, the Cape, Izarelai and Haldmark was cut).
2. **Offer 2–3 government seeds**, each with:
   - **Who rules, concretely**, answering the four questions a foreigner needs: who rules day to day, who receives an envoy, who signs the treaty, who decides to build the bridge. If the polity has a **special state** (an emergency office, a regency, an interregnum), answer the four questions **twice**: in ordinary times and in the special state, including how power is divided between them.
   - **Why they are fit to rule:** actual statecraft (planning, logistics, law, diplomacy) where this society already practises it. Craft-prestige is not competence.
   - **Why the ruled accept it:** the founding story, and the standing reason an ordinary person tolerates it today.
   - **The honest cost,** named plainly: a plutocracy is called a plutocracy.
3. **The incentive check:** re-derive who actually wins any standing metric (seniority that reduces to age, stake that reduces to the biggest purse, a rule that rewards inventing guilt, like the Order of Law's "cosmetic knot"). Rework any seed the check breaks.
4. **The three tests** on the recommended seed: **unity** (why does it not fracture?), **external agency** (how does it make a deal with a neighbour?), **internal provision** (how does it decide to build?). "No ruler" passes only by naming the non-governmental force that binds the place and the standing custom a foreigner deals with (No Man's Land: the kindling and the line captain).
5. **Settle the powers:** what the rulers may do, what they may not, and where the lines are deliberately muddy (Namur: the Dictator may sign anything the oath requires, and what it requires is argued). A muddy line is often the live tension.
6. **When the seed is itself a government** (Namur), offer variants of its mechanics rather than whole new governments, and settle how its offices are filled (who may be chosen, and why they are fit).
7. **Recommend one.** The user picks, combines, or inverts.

**Output:** the chosen government in chat: offices, who fills them and how, the four answers, the three test results, the powers and their muddy edges, the honest cost.

**Closes when:** the user says it is good.

---

## Phase 6: Economy

**Topic:** how the people eat, what the place sells, what brings outsiders if any, and how it all moves.

**What must be done:**
1. **Subsistence:** what feeds the people (farming, herding, fishing, forage), and whether they feed themselves or depend on imports (Eldara cannot, and that shaped No Man's Land). Answer for plausibility: a country rarely depends on its enemy for bread, and lean years draw on every neighbour. "They feed themselves" is a complete answer.
2. **The draw:** why outsiders come, if they do: a good, a service, a skill, a rite, a pilgrimage, ordinary trade, family ties, or a convenient route. It need not be exclusive to this place. "Few outsiders come" is a valid answer; explain its access and local role without inventing an attraction.
3. **What it sells and buys, and with whom:** named partners among the neighbours and on the wider network. Check the partners' own canon agrees, or note what it needs updating (the Thousand Kingdom buying Namur's ore).
4. **Routes and transport:** whether it is on the rail (checked against `lore/transport.md` and the network's lines), its ports and sea routes, its roads and river traffic, and any single choke point. **Changing transport canon is a canon move like any other** (a new line, a closed route, a new crossing): name the change, get the user's yes, list the files it touches. What is never allowed is contradicting it *silently*.
5. **How the economy feeds the tension:** the stake each side of the live tension has in it (Namur's closed mines against the reformers).
6. **Table note, optional:** if a material or good maps to a PF2e item, check it in `tools/encounterBuilder/items.db` (`loot.py search`; rebuild with `rebuild.py` if absent), and against a second source (Archives of Nethys) if the database lacks it. The Foundry packs are not complete (warpglass is missing from them).

**Output:** the settled economy in chat: subsistence, the draw, partners and goods, routes and transport, its stake in the tension, any table note. (Who gets rich matters only where the seed or the tension makes it matter, and then those phases carry it.)

**Closes when:** the user says it is good.

---

## Phase 7: Daily life

**Topic:** what it is like to live here on an ordinary day: the texture a reader remembers and a player walks into.

**What must be done:**
1. **The ordinary day and the shared ritual:** how an ordinary person's day runs, and the civic ritual everyone shares, if there is one (the Oath-Day count, the dawn page, the Apprentice's Fire).
2. **The senses and habits, as a few telling examples:** what is special here or tellingly ordinary among food, drink, dress, song, smell, the market, and the regional vice (Namur: the sworn-name tag at every throat, betting on the Oath-Day count, the spirit drunk only when a word is given). No full inventory, and **no blanket claims across classes** (rich and poor, town and country). Include **how people talk** where telling (Namur's "perhaps"); ordinary speech and habits shared with neighbours are valid answers.
3. **Movement:** how an ordinary person gets around, and any **signature movement** the region already warrants (the page-riders, the Bread Road convoy, the ferry every tide). Ordinary walking, riding, or carts may be the whole answer. This is the daily side of Phase 6's routes.
4. **Visitor against native:** what an outsider sees or misreads, and what a local knows; usually a gap in custom or knowledge.
5. **Youth:** the **coming-of-age** act; the **sanctioned transgression** (what the young get away with, and who keeps it in check); and whether it is a **slope or a switch** (growing up is rarely a flip; the Namur fool's oath).
6. **Faith as lived:** how the domain's god, or the region's own faith, shows in an ordinary day; clergy presence; devout, indifferent, syncretic, or hostile.

**Output:** the settled daily life in chat: day and ritual, senses and speech, movement (including any signature movement), visitor against native, youth, faith as lived.

**Closes when:** the user says it is good.

---

## Phase 8: Naming

**Topic:** what everything is called, why, and in which stratum. A name tells a reader when a thing was named and by whom.

**What must be done:**
1. **The region's register:** first read `lore/geography/_continent.md`, *The families of Talan* and *The regional registers*, including any pending re-render. Choose the **word-base** inside the family assigned by physical location and history, following culture rather than ancestry or god-domain. Word-bases may be shared; use local sound rules and plain letters speakable at a German- and English-speaking table. The **personal-name structure** remains unique to the region, grown from its culture (Legea's day-name, the Order's self-chosen name, Namur's sworn name; never another region's shape). Old examples illustrate structures, not permission to reuse a superseded word-base. A god-city gets its own naming scheme over its host region's tongue. If the family is unassigned, surface that gap and settle it with the user before choosing a base.
2. **The local tongue:** define it (name, who speaks it, how it sits beside Talanese and its family), or record any still-open details as pending. Pending details do not waive the assigned family or permit unchecked names.
3. **Stratum per name, by era and namer:** read `_continent.md`, *Naming strata across the eras*. Icelandic renders the **Silent Tongue**; Basque renders the **Court Tongue**. They have distinct histories and are never interchangeable choices for an "old" name. Follow that section for regional and Talanese strata too; an Adventurer-Era name is not automatically Talanese. Appendix C summarises the checks.
4. **Candidates scaled to importance**, each with **source language, literal meaning, and drift step**: up to **three** for what a reader carries (the region if unnamed, the capital, the signature institution, the name structure); a **single recommendation** for side names (offices, rites, the demonym, figures), alternatives on request.
5. **Check the real-language words.** Any word not known with certainty is checked before it is offered, or marked unverified.
6. **The collision check** before offering: search lore, docs, and published for every candidate. Flag confusing proper-name collisions and explain deliberate echoes. Generic titles and shared rites may recur where they fit; Appendix C lists existing uses to compare, not exclusive ownership. Personal-name structures remain unique.
7. **Named figures:** everyone the draft will name or quote, in the register's structure, with a one-line role.

**Output:** a name table in chat: register and structure; the local tongue or "pending"; every slot with its pick and etymology; named figures; collisions found and resolved.

**Closes when:** the user has picked every slot and says it is good.

---

## Phase 9: Tension and reveal

**Topic:** what presses on the place now, what the folk say, what is really true, and which topics carry the page's weight.

**What must be done:**
1. **Pin the live tension:** the pressure or change the place is living through, stated as fact, left open, won by nobody; a campaign seed, never a hook. Name each side and what it has at stake. A muddy line from Phase 5 or a stake from Phase 6 is often it.
2. **◈ Popular Belief:** 1–3 candidates for what the folk say (tavern-tales, sayings, superstitions, including the parts that are wrong); one may quietly hedge toward the secret. Recommend one.
3. **⚿ GM Secret:** 1–3 candidates, each naming the **chronicle surface** (what open prose can hint at) and the **hidden truth**, and passing the **weight test**: what in the world reads differently once the truth is known (which open-prose facts, places, peoples, or institutions it explains or changes). If nothing reads differently, the candidate is weak and is replaced. **Write no story set-ups or hooks for a secret** (GM ruling, 2026-10-02): the setting carries world truth, never adventure material. **Check every route, port, owner, and trade a secret leans on against canon and the map** before offering it (the Tahu Tangata paymaster failed this: Eldara's sea-borne food was claimed as Rika Tikur's, but the Throat opens onto the open Midarra and canon names no carrier). The ⚿ box carries the hidden world truth; campaign prompts never go into `/setting/`, even inside a GM box. If the user requests campaign material, develop it separately in the appropriate campaign layer under `docs/campaign-layer.md`. Check each secret against existing secrets and cosmology for coherence. Valid non-answers: **none yet**, **placed but draft**, **none at this level**. A page may carry several secrets, each placed after the section it answers.
4. **Section mass:** the user decides which topics carry the weight, or hands the call to me; either way the weighting is written down before drafting.

**Output:** in chat, the live tension (sides and stakes), the chosen belief, the chosen secret(s) with surface, truth, and what each changes in the world, and the section weights.

**Closes when:** the user says it is good.

---

## Phase 10: Draft

**Topic:** turn every settled phase into the region's lore, drafted in full and reviewed before anything is written to canon.

**What must be done:**
1. **Write the whole draft as one persistent file**, `docs/pencilled/<region>-draft.md`, headed **Draft: not canon** and linked from the working record, in lettered targets:
   - **(A) the deep file** `lore/geography/<domain>/<region>.md`: the facts header (etymology, position, terrain, character, peoples, tongue, faith, rule, founded); sections in the Phase 9 weights; the traveller's image at the top of its section; voices quoted at section heads; ◈ and ⚿ after the sections they answer; *What a … is called*; named figures, the Voices list, *Still open*; any in-world document published whole at the end.
   - **(B) the domain-file summary** replacing the stub.
   - **(C) the glossary block and the register row** (`_continent.md`, the regional-registers table).
   - **(D) every other file the approved canon moves touch.**
   - **(E) docs:** open-threads, deepening-ideas, map-todo, the working record. Keep these authoring targets separate from the publishable prose in (A)–(D).
2. **Nothing new sneaks in.** The draft uses only what Phases 0–9 settled; anything added (a number, a date, a custom, a quote) goes on a **derivations list**.
3. **The prose contract** (`docs/region-prose.md` plus the global rules): eye-level narration, wit only in attributed quotes, affirmative prose, no em-dashes, *mortals* not *humans*, no name-glossing in narration, nothing from the banned list.
4. **Five checks before sending:**
   - **Ending check:** the last sentence of every paragraph and section is a fact or a hook, never an epigram (a short line that resolves the meaning, a paired antithesis, a significance line, a *never*-closer).
   - **Leak check:** open prose holds nothing only a ⚿ box may say; no private story uses or campaign prompts appear in setting prose, including its ⚿ boxes.
   - **Consistency check:** numbers, dates, and names agree across the draft, the in-world documents, and existing canon.
   - **Arithmetic check:** every count, threshold, and population adds up (the capital within 1–3% of the country).
   - **Reverse check:** compare the draft with the working record's current approved decisions from Phases 0–9. Confirm each publishable fact landed; account separately for private story uses, rejected options, and deliberately deferred items. Resolve every reopened decision affecting the draft before approval. Settled answers dropped in drafting are the commonest miss (Namur lost a visitor-against-native line and its rail this way).
5. **Send the file**, with a chat summary: the structure, the derivations list, what each check caught and fixed.
6. **Revise until approved:** each round of notes is applied and summarised, the checks re-run on anything changed.

**Output:** the approved draft file and a derivations list the user has accepted.

**Closes when:** the user says "commit" or its equivalent.

---

## Phase 11: Commit lore

**Topic:** write the approved draft into canon exactly as approved, plus everything it touches, and nothing else.

**What must be done:**
1. **Apply every target** from the approved draft, verbatim: the deep file; the domain summary replacing the stub; glossary fixes and the new block; the register row; `lore/ancestries.md` if a people was anchored or trimmed; every file an approved canon move touches (factions, other domains, timeline, transport); in-world documents with placeholders filled.
2. **Update the tracking docs:** `open-threads.md` (the census line struck and marked built; every thread the build closed or changed: naming, the Nine, earmarks; any new open question); `deepening-ideas.md` (follow-ups); `map-todo.md` (labels for new names and features at map scale, the "no capital yet" list); `docs/pencilled/<region>.md` (status line).
3. **Repair references:** search for links to anything moved or renamed (an old section anchor, an old stub's wording, a retired earmark) and repoint them.
4. **Verify pass:** no em-dashes in touched files; lore-side GM content sits under `⚿ GM Secret:` headings or inline ⚿ markers; every file the draft listed was changed; `git diff --stat` matches the target list.
5. **Commit:** `git status`, then stage **explicit paths only** (never `-A`, `.`, or `-a`); leave anything this session did not touch unstaged; commit with a message naming what landed and the canon moves; push.
6. **Stop.** No HTML until the user gives a publish signal.

**Output:** the commit hash and a summary of what landed where: every file, every canon move, anything the verify pass caught.

**Closes when:** the push has landed and the user has seen the summary.

---

## Phase 12: Publish

**Topic:** mirror the committed lore onto the site, and wire it in everywhere it belongs.

**What must be done:**
1. **Build the page** at `published/setting/talan/domains/<domain>/<slug>/<slug>.html`, Style B, on the current template (the 2026-09 Zuzental and Sumendar pages): an accent checked with `node tools/contrast.mjs` (at least 4.5:1 if used for text, 3:1 if graphics only); At a Glance and the capital callout (clickable if the target has a page); **the prose mirrored from the lore file, generated from it where possible** so the page cannot drift; voice quotes; ◈ and ⚿ as expandables (`site-interactions.js` loaded) placed as in the lore; in-world documents published whole as **log cards** (`.log-letters`); named figures, Continue Reading, Open in the Chronicle Record; the card conventions (`docs/card-conventions.md`).
2. **Wire it in:** `published/setting/assets/site-nav.js`; the domain page's card made clickable with ` →`; the interactive map's region link (`published/setting/assets/maps/map-data.json`; auto-matched on the next export); `docs/site-inventory.md`.
3. **Mirror everywhere:** search `published/` for the region's name and for everything the canon moves touched (a moved General's card on the Binding, a neighbour's text, the ancestries page, the registrar), and bring each mention in line with the lore.
4. **GM badges:** check every page touched. A real prose or canon change to a GM-Vetted page strips the badge; a GM-Written page gets only the change the user asked for; chrome-only changes keep the badge.
5. **Verify in the browser:** markup well-formed on every touched page; every section renders and the sidebar marks the page current; every expandable opens and reports `aria-expanded="true"`; no console errors; no sideways scrolling at desktop and phone width, measured as `document.documentElement.scrollWidth` against `clientWidth` (not the window width, which includes the scrollbar).
6. **Commit:** explicit paths; a message naming the page and every mirror; push.
7. **Several pages at once:** a single page is built directly; fan out one agent per page only when two or more are built together (Appendix F).

**Publication boundary:** mirror approved world prose and hidden truths only. Exclude working records, draft annotations, private story uses, and campaign prompts, including any such notes encountered in older lore files. If separating them requires rewriting approved prose, return that revision to lore review first. Publishing grants no authority to invent a name, fact, quote, belief, or secret. Report proposed additions to the user; review affected decisions and draft targets through Phases 10–11, commit the approved lore, then mirror it. Layout and accessibility choices may proceed within the existing conventions.

**Output:** the publish commit hash and a summary: the page, its wiring, every mirror, badge decisions, the browser check results.

**Closes when:** the push has landed and the user has seen the summary.

---

## Appendix A: The ancestry-distribution model

Do not assign one ancestry per sub-region, and do not invent a meta-rule that "decouples" peoples from places. The model the exemplars use:

- **Each anchor ancestry has one sub-region of full expression** (Kitsune in Emarrea, Halflings in Atarialda, Vishkanya in Itsasalda, Humans in Legea, Hobgoblins in Namur, Goblins in Haraour Eliza, Kobolds in Burdineyja). That home is where the feeling runs at full strength.
- **The same ancestry also lives across the other sub-regions, a different life in each** (Lautara's Kitsune are also Merkavar brokers, Itsasalda bar-owners, Cape record-keepers). A home is not a confinement.
- **Some sub-regions are not sorted by a people at all**, but defined by an institution or a faith (Rika Tikur's Company, the Cape's theocracy, the Order of Law, No Man's Land).
- **The god-city belongs to all the domain's anchors at once.**

**Ancestries are a feeling, not a job.** An entry in `lore/ancestries.md` says what a people *is* (the temperament); a vocation, culture, or settlement history baked into it is stale lore that belongs to a place. Before building on an anchor, check its entry is feeling-only; strip the vocation into the region that carries it (the Kobold's prototypes and the Goblin's brewing moved into Burdineyja and Haraour Eliza). The two failure modes: concluding "people X must get territory Y" from thin canon, or over-correcting into a domain-level theory the exemplars contradict. When a tension surfaces, check how an exemplar resolves it before inventing a rule.

## Appendix B: Government forms already on Talan (the Phase 5 census)

Keep this current as regions are built.

- **Monarchies and houses:** the Thousand Kingdom (crown and sworn houses); the Emerald Isles; Harro Distiratsua (crown and Lamphold houses); Fellibylur (chartered merchant kingdom, parallel seats).
- **Theocracies and clergy rule:** Legea (hereditary demigod theocracy, the readers of the book); the Dreaming Cape (Twin Lantern); Hirubaso (Elkaride hierocracy); the Order of Law (found Trimpon, forest chapter, Desi and Seneschals).
- **Councils and assemblies (many):** the Vordsbench (Itsasalda), the hearth-council (Atarialda), the Open Floor (Azkataria), the Hightable, Baerfrost's chieftains, the Wyndwalken chapter, Fenurra's War Council, the Skarvorn, Myrria's Council of Adventurers; the Namur Senate (senators elected on self-written oaths) with its sworn Dictator.
- **Money and property:** Rika Tikur (the Company, a plutocracy); Baratalda (Housen plutocracy, the Sealhouse); the Vernua Maors (oligarchy of the chain over voluntary comhar).
- **Chance and rotation:** Frae City (offices by lot and rotation); Nahaskel (the coin at the Casting); Balatur Erui (the ear-stone lot); Tvisol (rule by the young in paired reigns).
- **Three estates in one hall:** Lograth (Throne, Lawspeakers, Stewardry).
- **Without a ruler:** Villtur (clans, no unity); the Basogur (no centre, the Roadwards keep the road); No Man's Land (cinders, kindlings, task-captains, the Apprentice's Fire); Crossroads (functionally independent).
- **Older archetype list** (for recognising shapes): clan-confederation; hereditary monarchy or jarldom; merchant republic; theocracy; march or border-state; mendicant order; mercantile guild-state; federated free-towns; rotating meritocracy; nomadic confederacy; two-tier hybrid; hearth-council; court-of-spectacle.

## Appendix C: Naming strata, drift, and collisions

**Read the current tables first:** `lore/geography/_continent.md`, *The families of Talan*, *Naming strata across the eras*, and *The regional registers* are authoritative. Family assignments follow geography and history; choose a word-base within the assigned family, observing stated exceptions and pending re-renders. Do not copy an older example's base over a current assignment.

**The two deep tongues are distinct.** The **Silent Tongue** (Icelandic with drift) belongs to names given in the Elden Era and the first stretch of the Gods' Era. A later use needs an established reason: Elden ground named then and settled later, or a learned coinage with a real scholarly reason. The **Court Tongue** (Basque with drift) belongs to the gods' rule, the hinge of 1 MR and early Lost Era, and holy or liturgical words; its surviving speech communities are specified in the canon. Being old or naming land alone does not choose between them.

**Later strata:** regional registers emerge in the late Lost Era and return from the Dark Era onward; Talanese (English with drift) dominates Golden-Era naming and is spreading again in the Adventurer Era. Check the full era table and who gave the name. A name's stratum follows when it was given, not the polity's present age or the current date.

**Talanese drift mechanisms:** vowel shift (i → y, ai → ae, ou → ow); consonant erosion (-ed → -t, -ing → -en); compound contraction; archaic suffixes (-en, -worn); loss of silent letters.

**Existing uses to check** (examples, not an exhaustive list or a ban on reuse; search current files before offering). Avoid confusing proper names; allow shared generic titles, customs, and imagery where their local use is clear:
- *Compact* (the Compact of the Bound Thirteen); *Order* (heavy traffic: Order of Steam, Voroir Daua, Order of Law).
- Titles and offices: *Speaker* (Fenurra's Speaker's Mantle); *Stewardry* (Lograth); *Reeve* (Azkataria, Lua Lasai, Tvisol); *Provost* (Thekkavar); *the Standing* (Edgeward).
- Rites and customs: *the Re-Swearing* (Lograth); *the Turning* (Haizava); *the Handing* (Villtur); *Muster* (Haldmark, Villtur).
- Images: *two chairs* (Nahaskel's Casting chamber); *tally-tokens* and *weighing* (Balaena); *the Crossing* (the Basogur log).

**Always record etymology in `lore/glossary.md`** at commit time: source language, literal meaning, drift step.

## Appendix D: Hard rules

- **Ancestry-as-label is not culture.** Give a people's life here local context. Shared occupations, customs, and institutions are plausible; merely copying a whole culture under a new place-name fails.
- **The specificity test.** Every seed and every committed region passes as a whole: what would have to change to move this place elsewhere in the setting? Ordinary features and shared traditions need no exclusive regional twist.
- **No em-dashes anywhere.** En-dashes for numeric ranges only (1321 MR – 2135 MR).
- **Affirmative prose.** No "Not X" or "Not X but Y" openings, except a true negation with no affirmative form ("his cult kept no records").
- **The region-entry contract** (`docs/region-prose.md`): eye-level narration, colour in attributed quotes, elevation only at peaks, endings on a fact or a hook, no name-glossing, the chronicler's *I* only for absences, a required live tension, section mass decided by the user.
- **Chronicler tier in open prose; GM tier inside `⚿ GM Secret` only.**
- **Kingdoms inherit names, not continuity.** No Talanese kingdom predates 1 MR; default to Dark-Era or Adventurer-Era foundings.
- **Pre-read before designing; canon moves only on the user's yes; no silent contradiction.**
- **Lore before HTML; surface before writing; a phase closes only on the user's word.**

## Appendix E: Common pitfalls

- **Leading seeds with the archetype menu.** The census is for Phase 5, after the seed.
- **Reducing an ancestry to its one-line lore**, or **building a value-society**: a people's feeling must *fit into* a full culture, never *fill* it. A culture needs a concrete engine (a craft, a trade, a place, a collision).
- **Making the government be the seed** (Baratalda rebuilt its government five times): the government is born of the seed's world and is *about* something else (Tvisol is the model).
- **Letting pre-placed canon drive the seed** (Ilun Tasun: "forget the Wardstones, forget the port"); **treating a stub as built canon**; **theorising the domain instead of reading the exemplars**; **reading a domain as a literal climate**.
- **Designing on canon before reading it** (the Ash-Binder "2180 MR" defeat, impossible because the Nine Dungeons erupted in 2524).
- **Leaking a secret into open prose** (the No Man's Land slag sentence that said the slag was the General's body).
- **Overselling a secret:** a GM secret that changes nothing a reader already sees is weak (the Ash-Binder "killed the Emperor" candidate). Its weight is in the world, never in a story set-up.
- **Epigram endings** (Vernua's six; Legea's "the Goddess of Law watched") and **arithmetic slips** (Namur's "fifty-seven more than a lapse needs").
- **Pulling the loudest neighbour into every answer** (Namur's bread proposed as Legean, from its enemy): answer each question for plausibility, with every neighbour.
- **Invoking a canon faction without reading it** (the Mercenary Guild proposed as a rival of Namur's companies; it is a deniable shadow network of individuals, nothing like them).
- **Unchecked words and data:** a real-language word offered from memory, or a tool database treated as complete (warpglass).
- **Confusing naming collisions** (check Stormpact against Compact, or Namur's Speaker against Fenurra's). Shared generic offices are allowed; explain their local function and keep personal-name structures unique.
- **Damaging neighbouring canon:** moving an ancestry or a General means cleaning the cross-references in every file that names it.
- **Arguing sameness on the page:** a paragraph explaining why the region differs from another (its government, its rite) is authoring residue; the page describes the place as it is.
- **Inner anchors in clickable cards** (`docs/card-conventions.md` forbids them).
- **Measuring overflow against the window width**, which includes the scrollbar and reports false sideways scrolling.

## Appendix F: Parallelization for multi-page builds

**One page: build it directly**, especially with its lore already in context; an agent only re-reads everything and runs slower. **Two or more pages: one general-purpose agent per page, in parallel**, each given: the approved lore source files; the template page; the convention docs (`CLAUDE.md`, `docs/card-conventions.md`, `docs/accessibility.md`, `docs/sidebar-nav.md`, `docs/region-prose.md`); 2–3 accent options to check with `node tools/contrast.mjs`; the fixed style rules; the seed verbatim; the Phase 12 publication boundary; and a short report-back spec (accent and contrast, section count, which approved ◈ and ⚿ boxes were mirrored, unresolved questions and proposed lore additions).

Agents must report proposed lore additions **without implementing them**, including new names, quotes, beliefs, or secrets. The parent takes proposals to the user, updates the affected decisions and draft for review, and commits any approved lore changes through Phase 11 before agents mirror them. Never treat an agent's report as approval or silently fold additions into the glossary. Keep private story uses out of every setting page.

## Appendix G: Worked examples

- **The seed pattern:** Emarrea (the gold standard: foxfire → illusion → spectacle → drama → Heart Court; `lore/geography/lautara/emarrea.md`); the Lautara resketch of Itsasalda (the dock that never moves), Azkataria (the philosopher-market), and Atarialda (the welcome threshold).
- **The prose exemplar:** Breidey (GM-written; `lore/geography/floteyn/breidey.md` and its page).
- **The 2026-09 builds under this workflow's lessons:** Legea Empire (`zuzental/legea-empire.md`; a full pass on a built region), Order of Law (`zuzental/order-of-law.md`), No Man's Land (`sumendar/no-mans-land.md`; anarchy passing the three tests), Namur Republic (`zuzental/namur-republic.md`, with the co-written journal `namur-journal.md` and the pencil file `docs/pencilled/namur-republic.md`; the first build run close to this phase order).
- **The older full-workflow precedents:** Baerfrost, the Air Monastery (Wyndwalken), and Fellibylur (`lore/geography/vindul.md` and their pages).
