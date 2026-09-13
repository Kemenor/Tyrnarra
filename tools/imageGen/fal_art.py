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


class FalError(Exception):
    """A render fal refused. Raised rather than exited so one rejected shot
    does not take the rest of the pass down with it: content rejections are
    per-shot and common (see the README), and the shots that would have
    succeeded are worth having."""


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


BACKENDS = {
    "flux2": {
        "t2i": "fal-ai/flux-2",
        "edit": "fal-ai/flux-2/edit",          # image_urls, max 4 references
        "size": _size_flux,
        "max_refs": 4,
        "price": {"t2i": 0.030, "edit": 0.045},
        # GM decision, 2026-09-13: the content checker refuses reference images
        # of wounded characters, which is most of a PF2e cast (see the README).
        # Off for FLUX.2; anything it still refuses goes to the local renderer,
        # which has no checker at all.
        "extra": {"enable_safety_checker": False},
        "note": "sharp linework; needs the style string to carry the look",
    },
    "seedream4": {
        # NOTE: the /edit id is confirmed from fal's docs; the text-to-image id
        # follows fal's naming and was verified by a successful render.
        "t2i": "fal-ai/bytedance/seedream/v4/text-to-image",
        "edit": "fal-ai/bytedance/seedream/v4/edit",
        "size": _size_flux,
        "max_refs": 10,
        "price": {"t2i": 0.030, "edit": 0.030},
        "extra": {},
        "note": "won the 2026-09-13 bake-off; best style match, highest res, cheapest",
    },
    "seedream45": {
        # Point release on the model that won the trial, not a new
        # architecture. Flat $0.04, up to 10 refs, up to 2048x2048.
        "t2i": "fal-ai/bytedance/seedream/v4.5/text-to-image",
        "edit": "fal-ai/bytedance/seedream/v4.5/edit",
        "size": _size_flux,
        "max_refs": 10,
        "price": {"t2i": 0.040, "edit": 0.040},
        "extra": {},
        "note": "v4's successor; a penny more, faster, higher ceiling",
    },
}

# House model as of 2026-09-13: Seedream 4.5. It refused nothing across the
# four-NPC trial (Sera Vance included, whom FLUX.2 refused outright), keeps the
# seed input, and returns 3072x4096 against v4's 1536x2048 for a penny more.
DEFAULT_MODEL = "seedream45"

# Two models were evaluated and REJECTED. Do not re-add either on a hunch; the
# adapters are in git history if the case ever changes.
#
# Nano Banana Pro (2026-09-13): held identity well, but invented backgrounds,
# painted a white sketchy border, rendered ancestry markers too faintly to read,
# and cost 5x the alternatives.
#
# Seedream 5, pro and lite (2026-09-13): on Caevan it all but erased the
# jewel-toned scaling that makes him read as Vishkanya, invented a stone-hall
# background against an explicit "uncluttered", and came back flatter and greyer
# than v4 at 4.5x the price. It also takes no seed input, so its shots cannot be
# pinned for comparison. Newer was worse here.


def backend(name):
    if name not in BACKENDS:
        sys.exit(f"unknown model '{name}'; known: {', '.join(BACKENDS)}")
    return BACKENDS[name]


# ----------------------------------------------------------------- styles
#
# Overlay on npc_art.STYLES rather than an edit to it: styles are being tried
# out here, npc_art.py is open in another session, and a preset that proves
# itself can move into npc_art later so the local renderer gets it too.
#
# "digital" is the house direction as of 2026-09-13. The brief: it should read
# as a DIGITAL PAINTING, crisp rather than smudged. The older "painterly" oil
# language existed to drag FLUX.2 away from photoreal and took the look further
# into smeared oils than wanted; crisper is explicitly fine.

STYLE_OVERRIDES = {
    "digital": ("Stylised digital painting, fantasy character illustration, "
                "crisp clean rendering, confident visible linework, cel-influenced "
                "shading with soft gradients, muted desaturated palette, "
                "uncluttered background, digital concept art, non-photorealistic, "
                "no oil paint texture, no canvas texture, no photographic detail."),
}


