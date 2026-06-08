# tools/keys — API keys (local only)

The GM build tools authenticate to a couple of paid services. Their key files
live **here** and are **gitignored** (`tools/**/*_key.txt`), so they never reach
GitHub. A fresh clone or new machine will not have them: copy them in from
**Proton Drive** (or recreate from the dashboards below).

| File | Env var | Used by | Get it |
|---|---|---|---|
| `fal_key.txt` | `FAL_KEY` | image generation (`tools/imageGen/`) | https://fal.ai/dashboard/keys (`id:secret`) |
| `forge_key.txt` | `FORGE_KEY` | Forge asset upload (`tools/foundryExport/upload_forge.py`) | The Forge → Account → API Keys (**write-assets**) |

Each script checks its env var first, then this folder, then (legacy) its own
directory. One key per file, the bare value, no quotes. The `.gitkeep` keeps this
folder present on a fresh clone even with the keys absent.
