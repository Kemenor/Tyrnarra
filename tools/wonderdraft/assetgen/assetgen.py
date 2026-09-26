#!/usr/bin/env python3
"""Generate Wonderdraft art for the Tyrnarra pack. See README.md for the workflow and the lessons.

  assetgen.sh generate conifer --seeds 100-139        images + masks from the tower's ComfyUI
  assetgen.sh build conifer --keep 32                 cut, check, finish, install into the pack
  assetgen.sh test conifer --round 7                  real Wonderdraft export vs the art Main uses now
  assetgen.sh test conifer --round 7 --offline        the same drawn here (render.py), no Wonderdraft

Every prompt style feeds the same pack folder (they look alike once greyscaled; together they
add variety). Work files: ~/.local/share/wdmap/assetgen/<family>/ (<style>/raw/, rejects.txt,
chosen.txt, sheet.jpg, compare-*.jpg; with --round N all but raw/ in round-N/, plus the sprites).
"""
import argparse
import os
import random
import sys

import comfy
import recipes

WORK = os.path.expanduser("~/.local/share/wdmap/assetgen")


def _seeds(spec):
    out = []
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out.extend(range(int(a), int(b or a) + 1))
    return out


def _family(name):
    if name not in recipes.FAMILIES:
        sys.exit("unknown family %r; known: %s" % (name, ", ".join(recipes.FAMILIES)))
    return dict(recipes.FAMILIES[name], name=name)


def cmd_generate(a):
    fam = _family(a.family)
    if not comfy.HOST:
        sys.exit("No ComfyUI address: set TYRNARRA_COMFY or write it to %s (README: Setup)" % comfy.URL_FILE)
    if not comfy.alive():
        sys.exit("ComfyUI at %s is not answering; start it in LAN mode on the tower (README: Setup)" % comfy.HOST)
    engine = a.engine or fam.get("engine", "sdxl")
    width, height = fam.get("canvas", (recipes.WIDTH, recipes.HEIGHT))
    negative = fam.get("negative", recipes.NEGATIVE)
    for style in a.style or recipes.styles(fam):
        raw = os.path.join(WORK, fam["name"], style, "raw")
        os.makedirs(raw, exist_ok=True)
        todo = []
        for seed in _seeds(a.seeds):
            if os.path.exists(os.path.join(raw, "%d.png" % seed)):
                continue
            todo.append((seed, recipes.prompt(fam, style, seed, engine)))
        if engine == "flux":
            # Several images per graph: the FLUX stack loads once for all of them.
            for i in range(0, len(todo), recipes.FLUX_BATCH):
                batch = todo[i:i + recipes.FLUX_BATCH]
                graph = comfy.flux_images([(p, seed, width, height) for seed, p in batch],
                                          prefix="tyrnarra/%s_%s" % (fam["name"], style))
                t, images = comfy.run(graph, timeout=3600)
                for (seed, prompt), image in zip(batch, images):
                    _save(raw, seed, image, None, "%s\nFLUX.2 dev Q4 + Turbo LoRA, 8 steps, guidance 4, %dx%d seed %d\n"
                          % (prompt, width, height, seed))
                print("%s %s seeds %s: %.0f s" % (fam["name"], style, ",".join(str(s) for s, _ in batch), t), flush=True)
            continue
        for seed, prompt in todo:
            graph = comfy.sdxl_with_mask(prompt, negative, seed, width, height,
                                         recipes.CHECKPOINT, recipes.STEPS, recipes.CFG, recipes.SAMPLER,
                                         recipes.SCHEDULER, recipes.BG_MODEL,
                                         prefix="tyrnarra/%s_%s_%d" % (fam["name"], style, seed))
            t, (image, mask) = comfy.run(graph)
            _save(raw, seed, image, mask, "%s\nnegative: %s\n%s %d steps cfg %s %s/%s %dx%d seed %d\n"
                  % (prompt, negative, recipes.CHECKPOINT, recipes.STEPS, recipes.CFG,
                     recipes.SAMPLER, recipes.SCHEDULER, width, height, seed))
            print("%s %s seed %d: %.1f s" % (fam["name"], style, seed, t), flush=True)


