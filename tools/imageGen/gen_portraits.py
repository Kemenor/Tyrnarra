#!/usr/bin/env python3
r"""
gen_portraits.py - batch-generate NPC portrait images from a portraits JSON.

Reads a portraits file ({"portraits":[{"slug","prompt"}, ...]}) and renders one
square image per entry to <out>/<slug>.<ext>, ready to upload to Foundry and
assign with `foundry_macro.py assign-images`.

Provider: fal.ai (https://fal.ai). It is model-agnostic - pass any fal image
model slug via --model, so "Flux.2 [dev] now, something else later" is a config
change, not a rewrite. (Moving to local ComfyUI later: reuse the same prompts in
the portraits JSON; only this generation step changes.)

Setup:
  pip install fal-client requests
  set FAL_KEY=<your fal key>          # PowerShell: $env:FAL_KEY = "..."

Usage:
  python gen_portraits.py --portraits ../../furrious-five/quest-venomqueen.portraits.json \
      --out ../../furrious-five/portraits --model fal-ai/flux/dev
  # add --force to overwrite, --only sable-rei,moss to render a subset

Notes:
  - Default --model is "fal-ai/flux-2" (confirmed working). Key in
    tools/keys/fal_key.txt (gitignored) or the FAL_KEY env var.
  - Replicate users: this script is fal-specific; the prompts JSON is portable,
    so a Replicate or local-ComfyUI runner can consume the same file.
"""
import argparse
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser(description="Batch-render NPC portraits from a portraits JSON via fal.ai.")
    ap.add_argument("--portraits", required=True, help="portraits JSON ({portraits:[{slug,prompt}]}).")
    ap.add_argument("--out", required=True, help="Output directory for <slug>.<ext> images.")
    ap.add_argument("--model", default="fal-ai/flux-2", help="fal image model slug (default fal-ai/flux-2, confirmed working).")
    ap.add_argument("--size", default="square_hd", help="fal image_size (default square_hd = 1024x1024).")
    ap.add_argument("--ext", default="png", help="Output extension (png/webp/jpg). Default png.")
    ap.add_argument("--only", help="Comma-separated slugs to render (default: all).")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files.")
    a = ap.parse_args()

    if not os.environ.get("FAL_KEY"):
        # Fallback: a gitignored fal_key.txt in tools/keys/ (legacy: next to this script).
        here = os.path.dirname(os.path.abspath(__file__))
        for keyfile in (os.path.join(here, os.pardir, "keys", "fal_key.txt"),
                        os.path.join(here, "fal_key.txt")):
            if os.path.exists(keyfile):
                os.environ["FAL_KEY"] = open(keyfile, encoding="utf-8").read().strip()
                break
    if not os.environ.get("FAL_KEY"):
        sys.exit("Set FAL_KEY in the environment, or put it in tools/keys/fal_key.txt "
                 "(gitignored). Get a key at https://fal.ai/dashboard/keys.")
    try:
        import fal_client
        import requests
    except ImportError:
        sys.exit("Missing deps. Run: pip install fal-client requests")

    data = json.load(open(a.portraits, encoding="utf-8-sig"))
    portraits = data.get("portraits") if isinstance(data, dict) else data
    if not portraits:
        sys.exit("No 'portraits' array found in the JSON.")
    only = set(s.strip() for s in a.only.split(",")) if a.only else None
    os.makedirs(a.out, exist_ok=True)

    rendered, skipped, failed = 0, 0, 0
    for p in portraits:
        slug, prompt = p.get("slug"), p.get("prompt")
        if not slug or not prompt or (only and slug not in only):
            continue
        dest = os.path.join(a.out, f"{slug}.{a.ext}")
        if os.path.exists(dest) and not a.force:
            print(f"  skip {slug} (exists)")
            skipped += 1
            continue
        print(f"  render {slug} ...", flush=True)
        try:
            args = {"prompt": prompt, "image_size": a.size, "num_images": 1}
            fmt = {"jpg": "jpeg"}.get(a.ext, a.ext)
            if fmt in ("png", "jpeg", "webp"):
                args["output_format"] = fmt
            result = fal_client.subscribe(a.model, arguments=args)
            url = (result.get("images") or [{}])[0].get("url")
            if not url:
                raise RuntimeError(f"no image url in result: {result}")
            img = requests.get(url, timeout=120)
            img.raise_for_status()
            with open(dest, "wb") as fh:
                fh.write(img.content)
            print(f"       -> {dest}")
            rendered += 1
        except Exception as e:                       # one failure should not kill the batch
            print(f"       ! failed: {e}", file=sys.stderr)
            failed += 1

    print(f"\nDone: {rendered} rendered, {skipped} skipped, {failed} failed -> {a.out}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
