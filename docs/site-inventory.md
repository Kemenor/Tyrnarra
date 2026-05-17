# Site Inventory — Current State

Live at **https://tyrnarra.kunkel.swiss** · Auto-deploys on push to `main` · No build step.

Last updated **2026-05-17**. For repo conventions and folder layout, see [`../CLAUDE.md`](../CLAUDE.md). For sidebar architecture, see [sidebar-nav.md](sidebar-nav.md).

---

## Page Tree — Publish Status

```
/                              [Style A · cosmic]
  index.html                   landing = world primer (cosmology)                POPULATED
  grand-gods.html              the 13 bound gods (data-driven, expandable)       POPULATED
  magic.html                   Magic & Faith — Four Schools / Magitech / Daily Life /
                               Mortal Ascent Ladder + GM Secret / Faith / Domains-Outside-13
                               REWRITE (2026-05-17 Tier 3 step 6)

/talan/                        [Style B · grounded]
  talan.html                   continent overview, three seas, 13 domain cards   POPULATED
                               + Continental Rail Network + Other Continents     (UPDATED 2026-05-17 Tier 3 step 7)
  history.html                 8 eras with three-tier knowledge UI               POPULATED
                               + Gods' Era three-tier expandables (Old Race + Storveldi)
                               + Week of Crimson Rain secret harmonised
                               + Dark Era amber Popular Belief (Sage Lorant
                                 Age-of-Corruption chronicle + calendar-conflation note)
                                                                                 (UPDATED 2026-05-17)
  the-binding.html             Wardstones + Nine Generals + War of Seals         POPULATED  (NEW 2026-05-16; GM Secret + General domain-grants added 2026-05-17)
                               + Vermin Queen card now links to dedicated
                               Hollow page                                        (UPDATED 2026-05-17)
  the-binding/hollow-of-ten-thousand-threads.html
                               Hollow of Ten Thousand Threads · The Vermin
                               Queen's Hive — first dedicated Nine-Dungeons page.
                               Sickly-olive accent. Four-card chamber geography
                               (Web-Tunnels / Brood Pits / Silken Vaults /
                               Throne); three red-bordered threat cards
                               (Endless Swarms / Corrupted Silk / Hive-Mind
                               Influence); Vermin Queen section with Swarm-
                               domain grant; blue Surki Counter callout (kin-
                               gone-wrong framing); two seal-blocks for War-
                               of-Seals context (2524 eruption + standing-threat
                               margin-pay callout); Open in Canon panel        POPULATED  (NEW 2026-05-17)
  bestiary.html                Peoples &amp; Heritages — distribution table, 13 domain cards,
                               Sortalde pointer, versatile heritages, virtue demons,
                               sin devils                                        POPULATED  (NEW 2026-05-17 Tier 4 step 10)

Tier 1 publishing pass — 2026-05-17:
  grand-gods.html              Vesuna +Free Will, Hinka +Violent Death extra cleric domains
  brauogi.html                 Minotaur added as 3rd dominant ancestry + Magitrain southern-network note
  lautara.html                 Emarrea card now links to its page; Crossroads sub-region card added; Magitrain hub + Sortalde embassies note
  lioaru.html                  Lost Kingdom expanded (Blackened Lands, Skeleton/Fleshwarp origin); Storveldi/Betibizi GM Secret expandable; Magitrain limits note
  sumendar.html                Order of Steam reframed as Magitech industrial heart (Elden-tech origin, House Eisenhart); Dragon's Reach two-recovery-projects friction; Magitech + Magitrain notes

/talan/domains/                13 domain pages — etymology, facts, character pills,
                               god's city, sub-region cards
  vindul/vindul.html           POPULATED      lautara/lautara.html     POPULATED
  myrkono/myrkono.html         POPULATED      floteyn/floteyn.html     POPULATED
                                              + Balaena Skywhale City featured section
                                              (4 info-cards + amber Popular Belief on
                                              the captivity truth)                  (UPDATED 2026-05-17)
  sumendar/sumendar.html       POPULATED      lioaru/lioaru.html       POPULATED
  brauogi/brauogi.html         POPULATED      ezkudon/ezkudon.html     POPULATED
  egulon/egulon.html           POPULATED      zuzental/zuzental.html   POPULATED
  nashavel/nashavel.html       POPULATED      ehizahar/ehizahar.html   POPULATED
  askamira/askamira.html       POPULATED

/talan/domains/<domain>/       Promoted sub-region & settlement pages
  ehizahar/fenurra.html        Fenurra · the Flame-Source                        POPULATED  (NEW 2026-05-16)
  lautara/emarrea.html         Emarrea · the Kitsune Kingdom                     POPULATED  (NEW 2026-05-16)
  lautara/crossroads.html      Crossroads · Tri-Domain Nexus + Spider's Silk Inn POPULATED  (NEW 2026-05-17)
  lioaru/lost-kingdom.html     Lost Kingdom · The Blackened Lands                POPULATED  (NEW 2026-05-17;
                               + Meat-on-a-Stick amber Popular Belief
                               (Storveldi cannibalism folk-trope)                 UPDATED 2026-05-17)
  myrkono/myrria/myrria.html   Myrria · City of Second Chances                   POPULATED  (NEW 2026-05-16;
                               + Faith of Many Faces section — three rites, sacred
                               iconography callout, edicts/anathema                UPDATED 2026-05-17)
  sumendar/order-of-steam/order-of-steam.html
                               Order of Steam · Industrial Kingdom-Guild Hybrid  POPULATED  (NEW 2026-05-17)
  sumendar/dragons-reach.html  Dragon's Reach · Dragon Capital — the city built
                               from the mid-Gods'-Era mothership wreckage;
                               three-tier lifespan band (non-purist / purist /
                               "the purest"); four purist-school cards; two-
                               sided purist-vs-pragmatist position blocks on
                               the age-weighted vote tension; Order-of-Steam
                               friction + Dragonet older-claim schism; amber
                               Popular Belief on the buried-alien-truth        POPULATED  (NEW 2026-05-17)
  sumendar/order-of-steam/house-eisenhart.html
                               House Eisenhart · Highforge Lineage + Stahlglanz  POPULATED  (NEW 2026-05-17)
  zuzental/thousand-kingdom.html
                               Thousand Kingdom · Forseti's Realm of Law — the
                               dual-bloodline (elf long-horizon / human short-
                               horizon) constitutional kingdom that holds
                               Lograth and the inseparable god-city/capital
                               fusion; four-card borderlands compass             POPULATED  (NEW 2026-05-17)
                               + Founding & History section with three-tier
                               UI: Demon-Demigod conquest of the warring
                               Thousand, adventurer-Queen of the Old King's
                               forged blood, the binding compact; amber Old-
                               King-myth folkloric layer; red GM Secret on the
                               Queen-knew-the-truth twist                        (UPDATED 2026-05-17)
  zuzental/emerald-isles.html  Emerald Isles · Three Main Isles + Bridgelands    POPULATED  (NEW 2026-05-17 Tier 4 pair w/ Sortalde)
  zuzental/legea-empire.html   Legea Empire · Demigod Theocracy of the Divine
                               Faith — at-a-glance with visible TBDs, two-sided
                               law-vs-law tension blocks (Faith vs Forseti
                               positions), missionary programme + Draconis
                               marriage, "Open in Canon" panel listing the 6
                               TBDs as deliberate state                          POPULATED  (NEW 2026-05-17)

/talan/factions/
  factions.html                taxonomy overview + 4 cards                       POPULATED
                               + Bandit Categories & Hazards (Train Pirates +
                               Conductor's Station)                              (UPDATED 2026-05-17)
  adventurers-guild.html       FULL REWRITE (2026-05-17) — branch hierarchy, rank ladder, Bank, Post, Lavisburg, Seraphel, Godshall
  mercenary-guild.html         POPULATED
  god-churches.html            POPULATED      remnants.html            POPULATED

/off-continent/                NEW top-level section (2026-05-17) — non-Talan continents & powers
  red-empire.html              The Red Empire — godless mortal-supremacist state POPULATED  (NEW 2026-05-17)
  sortalde.html                Sortalde · Tao Hua Yuan · The Petal Continent     POPULATED  (NEW 2026-05-17 Tier 4)
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
- `/talan/history.html` — **Elden Era**, **Gods' Era**, and **Week of Crimson Rain** have all three tiers (Gods' Era added 2026-05-17). The remaining 5 eras have only common-knowledge text.
- `/talan/the-binding.html` — GM Secret expandable (Corrupted God = Elden + four General domain-grants).
- `/talan/domains/lioaru/lioaru.html` — GM Secret (Storveldi/Betibizi/Lost Kingdom truth).
- `/talan/domains/lioaru/lost-kingdom.html` — four amber Popular Belief expandables + comprehensive GM Secret.
- `/talan/domains/floteyn/floteyn.html` — one amber Popular Belief expandable (Balaena's captivity).
- `/talan/domains/zuzental/thousand-kingdom.html` — full three-tier on the founding: plain prose + amber Popular Belief (Old King myth) + red GM Secret (Demigod's tragic motive + forged Queen lineage + the throne-held truth).
- `/talan/domains/sumendar/dragons-reach.html` — one amber Popular Belief expandable (most Talanese don't know Dragons are alien — truth is findable, not GM-secret).
- `/talan/domains/lautara/crossroads.html` — four amber tavern-rumour expandables.
- `/magic.html` — GM Secret on the Mortal Ascent Ladder (integration-procedure / Storveldi / Betibizi).

---

This file is a **description of what is published**, not a TODO list. For forward work — what needs writing, fleshing out, or publishing next — see [`open-threads.md`](open-threads.md).
