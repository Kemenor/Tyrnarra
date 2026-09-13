#!/usr/bin/env python3
r"""
mj_server.py - the local half of the Midjourney helper. USER-RUN, unusually.

Midjourney has no API and forbids automated access, so its tier cannot work
like npc_art.py or fal_art.py, where Claude drives everything. Here the GM
drives the browser and this server only removes the tedium around it:

  * it serves the SAME prompts the other two renderers use, so Midjourney art
    comes out of the same <slug>.set.json rather than hand-retyped prose that
    drifts away from the house style, and
  * it saves chosen images back into the spec's directory under the right
    filename, so a set does not end up as three downloads called
    "0_2 (1).png" in ~/Downloads.

Pair it with mj-overlay.user.js (Tampermonkey), which renders the panel on
midjourney.com and calls these endpoints.

Run:
    python3 mj_server.py                 # http://127.0.0.1:8765
    python3 mj_server.py --port 9000 --root /path/to/repo

Endpoints:
    GET  /specs                 -> [{slug, path, shots:[key]}]
    GET  /prompts?slug=<slug>   -> {slug, shots:[{key, file, mode, ar, prompt}]}
    POST /save {slug,shot,url}  -> {path}   downloads url into the spec's out dir

Binds 127.0.0.1 only. It writes files and fetches URLs, so it has no business
listening to anything but this machine.
"""
import argparse
import glob
import json
import os
import sys
import base64
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fal_art          # for resolve_style: one style vocabulary across renderers
import npc_art          # for prompt_for / load_spec: one prompt builder

# Midjourney takes an aspect ratio flag, not a pixel size. Explicit map rather
# than reducing SIZES by gcd, which turns 896x1184 into a useless "28:37".
AR = {"square_hd": "1:1", "square": "1:1", "portrait_4_3": "3:4",
      "portrait_16_9": "9:16", "landscape_4_3": "4:3", "landscape_16_9": "16:9"}

# Midjourney expresses exclusions as --no. Left inline as "no oil paint
# texture", the words read as things to DRAW, which is the opposite of the
# intent - so split_negatives() lifts every "no ..." clause out of the prompt
# and folds it into the flag, alongside these standing ones.
MJ_NO = ["photo", "photorealistic", "3d render", "text", "watermark", "signature"]


def split_negatives(prompt):
    """(positive prompt, [negatives]) - every ", no X" clause moved to --no.

    Only clauses that begin with "no " move. "non-photorealistic" stays put: it
    is one word describing the rendering, not an exclusion, and Midjourney reads
    it correctly where it is.
    """
    keep, negs = [], []
    for clause in prompt.split(", "):
        c = clause.strip()
        if c.lower().startswith("no ") and len(c) > 3:
            negs.append(c[3:].rstrip(". "))
        else:
            keep.append(clause)
    return ", ".join(keep), negs

ROOT = None             # repo root; set from argv

# Midjourney carries the house look in a PERSONALIZATION PROFILE (--profile),
# so the long style sentence the other renderers need is mostly dead weight
# here, and it competes with the profile for influence over the image. Default
# to sending none of it and letting the profile do its job; ?style=digital puts
# it back for a one-off, and ?style=<anything> passes a literal through.
DEFAULT_STYLE = "none"


def styled(spec, style):
    """Apply a style name, or strip the style entirely for "none".

    npc_art.prompt_for drops empty parts, so an empty style simply leaves the
    sentence off the end rather than leaving a dangling separator.
    """
    if style == "none":
        s = dict(spec)
        s["style"] = ""
        return s
    return fal_art.with_style(spec, style)


def find_specs():
    """Every <slug>.set.json under the GM notes, newest first."""
    pat = os.path.join(ROOT, "published", "gm-notes", "**", "*.set.json")
    out = []
    for p in sorted(glob.glob(pat, recursive=True), key=os.path.getmtime,
                    reverse=True):
        try:
            spec = json.load(open(p, encoding="utf-8-sig"))
        except Exception:
            continue                      # a spec mid-edit must not break the list
        if not spec.get("shots"):
            continue
        out.append({"slug": spec.get("slug") or os.path.basename(p)[:-9],
                    "path": p, "shots": list(spec["shots"])})
    return out


def spec_by_slug(slug):
    for s in find_specs():
        if s["slug"] == slug:
            return s
    return None


