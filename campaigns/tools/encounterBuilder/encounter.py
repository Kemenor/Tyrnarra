#!/usr/bin/env python3
"""
encounter.py - Thematic creature search + PF2e encounter builder over bestiary.db.

PF2e encounter budgets are fully deterministic, so the math here is exact; the
only "fuzzy" part is which creatures get pulled from the filtered pool.

  search:  filter the bestiary by type / level / size / rarity / trait / text / source
  build:   assemble an encounter to a threat budget for a given party

search() and build() are plain functions (kept importable for a future MCP wrap).

Examples:
  python encounter.py search --type undead --level 3-7 --text "swamp bog" --rarity common
  python encounter.py search --trait fire --trait undead --size lg   # fire AND undead
  python encounter.py build --party-level 5 --party-size 4 --threat severe \
         --type undead --text crypt --shape boss --tolerance 0.1
"""
import argparse
import random
import sqlite3
import sys

# --- PF2e budget tables (GM Core) -------------------------------------------
THREAT_BUDGET = {"trivial": 40, "low": 60, "moderate": 80, "severe": 120, "extreme": 160}
# XP added to / removed from the budget per character above/below a party of 4:
THREAT_ADJUST = {"trivial": 10, "low": 20, "moderate": 20, "severe": 30, "extreme": 40}
# Creature XP by its level relative to the party level:
XP_BY_REL = {-4: 10, -3: 15, -2: 20, -1: 30, 0: 40, 1: 60, 2: 80, 3: 120, 4: 160}

# Selection templates: which relative-level bands a "shape" prefers, in order.
SHAPES = {
    "boss":   [3, 2, -1, -2, -3, -4],      # one big threat, then chaff
    "elite":  [2, 1, 0, -1],               # a tough pair/trio
    "spread": [1, 0, -1, 0, 1, -1],        # several near-level foes
    "horde":  [-2, -3, -4, -2, -3, -4],    # many weak foes
}


def budget(party_level, party_size, threat):
    return THREAT_BUDGET[threat] + THREAT_ADJUST[threat] * (party_size - 4)


def connect(db):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con


def search(con, ctype=None, traits=None, weak=None, resist=None, immune=None,
           move=None, family=None, level=None, size=None, rarity=None,
           source=None, no_homebrew=False, text=None, limit=200):
    where, where_params = ["1=1"], []
    joins, join_params = [], []

    if ctype:
        where.append("c.creature_type = ?"); where_params.append(ctype)
    if rarity:
        where.append("c.rarity = ?"); where_params.append(rarity)
    if size:
        where.append("c.size = ?"); where_params.append(size)
    if source:
        where.append("c.pack = ?"); where_params.append(source)
    if no_homebrew:
        where.append("c.is_homebrew = 0")
    if level:
        lo, hi = level
        where.append("c.level BETWEEN ? AND ?"); where_params += [lo, hi]
    if family:
        # "Family" has no Foundry field: it's a trait for most kinds (dragon,
        # demon, construct...) and only a name for the rest (mephit, sphinx).
        f = family.lower()
        where.append("(EXISTS (SELECT 1 FROM creature_traits ft "
                     "WHERE ft.creature_id = c.id AND ft.trait = ?) OR c.name LIKE ?)")
        where_params += [f, f"%{f}%"]

    # Junction-based AND filters: one join per requested value (repeat => must
    # have all). Join text comes before WHERE, so its params bind first.
    def add(table, col, values, alias):
        for i, v in enumerate(values or []):
            a = f"{alias}{i}"
            joins.append(f"JOIN {table} {a} ON {a}.creature_id = c.id AND {a}.{col} = ?")
            join_params.append(v)
    add("creature_traits", "trait", traits, "ct")
    add("creature_weaknesses", "type", weak, "w")
    add("creature_resistances", "type", resist, "r")
    add("creature_immunities", "type", immune, "im")
    add("creature_speeds", "type", move, "sp")

    if text:
        joins.append("JOIN creatures_fts f ON f.rowid = c.id")
        where.append("creatures_fts MATCH ?"); where_params.append(text)

    sql = (f"SELECT DISTINCT c.* FROM creatures c {' '.join(joins)} "
           f"WHERE {' AND '.join(where)} ORDER BY c.level, c.name LIMIT {int(limit)}")
    return [dict(r) for r in con.execute(sql, join_params + where_params)]


def defenses(con, cid):
    """Per-creature weakness/resistance/immunity/speed summary for verbose output."""
    def fetch(table, valued):
        rows = con.execute(f"SELECT type, value FROM {table} WHERE creature_id = ?"
                           if valued else
                           f"SELECT type FROM {table} WHERE creature_id = ?", (cid,))
        if valued:
            return [f"{t} {v}" if v is not None else t for t, v in rows]
        return [t for (t,) in rows]
    return {"speed": fetch("creature_speeds", True),
            "weak": fetch("creature_weaknesses", True),
            "resist": fetch("creature_resistances", True),
            "immune": fetch("creature_immunities", False)}


