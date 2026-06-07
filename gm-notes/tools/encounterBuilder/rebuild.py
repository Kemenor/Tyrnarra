#!/usr/bin/env python3
"""
rebuild.py - cross-platform prestart hook: sync Foundry pf2e creature packs and
rebuild the static bestiary.db. Runs natively on Windows/macOS/Linux (no bash).

  python rebuild.py            # first run clones + builds; later runs pull + rebuild

It sparse-checks-out only the creature packs (anything whose folder name matches
PACK_RE), so the working copy stays small. Pack names are discovered from the git
tree rather than hardcoded, so new AP/Lost Omens bestiaries are picked up
automatically and we don't depend on a fixed repo layout.

Env overrides: PF2E_REPO (checkout dir), HOMEBREW_DIR (your creature JSON).
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("PF2E_REPO", os.path.join(HERE, "_sources", "pf2e"))
HOMEBREW = os.environ.get("HOMEBREW_DIR", os.path.join(HERE, "homebrew"))
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
        git("-C", REPO, "pull", "--depth", "1", "--ff-only")


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
    subprocess.run(cmd, check=True)

    # 2. equipment -> items.db
    eq_dir = os.path.join(REPO, EQUIPMENT_PACK.replace("/", os.sep))
    subprocess.run([sys.executable, os.path.join(HERE, "build_items.py"),
                    "--packs", eq_dir, "--out", os.path.join(HERE, "items.db")],
                   check=True)
    print("Rebuild complete: bestiary.db + items.db")


if __name__ == "__main__":
    main()