def build_prompts(slug, style=DEFAULT_STYLE):
    entry = spec_by_slug(slug)
    if not entry:
        return None
    spec, _out = npc_art.load_spec(entry["path"])
    spec = styled(spec, style)
    anchor = spec.get("anchor") or next(iter(spec["shots"]))
    shots = []
    for key, shot in spec["shots"].items():
        mode = "text" if key == anchor else shot.get("mode", "ref")
        is_ref = mode == "ref"
        # The KEEP clause and RECOMPOSE earn their place here too: with --oref,
        # Midjourney inherits the reference's composition exactly as fal's edit
        # endpoint does.
        extra = fal_art.RECOMPOSE if is_ref else ""
        prompt = npc_art.prompt_for(spec, shot, is_edit=is_ref, extra=extra)
        positive, negs = split_negatives(prompt)
        no = ", ".join(dict.fromkeys(negs + MJ_NO))     # dedupe, keep order
        ar = AR.get(shot.get("size", "portrait_4_3"), "3:4")
        shots.append({
            "key": key, "file": shot["file"], "mode": mode, "ar": ar,
            "prompt": f"{positive.rstrip('. ')}. --ar {ar} --no {no}",
        })
    return {"slug": slug, "path": entry["path"], "anchor": anchor,
            "out_dir": os.path.dirname(entry["path"]), "shots": shots}


def save_image(slug, shot_key, b64):
    """Write a chosen Midjourney image into the spec's directory.

    THE BYTES COME FROM THE BROWSER, not from here. cdn.midjourney.com answers
    a page fetch but 403s a plain server-side one (measured 2026-09-13), so the
    userscript reads the blob in the page and posts it base64. Do not "simplify"
    this back into a server-side download; it cannot work.

    The file is named for the shot, and for the format the bytes actually are,
    the same rule fal_art.download follows and for the same reason: a .png that
    holds webp breaks the token-bake step downstream.
    """
    data = build_prompts(slug)
    if not data:
        raise ValueError(f"unknown slug: {slug}")
    shot = next((s for s in data["shots"] if s["key"] == shot_key), None)
    if not shot:
        raise ValueError(f"unknown shot '{shot_key}' for {slug}")
    blob = base64.b64decode(b64)
    ext = next((e for sig, e in fal_art._MAGIC if blob.startswith(sig)), None)
    if not ext:
        # This endpoint writes files and is reachable from a browser page, so it
        # accepts images and nothing else.
        raise ValueError("payload is not a PNG, JPEG or WebP")
    dest = os.path.join(data["out_dir"], f"{shot['file']}.{ext}")
    with open(dest, "wb") as fh:
        fh.write(blob)
    return dest


class Handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # The userscript uses GM_xmlhttpRequest, which is not subject to CORS,
        # but these headers let a plain fetch from the page work too, which is
        # the difference between a five-second debug and a baffling one.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send({})

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path == "/specs":
            return self._send([{"slug": s["slug"], "shots": s["shots"]}
                               for s in find_specs()])
        if u.path == "/prompts":
            slug = (q.get("slug") or [""])[0]
            data = build_prompts(slug, (q.get("style") or [DEFAULT_STYLE])[0])
            return self._send(data or {"error": f"unknown slug: {slug}"},
                              200 if data else 404)
        return self._send({"error": "not found"}, 404)

    def do_POST(self):
        if urllib.parse.urlparse(self.path).path != "/save":
            return self._send({"error": "not found"}, 404)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(n) or b"{}")
            dest = save_image(body["slug"], body["shot"], body["data"])
        except Exception as e:
            return self._send({"error": str(e)}, 400)
        print(f"  saved -> {dest}", flush=True)
        return self._send({"path": dest, "name": os.path.basename(dest)})

    def log_message(self, *a):
        pass                      # the saves are logged; the request noise is not


def main():
    global ROOT
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Local prompt/save server for the "
                                             "Midjourney overlay.")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--root", default=os.path.normpath(
        os.path.join(here, os.pardir, os.pardir)))
    a = ap.parse_args()
    ROOT = a.root
    specs = find_specs()
    print(f"mj_server on http://127.0.0.1:{a.port}  (root {ROOT})")
    print(f"  {len(specs)} spec(s): {', '.join(s['slug'] for s in specs) or '-'}")
    print("  install mj-overlay.user.js in Tampermonkey, then open "
          "midjourney.com/imagine")
    HTTPServer(("127.0.0.1", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
