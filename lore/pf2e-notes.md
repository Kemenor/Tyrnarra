# PF2e Notes: System-Side Bookkeeping

Tyrnarra is built for play with **Pathfinder 2e (Remaster)**. The lore files capture *what is true in the world*; this file captures *how that world maps onto the rules*. GM-facing reference, not canon prose.

**See also:** `ancestries.md` (where each ancestry lives in Tyrnarra), `gods.md` (cleric domains per bound god + Domains Outside the Thirteen), `cosmology.md` (the four schools of magic).

---

## Ancestry roster vs. the standard 44

Tyrnarra uses the PF2e Remaster ancestry roster, plus the additions below.

### Tyrnarra-canon additions (outside the standard 44)

- **Dragons**: the alien-mothership lineage. Distinct from PF2e's **Dragonet** ancestry (Tyrnarra uses *Dragonet* for native Zaharsuge-line wyrmkin); both ancestries exist on Talan and are unrelated.

### Access tags

The PF2e *common / uncommon / rare* access tags apply at **Talan scale**: they describe how likely a people is to be met somewhere on the continent at random, and this is the system-facing access value. **In-region commonness is a separate axis.** A people native to and concentrated in a region is *common in that region* regardless of its Talan-scale tag, so a Talan-uncommon ancestry can still be the common, expected face of its own heartland (Jotunborn in Baerfrost, Automaton in Eldara, Conrasu in Nashavel). The two statements never collapse into one tag: the Talan-scale tag stays the PF2e access value; the in-region reading is set by where the people actually live. A corollary the Ancestry Distribution table obeys: a people with a heartland is never written up as uncommon or rare *everywhere*, only as Talan-scale uncommon or rare with its heartland named. The table at the top of `ancestries.md` lists per-domain heartland peoples (common where they live, sub-region noted when they cluster in one) alongside the peoples thin even within a domain.

### Sortalde (Tian Xia) ancestry placements

The six Tian Xia ancestries (Samsaran, Sarangay, Tanuki, Wayang, Yaksha, Yaoguai) are placed on **Sortalde**, the petal-archipelago continent east of Talan. Each occupies a single petal; on Talan they are vanishingly rare. Placement and access in `ancestries.md` (*Ancestry Distribution by Domain → Sortalde-native* and the combined alphabetical entry); full per-people canon in `geography/_off-continent.md`, *Sortalde → The Six Peoples*.

**Hungerseed** is resolved as half-Oni; Oni are bound spirits of **Lingdao** (Spirit Island). Almost all Hungerseeds in canon are Sortalde-born.

---

## Versatile Heritages

The PF2e versatile-heritage roster maps to Tyrnarra by source family (the 2026 planar-strata architecture):

- **Sparks of the substrate (Layer 1)**: Ifrit/Suzar · Undine/Urzar · Oread/Lurzahar · Sylph/Haizar · Ardande/Zurzar (Feyworld wood) · Talos/Burdinzar (Shadowplane metal) · Suli (the blend).
- **Essence of the sibling planes (Layer 2)**: Aphorite (Shadowplane, Order) · Ganzi (Feyworld, Chaos), the counterpart pair.
- **Divine parentage (Layer 3)**: **Nephilim** only, any god or devil, the bound thirteen included; a god's touch never rides a bloodline, parentage is the one way in.
- **Mortal mixes**: Aiuvarin (elf-blood) · Dromaar (orc-blood) · Beastkin (the Awakened line).
- **The old powers' lines**: Duskwalker (Epairima) · Changeling (Bikiargi) · Dhampir (vampire-line) · Dragonblood (Wyrmkin line) · Hungerseed (half-Oni) · Reflection (Wellspring-direct).

Full source mapping and the carry-register prose live in `ancestries.md`, *Versatile Heritages*; the quick-reference list is in `glossary.md`, *Versatile heritage placements*.

---

## Cleric Domains

The official PF2e cleric-domain register (61 domains as of the Remaster + Tian Xia + War of Immortals expansions) is the authoritative mechanical list. The published reference page at [`pf2e-registrar.html`](../published/setting/cosmology/pf2e-registrar.html) holds the master mapping from each PF2e domain to its in-world Tyrnarra granter (Bound 13 god, non-bound god, Vice Demon, Virtue Devil, General of Corruption, or Open / canon-pending).

### The Thirteen's domains

The 13 Bound Gods' grantable cleric domains live on [`pf2e-registrar.html`](../published/setting/cosmology/pf2e-registrar.html). Bound god assignments follow a **no-sharing rule**: each PF2e domain that any of the Thirteen grants is granted by exactly one god, the deity it fits most strongly. Cross-portfolio overlap (a domain credibly fitting two gods) is resolved by giving the domain to whichever god's *primary* aspects align most directly; the other god keeps the *flavour* of the domain in lore but not the mechanical grant. The Thirteen between them currently claim **46 of the 61 PF2e cleric domains**.

### Lore-implicit domains: Tyrnarra theological flavour, not PF2e-mechanical

