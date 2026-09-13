#!/usr/bin/env python3
r"""
fal_art.py - hosted NPC art renderer. CLAUDE-OPERATED: the user never runs this.

The cloud sibling of npc_art.py. Same spec, same prompts, same stage names; the
render happens on fal.ai instead of the local GPU, so it works while the local
ComfyUI box is busy, broken, or swap-thrashing, and it can reach models the
local install does not have (Nano Banana Pro, Seedream).

WHY THIS IMPORTS npc_art: prompt parity. `character` + `wardrobe` + `framing` +
house style are assembled by npc_art.prompt_for(), and the size names and the
KEEP-the-same-character instruction come from npc_art too. If this module
rebuilt its own prompts they would drift, and a local-vs-hosted comparison
would be measuring the prompt difference rather than the model difference.
Only constants and pure functions are imported; nothing in npc_art runs at
import time, so importing it never touches the local ComfyUI server.

Stdlib only, like npc_art (no fal-client, no requests, no pip step). Reference
images go up as base64 data URIs, which fal accepts for image inputs, so there
is no separate upload step to get wrong.

Spec: the SAME <slug>.set.json npc_art uses. A spec rendered locally can be
re-rendered here with no edits.

Stages:
  python3 fal_art.py variations --spec <spec> [--count 2] [--model flux2]
  python3 fal_art.py set        --spec <spec> --draft 1 [--scene "extra"] [--only k,k]
  python3 fal_art.py upscale    --spec <spec> [--scale 2]
  python3 fal_art.py bakeoff    --spec <spec> [--models flux2,nano-banana-pro,seedream4]
  python3 fal_art.py models
  ...any render stage also takes --dry-run, which prints the prompts and the
  cost estimate and spends nothing.

`bakeoff` renders the same spec through several models into
<out>/bakeoff/<model>/ so the shots can be compared side by side without
touching the committed art. That is the intended first use: pick the house
model on this project's own NPCs rather than on someone's benchmark.

Key: FAL_KEY in the environment, else tools/keys/falai.key (gitignored).
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import npc_art
except Exception as e:                      # a half-edited npc_art must say so
    sys.exit(f"fal_art needs npc_art.py beside it for the shared prompt builder "
             f"(import failed: {e})")

QUEUE = "https://queue.fal.run"


# ----------------------------------------------------------------- backends
#
# One entry per model family. The three differ in how they take a size and
# what a reference image costs, and nothing else that matters here.
#
# "price" is an ESTIMATE in USD per 1MP image, for the running total this
# module prints. fal changes prices without telling us; the dashboard is the
# authority. Treat the total as "am I about to spend cents or dollars", never
# as billing.

def _size_flux(size):
    """fal's own size enum; the spec already speaks it."""
    return {"image_size": size}


_ASPECT = {"square_hd": "1:1", "square": "1:1", "portrait_4_3": "3:4",
           "portrait_16_9": "9:16", "landscape_4_3": "4:3",
           "landscape_16_9": "16:9"}


def _size_nb(size):
    """Nano Banana Pro takes aspect_ratio + resolution, not a size enum.
    portrait_4_3 is a PORTRAIT of 4:3 proportions, i.e. 3:4 width:height."""
    return {"aspect_ratio": _ASPECT.get(size, "3:4"), "resolution": "1K"}


