#!/usr/bin/env python3
"""Stitch a magirail consist into one battlemap + merged clickable-area JSON.

Cars are the Tom Cartos "Steam Train" modular set (uniform 14x5 grid). A consist
is an ordered list of cars laid front-to-rear over a 14x7 terrain background, so
each car leaves one square of ground top and bottom for movement around the
train. Per-car area files in areas/ (drawn once on the bare car) are
offset-and-scaled into each car's slot in the consist; any car without an area
file gets a single whole-car area as a fallback.

Image stitching uses ImageMagick (`magick`); the area math is pure Python.

Run from the repo root, e.g.:

  python tools/map-library/stitch.py \
    --consist "01 Engine,28 Cargo Coal,24 Military Transport,14 Steerage,23 Cannons,03 Crew Quarters" \
    --terrain Rock --out narrows-job-train --maps published/gm-notes/furrious-five/assets/maps

Outputs: <maps>/_full/<out>.webp (full-res, gitignored), <maps>/<out>.webp
(downsized web copy), and <maps>/<out>.areas.json. Pass --verify to also write
<maps>/_full/<out>_verify.png with the merged areas drawn on, for a visual check.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRAINS = HERE / "_full" / "trains" / "Modular Trains"
BG = HERE / "_full" / "trains" / "Seemless Background"
AREAS = HERE / "areas"

CAR_W, CAR_H = 1960, 700   # 14x5 at 140px/square
BG_W, BG_H = 1960, 980     # 14x7

# Vertical band the cars occupy on a 14x7 background, in percent.
BAND_TOP = (BG_H - CAR_H) / 2 / BG_H * 100   # 14.2857
BAND_H = CAR_H / BG_H * 100                  # 71.4286
Y_OFFSET = (BG_H - CAR_H) // 2               # 140 px


def parse_token(token):
    """'14 Steerage:detailed' -> ('14 Steerage', 'detailed'); else (token, None)."""
    if ":" in token:
        base, variant = token.split(":", 1)
        return base.strip(), variant.strip()
    return token.strip(), None


def area_file(token):
    base, variant = parse_token(token)
    suffix = f".{variant}" if variant else ""
    return AREAS / f"TC_ST Car {base}_14x5.areas{suffix}.json"


def car_path(token):
    p = TRAINS / f"TC_ST Car {token}_14x5.webp"
    if not p.exists():
        sys.exit(f"car not found: {p}")
    return p


def bg_path(terrain):
    cand = sorted(BG.glob(f"TC_ST Background *{terrain}*_No Grid_14x7.webp"))
    # Prefer the day variant (the one without 'Night' in the name).
    day = [c for c in cand if "Night" not in c.name]
    if day:
        return day[0]
    if cand:
        return cand[0]
    sys.exit(f"background not found for terrain '{terrain}'")


def magick(*args):
    subprocess.run(["magick", *map(str, args)], check=True)


def stitch_image(cars, bg, out_full, out_web, web_width):
    out_full.parent.mkdir(parents=True, exist_ok=True)
    band = out_full.parent / "_band.png"
    strip = out_full.parent / "_strip.png"
    magick(*cars, "+append", band)
    magick(*([bg] * len(cars)), "+append", strip)
    magick(strip, band, "-geometry", f"+0+{Y_OFFSET}", "-composite", out_full)
    band.unlink()
    strip.unlink()
    out_web.parent.mkdir(parents=True, exist_ok=True)
    magick(out_full, "-resize", f"{web_width}x", out_web)


def merge_areas(tokens, out_name):
    n = len(tokens)
    slot = 100.0 / n
    out = {"image": f"{out_name}.webp", "areas": []}
    for i, token in enumerate(tokens):
        af = area_file(token)
        if af.exists():
            data = json.loads(af.read_text(encoding="utf-8"))
            for a in data["areas"]:
                rects = [{
                    "left": round(i * slot + r["left"] / 100 * slot, 3),
                    "top": round(BAND_TOP + r["top"] / 100 * BAND_H, 3),
                    "width": round(r["width"] / 100 * slot, 3),
                    "height": round(r["height"] / 100 * BAND_H, 3),
                } for r in a["rects"]]
                out["areas"].append({"label": a["label"], "desc": a.get("desc", ""), "rects": rects})
        else:
            out["areas"].append({
                "label": parse_token(token)[0],
                "desc": "",
                "rects": [{"left": round(i * slot, 3), "top": round(BAND_TOP, 3),
                           "width": round(slot, 3), "height": round(BAND_H, 3)}],
            })
    return out


def verify_overlay(out_web, areas, out_png):
    dims = subprocess.run(["magick", "identify", "-format", "%w %h", str(out_web)],
                          check=True, capture_output=True, text=True).stdout.split()
    w, h = int(dims[0]), int(dims[1])
    args = [str(out_web), "-strokewidth", "2"]
    for a in areas["areas"]:
        for r in a["rects"]:
            x1 = r["left"] / 100 * w
            y1 = r["top"] / 100 * h
            x2 = (r["left"] + r["width"]) / 100 * w
            y2 = (r["top"] + r["height"]) / 100 * h
            args += ["-stroke", "red", "-fill", "rgba(255,40,40,0.10)",
                     "-draw", f"rectangle {x1:.0f},{y1:.0f} {x2:.0f},{y2:.0f}"]
            args += ["-stroke", "none", "-fill", "yellow", "-pointsize", "13",
                     "-draw", f"text {x1 + 3:.0f},{y1 + 14:.0f} '{a['label'][:18]}'"]
    magick(*args, out_png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--consist", required=True,
                    help="comma list of car tokens, e.g. '01 Engine,28 Cargo Coal'")
    ap.add_argument("--terrain", default="Rock")
    ap.add_argument("--out", required=True)
    ap.add_argument("--maps", required=True,
                    help="campaign maps dir, e.g. published/gm-notes/furrious-five/assets/maps")
    ap.add_argument("--web-width", type=int, default=3000)
    ap.add_argument("--no-image", action="store_true", help="only (re)generate the areas JSON")
    ap.add_argument("--verify", action="store_true", help="also write _verify.png with areas drawn")
    a = ap.parse_args()

    tokens = [t.strip() for t in a.consist.split(",") if t.strip()]
    maps = Path(a.maps)
    out_full = maps / "_full" / f"{a.out}.webp"
    out_web = maps / f"{a.out}.webp"

    if not a.no_image:
        cars = [car_path(parse_token(t)[0]) for t in tokens]
        stitch_image(cars, bg_path(a.terrain), out_full, out_web, a.web_width)

    areas = merge_areas(tokens, a.out)
    (maps / f"{a.out}.areas.json").write_text(json.dumps(areas, indent=2), encoding="utf-8")

    if a.verify and not a.no_image:
        verify_overlay(out_web, areas, maps / "_full" / f"{a.out}_verify.png")

    detail = sum(1 for t in tokens if area_file(t).exists())
    print(f"cars: {len(tokens)}  ({detail} with per-car detail)  "
          f"areas: {len(areas['areas'])}  -> {out_web} (+ .areas.json)")


if __name__ == "__main__":
    main()
