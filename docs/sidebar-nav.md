# Sidebar Navigation — Architecture

How the persistent sidebar on every page is built and how to extend it.

---

## How it works

- The sidebar structure lives in `/assets/site-nav.js`. Two data sources drive it:
  - **`DOMAINS`** — the array of 13 god-domains. Each entry has a `slug`, `label`, `href`, and a `children` list of nested sub-region/settlement pages.
  - **The top-level section markup** (World & Cosmos, Talan section, Factions) — string literals inside `buildNavHtml()`.
- The sidebar styling lives in `/assets/site-nav.css`.
- Every page references both via two tags in `<head>`:

  ```html
  <link rel="stylesheet" href="/assets/site-nav.css">
  <script defer src="/assets/site-nav.js"></script>
  ```

- On `DOMContentLoaded`, the script builds the sidebar markup from the data arrays, injects it as the first child of `<body>`, then wires up the toggle button, the scrim, the Escape-key handler, the `.is-current` highlight, and the accordion chevrons.

The page tells the sidebar which entry to highlight with:

```html
<body data-page="vindul">
```

If the page isn't in the sidebar (e.g. a settlement or sub-region page), just omit `data-page` or use any value — no match is found and nothing breaks.

---

## How `data-page` works

- The JS reads `document.body.getAttribute('data-page')`.
- It finds the matching link in the sidebar via `a[data-page="..."]`.
- Adds `.is-current` to highlight it.

The slug doesn't have to match the filename — it just has to match between the page's `<body data-page="...">` and a sidebar link's `data-page="..."` attribute.

---

## How to extend the nav

**To add a new top-level page** (a new continent-level reference, a new faction, etc.):

1. Open `/assets/site-nav.js`.
2. Inside `buildNavHtml()`, find the matching top-level section's string array (World &amp; Cosmos, Talan, or Factions).
3. Add a `<li>` line with a unique `data-page="<slug>"`.
4. On the new HTML page, set `<body data-page="<slug>">`.

**To add a sub-region or settlement under a domain** (nested accordion entry):

1. Open `/assets/site-nav.js`.
2. Find the matching entry in the `DOMAINS` array.
3. Push a child object `{ slug, label, href }` into its `children` array.
4. On the new HTML page, set `<body data-page="<slug>">` matching the child's slug.

The accordion will:
- Show a chevron `▸` next to any domain whose `children` array is non-empty (and no chevron for domains with empty children).
- Auto-expand the domain when the current page is either **that domain itself** or one of its **nested children**. So visiting Myrria auto-opens the Myrkono submenu; visiting the Myrkono domain page also auto-opens it (so the chevron isn't required to discover what's underneath).
- Toggle open/closed on chevron click. The domain name itself stays a normal link — clicking it navigates to the domain page rather than expanding.

One file edited. No find-and-replace across pages.

---

## Mobile + accessibility

- The sidebar slides in from the left on toggle click, covers the page with a scrim, and closes on Escape, scrim click, or another toggle click.
- On mobile (`max-width: 600px`) the sidebar occupies 86% of viewport width.
- Body content does **not** shift when the sidebar opens — the sidebar overlays the page. This avoids rewriting every existing page's layout.

---

## Scope

The sidebar carries:
- **Top-level world-and-Talan structure** — World & Cosmos, Talan-level pages (Overview, History, The Binding), Factions.
- **The 13 Domains**, each with an optional nested list of promoted sub-region and settlement pages (accordion, click-to-expand).

To avoid sidebar bloat, only **promoted** sub-regions get a sidebar entry. A sub-region is "promoted" when it has its own HTML page (e.g. Fenurra, Emarrea, Myrria). Sub-regions and settlements that exist only as cards or sections on a domain page are not in the sidebar — visitors reach them via the parent domain page.
