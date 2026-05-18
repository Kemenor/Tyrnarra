# PF2e Notes — System-Side Bookkeeping

Tyrnarra is built for play with **Pathfinder 2e (Remaster)**. The lore files capture *what is true in the world*; this file captures *how that world maps onto the rules*. GM-facing reference, not canon prose.

**See also:** `bestiary.md` (where each ancestry lives in Tyrnarra), `gods.md` (cleric domains per bound god + Domains Outside the Thirteen), `cosmology.md` (the four schools of magic).

---

## Ancestry roster vs. the standard 44

Tyrnarra adopts the 44 PF2e Remaster ancestries with three adjustments:

### Renames adopted from the Remaster

- **Kholo** (formerly Gnoll) — full canon entry in `bestiary.md`.
- **Tripkee** (formerly Grippli) — full canon entry in `bestiary.md`.

### Tyrnarra-canon additions (outside the standard 44)

- **Dragons** — the alien-mothership lineage. Distinct from PF2e's **Dragonet** ancestry (Tyrnarra uses *Dragonet* for native Zaharsuge-line wyrmkin); both ancestries exist on Talan and are unrelated.
- **Slimes** — Darklands-adapted; the published slime ancestry on Talan is almost always a Darklands-born individual that worked its way to the surface.
- **Rabbitfolk** — uncommon everywhere; widely scattered, frequently nomadic.

### Removed

- **Dragonkin** — D&D 5e migration relic. No narrative footprint worth keeping. Dragons (alien lineage) and Dragonet (native wyrmkin) cover the dragon-coded play space.

### Access tags

The PF2e *common / uncommon / rare* access tags apply at Talan scale. The Ancestry Distribution table at the top of `bestiary.md` lists per-domain dominance, uncommon access, and rare access for every placement.

### Drow — Talan-specific framing

PF2e's default drow are underdark-dwelling. On Talan, the underdark is the **Darklands** — the Corrupted God's territory. Drow on Talan are surface-dwelling children of shadow, concentrated in Myrkono around Araphel's domain. The mechanical ancestry is unchanged; the framing is.

### Sortalde (Tian Xia) ancestry placements

The six Tian Xia ancestries (Samsaran, Sarangay, Tanuki, Wayang, Yaksha, Yaoguai) are placed on **Sortalde**, the petal-archipelago continent east of Talan. Each occupies a single petal; on Talan they are vanishingly rare. Full per-ancestry detail in `bestiary.md` — *Sortalde Ancestries — The Six Petals*.

**Hungerseed** is resolved as half-Oni; Oni are bound spirits of **Lingdao** (Spirit Island). Almost all Hungerseeds in canon are Sortalde-born.

---

## Versatile Heritages — Remaster reshuffle

The Remaster reshuffled the versatile-heritage roster:

- **Nephilim** absorbs the former Aasimar (celestial) and Tiefling (fiendish) heritages — both expressions are now Nephilim, with parentage determining the manifestation.
- **Ardande** (Wood) and **Talos** (Metal) are new elemental options. In Tyrnarra they map to the two non-Material planes of the Life Layer — Ardande to **Feyworld**, Talos to **Shadowplane**.
- **Aiuvarin** and **Dromaar** replace Half-Elf and Half-Orc as the canonical mixed-ancestry heritages.
- **Suli** is now generic geniekin, with no single-element specialisation.

Full source-mapping table (which god / plane each heritage descends from) lives in `bestiary.md` — *Versatile Heritages*.

### Bound gods whose touch is not bloodline-borne

After the Remaster reshuffle, four of the bound thirteen have no exclusive heritage on Talan:

- **Iro** (Light) — celestial Nephilim covers the divine-blood expression.
- **Enki** (Knowledge) — Enki was Suli pre-Remaster; Suli is now generic geniekin. Enki's touch manifests as scholarly aptitude rather than physical change.
- **Jianna** (Commerce) — blessing accumulates as trade fortune, not body trait.
- **Cronus** (Freedom) — worshippers are made by choice, not blood (see `secret-history.md` — *Cronus — The Secret*).

---

## Cleric Domains

The official PF2e cleric-domain register (61 domains as of the Remaster + Tian Xia + War of Immortals expansions) is the authoritative mechanical list. The published reference page at [`pf2e-registrar.html`](../pf2e-registrar.html) holds the master mapping from each PF2e domain to its in-world Tyrnarra granter (Bound 13 god, non-bound god, sin-devil, virtue-demon, General of Corruption, or Open / canon-pending).

### The Thirteen's domains

The 13 Bound Gods' grantable cleric domains live on [`pf2e-registrar.html`](../pf2e-registrar.html). Bound god assignments follow a **no-sharing rule**: each PF2e domain that any of the Thirteen grants is granted by exactly one god — the deity it fits most strongly. Cross-portfolio overlap (a domain credibly fitting two gods) is resolved by giving the domain to whichever god's *primary* aspects align most directly; the other god keeps the *flavour* of the domain in lore but not the mechanical grant. The Thirteen between them currently claim **46 of the 61 PF2e cleric domains**.

