#!/usr/bin/env python3
"""Generate Wonderdraft art for the Tyrnarra pack. See README.md for the workflow and the lessons.

  assetgen.sh generate conifer --seeds 100-139        images + masks from the tower's ComfyUI
  assetgen.sh build conifer --keep 32                 cut, check, finish, install into the pack
  assetgen.sh test conifer                            real Wonderdraft export vs the built-in art

Every prompt style feeds the same pack folder (they look alike once greyscaled; together they
add variety). Work files: ~/.local/share/wdmap/assetgen/<family>/ (<style>/raw/, rejects.txt,
chosen.txt, sheet.jpg, compare-*.jpg).
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
    for style in a.style:
        raw = os.path.join(WORK, fam["name"], style, "raw")
        os.makedirs(raw, exist_ok=True)
        for seed in _seeds(a.seeds):
            img = os.path.join(raw, "%d.png" % seed)
            if os.path.exists(img):
                continue
            variants = fam.get("variants") or [""]
            prompt = (fam["subject"].format(variant=variants[seed % len(variants)])
                      + recipes.FRAME + ", " + recipes.STYLES[style])
            graph = comfy.sdxl_with_mask(prompt, recipes.NEGATIVE, seed, recipes.WIDTH, recipes.HEIGHT,
                                         recipes.CHECKPOINT, recipes.STEPS, recipes.CFG, recipes.SAMPLER,
                                         recipes.SCHEDULER, recipes.BG_MODEL,
                                         prefix="tyrnarra/%s_%s_%d" % (fam["name"], style, seed))
            t, (image, mask) = comfy.run(graph)
            with open(os.path.join(raw, "%d_mask.png" % seed), "wb") as f:
                f.write(mask)
            with open(os.path.join(raw, "%d.txt" % seed), "w") as f:
                f.write("%s\nnegative: %s\n%s %d steps cfg %s %s/%s %dx%d seed %d\n"
                        % (prompt, recipes.NEGATIVE, recipes.CHECKPOINT, recipes.STEPS, recipes.CFG,
                           recipes.SAMPLER, recipes.SCHEDULER, recipes.WIDTH, recipes.HEIGHT, seed))
            with open(img, "wb") as f:
                f.write(image)
            print("%s %s seed %d: %.1f s" % (fam["name"], style, seed, t), flush=True)


def cmd_build(a):
    from collections import Counter
    import sprites
    fam = _family(a.family)
    base = os.path.join(WORK, fam["name"])
    pool, rejects = [], []
    for style in a.style:
        raw = os.path.join(base, style, "raw")
        if not os.path.isdir(raw):
            continue
        seeds = sorted(int(f[:-4]) for f in os.listdir(raw) if f.endswith(".png") and "_mask" not in f)
        good = []
        for seed in seeds:
            rgba, why = sprites.cut(os.path.join(raw, "%d.png" % seed), os.path.join(raw, "%d_mask.png" % seed))
            why = why or sprites.check(rgba, fam)
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
    chosen = sorted(pool[: a.keep], key=lambda t: (t[0], t[1]))
    finished = [sprites.finish(c, fam, lv) for _, _, c, lv in chosen]
    folder = sprites.install(finished, fam)
    with open(os.path.join(base, "rejects.txt"), "w") as f:
        f.write("\n".join(rejects) + "\n")
    with open(os.path.join(base, "chosen.txt"), "w") as f:
        f.write("\n".join("%s <- %s seed %d" % (fam["file"].format(n=n), style, seed)
                          for n, (style, seed, _, _) in enumerate(chosen, 1)) + "\n")
    sheet = sprites.contact_sheet(finished, os.path.join(base, "sheet.jpg"))
    print("%s: %d usable, %d installed in %s; sheet %s" % (fam["name"], len(pool), len(finished), folder, sheet))
    print("  rejected: %s" % dict(Counter(r.split(": ", 1)[1].split(" (")[0] for r in rejects)))


def cmd_test(a):
    import wdtest
    fam = _family(a.family)
    out = os.path.join(WORK, fam["name"])
    for p in wdtest.run(fam, out, export=not a.no_export):
        print(p)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("generate", cmd_generate), ("build", cmd_build), ("test", cmd_test)):
        s = sub.add_parser(name)
        s.add_argument("family")
        if name != "test":
            s.add_argument("--style", type=lambda v: v.split(","), default=list(recipes.STYLES),
                           help="comma-separated prompt styles (default: all)")
        s.set_defaults(fn=fn)
        if name == "generate":
            s.add_argument("--seeds", default="1-40", help="e.g. 1-40 or 5,9,12-20")
        if name == "build":
            s.add_argument("--keep", type=int, default=32, help="variants to install")
            s.add_argument("--seed", type=int, default=7, help="shuffle seed for picking variants")
        if name == "test":
            s.add_argument("--no-export", action="store_true", help="only rebuild maps and crops")
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