def resolve_style(name):
    """Preset name -> the literal style sentence. Overlay first, then npc_art's
    presets, then treat the string as a literal (npc_art.style_of's rule)."""
    if name in STYLE_OVERRIDES:
        return STYLE_OVERRIDES[name]
    return npc_art.STYLES.get(name, name)


def with_style(spec, style):
    """A shallow copy of the spec carrying a literal style string.

    Never mutates the caller's spec: these specs are live files, and a style
    trial must not leave a fingerprint on one.
    """
    if not style:
        return spec
    s = dict(spec)
    s["style"] = resolve_style(style)
    return s


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
    # Read it WHOLE. fal replays the entire request in the error body, base64
    # reference included, so a truncated read cuts the JSON mid-object and the
    # summariser below falls back to dumping raw text. Truncate after parsing.
    try:
        return e.read().decode()
    except Exception:
        return "<no body>"


def _summarise(body):
    """The failure reason plus WHICH FIELD it came from, without the echoed
    input (fal replays the whole request, base64 reference and all, which
    buries the one useful sentence under a megabyte of noise).

    The field matters: 'image_urls' means the reference picture was refused,
    'prompt' means the words were. They are separate checks with separate
    remedies, and telling them apart is the whole diagnosis.
    """
    try:
        d = json.loads(body)["detail"][0]
        return f"[{'.'.join(str(x) for x in d.get('loc', []))}] {d.get('msg', '')}"
    except Exception:
        return body[:300]


def data_uri(path):
    """Reference images travel inline as base64. Avoids fal's upload endpoint
    (and therefore the fal-client dependency) at the cost of a fatter request;
    a 1MP png is ~1.5 MB base64, which is fine."""
    mime = mimetypes.guess_type(path)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def submit(endpoint, args, key, label, timeout=900, metrics=None):
    """Queue one job and wait for it. Returns the result JSON.

    Polls the status_url fal hands back rather than rebuilding the path: model
    ids are nested to different depths (fal-ai/flux-2/edit vs
    fal-ai/bytedance/seedream/v4/edit) and the returned URLs are always right.
    """
    try:
        sub = _post(f"{QUEUE}/{endpoint}", args, key)
    except urllib.error.HTTPError as e:
        raise FalError(f"{label}: fal rejected the submit ({e.code}) on "
                       f"{endpoint}: {_summarise(_http_detail(e))}")
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
            if metrics is not None:
                # fal reports the GPU time it actually spent. The gap between
                # this and our wall clock is queue wait + transfer, which is
                # the part that varies with fal's load rather than with the
                # model, and the part a single sample can badly misrepresent.
                metrics["infer_s"] = (st.get("metrics") or {}).get("inference_time")
            # COMPLETED means the job left the queue, NOT that it succeeded: a
            # validation or policy rejection surfaces as a 4xx with the reason
            # in the body of the result fetch.
            try:
                return _get(result_url, key, timeout=120)
            except urllib.error.HTTPError as e:
                raise FalError(f"{label}: fal returned no result ({e.code}) "
                               f"from {endpoint}: "
                               f"{_summarise(_http_detail(e))}")
        if state in ("FAILED", "ERROR"):
            raise FalError(f"{label}: render failed: {json.dumps(st)[:400]}")
        if now - last >= 20:                        # same heartbeat habit as npc_art
            last = now
            el = f"{int(now - t0) // 60}m{int(now - t0) % 60:02d}s"
            where = (f"queued behind {st.get('queue_position')}"
                     if state == "IN_QUEUE" else "rendering")
            print(f"    ... {label}: {el} elapsed, {where}", flush=True)
        if now - t0 > timeout:
            raise FalError(f"{label}: timed out after {timeout // 60} min")


_MAGIC = ((b"\x89PNG\r\n\x1a\n", "png"), (b"\xff\xd8\xff", "jpg"),
          (b"RIFF", "webp"))
