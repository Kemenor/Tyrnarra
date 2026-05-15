# Sidebar Navigation — Architecture

**This file is now mostly historical.** The sidebar is no longer pasted into every page. Instead:

- The sidebar markup lives in `/assets/site-nav.js` (in the `NAV_HTML` array near the top).
- The sidebar styling lives in `/assets/site-nav.css`.
- Every page references both via two tags in `<head>`:

  ```html
  <link rel="stylesheet" href="/assets/site-nav.css">
  <script defer src="/assets/site-nav.js"></script>
  ```

- The page tells the sidebar which entry to highlight with:

  ```html
  <body data-page="vindul">
  ```

---

## How to extend the nav

**To add a new top-level page** (a new domain, a new faction, a new world reference):

1. Open `/assets/site-nav.js`.
2. Add a `<li>` to the matching `nav-section` inside the `NAV_HTML` array.
3. Use a unique `data-page="<slug>"`.
4. On the new HTML page, set `<body data-page="<slug>">`.

That's it. One file edited. No find-and-replace across 26 pages.

## How `data-page` works

- The JS reads `document.body.getAttribute('data-page')`.
- It finds the matching link in the sidebar via `a[data-page="..."]`.
- Adds `.is-current` to highlight it.
- If the page isn't in the nav (e.g. a settlement or sub-region page), no match is found and nothing breaks.

## Mobile + accessibility

- The sidebar slides in from the left on click, covers the page with a scrim, and closes on Escape, scrim click, or toggle click.
- On mobile (`max-width: 600px`) the sidebar occupies 86% of viewport width.
- Body content does **not** shift when the sidebar opens — the sidebar overlays the page. This was chosen to avoid rewriting every existing page's layout.

## Scope

The sidebar carries only top-level structure (World & Cosmos, Talan, Domains, Factions). Settlement pages and sub-region pages are accessed from their parent domain page, not from the sidebar, to avoid bloat.