def build(con, party_level, party_size, threat, shape="spread", seed=None,
          tolerance=0.0, **filters):
    rng = random.Random(seed)
    cap = budget(party_level, party_size, threat)
    floor = round(cap * (1 - tolerance))      # acceptable to stop anywhere in [floor, cap]
    pool = search(con, level=(party_level - 4, party_level + 4), limit=1000, **filters)
    by_rel = {}
    for c in pool:
        by_rel.setdefault(c["level"] - party_level, []).append(c)

    picks, spent = [], 0
    for rel in SHAPES.get(shape, SHAPES["spread"]):
        candidates = by_rel.get(rel, [])
        if not candidates:
            continue
        cost = XP_BY_REL[rel]
        if spent + cost > cap:
            continue
        picks.append(rng.choice(candidates))
        spent += cost
    # Top up toward the budget; stop once we're within the tolerance band (>= floor).
    progress = True
    while spent < floor and progress:
        progress = False
        for rel in sorted(XP_BY_REL, key=lambda r: XP_BY_REL[r]):
            if by_rel.get(rel) and spent + XP_BY_REL[rel] <= cap:
                picks.append(rng.choice(by_rel[rel])); spent += XP_BY_REL[rel]
                progress = True
                break

    warning = None
    if spent < floor:
        warning = (f"pool too thin to reach floor ({spent}/{floor} XP); "
                   f"widen filters or lower the threat")

    # Collapse duplicates into counts.
    agg = {}
    for c in picks:
        agg.setdefault(c["slug"], {"c": c, "n": 0})["n"] += 1
    return {"budget": cap, "floor": floor, "spent": spent, "threat": threat,
            "fill_pct": round(100 * spent / cap) if cap else 0, "warning": warning,
            "members": [{"name": v["c"]["name"], "level": v["c"]["level"],
                         "type": v["c"]["creature_type"], "count": v["n"],
                         "source": v["c"]["source"],
                         "xp_each": XP_BY_REL[v["c"]["level"] - party_level]}
                        for v in agg.values()]}


def parse_level(s):
    if "-" in s:
        a, b = s.split("-"); return (int(a), int(b))
    return (int(s), int(s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="bestiary.db")
    sub = ap.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--type", dest="ctype")
    common.add_argument("--trait", action="append", dest="traits",
                        help="Repeatable; multiple traits are ANDed.")
    common.add_argument("--weak", action="append", help="Has weakness to type (repeatable, AND).")
    common.add_argument("--resist", action="append", help="Has resistance to type (repeatable, AND).")
    common.add_argument("--immune", action="append", help="Immune to damage type or condition (repeatable, AND).")
    common.add_argument("--move", action="append", help="Has movement type, e.g. fly/swim/climb/burrow (repeatable, AND).")
    common.add_argument("--family", help="Creature kind: matches a trait OR the name (dragon, mephit, construct...).")
    common.add_argument("--size")
    common.add_argument("--rarity")
    common.add_argument("--text")
    common.add_argument("--source", help="Restrict to one pack (folder name, e.g. pathfinder-monster-core).")
    common.add_argument("--no-homebrew", action="store_true")

    s = sub.add_parser("search", parents=[common])
    s.add_argument("--level", type=parse_level)
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("-v", "--verbose", action="store_true",
                   help="Print each result's speeds and defenses.")

    b = sub.add_parser("build", parents=[common])
    b.add_argument("--party-level", type=int, required=True)
    b.add_argument("--party-size", type=int, default=4)
    b.add_argument("--threat", default="moderate", choices=list(THREAT_BUDGET))
    b.add_argument("--shape", default="spread", choices=list(SHAPES))
    b.add_argument("--tolerance", type=float, default=0.0,
                   help="Fraction under budget that's acceptable, e.g. 0.1 = stop at 90%%+.")
    b.add_argument("--seed", type=int)

    a = ap.parse_args()
    con = connect(a.db)
    filt = dict(ctype=a.ctype, traits=a.traits, weak=a.weak, resist=a.resist,
                immune=a.immune, move=a.move, family=a.family, size=a.size,
                rarity=a.rarity, source=a.source, no_homebrew=a.no_homebrew, text=a.text)

    if a.cmd == "search":
        rows = search(con, level=a.level, limit=a.limit, **filt)
        for r in rows:
            print(f"  L{r['level']:>2} {r['name']:<34} {r['creature_type']:<10} "
                  f"{r['rarity']:<8} {r['source']}")
            if a.verbose:
                d = defenses(con, r["id"])
                for k in ("speed", "weak", "resist", "immune"):
                    if d[k]:
                        print(f"         {k:>7}: {', '.join(str(x) for x in d[k])}")
        print(f"\n{len(rows)} result(s)")
    else:
        res = build(con, a.party_level, a.party_size, a.threat, shape=a.shape,
                    seed=a.seed, tolerance=a.tolerance, **filt)
        print(f"\n{a.threat.upper()} encounter for {a.party_size}x level "
              f"{a.party_level}  |  budget {res['budget']} XP, "
              f"spent {res['spent']} XP ({res['fill_pct']}%)  |  shape: {a.shape}\n")
        for m in res["members"]:
            print(f"  {m['count']}x  L{m['level']:>2}  {m['name']:<34} "
                  f"({m['type']}, {m['xp_each']} XP ea)  {m['source']}")
        if res["warning"]:
            print(f"\n  ! {res['warning']}", file=sys.stderr)
        print()


if __name__ == "__main__":
    main()
