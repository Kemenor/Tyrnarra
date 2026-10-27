#!/usr/bin/env python3
"""
check_setup.py - is this machine ready to run the GM tools? (see tools/README.md)

  python3 tools/check_setup.py                       # check everything
  python3 tools/check_setup.py --foundry "<ssh-alias>:/<foundry-root>" --comfy http://<desktop-ip>:8188
                                                     # write the two private address files, then check
  python3 tools/check_setup.py --link                # link keys, map art and config into the sync folder

Checks the toolchain (python packages, node, rsync, ssh), the private address
files in ~/.config/tyrnarra/ (kept out of this public repo), the Foundry server
over ssh (and that every campaign in foundryExport/campaigns.json has its world),
the ComfyUI renderer, the built encounter/loot databases, and the links into the
Syncthing sync folder ("~/Sync/Tyrnarra", or $TYRNARRA_SYNC). It never changes
anything except the address files you pass and, with --link, those links.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
GM_NOTES = os.path.join(os.path.dirname(HERE), "published", "gm-notes")
APPDATA = os.path.expanduser("~/.local/share")
CONF = os.path.expanduser("~/.config/tyrnarra")
FOUNDRY_FILE = os.path.join(CONF, "foundry-remote")
COMFY_FILE = os.path.join(CONF, "comfyui-url")
SYNC = os.path.expanduser(os.environ.get("TYRNARRA_SYNC", "~/Sync/Tyrnarra"))

failed = 0


def report(ok, what, fix=""):
    global failed
    mark = "ok  " if ok is True else ("warn" if ok is None else "FAIL")
    if ok is False:
        failed += 1
    print(f"  [{mark}] {what}" + (f"\n         -> {fix}" if fix and ok is not True else ""))


def setting(env, path):
    if os.environ.get(env):
        return os.environ[env].strip()
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.readline().strip()
    except OSError:
        return ""


def write(path, value):
    os.makedirs(CONF, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(value.strip() + "\n")
    print(f"  wrote {path}")


def links():
    """(link, target) pairs: the real files live in the sync folder, the tools reach them through
    links. comfyui-url stays a plain local file, because it differs per machine."""
    pairs = [(os.path.join(HERE, "map-library", "_full"), os.path.join(SYNC, "map-library")),
             (FOUNDRY_FILE, os.path.join(SYNC, "config", "foundry-remote")),
             (os.path.join(APPDATA, "wdmap", "assetgen"), os.path.join(SYNC, "assetgen-work", "work"))]
    keys = os.path.join(SYNC, "keys")
    for name in sorted(os.listdir(keys)) if os.path.isdir(keys) else []:
        pairs.append((os.path.join(HERE, "keys", name), os.path.join(keys, name)))
    # GM-notes full-res art: published/gm-notes/<rel>/_full <-> published-full/<rel>, from either side
    full = os.path.join(SYNC, "published-full")
    rels = set()
    for root, dirs, _ in os.walk(GM_NOTES):
        if "_full" in dirs:
            rels.add(os.path.relpath(root, GM_NOTES))
        dirs[:] = [d for d in dirs if d != "_full"]
    for root, dirs, files in os.walk(full):
        if files and root != full:
            rels.add(os.path.relpath(root, full))
            dirs[:] = []
    for rel in sorted(rels):
        pairs.append((os.path.join(GM_NOTES, rel, "_full"), os.path.join(full, rel)))
    # app data the maps need to render, on machines that have the app. The asset packs live in
    # Kartofuchs/packs: Kartofuchs' own pack folder, and Wonderdraft's asset folder while it is installed.
    packs = os.path.join(SYNC, "Kartofuchs", "packs")
    for app, sub, names in (("Wonderdraft", "Wonderdraft", ("themes",)),
                            ("kartofuchs", "Kartofuchs", ("stamps", "themes", "mappings", "art-sizes.json"))):
        if os.path.isdir(os.path.join(APPDATA, app)):
            pairs += [(os.path.join(APPDATA, app, n), os.path.join(SYNC, sub, "app", n)) for n in names]
            pairs.append((os.path.join(APPDATA, app, "assets" if app == "Wonderdraft" else "packs"), packs))
    # the maps' fonts (labels, and what the Avoro themes name), as user fonts for both map apps
    fonts = (os.path.join(APPDATA, "fonts", "tyrnarra"), os.path.join(SYNC, "fonts"))
    if any(os.path.exists(p) for p in fonts):
        pairs.append(fonts)
    return pairs


def link(path, target):
    """Point path at target. A local file or folder with no synced copy yet moves into the sync folder
    first; anything else already at path is left alone and reported."""
    if os.path.islink(path):
        if os.path.realpath(path) == os.path.realpath(target):
            return
        os.remove(path)
    elif os.path.isdir(path):
        if set(os.listdir(path)) - {".gitkeep"}:
            if os.path.exists(target):
                print(f"  skipped {path}: {target} exists too; merge them into {target} first")
                return
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.move(path, target)
            print(f"  moved {path} -> {target}")
        else:
            shutil.rmtree(path)
    elif os.path.exists(path):
        if os.path.exists(target):
            print(f"  skipped {path}: {target} exists too; keep one of them")
            return
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.move(path, target)
        print(f"  moved {path} -> {target}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.symlink(target, path)
    print(f"  linked {path} -> {target}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--foundry", help='Write ~/.config/tyrnarra/foundry-remote ("<ssh-host>:/<foundry-root>").')
    ap.add_argument("--comfy", help="Write ~/.config/tyrnarra/comfyui-url (http://<host>:8188).")
    ap.add_argument("--link", action="store_true",
                    help="Link keys, map art, foundry-remote, assetgen work and map-app data into the sync folder.")
    a = ap.parse_args()
    if a.link:
        if not os.path.isdir(SYNC):
            sys.exit(f"no sync folder at {SYNC} (set TYRNARRA_SYNC)")
        for path, target in links():
            link(path, target)
        if shutil.which("fc-cache"):
            subprocess.run(["fc-cache", "-f", os.path.join(APPDATA, "fonts")], check=False)
    if a.foundry:
        write(FOUNDRY_FILE, a.foundry)
    if a.comfy:
        write(COMFY_FILE, a.comfy)

    print("Toolchain")
    report(sys.version_info >= (3, 10), f"python {sys.version.split()[0]}", "install Python 3.10+")
    for mod, pkg, need in (("requests", "requests", True), ("PIL", "pillow", True),
                           ("numpy", "numpy", True), ("scipy", "scipy", False)):
        try:
            __import__(mod)
            report(True, f"python package {pkg}")
        except ImportError:
            report(False if need else None, f"python package {pkg}" + ("" if need else " (wonderdraft tools only)"),
                   f"pip install {pkg}")
    for cmd, why, need in (("git", "repo", True), ("ssh", "Foundry server", True),
                           ("rsync", "Foundry mirror + art upload", True),
                           ("node", "module export, contrast check, local site server", True),
                           ("sqlite3", "poking the DBs by hand", False)):
        report(bool(shutil.which(cmd)) or (None if not need else False), f"{cmd} ({why})",
               f"install {cmd}")

    print("Foundry server")
    remote = setting("TYRNARRA_FOUNDRY", FOUNDRY_FILE)
    if ":" not in remote:
        report(False, "no address", f'python3 tools/check_setup.py --foundry "<ssh-host>:/<foundry-root>"')
    else:
        host, root = remote.split(":", 1)
        report(True, f"address set (ssh host '{host}')")
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=6", host,
                            f"ls -1 '{root.rstrip('/')}/data/Data/worlds'"],
                           capture_output=True, text=True)
        if r.returncode:
            report(False, f"ssh {host}: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'failed'}",
                   f"add '{host}' to ~/.ssh/config with your key (ssh-copy-id), and be on the home network")
        else:
            worlds = {w for w in r.stdout.split() if not w.endswith(".txt")}
            report(True, f"reachable; worlds: {', '.join(sorted(worlds))}")
            with open(os.path.join(HERE, "foundryExport", "campaigns.json"), encoding="utf-8") as fh:
                for camp, world in json.load(fh).items():
                    if not world:
                        report(None, f"campaign {camp}: no Foundry world yet")
                    else:
                        report(world in worlds, f"campaign {camp} -> world {world}",
                               "fix the world id in tools/foundryExport/campaigns.json")

    print("ComfyUI renderer (npc_art / scene_art / assetgen)")
    comfy = setting("TYRNARRA_COMFY", COMFY_FILE) or "http://127.0.0.1:8188"
    try:
        urllib.request.urlopen(comfy.rstrip("/") + "/system_stats", timeout=4)
        report(True, f"answering at {comfy}")
    except Exception:
        report(None, f"not answering at {comfy}",
               "on the desktop npc_art starts it itself; from the laptop start run-comfyui-lan.sh "
               "on the desktop and set --comfy http://<desktop-ip>:8188")

    print("Databases")
    for db in ("bestiary.db", "items.db"):
        report(os.path.exists(os.path.join(HERE, "encounterBuilder", db)) or False, f"encounterBuilder/{db}",
               "python3 tools/encounterBuilder/rebuild.py")

    print(f"Sync folder ({SYNC})")
    if not os.path.isdir(SYNC):
        report(None, "missing", "set up Syncthing (tools/README.md), or set TYRNARRA_SYNC")
    else:
        for path, target in links():
            root = os.path.dirname(HERE)
            short = os.path.relpath(path, root) if path.startswith(root) else path.replace(os.path.expanduser("~"), "~")
            ok = os.path.islink(path) and os.path.realpath(path) == os.path.realpath(target)
            report(ok or None, f"{short} -> sync folder", "python3 tools/check_setup.py --link")

    print("Keys (tools/keys/, linked from the sync folder's keys/)")
    report(os.path.exists(os.path.join(HERE, "keys", "falai.key")) or None,
           "falai.key (fal.ai fallback renderer only)",
           "put it in the sync folder's keys/ and run check_setup.py --link")

    print("\nAll required checks passed." if not failed else f"\n{failed} required check(s) failed.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
