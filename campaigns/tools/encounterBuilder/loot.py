#!/usr/bin/env python3
"""
loot.py - Thematic item search over items.db (PF2e equipment).

Sibling to encounter.py. `search` filters the equipment list by type / level /
price / trait / rarity / category / text so loot can be themed and level-gated.
A treasure-budget builder (build) is planned once the GM Core Treasure-by-Level
table is locked; search() is kept importable for it and for a future MCP/skill.

Examples:
  python loot.py search --text "fire OR flame" --level 1-5 --permanent
  python loot.py search --type weapon --trait magical --price-max 200 --core-rarity common
  python loot.py search --type consumable --text "healing" --level 1-3 -v
"""
import argparse
import json
import sqlite3


def connect(db):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con


def gp(price_cp):
    """Render a copper price as a compact gp/sp/cp string."""
    if price_cp is None:
        return "-"
    if price_cp == 0:
        return "0 gp"
    if price_cp % 100 == 0:
        return f"{price_cp // 100} gp"
    if price_cp % 10 == 0:
        return f"{price_cp / 100:g} gp"
    return f"{price_cp} cp"


def search(con, item_type=None, traits=None, not_traits=None, level=None,
           price_min=None, price_max=None, rarity=None, category=None,
           group=None, consumable=None, source=None, text=None, limit=200):
    where, where_params = ["1=1"], []
    joins, join_params = [], []

    if item_type:
        where.append(f"i.item_type IN ({','.join('?' * len(item_type))})")
        where_params += list(item_type)
    if rarity:
        where.append("i.rarity = ?"); where_params.append(rarity)
    if category:
        where.append("i.category = ?"); where_params.append(category)
    if group:
        where.append("i.grp = ?"); where_params.append(group)
    if consumable is not None:
        where.append("i.consumable = ?"); where_params.append(1 if consumable else 0)
    if source:
        where.append("i.source LIKE ?"); where_params.append(f"%{source}%")
    if level:
        lo, hi = level
        where.append("i.level BETWEEN ? AND ?"); where_params += [lo, hi]
    if price_min is not None:
        where.append("i.price_cp >= ?"); where_params.append(int(price_min * 100))
    if price_max is not None:
        where.append("i.price_cp <= ?"); where_params.append(int(price_max * 100))
    for v in not_traits or []:
        where.append("NOT EXISTS (SELECT 1 FROM item_traits x "
                     "WHERE x.item_id = i.id AND x.trait = ?)")
        where_params.append(v)

    for idx, t in enumerate(traits or []):
        a = f"it{idx}"
        joins.append(f"JOIN item_traits {a} ON {a}.item_id = i.id AND {a}.trait = ?")
        join_params.append(t)
    if text:
        joins.append("JOIN items_fts f ON f.rowid = i.id")
        where.append("items_fts MATCH ?"); where_params.append(text)

    sql = (f"SELECT DISTINCT i.* FROM items i {' '.join(joins)} "
           f"WHERE {' AND '.join(where)} ORDER BY i.level, i.price_cp, i.name "
           f"LIMIT {int(limit)}")
    return [dict(r) for r in con.execute(sql, join_params + where_params)]


def parse_level(s):
    if "-" in s:
        a, b = s.split("-"); return (int(a), int(b))
    return (int(s), int(s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="items.db")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("--type", action="append", dest="item_type",
                   help="weapon/armor/shield/equipment/consumable/ammo/treasure; repeatable => OR.")
    s.add_argument("--trait", action="append", dest="traits", help="Repeatable, ANDed.")
    s.add_argument("--not-trait", action="append", dest="not_traits", help="Exclude trait; repeatable.")
    s.add_argument("--level", type=parse_level)
    s.add_argument("--price-min", type=float, help="Minimum price in gp.")
    s.add_argument("--price-max", type=float, help="Maximum price in gp.")
    s.add_argument("--rarity")
    s.add_argument("--category", help="e.g. simple/martial/advanced (weapons), light/medium/heavy (armor).")
    s.add_argument("--group", help="e.g. sword/bow/plate.")
    s.add_argument("--permanent", action="store_true", help="Only kept/worn items.")
    s.add_argument("--consumable", action="store_true", help="Only spent items (consumable/ammo/treasure).")
    s.add_argument("--source", help="Match publication title (substring).")
    s.add_argument("--text", help="Fuzzy FTS5 over name/traits/flavor.")
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--json", action="store_true")
    s.add_argument("-v", "--verbose", action="store_true", help="Print traits per item.")

    a = ap.parse_args()
    con = connect(a.db)

    consumable = True if a.consumable else (False if a.permanent else None)
    rows = search(con, item_type=a.item_type, traits=a.traits, not_traits=a.not_traits,
                  level=a.level, price_min=a.price_min, price_max=a.price_max,
                  rarity=a.rarity, category=a.category, group=a.group,
                  consumable=consumable, source=a.source, text=a.text, limit=a.limit)

    if a.json:
        print(json.dumps(rows, indent=2)); return
    for r in rows:
        print(f"  L{r['level']:>2} {gp(r['price_cp']):>9}  {r['name']:<38} "
              f"{r['item_type']:<10} {r['rarity']:<8} {r['source']}")
        if a.verbose and r["traits_text"]:
            print(f"              traits: {r['traits_text']}")
    print(f"\n{len(rows)} result(s)")


if __name__ == "__main__":
    main()