_EXTS = ("png", "jpg", "webp")


def existing(dest):
    """The already-rendered file for `dest`, whatever extension it landed with.

    Needed because download() names files for their real format: a Seedream
    shot asked for as <file>.png is on disk as <file>.jpg. Without this, the
    skip-if-exists checks never match, every run re-renders everything, and
    a set that references its anchor cannot find the anchor it just made.
    """
    stem = os.path.splitext(dest)[0]
    for e in _EXTS:
        if os.path.exists(f"{stem}.{e}"):
            return f"{stem}.{e}"
    return None


def download(url, dest):
    """Write the image, naming it for what it ACTUALLY is. Returns the path.

    Seedream has no `output_format` input and ignores the one we send, so it
    returns JPEG however politely we ask for PNG. Writing those bytes to a
    .png is a lie that breaks downstream: bake_token.py chroma-keys ring art
    and composites portraits expecting real PNG with alpha. Sniff the magic
    bytes and use the true extension instead.
    """
    with urllib.request.urlopen(url, timeout=300) as r:
        data = r.read()
    ext = next((e for sig, e in _MAGIC if data.startswith(sig)), None)
    if ext and not dest.lower().endswith("." + ext):
        dest = os.path.splitext(dest)[0] + "." + ext
    with open(dest, "wb") as fh:
        fh.write(data)
    return dest


def first_url(res, label):
    imgs = res.get("images") or []
    if not imgs or not imgs[0].get("url"):
        raise FalError(f"{label}: no image in result: {json.dumps(res)[:400]}")
    return imgs[0]["url"]


# ----------------------------------------------------------------- spend

class Pace:
    """Per-shot timings for a pass, printed at the end.

    The comparison this exists for: the local renderer takes ~220 s per image
    warm, plus a multi-minute cold model load, which is why npc_art renders a
    whole set in ONE graph. Compare set against set, not image against image.
    """

    def __init__(self):
        self.rows = []          # (label, wall_seconds, fal_inference_seconds)

    def add(self, label, wall, infer):
        self.rows.append((label, wall, infer))

    def report(self):
        if not self.rows:
            return
        total = sum(w for _, w, _ in self.rows)
        for label, wall, infer in self.rows:
            got = f"{infer:.1f}s gpu" if infer else "gpu time not reported"
            print(f"      {label}: {wall:.1f}s wall ({got})", flush=True)
        n = len(self.rows)
        print(f"  {total:.0f}s for {n} shot(s), {total / n:.0f}s/shot avg "
              f"(local FLUX.2 is ~220s/image warm)", flush=True)


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
                dry_run=False, label="shot", pace=None):
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
    args = {"prompt": prompt, "num_images": 1, "seed": seed,
            "output_format": "png"}
    args.update(b["size"](size))
    args.update(b.get("extra", {}))             # per-backend flags, e.g. safety
    for k in b.get("omit", ()):                 # fields this backend has no input for
        args.pop(k, None)
    if is_edit:
        args["image_urls"] = [data_uri(ref_path)]
    metrics, t0 = {}, time.monotonic()
    res = submit(b["edit"] if is_edit else b["t2i"], args, key, label,
                 metrics=metrics)
    if pace is not None:
        pace.add(label, time.monotonic() - t0, metrics.get("infer_s"))
    return first_url(res, label)