BACKENDS = {
    "flux2": {
        "t2i": "fal-ai/flux-2",
        "edit": "fal-ai/flux-2/edit",          # image_urls, max 4 references
        "size": _size_flux,
        "max_refs": 4,
        "price": {"t2i": 0.030, "edit": 0.045},
        "note": "the local pipeline's model; the like-for-like comparison",
    },
    "nano-banana-pro": {
        "t2i": "fal-ai/nano-banana-pro",
        "edit": "fal-ai/nano-banana-pro/edit",
        "size": _size_nb,
        "max_refs": 14,
        "price": {"t2i": 0.150, "edit": 0.150},
        "note": "strongest identity consistency; pulls toward photoreal",
    },
    "seedream4": {
        # NOTE: the /edit id is confirmed from fal's docs; the text-to-image id
        # follows fal's naming and is unverified. A wrong id fails loudly at
        # submit with a 404, so it cannot silently render the wrong thing.
        "t2i": "fal-ai/bytedance/seedream/v4/text-to-image",
        "edit": "fal-ai/bytedance/seedream/v4/edit",
        "size": _size_flux,
        "max_refs": 10,
        "price": {"t2i": 0.030, "edit": 0.030},
        "note": "cheapest; reviews favour it for stylised fantasy lighting",
    },
}
DEFAULT_MODEL = "flux2"


def backend(name):
    if name not in BACKENDS:
        sys.exit(f"unknown model '{name}'; known: {', '.join(BACKENDS)}")
    return BACKENDS[name]


# ----------------------------------------------------------------- key + http

def load_key():
    if os.environ.get("FAL_KEY"):
        return os.environ["FAL_KEY"]
    here = os.path.dirname(os.path.abspath(__file__))
    for kf in (os.path.join(here, os.pardir, "keys", "falai.key"),
               os.path.join(here, os.pardir, "keys", "fal_key.txt")):  # legacy name
        if os.path.exists(kf):
            return open(kf, encoding="utf-8").read().strip()
    sys.exit("No fal key. Set FAL_KEY, or put it in tools/keys/falai.key "
             "(gitignored). Keys: https://fal.ai/dashboard/keys")


