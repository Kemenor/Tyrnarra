#!/usr/bin/env python3
"""
build_db.py - Flatten Foundry pf2e creature JSON into a queryable SQLite DB.

Source-agnostic: point --packs at any number of directories containing Foundry
actor JSON (type == "npc"). Official bestiaries and your Tyrnarra/Azkataria
homebrew can live side by side; everything is tagged with `pack` (folder name)
and `source` (publication title) so you can filter or mix freely.

Dedup: when official packs overlap (legacy Bestiary 1-3 vs. Monster Core), the
same creature appears twice. Official rows are deduped by name, preferring the
remastered entry. Homebrew rows are never deduped away (yours always survive).

Designed to be re-run from scratch on every rebuild (drops + recreates).
"""
import argparse
import glob
import html
import json
import os
import re
import sqlite3

# Canonical PF2e creature-type traits, in priority order. The first one a
# creature has becomes its `creature_type` (the best single thematic bucket).
TYPE_TRAITS = [
    "aberration", "undead", "fiend", "celestial", "dragon", "fey", "elemental",
    "construct", "ooze", "plant", "fungus", "giant", "beast", "animal",
    "monitor", "spirit", "astral", "ethereal", "dream", "time", "humanoid",
]

TAG_RE = re.compile(r"<[^>]+>")
INLINE_RE = re.compile(r"@[A-Za-z]+\[[^\]]*\](\{[^}]*\})?")  # @UUID[...]{...}, @Damage[...]


