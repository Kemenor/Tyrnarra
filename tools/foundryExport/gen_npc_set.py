#!/usr/bin/env python3
r"""
gen_npc_set.py - generate a CONSISTENT multi-shot image set for one NPC via fal.ai.

Companion to gen_portraits.py. That script renders independent square portraits
from a portraits JSON; this one renders ONE character as a coherent set (for
example: full body + head-and-shoulders portrait + an in-scene shot), keeping the
same face, fur, and wardrobe across all of them.

How it stays consistent: it renders an ANCHOR shot first as plain text-to-image
(the most identity-bearing view, usually the full body), then renders every other
shot through FLUX.2's reference endpoint (fal-ai/flux-2/edit), passing the anchor
image as a reference so the character carries over. FLUX.2 [dev] accepts up to
four reference images; we use the one anchor.

Set-spec JSON:
{
  "slug": "sable-rei",
  "out": ".",                       # output dir, relative to THIS spec file
  "anchor": "full",                 # which shot is the text-to-image anchor
  "character": "shared subject description, reused in every shot",
  "wardrobe":  "shared wardrobe, reused in every shot",
  "style":     "shared style suffix, reused in every shot",
  "shots": {
    "full":     {"file": "sable-rei-full",    "size": "portrait_4_3", "framing": "..."},
    "portrait": {"file": "sable-rei",         "size": "square_hd",    "framing": "..."},
    "lowspan":  {"file": "sable-rei-lowspan", "size": "portrait_4_3", "framing": "..."}
  }
}

Each shot's prompt is assembled as: framing + character + wardrobe + style. The
non-anchor shots additionally instruct the model to keep the reference character.

Setup:
  pip install fal-client requests
  FAL_KEY env var, or fal_key.txt next to this script (gitignored).

Usage:
  python gen_npc_set.py --spec ../../published/gm-notes/furrious-five/assets/portraits/sable-rei.set.json
  # --only portrait,lowspan renders a subset (the on-disk anchor is uploaded as the
  #   reference if it already exists); --force overwrites existing files.
"""
import argparse
import json
import os
import sys


def build_prompt(shot, spec, is_edit):
    parts = []
    if is_edit:
        parts.append("Keep the exact same character as in the reference image: "
                     "same face, same fur pattern and colour, same tail, same coat.")
    parts.append(shot["framing"])
    parts.append(spec["character"].strip() + ", " + spec["wardrobe"].strip() + ".")
    parts.append(spec["style"])
    return " ".join(p.strip() for p in parts if p and p.strip())