Some domain names in the Tyrnarra canon are **theological-flavour names**, not entries in the official PF2e cleric-domain register. They live in canon as the way mortals on Talan name an aspect of a god's portfolio, but they do not grant a discrete PF2e domain. A cleric of one of these gods picks from the god's PF2e-canonical domains; the lore-implicit names are the *flavour* through which that god's worshippers describe their own work.

| Lore-implicit name | God that carries it (as flavour) | What it expresses through (mechanically) |
|---|---|---|
| **Arcane Magic** | Forseti | Truth · Secrecy · Star · Glyph; the Wellspring channeled through law: rigid, mathematical, ritual lines drawn at exact angles because they must be. |
| **Divine Magic** | Iro & Araphel | Sun · Healing · Dust · Zeal (Iro) and Darkness · Nothingness · Protection (Araphel); the god-granted tradition at both its poles: dawn and dusk, blessing and rebirth, faith made power whether by sunlight or shadow. |
| **Occult Magic** | Enki | Knowledge · Magic · Perfection; knowledge in all its forms, including the felt, the sung, and the told: the recipe, the lullaby, the dissertation. |
| **Primal Magic** | The Four Elemental Gods (Sarrum · Komo · Shuun · Fisaya); and Jianna | Earth · Fire · Water · Air, the substrate of the material plane: Primal magic is the four-fold balance made channelable, what every living thing is composed of. Jianna carries it a step on, as civilization read as a living system: the city as an ecology, trade as the flow that feeds it, the family as the first ecology. |

**The convention.** When the Tyrnarra canon uses a domain name not on the official PF2e register, treat it as Tyrnarra theological flavour for the god's PF2e-canonical portfolio. Players selecting a cleric of, say, Forseti pick from the PF2e domains Forseti grants (Truth, Secrecy, Star, Glyph). *Arcane Magic* is the in-world name Forseti's clergy use for their work, not a separate domain at character-build time.

### Non-bound granters: all assigned

Every PF2e cleric domain now carries a granter in the registrar; **no domain remains Open / canon-pending** on the non-bound side. The thirteen formerly-pending domains (Abomination, Decay, Destruction, Indulgence, Naga, Nightmares, Pain, Plague, Sorrow, Swarm, Toil, Tyranny, Undeath) were closed across the Vice Demon, Virtue Devil, General-of-Corruption, Betibizi, and Corrupted-God assignment passes; the registrar holds the current grantor for each.

### Source categories and closure status

**All previously-pending domain rows are now closed.** Dragon (Zaharsuge), Moon (Bikiargi · Honokage), Undeath (Betibizi), Swarm (Vermin Queen). Naga is jointly granted by Zaharsuge and the Maw Serpent. Five source-category pills are in use: **Bound 13**, **Vice Demon**, **Non-Bound** (Layer-3 unbound deities: Solyra, Bikiargi, Zaharsuge, Epairima, Betibizi, Odain, and the three Kyūbi-no-Den gods Hahane / Honokage / Yumegatari; Layer-1-tier primordials Suzar, Urzar, Lurzahar, Haizar, Indazar, Hutzar, Iturima, Zurzar, Burdinzar), **General** (surviving Generals of Corruption: Vermin Queen, Rot-Tyrant, Blight-Seer, Flesh-Sculptor, Whisperer in Dreams, Maw Serpent, False Saint, Root-Twister; the Ash-Binder is defeated and grants no current domain), and **Corrupted God** (direct grants from the imprisoned god). The Corrupted God holds direct grants on five domains: **Plague, Abomination, Nothingness, Decay, Destruction**. See the registrar for the full table.

**Kyūbi-no-Den additions.** The three gods of the kitsune ancestral pantheon (Elysium-resident) joined the Non-Bound granters with nine cross-pantheon co-grants: **Hahane** grants *Family · Passion · Indulgence*; **Honokage** grants *Trickery · Magic · Moon*; **Yumegatari** grants *Dreams · Knowledge · Soul*. All nine sit alongside existing Bound 13 / Vice Demon granters of those domains. The pantheon follows the same no-sharing-within-a-pantheon rule as the Bound 13 and Vice Demons: each of the nine domains is granted by exactly one Kyūbi-no-Den god.

---

## Favoured weapons

Per-god favoured weapons in `gods.md`, *The Thirteen: Per-God Sheet*, are both iconography and PF2e cleric mechanical favoured weapons, drawn exclusively from the PF2e **Advanced** weapon category. Araphel's **Sickle-Saber** (curved blade with a secondary grip) is canon both ways.

---

## Ancestries unchanged from PF2e canon

A handful of ancestry entries in `ancestries.md` carry no Tyrnarra-specific reframing; their PF2e default is the canon default. Notable examples: **Gnome**, **Poppet**, **Sprite**. These read as they do in published PF2e material; placement notes in `ancestries.md` capture only their Talan-specific distribution.

---

## Mechanical-rules reference

The world canon does not duplicate PF2e crunch. For mechanical traits, ability scores, feats, languages, hit-die progressions, and other system specifics, refer to the published PF2e Remaster ancestry / heritage / cleric domain entries. Tyrnarra-specific deviations are limited to the placements, renames, and additions noted above.
