#!/usr/bin/env python3
r"""
mj_prompts.py - emit Midjourney prompts from the same set-spec gen_npc_set.py uses.

A no-API companion to gen_npc_set.py: it does NOT call anything, it just prints
ready-to-paste Midjourney `/imagine` prompts so you can test a character in
Midjourney in parallel with the fal.ai render and compare. Same `<slug>.set.json`
in, Midjourney text out.

Per shot it assembles `framing + character + wardrobe + style` and appends
Midjourney parameters: `--ar` (from each shot's size), `--v`, `--raw`, plus any of
`--s` (stylize), `--profile`, `--no` (negative) that are set.

Config resolves in layers, each overriding the previous:
  1. the spec's top-level (fal) fields,
  2. tools/imageGen/mj.defaults.json - house-wide Midjourney settings shared by
     every character: your personalization `profile`, default `style`, `version`,
     `raw`, `ow`,
  3. the spec's optional `mj` block - per-character overrides,
  4. CLI flags.
So your Midjourney personalization profile + house style live once in
mj.defaults.json and every character inherits them; a character's `mj` block only
carries what is specific to it (e.g. anthro/furry wording so a beast-ancestry reads
as fox-folk, not a human with fox ears).

With a `--profile` (or mj.profile / defaults) set, Midjourney pulls the look from a
personalization profile you trained, so you usually don't need artist names or a
heavy style string. Negatives (`--no`) and artist anchors are optional and OFF
unless you set them.

Consistency: Midjourney's character lock is the omni-reference (`--oref <image
URL> --ow <0-1000>`, V7-only). Generate the anchor shot first, then append
`--oref <its image URL> --ow <n>` to the other shots (or drag the anchor image in).
The footer prints that hint per shot.

Usage:
  python mj_prompts.py --spec ../../published/gm-notes/furrious-five/assets/portraits/sable-rei.set.json
  # --profile <id>; --version 8.1; --stylize 250; --ow 400; --artists "Brom, Donato Giancola"
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
    # Drop a fal-style negative tail ("no text, no frame, no watermark.") if a spec
    # falls back to its fal style; Midjourney does negatives via --no instead.
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


def build_prompt(shot, character, wardrobe, style, artists, profile, version, stylize, raw, negative):
    desc = f"{shot['framing'].strip()} {character.strip()}, {wardrobe.strip()}. {clean_style(style)}."
    if artists:
        desc += " in the style of " + ", ".join(artists) + "."
    parts = [desc, f"--ar {ar_of(shot.get('size'))}", f"--v {version}"]
    if raw:
        parts.append("--raw")
    if stylize is not None:
        parts.append(f"--s {stylize}")
    if profile:
        parts.append(f"--profile {profile}")
    if negative:
        parts.append(f"--no {negative}")
    return " ".join(parts)


def load_defaults(script_dir):
    path = os.path.join(script_dir, "mj.defaults.json")
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8-sig"))
    return {}


def main():
    ap = argparse.ArgumentParser(description="Print Midjourney prompts from a gen_npc_set set-spec.")
    ap.add_argument("--spec", required=True, help="Set-spec JSON (the same one gen_npc_set.py reads).")
    ap.add_argument("--profile", help="Midjourney personalization profile id for --profile. Overrides mj.profile / defaults.")
    ap.add_argument("--version", help="Model version for --v (default 7; --oref is V7-only). Overrides mj.version / defaults.")
    ap.add_argument("--stylize", type=int, help="--s value (0-1000; off unless set). Overrides mj.stylize / defaults.")
    ap.add_argument("--ow", type=int, help="Omni-weight for the consistency hint (default 100). Overrides mj.ow / defaults.")
    ap.add_argument("--negative", help="Terms for --no (off unless set). Overrides mj.negative / defaults.")
    ap.add_argument("--artists", help="Comma-separated style anchors -> 'in the style of ...' (off unless set). Overrides mj.artists / defaults.")
    ap.add_argument("--anchor-url", help="URL of the rendered anchor image; bakes --oref <url> --ow into the non-anchor prompts.")
    ap.add_argument("--no-raw", action="store_true", help="Drop --raw.")
    a = ap.parse_args()

    spec = json.load(open(os.path.abspath(a.spec), encoding="utf-8-sig"))
    shots = spec.get("shots") or {}
    if not shots:
        sys.exit("No 'shots' in the spec.")
    d = load_defaults(os.path.dirname(os.path.abspath(__file__)))   # mj.defaults.json (house-wide)
    mj = spec.get("mj") or {}
    slug = spec.get("slug", "npc")
    anchor = spec.get("anchor") or next(iter(shots))
    order = sorted(shots, key=lambda k: 0 if k == anchor else 1)

    # Precedence: CLI flag > spec mj.* > mj.defaults.json > top-level (fal) / built-in.
    def layered(key, fal_default=None):
        if key in mj:
            return mj[key]
        if key in d:
            return d[key]
        return fal_default

    character = layered("character", spec.get("character", ""))
    wardrobe = layered("wardrobe", spec.get("wardrobe", ""))
    style = layered("style", spec.get("style", ""))
    artists = as_list(a.artists) if a.artists else as_list(layered("artists"))
    profile = a.profile or layered("profile")
    version = a.version or layered("version") or "7"
    stylize = a.stylize if a.stylize is not None else layered("stylize")
    negative = a.negative or layered("negative")
    ow = a.ow if a.ow is not None else layered("ow")
    if ow is None:
        ow = 100
    raw = False if a.no_raw else bool(layered("raw", True))

    print(f"# Midjourney prompts for {slug}  (--v {version}{', profile' if profile else ''})")
    print(f"# Paste each line as one /imagine. For a consistent set, generate the anchor")
    print(f"# ('{anchor}') first, then append  --oref <its image URL> --ow {ow}  to the")
    print(f"# others (or drag the anchor image into the prompt box). --oref is V7-only.\n")
    for key in order:
        tag = "  (anchor, make this first)" if key == anchor else ""
        print(f"## {key}{tag}")
        line = build_prompt(shots[key], character, wardrobe, style, artists, profile, version, stylize, raw, negative)
        if key != anchor and a.anchor_url:
            line += f" --oref {a.anchor_url} --ow {ow}"
        print(line)
        if key != anchor and not a.anchor_url:
            print(f"#  consistent: append  --oref <{anchor} image URL> --ow {ow}")
        print()


if __name__ == "__main__":
    main()
