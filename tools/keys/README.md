# tools/keys — API keys (local only)

The GM build tools authenticate to a paid service. Its key file lives **here**
and is **gitignored** (`tools/**/*_key.txt`), so it never reaches GitHub. A
fresh clone or new machine will not have it: copy it in from **Proton Drive**
(or recreate from the dashboard below).

| File | Env var | Used by | Get it |
|---|---|---|---|
| `forge_key.txt` | `FORGE_KEY` | Forge asset upload (`tools/foundryExport/upload_forge.py`) | The Forge → Account → API Keys (**write-assets**) |

(`fal_key.txt` was the fal.ai image-generation key; that tier was retired
June 2026 in favour of local ComfyUI rendering (`tools/imageGen/`), which
needs no key.)

Each script checks its env var first, then this folder, then (legacy) its own
directory. One key per file, the bare value, no quotes. The `.gitkeep` keeps this
folder present on a fresh clone even with the keys absent.