def variations(spec_path, count=2, seed=None, model=DEFAULT_MODEL, dry_run=False,
               out_dir=None, write_meta=True, style=None):
    """N takes on the anchor shot, for the user to pick from.

    Default 2 here rather than npc_art's 1: hosted models actually move between
    seeds (npc_art's 1 is a workaround for the Turbo LoRA at 8 steps barely
    differing), and a second take costs cents.
    """
    spec, spec_out = npc_art.load_spec(spec_path)
    spec = with_style(spec, style)
    out_dir = out_dir or spec_out
    key = load_key()
    anchor = spec["shots"][spec.get("anchor") or next(iter(spec["shots"]))]
    seed = seed if seed is not None else int.from_bytes(os.urandom(4), "big")
    vdir = os.path.join(out_dir, "variations")
    os.makedirs(vdir, exist_ok=True)
    spend, pace, paths = Spend(model), Pace(), []
    print(f"  {count} variations on {model} (base seed {seed}) ...", flush=True)
    for i in range(count):
        lbl = f"v{i + 1}"
        url = render_shot(spec, anchor, model, key, seed + i, dry_run=dry_run,
                          label=lbl, pace=pace)
        spend.add("t2i")
        if dry_run:
            continue
        dest = os.path.join(vdir, f"{spec.get('slug', 'npc')}-{lbl}.png")
        dest = download(url, dest)
        paths.append(dest)
        print(f"        -> {dest}", flush=True)
    spend.report()
    pace.report()
    if not dry_run and write_meta:
        npc_art.save_render_meta(spec_path, spec, variations_seed=seed,
                                 variations_count=count, variations_model=model)
    return paths


def render_set(spec_path, draft=None, scene_extra="", only=None, force=False,
               seed=None, model=DEFAULT_MODEL, dry_run=False, out_dir=None,
               write_meta=True, style=None):
    """Anchor first, then every other shot referencing it.

    Identity chain, same as npc_art: the chosen variation anchors the anchor
    shot, the anchor shot anchors the rest. A shot with "mode": "text" renders
    fresh and WILL come back as a different person; that is what it is for, and
    it is wrong for portraits.
    """
    spec, spec_out = npc_art.load_spec(spec_path)
    spec = with_style(spec, style)
    out_dir = out_dir or spec_out
    os.makedirs(out_dir, exist_ok=True)
    key = load_key()
    shots = spec["shots"]
    anchor_key = spec.get("anchor") or next(iter(shots))
    want = [k for k in shots if not only or k in only]
    seed = (seed if seed is not None
            else spec.get("render", {}).get("set_seed")
            or int.from_bytes(os.urandom(4), "big"))
    spend, pace, out = Spend(model), Pace(), {}

    def dest_of(k):
        return os.path.join(out_dir, f"{shots[k]['file']}.png")

    def mode_of(k):
        return "text" if k == anchor_key else shots[k].get("mode", "ref")

    # 1) the anchor, referencing the chosen variation when there is one
    anchor_dest = dest_of(anchor_key)
    anchor_have = existing(anchor_dest)
    if anchor_key in want and (force or not anchor_have):
        ref = None
        if draft:
            ref = os.path.join(out_dir, "variations",
                               f"{spec.get('slug', 'npc')}-v{draft}.png")
            ref = existing(ref) or ref
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
                          dry_run=dry_run, label=f"anchor {anchor_key}",
                          pace=pace)
        spend.add("edit" if ref else "t2i")
        if not dry_run:
            anchor_dest = download(url, anchor_dest)
            print(f"        -> {anchor_dest}", flush=True)
            out[anchor_key] = anchor_dest
    elif anchor_key in want:
        print(f"  skip {anchor_key} (exists)")

    # 2) the rest, each referencing the anchor on disk
    pend = [k for k in want if k != anchor_key
            and (force or not existing(dest_of(k)))]
    for k in [k for k in want if k != anchor_key and k not in pend]:
        print(f"  skip {k} (exists)")
    if pend and any(mode_of(k) == "ref" for k in pend) and not dry_run:
        anchor_have = existing(anchor_dest)
        if not anchor_have:
            sys.exit(f"anchor missing ({anchor_dest}); render it first")
        anchor_dest = anchor_have
    refused = []
    for k in pend:
        m = mode_of(k)
        print(f"  shot {k} [{m}] ...", flush=True)
        try:
            url = render_shot(spec, shots[k], model, key, seed,
                              ref_path=anchor_dest if m == "ref" else None,
                              extra=scene_extra if k == "scene" else "",
                              dry_run=dry_run, label=f"shot {k}", pace=pace)
        except FalError as e:
            # Keep going: a refused portrait should not cost us the scene shot.
            print(f"        ! {e}", file=sys.stderr, flush=True)
            refused.append(k)
            continue
        spend.add("edit" if m == "ref" else "t2i")
        if dry_run:
            continue
        written = download(url, dest_of(k))
        print(f"        -> {written}", flush=True)
        out[k] = written

    spend.report()
    pace.report()
    if refused:
        print(f"  ! {len(refused)} shot(s) refused by fal: {', '.join(refused)}. "
              f"Render these locally (npc_art.py has no content checker).",
              flush=True)
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
        src = existing(os.path.join(out_dir, f"{s['file']}.png"))
        if not src:
            print(f"  skip {k} (no render)")
            continue
        print(f"  upscale {k} {scale}x ...", flush=True)
        if dry_run:
            continue
        res = submit(model, {"image_url": data_uri(src), "scale": scale}, key,
                     f"upscale {k}")
        dest = os.path.join(out_dir, f"{s['file']}-{scale}x.png")
        dest = download(first_url(res, f"upscale {k}"), dest)
        print(f"        -> {dest}", flush=True)
        done[k] = dest
    return done