def _save(raw, seed, image, mask, settings):
    """One generated image, its mask (none for FLUX: sprites.flood_mask cuts it) and its settings."""
    if mask is not None:
        with open(os.path.join(raw, "%d_mask.png" % seed), "wb") as f:
            f.write(mask)
    with open(os.path.join(raw, "%d.txt" % seed), "w") as f:
        f.write(settings)
    with open(os.path.join(raw, "%d.png" % seed), "wb") as f:
        f.write(image)


def _out(fam, n):
    """Where a family's (or one round's) build and test files go."""
    out = os.path.join(WORK, fam["name"], *(["round-%d" % n] if n else []))
    os.makedirs(out, exist_ok=True)
    return out


def cmd_build(a):
    from collections import Counter
    import shutil
    import sprites
    fam = _family(a.family)
    base = os.path.join(WORK, fam["name"])
    out = _out(fam, a.round)
    for kv in a.set or []:
        # Finishing experiments without editing recipes.py: --set OUTLINE=3 --set INNER_LIGHTEN=0.5
        key, _, value = kv.partition("=")
        if not hasattr(recipes, key):
            sys.exit("recipes.py has no %s" % key)
        setattr(recipes, key, float(value) if "." in value else int(value))
    if a.no_install and not a.round:
        sys.exit("--no-install needs --round (the sprites go to its folder only)")
    pool, rejects = [], []
    for style in a.style or recipes.styles(fam):
        raw = os.path.join(base, style, "raw")
        if not os.path.isdir(raw):
            continue
        seeds = sorted(int(f[:-4]) for f in os.listdir(raw) if f.endswith(".png") and "_mask" not in f)
        if a.seeds:
            wanted = set(_seeds(a.seeds))
            seeds = [s for s in seeds if s in wanted]
        good = []
        for seed in seeds:
            rgba, why = sprites.cut(os.path.join(raw, "%d.png" % seed), os.path.join(raw, "%d_mask.png" % seed),
                                    fam.get("shape", "tree"))
            why = why or sprites.check(rgba, fam)
            if not why and fam.get("draw") != "custom_colors":
                rgba = sprites.thin_ink(rgba, recipes.INK_THIN)   # greyscale; icons keep their colours
            (rejects.append("%s %d: %s" % (style, seed, why)) if why else good.append((seed, rgba)))
        if not good:
            print("%s: nothing usable from %d images" % (style, len(seeds)))
            continue
        # Levels per prompt style (their ink differs), so every style lands on the same brightness.
        lv = sprites.levels([c for _, c in good])
        pool += [(style, seed, c, lv) for seed, c in good]
        print("%s: %d images, %d usable (levels %.0f-%.0f, gamma %.2f)"
              % (style, len(seeds), len(good), lv[0], lv[1], lv[2]))
    if not pool:
        sys.exit("nothing usable")
    random.Random(a.seed).shuffle(pool)
    if "items" in fam:
        # Named icons: up to per_item usable drawings of each item, files "<item>_<k>".
        chosen, names, missing = [], [], []
        for i, (item, _) in enumerate(fam["items"]):
            got = sorted([t for t in pool if t[1] % len(fam["items"]) == i], key=lambda t: (t[0], t[1]))
            got = [t for t in pool if t in got][: fam.get("per_item", 1)]
            missing += [item] if not got else []
            chosen += got
            names += [fam["file"].format(item=item, n=k) for k in range(1, len(got) + 1)]
        if missing:
            print("  no usable drawing yet for: %s" % ", ".join(missing))
    else:
        chosen = sorted(pool[: a.keep], key=lambda t: (t[0], t[1]))
        names = [fam["file"].format(n=n) for n in range(1, len(chosen) + 1)]
    finished = [sprites.finish(c, fam, lv) for _, _, c, lv in chosen]
    if a.no_install:
        folder = sprites.install(finished, fam, os.path.join(out, "sprites"), names)
    else:
        folder = sprites.install(finished, fam, names=names)
    if a.round and not a.no_install:
        # A copy of the round's sprites, for comparing rounds after the next build replaced them.
        shutil.rmtree(os.path.join(out, "sprites"), ignore_errors=True)
        shutil.copytree(folder, os.path.join(out, "sprites"))
    if a.set:
        with open(os.path.join(out, "settings.txt"), "w") as f:
            f.write("\n".join(a.set) + "\n")
    with open(os.path.join(out, "rejects.txt"), "w") as f:
        f.write("\n".join(rejects) + "\n")
    with open(os.path.join(out, "chosen.txt"), "w") as f:
        f.write("\n".join("%s <- %s seed %d" % (name, style, seed)
                          for name, (style, seed, _, _) in zip(names, chosen)) + "\n")
    sheet = sprites.contact_sheet(finished, os.path.join(out, "sheet.jpg"), cc=fam.get("draw") == "custom_colors")
    print("%s: %d usable, %d installed in %s; sheet %s" % (fam["name"], len(pool), len(finished), folder, sheet))
    print("  rejected: %s" % dict(Counter(r.split(": ", 1)[1].split(" (")[0] for r in rejects)))


