#!/usr/bin/env python3
r"""
audio.py - search, fetch and ship table ambience and music to Foundry playlists.

Three sources, one search:
  tta       Tabletop Audio: ~530 ten-minute ambiences and music tracks, free for home
            games (CC BY-NC-ND 4.0). The tagged catalogue comes from tabletopaudio.com
            and is cached in _cache/ (refreshed every 14 days, or with `refresh`).
  fs        Freesound: short CC-licensed loops and effects (rain, surf, crowds, forges)
            through its API. Needs a free API key: FREESOUND_KEY, else tools/keys/freesound.key.
  local     Anything else in _full/ (a bought pack dropped into _full/<pack>/), matched
            on its folder and file names.

Downloaded audio lives in _full/ (a link into the sync folder's audio-library/, never
in git). On the server everything goes to the shared Data/assets/audio/<source>/,
so one copy serves every world.

Refs name a sound everywhere: tta:376, fs:123456, local:<path under _full>.

Usage:
  python audio.py search docks harbor night            # tta + local (+ fs when a key is set)
  python audio.py search tavern -crowded --type ambience --source tta
  python audio.py search "rain on canvas" --source fs --min-dur 30
  python audio.py show tta:376 fs:123456
  python audio.py fetch tta:376 fs:123456              # download into _full/
  python audio.py playlist --spec <quest>.audio.json --upload --out <quest>.audio.macro.js
"""
import argparse
import json
import math
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "_full")
CACHE = os.path.join(HERE, "_cache")
KEYS = os.path.join(os.path.dirname(HERE), "keys")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "foundryExport"))

UA = "TyrnarraGM-audio-library/1.0"
TTA_DATA = "https://tabletopaudio.com/tta_data"
TTA_HOME = "https://tabletopaudio.com/"
TTA_SOUNDS = "https://sounds.tabletopaudio.com/"
FS_API = "https://freesound.org/apiv2/"
FS_FIELDS = ("id,name,tags,description,duration,license,username,previews,"
             "avg_rating,num_ratings,num_downloads,url")
AUDIO_EXTS = (".mp3", ".ogg", ".oga", ".wav", ".flac", ".m4a", ".webm", ".opus")
REMOTE_SUB = "assets/audio"          # under the server's Data/
MAX_AGE = 14 * 86400

# Query words that should also find their near-synonyms in the tags (matched at a discount).
SYNONYMS = [
    {"tavern", "inn", "pub", "alehouse", "bar", "hearth", "taproom"},
    {"dock", "harbor", "port", "pier", "wharf", "quay", "shipyard"},
    {"ship", "boat", "sailing", "vessel", "nautical", "sail"},
    {"sea", "ocean", "wave", "surf", "shore", "coast", "beach"},
    {"pirate", "smuggler", "brigand", "corsair"},
    {"forest", "wood", "woodland", "jungle"},
    {"city", "town", "urban", "street", "village"},
    {"market", "bazaar", "fair", "merchant"},
    {"fight", "combat", "battle", "action", "war", "skirmish"},
    {"horror", "creepy", "eerie", "spooky", "dread", "haunted", "scary"},
    {"cave", "cavern", "underground", "underdark", "mine", "tunnel"},
    {"dungeon", "crypt", "catacomb", "tomb", "prison", "jail"},
    {"temple", "church", "cathedral", "shrine", "monastery", "chant"},
    {"storm", "thunder", "rain", "wind"},
    {"train", "rail", "railway", "locomotive", "steam"},
    {"magic", "arcane", "wizard", "spell", "sorcery"},
    {"night", "evening", "dark"},
    {"calm", "peaceful", "quiet", "rest", "relax", "serene"},
    {"tense", "tension", "suspense", "stealth", "sneak"},
    {"noble", "court", "palace", "castle", "ball", "royal"},
    {"desert", "sand", "dune"},
    {"snow", "ice", "frozen", "winter", "cold"},
    {"swamp", "bog", "marsh"},
    {"festival", "celebration", "party", "feast"},
]
# Freesound sounds tagged with these are dropped by the default fantasy setting.
# (Trains stay: Talan has rail.)
MODERN_NOISE = {"car", "traffic", "engine", "diesel", "motor", "motorcycle", "truck", "highway",
                "airplane", "aeroplane", "jet", "helicopter", "siren", "phone", "smartphone",
                "computer", "keyboard", "radio", "television", "tv", "industrial", "industry",
                "factory", "cargo", "container", "freeway", "tram", "subway", "metro", "bus",
                "electric", "electronic", "synth", "beep", "notification", "dubstep", "edm"}
