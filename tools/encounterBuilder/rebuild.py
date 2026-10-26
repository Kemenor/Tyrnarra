#!/usr/bin/env python3
"""
rebuild.py - cross-platform prestart hook: sync Foundry pf2e creature packs and
rebuild the static bestiary.db. Runs natively on Windows/macOS/Linux (no bash).

  python rebuild.py            # first run clones + builds; later runs pull + rebuild

It sparse-checks-out only the creature packs (anything whose folder name matches
PACK_RE), so the working copy stays small. Pack names are discovered from the git
tree rather than hardcoded, so new AP/Lost Omens bestiaries are picked up
automatically and we don't depend on a fixed repo layout.

The Actor and Item packs of your installed Foundry modules are ingested too.
The Foundry server is self-hosted: its rsync address ("host:/root", where root
holds app/ and data/Data/) comes from TYRNARRA_FOUNDRY, else the first line of
~/.config/tyrnarra/foundry-remote, so no host detail lives in this public repo. Each run
mirrors just the module manifests, their Actor + Item packs and the app's
classic-level reader into _sources/foundry/ (gitignored), then
export_modules.mjs (needs node) converts them. If the server is unreachable it
falls back to the last mirror, then to a local ~/foundry install.

Env overrides: PF2E_REPO (checkout dir), HOMEBREW_DIR (your creature JSON),
TYRNARRA_FOUNDRY (rsync source; "" disables the sync), FOUNDRY_DATA / FOUNDRY_APP
(a local Foundry install, see export_modules.mjs).
"""
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("PF2E_REPO", os.path.join(HERE, "_sources", "pf2e"))
HOMEBREW = os.environ.get("HOMEBREW_DIR", os.path.join(HERE, "homebrew"))
REMOTE_FILE = os.path.expanduser("~/.config/tyrnarra/foundry-remote")
MIRROR = os.path.join(HERE, "_sources", "foundry")
LOCAL_FOUNDRY = os.path.join(os.path.expanduser("~"), "foundry")
MODULES_OUT = os.path.join(HERE, "_sources", "modules")
MODULE_ITEMS_OUT = os.path.join(HERE, "_sources", "module-items")
# classic-level plus its runtime dependency closure, copied out of the Foundry
# app (its prebuilds cover linux-x64 as well as the Pi's arm64). If a Foundry
# update adds a dependency, export_modules.mjs fails loudly on the require.
LEVEL_PKGS = ["classic-level", "abstract-level", "level-supports", "level-transcoder",
              "module-error", "maybe-combine-errors", "buffer", "is-buffer",
              "napi-macros", "node-gyp-build", "base64-js", "ieee754"]
REMOTE = "https://github.com/foundryvtt/pf2e.git"
# Creature-bearing packs: every bestiary, Monster Core, and the NPC gallery...
PACK_RE = re.compile(r"bestiary|monster-core|npc-gallery", re.I)
# ...minus the bestiary-adjacent rules packs that hold no actors (npc JSON).
EXCLUDE_RE = re.compile(r"glossary|effects", re.I)
# pf2e packs live under packs/pf2e/ (packs/sf2e/ is Starfinder; skip it).
PACKS_ROOT = "packs/pf2e"


def git(*args, capture=False):
    return subprocess.run(["git", *args], check=True, text=True,
                          capture_output=capture)


def ensure_repo():
    if not os.path.isdir(os.path.join(REPO, ".git")):
        os.makedirs(os.path.dirname(REPO), exist_ok=True)
        git("clone", "--filter=blob:none", "--no-checkout", "--depth", "1", REMOTE, REPO)
        git("-C", REPO, "sparse-checkout", "init", "--cone")
    else:
        # A depth-1 clone can't fast-forward (its lone commit shares no history
        # with the new tip), so fetch the tip and reset onto it. The checkout is
        # a read-only mirror; nothing local to lose.
        git("-C", REPO, "fetch", "--depth", "1", "origin", "HEAD")
        git("-C", REPO, "reset", "--hard", "FETCH_HEAD")


def discover_packs():
    # List the pf2e pack dirs from the tree (no blob fetch needed) and keep only
    # the creature-bearing ones.
    out = git("-C", REPO, "ls-tree", "-d", "--name-only", "HEAD", PACKS_ROOT + "/",
              capture=True).stdout
    packs = []
    for d in out.splitlines():
        base = os.path.basename(d)
        if PACK_RE.search(base) and not EXCLUDE_RE.search(base):
            packs.append(d)
    return packs


EQUIPMENT_PACK = PACKS_ROOT + "/equipment"


def rsync(src, dest, *opts):
    os.makedirs(dest, exist_ok=True)
    subprocess.run(["rsync", "-a", "--delete", "--delete-excluded", "-m", *opts, src, dest],
                   check=True)


