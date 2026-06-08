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

Midjourney-only overrides: if the spec has an `mj` block, its keys replace the fal
text for MJ output: `mj.character` / `mj.wardrobe` / `mj.style` (e.g. anthro/furry
vocabulary so a beast-ancestry reads as fox-folk, not a human with fox ears), plus
`mj.artists` (style anchors) / `mj.version` / `mj.stylize` / `mj.negative` / `mj.ow`. CLI flags beat the mj block,
which beats the top-level fal values.

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


def as_list(v):
    if not v:
        return []
    if isinstance(v, str):
        return [s.strip() for s in v.split(",") if s.strip()]
    return [str(s).strip() for s in v if str(s).strip()]


def build_prompt(shot, character, wardrobe, style, artists, version, stylize, raw, negative):
    desc = f"{shot['framing'].strip()} {character.strip()}, {wardrobe.strip()}. {clean_style(style)}."
    if artists:
        desc += " in the style of " + ", ".join(artists) + "."
    parts = [desc, f"--ar {ar_of(shot.get('size'))}", f"--v {version}"]
    if raw:
        parts.append("--style raw")
    if stylize is not None:
        parts.append(f"--s {stylize}")
    parts.append(f"--no {negative}")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Print Midjourney prompts from a gen_npc_set set-spec.")
    ap.add_argument("--spec", required=True, help="Set-spec JSON (the same one gen_npc_set.py reads).")
    ap.add_argument("--version", help="Midjourney model version for --v (default 7; --oref is V7-only). Overrides spec mj.version.")
    ap.add_argument("--stylize", type=int, help="--s value (0-1000). Overrides spec mj.stylize.")
    ap.add_argument("--ow", type=int, help="Omni-weight for the consistency hint (0-1000, default 100). Overrides spec mj.ow.")
    ap.add_argument("--negative", help="Terms for --no. Overrides spec mj.negative.")
    ap.add_argument("--artists", help="Comma-separated style anchors -> 'in the style of ...'. Overrides spec mj.artists.")
    ap.add_argument("--no-raw", action="store_true", help="Drop --style raw.")
    a = ap.parse_args()

    spec = json.load(open(os.path.abspath(a.spec), encoding="utf-8-sig"))
    shots = spec.get("shots") or {}
    if not shots:
        sys.exit("No 'shots' in the spec.")
    mj = spec.get("mj") or {}
    slug = spec.get("slug", "npc")
    anchor = spec.get("anchor") or next(iter(shots))
    order = sorted(shots, key=lambda k: 0 if k == anchor else 1)

    # Precedence: CLI flag > spec mj.* override > top-level (fal) value / default.
    character = mj.get("character", spec.get("character", ""))
    wardrobe = mj.get("wardrobe", spec.get("wardrobe", ""))
    style = mj.get("style", spec.get("style", ""))
    artists = as_list(a.artists) if a.artists else as_list(mj.get("artists"))
    version = a.version or mj.get("version") or "7"
    stylize = a.stylize if a.stylize is not None else mj.get("stylize")
    negative = a.negative or mj.get("negative") or DEFAULT_NEG
    ow = a.ow if a.ow is not None else mj.get("ow", 100)
    raw = not a.no_raw

    print(f"# Midjourney prompts for {slug}  (--v {version})")
    print(f"# Paste each line as one /imagine. For a consistent set, generate the anchor")
    print(f"# ('{anchor}') first, then append  --oref <its image URL> --ow {ow}  to the")
    print(f"# others (or drag the anchor image into the prompt box). --oref is V7-only.\n")
    for key in order:
        tag = "  (anchor, make this first)" if key == anchor else ""
        print(f"## {key}{tag}")
        print(build_prompt(shots[key], character, wardrobe, style, artists, version, stylize, raw, negative))
        if key != anchor:
            print(f"#  consistent: append  --oref <{anchor} image URL> --ow {ow}")
        print()


if __name__ == "__main__":
    main()