def clean_text(s: str) -> str:
    if not s:
        return ""
    s = INLINE_RE.sub(lambda m: (m.group(1) or "")[1:-1] if m.group(1) else "", s)
    s = TAG_RE.sub(" ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def derive_type(traits):
    tset = set(traits)
    for t in TYPE_TRAITS:
        if t in tset:
            return t
    return "unknown"


def load_creature(path, pack, is_homebrew):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    # Packs also carry non-actor JSON (e.g. _folders.json holds a list).
    if not isinstance(d, dict) or d.get("type") != "npc":
        return None
    sys = d.get("system", {})
    det = sys.get("details", {})
    tr = sys.get("traits", {})
    attrs = sys.get("attributes", {})
    traits = [t for t in tr.get("value", []) if t]
    flavor = " ".join(filter(None, [det.get("blurb"), clean_text(det.get("publicNotes", ""))]))

    # Defenses: weaknesses/resistances carry a value; immunities are bare types
    # (a mix of damage types and conditions). Any of these can be null/empty.
    def _typed_values(key):
        return [(x["type"], x.get("value"))
                for x in (attrs.get(key) or []) if x.get("type")]
    immunities = [x["type"] for x in (attrs.get("immunities") or []) if x.get("type")]

    # Movement: land speed + every otherSpeeds entry (fly/swim/climb/burrow/...).
    speed = attrs.get("speed") or {}
    speeds = []
    if speed.get("value") not in (None, ""):
        speeds.append(("land", speed.get("value")))
    for o in speed.get("otherSpeeds") or []:
        if o.get("type"):
            speeds.append((o["type"], o.get("value")))

    # Senses (darkvision/tremorsense/scent/...) from the perception block.
    senses = [s["type"] for s in (sys.get("perception", {}).get("senses") or [])
              if s.get("type")]

    # Spellcasting: caster flag + the set of traditions across all entries.
    caster_entries = [it for it in d.get("items", []) if it.get("type") == "spellcastingEntry"]
    traditions = sorted({(it.get("system", {}).get("tradition", {}) or {}).get("value")
                         for it in caster_entries} - {None, ""})

    return {
        "slug": os.path.splitext(os.path.basename(path))[0],
        "name": d.get("name", "").strip(),
        "level": (det.get("level") or {}).get("value"),
        "size": (tr.get("size") or {}).get("value", ""),
        "rarity": tr.get("rarity", "common"),
        "creature_type": derive_type(traits),
        "traits": traits,
        "weaknesses": _typed_values("weaknesses"),
        "resistances": _typed_values("resistances"),
        "immunities": immunities,
        "speeds": speeds,
        "senses": senses,
        "caster": 1 if caster_entries else 0,
        "traditions": " ".join(traditions),
        "hp": (attrs.get("hp") or {}).get("max"),
        "ac": (attrs.get("ac") or {}).get("value"),
        "pack": pack,
        "source": (det.get("publication") or {}).get("title") or pack,
        "remaster": 1 if (det.get("publication") or {}).get("remaster") else 0,
        "is_homebrew": 1 if is_homebrew else 0,
        "flavor": flavor,
    }


SCHEMA = """
DROP TABLE IF EXISTS creatures;
DROP TABLE IF EXISTS creature_traits;
DROP TABLE IF EXISTS creature_weaknesses;
DROP TABLE IF EXISTS creature_resistances;
DROP TABLE IF EXISTS creature_immunities;
DROP TABLE IF EXISTS creature_speeds;
DROP TABLE IF EXISTS creature_senses;
DROP TABLE IF EXISTS creatures_fts;
CREATE TABLE creatures (
    id INTEGER PRIMARY KEY,
    slug TEXT, name TEXT, level INTEGER, size TEXT, rarity TEXT,
    creature_type TEXT, hp INTEGER, ac INTEGER, pack TEXT, source TEXT,
    remaster INTEGER, is_homebrew INTEGER, caster INTEGER, traditions TEXT,
    traits_text TEXT, flavor TEXT
);
CREATE TABLE creature_traits (creature_id INTEGER, trait TEXT);
CREATE TABLE creature_weaknesses (creature_id INTEGER, type TEXT, value INTEGER);
CREATE TABLE creature_resistances (creature_id INTEGER, type TEXT, value INTEGER);
CREATE TABLE creature_immunities (creature_id INTEGER, type TEXT);
CREATE TABLE creature_speeds (creature_id INTEGER, type TEXT, value INTEGER);
CREATE TABLE creature_senses (creature_id INTEGER, type TEXT);
CREATE INDEX idx_ct_trait ON creature_traits(trait);
CREATE INDEX idx_weak ON creature_weaknesses(type);
CREATE INDEX idx_resist ON creature_resistances(type);
CREATE INDEX idx_immune ON creature_immunities(type);
CREATE INDEX idx_speed ON creature_speeds(type);
CREATE INDEX idx_sense ON creature_senses(type);
CREATE INDEX idx_level ON creatures(level);
CREATE INDEX idx_type ON creatures(creature_type);
CREATE INDEX idx_pack ON creatures(pack);
CREATE VIRTUAL TABLE creatures_fts USING fts5(
    name, traits_text, flavor, content='creatures', content_rowid='id'
);
"""


def load_dir(d, is_homebrew):
    pack = os.path.basename(os.path.normpath(d))
    out = []
    for path in glob.glob(os.path.join(d, "**", "*.json"), recursive=True):
        c = load_creature(path, pack, is_homebrew)
        if c and c["level"] is not None:
            out.append(c)
    return out


def dedup(loaded):
    """Official rows deduped by name (prefer remaster); homebrew always kept."""
    chosen, homebrew = {}, []
    for c in loaded:
        if c["is_homebrew"]:
            homebrew.append(c)
            continue
        k = c["name"].lower()
        cur = chosen.get(k)
        if cur is None or (c["remaster"] and not cur["remaster"]):
            chosen[k] = c
    return list(chosen.values()) + homebrew


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packs", nargs="+", required=True,
                    help="Directories of official Foundry actor JSON (globbed recursively).")
    ap.add_argument("--homebrew", help="Directory of your homebrew actor JSON (never deduped away).")
    ap.add_argument("--out", default="bestiary.db")
    args = ap.parse_args()

    loaded = []
    for d in args.packs:
        loaded += load_dir(d, is_homebrew=False)
    if args.homebrew and os.path.isdir(args.homebrew):
        loaded += load_dir(args.homebrew, is_homebrew=True)

    rows = dedup(loaded)

    con = sqlite3.connect(args.out)
    con.executescript(SCHEMA)
    for c in rows:
        cur = con.execute(
            "INSERT INTO creatures(slug,name,level,size,rarity,creature_type,"
            "hp,ac,pack,source,remaster,is_homebrew,caster,traditions,traits_text,flavor) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (c["slug"], c["name"], c["level"], c["size"], c["rarity"],
             c["creature_type"], c["hp"], c["ac"], c["pack"], c["source"],
             c["remaster"], c["is_homebrew"], c["caster"], c["traditions"],
             " ".join(c["traits"]), c["flavor"]))
        cid = cur.lastrowid
        con.executemany("INSERT INTO creature_traits VALUES (?,?)",
                        [(cid, t) for t in c["traits"]])
        con.executemany("INSERT INTO creature_weaknesses VALUES (?,?,?)",
                        [(cid, t, v) for t, v in c["weaknesses"]])
        con.executemany("INSERT INTO creature_resistances VALUES (?,?,?)",
                        [(cid, t, v) for t, v in c["resistances"]])
        con.executemany("INSERT INTO creature_immunities VALUES (?,?)",
                        [(cid, t) for t in c["immunities"]])
        con.executemany("INSERT INTO creature_speeds VALUES (?,?,?)",
                        [(cid, t, v) for t, v in c["speeds"]])
        con.executemany("INSERT INTO creature_senses VALUES (?,?)",
                        [(cid, t) for t in c["senses"]])
    con.execute("INSERT INTO creatures_fts(rowid,name,traits_text,flavor) "
                "SELECT id,name,traits_text,flavor FROM creatures")
    con.commit()
    dropped = len(loaded) - len(rows)
    print(f"Ingested {len(rows)} creatures -> {args.out} "
          f"({dropped} duplicate official entries collapsed)")
    con.close()


if __name__ == "__main__":
    main()