def foundry_remote():
    """The server's rsync source: TYRNARRA_FOUNDRY, else ~/.config/tyrnarra/foundry-remote."""
    if "TYRNARRA_FOUNDRY" in os.environ:
        return os.environ["TYRNARRA_FOUNDRY"].strip()
    try:
        with open(REMOTE_FILE, encoding="utf-8") as fh:
            return fh.readline().strip()
    except OSError:
        return ""


def sync_foundry():
    """Mirror the server's module manifests, Actor + Item packs and the classic-level
    reader into MIRROR. Returns (data_dir, app_dir) for export_modules.mjs, or
    None when no Foundry source is available at all."""
    data, app = os.path.join(MIRROR, "data", "Data"), os.path.join(MIRROR, "app")
    mods = os.path.join(data, "modules")
    remote = foundry_remote()
    if remote and shutil.which("rsync"):
        try:
            src = remote.rstrip("/")
            # 1. manifests only, to learn where each module keeps its packs
            rsync(f"{src}/data/Data/modules/", mods + "/",
                  "--include=/*/", "--include=/*/module.json", "--exclude=*")
            # 2. manifests + Actor/Item pack dirs (each path's parent dirs must be included)
            rules = ["--include=/*/", "--include=/*/module.json"]
            for mod in sorted(os.listdir(mods)):
                with open(os.path.join(mods, mod, "module.json"), encoding="utf-8") as fh:
                    m = json.load(fh)
                for p in m.get("packs") or []:
                    if p.get("type") not in ("Actor", "Item"):
                        continue
                    rel = re.sub(r"\.db$", "", p["path"].lstrip("/"))
                    parts = rel.split("/")
                    for i in range(1, len(parts)):
                        rules.append(f"--include=/{mod}/{'/'.join(parts[:i])}/")
                    rules.append(f"--include=/{mod}/{rel}/***")
            rsync(f"{src}/data/Data/modules/", mods + "/", *rules, "--exclude=*")
            # 3. the LevelDB reader from the server's own Foundry app
            rsync(f"{src}/app/", app + "/", "--include=/package.json",
                  "--include=/node_modules/",
                  *[f"--include=/node_modules/{p}/***" for p in LEVEL_PKGS], "--exclude=*")
            print("Mirrored Foundry modules from the server.")
        except (subprocess.CalledProcessError, OSError) as e:
            print(f"Foundry sync failed ({e}); using what is on disk.")
    if os.path.isdir(mods) and os.path.isdir(os.path.join(app, "node_modules", "classic-level")):
        return data, app
    if os.path.isdir(os.path.join(LOCAL_FOUNDRY, "app")):
        return (os.environ.get("FOUNDRY_DATA", os.path.join(LOCAL_FOUNDRY, "data", "Data")),
                os.environ.get("FOUNDRY_APP", os.path.join(LOCAL_FOUNDRY, "app")))
    return None


def subdirs(d):
    return sorted(os.path.join(d, x) for x in os.listdir(d)) if os.path.isdir(d) else []


def main():
    ensure_repo()
    packs = discover_packs()
    if not packs:
        sys.exit("No creature packs discovered under packs/; check the repo layout.")
    git("-C", REPO, "sparse-checkout", "set", *packs, EQUIPMENT_PACK)
    git("-C", REPO, "checkout")
    print(f"Sparse-checked-out {len(packs)} creature packs + equipment.")

    # 1. creatures -> bestiary.db
    pack_dirs = [os.path.join(REPO, p.replace("/", os.sep)) for p in packs]
    cmd = [sys.executable, os.path.join(HERE, "build_db.py"),
           "--packs", *pack_dirs, "--out", os.path.join(HERE, "bestiary.db")]
    if os.path.isdir(HOMEBREW):
        cmd += ["--homebrew", HOMEBREW]
    # Installed Foundry modules (Battlezoo, Jam & Jax, ...), mirrored from the server.
    foundry = sync_foundry() if shutil.which("node") else None
    if foundry:
        env = dict(os.environ, FOUNDRY_DATA=foundry[0], FOUNDRY_APP=foundry[1])
        subprocess.run(["node", os.path.join(HERE, "export_modules.mjs")], check=True, env=env)
    else:
        print("No Foundry source (server, mirror or ~/foundry) or no node; skipping module content.")
    mod_dirs = subdirs(MODULES_OUT) if foundry else []
    if mod_dirs:
        cmd += ["--modules", *mod_dirs]
    subprocess.run(cmd, check=True)

    # 2. equipment -> items.db
    eq_dir = os.path.join(REPO, EQUIPMENT_PACK.replace("/", os.sep))
    item_cmd = [sys.executable, os.path.join(HERE, "build_items.py"),
                "--packs", eq_dir, "--out", os.path.join(HERE, "items.db")]
    item_mods = subdirs(MODULE_ITEMS_OUT) if foundry else []
    if item_mods:
        item_cmd += ["--modules", *item_mods]
    subprocess.run(item_cmd, check=True)
    print("Rebuild complete: bestiary.db + items.db")


if __name__ == "__main__":
    main()
