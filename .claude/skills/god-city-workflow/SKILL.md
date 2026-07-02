---
name: god-city-workflow
description: Use this skill when building or fleshing out one of the thirteen Bound-god city-states of Talan (the god-cities) in the Tyrnarra worldbuilding project, taking it from its locked seed in docs/god-city-seeds.md to full lore and a dedicated Style B HTML page. Trigger on "build [god-city]", "flesh out [god-city]", "next god-city", "promote [god-city]", the god-city pass, or any of the thirteen names: Merkavar (Commerce/Jianna), Myrria (Darkness/Araphel), Haizava (Wind/Fisaya), Eldara (Fire/Komo), Valreka (Time/Tani, formerly Denbora), Thekkavar (Knowledge/Enki), Frae City (Freedom/Cronus), Uravel (Water/Shuun), Lurrath (Earth/Sarrum), Ljosarn (Light/Iro), Lograth (Law/Forseti), Veidrath (Hunt/Hinka), Nahaskel (Chaos/Vesuna). Also trigger when working with docs/god-city-seeds.md (the seed roster), or deepening/maturing an already-built god-city. Builds on sub-region-workflow and composes with grill-me-lore. Do NOT use for ordinary sub-regions, kingdoms, or factions (use sub-region-workflow), nor for cosmology or pantheon work.
---

# God-city workflow

## What this skill is for

Taking one of the **thirteen Bound-god city-states** from its **locked seed** (in [`docs/god-city-seeds.md`](../../../docs/god-city-seeds.md)) to fully fleshed lore and a dedicated Style B HTML page, in a single session, with the user's voice setting direction at every phase boundary. A god-city is the seat of a Grand God; it is not a normal sub-region, and it earns a dedicated page by default (the seed roster exists precisely so each of the thirteen reads distinct).

The build pass is complete: **all thirteen god-cities carry full lore and a published page** (status roster in `docs/god-city-seeds.md`). The skill now serves the maturation passes: deepening an already-built city (the Myrria/Merkavar retro-pass of 2026-06-16 is the model), naming its figures, festivals, and landmarks, or mirroring new canon onto its page. The same phases apply, with Phase 7 an edit of the existing page rather than a build. Read two or three built cities side by side before designing; they are what a finished god-city reads like.

## This skill is built on `sub-region-workflow`

The shared machinery lives there; **do not duplicate it, reuse it**. From `sub-region-workflow`, carry over verbatim:

- The **eight-phase spine** and the phase-boundary discipline (surface at each seam, even under "work through it").
- The **naming-stratum rule** (old → Basque/Icelandic drift; modern/institutional → English drift; regional registers) and the **collision check** (*Compact* reserved, *Order* heavy).
- **Surface-before-writing**, **lore-first**, and the **commit / publish signal** protocol (commit to lore only on "commit"; touch HTML only on an explicit publish/promote signal).
- The **single-page rule**: a god-city is one page, so **build it directly, no agent**, especially when you just wrote its lore and hold the canon in context.
- The **Style B page conventions** (template `published/setting/talan/domains/vindul/haizetsua/haizetsua.html`; accent must clear 3:1 against `#0f0c08`; card conventions; absolute links; no em-dashes).

What this skill **adds** is everything below: the pre-locked seed, the depth axes, the manifestation pattern, the two-tier reveal, and the god-city-specific conventions.

## The roster

[`docs/god-city-seeds.md`](../../../docs/god-city-seeds.md) is the source of truth for the pass: the thirteen seeds, the **uniqueness architecture** (the elemental quartet; the make/build/know cluster; the light-dark pair; the knowledge trio; Frae-vs-Nahaskel), the **per-city build-notes** (rich design + build flags for the unbuilt cities), and the **status** of each. Open it first. Update the city's status there at commit and again at HTML promotion.

## The god-city flow (phases, adapted)

