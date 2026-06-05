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
import random
import sqlite3

# --- PF2e treasure tables (GM Core) -----------------------------------------
# Total treasure value gained per character level, for a party of 4. VET THESE.
TREASURE_BY_LEVEL = {
    1: 175, 2: 300, 3: 500, 4: 850, 5: 1350, 6: 2000, 7: 2900, 8: 4000,
    9: 5700, 10: 8000, 11: 11500, 12: 16500, 13: 25000, 14: 36500, 15: 54500,
    16: 82500, 17: 128000, 18: 208000, 19: 355000, 20: 490000,
}
# Canonical permanent-item spread per level: two at level+1, two at level.
# (One extra at `level` per PC above 4; one fewer per PC below.)
PERM_PATTERN = [1, 1, 0, 0]  # offsets from party level


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


def build(con, party_level, party_size=4, share=None, value=None,
          perm_share=0.5, seed=None, **filters):
    """Assemble a themed treasure haul to a target value.

    Both halves follow the GM Core spread (2x level+1, 2x level, +/-1 per PC off
    4): permanent items, then consumables (type=consumable only, so ammo/gems are
    excluded), each a real level-appropriate pick priced from item data. Permanent
    items are held to ~perm_share of the target so they don't eat the haul; coins
    absorb the remainder. `filters` are theme filters (text/trait/rarity/source).
    """
    rng = random.Random(seed)
    cap = lambda lv: max(0, min(20, lv))
    if value is not None:
        target = float(value)
    else:
        base = TREASURE_BY_LEVEL[party_level] * (share if share is not None else 1.0)
        target = base * (party_size / 4)
    target_cp = round(target * 100)

    # Item slots (offsets from party level), scaled by party size.
    offsets = list(PERM_PATTERN)
    extra = party_size - 4
    if extra > 0:
        offsets += [0] * extra
    elif extra < 0:
        offsets = offsets[:max(1, len(offsets) + extra)]

    def pick(lv, budget, item_type, consumable):
        last = []
        for lo in (lv, lv - 1, lv - 2, lv - 3):      # relax downward if theme is thin
            pool = [p for p in search(con, item_type=item_type, level=(cap(lo), cap(lv)),
                                      consumable=consumable, limit=400, **filters)
                    if p["price_cp"]]
            if pool:
                last = pool
                afford = [p for p in pool if p["price_cp"] <= budget]
                if afford:
                    return rng.choice(afford)
        return min(last, key=lambda p: p["price_cp"]) if last else None

    # Permanent items, each capped near an even slice of the permanent portion.
    perm_slot = max(100, round(target_cp * perm_share / max(1, len(offsets))))
    perms = [pick(party_level + off, perm_slot, None, False) for off in offsets]
    perms = [p for p in perms if p]
    perm_spent = sum(p["price_cp"] for p in perms)

    # Consumables: same slot spread, type=consumable only (no ammo/treasure spam).
    cons = [pick(party_level + off, 10 ** 12, ["consumable"], None) for off in offsets]
    cons = [c for c in cons if c]
    cons_spent = sum(c["price_cp"] for c in cons)

    coin_cp = max(0, target_cp - perm_spent - cons_spent)
    total_cp = perm_spent + cons_spent + coin_cp

    def agg(picks):
        out = {}
        for p in picks:
            e = out.setdefault(p["slug"], {"item": p, "n": 0})
            e["n"] += 1
        return [{"name": v["item"]["name"], "level": v["item"]["level"],
                 "type": v["item"]["item_type"], "count": v["n"],
                 "price": gp(v["item"]["price_cp"]), "source": v["item"]["source"]}
                for v in out.values()]

    return {"target": gp(target_cp), "total": gp(total_cp),
            "fill_pct": round(100 * total_cp / target_cp) if target_cp else 0,
            "currency": gp(coin_cp), "permanent": agg(perms), "consumables": agg(cons)}


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

    b = sub.add_parser("build")
    b.add_argument("--party-level", type=int, required=True)
    b.add_argument("--party-size", type=int, default=4)
    b.add_argument("--share", type=float, help="Fraction of the level's treasure this haul is (default 1.0).")
    b.add_argument("--value", type=float, help="Absolute target in gp (overrides --share).")
    b.add_argument("--perm-share", type=float, default=0.5,
                   help="Fraction of the target steered into permanent items (rest is consumables + coins).")
    b.add_argument("--trait", action="append", dest="traits", help="Theme: repeatable, ANDed.")
    b.add_argument("--not-trait", action="append", dest="not_traits")
    b.add_argument("--rarity")
    b.add_argument("--source")
    b.add_argument("--text", help="Theme: fuzzy FTS5 over name/traits/flavor.")
    b.add_argument("--seed", type=int)
    b.add_argument("--json", action="store_true")

    a = ap.parse_args()
    con = connect(a.db)

    if a.cmd == "search":
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
        return

    res = build(con, a.party_level, a.party_size, share=a.share, value=a.value,
                perm_share=a.perm_share, seed=a.seed, traits=a.traits,
                not_traits=a.not_traits, rarity=a.rarity, source=a.source, text=a.text)
    if a.json:
        print(json.dumps(res, indent=2)); return
    print(f"\nTreasure for {a.party_size}x level {a.party_level}  |  target {res['target']}, "
          f"assembled {res['total']} ({res['fill_pct']}%)\n")
    print("  Permanent:")
    for m in res["permanent"]:
        print(f"    {m['count']}x  L{m['level']:>2}  {m['price']:>9}  {m['name']:<36} {m['source']}")
    print("  Consumables:")
    for m in res["consumables"]:
        print(f"    {m['count']}x  L{m['level']:>2}  {m['price']:>9}  {m['name']:<36} {m['source']}")
    print(f"  Coins: {res['currency']}\n")


if __name__ == "__main__":
    main()
