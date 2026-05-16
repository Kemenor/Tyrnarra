# Site Inventory — Current State

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

Last updated **2026-05-16**. For repo conventions and folder layout, see [`../CLAUDE.md`](../CLAUDE.md). For sidebar architecture, see [sidebar-nav.md](sidebar-nav.md).

---

## Page Tree — Publish Status

```
/                              [Style A · cosmic]
  index.html                   landing = world primer (cosmology)                POPULATED
  grand-gods.html              the 13 bound gods (data-driven, expandable)       POPULATED
  magic.html                   Magic & Faith — Four Schools / Daily Life / Faith POPULATED

/talan/                        [Style B · grounded]
  talan.html                   continent overview, three seas, 13 domain cards   POPULATED
  history.html                 8 eras with three-tier knowledge UI               POPULATED
  the-binding.html             Wardstones + Nine Generals + War of Seals         POPULATED  (NEW 2026-05-16)

/talan/domains/                13 domain pages — etymology, facts, character pills,
                               god's city, sub-region cards
  vindul/vindul.html           POPULATED      lautara/lautara.html     POPULATED
  myrkono/myrkono.html         POPULATED      floteyn/floteyn.html     POPULATED
  sumendar/sumendar.html       POPULATED      lioaru/lioaru.html       POPULATED
  brauogi/brauogi.html         POPULATED      ezkudon/ezkudon.html     POPULATED
  egulon/egulon.html           POPULATED      zuzental/zuzental.html   POPULATED
  nashavel/nashavel.html       POPULATED      ehizahar/ehizahar.html   POPULATED
  askamira/askamira.html       POPULATED

/talan/domains/<domain>/       Promoted sub-region & settlement pages
  ehizahar/fenurra.html        Fenurra · the Flame-Source                        POPULATED  (NEW 2026-05-16)
  lautara/emarrea.html         Emarrea · the Kitsune Kingdom                     POPULATED  (NEW 2026-05-16)
  myrkono/myrria/myrria.html   Myrria · City of Second Chances                   POPULATED  (NEW 2026-05-16)

/talan/factions/
  factions.html                taxonomy overview + 4 cards                       POPULATED
  adventurers-guild.html       POPULATED      mercenary-guild.html     POPULATED
  god-churches.html            POPULATED      remnants.html            POPULATED
```

Removed in earlier phases: `talan-primer.html`, `tyrnarra-primer.html`, `tyrnarra-gods.html` (renamed to `grand-gods.html`), `/talan/magic.html` (moved to `/magic.html`).

---

## Cross-Links Between Pages

- Each god card on `grand-gods.html` has a **"Visit [Domain Name] →"** link in its expanded view, pointing to the matching `/talan/domains/<slug>/<slug>.html`. When god city-states get their own pages later, a second link will go there.
- The landing page's portal cards link out to the gods, magic, Talan, and history pages.
- Each domain page breadcrumbs back to `/talan/talan.html` and `/index.html`.

---

## Three-Tier Knowledge System — Inventory

The site uses three layers of revealability for setting information:

- **Plain text** — common knowledge, no interaction.
- **Amber ◈ pill** — "Popular Belief", expandable. `.legend-era-toggle` / `.legend-era-content` (Style B / history page).
- **Red ⚿ pill** — "GM Secret", expandable. `.secret-toggle` / `.secret-content` (gods page) or `.secret-era-toggle` (history page).

Currently used in:
- `grand-gods.html` — all 13 gods have at least the red GM Secret tier (Cronus's is fully written; others have placeholder text).
- `/talan/history.html` — Elden Era and Week of Crimson Rain have all three tiers. The remaining 6 eras have only common-knowledge text.

---

## Future Work

- **Settlements**: reintroduce Millhaven under `/talan/domains/brauogi/millhaven/millhaven.html`.
- **Sub-region promotion (remaining major)**: Thousand Kingdom, Order of Steam, Lost Kingdom, Dragon's Reach, River Duchies. The pattern is now established by Fenurra / Emarrea / Myrria.
- **Other god city-state pages**: Myrria's pattern (folder under domain, settlement page named after the folder) can be replicated for Haizava, Merkavar, Uravel, Eldara, Denbora, Lurrath, Thekkavar, Ljosarn, Lograth, Nahaskel, Veidrath, Frae City as their content matures.
- **Myrria sub-pages**: Myrria's Godshall (Adventurers' Guild facility) and Seraphel Duskbane (Guild Sovereign of Myrkono) — both flagged as stubs from the Myrria city page and currently held in `lore/factions.md`. Promote when Phase 3 of the WA migration runs.
- **The other six Wardstones**: their host cities (Lakeside, Steppes, Forest, Temple, Monastery, Port) currently lack names — once named, each can become its own settlement page linked from the-binding.html.
- **The eight remaining Nine Generals' dungeons**: only the Vermin Queen's Hollow of Ten Thousand Threads is sited. The other seven need placement before they can earn their own dungeon pages.
- **Three-tier UI on remaining eras**: extend the amber Popular Belief / red GM Secret expandables to Gods', Lost, Golden, Dark, Adventurer eras as content gets written.
- **Per-god GM Secrets**: fill out the 12 placeholder secrets on `grand-gods.html` (Cronus is done).
- **Legea Empire page**: the Zuzental sub-region housing the Divine Faith demigod theocracy — pending the deity-name / demigod-name / prince-name calls.
