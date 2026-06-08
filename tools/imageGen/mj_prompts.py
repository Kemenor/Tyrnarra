#!/usr/bin/env python3
r"""
mj_prompts.py - emit Midjourney prompts from the same set-spec gen_npc_set.py uses.

A no-API companion to gen_npc_set.py: it does NOT call anything, it just prints
ready-to-paste Midjourney `/imagine` prompts so you can test a character in
Midjourney in parallel with the fal.ai render and compare. Same `<slug>.set.json`
in, Midjourney text out.

Per shot it assembles `framing + character + wardrobe + style` (the fal-style
"no text / no frame / no watermark" tail is moved into `--no`) and appends
Midjourney parameters: `--ar` (from each shot's size), `--v`, `--style raw`,
optional `--s` (stylize), and `--no`.

Consistency: Midjourney's character lock is the **omni-reference** (`--oref <image
URL> --ow <0-1000>`, default 100), which is **V7-only**. There is no URL until you
generate the anchor, so generate the anchor shot first, then append
`--oref <its image URL> --ow <n>` to the other shots (or drag the anchor image
into the prompt box). The footer of the output spells this out per shot.

Usage:
  python mj_prompts.py --spec ../../published/gm-notes/furrious-five/assets/portraits/sable-rei.set.json
  # --version 8.1 to test the newer model (no --oref there); --stylize 250; --ow 400
"""
import argparse
import json
import math
import os
import sys

# fal image_size presets -> Midjourney aspect ratios.
AR = {
    "square_hd": "1:1", "square": "1:1",
    "portrait_4_3": "3:4", "portrait_16_9": "9:16",
    "landscape_4_3": "4:3", "landscape_16_9": "16:9",
}
DEFAULT_NEG = "text, watermark, frame, border, signature"


def ar_of(size):
    if isinstance(size, dict):
        w, h = int(size.get("width", 1)), int(size.get("height", 1))
        g = math.gcd(w, h) or 1
        return f"{w // g}:{h // g}"
    if isinstance(size, str):
        if size in AR:
            return AR[size]
        if ":" in size:            # already an aspect ratio
            return size
    return "1:1"


def clean_style(style):
    # Drop the fal-style negative tail ("no text, no frame, no watermark."); it
    # belongs in --no for Midjourney.
    low = style.lower()
    i = low.find("no text")
    if i != -1:
        style = style[:i]
    return style.strip().rstrip(",;. ").strip()


def build_prompt(shot, spec, a):
    desc = f"{shot['framing'].strip()} {spec['character'].strip()}, {spec['wardrobe'].strip()}. {clean_style(spec['style'])}."
    parts = [desc, f"--ar {ar_of(shot.get('size'))}", f"--v {a.version}"]
    if not a.no_raw:
        parts.append("--style raw")
    if a.stylize is not None:
        parts.append(f"--s {a.stylize}")
    parts.append(f"--no {a.negative}")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Print Midjourney prompts from a gen_npc_set set-spec.")
    ap.add_argument("--spec", required=True, help="Set-spec JSON (the same one gen_npc_set.py reads).")
    ap.add_argument("--version", default="7", help="Midjourney model version for --v (default 7; --oref is V7-only).")
    ap.add_argument("--stylize", type=int, help="Optional --s value (0-1000; Midjourney default is 100).")
    ap.add_argument("--ow", type=int, default=100, help="Omni-weight for the consistency hint (0-1000, default 100).")
    ap.add_argument("--negative", default=DEFAULT_NEG, help="Terms for --no.")
    ap.add_argument("--no-raw", action="store_true", help="Drop --style raw.")
    a = ap.parse_args()

    spec = json.load(open(os.path.abspath(a.spec), encoding="utf-8-sig"))
    shots = spec.get("shots") or {}
    if not shots:
        sys.exit("No 'shots' in the spec.")
    slug = spec.get("slug", "npc")
    anchor = spec.get("anchor") or next(iter(shots))
    order = sorted(shots, key=lambda k: 0 if k == anchor else 1)

    print(f"# Midjourney prompts for {slug}  (--v {a.version})")
    print(f"# Paste each line as one /imagine. For a consistent set, generate the anchor")
    print(f"# ('{anchor}') first, then append  --oref <its image URL> --ow {a.ow}  to the")
    print(f"# others (or drag the anchor image into the prompt box). --oref is V7-only.\n")
    for key in order:
        tag = "  (anchor, make this first)" if key == anchor else ""
        print(f"## {key}{tag}")
        print(build_prompt(shots[key], spec, a))
        if key != anchor:
            print(f"#  consistent: append  --oref <{anchor} image URL> --ow {a.ow}")
        print()


if __name__ == "__main__":
    main()
