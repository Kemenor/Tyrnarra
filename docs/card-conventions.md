# Card Conventions

How cards behave on the site. Read this before adding a new card type or making a card clickable.

The site uses cards heavily (domain cards, sub-region cards, ancestry cards, continent cards, god cards, the Nine Generals cards on the-binding.html, the historical-civilisation hub cards, etc.). They split into three camps: **plain**, **clickable** (navigates to another page), and **expandable** (reveals more content in place). Each camp has a strict convention so the affordance reads the same everywhere on the site.

---

## The rules

> **If a card links somewhere, the entire card is the link, and the card's title ends with ` →`.**
>
> **If a card expands in place, it carries a `Tap ▾` pill in its header.**
>
> If a card does neither, it is a `<div>` with no arrow, no pill, no hover-lift.

All three conventions are non-negotiable for new cards. Mixed-state cards (links inside an otherwise-plain card body) are not allowed: see *Inner anchors* below.

---

## Clickable card pattern

```html
<a class="accent-card outlined thin <card-flavour-class> is-link"
   href="/destination/path.html"
   style="--card-accent: #colour;">
  <div class="<flavour>-title">Card Title →</div>
  <div class="<flavour>-body">
    Body content. Plain prose, <b>bold</b>, <i>italic</i> allowed.
    No inline anchors.
  </div>
</a>
```

What this gets you, from the shared rules in [`/assets/style-b.css`](../assets/style-b.css) (`a.accent-card`, `.accent-card.is-link`, `.accent-card.is-link:hover`):