**Phase 0 — read the canon.** Same pre-read discipline as `sub-region-workflow`, plus the god-city specifics:
- The **domain file** (`lore/geography/<domain>.md`) and each **bordering domain** end-to-end.
- The **god's per-god sheet in `gods.md`, including the per-god `⚿ GM Secret`** (Cronus's mortality, Tani's death/rebirth, etc.). The GM-tier seam of a god-city usually grows from the god's own secret, so read it.
- The **`docs/god-city-seeds.md` entry** (seed + uniqueness + build-notes + build flags) and the **sibling god-cities** for the uniqueness test.
- **Grep the city name** across the repo: god-cities accrete stray canon (Frae City had The Lantern Press and the Cronus-clergy envoys; Thekkavar had the Helgaft and Jeanne Pintos). The **`published/setting/cosmology/grand-gods.html` per-god `city` field and worship/depiction lines** are player-facing canon to honor and elaborate, not contradict.
- If the seed touches loaded canon (Crimson Rain, the Storveldi Denbora, a god's death), pre-read the relevant `timeline.md` / `cosmology.md` section too.

**Phases 1-2 — the seed is already locked.** Do not run the seed-questions or generate seeds. **Confirm the locked seed back to the user from the roster** and short-circuit, the way the Lautara resketch did. The per-city build-notes often carry extra design the user set in an earlier workshop; fold it in.

**Phase 3 — grill the depth axes** (below) one at a time via `grill-me-lore`, each question with a recommended answer drawn from canon and the seed.

**Phase 4 — naming pass.** The god-city's own name is usually set (propose a better-fitting one only if it genuinely fits, as with Denbora → Valreka). Coin the institutions, the manifestation's folk-name, and any signature features. Record etymologies in `glossary.md` at commit.

**Phase 5 — surface the full draft** for review (the `## <City>` section for `lore/geography/<domain>.md`, glossary sub-region + faction blocks, ancestry notes), with the chronicler-tier check and flagged derivations. Do not commit yet.

**Phase 6 — commit lore** on the explicit go: the city section in `lore/geography/<domain>.md`, glossary (sub-region etymology + faction proper-nouns block), `lore/ancestries.md` notes for the anchor peoples, `docs/open-threads.md`, and the **status cell in `docs/god-city-seeds.md`**.

**Phase 7 — HTML promotion** on the explicit publish/promote signal: build `published/setting/talan/domains/<domain>/<slug>/<slug>.html` directly; upgrade the domain page's **God's-City callout** from a plain `<div>` to a clickable `<a class="gods-city">` with trailing ` →`; wire `published/setting/assets/site-nav.js`, `docs/site-inventory.md`; mirror any **rename ripple** onto `published/setting/talan/domains/domains.html` and `published/setting/cosmology/grand-gods.html` (the Denbora → Valreka case); update the seeds-doc status to done.

## The depth axes (grill all of these)

Render them in the Phase 5 lore and the Phase 7 page. A full god-city build hits every one.

- **Daily life: the trio, and the job each leg does.** Cover all three; a single thematic lens (the descent, the discipline of restraint, the climb) is the *content* the trio reveals, not a replacement for it.
  - **Mass life** — the ordinary person's day and rhythm, and the shared civic ritual if there is one (Haizava's dawn reading, Thekkavar's Quiet Hour and tea-houses, Valreka's herd-rhythm).
  - **Transport / circulation** — how people and goods actually move, and the **signature movement** below.
  - **Visitor vs native** — what the outsider sees versus what the local knows, usually a knowledge-or-danger gap (which lift to trust, which booms mean run, that the deep is lethal, how to read the herd, the Quiet Hour you don't talk through, the contract you accepted by climbing).
  - **Youth** — rebellion, fun, freedom from the rules: the sanctioned transgression (Haizava's svif trick-crews, Eldara's scorch-yard, Valreka's Strays, Thekkavar's unauthorised descent, Frae City's climb-racers who scorn the paid ways up) and the coming-of-age act.
- **The signature movement.** Each city gets one, or pointedly does not (and the absence is the point). Haizava: the svif and the clergy-piloted windrift. Valreka: outriders on breaching Stokkul, plus the contraption-bridges. Eldara: the one-off lifts, no universal craft. Thekkavar: page-runners and a deliberate walking-pace. Frae City: the climb, the lift, and the airship Rim.
- **The god in the city (the manifestation pattern).** Every bound god appears in their seat in the shape of that city's life; **coin how**. It is usually the **◈ Popular Belief**, sometimes with a **⚿ GM Secret** beneath (the hidden or truer version). Locked examples: Araphel a stranger who talks (Myrria); Jianna a trader, the customer who might be Her (Merkavar); Fisaya herself, riding a svif (Haizava); Komo the apprentice who offers help (Eldara); Tani the old woman at the dig (◈) and Amona of the Strays (⚿) (Valreka); Enki the incognito lecturer who teaches and withholds (Thekkavar); Cronus the broken-chain man who arm-wrestles and never loses (Frae City). The humble/incognito register is the norm; the god meets the people in a joyful, egalitarian act of the city's own life.
- **The two-tier reveal.** A god-city carries at least one **◈ Popular Belief** (the folk manifestation or tale, often quietly true) and at least one **⚿ GM Secret** (the domain's hidden seam, which usually grows from the god's own per-god secret): Haizava's counter-trim, Eldara's eruption-clock, Merkavar's Stall-Jianna-Keeps, Valreka's Amona, Thekkavar's price in the Leize, Frae City's Cronus-was-mortal. **Open prose stays chronicler-tier; the seam lives in the box.** Long pages take several themed ⚿ boxes, not one wall.
- **Seed and uniqueness.** Confirm the locked seed; run the **two-sentence test against the other twelve god-cities**, not only same-domain siblings (the elemental quartet and the make/build/know cluster are the easy blurs). Answer the **economy question** (what the city makes, keeps, or needs, and what leaves it). On the page, the **first themed section expands the seed, never governance**.

## God-city conventions

- **A god rules his temple, not his city** (canon, `gods.md`, *The Gods' City-States*). The city-state is self-governing; the god governs only his sanctum and **walks among the citizens** (the manifestation). Design the civic government as a mortal polity; keep the god's seat a separate beat.
- **The God's-City callout** renders the city's heart as a `.gods-city` block (the Eye, the Open Forge, the Mother Whale, the Leize, the seven-chained rock). On promotion it becomes the clickable link from the domain page.
- **Accent**: pick a hue that fits the god and clears 3:1 against `#0f0c08`; where the god has a pantheon orb accent in `published/setting/cosmology/grand-gods.html`, harmonising with it is a nice touch (Tani's `#9070b0` → Valreka's amethyst).
- **Honor the `published/setting/cosmology/grand-gods.html` canon.** Each god-city has a `city` field plus worship/depiction lines there; the page should elaborate them, never contradict (Thekkavar's Infinite Library test; Frae City's lightest-touch clergy and the tavern claims that hold up).

## Reference implementations (all thirteen are built; these seven are the annotated depth-bar)

| City | File(s) | ◈ / ⚿ seam |
|---|---|---|
| **Merkavar** | `lore/geography/lautara.md` *(Notable Locations)*; `published/setting/talan/domains/lautara/merkavar/merkavar.html` | the smile-touched ◈; the Stall Jianna Keeps ⚿ |
| **Myrria** | `lore/geography/myrkono.md`; promoted page | reference-depth (sanctuary / second chances) |
| **Haizava** | `lore/geography/vindul.md`; `published/setting/talan/domains/vindul/haizava/haizava.html` | the Stranger on the Svif ◈; Who Banishes the Grasping ⚿ |
| **Eldara** | `lore/geography/sumendar.md`; `published/setting/talan/domains/sumendar/eldara/eldara.html` | the Apprentice ◈; the eruption-clock + the Odain tie ⚿⚿ |
| **Valreka** | `lore/geography/lioaru.md`; `published/setting/talan/domains/lioaru/valreka/valreka.html` | the old woman at the dig ◈; Amona is Tani + the water-bearers' atonement ⚿⚿ |
| **Thekkavar** | `lore/geography/ezkudon.md`; `published/setting/talan/domains/ezkudon/thekkavar/thekkavar.html` | Enki teaches ◈; the price in the deep + what waits in the Leize ⚿⚿ |
| **Frae City** | `lore/geography/askamira.md`; `published/setting/talan/domains/askamira/frae-city/frae-city.html` | the broken-chain man ◈; Cronus was mortal ⚿ |

The other six (**Lograth** · zuzental, **Veidrath** · ehizahar, **Nahaskel** · nashavel, **Uravel** · floteyn, **Lurrath** · brauogi, **Ljosarn** · egulon) follow the same pattern: lore in the domain's `lore/geography/<domain>.md`, page at `published/setting/talan/domains/<domain>/<slug>/<slug>.html`, each with its own ◈/⚿ seam on the page.

## Hard rules (inherited, restated)

- **Chronicler-tier in open prose; GM-tier only inside `⚿ GM Secret` boxes.** If a chronicler reading the open prose would learn something the lore marks GM-only (a god's secret, a hidden mechanism), move it into the box.
- **No em-dashes** anywhere (en-dashes for numeric ranges only). **Affirmative prose.** **Mortals, not humans.**
- **Lore-first; surface before writing; commit only on an explicit go; touch HTML only on an explicit publish/promote signal.**
- **Pre-read before designing.** A god-city sits on top of the most loaded canon in the setting; read the god's sheet (and its `⚿` secret) and the touched `timeline.md` / `cosmology.md` sections first.
