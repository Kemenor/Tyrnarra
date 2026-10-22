"""Scene art: plain text-to-image renders with no character, on the same FLUX.2
graph as npc_art.py. For region-page sketches and other places with no NPC in
them. Claude-operated, like npc_art.

    python3 scene_art.py --spec <scene>.json [--count 2] [--api http://HOST:8188]

The spec is JSON: {"out": "<dir, relative to the spec>", "style": "<literal style
string>", "size": "landscape_4_3", "scenes": {"<key>": "<what a camera would
see>", ...}, "only": ["<key>", ...] (optional)}. Every scene renders `count`
variations in ONE ComfyUI prompt (one model load), seeds recorded in
<out>/<key>-v<n>.png's sidecar <out>/render.json.

--api points at a ComfyUI server elsewhere (the tower on the LAN, say); the
server must already be running there, since this script never starts one on a
remote host. Without --api it uses npc_art's local server and starts it.
"""
import argparse, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import npc_art


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--count", type=int, default=2)
    ap.add_argument("--api", default=None)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.spec))
    out = os.path.normpath(os.path.join(base, spec.get("out", ".")))
    os.makedirs(out, exist_ok=True)
    w, h = npc_art.SIZES[spec.get("size", "landscape_4_3")]
    style = spec["style"]
    keys = a.only or spec.get("only") or list(spec["scenes"])

    if a.api:
        npc_art.API = a.api.rstrip("/")
        if not npc_art.server_up():
            sys.exit(f"No ComfyUI answering at {npc_art.API}; start it on that host first.")
    else:
        npc_art.ensure_server()

    jobs = []
    for k in keys:
        for n in range(1, a.count + 1):
            jobs.append({"key": f"{k}-v{n}", "prompt": f"{spec['scenes'][k]} {style}",
                         "width": w, "height": h, "seed": random.randint(1, 2**31 - 1)})
    graph, saves = npc_art.flux_graph(jobs)
    res = npc_art.run_graph(graph, list(saves.values()), "scenes")
    meta_path = os.path.join(out, "render.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for j in jobs:
        fn, sub = res[saves[j["key"]]][0]
        dest = os.path.join(out, f"{j['key']}.png")
        npc_art.download(fn, sub, dest)
        meta[j["key"]] = {"seed": j["seed"], "prompt": j["prompt"], "size": [w, h]}
        print("  wrote", dest)
    json.dump(meta, open(meta_path, "w"), indent=2)


if __name__ == "__main__":
    main()
