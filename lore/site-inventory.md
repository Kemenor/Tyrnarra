# Site Inventory — Current State

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

---

## Pages

### `index.html` — Landing Page
- Style A (cosmic)
- Two sections: **World & Cosmos** (3 cards) and **Settlements** (1 card)
- Links to: `tyrnarra-primer.html`, `tyrnarra-gods.html`, `talan-primer.html`, `millhaven/millhaven.html`
- Flavor text: *"A continent of bound gods and merchant councils, of cloudships that cross the white expanse and rivers that remember more than they should."*

---

### `tyrnarra-primer.html` — World Cosmology
- Style A (cosmic, animated starfield)
- Covers: the Wellspring, three-layer cosmology (Prelife / Life Layer / Postlife), the Cloud Sea, Solyra & the two moons (Veyru, Calune), the 13 Bound Gods grid (summary only), planar travel note
- Notable: interactive planar diagram, god-grid with color-coded domains

---

### `tyrnarra-gods.html` — The 13 Bound Gods
- Style A (cosmic)
- One expandable card per god; cards grouped by Primordial Six / Ascendant Six / Life Layer (Cronus alone)
- Each card: domain, region, nature summary, public detail, and a red **⚿ GM Secret** expandable section
- Three-tier knowledge system implemented: public text is common knowledge; secret sections are GM-only
- Cronus's secret (mortal ascension, shard mechanic) is the most developed secret entry

---

### `talan-primer.html` — The Continent
- Style B (grounded, tabbed layout)
- Four tabs:
  - **History** — eight eras (Creation → Adventurer Era) with three-tier knowledge system partially implemented; Elden Era and Week of Crimson Rain have all three tiers (common / amber Popular Belief / red GM Secret); other eras have common knowledge text only
  - **Regions** — 13 expandable region cards (one per god domain), each with type, notable places, character description, and pills
  - **Factions** — 6 faction entries (Adventurers Guild, 13 Bound Gods, Order of Steam, Legea Empire, Nanuu Republic, Remnants of Corruption)
  - **Magic** — Four Schools section (Arcane / Occult / Primal / Divine) at top; "Magic in Daily Life" section below

---

## Missing / Broken

- **`millhaven/millhaven.html`** — linked from `index.html` but the folder was removed. Link is currently broken. Millhaven is to be re-added later.

---

## Visual Styles in Use

| Style | Used on | Key fonts |
|---|---|---|
| A — Cosmic | `index.html`, `tyrnarra-primer.html`, `tyrnarra-gods.html` | Cormorant Garamond, Cormorant SC, IM Fell English |
| B — Grounded | `talan-primer.html` (and future settlement pages) | Libre Baskerville, Philosopher, Josefin Sans |

---

## Three-Tier Knowledge System (current implementation)

Used in `talan-primer.html` (History tab) and `tyrnarra-gods.html` (god secrets):

- **Plain text** — common knowledge, no interaction needed
- **Amber ◈ pill** — "Popular Belief" expandable, `toggleEraLegend()` / amber color scheme
- **Red ⚿ pill** — "GM Secret" expandable, `toggleEraSecret()` / `toggleSecret()` / red color scheme

Partially applied to history eras — only Elden Era and Week of Crimson Rain have all three tiers. To do: Gods' Era, Lost Era, Golden Era, Dark Era, Adventurer Era.
