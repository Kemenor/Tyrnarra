# Sidebar Navigation — Architecture

How the persistent sidebar on every page is built and how to extend it.

---

## How it works

- The sidebar markup lives in `/assets/site-nav.js` (the `NAV_HTML` array near the top).
- The sidebar styling lives in `/assets/site-nav.css`.
- Every page references both via two tags in `<head>`:

  ```html
  <link rel="stylesheet" href="/assets/site-nav.css">
  <script defer src="/assets/site-nav.js"></script>
  ```

- On `DOMContentLoaded`, the script injects the sidebar markup as the first child of `<body>`, then wires up the toggle button, the scrim, the Escape-key handler, and the "is-current" highlight.

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

**To add a new top-level page** (a new domain, a new faction, a new world reference):

1. Open `/assets/site-nav.js`.
2. Add a `<li>` to the matching `nav-section` inside the `NAV_HTML` array.
3. Use a unique `data-page="<slug>"`.
4. On the new HTML page, set `<body data-page="<slug>">`.

That's it. One file edited. No find-and-replace across pages.

---

## Mobile + accessibility

- The sidebar slides in from the left on toggle click, covers the page with a scrim, and closes on Escape, scrim click, or another toggle click.
- On mobile (`max-width: 600px`) the sidebar occupies 86% of viewport width.
- Body content does **not** shift when the sidebar opens — the sidebar overlays the page. This avoids rewriting every existing page's layout.

---

## Scope

The sidebar carries only top-level structure — World & Cosmos, Talan, Domains, Factions. Settlement pages and sub-region pages are accessed from their parent domain page, not from the sidebar, to avoid bloat.