### Lore-implicit domains — Tyrnarra theological flavour, not PF2e-mechanical

Some domain names in the Tyrnarra canon are **theological-flavour names**, not entries in the official PF2e cleric-domain register. They live in canon as the way mortals on Talan name an aspect of a god's portfolio, but they do not grant a discrete PF2e domain. A cleric of one of these gods picks from the god's PF2e-canonical domains; the lore-implicit names are the *flavour* through which that god's worshippers describe their own work.

| Lore-implicit name | God that carries it (as flavour) | What it expresses through (mechanically) |
|---|---|---|
| **Arcane Magic** | Forseti | Truth · Secrecy · Star · Glyph |
| **Divine Magic** | Iro | Sun · Healing · Dust · Zeal |
| **Occult Magic** | Enki | Knowledge · Magic · Perfection |
| **Primal Magic** | Jianna | Cities · Family · Wealth |
| **Progress** | Jianna | Cities · Family · Wealth — civic-growth flavour |
| **Free Will** | Vesuna | Luck · Trickery · Change · Disorientation — choice flavour |
| **Second Chances** | Araphel | Darkness · Nothingness · Protection — rebirth flavour |

**The convention.** When the Tyrnarra canon uses a domain name not on the official PF2e register, treat it as Tyrnarra theological flavour for the god's PF2e-canonical portfolio. Players selecting a cleric of, say, Forseti pick from the PF2e domains Forseti grants (Truth, Secrecy, Star, Glyph) — *Arcane Magic* is the in-world name Forseti's clergy use for their work, not a separate domain at character-build time.

**Reconciled out of canon.** Several flavour names previously in canon have been **retired** during the PF2e domain rebuild: *Peaceful Death* (dropped from Tani; **Death is now Hinka's alone** — Tani retains Fate and Time, plus Soul; her death-and-return remains character canon), *Violent Death* (replaced for Hinka by the PF2e Death domain), and *Delirium* (dropped entirely; the Temperance-deficiency virtue-demon's PF2e grant is now canon-pending). The older *Void* domain has been **renamed** in line with the PF2e Remaster to *Nothingness* — Araphel grants Nothingness; older canon's *Void* readings continue to mean the same domain.

### Non-bound granters — canon-pending

A previous canon pass mapped 13 PF2e domains to non-bound granters (sin-devils, virtue-demons, Generals of Corruption, Betibizi, the Corrupted God directly). **That mapping has been rolled back to Open** as part of the bound-god rebuild — the non-bound entities still exist as canonical beings, but their specific PF2e cleric-domain grants are now canon-pending, awaiting a fresh assignment pass focused on the non-bound side. The 13 domains in this state are:

- **Abomination** *(prior candidate: Muiral the Misshapen, Modesty-line virtue-demon)*
- **Decay** *(prior candidate: The Rot-Tyrant, General of Corruption)*
- **Destruction** *(prior candidate: The Wrath Sin-Devil)*
- **Indulgence** *(prior candidate: The Gluttony Sin-Devil)*
- **Naga** *(prior candidate: The Maw Serpent, General of Corruption)*
- **Nightmares** *(prior candidate: The Whisperer in Dreams, General of Corruption)*
- **Pain** *(prior candidate: virtue-demon, Patience-line excess)*
- **Plague** *(prior candidate: The Corrupted God, direct grant)*
- **Sorrow** *(prior candidate: virtue-demon, Magnanimity-line deficiency)*
- **Swarm** *(prior candidate: The Vermin Queen, General of Corruption)*
- **Toil** *(prior candidate: virtue-demon, Industriousness-line excess)*
- **Tyranny** *(prior candidate: The Pride Sin-Devil)*
- **Undeath** *(prior candidate: Betibizi, self-ascended Minor God in Abyss)*

### Domains not yet claimed — Open / GM ruling

Two PF2e domains exist in the system but have no canonical Tyrnarra granter on either side (bound or non-bound), and no prior assignment to roll back: **Dragon** and **Moon**. Plausible candidates exist (Zaharsuge for Dragon; Bikiargi for Moon) but neither is decided. Treat these as obscure or experimental claims that need a GM ruling until canon settles them.

---

## Favoured weapons

Per-god favoured weapons in `gods.md` — *The Thirteen — Per-God Sheet* are both iconography and PF2e cleric mechanical favoured weapons. Araphel's **Kusarigama** (sickle-and-chain) is canon both ways.

---

## Ancestries unchanged from PF2e canon

A handful of ancestry entries in `bestiary.md` carry no Tyrnarra-specific reframing — their PF2e default is the canon default. Notable examples: **Gnome**, **Poppet**, **Sprite**. These read as they do in published PF2e material; placement notes in `bestiary.md` capture only their Talan-specific distribution.

---

## Mechanical-rules reference

The world canon does not duplicate PF2e crunch. For mechanical traits, ability scores, feats, languages, hit-die progressions, and other system specifics, refer to the published PF2e Remaster ancestry / heritage / cleric domain entries. Tyrnarra-specific deviations are limited to the placements, renames, and additions noted above.
