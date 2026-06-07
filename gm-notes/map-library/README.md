# Map Library

Shared, reusable battlemap resources for the campaign layer. Two kinds of thing live here:

- **Committed text catalogues** (e.g. [`magirail-stock.md`](magirail-stock.md)): descriptions, role tags, grid sizes, and ready-made recipes. These travel in git.
- **Local-only source art** under `_full/` (gitignored): the actual high-resolution map images (Tom Cartos, CzePeku). They are subscription/licensed and are never committed or published.

## Restoring the art on a new PC

The `_full/` art is **not in git**. It is synced between machines through a private **Proton Drive**, so a fresh clone has the catalogues but no images. Copy the art across before stitching any maps:

- **Proton Drive source:** `%USERPROFILE%\Proton Drive\My Files\map-library\`
- **Repo target:** `campaigns\map-library\_full\`

Copy the contents of the Proton folder into `_full/` so the subfolders line up (e.g. `…\map-library\trains\` lands at `campaigns\map-library\_full\trains\`). A mirror copy from the repo root:

```powershell
robocopy "$env:USERPROFILE\Proton Drive\My Files\map-library" "campaigns\map-library\_full" /E
```

Once copied, the catalogue filenames match the files in `_full/` and Claude can assemble consists. Re-downloading from the Tom Cartos / CzePeku subscriptions is the fallback if the Proton sync is unavailable.

> Campaign-specific art (for example a single quest's station map under a campaign's own `assets/maps/_full/`) is restored the same way from its own source; only the shared library art lives under this folder.
