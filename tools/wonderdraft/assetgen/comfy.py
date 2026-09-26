"""Minimal ComfyUI API client: queue a workflow graph, wait for it, download the images.

The server address stays out of this public repo: TYRNARRA_COMFY=http://host:port, else the
first line of ~/.config/tyrnarra/comfyui-url (README: "Setup").
"""
import json
import os
import time
import urllib.parse
import urllib.request
import uuid

URL_FILE = os.path.expanduser("~/.config/tyrnarra/comfyui-url")


def _host():
    if os.environ.get("TYRNARRA_COMFY"):
        return os.environ["TYRNARRA_COMFY"].rstrip("/")
    try:
        with open(URL_FILE) as f:
            return f.readline().strip().rstrip("/")
    except OSError:
        return ""


HOST = _host()


def _post(path, data):
    req = urllib.request.Request(HOST + path, json.dumps(data).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))


def _get(path, timeout=30):
    return urllib.request.urlopen(HOST + path, timeout=timeout)


def alive():
    if not HOST:
        return False
    try:
        return _get("/system_stats", 5).status == 200
    except OSError:
        return False


def run(graph, timeout=900):
    """Run a graph; returns (seconds, [PNG bytes per image, in output-node order])."""
    t0 = time.time()
    pid = _post("/prompt", {"prompt": graph, "client_id": str(uuid.uuid4())})["prompt_id"]
    while True:
        h = json.load(_get("/history/" + pid))
        if pid in h:
            break
        if time.time() - t0 > timeout:
            raise TimeoutError("ComfyUI job %s took over %ds" % (pid, timeout))
        time.sleep(1)
    st = h[pid]["status"]
    if st.get("status_str") != "success":
        raise RuntimeError("ComfyUI job failed: %s" % json.dumps(st)[:1500])
    images = []
    for node in sorted(h[pid]["outputs"], key=int):
        for im in h[pid]["outputs"][node].get("images", []):
            q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
            images.append(_get("/view?" + q, 60).read())
    return time.time() - t0, images


def sdxl_with_mask(prompt, negative, seed, width, height, checkpoint, steps, cfg, sampler, scheduler, bg_model,
                   prefix="tyrnarra/assetgen"):
    """SDXL text-to-image plus a BiRefNet foreground mask of the result: outputs [image, mask]."""
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": negative, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0],
              "latent_image": ["4", 0], "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": sampler,
              "scheduler": scheduler, "denoise": 1.0}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}},
        "8": {"class_type": "LoadBackgroundRemovalModel", "inputs": {"bg_removal_name": bg_model}},
        "9": {"class_type": "RemoveBackground", "inputs": {"bg_removal_model": ["8", 0], "image": ["6", 0]}},
        "10": {"class_type": "MaskToImage", "inputs": {"mask": ["9", 0]}},
        "11": {"class_type": "SaveImage", "inputs": {"images": ["10", 0], "filename_prefix": prefix + "_mask"}},
    }


FLUX_MODELS = {"unet": "flux2-dev-Q4_K_M.gguf", "clip": "mistral_3_small_flux2_fp8.safetensors",
               "vae": "flux2-vae.safetensors", "turbo_lora": "Flux_2-Turbo-LoRA_comfyui.safetensors"}


def flux_images(jobs, steps=8, guidance=4.0, prefix="tyrnarra/assetgen"):
    """FLUX.2 [dev] (GGUF Q4) with the Turbo LoRA, several images in one graph so the big models
    load once: jobs = [(prompt, seed, width, height)], outputs one image per job, in order.
    FLUX follows shape instructions (a short trunk, a wide crown, a whale under a city) that
    SDXL Turbo ignores. No negative prompt, and no background-removal model: the drawings come
    on clean white, which sprites.flood_mask cuts out locally.

    The tower's server must run with npc_art's flags (--cache-none --reserve-vram 2.0
    --cpu-vae; tools/imageGen/npc_art.py): without them a second FLUX job wedged the LAN server
    in a model load that /interrupt cannot stop (2026-09-27). About 4 min per image there."""
    g = {
        "u": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": FLUX_MODELS["unet"]}},
        "lo": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "lora_name": FLUX_MODELS["turbo_lora"], "strength_model": 1.0, "model": ["u", 0]}},
        "c": {"class_type": "CLIPLoader", "inputs": {"clip_name": FLUX_MODELS["clip"], "type": "flux2", "device": "default"}},
        "v": {"class_type": "VAELoader", "inputs": {"vae_name": FLUX_MODELS["vae"]}},
        "ks": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
    }
    for i, (prompt, seed, width, height) in enumerate(jobs):
        k = str(i)
        g["t" + k] = {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["c", 0]}}
        g["g" + k] = {"class_type": "FluxGuidance", "inputs": {"guidance": guidance, "conditioning": ["t" + k, 0]}}
        g["bg" + k] = {"class_type": "BasicGuider", "inputs": {"model": ["lo", 0], "conditioning": ["g" + k, 0]}}
        g["fs" + k] = {"class_type": "Flux2Scheduler", "inputs": {"steps": steps, "width": width, "height": height}}
        g["el" + k] = {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}}
        g["rn" + k] = {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}}
        g["sa" + k] = {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["rn" + k, 0], "guider": ["bg" + k, 0], "sampler": ["ks", 0], "sigmas": ["fs" + k, 0],
            "latent_image": ["el" + k, 0]}}
        g["vd" + k] = {"class_type": "VAEDecode", "inputs": {"samples": ["sa" + k, 0], "vae": ["v", 0]}}
        # Numeric ids in job order: run() returns output images sorted by node id.
        g[str(1000 + i)] = {"class_type": "SaveImage", "inputs": {"images": ["vd" + k, 0],
                                                                  "filename_prefix": "%s_%d" % (prefix, seed)}}
    return g
