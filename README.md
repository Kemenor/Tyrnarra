# Tyrnarra

A personal fantasy worldbuilding site, published as a static GitHub Pages site at **https://tyrnarra.kunkel.swiss**.

For project conventions (naming rule, folder layout, style guide) see [`CLAUDE.md`](CLAUDE.md). For what's currently published vs. stub, see [`docs/site-inventory.md`](docs/site-inventory.md).

---

## Repo shape

Everything that ships to the web lives under **`/published/`**; everything else in the repo is private and never served.

GitHub Pages serves `/published/` *as the site root*, so `/published/setting/talan/x.html` is live at `/setting/talan/x.html` — the `/published/` prefix is stripped at deploy and never appears in a link.

- **`/published/`** — the deploy artifact (served as root).
  - **`setting/`** — the worldbuilding site (served at `/setting/…`): `index.html` (the cosmology/world-primer homepage) + `cosmology/` (world-level Style A pages) + `talan/` (the continent) + `off-continent/` + `assets/` (shared chrome).
  - **`gm-notes/`** — GM / table material (served at `/gm-notes/`, unlinked from the player nav). Keeps the in-browser `tools/map-area-editor.html`.
  - **`player-campaigns/`** — the player companion (served at `/player-campaigns/`).
  - `index.html` (root redirect → `/setting/`), `CNAME`, `robots.txt`, `favicon*`, `site.webmanifest`.
- **`/tools/`** — private GM build tooling, **not served**: `encounterBuilder/`, `foundryExport/`, `map-library/`, `token-frames/`.
- **`/lore/`**, **`/docs/`** — private canon + site docs, **not served**.

---

## Local preview

The site uses absolute paths (e.g. `/setting/assets/site-nav.css`), so opening a page with `file://` won't work; you need a local webserver that serves **`published/` as the root** (matching production).

Two helper scripts do exactly that via **`live-server`** (npx; auto-opens the browser and live-reloads on HTML/CSS/JS changes). Requires Node.js.

**Windows**: double-click `serve.bat`, or run it from a terminal:

```cmd
serve.bat
```

**macOS / Linux / WSL**: run `./serve.sh`.

Both serve the `published/` folder as the site root, so local URLs (`/setting/…`, `/gm-notes/…`, the `/` redirect) match production exactly. Windows serves at <http://localhost:8008>, the shell script at <http://localhost:8000>; the browser opens automatically and refreshes on edit. `Ctrl+C` to stop.

**First run note:** `npx --yes live-server` downloads `live-server` on its first invocation (~25 MB, one time). Subsequent runs start instantly.

### Fallback: Python's built-in server

If Node isn't available, Python's `http.server` works (no auto-reload). Serve the `published/` folder as root:

```bash
python -m http.server 8000 --directory published    # Windows
python3 -m http.server 8000 --directory published   # macOS / Linux
```

Open <http://localhost:8000>; hit `Ctrl+R` after each edit.

---

## Deployment

GitHub Pages deploys via a **GitHub Actions workflow** ([`.github/workflows/pages.yml`](.github/workflows/pages.yml)) on every push to `main`: it uploads the **`published/`** folder as the Pages artifact and deploys it as the site root. No other build step.

- Repo **Settings → Pages → Source** must be set to **GitHub Actions** (not branch deploy).
- The served root needs a homepage: `published/index.html` is a meta-refresh redirect to `/setting/` (the cosmology primer lives at `/setting/index.html`).
- All pages use absolute paths (start with `/`), resolved against the served root.
- The custom domain `tyrnarra.kunkel.swiss` is configured via `published/CNAME`.

To preview a change live, push to `main` and wait ~1–2 min for the Actions deploy.

---

## Where things live (quick orientation)

- **Worldbuilding HTML**: `/published/setting/` — `cosmology/` for world-level pages (cosmology, gods, magic, …), `talan/` for the continent, `talan/domains/<slug>/` for the 13 god domains, `talan/factions/` for organisations, `off-continent/` for non-Talan powers.
- **Shared CSS + sidebar nav**: `/published/setting/assets/` (loaded by every worldbuilding page).
- **Campaign layers**: `/published/gm-notes/` (GM-only, behind the screen) and `/published/player-campaigns/` (player-facing companion).
- **Private GM tooling** (not served): `/tools/` — the PF2e encounter/loot builders, the Foundry export pipeline, the map library, the token frames.
- **Worldbuilding canon** (not served): `/lore/`. The authoritative world notes.
- **Site documentation** (not served): `/docs/`. site-inventory.md (status), sidebar-nav.md, campaign-layer.md, and the rest.

For the full folder tree, layer-to-folder mapping, and conventions, see [`CLAUDE.md`](CLAUDE.md).