def main():
    ap = argparse.ArgumentParser(description="Render a consistent multi-shot NPC image set via fal.ai FLUX.2.")
    ap.add_argument("--spec", required=True, help="Set-spec JSON (see module docstring).")
    ap.add_argument("--model", default="fal-ai/flux-2", help="Text-to-image model for the anchor (default fal-ai/flux-2).")
    ap.add_argument("--edit-model", default="fal-ai/flux-2/edit", help="Reference/edit model for the other shots.")
    ap.add_argument("--ext", default="webp", help="Output extension (webp/png/jpg). Default webp.")
    ap.add_argument("--only", help="Comma-separated shot keys to render (default: all).")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files.")
    a = ap.parse_args()

    # Key: env var, or the gitignored fal_key.txt next to this script.
    if not os.environ.get("FAL_KEY"):
        keyfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fal_key.txt")
        if os.path.exists(keyfile):
            os.environ["FAL_KEY"] = open(keyfile, encoding="utf-8").read().strip()
    if not os.environ.get("FAL_KEY"):
        sys.exit("Set FAL_KEY in the environment, or put it in fal_key.txt next to this "
                 "script (gitignored). Get a key at https://fal.ai/dashboard/keys.")
    try:
        import fal_client
        import requests
    except ImportError:
        sys.exit("Missing deps. Run: pip install fal-client requests")

    spec_path = os.path.abspath(a.spec)
    spec = json.load(open(spec_path, encoding="utf-8-sig"))
    shots = spec.get("shots") or {}
    if not shots:
        sys.exit("No 'shots' in the spec.")
    anchor_key = spec.get("anchor") or next(iter(shots))
    if anchor_key not in shots:
        sys.exit(f"anchor '{anchor_key}' is not one of the shots.")

    out_dir = os.path.normpath(os.path.join(os.path.dirname(spec_path), spec.get("out", ".")))
    os.makedirs(out_dir, exist_ok=True)
    fmt = {"jpg": "jpeg"}.get(a.ext, a.ext)
    only = set(s.strip() for s in a.only.split(",")) if a.only else None
    want = [k for k in shots if not only or k in only]

    def dest_of(key):
        return os.path.join(out_dir, f"{shots[key]['file']}.{a.ext}")

    def url_from(res):
        url = (res.get("images") or [{}])[0].get("url")
        if not url:
            raise RuntimeError(f"no image url in result: {res}")
        return url

    def save(url, key):
        img = requests.get(url, timeout=180)
        img.raise_for_status()
        with open(dest_of(key), "wb") as fh:
            fh.write(img.content)
        print(f"        -> {dest_of(key)}")

    # A shot is rendered text-to-image ("text") or as an anchor-referenced edit
    # ("ref"). The anchor is always text; other shots default to ref, but a shot
    # can set "mode": "text" to get a fresh composition (e.g. a tight head-and-
    # shoulders portrait, which the reference endpoint will not crop to).
    def mode_of(key):
        return "text" if key == anchor_key else shots[key].get("mode", "ref")

    def render(key, ref_url):
        s = shots[key]
        if mode_of(key) == "ref":
            return url_from(fal_client.subscribe(a.edit_model, arguments={
                "prompt": build_prompt(s, spec, is_edit=True),
                "image_urls": [ref_url],
                "image_size": s.get("size", "portrait_4_3"),
                "num_images": 1, "output_format": fmt}))
        return url_from(fal_client.subscribe(a.model, arguments={
            "prompt": build_prompt(s, spec, is_edit=False),
            "image_size": s.get("size", "portrait_4_3"),
            "num_images": 1, "output_format": fmt}))

    rendered, skipped, failed = 0, 0, 0
    anchor_url = None
    need_ref = any(k != anchor_key and mode_of(k) == "ref" for k in want)

    # 1) Anchor first (always text-to-image; it is the reference for ref-mode shots).
    anchor_dest = dest_of(anchor_key)
    if anchor_key in want and (a.force or not os.path.exists(anchor_dest)):
        print(f"  anchor {anchor_key} ({shots[anchor_key]['file']}) ...", flush=True)
        try:
            anchor_url = render(anchor_key, None)
            save(anchor_url, anchor_key)
            rendered += 1
        except Exception as e:
            sys.exit(f"anchor render failed (the set needs it as its reference): {e}")
    elif anchor_key in want:
        print(f"  skip {anchor_key} (exists)")
        skipped += 1

    if need_ref and not anchor_url:
        if not os.path.exists(anchor_dest):
            sys.exit(f"need the anchor as a reference, but {anchor_dest} is missing; "
                     f"render it first (drop --only, or pass --force).")
        print(f"  upload existing anchor {anchor_key} as reference ...", flush=True)
        anchor_url = fal_client.upload_file(anchor_dest)

    # 2) Every other shot: anchor-referenced edit, or its own text-to-image (mode:text).
    for key in want:
        if key == anchor_key:
            continue
        if os.path.exists(dest_of(key)) and not a.force:
            print(f"  skip {key} (exists)")
            skipped += 1
            continue
        m = mode_of(key)
        print(f"  shot   {key} ({shots[key]['file']}) [{m}] ...", flush=True)
        try:
            url = render(key, anchor_url)
            save(url, key)
            rendered += 1
        except Exception as e:                       # one failure should not kill the batch
            print(f"        ! failed: {e}", file=sys.stderr)
            failed += 1

    print(f"\nDone: {rendered} rendered, {skipped} skipped, {failed} failed -> {out_dir}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