UNMODERN = {"scifi", "modern"}       # dropped by the default fantasy setting...
KEEP = {"fantasy", "historical"}     # ...unless the track is also one of these


# ---------------------------------------------------------------- helpers

def http(url, binary=False, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")


def stem(w):
    w = w.lower()
    if w == "harbour":
        w = "harbor"
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def words(text):
    return {stem(w) for w in re.findall(r"[a-z0-9']+", str(text).lower())}


def syn(term):
    out = set()
    for group in SYNONYMS:
        if term in group:
            out |= group
    return out - {term}


def slug(text, n=60):
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s[:n].rstrip("-") or "sound"


def tidy(text, n=110):
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(text))).strip()
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


# ---------------------------------------------------------------- Tabletop Audio

def tta_catalogue(force=False):
    """The tagged track list, each track with its real filename on the sound server
    (the catalogue's own links are lowercased and 403; the player script has the
    exact names)."""
    path = os.path.join(CACHE, "tta.json")
    if not force and os.path.exists(path) and time.time() - os.path.getmtime(path) < MAX_AGE:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    try:
        tracks = json.loads(http(TTA_DATA))["tracks"]
        home = http(TTA_HOME)
        js = re.search(r'src="(bootstrap/js/tta[^"]*\.js[^"]*)"', home)
        files = {}
        if js:
            player = http(TTA_HOME + js.group(1))
            files = {k: f for k, f in re.findall(
                r'song_(\d+):\{title:"[^"]*",artist:\w+,mp3:\w+\+"([^"]+)"', player)}
    except (urllib.error.URLError, ValueError, KeyError) as e:
        if os.path.exists(path):
            print(f"(Tabletop Audio unreachable, using the cached catalogue: {e})", file=sys.stderr)
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        sys.exit(f"Could not load the Tabletop Audio catalogue: {e}")
    out = []
    for t in tracks:
        genres = sorted({g.strip() for x in t.get("track_genre", []) for g in x.split(",") if g.strip()})
        out.append({
            "ref": f"tta:{t['key']}",
            "title": t["track_title"],
            "type": re.sub(r"\s+", " ", t.get("track_type", "").replace(",", "")).replace("+ ", "+ ").strip(),
            "genres": genres,
            "tags": [x.strip() for x in t.get("tags", []) if x.strip()],
            "flavor": t.get("flavor_text", ""),
            "file": files.get(str(t["key"])),
            "minutes": 10,
        })
    missing = [t["ref"] for t in out if not t["file"]]
    if missing:
        print(f"(no sound file found for {len(missing)} track(s): {', '.join(missing[:8])})", file=sys.stderr)
    os.makedirs(CACHE, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    return out


def score(query, excludes, fields):
    """fields: [(weight, set_of_words)]. Each query term scores the best field it hits;
    a synonym hit counts at 0.6. Every term hit earns a bonus, so 'harbor night' ranks
    a track with both above one with either."""
    allwords = set().union(*(w for _, w in fields))
    if excludes & allwords:
        return 0
    total, hits = 0.0, 0
    for term in query:
        best = 0.0
        for weight, ws in fields:
            if term in ws:
                best = max(best, weight)
            elif syn(term) & ws:
                best = max(best, weight * 0.6)
        total += best
        hits += best > 0
    if hits == 0:
        return 0
    return total + (2.0 if hits == len(query) and len(query) > 1 else 0)


def search_tta(query, excludes, a):
    res = []
    for t in tta_catalogue():
        g = set(t["genres"])
        if a.setting == "fantasy" and g & UNMODERN and not g & KEEP:
            continue
        if a.type == "ambience" and not t["type"].startswith("ambience"):
            continue
        if a.type == "music" and not t["type"].startswith("music"):
            continue
        tagwords = set().union(*(words(x) for x in t["tags"])) if t["tags"] else set()
        s = score(query, excludes, [(4, words(t["title"])), (3, tagwords),
                                    (2, words(" ".join(t["genres"]))),
                                    (1.5, words(t["flavor"])), (1, words(t["type"]))])
        if s:
            res.append((s, t))
    return res


# ---------------------------------------------------------------- Freesound

def fs_key(required=False):
    key = os.environ.get("FREESOUND_KEY", "").strip()
    if not key:
        try:
            with open(os.path.join(KEYS, "freesound.key"), encoding="utf-8") as fh:
                key = fh.readline().strip()
        except OSError:
            pass
    if required and not key:
        sys.exit("No Freesound key: put the API key in the sync folder's keys/freesound.key and run "
                 "python3 tools/check_setup.py --link (or set FREESOUND_KEY). See README.md.")
    return key


def fs_get(path, **params):
    params["token"] = fs_key(required=True)
    url = FS_API + path + "?" + urllib.parse.urlencode(params)
    try:
        return json.loads(http(url))
    except urllib.error.HTTPError as e:
        sys.exit(f"Freesound {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def fs_entry(s):
    lic = s.get("license", "")
    short = ("CC0" if "zero" in lic or "/publicdomain/" in lic else
             "CC BY-NC" if "by-nc" in lic else "CC BY" if "/by/" in lic else
             "Sampling+" if "sampling" in lic else lic.rsplit("/", 3)[-3] if lic.count("/") > 3 else lic)
    return {
        "ref": f"fs:{s['id']}",
        "title": s["name"],
        "type": "sound",
        "tags": s.get("tags", [])[:12],
        "flavor": tidy(s.get("description", ""), 140),
        "seconds": round(s.get("duration", 0)),
        "license": short,
        "license_url": lic,
        "author": s.get("username", ""),
        "rating": round(s.get("avg_rating") or 0, 1),
        "downloads": s.get("num_downloads", 0),
        "preview": (s.get("previews") or {}).get("preview-hq-mp3"),
        "page": s.get("url", ""),
    }


def search_fs(query_text, a):
    lo, hi = a.min_dur or 0, a.max_dur or "*"
    flt = [f"duration:[{lo} TO {hi}]"]
    if a.cc0:
        flt.append('license:"Creative Commons 0"')
    pool = 60 if a.fs_sort == "score" else min(a.limit, 150)
    data = fs_get("search/text/", query=query_text, filter=" ".join(flt), fields=FS_FIELDS,
                  page_size=pool, sort=a.fs_sort)
    res = []
    for i, s in enumerate(data.get("results", [])):
        r = fs_entry(s)
        if a.setting == "fantasy" and words(" ".join(r["tags"]) + " " + r["title"]) & MODERN_NOISE:
            continue
        if a.fs_sort != "score":
            res.append((1000 - i, r))
            continue
        # Freesound's relevance order, nudged towards sounds other people found worth using:
        # a sound ranked 10th with 5,000 downloads beats the 1st with 3.
        res.append((30 * (1 - i / pool) + 6 * math.log10(r["downloads"] + 1) + 2 * r["rating"], r))
    return res


# ---------------------------------------------------------------- local packs

def local_files():
    out = []
    if not os.path.isdir(FULL):
        return out
    for root, dirs, files in os.walk(FULL, followlinks=True):
        rel_root = os.path.relpath(root, FULL)
        if rel_root.split(os.sep)[0] in ("tta", "freesound"):
            dirs[:] = []
            continue
        for f in files:
            if f.lower().endswith(AUDIO_EXTS):
                rel = os.path.normpath(os.path.join(rel_root, f))
                out.append({"ref": f"local:{rel}", "title": os.path.splitext(f)[0],
                            "type": "local", "tags": rel.split(os.sep)[:-1], "flavor": "", "path": rel})
    return out


def search_local(query, excludes):
    res = []
    for t in local_files():
        nice = re.sub(r"[_\-.]+", " ", t["path"])
        s = score(query, excludes, [(4, words(re.sub(r"[_\-.]+", " ", t["title"]))), (2, words(nice))])
        if s:
            res.append((s, t))
    return res


# ---------------------------------------------------------------- resolve / fetch

def resolve(ref):
    src, _, ident = ref.partition(":")
    if src == "tta":
        for t in tta_catalogue():
            if t["ref"] == ref:
                return t
        sys.exit(f"No Tabletop Audio track {ref}.")
    if src == "fs":
        meta = os.path.join(FULL, "freesound", f"fs{ident}.json")
        if os.path.exists(meta):
            with open(meta, encoding="utf-8") as fh:
                return json.load(fh)
        return fs_entry(fs_get(f"sounds/{int(ident)}/", fields=FS_FIELDS))
    if src == "local":
        if not os.path.exists(os.path.join(FULL, ident)):
            sys.exit(f"No local file {ident} under {FULL}.")
        return {"ref": ref, "title": os.path.splitext(os.path.basename(ident))[0], "type": "local",
                "tags": [], "flavor": "", "path": ident}
    sys.exit(f"Unknown ref '{ref}': use tta:<n>, fs:<n> or local:<path>.")


def local_path(t):
    """(path under _full, path under the server's assets/audio)."""
    src = t["ref"].split(":", 1)[0]
    if src == "tta":
        return os.path.join("tta", t["file"]), f"tta/{t['file']}"
    if src == "fs":
        name = f"fs{t['ref'][3:]}_{slug(t['title'], 50)}.mp3"
        return os.path.join("freesound", name), f"freesound/{name}"
    parts = t["path"].split(os.sep)
    remote = "/".join(slug(p, 60) for p in parts[:-1])
    stem_, ext = os.path.splitext(parts[-1])
    return t["path"], (remote + "/" if remote else "local/") + slug(stem_, 80) + ext.lower()


def have(t):
    return os.path.exists(os.path.join(FULL, local_path(t)[0]))


def fetch(t):
    rel, _ = local_path(t)
    dest = os.path.join(FULL, rel)
    if os.path.exists(dest):
        return dest
    if not os.path.isdir(FULL):
        sys.exit(f"{FULL} is missing: run python3 tools/check_setup.py --link "
                 "(it links _full to the sync folder's audio-library/).")
    src = t["ref"].split(":", 1)[0]
    if src == "tta":
        if not t.get("file"):
            sys.exit(f"{t['ref']} has no known sound file; try `audio.py refresh`.")
        url = TTA_SOUNDS + t["file"]
    elif src == "fs":
        url = t.get("preview") or sys.exit(f"{t['ref']} has no preview to download.")
    else:
        sys.exit(f"{t['ref']} is a local file but missing: {dest}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f"  downloading {t['ref']} {t['title']} ...", file=sys.stderr)
    data = http(url, binary=True, timeout=300)
    with open(dest + ".part", "wb") as fh:
        fh.write(data)
    os.replace(dest + ".part", dest)
    if src == "fs":   # keep the credit beside the file
        with open(os.path.join(FULL, "freesound", f"fs{t['ref'][3:]}.json"), "w", encoding="utf-8") as fh:
            json.dump(t, fh, ensure_ascii=False, indent=1)
    return dest


def credit(t):
    src = t["ref"].split(":", 1)[0]
    if src == "tta":
        return "Tabletop Audio (tabletopaudio.com), CC BY-NC-ND 4.0"
    if src == "fs":
        return f"\"{t['title']}\" by {t['author']} on Freesound ({t['license']}) {t.get('page', '')}".strip()
    return f"local: {t['path']}"


# ---------------------------------------------------------------- output

def line(t):
    mark = "✓" if have(t) else " "
    src = t["ref"].split(":", 1)[0]
    if src == "tta":
        meta = f"[{t['type']} | {','.join(t['genres'])}]"
    elif src == "fs":
        meta = f"[{t['seconds']}s | {t['license']} | {t['author']} | ★{t['rating']} {t['downloads']}dl]"
    else:
        meta = "[local]"
    out = f"{mark} {t['ref']:<11} {t['title']}  {meta}"
    if t.get("flavor"):
        out += f"\n      {tidy(t['flavor'])}"
    if t.get("tags"):
        out += f"\n      tags: {', '.join(t['tags'][:10])}"
    return out


# ---------------------------------------------------------------- playlist macro

MACRO = r"""// Tyrnarra audio: Foundry playlists for __FOLDER__
// Generated by tools/audio-library/audio.py from __SPEC__. Run as GM (Script macro).
// Add-only: an existing playlist keeps its sounds and settings; only sounds missing
// by name are added. Files live in the shared Data/assets/audio/ folder.
const SPEC = __DATA__;
const MODES = CONST.PLAYLIST_MODES;
const AH = foundry.audio?.AudioHelper ?? globalThis.AudioHelper;
const vol = v => AH.inputToVolume(v ?? 0.5);
let folder = game.folders.find(f => f.type === "Playlist" && f.name === SPEC.folder && !f.folder);
if (!folder) folder = await Folder.create({ name: SPEC.folder, type: "Playlist", sorting: "m" });
const log = [];
for (const [i, pl] of SPEC.playlists.entries()) {
  let p = game.playlists.find(x => x.name === pl.name && x.folder?.id === folder.id);
  if (!p) {
    p = await Playlist.create({ name: pl.name, folder: folder.id, sort: i * 1000,
      mode: MODES[pl.mode] ?? MODES.SEQUENTIAL, fade: pl.fade ?? 2000, description: pl.description ?? "" });
    log.push(`+ playlist <b>${pl.name}</b>`);
  }
  const have = new Set(p.sounds.map(s => s.name));
  const add = pl.sounds.filter(s => !have.has(s.name)).map((s, j) => ({
    name: s.name, path: s.path, repeat: s.repeat ?? true, volume: vol(s.volume),
    fade: s.fade ?? pl.fade ?? 2000, description: s.credit ?? "", sort: (j + p.sounds.size) * 1000 }));
  if (add.length) {
    await p.createEmbeddedDocuments("PlaylistSound", add);
    log.push(`&nbsp;&nbsp;${pl.name}: +${add.length} sound(s)`);
  }
  if (pl.scene) {
    const sc = game.scenes.getName(pl.scene);
    if (!sc) log.push(`&nbsp;&nbsp;<i>scene "${pl.scene}" not found, not linked</i>`);
    else {
      const first = p.sounds.getName(pl.sounds[0]?.name);
      await sc.update({ playlist: p.id, playlistSound: pl.mode === "SIMULTANEOUS" ? null : (first?.id ?? null) });
      log.push(`&nbsp;&nbsp;linked to scene <b>${sc.name}</b>`);
    }
  }
}
ChatMessage.create({ whisper: ChatMessage.getWhisperRecipients("GM"),
  content: `<h3>Audio: ${SPEC.folder}</h3>` + (log.join("<br>") || "Everything was already there.") });
"""


def build_playlists(spec):
    out = {"folder": spec["folder"], "playlists": []}
    refs = []
    for pl in spec["playlists"]:
        mode = pl.get("mode", "sequential").upper()
        if mode not in ("SEQUENTIAL", "SHUFFLE", "SIMULTANEOUS", "DISABLED"):
            sys.exit(f"Playlist '{pl['name']}': mode must be sequential, shuffle, simultaneous or disabled.")
        sounds = []
        for s in pl["sounds"]:
            s = {"ref": s} if isinstance(s, str) else s
            t = resolve(s["ref"])
            refs.append(t)
            sounds.append({k: v for k, v in {
                "name": s.get("name") or re.sub(r"\.(wav|mp3|flac|ogg|aiff?|m4a)$", "", t["title"], flags=re.I),
                "path": f"{REMOTE_SUB}/{local_path(t)[1]}",
                "volume": s.get("volume"), "repeat": s.get("repeat"), "fade": s.get("fade"),
                "credit": credit(t)}.items() if v is not None})
        out["playlists"].append({k: v for k, v in {
            "name": pl["name"], "mode": mode, "fade": pl.get("fade"), "scene": pl.get("scene"),
            "description": pl.get("description"), "sounds": sounds}.items() if v is not None})
    return out, refs


def upload(tracks):
    from upload_foundry import foundry_remote
    host, root = foundry_remote()
    stage = os.path.join(CACHE, "stage")
    if os.path.isdir(stage):
        subprocess.run(["rm", "-rf", stage], check=True)
    for t in tracks:
        src = fetch(t)
        dst = os.path.join(stage, *local_path(t)[1].split("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.lexists(dst):
            os.symlink(src, dst)
    # -L copies the files behind the stage links; no --delete, so other audio stays.
    subprocess.run(["rsync", "-rtL", "--mkpath", "--chmod=D755,F644", "--itemize-changes",
                    stage + "/", f"{host}:{root}/data/Data/{REMOTE_SUB}/"], check=True)
    print(f"Uploaded {len(tracks)} file(s) to Data/{REMOTE_SUB}/", file=sys.stderr)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search the sources; prefix a word with - to exclude it.")
    s.add_argument("terms", nargs="+")
    s.add_argument("--source", default="auto", help="tta,fs,local (default: all; fs only when a key is set)")
    s.add_argument("--type", choices=("any", "ambience", "music"), default="any",
                   help="Tabletop Audio: ambience-led or music-led tracks only")
    s.add_argument("--setting", choices=("fantasy", "any"), default="fantasy",
                   help="fantasy (default) drops sci-fi/modern-only Tabletop Audio tracks")
    s.add_argument("-n", "--limit", type=int, default=12)
    s.add_argument("--min-dur", type=float, help="Freesound: shortest length in seconds")
    s.add_argument("--max-dur", type=float, help="Freesound: longest length in seconds")
    s.add_argument("--cc0", action="store_true", help="Freesound: CC0 only")
    s.add_argument("--fs-sort", default="score",
                   help="Freesound sort: score, rating_desc, downloads_desc, duration_desc ...")
    s.add_argument("--json", action="store_true")

    sh = sub.add_parser("show", help="Full metadata for refs.")
    sh.add_argument("refs", nargs="+")
    f = sub.add_parser("fetch", help="Download refs into _full/.")
    f.add_argument("refs", nargs="+")
    sub.add_parser("refresh", help="Re-download the Tabletop Audio catalogue.")

    p = sub.add_parser("playlist", help="Spec -> Foundry playlist macro (and upload the files).")
    p.add_argument("--spec", required=True)
    p.add_argument("--out", help="Write the macro here (default: stdout).")
    p.add_argument("--upload", action="store_true", help="Fetch and rsync the files to the server first.")
    # `-word` excludes a word from a search; argparse would read it as an unknown option.
    a, extra = ap.parse_known_args()
    bad = [x for x in extra if not (x.startswith("-") and not x.startswith("--") and len(x) > 1)]
    if bad or (extra and a.cmd != "search"):
        ap.error(f"unrecognized arguments: {' '.join(extra)}")
    if extra:
        a.terms += extra

    if a.cmd == "refresh":
        print(f"{len(tta_catalogue(force=True))} Tabletop Audio tracks cached.")
    elif a.cmd == "search":
        terms = [w for t in a.terms for w in t.split()]
        query = [stem(w) for w in terms if not w.startswith("-")]
        excludes = {stem(w[1:]) for w in terms if w.startswith("-") and len(w) > 1}
        if a.source == "auto":
            sources = ["tta", "local"] + (["fs"] if fs_key() else [])
        else:
            sources = a.source.split(",")
        blocks = []
        if "tta" in sources:
            blocks.append(("Tabletop Audio", search_tta(query, excludes, a)))
        if "local" in sources:
            blocks.append(("Local packs", search_local(query, excludes)))
        if "fs" in sources:
            text = " ".join(w for w in terms if not w.startswith("-")) + "".join(
                f" -{e}" for e in sorted(excludes))
            blocks.append(("Freesound", search_fs(text, a)))
        if a.json:
            print(json.dumps({name: [t for _, t in sorted(r, key=lambda x: -x[0])[:a.limit]]
                              for name, r in blocks}, ensure_ascii=False, indent=1))
            return
        for name, res in blocks:
            res.sort(key=lambda x: -x[0])
            if not res and name == "Local packs" and not local_files():
                continue
            print(f"== {name}: {len(res)} match(es)" + (f", top {a.limit}" if len(res) > a.limit else ""))
            for _, t in res[:a.limit]:
                print(line(t))
            print()
        if "fs" not in sources and a.source == "auto":
            print("(Freesound skipped: no key in tools/keys/freesound.key)")
    elif a.cmd == "show":
        for r in a.refs:
            t = resolve(r)
            print(json.dumps(dict(t, local=os.path.join(FULL, local_path(t)[0]), downloaded=have(t),
                                  server=f"{REMOTE_SUB}/{local_path(t)[1]}", credit=credit(t)),
                             ensure_ascii=False, indent=1))
    elif a.cmd == "fetch":
        for r in a.refs:
            print(fetch(resolve(r)))
    elif a.cmd == "playlist":
        with open(a.spec, encoding="utf-8") as fh:
            spec = json.load(fh)
        data, tracks = build_playlists(spec)
        if a.upload:
            upload(tracks)
        js = (MACRO.replace("__FOLDER__", spec["folder"])
                   .replace("__SPEC__", os.path.basename(a.spec))
                   .replace("__DATA__", json.dumps(data, ensure_ascii=False, indent=1)))
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(js)
            print(f"Wrote {a.out}: {len(data['playlists'])} playlist(s), "
                  f"{sum(len(p['sounds']) for p in data['playlists'])} sound(s).", file=sys.stderr)
        else:
            print(js)


if __name__ == "__main__":
    main()