def cmd_test(a):
    import wdtest
    fam = _family(a.family)
    out = _out(fam, a.round)
    if a.offline:
        paths = wdtest.offline(fam, out, a.round)
    else:
        paths = wdtest.run(fam, out, export=not a.no_export, n=a.round)
    for p in paths:
        print(p)


def cmd_builtin_refs(a):
    import wdtest
    wdtest.builtin_refs(export=not a.no_export)


def cmd_measure(a):
    import packswap
    packswap.measure(export=not a.no_export)


def cmd_packswap(a):
    import packswap
    if a.apply:
        packswap.apply(os.path.abspath(os.path.expanduser(a.apply)))
        return
    path = packswap.make_swapped()
    if not a.no_export:
        import wd_export
        wd_export.export_views([path])
    packswap.compare(os.path.join(WORK, "packswap"))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn, text in (("measure-builtins", cmd_measure, "measure the built-in art's sizes (one export)"),
                           ("builtin-refs", cmd_builtin_refs, "built-in art as local reference sprites (two exports)"),
                           ("packswap", cmd_packswap, "Base view with built-ins swapped per pack-swap.json, exported")):
        s = sub.add_parser(name, help=text)
        s.add_argument("--no-export", action="store_true", help="reuse the last export")
        if name == "packswap":
            s.add_argument("--apply", metavar="MAP", help="swap this map in place (with backup) instead of a test copy")
        s.set_defaults(fn=fn)
    for name, fn in (("generate", cmd_generate), ("build", cmd_build), ("test", cmd_test)):
        s = sub.add_parser(name)
        s.add_argument("family")
        if name != "test":
            s.add_argument("--style", type=lambda v: v.split(","),
                           help="comma-separated prompt styles (default: the family's)")
        s.set_defaults(fn=fn)
        if name == "generate":
            s.add_argument("--seeds", default="1-40", help="e.g. 1-40 or 5,9,12-20")
            s.add_argument("--engine", choices=("sdxl", "flux"), help="override the family's engine")
        if name == "build":
            s.add_argument("--keep", type=int, default=32, help="variants to install")
            s.add_argument("--seeds", help="only these generated seeds, e.g. 101-200 (default: all)")
            s.add_argument("--seed", type=int, default=7, help="shuffle seed for picking variants")
            s.add_argument("--set", action="append", metavar="KEY=VALUE",
                           help="override a finishing constant of recipes.py, e.g. OUTLINE=3 (repeatable)")
            s.add_argument("--no-install", action="store_true",
                           help="with --round: write the sprites to the round's folder only, not the pack")
        if name in ("build", "test"):
            s.add_argument("--round", type=int, help="round number: keep this round's files apart (README: Results log)")
        if name == "test":
            s.add_argument("--no-export", action="store_true", help="only rebuild maps and crops")
            s.add_argument("--offline", action="store_true",
                           help="draw the comparison here (render.py) instead of exporting with Wonderdraft")
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
