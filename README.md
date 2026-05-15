# Tyrnarra

A personal fantasy worldbuilding site, published as a static GitHub Pages site at **https://tyrnarra.kunkel.swiss**.

For setting canon, naming conventions, file layout, and styling rules, see [`CLAUDE.md`](CLAUDE.md).

---

## Local preview

The site uses absolute paths (e.g. `/assets/site-nav.css`), so opening a page directly with `file://` won't work — the browser can't resolve `/assets/...` from the filesystem root. You need a local webserver.

Two helper scripts are included. They use **`live-server`** via `npx`, which auto-opens the browser and refreshes it whenever an HTML/CSS/JS file changes. Requires Node.js (already installed on most modern setups).

**Windows** — double-click `serve.bat`, or run it from a terminal:

```cmd
serve.bat
```

**macOS / Linux / WSL** — run `serve.sh`:

```bash
./serve.sh
```

Either way:

- The site is served at <http://localhost:8000>.
- Your default browser opens automatically.
- Edit any HTML/CSS/JS file → browser refreshes itself.
- Edits to `lore/**` and `.git/**` are ignored (so taking notes doesn't trigger reloads).
- Press `Ctrl+C` in the terminal to stop.

**First run note:** `npx --yes live-server` downloads `live-server` on its first invocation (~25 MB, one time). Subsequent runs start instantly.

### Fallback: Python's built-in server

If Node isn't available, Python's `http.server` works fine — it just doesn't auto-reload:

```bash
python -m http.server 8000   # Windows
python3 -m http.server 8000  # macOS / Linux
```

Run it from the repo root and open <http://localhost:8000>. You'll need to hit `Ctrl+R` after every edit.

---

## Deployment

GitHub Pages deploys automatically on push to `main`. No build step, no GitHub Actions workflow.

- `index.html` at the repo root is the landing page.
- All sub-pages use absolute paths (start with `/`).
- The custom domain is `tyrnarra.kunkel.swiss` (configured via `CNAME`).

To preview a change live, push to `main` and wait ~30 seconds for the Pages build.

---

## Where things live

```
/                                      ← repo root
  index.html                           ← landing page = world primer (cosmology)
  grand-gods.html                   ← the 13 bound gods
  magic.html                           ← Magic & Faith — Four Schools, daily life, faith

  talan/                               ← continent-level content
    talan.html                         ← continent overview
    history.html                       ← eras / timeline
    domains/<slug>/<slug>.html         ← one folder per god domain
    factions/                          ← independent organisations

  assets/                              ← shared chrome (sidebar nav, base CSS)
    site-nav.css
    site-nav.js                        ← single source of truth for menu structure
    style-a.css                        ← world-level pages (landing, gods, magic)
    style-b.css                        ← /talan/ pages

  lore/                                ← markdown reference notes (NOT published)
    world-notes.md                     ← authoritative canon
    geography.md
    factions.md
    glossary.md
    timeline.md
    site-inventory.md
    restructure-plan.md
    sidebar-nav.md

  CLAUDE.md                            ← project conventions + naming rule
  README.md                            ← this file
  CNAME
  serve.bat / serve.sh                 ← local dev server helpers
```

For the full conventions (naming rule, folder l