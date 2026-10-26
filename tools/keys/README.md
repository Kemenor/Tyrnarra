# tools/keys — API keys (local only)

Paid-service keys for the GM tools live **here** and are **gitignored**
(everything in `tools/keys/` except this README and `.gitkeep`), so they never
reach GitHub. The keys themselves live in the Syncthing sync folder
(`~/Sync/Tyrnarra/keys/`), and each one here is a link to its synced
copy: `python3 tools/check_setup.py --link` makes the links on a new machine.
Recreate a lost key from the dashboard below.

| File | Env var | Used by | Get it |
|---|---|---|---|
| `falai.key` | `FAL_KEY` | fal.ai fallback renderer (`tools/imageGen/fal_art.py`) | fal.ai dashboard → Keys |

Primary renders are local (ComfyUI on the desktop, `tools/imageGen/`) and need
no key. The old `forge_key.txt` (The Forge asset upload) is retired: Foundry is
self-hosted now and art goes up with `tools/foundryExport/upload_foundry.py`
over ssh.

**Addresses are not keys and do not live here.** The Foundry server's ssh
address and the ComfyUI desktop's URL go in `~/.config/tyrnarra/` on each
machine (see [`../README.md`](../README.md)), so no host detail is ever in the repo.

Each script checks its env var first, then this folder. One key per file, the
bare value, no quotes. The `.gitkeep` keeps this folder present on a fresh clone
even with the keys absent.
