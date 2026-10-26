#!/usr/bin/env python3
r"""
upload_foundry.py - copy local images into a world's assets folder on the
self-hosted Foundry server (rsync over ssh; replaces the old Forge upload).

Foundry serves its Data folder at the site root, so an image copied to
Data/worlds/<world>/assets/<sub>/<file> is addressable in the world as the
relative path "worlds/<world>/assets/<sub>/<file>". This prints, and optionally
writes, a {filename -> that path} map you can feed straight into
`foundry_macro.py assign-images` (or pass the printed --base).

The server address stays out of this public repo: TYRNARRA_FOUNDRY ("host:/root",
where root holds data/Data/), else the first line of
~/.config/tyrnarra/foundry-remote. The host is an ssh alias or LAN name from
your ~/.ssh/config, so any machine on the home network with that alias and key
can upload. Repo campaign -> Foundry world ids live in campaigns.json beside
this script.

Usage:
  python upload_foundry.py --list-worlds
  python upload_foundry.py --dir ../../published/gm-notes/furrious-five/millhaven/art \
      --campaign furrious-five --sub tokens/npc --out foundry_urls.json
  python upload_foundry.py --dir <dir> --world heavens-dragons --sub portraits
"""
import argparse
import json
import os
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REMOTE_FILE = os.path.expanduser("~/.config/tyrnarra/foundry-remote")
CAMPAIGNS = os.path.join(HERE, "campaigns.json")
IMAGE_EXTS = ".webp,.png,.jpg,.jpeg,.gif,.svg"


def foundry_remote():
    """(host, root) from TYRNARRA_FOUNDRY, else ~/.config/tyrnarra/foundry-remote."""
    remote = os.environ.get("TYRNARRA_FOUNDRY", "").strip()
    if not remote:
        try:
            with open(REMOTE_FILE, encoding="utf-8") as fh:
                remote = fh.readline().strip()
        except OSError:
            pass
    if ":" not in remote:
        sys.exit("No Foundry server configured: write \"<ssh-host>:/<foundry-root>\" to "
                 f"{REMOTE_FILE} or set TYRNARRA_FOUNDRY (see tools/README.md).")
    host, root = remote.split(":", 1)
    return host, root.rstrip("/")


def ssh(host, cmd):
    return subprocess.run(["ssh", "-o", "BatchMode=yes", host, cmd], check=True,
                          text=True, capture_output=True).stdout


def list_worlds(host, root):
    out = ssh(host, f"ls -1 {shlex.quote(root + '/data/Data/worlds')}")
    return [w for w in out.split() if not w.endswith(".txt")]


def world_for(campaign):
    with open(CAMPAIGNS, encoding="utf-8") as fh:
        worlds = json.load(fh)
    if campaign not in worlds:
        sys.exit(f"Campaign '{campaign}' is not in {CAMPAIGNS}; add it or pass --world.")
    if not worlds[campaign]:
        sys.exit(f"Campaign '{campaign}' has no Foundry world yet; create it, record its id "
                 f"in {CAMPAIGNS}, or pass --world.")
    return worlds[campaign]


def main():
    ap = argparse.ArgumentParser(description="Upload images into a Foundry world's assets folder.")
    ap.add_argument("--dir", help="Local directory of images to upload.")
    who = ap.add_mutually_exclusive_group()
    who.add_argument("--campaign", help="Repo campaign slug (looked up in campaigns.json).")
    who.add_argument("--world", help="Foundry world id (folder under Data/worlds/).")
    ap.add_argument("--sub", default="tokens/npc",
                    help="Folder under the world's assets/ (default tokens/npc, the worlds' convention).")
    ap.add_argument("--ext", default=IMAGE_EXTS, help="Comma-separated extensions to upload.")
    ap.add_argument("--out", help="Write a {filename: foundry path} JSON map here.")
    ap.add_argument("--list-worlds", action="store_true", help="List the server's worlds and exit.")
    a = ap.parse_args()

    host, root = foundry_remote()
    worlds = list_worlds(host, root)
    if a.list_worlds:
        print("\n".join(worlds))
        return
    if not a.dir or not (a.campaign or a.world):
        ap.error("--dir and one of --campaign/--world are required")

    world = a.world or world_for(a.campaign)
    if world not in worlds:
        sys.exit(f"World '{world}' is not on the server (have: {', '.join(worlds)}).")
    sub = a.sub.strip("/")
    exts = tuple(e if e.startswith(".") else "." + e for e in a.ext.lower().split(","))
    files = sorted(f for f in os.listdir(a.dir)
                   if f.lower().endswith(exts) and os.path.isfile(os.path.join(a.dir, f)))
    if not files:
        sys.exit(f"No matching images in {a.dir}")

    rel = f"worlds/{world}/assets/{sub}"
    dest = f"{host}:{root}/data/Data/{rel}/"
    # No --delete: other art already in that folder stays. --mkpath creates the
    # sub-folder; --chmod keeps files readable by the Foundry container.
    subprocess.run(["rsync", "-t", "--mkpath", "--chmod=D755,F644", "--itemize-changes",
                    *[os.path.join(a.dir, f) for f in files], dest], check=True)

    urls = {f: f"{rel}/{f}" for f in files}
    print(f"\nDone: {len(files)} file(s) in {rel}/")
    print(f"assign-images base: --base \"{rel}/\"")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(urls, fh, ensure_ascii=False, indent=2)
        print(f"Wrote path map: {a.out}")


if __name__ == "__main__":
    main()
