#!/usr/bin/env python3
r"""
upload_forge.py - upload local images to The Forge Assets Library via its API.

Posts each file to https://upload.forge-vtt.com with an `Access-Key` header
(multipart fields `path` = "<target>/<filename>" and `file`), exactly as The
Forge's own FilePicker does. Prints, and optionally writes, a {filename -> asset
URL} map you can feed straight into `foundry_macro.py assign-images` (the URLs
are absolute, so they're used as-is).

Key: reads FORGE_KEY from the environment, else a gitignored forge_key.txt next
to this script. Get one at The Forge -> Account -> API Keys (needs write-assets).

Usage:
  python upload_forge.py --dir ../../furrious-five/portraits \
      --target furrious-five/below-the-quiet-docks --out forge_urls.json
"""
import argparse
import json
import os
import sys

UPLOAD_ENDPOINT = "https://upload.forge-vtt.com"
CONTENT_TYPES = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg",
                 ".jpeg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml"}


def get_key():
    key = os.environ.get("FORGE_KEY")
    if not key:
        kf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "forge_key.txt")
        if os.path.exists(kf):
            key = open(kf, encoding="utf-8").read().strip()
    if not key:
        sys.exit("Set FORGE_KEY in the environment or put it in forge_key.txt (gitignored).")
    return key


def upload_one(requests, key, path_in_library, local_path, content_type):
    with open(local_path, "rb") as fh:
        files = {"file": (os.path.basename(local_path), fh, content_type)}
        data = {"path": path_in_library}
        r = requests.post(UPLOAD_ENDPOINT, headers={"Access-Key": key},
                          data=data, files=files, timeout=120)
    r.raise_for_status()
    body = r.json()
    if not (body.get("url") or body.get("status") == "success"):
        raise RuntimeError(f"unexpected response: {body}")
    return body.get("url")


def main():
    ap = argparse.ArgumentParser(description="Upload images to The Forge Assets Library.")
    ap.add_argument("--dir", required=True, help="Local directory of images to upload.")
    ap.add_argument("--target", required=True,
                    help="Destination folder in your Forge assets, e.g. furrious-five/below-the-quiet-docks")
    ap.add_argument("--ext", default=".webp,.png,.jpg,.jpeg",
                    help="Comma-separated extensions to upload (default images).")
    ap.add_argument("--out", help="Write a {filename: url} JSON map here.")
    a = ap.parse_args()

    try:
        import requests
    except ImportError:
        sys.exit("Missing dep. Run: pip install requests")

    key = get_key()
    exts = tuple(e if e.startswith(".") else "." + e for e in a.ext.split(","))
    target = a.target.strip("/")
    files = sorted(f for f in os.listdir(a.dir) if f.lower().endswith(exts))
    if not files:
        sys.exit(f"No matching images in {a.dir}")

    urls, failed = {}, 0
    for f in files:
        local = os.path.join(a.dir, f)
        path_in_library = f"{target}/{f}"
        ct = CONTENT_TYPES.get(os.path.splitext(f)[1].lower(), "application/octet-stream")
        try:
            url = upload_one(requests, key, path_in_library, local, ct)
            urls[f] = url
            print(f"  uploaded {f} -> {url}")
        except Exception as e:
            print(f"  ! {f} failed: {e}", file=sys.stderr)
            failed += 1

    print(f"\nDone: {len(urls)} uploaded, {failed} failed -> {target}/")
    if a.out and urls:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(urls, fh, ensure_ascii=False, indent=2)
        print(f"Wrote URL map: {a.out}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