def bakeoff(spec_path, models=None, draft=None, seed=None, dry_run=False,
            subdir="falai", style=None):
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
        b = backend(m)                               # fail fast on a typo
        d = os.path.join(spec_out, subdir, m)
        os.makedirs(d, exist_ok=True)
        print(f"\n=== {m} ({b['note']}) -> {d}", flush=True)
        if "seed" in b.get("omit", ()):
            # Say it out loud: the pinned seed is the thing that makes a
            # bake-off a comparison rather than three separate rolls, and this
            # backend simply has no seed input to pin.
            print(f"    (note: {m} takes no seed; its shots are an unpinned "
                  f"roll, so judge style and identity, not framing luck)",
                  flush=True)
        if draft:
            variations(spec_path, count=1, seed=seed, model=m, dry_run=dry_run,
                       out_dir=d, write_meta=False, style=style)
        results[m] = render_set(spec_path, draft=draft, seed=seed, model=m,
                                dry_run=dry_run, out_dir=d, force=True,
                                write_meta=False, style=style)
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
    ap.add_argument("--style",
                    help="override the spec's style: a preset name "
                         f"({', '.join(list(STYLE_OVERRIDES) + list(npc_art.STYLES))}) "
                         "or a literal style sentence.")
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
    try:
        _dispatch(a)
    except FalError as e:               # anchor-level refusal, nothing to salvage
        sys.exit(str(e))


def _dispatch(a):
    if a.stage == "models":
        for n, b in BACKENDS.items():
            print(f"  {n:18s} {b['t2i']:42s} ~${b['price']['t2i']:.3f}/img  "
                  f"{b['note']}")
        return
    if not a.spec:
        sys.exit(f"{a.stage} needs --spec")
    if a.subdir != "falai" and a.stage != "bakeoff":
        # Caught this the hard way: --subdir looks like "put the output over
        # there" and is bakeoff-only, so a `set` carrying it writes straight
        # into the spec's own directory, on top of the approved art.
        sys.exit("--subdir only applies to bakeoff. For a throwaway render "
                 "elsewhere, copy the spec into a scratch directory and run "
                 "against the copy.")
    only = set(s.strip() for s in a.only.split(",")) if a.only else None
    if a.stage == "variations":
        variations(a.spec, a.count, a.seed, a.model, a.dry_run, style=a.style)
    elif a.stage == "set":
        render_set(a.spec, a.draft, a.scene, only, a.force, a.seed, a.model,
                   a.dry_run, style=a.style)
    elif a.stage == "upscale":
        upscale(a.spec, a.scale, only, a.dry_run)
    elif a.stage == "bakeoff":
        models = [m.strip() for m in a.models.split(",")] if a.models else None
        bakeoff(a.spec, models, a.draft, a.seed, a.dry_run, a.subdir, a.style)


if __name__ == "__main__":
    main()
