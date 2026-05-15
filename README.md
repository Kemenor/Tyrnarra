# Tyrnarra

A personal fantasy worldbuilding site, published as a static GitHub Pages site at **https://tyrnarra.kunkel.swiss**.

For project conventions (naming rule, folder layout, style guide) see [`CLAUDE.md`](CLAUDE.md). For what's currently published vs. stub, see [`docs/site-inventory.md`](docs/site-inventory.md).

---

## Local preview

The site uses absolute paths (e.g. `/assets/site-nav.css`), so opening a page directly with `file://` won't work — the browser can't resolve `/assets/...` from the filesystem root. You need a local webserver.

Two helper scripts are included. They use **`live-server`** via `npx`, which auto-opens the browser and refreshes it whenever an HTML/CSS/JS file changes. Requires Node.js.

**Windows** — double-click `serve.bat`, or run it from a terminal:

```cmd
serve.bat
```

**macOS / Linux / WSL** — run `./serve.sh`.

Either way:

- The site is served at <http://localhost:8000>.
- Your default browser opens automatically.
- Edit any HTML/CSS/JS file → browser refreshes itself.
- Edits to `lore/**`, `docs/**`, and `.git/**` are ignored (so taking notes doesn't trigger reloads).
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

- `index.html` at the repo root is the landing page (the cosmology primer).
- All sub-pages use absolute paths (start with `/`).
- The custom domain is `tyrnarra.kunkel.swiss` (configured via `CNAME`).

To preview a change live, push to `main` and wait ~30 seconds for the Pages build.

---

## Where things live (quick orientation)

- **HTML pages**: root for world-level (`index.html`, `grand-gods.html`, `magic.html`); `/talan/` for continent-level; `/talan/domains/<slug>/` for the 13 god domains; `/talan/factions/` for independent organisations.
- **Shared CSS + sidebar nav**: `/assets/` (loaded by every page).
- **Worldbuilding canon** (not published): `/lore/` — five markdown files of authoritative world notes.
- **Site documentation** (not published): `/docs/` — site-inventory.md (status) and sidebar-nav.md (architecture).

For the full folder tree, layer-to-folder mapping, and conventions, see [`CLAUDE.md`](CLAUDE.md).
