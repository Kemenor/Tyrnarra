#!/usr/bin/env python3
"""
check_setup.py - is this machine ready to run the GM tools? (see tools/README.md)

  python3 tools/check_setup.py                       # check everything
  python3 tools/check_setup.py --foundry "<ssh-alias>:/<foundry-root>" --comfy http://<desktop-ip>:8188
                                                     # write the two private address files, then check

Checks the toolchain (python packages, node, rsync, ssh), the private address
files in ~/.config/tyrnarra/ (kept out of this public repo), the Foundry server
over ssh (and that every campaign in foundryExport/campaigns.json has its world),
the ComfyUI renderer, and the built encounter/loot databases. It never changes
anything except the address files you pass.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.expanduser("~/.config/tyrnarra")
FOUNDRY_FILE = os.path.join(CONF, "foundry-remote")
COMFY_FILE = os.path.join(CONF, "comfyui-url")

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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--foundry", help='Write ~/.config/tyrnarra/foundry-remote ("<ssh-host>:/<foundry-root>").')
    ap.add_argument("--comfy", help="Write ~/.config/tyrnarra/comfyui-url (http://<host>:8188).")
    a = ap.parse_args()
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

    print("Keys (tools/keys/, from Proton Drive)")
    report(os.path.exists(os.path.join(HERE, "keys", "falai.key")) or None,
           "falai.key (fal.ai fallback renderer only)", "copy it from Proton Drive if you need fal")

    print("\nAll required checks passed." if not failed else f"\n{failed} required check(s) failed.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