def _post(url, payload, key, timeout=60):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def _get(url, key, timeout=60):
    req = urllib.request.Request(url, headers={"Authorization": f"Key {key}"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def _http_detail(e):
    """fal puts the useful part (which field it disliked, and why) in the
    RESPONSE BODY of a 4xx, not in the status line. Read it or debug blind."""
    try:
        return e.read().decode()[:900]
    except Exception:
        return "<no body>"


def data_uri(path):
    """Reference images travel inline as base64. Avoids fal's upload endpoint
    (and therefore the fal-client dependency) at the cost of a fatter request;
    a 1MP png is ~1.5 MB base64, which is fine."""
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def submit(endpoint, args, key, label, timeout=900):
    """Queue one job and wait for it. Returns the result JSON.

    Polls the status_url fal hands back rather than rebuilding the path: model
    ids are nested to different depths (fal-ai/flux-2/edit vs
    fal-ai/bytedance/seedream/v4/edit) and the returned URLs are always right.
    """
    try:
        sub = _post(f"{QUEUE}/{endpoint}", args, key)
    except urllib.error.HTTPError as e:
        sys.exit(f"{label}: fal rejected the submit ({e.code}) on {endpoint}: "
                 f"{_http_detail(e)}")
    status_url, result_url = sub["status_url"], sub["response_url"]
    t0 = last = time.time()
    while True:
        time.sleep(3)
        now = time.time()
        try:
            st = _get(status_url, key, timeout=30)
        except Exception:
            continue                                # transient; keep polling
        state = st.get("status")
        if state == "COMPLETED":
            # COMPLETED means the job left the queue, NOT that it succeeded: a
            # validation or policy rejection surfaces as a 4xx with the reason
            # in the body of the result fetch.
            try:
                return _get(result_url, key, timeout=120)
            except urllib.error.HTTPError as e:
                sys.exit(f"{label}: fal returned no result ({e.code}) from "
                         f"{endpoint}: {_http_detail(e)}")
        if state in ("FAILED", "ERROR"):
            sys.exit(f"{label}: render failed: {json.dumps(st)[:600]}")
        if now - last >= 20:                        # same heartbeat habit as npc_art
            last = now
            el = f"{int(now - t0) // 60}m{int(now - t0) % 60:02d}s"
            where = (f"queued behind {st.get('queue_position')}"
                     if state == "IN_QUEUE" else "rendering")
            print(f"    ... {label}: {el} elapsed, {where}", flush=True)
        if now - t0 > timeout:
            sys.exit(f"{label}: timed out after {timeout // 60} min")


def download(url, dest):
    with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as fh:
        fh.write(r.read())


def first_url(res, label):
    imgs = res.get("images") or []
    if not imgs or not imgs[0].get("url"):
        sys.exit(f"{label}: no image in result: {json.dumps(res)[:500]}")
    return imgs[0]["url"]


# ----------------------------------------------------------------- spend

class Spend:
    """Running cost estimate for one pass, printed at the end. Cheap insurance
    against discovering a bake-off cost real money only on the invoice."""

    def __init__(self, model):
        self.model, self.total, self.calls = model, 0.0, 0

    def add(self, kind):
        self.total += BACKENDS[self.model]["price"][kind]
        self.calls += 1

    def report(self):
        print(f"  ~${self.total:.2f} est. for {self.calls} render(s) on "
              f"{self.model} (estimate, check the fal dashboard)", flush=True)


# ----------------------------------------------------------------- render

def render_shot(spec, shot, model, key, seed, ref_path=None, extra="",
                dry_run=False, label="shot"):
    """One shot. With ref_path it is an edit referencing that image (identity
    carries over); without, a fresh text-to-image."""
    b = backend(model)
    is_edit = ref_path is not None
    prompt = npc_art.prompt_for(spec, shot, is_edit=is_edit, extra=extra)
    size = shot.get("size", "portrait_4_3")
    # Before anything touches the reference file: a dry run must work when the
    # references do not exist yet, which is the whole point of previewing.
    if dry_run:
        print(f"  [dry-run] {label} [{'ref' if is_edit else 'text'}] {size}\n"
              f"           {prompt}", flush=True)
        return None
    args = {"prompt": prompt, "num_images": 1, "seed": seed}
    args.update(b["size"](size))
    if model != "nano-banana-pro":
        args["output_format"] = "png"           # nb-pro defaults to png already
    if is_edit:
        args["image_urls"] = [data_uri(ref_path)]
    return first_url(submit(b["edit"] if is_edit else b["t2i"], args, key, label),
                     label)


def variations(spec_path, count=2, seed=None, model=DEFAULT_MODEL, dry_run=False,
               out_dir=None, write_meta=True):
    """N takes on the anchor shot, for the user to pick from.

    Default 2 here rather than npc_art's 1: hosted models actually move between
    seeds (npc_art's 1 is a workaround for the Turbo LoRA at 8 steps barely
    differing), and a second take costs cents.
    """
    spec, spec_out = npc_art.load_spec(spec_path)
    out_dir = out_dir or spec_out
    key = load_key()
    anchor = spec["shots"][spec.get("anchor") or next(iter(spec["shots"]))]
    seed = seed if seed is not None else int.from_bytes(os.urandom(4), "big")
    vdir = os.path.join(out_dir, "variations")
    os.makedirs(vdir, exist_ok=True)
    spend, paths = Spend(model), []
    print(f"  {count} variations on {model} (base seed {seed}) ...", flush=True)
    for i in range(count):
        lbl = f"v{i + 1}"
        url = render_shot(spec, anchor, model, key, seed + i, dry_run=dry_run,
                          label=lbl)
        spend.add("t2i")
        if dry_run:
            continue
        dest = os.path.join(vdir, f"{spec.get('slug', 'npc')}-{lbl}.png")
        download(url, dest)
        paths.append(dest)
        print(f"        -> {dest}", flush=True)
    spend.report()
    if not dry_run and write_meta:
        npc_art.save_render_meta(spec_path, spec, variations_seed=seed,
                                 variations_count=count, variations_model=model)
    return paths


def render_set(spec_path, draft=None, scene_extra="", only=None, force=False,
               seed=None, model=DEFAULT_MODEL, dry_run=False, out_dir=None,
               write_meta=True):
    """Anchor first, then every other shot referencing it.

    Identity chain, same as npc_art: the chosen variation anchors the anchor
    shot, the anchor shot anchors the rest. A shot with "mode": "text" renders
    fresh and WILL come back as a different person; that is what it is for, and
    it is wrong for portraits.
    """
    spec, spec_out = npc_art.load_spec(spec_path)
    out_dir = out_dir or spec_out
    os.makedirs(out_dir, exist_ok=True)
    key = load_key()
    shots = spec["shots"]
    anchor_key = spec.get("anchor") or next(iter(shots))
    want = [k for k in shots if not only or k in only]
    seed = (seed if seed is not None
            else spec.get("render", {}).get("set_seed")
            or int.from_bytes(os.urandom(4), "big"))
    spend, out = Spend(model), {}

    def dest_of(k):
        return os.path.join(out_dir, f"{shots[k]['file']}.png")

    def mode_of(k):
        return "text" if k == anchor_key else shots[k].get("mode", "ref")

    # 1) the anchor, referencing the chosen variation when there is one
    anchor_dest = dest_of(anchor_key)
    if anchor_key in want and (force or not os.path.exists(anchor_dest)):
        ref = None
        if draft:
            ref = os.path.join(out_dir, "variations",
                               f"{spec.get('slug', 'npc')}-v{draft}.png")
            if not os.path.exists(ref):
                # A dry run never opens the file, so a missing variation must
                # not stop it: previewing the prompts BEFORE rendering any
                # variations is exactly when the preview is most useful.
                if not dry_run:
                    sys.exit(f"variation not found: {ref}")
                print(f"  ! variation not found ({ref}); "
                      f"the real run will need it", flush=True)
        print(f"  anchor {anchor_key} "
              f"[{'variation-ref' if ref else 'text'}] ...", flush=True)
        url = render_shot(spec, shots[anchor_key], model, key, seed, ref_path=ref,
                          dry_run=dry_run, label=f"anchor {anchor_key}")
        spend.add("edit" if ref else "t2i")
        if not dry_run:
            download(url, anchor_dest)
            print(f"        -> {anchor_dest}", flush=True)
            out[anchor_key] = anchor_dest
    elif anchor_key in want:
        print(f"  skip {anchor_key} (exists)")

    # 2) the rest, each referencing the anchor on disk
    pend = [k for k in want if k != anchor_key
            and (force or not os.path.exists(dest_of(k)))]
    for k in [k for k in want if k != anchor_key and k not in pend]:
        print(f"  skip {k} (exists)")
    if pend and any(mode_of(k) == "ref" for k in pend) and not dry_run:
        if not os.path.exists(anchor_dest):
            sys.exit(f"anchor missing ({anchor_dest}); render it first")
    for k in pend:
        m = mode_of(k)
        print(f"  shot {k} [{m}] ...", flush=True)
        url = render_shot(spec, shots[k], model, key, seed,
                          ref_path=anchor_dest if m == "ref" else None,
                          extra=scene_extra if k == "scene" else "",
                          dry_run=dry_run, label=f"shot {k}")
        spend.add("edit" if m == "ref" else "t2i")
        if dry_run:
            continue
        download(url, dest_of(k))
        print(f"        -> {dest_of(k)}", flush=True)
        out[k] = dest_of(k)

    spend.report()
    if not dry_run and write_meta:
        npc_art.save_render_meta(
            spec_path, spec, set_seed=seed, set_model=model,
            chosen_variation=draft or spec.get("render", {}).get("chosen_variation"))
    return out


def upscale(spec_path, scale=2, only=None, dry_run=False, model="fal-ai/esrgan"):
    """Finished shots through a hosted upscaler -> <file>-<scale>x.png.

    UNVERIFIED endpoint: fal-ai/esrgan is long-standing but this stage has not
    been run here yet. The local npc_art.upscale (4x-UltraSharp) is the proven
    path and costs nothing; prefer it when the local box is up.
    """
    spec, out_dir = npc_art.load_spec(spec_path)
    key = load_key()
    done = {}
    for k, s in spec["shots"].items():
        if only and k not in only:
            continue
        src = os.path.join(out_dir, f"{s['file']}.png")
        if not os.path.exists(src):
            print(f"  skip {k} (no render)")
            continue
        print(f"  upscale {k} {scale}x ...", flush=True)
        if dry_run:
            continue
        res = submit(model, {"image_url": data_uri(src), "scale": scale}, key,
                     f"upscale {k}")
        dest = os.path.join(out_dir, f"{s['file']}-{scale}x.png")
        download(first_url(res, f"upscale {k}"), dest)
        print(f"        -> {dest}", flush=True)
        done[k] = dest
    return done


def bakeoff(spec_path, models=None, draft=None, seed=None, dry_run=False,
            subdir="falai"):
    """The same spec through several models, into <out>/<subdir>/<model>/.

    Two deliberate properties. It pins ONE seed across every model, so the
    comparison is of the models and not of the dice. And it writes NO render
    metadata back into the spec: a bake-off is a comparison, not an approved
    render, and the specs it reads are live files another session may be
    editing.
    """
    models = models or list(BACKENDS)
    spec, spec_out = npc_art.load_spec(spec_path)
    seed = seed if seed is not None else int.from_bytes(os.urandom(4), "big")
    results = {}
    for m in models:
        backend(m)                                   # fail fast on a typo
        d = os.path.join(spec_out, subdir, m)
        os.makedirs(d, exist_ok=True)
        print(f"\n=== {m} ({BACKENDS[m]['note']}) -> {d}", flush=True)
        if draft:
            variations(spec_path, count=1, seed=seed, model=m, dry_run=dry_run,
                       out_dir=d, write_meta=False)
        results[m] = render_set(spec_path, draft=draft, seed=seed, model=m,
                                dry_run=dry_run, out_dir=d, force=True,
                                write_meta=False)
    print(f"\nBake-off seed {seed}. Compare the sets under "
          f"{os.path.join(spec_out, subdir)}/.", flush=True)
    return results


# ----------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(
        description="Hosted NPC art renderer via fal.ai (Claude-operated).")
    ap.add_argument("stage", choices=["variations", "set", "upscale", "bakeoff",
                                      "models"])
    ap.add_argument("--spec", help="Spec JSON (same file npc_art.py uses).")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"backend ({', '.join(BACKENDS)}); default {DEFAULT_MODEL}")
    ap.add_argument("--models", help="bakeoff: comma-separated backends.")
    ap.add_argument("--subdir", default="falai",
                    help="bakeoff: output folder under the spec's out dir.")
    ap.add_argument("--count", type=int, default=2, help="variations to render.")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--draft", type=int, help="set: chosen variation number.")
    ap.add_argument("--scene", default="", help="set: extra scene detail.")
    ap.add_argument("--only", help="comma-separated shot keys.")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--scale", type=int, default=2, choices=[2, 4])
    ap.add_argument("--dry-run", action="store_true",
                    help="print prompts + cost estimate, spend nothing.")
    a = ap.parse_args()

    if a.stage == "models":
        for n, b in BACKENDS.items():
            print(f"  {n:18s} {b['t2i']:42s} ~${b['price']['t2i']:.3f}/img  "
                  f"{b['note']}")
        return
    if not a.spec:
        sys.exit(f"{a.stage} needs --spec")
    only = set(s.strip() for s in a.only.split(",")) if a.only else None
    if a.stage == "variations":
        variations(a.spec, a.count, a.seed, a.model, a.dry_run)
    elif a.stage == "set":
        render_set(a.spec, a.draft, a.scene, only, a.force, a.seed, a.model,
                   a.dry_run)
    elif a.stage == "upscale":
        upscale(a.spec, a.scale, only, a.dry_run)
    elif a.stage == "bakeoff":
        models = [m.strip() for m in a.models.split(",")] if a.models else None
        bakeoff(a.spec, models, a.draft, a.seed, a.dry_run, a.subdir)


if __name__ == "__main__":
    main()
