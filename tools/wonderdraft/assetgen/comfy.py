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


def flux_with_mask(prompt, seed, width, height, bg_model, steps=8, guidance=4.0, prefix="tyrnarra/assetgen"):
    """FLUX.2 [dev] (GGUF) with the Turbo LoRA plus a BiRefNet foreground mask: outputs [image, mask].
    Slower than SDXL Turbo but follows shape instructions (a short trunk, a wide crown) that
    SDXL ignores. It takes no negative prompt."""
    return {
        "u": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": FLUX_MODELS["unet"]}},
        "lo": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "lora_name": FLUX_MODELS["turbo_lora"], "strength_model": 1.0, "model": ["u", 0]}},
        "c": {"class_type": "CLIPLoader", "inputs": {"clip_name": FLUX_MODELS["clip"], "type": "flux2", "device": "default"}},
        "v": {"class_type": "VAELoader", "inputs": {"vae_name": FLUX_MODELS["vae"]}},
        "ks": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "t": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["c", 0]}},
        "g": {"class_type": "FluxGuidance", "inputs": {"guidance": guidance, "conditioning": ["t", 0]}},
        "bg": {"class_type": "BasicGuider", "inputs": {"model": ["lo", 0], "conditioning": ["g", 0]}},
        "fs": {"class_type": "Flux2Scheduler", "inputs": {"steps": steps, "width": width, "height": height}},
        "el": {"class_type": "EmptyFlux2LatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
        "rn": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "sa": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["rn", 0], "guider": ["bg", 0], "sampler": ["ks", 0], "sigmas": ["fs", 0], "latent_image": ["el", 0]}},
        "vd": {"class_type": "VAEDecode", "inputs": {"samples": ["sa", 0], "vae": ["v", 0]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["vd", 0], "filename_prefix": prefix}},
        "8": {"class_type": "LoadBackgroundRemovalModel", "inputs": {"bg_removal_name": bg_model}},
        "9": {"class_type": "RemoveBackground", "inputs": {"bg_removal_model": ["8", 0], "image": ["vd", 0]}},
        "10": {"class_type": "MaskToImage", "inputs": {"mask": ["9", 0]}},
        "11": {"class_type": "SaveImage", "inputs": {"images": ["10", 0], "filename_prefix": prefix + "_mask"}},
    }
