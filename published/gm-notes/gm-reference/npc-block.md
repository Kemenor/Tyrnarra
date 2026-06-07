# NPC Blocks (GM Layer)

How we define the people the party meets. **Build an NPC to the depth the table needs, not to a fixed template.** Most folk are **Cardboard**, a few are **Semi-Important**, and the recurring cast are **Full Blocks**. An NPC can just *be*: a baker is allowed to be a baker you talk to once. Not everyone needs a goal, and almost no one needs a hook.

Two things every NPC carries at every depth: a **Level / Non-Combat Level** (so any check against them resolves) and a **physical description** (so a portrait can be generated for any face in the cast). The description scales with depth: a line or two at Cardboard, a full paragraph at Full.

These blocks are GM-side. A stripped, secret-free version may later feed the player `/player-campaigns/` cards.

Sources: AoN [NPCs (2919)](https://2e.aonprd.com/Rules.aspx?ID=2919), [Skills table 2–3 (2885)](https://2e.aonprd.com/Rules.aspx?ID=2885). For interaction DCs (Coerce, Make an Impression, Request, Lie) once you have a Disposition, see [`dc-cheatsheet.md`](dc-cheatsheet.md).

## The three depths

- **Cardboard** — a merchant, a barmaid, some dock-hand. Enough to play for one scene and never again. Six or seven lines, all one-liners.
- **Semi-Important** — might come up again; needs enough to hold a real conversation or carry a quest beat, even if the party only talks to them once. Adds the performance layer, a motive, and a starting attitude.
- **Full Block** — recurring, important, in-depth: Aldric Fenn, Sable Rei, Vara Mink. Turns on the relationship web, the fears and secrets, the portrait, and arc-tracking across sessions.

## Field allocation

| Field | Cardboard | Semi | Full |
|---|:---:|:---:|:---:|
| Name | ● | ● | ● |
| Pronouns | ● | ● | ● |
| Occupation | ● | ● | ● |
| Ancestry + Age | ● | ● | ● |
| **Level / Non-Combat Level** | ● | ● | ● |
| The Read *(one line: how they come across)* | ● | ● | ● |
| Physical description *(scales: 1–2 sentences → full paragraph)* | ● | ● | ● |
| Clothing & dress *(full paragraph)* | – | ○ | ● |
| Voice | ○ | ● | ● |
| Skills *(with numbers, noteworthy only)* | ○ | ● | ● |
| Sample line | ○ | ● | ● |
| Mannerisms | – | ● | ● |
| Disposition *(starting attitude to party)* | – | ● | ● |
| Goal | – | ● | ● |
| Background *(2–3 driving facts)* | – | ● | ● |
| Faith | – | ○ | ● |
| Faction & Ties | – | ○ | ● |
| Fear | – | ○ | ● |
| Secret | – | ○ | ○ |
| Portrait | – | ○ | ● |
| Status | – | ○ | ● |

● core · ○ optional · – not at this depth

## Field notes

- **Level / Non-Combat Level.** Combat **Level** for anyone who might fight or needs scaling; **Non-Combat Level** for someone who never fights but is expert at a craft (a master baker is a non-combatant who is still Non-Combat Lvl 5 *at baking*). The level sets the baseline every skill reads off. See [NPCs (2919)](https://2e.aonprd.com/Rules.aspx?ID=2919). A full stat block is rarely needed; reach for one only when the party will actually trade blows with them, and grab an existing Monster Core / NPC Gallery creature by name before building bespoke.
- **The Read vs the physical description.** The Read is the gestalt: how they come across, what you'd notice first about their manner. The physical description is the literal look, and it scales with depth: a line or two at Cardboard, a full paragraph at Full (optional at Semi).
- **Clothing & dress.** Reading prose to picture the person at the table, required at Full and optional at Semi. It also sharpens any portrait prompt, so writing it is never wasted.
- **Portrait prompts are distilled, not stored.** When you generate art, Claude distills the physical + clothing text into the fal.ai prompt at that moment, and the tuned prompt lives in the quest's `portraits.json`, not in the block. There is no separate image-seed field to keep in sync with the paragraph.
- **Disposition.** Their starting attitude to the party, on the PF2e ladder. It sets how the first beat plays and anchors any interaction DC.

  | Attitude | Plays as |
  |---|---|
  | Hostile | wants to act against the party |
  | Unfriendly | dislikes and distrusts them |
  | Indifferent | no opinion yet (most strangers) |
  | Friendly | likes them, will help within reason |
  | Helpful | will take real risks for them |

- **Faith.** This is a multi-god setting; the default is **casual multifaith** (a common person prays to several gods across a day: Jianna at the stall, Shuun before a crossing). Note the gods they actually lean on and when. Reserve a single **patron** (and any edicts / anathema) for the genuinely devout: clergy, champions, zealots. Remaster has no alignment, so do not record one.
- **Faction & Ties.** Faction first (which bloc, guild, or house). Add the key personal ties (who they answer to, owe, love, or hate) at Full depth.
- **Secret.** Optional at every depth, including Full. Not everyone is hiding something; only write one when it exists.
- **Status.** Alive / dead / where in their arc, for tracking the recurring cast across sessions.

## Level + Skills (Table 2–3)

The NPC's Level (or Non-Combat Level) sets the baseline; each **noteworthy** skill reads off the column that matches how good they are. List only the skills that matter for who they are: Stealth for a rogue, Diplomacy for a merchant.

- **Specialty** (what they are known for) → **High**, or **Extreme** only if world-class for their level.
- **Competent** → **Moderate**.
- **Trained but incidental** → **Low**.

Most NPCs list 1–3 skills. A master gets one Extreme; everyone else tops out at High.

| Level | Extreme | High | Moderate | Low |
|---|---|---|---|---|
| -1 | +8 | +5 | +4 | +2 / +1 |
| 0 | +9 | +6 | +5 | +3 / +2 |
| 1 | +10 | +7 | +6 | +4 / +3 |
| 2 | +11 | +8 | +7 | +5 / +4 |
| 3 | +13 | +10 | +9 | +7 / +5 |
| 4 | +15 | +12 | +10 | +8 / +7 |
| 5 | +16 | +13 | +12 | +10 / +8 |
| 6 | +18 | +15 | +13 | +11 / +9 |
| 7 | +20 | +17 | +15 | +13 / +11 |
| 8 | +21 | +18 | +16 | +14 / +12 |
| 9 | +23 | +20 | +18 | +16 / +13 |
| 10 | +25 | +22 | +19 | +17 / +15 |
| 11 | +26 | +23 | +21 | +19 / +16 |
| 12 | +28 | +25 | +22 | +20 / +17 |
| 13 | +30 | +27 | +24 | +22 / +19 |
| 14 | +31 | +28 | +25 | +23 / +20 |
| 15 | +33 | +30 | +27 | +25 / +21 |
| 16 | +35 | +32 | +28 | +26 / +23 |
| 17 | +36 | +33 | +30 | +28 / +24 |
| 18 | +38 | +35 | +31 | +29 / +25 |
| 19 | +40 | +37 | +33 | +31 / +27 |
| 20 | +41 | +38 | +34 | +32 / +28 |
| 21 | +43 | +40 | +36 | +34 / +29 |
| 22 | +45 | +42 | +37 | +35 / +31 |
| 23 | +46 | +43 | +38 | +36 / +32 |
| 24 | +48 | +45 | +40 | +38 / +33 |

## Reference blocks

### Cardboard

> **Nessa Crale** · she/her · barmaid, the Sodden Mast · Human, ~30 · **Non-Combat Lvl 1**
> *The Read:* pours fast, hears everything, never forgets a face or a tab.
> *Physical:* stocky and ruddy, dark hair tied back, sleeves shoved to the elbow, a permanent half-smile that doesn't reach tired eyes.
> *Skill:* Society +7 (every regular, every debt, who's not talking to whom)

### Semi-Important

> **Oswin Thetch** · he/him · proprietor, the Empirical Eye (Cape side) · Human, ~60 · **Lvl 8** (non-combatant in play; stat at 8 if ever pushed)
> *The Read:* a tidy, precise old shopkeep who has clearly seen worse than you.
> *Physical:* spare and ink-stained, close-cropped grey, wire spectacles, moves around a cluttered shop without ever once looking for anything.
> *Voice:* dry, exact, faintly amused. *Mannerisms:* alphabetises as he talks; corrects your terminology gently.
> *Sample line:* "Minor enchantment, you said. People always do. Show me the thing."
> *Disposition:* Friendly (fond of young adventurers, in the way of someone who has buried several).
> *Goal:* a quiet retirement that stays quiet.
> *Background:* high-rank retired adventurer; does not discuss it; learned component-discipline the hard way.
> *Skills:* Arcana +18 (High), Crafting +16 (Moderate). *Faith:* casual; a nod to Enki over a hard identification.
> *(Full Physical / Clothing paragraphs are optional at this depth; add them if he becomes a recurring face.)*

### Full Block

> **Sable Rei** · they/them · Merchant-Lord, the Clearwater docks · Bridge council seat · Kitsune, *appears* mid-30s (older) · **Lvl 7**
> *Portrait:* `assets/portraits/sable-rei.webp` · *Status:* active · Friendly to party · arc: do they pull the party into the free-trader world?
> *The Read:* charming, theatrical, introduces themselves differently every time; you like them immediately and that's the point.
> *Physical:* Sable wears the body lightly, the way someone does who has worn others. In their preferred shape they read as a slim, mid-thirties Kitsune of no fixed gender: fur silvering at the temples, one ear out and the other tucked under hair as if they forgot to finish the disguise. The amber eyes track everything and rest on nothing. A hand, a tail, sometimes the jaw flickers to fox for half a sentence and back, never the full change in company, just enough to remind you they could. Under the poise runs a thread of worry the smile is built to cover.
> *Clothing & dress:* Immaculate, never quite formal. A fine charcoal high-collared coat cut for movement, good boots that have clearly run, and exactly one flamboyant detail per outfit that changes by the day: a cravat the colour of a warning flag, a ringed thumb, a brooch shaped like a ship that is not one of their ships. Nothing carries a maker's mark you could trace, and every layer has a pocket. They dress a half-step richer than a bridge merchant and a half-step poorer than they could, so you read them as successful rather than dangerous.
> *Voice:* warm, quick, shifts register to match the room. *Mannerisms:* flicks a hand to fox-form mid-sentence for emphasis; never sits with their back to a door.
> *Sample line:* "Oh, I have *several* names. Use whichever one buys you the most trust today. I certainly do."
> *Disposition:* Friendly, and entirely self-interested; both are real.
> *Goal:* keep the fleet's paperwork immaculate and the bridge bloc ungoverned. *Fear:* being pinned to one fixed identity, or one ledger that names them. *Secret:* the six-port fleet's legitimacy rests on a single forged charter; one other person alive knows.
> *Faction & Ties:* Bridge bloc with Aldric Fenn and Tomas Hewer; the Midarra free-traders; quietly at odds with Watch-Captain Holt Drevyn.
> *Skills:* Deception +20 (Extreme), Society +17 (High), Diplomacy +17 (High), Stealth +15 (Moderate). *Faith:* casual multifaith, public nods to Jianna, a real private lean on Nirfel.

## How it renders

These map straight onto the existing `.npc-card` (see [`gm.js`](../assets/gm.js) / [`gm.css`](../assets/gm.css)), so no chrome work is needed to start using them:

- **role row** → Occupation (+ Level, faction seat)
- **`npc-summary`** → The Read
- **`npc-body`** → one `exp-label` section per remaining field, with `trait-list` carrying Skills and any "What They Want" list

A Cardboard NPC needs only the header and summary; a Full Block fills the body.