- `cursor: pointer` over the whole card surface.
- `color: inherit; text-decoration: none;` so the body prose looks like card content, not a link.
- On hover: `transform: translateY(-2px)` to lift the card.
- Per-card accent stripe via `--card-accent` is preserved on hover (don't override `border-color` in the hover rule on a card-flavour selector, which erases the stripe; see *Pitfalls* below).

The title's trailing `→` is part of the text content, not a CSS pseudo-element. Put it in the HTML so screen readers announce it.

### Reference implementations

- **Sub-region cards on sumendar.html** ([`/talan/domains/sumendar/sumendar.html`](../talan/domains/sumendar/sumendar.html)): *Order of Steam →* and *Dragon's Reach →* use the canonical `<a class="subregion-card">` pattern. Other sub-regions on the same page are non-clickable `<div class="subregion-card">` because they have no dedicated page yet. This is the strictest model: the same hub displays both states side-by-side cleanly.
- **Domain cards on talan.html** ([`/talan/talan.html`](../talan/talan.html)): 13 `<a class="domain-card">` cards, one per god domain.
- **Ancestry cards on ancestries.html** ([`/talan/ancestries.html`](../talan/ancestries.html)): 13 `<a class="accent-card ... ancestry-card is-link">` cards.
- **Historical civilisation cards on historical.html** ([`/talan/historical/historical.html`](../talan/historical/historical.html)): three `<a class="subregion-card">` cards (Golden Empire, Storveldi Denbora, Elden).
- **Continent cards on talan.html** Other Continents section: Sortalde and the Red Empire continent are `<a class="accent-card framed is-link continent-card">`; the *Unmapped* placeholder is a plain `<div>`.
- **The Vermin Queen card on the-binding.html** ([`/talan/the-binding.html`](../talan/the-binding.html)): the only General with a sited dungeon page, so the only one of nine that's clickable. Pattern: `<a class="accent-card framed general-card is-link">` linking to the Hollow.

---

## Expandable card pattern

For cards that reveal more content in place when clicked (rather than navigating to another page), use the `expand-hint` pill in the card's header row:

```html
<div class="<flavour>-card" onclick="toggleCard(event, this)">
  <div class="card-top">
    <!-- title, subtitle, etc. -->
    <div class="expand-hint">Tap ▾</div>
  </div>
  <div class="card-summary">Always-visible summary text.</div>
  <div class="card-expanded">
    <!-- revealed content -->
  </div>
</div>
```

Styling (from [`/assets/style-a.css`](../assets/style-a.css) `.expand-hint`):

- Small Cinzel uppercase text in a thin gold-bordered pill.
- Brightens on card hover.
- Hidden once the card is in the expanded state (`.<card>.expanded .expand-hint { display: none }`).

The pill is the universal affordance for *click me to reveal more*. Don't replace it with a chevron-only or text-only variant; the bordered pill is what makes it visible against the moody Style-A background.

### Reference implementations

- **God cards on grand-gods.html** ([`/grand-gods.html`](../grand-gods.html)): each of the 13 gods. The pill sits in the top-right of the card header alongside the orb and title block, and disappears when the card is expanded.

### When to use the expand pill

- The card has a default-collapsed body that opens in place. Use the pill.
- The card is a button-style toggle (the `.legend-era-toggle` / `.secret-era-toggle` ◈ / ⚿ buttons on history.html and the rest of Style B): the glyph + label already carry the affordance, no pill needed.
- The card navigates instead of expanding: use the ` →` arrow in the title, not the pill.

---

## Plain (non-clickable) card pattern

```html
<div class="accent-card outlined thin <card-flavour-class>"
     style="--card-accent: #colour;">
  <div class="<flavour>-title">Card Title</div>
  <div class="<flavour>-body">
    Body content. Inline links inside body prose are allowed.
  </div>
</div>
```

No `→`, no `is-link`, no hover transform. Inline anchors are permitted in a plain card's body because the card itself isn't competing for the click.

---

## Inner anchors inside clickable cards

**Forbidden by HTML and by convention.** Nested `<a>` tags are invalid HTML (browsers split or drop them), and even if they rendered, the mixed-affordance card creates a usability mess: most of the card goes to destination A, small inline regions go to destination B, and a reader can't tell where they're about to click.

When a clickable card's body would naturally cross-reference another page, **drop the inline anchor and use plain `<b>`**. The destination is usually reachable through the card's main link anyway (e.g. the Myrkono ancestry-card links to the Myrkono domain page, which itself links to Myrria, so dropping the inline *Myrria* link costs one extra click).

### History note: the CSS-pseudo trick

It is technically possible to keep inner anchors clickable while making the whole card clickable, using a `::before` pseudo-element on the title's anchor with `position: absolute; inset: 0` to cover the card, plus `pointer-events: none` on the body and `pointer-events: auto` on inner anchors to re-enable them. This was tried once on ancestries.html and reverted. Reasons:

- Mixed-affordance card is confusing visually and for screen readers.
- Touch hit-targets crowd: most of the card goes to A, narrow inline strips go to B; mis-taps on mobile.
- The mechanism is non-obvious to anyone editing the page later (silent `pointer-events: none` is easy to break).

**Don't use the pseudo trick.** Use the plain `<a>`-wrap and accept the plain-`<b>` substitution for inner cross-references.

---

## Pitfalls

### Don't override `border-color` in hover

`.accent-card` sets the left accent stripe via `border-left: 4px solid var(--card-accent, ...)`. A hover rule that says `border-color: <some gold>` will erase the per-card accent stripe (changing all four borders, including the left). If you want a hover indicator beyond the lift, change the `background` or use a `box-shadow` rather than `border-color`.

### Don't forget to copy the `style="--card-accent:..."` when changing the wrapper

If you're converting a non-clickable card to clickable, the per-card accent colour lives on the outer wrapper. Move the `style="--card-accent: #..."` attribute with the wrapper as you change `<div>` to `<a>`.

### Don't add a redundant *Page →* tag pill

Earlier patterns sometimes used `<span class="subregion-tag">Page →</span>` in the tags row of clickable cards. The `→` in the title carries the affordance; the tag duplicates it and clutters the tag row. Drop those pills when you find them. (Done for the three historical hub cards.)

### `<a>` cannot contain block-level interactive content

Buttons, form inputs, summary/details, and nested anchors are forbidden inside `<a>`. Plain prose, `<b>`, `<i>`, `<span>`, `<br>`, and block-level `<div>`/`<p>` content are fine.

---

## When to add a new clickable card

- The destination page exists and is published.
- The card meaningfully represents a navigable thing (domain, sub-region, settlement, faction, civilisation, ancestry-group, etc.). Cards that represent abstract concepts or status states usually stay plain.
- The full destination page would naturally be the next click for a reader interested in this card.

If the destination is unwritten, leave the card as `<div>`. Promote it to `<a>` the same day you publish the destination page. (See [`open-threads.md`](open-threads.md) for the rolling promotion-pattern across sub-regions, god city-states, and god churches.)

---

## Audit checklist for new pages

Before shipping a page with cards:

1. Every `<a class="...card...">` ends its title with ` →`.
2. Every expandable card carries a `Tap ▾` pill (`.expand-hint`) in its header row.
3. No `<a>` tag appears inside any other `<a>` tag.
4. Every clickable card uses `is-link` (or `a.accent-card`, which has the same display-block reset).
5. Plain `<div class="...card...">` cards have no `→`, no pill, and no `is-link`.
6. Per-card `--card-accent` accent stripe survives hover (test by hovering; the left stripe should not change colour).
