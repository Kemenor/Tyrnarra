#!/usr/bin/env python3
r"""
npc_art.py - local NPC art renderer. CLAUDE-OPERATED: the user never runs this.

Renders consistent multi-shot NPC image sets on the local GPU via the ComfyUI
API with FLUX.2 [dev] (GGUF + Turbo LoRA). Claude distills each NPC's
*physical description* + *clothing & dress* from the GM block
(published/gm-notes/gm-reference/npc-block.md fields) into a spec, then drives
the conversational flow defined in .claude/skills/npc-art/SKILL.md:

  variations -> user picks one -> set (anchor -> portrait + scene) -> upscale

Consistency: the anchor is rendered with the chosen variation as a
ReferenceLatent reference, and every ref-mode shot references the anchor.
A shot with "mode": "text" renders fresh, with NO reference to the anchor, so
it comes back as a DIFFERENT PERSON. Do not use it for portraits: identity is
not preserved by a shared seed across different sizes and framings (that claim
was wrong and shipped mismatched close-ups). Keep portraits on "ref" and fight
the loose crop in the framing text instead.

House styles (the "style" field, or any literal style string):
  painterly (default) - hand-painted fantasy book illustration (approved 2026-06)
  inked               - ink + watercolor storybook look (approved secondary)

Spec (<slug>.set.json, Claude-authored, lives beside the output art):
{
  "slug": "sable-rei",
  "out": ".",                      # output dir, relative to the spec file
  "style": "painterly",            # preset name or a literal style string
  "anchor": "full",
  "character": "distilled from the NPC block's physical description",
  "wardrobe":  "distilled from clothing & dress",
  "shots": {
    "full":     {"file": "<slug>-full",  "size": "portrait_4_3", "framing": "..."},
    "portrait": {"file": "<slug>",       "size": "square_hd",    "framing": "...", "mode": "text"},
    "scene":    {"file": "<slug>-scene", "size": "portrait_4_3", "framing": "..."}
  },
  "render": { ... }                # written back: chosen seed/draft per approved set
}

Stages (also importable as functions):
  python3 npc_art.py variations --spec <spec> [--count 1] [--seed N]
  python3 npc_art.py set        --spec <spec> --draft N [--scene "extra"] [--only k,k] [--force]
  python3 npc_art.py upscale    --spec <spec> [--scale 2]
  python3 npc_art.py frame      --name <frame> --desc "ring description"   # token-frame ring art

`frame` renders ornate ring art on a SOLID MAGENTA field into
tools/token-frames/, ready for `bake_token.py prep`. Token baking itself is
user-directed and faction-level (one frame per faction, most NPCs need no
token) - see tools/foundryExport/README.md.

This module is machine-bound to the ComfyUI install at /var/mnt/games1tb/comfyui
(see that repo's QUICKSTART.md). It auto-starts the server if it is down and
restarts it if RAM is poisoned by another engine's cached weights.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

API = "http://127.0.0.1:8188"
LAUNCHER = "/var/mnt/games1tb/comfyui/run-comfyui-lan.sh"
CONTAINER = "comfyui"   # podman/distrobox container the ComfyUI venv runs in
SERVER_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "comfy-server.log")


def _server_logfile():
    """Log the server; never discard it. When ComfyUI dies mid-prompt (VRAM OOM,
    gfxhub page fault) its stdout is the ONLY place that says why. With DEVNULL
    the failure is invisible and all you see is a driver polling a corpse.
    Truncated per start, so it always describes the current run."""
    try:
        return open(SERVER_LOG, "wb")
    except OSError:
        return subprocess.DEVNULL

MODELS = {
    "unet": "flux2-dev-Q4_K_M.gguf",
    "clip": "mistral_3_small_flux2_fp8.safetensors",
    "vae": "flux2-vae.safetensors",
    "turbo_lora": "Flux_2-Turbo-LoRA_comfyui.safetensors",
    "upscaler": "4x-UltraSharp.pth",
}
STEPS, GUIDANCE = 8, 4.0   # Turbo LoRA sampling

STYLES = {
    "painterly": ("Hand-painted fantasy book illustration, visible expressive "
                  "brushstrokes, painterly digital art, muted earthy palette, soft "
                  "edges, non-photorealistic, traditional painting texture, dark "
                  "vignette background."),
    "inked": ("Stylized ink and watercolor illustration, strong linework, flat cel "
              "shading with watercolor washes, storybook fantasy art, desaturated "
              "palette, no photorealism."),
}

KEEP = ("Keep the exact same character as in the reference image: same face, same "
        "fur and skin pattern and colour, same build, same wardrobe.")

# fal-era size names kept for spec continuity -> ~1MP, multiples of 16
SIZES = {
    "square_hd": (1024, 1024), "square": (1024, 1024),
    "portrait_4_3": (896, 1184), "portrait_16_9": (768, 1344),
    "landscape_4_3": (1184, 896), "landscape_16_9": (1344, 768),
}

MAGENTA_FIELD = ("solid flat pure magenta background (#FF00FF) filling the entire "
                 "canvas including the ring's open centre, nothing else but the ring")


# ----------------------------------------------------------------- server

def server_up():
    try:
        urllib.request.urlopen(API + "/system_stats", timeout=4)
        return True
    except Exception:
        return False


def ensure_server(timeout=180):
    """Ping; auto-start detached if down; wait until ready."""
    if server_up():
        return
    print("  (starting ComfyUI server ...)", flush=True)
    # --cache-none is REQUIRED on this machine, measured 2026-09-13.
    # ComfyUI's `objects` cache holds the loaded model instances from the
    # loader nodes and is exempt from RAM-pressure eviction (execution.py:
    # init_ram_cache / init_lru_cache both leave it a plain HierarchicalCache;
    # only init_null_cache clears it). Without this flag every pass stacks
    # another copy of the model patchers on the last: measured +14.7 GB per
    # pass, RSS 38 -> 55 GB, then swap thrash at ~480 MB/s. With it, RSS sits
    # at ~2.5 GB between passes and drifted +164 MB over four passes.
    # The documented cost ("executes every node each run") is real - every pass
    # reloads the stack - but it is FASTER here, 221 s/image vs 432 s and
    # climbing, because the reload is trivial next to the paging it avoids.
    # VRAM budget: the card is 24 GB and the two big loads are the text encoder
    # (17.2 GB) and the unet (19.6 GB), which already cannot be resident
    # together. On top of the unet the Turbo LoRA needs ~650 MB more, and that
    # is the allocation that decides whether a render survives.
    #   --reserve-vram 1.0 -> KWin starves: amdgpu "Failed to pin framebuffer
    #                         with error -12" (ENOMEM), desktop resets, stutter.
    #   --reserve-vram 3.0 -> ComfyUI starves: the LoRA OOMs applying to the
    #                         unet ("Tried to allocate 648.00 MiB", 768 MB
    #                         free), then a gfxhub page fault kills the server.
    # 2.0 is the middle, with expandable_segments to reclaim the fragmentation
    # the OOM message itself flagged (558 MB reserved-but-unallocated).
    # --cpu-vae is NOT about memory. The GPU VAE path faults on this card:
    #   "Requested to load AutoencoderKL / Memory access fault by GPU node-1 on
    #    address 0x... Reason: Page not present or supervisor privilege"
    # That is an ILLEGAL ACCESS (ROCm driver bug), not an OOM: it killed the
    # server 31 s in with VRAM at 1.1 GB, before the unet or text encoder
    # loaded, so no --reserve-vram value can reach it. The VAE is 160 MB and
    # does one encode + one decode per image, so CPU costs seconds and removes
    # the fault by construction.
    env = dict(os.environ)
    env.setdefault("PYTORCH_HIP_ALLOC_CONF", "expandable_segments:True")
    env.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
    subprocess.Popen(["bash", LAUNCHER, "--cache-none", "--reserve-vram", "2.0", "--cpu-vae"],
                     stdout=_server_logfile(), stderr=subprocess.STDOUT,
                     start_new_session=True, env=env)
    print(f"  (server log: {SERVER_LOG})", flush=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        if server_up():
            return
        time.sleep(3)
    sys.exit("ComfyUI server did not come up; check the comfyui install.")


def _kill_server_procs():
    """Kill ComfyUI wherever it actually runs.

    This install runs ComfyUI *inside a podman (distrobox) container*, so a host
    `pkill -f main.py` matches only the distrobox wrapper and the `podman exec`
    shim: the real Python survives, still holding ~50 GB, while the API goes
    away. That is strictly worse than doing nothing, so kill inside the
    container first and only then sweep the host-side wrappers.
    """
    subprocess.run(["podman", "exec", CONTAINER, "pkill", "-9", "-f", "main.py"],
                   check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for pat in ("main.py --reserve-vram", "run-comfyui", f"distrobox enter {CONTAINER}"):
        subprocess.run(["pkill", "-9", "-f", pat], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def restart_server(timeout=60):
    """Use when RAM is poisoned by another engine's cached weights, or when a
    prompt is wedged in a non-interruptible load (/interrupt returns 200 and
    nothing happens). 30s restart beats a 20-min thrash.

    Verifies the API is really gone before restarting, so a half-killed server
    holding tens of GB cannot masquerade as a fresh one.
    """
    _kill_server_procs()
    t0 = time.time()
    while server_up() and time.time() - t0 < timeout:
        time.sleep(2)
        _kill_server_procs()
    if server_up():
        sys.exit("restart_server: ComfyUI would not die; kill it by PID "
                 "(ps -eo rss,pid,comm --sort=-rss | head) and retry.")
    time.sleep(3)
    ensure_server()


# ----------------------------------------------------------------- client

def _req(path, data=None, headers=None, timeout=120):
    req = urllib.request.Request(API + path, data=data, headers=headers or {})
    return urllib.request.urlopen(req, timeout=timeout)


def queue_state():
    """(running, pending) prompt counts, or (0, 0) if the API is unreachable."""
    try:
        d = json.load(_req("/queue", timeout=10))
        return len(d.get("queue_running", [])), len(d.get("queue_pending", []))
    except Exception:
        return 0, 0


def queue_position(pid):
    """Where our prompt is: ('running'|'queued'|'gone', jobs_ahead)."""
    try:
        d = json.load(_req("/queue", timeout=10))
    except Exception:
        return None, 0
    for it in d.get("queue_running", []):
        if it[1] == pid:
            return "running", 0
    for i, it in enumerate(d.get("queue_pending", [])):
        if it[1] == pid:
            return "queued", i + 1 + len(d.get("queue_running", []))
    return "gone", 0


def preflight_queue(label):
    """Shout if the queue is already busy.

    Submitting behind someone else's prompt is invisible otherwise: the pass
    reports 'still rendering' for as long as the job in front takes, which is
    forever if that job is wedged. One driver at a time is the rule; this is
    the check that the rule was followed.
    """
    r, p = queue_state()
    if r or p:
        print(f"  ! {label}: ComfyUI queue is NOT empty ({r} running, {p} pending).",
              flush=True)
        print("    Another driver is rendering, or a stale prompt is wedged; this "
              "pass will sit behind it.", flush=True)
        print("    Clear it:  curl -X POST http://127.0.0.1:8188/queue "
              "-H 'Content-Type: application/json' -d '{\"clear\":true}'", flush=True)
        print("    If the running job ignores /interrupt it is wedged in a model "
              "load: npc_art.restart_server()", flush=True)
    return r, p


def run_graph(graph, save_nodes, label, timeout=3600):
    """Queue; wait; {save_node: [(filename, subfolder)]}. Tolerates the API
    blocking during model loads."""
    preflight_queue(label)
    body = json.dumps({"prompt": graph, "client_id": str(uuid.uuid4())}).encode()
    try:
        pid = json.load(_req("/prompt", body,
                             {"Content-Type": "application/json"}))["prompt_id"]
    except urllib.error.HTTPError as e:
        sys.exit(f"{label}: graph rejected: {e.read().decode()[:800]}")
    t0 = last = time.time()
    dead = 0
    while True:
        time.sleep(5)
        now = time.time()
        if now - last >= 30:
            # ComfyUI only fills /history when the WHOLE prompt is done, so a
            # multi-shot pass writes nothing until the end and looks dead. Say
            # so, rather than leaving a silent terminal for 15 minutes. A cold
            # first pass spends several of those loading ~38 GB; if the elapsed
            # time climbs with no GPU activity (rocm-smi --showuse), the load
            # has thrashed and restart_server() is the fix.
            #
            # Report QUEUE POSITION, not just elapsed: "still rendering" is a
            # lie when the prompt has not started because something ahead of it
            # is wedged, and that lie cost 16 minutes once.
            last = now
            el = f"{int(now - t0) // 60}m{int(now - t0) % 60:02d}s"
            state, ahead = queue_position(pid)
            if state == "queued":
                where = f"NOT STARTED, queued behind {ahead - 1} job(s)"
                dead = 0
            elif state == "running":
                where = "rendering"
                dead = 0
            elif state == "gone":
                where = "finishing (left the queue, writing output)"
                dead = 0
            else:
                # queue_position() returns None when the API is UNREACHABLE, which
                # is not the same as "still working". A server that dies mid-prompt
                # (VRAM OOM into a gfxhub page fault, say) leaves this loop polling
                # /history for a prompt that will never complete, and reporting
                # "rendering" the whole time. That cost 11 minutes once. Confirm the
                # server is actually up, and bail loudly if it is not.
                dead += 1
                if not server_up():
                    sys.exit(f"{label}: ComfyUI is GONE after {el} "
                             f"(API unreachable, prompt {pid[:8]} will never "
                             f"complete). It most likely died mid-prompt - check "
                             f"the server log for 'out of memory' or a gfxhub page "
                             f"fault, then restart_server() and re-run.")
                where = f"queue unreadable x{dead} (server still answering)"
            print(f"    ... {label}: {el} elapsed, {where}", flush=True)
        try:
            h = json.load(_req(f"/history/{pid}"))
        except Exception:
            continue
        if pid in h:
            res = {}
            for sn in save_nodes:
                imgs = h[pid]["outputs"].get(sn, {}).get("images")
                if not imgs:
                    sys.exit(f"{label}: node {sn} produced no image: "
                             f"{json.dumps(h[pid].get('status', {}))[:500]}")
                res[sn] = [(i["filename"], i.get("subfolder", "")) for i in imgs]
            return res
        if time.time() - t0 > timeout:
            sys.exit(f"{label}: timed out after {timeout // 60} min")


def download(filename, subfolder, dest):
    q = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder,
                                "type": "output"})
    with _req(f"/view?{q}") as r, open(dest, "wb") as fh:
        fh.write(r.read())


def upload(path):
    name = f"npcart_{uuid.uuid4().hex[:10]}_{os.path.basename(path)}"
    boundary = uuid.uuid4().hex
    img = open(path, "rb").read()
    body = (f"--{boundary}\r\nContent-Disposition: form-data; "
            f'name="image"; filename="{name}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n").encode() + img + \
           f"\r\n--{boundary}--\r\n".encode()
    return json.load(_req("/upload/image", body,
                          {"Content-Type":
                           f"multipart/form-data; boundary={boundary}"}))["name"]


# ----------------------------------------------------------------- graph

def flux_graph(jobs, ref_name=None, chain_anchor=None):
    """One graph, N shots: the heavy models load once for the whole pass.
    jobs: [{key, prompt, width, height, seed, use_ref}].
    ref_name: an uploaded input image used as the reference for use_ref jobs.
    chain_anchor: a job KEY whose sampler OUTPUT LATENT becomes the reference
    for the other use_ref jobs instead - this renders an anchor and the shots
    that reference it in ONE pass (one text-encoder residency, one Flux load),
    which roughly halves a set render on this swap-bound machine."""
    g = {
        "u": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": MODELS["unet"]}},
        "lo": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "lora_name": MODELS["turbo_lora"], "strength_model": 1.0, "model": ["u", 0]}},
        "c": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": MODELS["clip"], "type": "flux2", "device": "default"}},
        "v": {"class_type": "VAELoader", "inputs": {"vae_name": MODELS["vae"]}},
        "ks": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
    }
    if ref_name:
        g["rli"] = {"class_type": "LoadImage", "inputs": {"image": ref_name}}
        g["rsc"] = {"class_type": "ImageScaleToTotalPixels", "inputs": {
            "upscale_method": "lanczos", "megapixels": 1.0, "resolution_steps": 1,
            "image": ["rli", 0]}}
        g["rve"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["rsc", 0],
                                                          "vae": ["v", 0]}}
    # the latent every use_ref job references: the chained anchor's sampler
    # output if chaining, else the uploaded reference image's encoding
    ref_latent = [f"sa_{chain_anchor}", 0] if chain_anchor else ["rve", 0]
    saves = {}
    for j in jobs:
        k, w, h = j["key"], j["width"], j["height"]
        g[f"t_{k}"] = {"class_type": "CLIPTextEncode", "inputs": {
            "text": j["prompt"], "clip": ["c", 0]}}
        g[f"g_{k}"] = {"class_type": "FluxGuidance", "inputs": {
            "guidance": GUIDANCE, "conditioning": [f"t_{k}", 0]}}
        cond = [f"g_{k}", 0]
        if j.get("use_ref"):
            # the chained anchor itself references the uploaded image (the
            # chosen variation); chained shots reference the anchor's latent
            latent = ["rve", 0] if k == chain_anchor else ref_latent
            g[f"rl_{k}"] = {"class_type": "ReferenceLatent", "inputs": {
                "conditioning": cond, "latent": latent}}
            cond = [f"rl_{k}", 0]
        g[f"bg_{k}"] = {"class_type": "BasicGuider", "inputs": {
            "model": ["lo", 0], "conditioning": cond}}
        g[f"fs_{k}"] = {"class_type": "Flux2Scheduler", "inputs": {
            "steps": STEPS, "width": w, "height": h}}
        g[f"el_{k}"] = {"class_type": "EmptyFlux2LatentImage", "inputs": {
            "width": w, "height": h, "batch_size": 1}}
        g[f"rn_{k}"] = {"class_type": "RandomNoise", "inputs": {"noise_seed": j["seed"]}}
        g[f"sa_{k}"] = {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": [f"rn_{k}", 0], "guider": [f"bg_{k}", 0], "sampler": ["ks", 0],
            "sigmas": [f"fs_{k}", 0], "latent_image": [f"el_{k}", 0]}}
        g[f"vd_{k}"] = {"class_type": "VAEDecode", "inputs": {
            "samples": [f"sa_{k}", 0], "vae": ["v", 0]}}
        g[f"si_{k}"] = {"class_type": "SaveImage", "inputs": {
            "filename_prefix": f"npcart/{k}", "images": [f"vd_{k}", 0]}}
        saves[k] = f"si_{k}"
    return g, saves


# ----------------------------------------------------------------- spec

def load_spec(path):
    spec = json.load(open(path, encoding="utf-8-sig"))
    if not spec.get("shots"):
        sys.exit("No 'shots' in the spec.")
    out_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(path)),
                                            spec.get("out", ".")))
    os.makedirs(out_dir, exist_ok=True)
    return spec, out_dir


def style_of(spec):
    s = spec.get("style", "painterly")
    return STYLES.get(s, s)


def prompt_for(spec, shot, is_edit=False, extra=""):
    framing = shot["framing"]
    if extra:
        framing = framing.rstrip(". ") + ". " + extra
    parts = [KEEP] if is_edit else []
    parts += [framing,
              spec["character"].strip() + ", " + spec["wardrobe"].strip() + ".",
              style_of(spec)]
    return " ".join(p.strip() for p in parts if p and p.strip())


def save_render_meta(spec_path, spec, **kv):
    spec.setdefault("render", {}).update(kv)
    json.dump(spec, open(spec_path, "w"), indent=2)


# ----------------------------------------------------------------- stages

def variations(spec_path, count=1, seed=None):
    """N full-body variations of the anchor shot. Returns list of paths.

    Default 1, not 4. FLUX.2 with the Turbo LoRA at 8 steps barely moves
    between seeds on an identical prompt: four "variations" come back as four
    near-identical images, so the extra three are pure render time. If the one
    shot is wrong, the fix is the spec (character / wardrobe / framing), not
    another roll of the dice.
    """
    spec, out_dir = load_spec(spec_path)
    ensure_server()
    anchor = spec["shots"][spec.get("anchor") or next(iter(spec["shots"]))]
    w, h = SIZES.get(anchor.get("size", "portrait_4_3"), SIZES["portrait_4_3"])
    seed = seed if seed is not None else int.from_bytes(os.urandom(4), "big")
    prompt = prompt_for(spec, anchor)
    jobs = [{"key": f"v{i+1}", "prompt": prompt, "width": w, "height": h,
             "seed": seed + i} for i in range(count)]
    print(f"  {count} variations (base seed {seed}) ...", flush=True)
    g, saves = flux_graph(jobs)
    res = run_graph(g, list(saves.values()), "variations")
    vdir = os.path.join(out_dir, "variations")
    os.makedirs(vdir, exist_ok=True)
    paths = []
    for i, j in enumerate(jobs, 1):
        fn, sub = res[saves[j["key"]]][0]
        dest = os.path.join(vdir, f"{spec.get('slug','npc')}-v{i}.png")
        download(fn, sub, dest)
        paths.append(dest)
        print(f"        -> {dest}", flush=True)
    save_render_meta(spec_path, spec, variations_seed=seed, variations_count=count)
    return paths


def render_set(spec_path, draft=None, scene_extra="", only=None, force=False,
               seed=None):
    """Anchor (referencing chosen variation) then the other shots (referencing
    the anchor; mode:text shots render fresh). Returns {shot: path}."""
    spec, out_dir = load_spec(spec_path)
    ensure_server()
    shots = spec["shots"]
    anchor_key = spec.get("anchor") or next(iter(shots))
    want = [k for k in shots if not only or k in only]
    seed = (seed if seed is not None
            else spec.get("render", {}).get("set_seed")
            or int.from_bytes(os.urandom(4), "big"))
    out = {}

    def dest_of(k):
        return os.path.join(out_dir, f"{shots[k]['file']}.png")

    def mode_of(k):
        return "text" if k == anchor_key else shots[k].get("mode", "ref")

    def job_for(k, use_ref, extra=""):
        s = shots[k]
        w, h = SIZES.get(s.get("size", "portrait_4_3"), SIZES["portrait_4_3"])
        return {"key": k, "width": w, "height": h, "seed": seed,
                "use_ref": use_ref,
                "prompt": prompt_for(spec, s, is_edit=use_ref, extra=extra)}

    anchor_dest = dest_of(anchor_key)
    render_anchor = anchor_key in want and (force or not os.path.exists(anchor_dest))
    pend = [k for k in want if k != anchor_key
            and (force or not os.path.exists(dest_of(k)))]
    for k in [anchor_key] if not render_anchor and anchor_key in want else []:
        print(f"  skip {k} (exists)")
    for k in [k for k in shots if k in want and k != anchor_key and k not in pend]:
        print(f"  skip {k} (exists)")

    jobs, ref_name, chain = [], None, None
    if render_anchor:
        ref_img = None
        if draft:
            vpath = os.path.join(out_dir, "variations",
                                 f"{spec.get('slug','npc')}-v{draft}.png")
            if not os.path.exists(vpath):
                sys.exit(f"variation not found: {vpath}")
            ref_img = upload(vpath)
        jobs.append(job_for(anchor_key, bool(ref_img)))
        ref_name, chain = ref_img, anchor_key
        print(f"  anchor {anchor_key} [{'variation-ref' if ref_img else 'text'}] queued",
              flush=True)
    elif pend and any(mode_of(k) == "ref" for k in pend):
        if not os.path.exists(anchor_dest):
            sys.exit(f"anchor missing ({anchor_dest}); render it first")
        ref_name = upload(anchor_dest)   # shots reference the existing anchor image

    for k in pend:
        m = mode_of(k)
        jobs.append(job_for(k, m == "ref",
                            extra=scene_extra if k == "scene" else ""))
        print(f"  shot {k} [{m}] queued", flush=True)

    if jobs:
        # ONE graph for anchor + shots: one text-encoder residency, one Flux
        # load. Chained shots reference the anchor's output latent directly.
        print(f"  rendering {len(jobs)} shot(s) in one chained pass ...", flush=True)
        g, saves = flux_graph(jobs, ref_name, chain_anchor=chain)
        res = run_graph(g, list(saves.values()), "set")
        for j in jobs:
            fn, sub = res[saves[j["key"]]][0]
            download(fn, sub, dest_of(j["key"]))
            print(f"        -> {dest_of(j['key'])}", flush=True)
            out[j["key"]] = dest_of(j["key"])
    save_render_meta(spec_path, spec, set_seed=seed,
                     chosen_variation=draft or spec.get("render", {}).get("chosen_variation"))
    return out


def upscale(spec_path, scale=2, only=None):
    """Finished shots through 4x-UltraSharp; <file>-<scale>x.png beside them."""
    spec, out_dir = load_spec(spec_path)
    ensure_server()
    done = {}
    for k, s in spec["shots"].items():
        if only and k not in only:
            continue
        src = os.path.join(out_dir, f"{s['file']}.png")
        if not os.path.exists(src):
            print(f"  skip {k} (no render)")
            continue
        name = upload(src)
        g = {"li": {"class_type": "LoadImage", "inputs": {"image": name}},
             "um": {"class_type": "UpscaleModelLoader",
                    "inputs": {"model_name": MODELS["upscaler"]}},
             "up": {"class_type": "ImageUpscaleWithModel", "inputs": {
                 "upscale_model": ["um", 0], "image": ["li", 0]}},
             "si": {"class_type": "SaveImage", "inputs": {
                 "filename_prefix": "npcart/up", "images": ["up", 0]}}}
        if scale != 4:
            g["rs"] = {"class_type": "ImageScaleBy", "inputs": {
                "upscale_method": "lanczos", "scale_by": scale / 4.0,
                "image": ["up", 0]}}
            g["si"]["inputs"]["images"] = ["rs", 0]
        print(f"  upscale {k} {scale}x ...", flush=True)
        fn, sub = run_graph(g, ["si"], f"upscale {k}")["si"][0]
        dest = os.path.join(out_dir, f"{s['file']}-{scale}x.png")
        download(fn, sub, dest)
        print(f"        -> {dest}", flush=True)
        done[k] = dest
    return done


def frame(name, desc, out_dir=None):
    """Token-frame ring art on a magenta field -> tools/token-frames/<name>.webp.
    Follow with: python bake_token.py prep --in <out> --out <name>.cut.png"""
    ensure_server()
    out_dir = out_dir or os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), os.pardir, "token-frames"))
    prompt = (f"An ornate circular token frame ring, {desc}, perfectly round ring "
              f"with an open empty centre, centered, symmetrical, fantasy "
              f"illustration style, {MAGENTA_FIELD}.")
    g, saves = flux_graph([{"key": "frame", "prompt": prompt, "width": 1024,
                            "height": 1024,
                            "seed": int.from_bytes(os.urandom(4), "big")}])
    print(f"  frame '{name}' ...", flush=True)
    fn, sub = run_graph(g, list(saves.values()), "frame")[saves["frame"]][0]
    dest = os.path.join(out_dir, f"{name}.png")
    download(fn, sub, dest)
    print(f"        -> {dest}\n  next: python ../foundryExport/bake_token.py prep "
          f"--in {dest} --out {os.path.join(out_dir, name)}.cut.png", flush=True)
    return dest


# ----------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description="Local NPC art renderer (Claude-operated).")
    ap.add_argument("stage", choices=["variations", "set", "upscale", "frame"])
    ap.add_argument("--spec", help="Spec JSON (variations/set/upscale).")
    ap.add_argument("--count", type=int, default=1,
                help="variations to render (default 1; FLUX seeds barely "
                     "differ - fix the spec instead of rolling again)")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--draft", type=int, help="set: chosen variation number.")
    ap.add_argument("--scene", default="", help="set: extra scene detail.")
    ap.add_argument("--only", help="comma-separated shot keys.")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--scale", type=int, default=2, choices=[2, 4])
    ap.add_argument("--name", help="frame: output stem.")
    ap.add_argument("--desc", help="frame: ring description.")
    a = ap.parse_args()
    only = set(s.strip() for s in a.only.split(",")) if a.only else None
    if a.stage == "frame":
        if not (a.name and a.desc):
            sys.exit("frame needs --name and --desc")
        frame(a.name, a.desc)
        return
    if not a.spec:
        sys.exit(f"{a.stage} needs --spec")
    if a.stage == "variations":
        variations(a.spec, a.count, a.seed)
    elif a.stage == "set":
        render_set(a.spec, a.draft, a.scene, only, a.force, a.seed)
    elif a.stage == "upscale":
        upscale(a.spec, a.scale, only)


if __name__ == "__main__":
    main()
