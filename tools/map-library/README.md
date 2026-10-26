# Map Library

Shared, reusable battlemap resources for the campaign layer. Two kinds of thing live here:

- **Committed text catalogues** (e.g. [`magirail-stock.md`](magirail-stock.md)): descriptions, role tags, grid sizes, and ready-made recipes. These travel in git.
- **Local-only source art** under `_full/` (gitignored): the actual high-resolution map images (Tom Cartos, CzePeku). They are subscription/licensed and are never committed or published.

## Restoring the art on a new PC

The `_full/` art is **not in git**. It lives in the private Proton Drive sync folder (`~/ProtonDrive/Tyrnarra sync/map-library/`), and `_full` is a link to that folder, so a fresh clone has the catalogues and gets the images by linking:

```bash
python3 tools/check_setup.py --link
```

The subfolders line up through the link (`map-library/trains/` in the sync folder is `tools/map-library/_full/trains/`), so the catalogue filenames match the files and Claude can assemble consists. Re-downloading from the Tom Cartos / CzePeku subscriptions is the fallback if the Proton sync is unavailable.

> Campaign-specific art (for example a single quest's station map under a campaign's own `assets/maps/_full/`) is restored the same way from its own source; only the shared library art lives under this folder.
