# Recall Knowledge (GM Layer)

How we write a knowledge check: what each degree says, and in what voice. The DC itself and the four-degree rules live in [`dc-cheatsheet.md`](dc-cheatsheet.md).

## Always

- **Spoken prose.** Each degree is a short paragraph the GM can read straight to the table, in the second person ("You have heard dockhands on every quay talk about them…"). A fact sheet is for the lore files.
- **Tiers stack.** The GM reads the lower tier, then the higher one, so each tier carries only what is new. A tier that builds on the one below carries the green **+** mark (`<span class="stack">+</span>`, styled in `gm.css`) before its label. Never open a tier with "everything in the success, and…".
- **Each degree opens with the roll it needs** in a boxed badge (`<span class="deg-at">≥30</span>`, styled in `gm.css`), then its label. The DC line gives the main skill's DC and, after a ·, each Lore's (usually 5 lower).
- **Critical failure is a confident falsehood**, in the players' voice, with a bracketed aside for the GM: *(False: a Freeboarder takes that as an insult.)* The best falsehoods are what mortals actually believe (a ◈ Popular Belief is the first place to look) and push the players toward a wrong but playable move.
- **Rumour, not file.** A check tells what is *said*: what an in-world scholar, sailor or tavern would pass on, hedged where the telling is hedged (*it is said*, *some say*, *many names were brought forth*). It serves the intrigue rather than settling it; even a critical success gives the best version of the story, never the GM's account. It may point at a GM secret; it never states one.
- Write it where it happens: a check sits right after the read-aloud that raises the question.

## Three shapes

### 1. Plain: one skill, four degrees

The default, for an ordinary subject. Simple DC by the proficiency a person would need to know it; a failure gives little or nothing.

*Reference:* the Twin Cities, Freeboard, Skysail and Pirate Lords topics on [`short-notice/quest-the-unspent/knowledge.html`](../short-notice/quest-the-unspent/knowledge.html); the flag check in Struck Colours.

### 2. Lenses: one mystery, a check per skill

When several skills would read the same thing differently, give each skill its own check with its own angle: what the thing *is* (Occultism, Arcana), how the faithful *read* it (Religion), who *trades* in it (Society), and so on. Each lens has a **common-knowledge line** at a low DC (what everyone local knows), the real DC above it, a critical success, and a critical failure. The players compare notes, and the mystery comes together from two directions.

*Reference: Furrious Five, Veldtmark, the drift (the GM's table, translated):*

> **Occultism: what the drift is**
> - **DC 15 (common knowledge; everyone in Millhaven knows it):** The drift comes over from the Cape and thins as it goes east: déjà vu, sounds arriving a heartbeat too early or too late, clocks that disagree. It stops at the river. On the Stillside there is none.
> - **Success (DC 23):** This far east the drift should be thin, a breath in the oldest lanes. Here, on the north edge of the Cape side, it is thicker than in the Drift Quarter, and the closer you come to the estate, the stronger it gets. Natural drift spreads like fog. This drift gathers.
> - **Critical success, also:** It does not just gather, it flows. Like water toward a drain, in one direction, toward the house. Something there is drawing it in, or drinking it.
> - **Critical failure:** They take it for ordinary Cape drift, harmless and familiar.
>
> **Religion: how the Cape side reads the drift**
> - **DC 15:** On the Cape side the drift counts as a blessing of Bikiargi of the twin moons, spilling east from the Cape. The Twin Lantern in Moonwatch teaches it. The Stillside calls it lake fog and laughs.
> - **Success (DC 23):** Bikiargi's blessing is meant to feel like a half-remembered dream on waking: gentle, a little wistful, peaceful. This feels different. The déjà vu is watchful, as if you had lived this moment before and been watched while you did.
> - **Critical success, also:** Bikiargi's cult knows the drift as something that comes from the moons, from above and outside. This feels as if it comes from below.
> - **Critical failure:** They take it for an unusually strong blessing, a good sign.

### 3. Stacked: a famous name with deep lore

For a subject that is common knowledge **and** has enough lore for three real tiers. Keep the DC high, and let a plain failure still give what everyone knows, as if it were a success on an easier check:

- **Critical failure (DC − 10 or less):** the falsehood.
- **Failure (DC − 9 to DC − 1):** the common facts.
- **+ Success:** the specific story, read after the failure.
- **+ Critical success:** the depth, read after both.

Use it sparingly; most subjects are plain.

*Reference:* Ninehulls, DC 25 (relevant Lore 20), on [`knowledge.html`](../short-notice/quest-the-unspent/knowledge.html) and in Struck Colours: a failure knows the name and the flag, a success the legend, a critical success the scar and the ambush.
