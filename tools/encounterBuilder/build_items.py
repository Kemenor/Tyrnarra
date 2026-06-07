#!/usr/bin/env python3
"""
build_items.py - Flatten Foundry pf2e equipment JSON into a queryable SQLite DB.

Sibling to build_db.py (creatures). Same model: static snapshot, drop + recreate
on every rebuild, dedup official items by name preferring the remastered entry.
Feeds loot.py (thematic item search + treasure-budget building).
"""
import argparse
import glob
import json
import os
import sqlite3

from build_db import clean_text  # shared HTML/inline-tag scrubber

# Item top-level types that are kept/worn rather than spent. Drives the
# permanent-vs-consumable split that PF2e treasure budgeting cares about.
PERMANENT_TYPES = {"weapon", "armor", "shield", "equipment", "backpack", "kit"}


def price_cp(price):
    """Flatten a Foundry price object to total copper (pp/gp/sp/cp)."""
    v = (price or {}).get("value") or {}
    return (v.get("pp", 0) * 1000 + v.get("gp", 0) * 100
            + v.get("sp", 0) * 10 + v.get("cp", 0))


def load_item(path, pack):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    if not isinstance(d, dict) or d.get("type") not in (
            PERMANENT_TYPES | {"consumable", "ammo", "treasure"}):
        return None
    s = d.get("system", {})
    tr = s.get("traits", {})
    itype = d["type"]
    return {
        "slug": os.path.splitext(os.path.basename(path))[0],
        "name": d.get("name", "").strip(),
        "item_type": itype,
        "level": (s.get("level") or {}).get("value", 0),
        "price_cp": price_cp(s.get("price")),
        "rarity": tr.get("rarity", "common"),
        "category": s.get("category") or "",
        "grp": s.get("group") or "",
        "bulk": (s.get("bulk") or {}).get("value"),
        "consumable": 0 if itype in PERMANENT_TYPES else 1,
        "traits": [t for t in tr.get("value", []) if t],
        "pack": pack,
        "source": (s.get("publication") or {}).get("title") or pack,
        "remaster": 1 if (s.get("publication") or {}).get("remaster") else 0,
        "flavor": clean_text((s.get("description") or {}).get("value", "")),
    }


SCHEMA = """
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS item_traits;
DROP TABLE IF EXISTS items_fts;
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    slug TEXT, name TEXT, item_type TEXT, level INTEGER, price_cp INTEGER,
    rarity TEXT, category TEXT, grp TEXT, bulk TEXT, consumable INTEGER,
    pack TEXT, source TEXT, remaster INTEGER, traits_text TEXT, flavor TEXT
);
CREATE TABLE item_traits (item_id INTEGER, trait TEXT);
CREATE INDEX idx_it_trait ON item_traits(trait);
CREATE INDEX idx_item_level ON items(level);
CREATE INDEX idx_item_type ON items(item_type);
CREATE INDEX idx_item_price ON items(price_cp);
CREATE VIRTUAL TABLE items_fts USING fts5(
    name, traits_text, flavor, content='items', content_rowid='id'
);
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--packs", nargs="+", required=True,
                    help="Directories of Foundry equipment JSON (globbed recursively).")
    ap.add_argument("--out", default="items.db")
    args = ap.parse_args()

    loaded = []
    for d in args.packs:
        pack = os.path.basename(os.path.normpath(d))
        for path in glob.glob(os.path.join(d, "**", "*.json"), recursive=True):
            it = load_item(path, pack)
            if it and it["name"]:
                loaded.append(it)

    # Dedup by name, preferring the remastered entry.
    chosen = {}
    for it in loaded:
        k = it["name"].lower()
        cur = chosen.get(k)
        if cur is None or (it["remaster"] and not cur["remaster"]):
            chosen[k] = it
    rows = list(chosen.values())

    con = sqlite3.connect(args.out)
    con.executescript(SCHEMA)
    for it in rows:
        cur = con.execute(
            "INSERT INTO items(slug,name,item_type,level,price_cp,rarity,category,"
            "grp,bulk,consumable,pack,source,remaster,traits_text,flavor) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (it["slug"], it["name"], it["item_type"], it["level"], it["price_cp"],
             it["rarity"], it["category"], it["grp"], str(it["bulk"]),
             it["consumable"], it["pack"], it["source"], it["remaster"],
             " ".join(it["traits"]), it["flavor"]))
        iid = cur.lastrowid
        con.executemany("INSERT INTO item_traits VALUES (?,?)",
                        [(iid, t) for t in it["traits"]])
    con.execute("INSERT INTO items_fts(rowid,name,traits_text,flavor) "
                "SELECT id,name,traits_text,flavor FROM items")
    con.commit()
    dropped = len(loaded) - len(rows)
    print(f"Ingested {len(rows)} items -> {args.out} "
          f"({dropped} duplicate entries collapsed)")
    con.close()


if __name__ == "__main__":
    main()
