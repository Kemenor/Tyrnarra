#!/usr/bin/env python3
"""Serve published/ on the local network for the map-area editor.

    python3 tools/map-area-server.py [--port 8010]

- Serves published/ as the site root, bound to every interface, so another
  machine on the LAN can open http://<this-machine>:<port>/.
- /__maps lists every *.areas.json under published/gm-notes/ with a link that
  opens the editor with its map and areas already loaded.
- POST /__save-areas?path=/gm-notes/.../<name>.areas.json writes the editor's
  JSON back into the repo. Only existing folders under published/gm-notes/ and
  only *.areas.json names are accepted.
"""
import argparse
import html
import json
import os
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

ROOT = Path(__file__).resolve().parent.parent / "published"
GM = ROOT / "gm-notes"
EDITOR = "/gm-notes/tools/map-area-editor.html"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if urlparse(self.path).path == "/__maps":
            return self.maps_index()
        super().do_GET()

    def maps_index(self):
        rows = []
        for f in sorted(GM.rglob("*.areas.json")):
            if "_full" in f.parts:
                continue
            try:
                image = json.loads(f.read_text()).get("image") or ""
            except ValueError:
                image = ""
            img = f.parent / image
            if not image or not img.is_file():
                continue
            areas_url = "/" + f.relative_to(ROOT).as_posix()
            map_url = "/" + img.relative_to(ROOT).as_posix()
            link = f"{EDITOR}?map={quote(map_url)}&areas={quote(areas_url)}"
            rows.append(f'<li><a href="{html.escape(link)}">{html.escape(areas_url)}</a></li>')
        body = ("<!doctype html><meta charset=utf-8><title>Map areas</title>"
                "<style>body{background:#14161c;color:#ddd;font:15px sans-serif;padding:16px}a{color:#f0b020}li{margin:6px 0}</style>"
                f"<h1>Map areas</h1><ul>{''.join(rows) or '<li>none found</li>'}</ul>").encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != "/__save-areas":
            return self.send_error(404)
        rel = (parse_qs(url.query).get("path") or [""])[0]
        target = (ROOT / rel.lstrip("/")).resolve()
        if (GM.resolve() not in target.parents or not target.name.endswith(".areas.json")
                or not target.parent.is_dir() or "_full" in target.parts):
            return self.send_error(403, "path must be an .areas.json file in an existing gm-notes folder")
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
        except ValueError:
            return self.send_error(400, "body is not JSON")
        target.write_text(json.dumps(data, indent=2) + "\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"saved")


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 80))
        return s.getsockname()[0]
    except OSError:
        return "localhost"
    finally:
        s.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8010)))
    port = ap.parse_args().port
    print(f"Serving {ROOT} on http://{lan_ip()}:{port}/  ·  map list: http://{lan_ip()}:{port}/__maps", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
