#!/usr/bin/env python3
r"""
foundry_macro.py - Turn a compact quest spec into a paste-and-run Foundry VTT
Script Macro that builds the quest's actor folder, imports its monsters + NPCs
from your installed compendiums, and creates loot-actor "chests" with items and
coins.

Why a macro (not a REST push): a macro runs inside your GM browser with the full
`game` API, needs no module / relay / API key, works the same on Forge-hosted
and self-hosted worlds, and ships *zero* Paizo stat data - every actor and item
is resolved by name from the compendiums your world already has, so the numbers
always match your installed system version.

Verified live against Foundry VTT 14.363 / pf2e 8.2.0 (the create -> verify ->
delete cycle for Folder.create, importFromCompendium with rename, blank npc
Actor.create, loot Actor.create, createEmbeddedDocuments, and the pf2e
inventory.addCoins coin API all pass).

The spec (JSON):

  {
    "folder": "Venomqueen's Lair",
    "monsters": [
      { "name": "Giant Viper", "count": 4 },
      { "name": "Goblin Warrior", "count": 6, "pack": "pathfinder-monster-core" }
    ],
    "npcs": [
      { "name": "The Venomqueen", "base": "Drow Priestess" },   // import + rename
      { "name": "Innkeeper Bren" }                               // blank narrative npc
    ],
    "chests": [
      { "name": "Hoard Chest",
        "items": [ { "name": "Dagger", "count": 1 }, { "name": "Lesser Healing Potion", "count": 3 } ],
        "coins": "120 gp" }                                      // or {"gp":120,"sp":40} or 120
    ]
  }

Only `folder` is required. `monsters` / `npcs` / `chests` are each optional.
`pack` on a monster/npc/item is an optional exact-pack hint: a bare repo folder
name ("pathfinder-monster-core") is prefixed to "pf2e.<name>"; a dotted value
("forge-vtt-shared-compendiums-tyrnara.actor-2-monsters-tyrnara") is used as-is.
Without a hint, the macro resolves by name against a remaster-first priority list
and then every other compendium as fallback.

CLI:
  python foundry_macro.py build --spec spec.json            # macro -> stdout
  python foundry_macro.py build --spec spec.json --out lair.js
  cat spec.json | python foundry_macro.py build              # spec on stdin

Assemble a spec straight from the leaf tools' --json (quest-workflow Phase 7),
so the spec falls out of the build instead of being hand-mapped:

  python foundry_macro.py spec --folder "Venomqueen's Lair" \
      --encounter room1.json room2.json \      # encounter.py build --json
      --loot haul.json --chest-name "Hoard Chest" \   # loot.py build --json
      --npc "The Venomqueen=Drow Priestess" \  # promote a boss: rename + base
      --npc "Innkeeper Bren" \                  # blank narrative npc
      --merge venomqueen.spec.json \            # extend a saved spec (optional)
      --out venomqueen.spec.json

make_macro(spec), spec_from_tools(...) and coins_to_dict(value) are importable
for an in-process Phase-7 orchestrator.
"""
import argparse
import json
import re
import sys

# Remaster-first priority, mirroring encounter.py's CORE_PACKS dedup preference.
# The macro tries these (in order) before falling back to every other Actor
# compendium in the world.
ACTOR_PRIORITY = [
    "pf2e.pathfinder-monster-core", "pf2e.pathfinder-monster-core-2",
    "pf2e.pathfinder-npc-core", "pf2e.npc-gallery",
    "pf2e.pathfinder-bestiary", "pf2e.pathfinder-bestiary-2",
    "pf2e.pathfinder-bestiary-3",
]
# loot.py's items.db is built only from the equipment pack, which lives in the
# world as pf2e.equipment-srd (the one folder->collection rename); other item
# packs are the fallback.
ITEM_PRIORITY = ["pf2e.equipment-srd"]


def coins_to_dict(value):
    """Normalize a coins value into a {pp,gp,sp,cp} dict for pf2e addCoins().

    Accepts:
      - a dict already in coin form ({"gp":120,"sp":40}) -> returned as-is
      - a number (gp) -> decomposed to whole gp + sp + cp
      - a string from loot.py's `currency` ("120 gp", "1.5 gp", "50 cp", "-")
    Value is preserved exactly (no lossy rounding); platinum is left to gp.
    """
    if value is None:
        return {}
    if isinstance(value, dict):
        return {k: int(v) for k, v in value.items() if v}
    if isinstance(value, (int, float)):
        total_cp = round(float(value) * 100)
    else:
        s = str(value).strip().lower()
        if not s or s == "-":
            return {}
        m = re.match(r"^([0-9]*\.?[0-9]+)\s*(pp|gp|sp|cp)?$", s)
        if not m:
            raise ValueError(f"unparseable coins value: {value!r}")
        amount, unit = float(m.group(1)), (m.group(2) or "gp")
        mult = {"pp": 1000, "gp": 100, "sp": 10, "cp": 1}[unit]
        total_cp = round(amount * mult)
    gp, rem = divmod(total_cp, 100)
    sp, cp = divmod(rem, 10)
    out = {}
    if gp:
        out["gp"] = gp
    if sp:
        out["sp"] = sp
    if cp:
        out["cp"] = cp
    return out


_DISPOSITIONS = ("hostile", "neutral", "friendly", "secret")


def _parse_place(s):
    """Parse a --place string 'AREA=Name[*N][:disposition]' into a placement dict.

    Examples: "1 . Entry=Goblin Warrior*3", "5 . Brood=The Broodmother:hostile".
    """
    label, sep, rest = s.partition("=")
    if not sep:
        raise ValueError(f"--place needs AREA=Name[*N][:disp]: {s!r}")
    label, rest = label.strip(), rest.strip()
    disp = None
    for d in _DISPOSITIONS:
        if rest.lower().endswith(":" + d):
            disp, rest = d, rest[:-(len(d) + 1)].strip()
            break
    name, star, cnt = rest.partition("*")
    out = {"area": label, "name": name.strip(),
           "count": int(cnt) if star and cnt.strip().isdigit() else 1}
    if disp:
        out["disposition"] = disp
    return out


def _normalize(spec):
    """Validate + canonicalize a spec (coins -> dict, defaults filled)."""
    if not isinstance(spec, dict) or not spec.get("folder"):
        raise ValueError("spec must be an object with a non-empty 'folder'")
    out = {"folder": str(spec["folder"]), "monsters": [], "npcs": [], "chests": []}
    if spec.get("imageBase"):
        out["imageBase"] = str(spec["imageBase"])   # folder prefix joined to bare npc image filenames
    for m in spec.get("monsters") or []:
        out["monsters"].append({"name": m["name"], "count": int(m.get("count", 1)),
                                **({"pack": m["pack"]} if m.get("pack") else {})})
    for n in spec.get("npcs") or []:
        e = {"name": n["name"]}
        if n.get("actor"):
            e["actor"] = n["actor"]          # full custom statblock (pf2e npc document)
        elif n.get("base"):
            e["base"] = n["base"]
        if n.get("pack"):
            e["pack"] = n["pack"]
        if n.get("image"):
            e["image"] = n["image"]          # portrait/token image (filename or path)
        out["npcs"].append(e)
    for c in spec.get("chests") or []:
        items = [{"name": it["name"], "count": int(it.get("count", 1)),
                  **({"pack": it["pack"]} if it.get("pack") else {})}
                 for it in (c.get("items") or [])]
        out["chests"].append({"name": c.get("name", "Treasure"), "items": items,
                              "coins": coins_to_dict(c.get("coins"))})
    # Optional token-placement data: areas are the map-area-editor export (% rects),
    # placement says which actor goes in which area on the active scene.
    if spec.get("areas"):
        out["areas"] = spec["areas"]
    if spec.get("placement"):
        out["placement"] = [{"area": p["area"], "name": p["name"],
                             "count": int(p.get("count", 1)),
                             **({"disposition": p["disposition"]} if p.get("disposition") else {})}
                            for p in spec["placement"]]
    return out


# The macro body. The spec is injected as a JSON literal at __SPEC__; everything
# else is static and was validated against the live API.
_TEMPLATE = r"""/* ============================================================================
   Foundry import macro - generated by gm-notes/tools/foundryExport
   Verified on Foundry VTT 14.363 / pf2e 8.2.0.

   HOW TO USE: Macro Directory -> Create Macro -> Type: "script" -> paste this ->
   Save -> double-click to run (as GM). It creates one Actor folder named below,
   imports one actor per distinct creature (you drop N tokens yourself), renames
   imported NPCs, makes blank npc actors for narrative-only NPCs, and builds each
   loot "chest" actor with its items + coins. Re-running is blocked if the folder
   already exists - delete it first to rebuild.
   ========================================================================== */
(async () => {
  if (!game.user.isGM) return ui.notifications.error("Run this macro as the GM.");

  const SPEC = __SPEC__;
  const ACTOR_PRIORITY = __ACTOR_PRIORITY__;
  const ITEM_PRIORITY = __ITEM_PRIORITY__;

  const orderPacks = (docType, priority) => {
    const all = game.packs.filter(p => p.documentName === docType);
    const head = priority.map(id => all.find(p => p.collection === id)).filter(Boolean);
    const tail = all.filter(p => !priority.includes(p.collection));
    return [...head, ...tail];
  };
  const actorPacks = orderPacks("Actor", ACTOR_PRIORITY);
  const itemPacks = orderPacks("Item", ITEM_PRIORITY);

  const idx = async p => { if (!p.indexed) await p.getIndex(); return p; };

  async function resolve(name, packHint, ordered) {
    if (packHint) {
      const id = String(packHint).includes(".") ? packHint : ("pf2e." + packHint);
      const p = game.packs.get(id);
      if (p) { await idx(p); const e = p.index.getName(name); if (e) return { pack: p, id: e._id }; }
    }
    for (const p of ordered) {
      await idx(p);
      const e = p.index.getName(name);
      if (e) return { pack: p, id: e._id };
    }
    return null;
  }

  // Guard: do not silently double-import on a re-run.
  if (game.folders.find(f => f.type === "Actor" && f.name === SPEC.folder))
    return ui.notifications.error(`An Actor folder "${SPEC.folder}" already exists. Delete it, then re-run.`);
  const folder = await Folder.create({ name: SPEC.folder, type: "Actor" });

  // Tidy subfolders, created lazily so empty categories leave no empty folder.
  const _sub = {};
  const sub = async name => {
    if (!_sub[name]) _sub[name] = await Folder.create({ name, type: "Actor", folder: folder.id });
    return _sub[name].id;
  };

  const made = [], missing = [], byName = {};

  for (const m of (SPEC.monsters || [])) {
    const hit = await resolve(m.name, m.pack, actorPacks);
    if (!hit) { missing.push("monster: " + m.name); continue; }
    // keepId:false: Foundry v14 keeps the source _id by default, so importing the
    // same creature twice (e.g. a boss sharing a base with regular monsters) would
    // collide; a fresh id per import keeps them distinct.
    const a = await game.actors.importFromCompendium(hit.pack, hit.id, { folder: await sub("Monsters") }, { keepId: false });
    byName[a.name] = a;
    made.push(`${m.count || 1}x ${a.name}  (drop ${m.count || 1} token${(m.count || 1) === 1 ? "" : "s"})`);
  }

  // Resolve a spec image (filename joined to SPEC.imageBase, or a full path/URL).
  const imgSrc = img => !img ? null : (String(img).includes("/") ? img : ((SPEC.imageBase || "") + img));

  for (const n of (SPEC.npcs || [])) {
    let a;
    if (n.actor) {
      // Full custom statblock embedded in the spec (a bespoke benchmark monster).
      const doc = foundry.utils.deepClone(n.actor);
      doc.name = n.name; doc.type = doc.type || "npc"; doc.folder = await sub("NPCs");
      doc.prototypeToken = Object.assign({}, doc.prototypeToken, { name: n.name });
      a = await Actor.create(doc);
      made.push("NPC " + a.name + "  (custom statblock)");
    } else if (n.base) {
      const hit = await resolve(n.base, n.pack, actorPacks);
      if (!hit) { missing.push("npc base: " + n.base + " (for " + n.name + ")"); continue; }
      // Rename both the actor and its prototype token, else placed/dropped tokens
      // keep the base creature's name (the actor is renamed but the token is not).
      a = await game.actors.importFromCompendium(hit.pack, hit.id, { folder: await sub("NPCs"), name: n.name, "prototypeToken.name": n.name }, { keepId: false });
      made.push("NPC " + a.name + "  (from " + n.base + ")");
    } else {
      a = await Actor.create({ name: n.name, type: "npc", folder: await sub("NPCs") });
      made.push("NPC " + a.name + "  (blank - statless)");
    }
    byName[a.name] = a;
    // Portrait + circle-masked token (Dynamic Token Ring) from a generated image.
    const src = imgSrc(n.image);
    if (src) await a.update({ img: src, "prototypeToken.texture.src": src, "prototypeToken.ring.enabled": true });
  }

  for (const c of (SPEC.chests || [])) {
    const chest = await Actor.create({ name: c.name, type: "loot", folder: await sub("Loot") });
    const objs = [];
    for (const it of (c.items || [])) {
      const hit = await resolve(it.name, it.pack, itemPacks);
      if (!hit) { missing.push("item: " + it.name + " (for " + c.name + ")"); continue; }
      const obj = (await hit.pack.getDocument(hit.id)).toObject();
      if (it.count && it.count > 1) obj.system.quantity = it.count;
      objs.push(obj);
    }
    if (objs.length) await chest.createEmbeddedDocuments("Item", objs);
    if (c.coins && Object.keys(c.coins).length) await chest.inventory.addCoins(c.coins);
    made.push("Chest " + chest.name + "  (" + objs.length + " item stack" + (objs.length === 1 ? "" : "s") +
      (c.coins && Object.keys(c.coins).length ? " + coins" : "") + ")");
  }

  // ---- optional token placement on the active/viewed scene ----------------
  // Areas are the map-area-editor export (% rects); placement says which actor
  // goes in which area. Tokens fan out, grid-snapped, on the scene you have open.
  const placements = SPEC.placement || [];
  const scene = game.scenes.viewed || game.scenes.active;
  let placed = 0;
  if (placements.length && !scene) {
    missing.push("no active scene - tokens not placed (open the quest scene, delete the folder, re-run)");
  } else if (placements.length) {
    const d = scene.dimensions, g = d.size;
    const DISP = { hostile: -1, neutral: 0, friendly: 1, secret: -2 };
    // pf2e derives a token's disposition from its actor's alliance and ignores a
    // bare disposition arg, so set alliance to colour survivors/foes correctly.
    const ALLIANCE = { hostile: "opposition", friendly: "party", neutral: null };
    const areas = SPEC.areas || [];
    const findArea = ref => {
      if (typeof ref === "number") return areas[ref];
      const k = String(ref).trim().toLowerCase();
      return areas.find(a => String(a.label || "").trim().toLowerCase() === k);
    };
    const center = a => {                      // bounding box of the area's rects -> center px
      const rs = a.rects || [];
      const L = Math.min(...rs.map(r => r.left)), T = Math.min(...rs.map(r => r.top));
      const R = Math.max(...rs.map(r => r.left + r.width)), B = Math.max(...rs.map(r => r.top + r.height));
      return { cx: d.sceneX + (L + R) / 200 * d.sceneWidth, cy: d.sceneY + (T + B) / 200 * d.sceneHeight };
    };
    const tokenData = [];
    for (const p of placements) {
      const area = findArea(p.area), actor = byName[p.name];
      if (!area || !(area.rects || []).length) { missing.push("placement area: " + p.area); continue; }
      if (!actor) { missing.push("placement actor: " + p.name + " (import it first)"); continue; }
      if (p.disposition && p.disposition in ALLIANCE && actor.system?.details && "alliance" in actor.system.details) {
        await actor.update({ "system.details.alliance": ALLIANCE[p.disposition] });
      }
      const { cx, cy } = center(area);
      const n = p.count || 1, tw = actor.prototypeToken?.width || 1, step = g * Math.max(1, tw);
      const cols = Math.ceil(Math.sqrt(n)), rows = Math.ceil(n / cols);
      const disp = (p.disposition in DISP) ? DISP[p.disposition] : -1;
      for (let i = 0; i < n; i++) {
        const ox = (i % cols - (cols - 1) / 2) * step, oy = (Math.floor(i / cols) - (rows - 1) / 2) * step;
        const x = Math.round((cx + ox - tw * g / 2) / g) * g, y = Math.round((cy + oy - tw * g / 2) / g) * g;
        tokenData.push((await actor.getTokenDocument({ x, y, disposition: disp })).toObject());
      }
      placed += n;
    }
    if (tokenData.length) await scene.createEmbeddedDocuments("Token", tokenData);
    if (placed) made.push(`Placed ${placed} token(s) on scene "${scene.name}"`);
  }

  const body = `<h3>Imported "${SPEC.folder}"</h3><ul>${made.map(x => "<li>" + x + "</li>").join("")}</ul>` +
    (missing.length ? `<p style="color:#b33"><b>Unresolved (${missing.length}):</b><br>${missing.join("<br>")}</p>`
      + `<p><i>Check the name spelling, or add a "pack" hint for the exact compendium.</i></p>` : "");
  await ChatMessage.create({ content: body, whisper: [game.user.id] });
  ui.notifications.info(`Imported "${SPEC.folder}": ${made.length} actor(s)` +
    (placed ? `, ${placed} token(s) on "${scene.name}"` : "") +
    (missing.length ? `, ${missing.length} unresolved (see chat)` : "") + ".");
})();
"""


def spec_from_tools(folder, encounters=None, loots=None, npcs=None,
                    chest_names=None, merge=None, areas=None, placements=None):
    """Assemble a foundryExport spec from the leaf tools' --json output.

    folder       : the Actor folder name.
    encounters   : list of `encounter.py build --json` dicts (one per combat
                   area). Their members are merged by name, summing counts.
    loots        : list of `loot.py build --json` dicts; each becomes one chest
                   (permanent + consumables -> items, currency -> coins).
    npcs         : list of "Name" (blank npc) or "Name=Base" (import Base, rename
                   to Name). A promoted Base that appears among the merged
                   monsters has one count removed there (the boss is now an NPC).
    chest_names  : optional names for the chests, positional with `loots`.
    merge        : an existing spec dict to extend (monsters summed, npcs/chests
                   appended) so the spec can accumulate while the quest is built.
    areas        : the map-area-editor export (a list of {label, rects}, or the
                   {"areas":[...]} wrapper) used to position tokens.
    placements   : list of {area, name, count, disposition} token placements.
    """
    base = merge if isinstance(merge, dict) else {}
    # Merge monster counts by name across this call's encounters + any prior spec.
    monsters = {}
    for m in base.get("monsters") or []:
        monsters[m["name"]] = monsters.get(m["name"], 0) + int(m.get("count", 1))
    for enc in encounters or []:
        for mem in enc.get("members") or []:
            monsters[mem["name"]] = monsters.get(mem["name"], 0) + int(mem.get("count", 1))

    npc_entries = list(base.get("npcs") or [])
    for raw in npcs or []:
        name, sep, b = raw.partition("=")
        name, b = name.strip(), b.strip()
        if sep and b:
            npc_entries.append({"name": name, "base": b})
            if b in monsters:                      # the boss is no longer chaff
                monsters[b] -= 1
                if monsters[b] <= 0:
                    del monsters[b]
        else:
            npc_entries.append({"name": name})

    chests = list(base.get("chests") or [])
    names = list(chest_names or [])
    many = len(loots or []) > 1
    for i, haul in enumerate(loots or []):
        items = [{"name": it["name"], "count": int(it.get("count", 1))}
                 for it in (haul.get("permanent") or []) + (haul.get("consumables") or [])]
        cname = names[i] if i < len(names) else (f"Treasure {i + 1}" if many else "Treasure")
        chest = {"name": cname, "items": items}
        if haul.get("currency"):
            chest["coins"] = haul["currency"]
        chests.append(chest)

    spec = {"folder": folder}
    if monsters:
        spec["monsters"] = [{"name": n, "count": c} for n, c in monsters.items()]
    if npc_entries:
        spec["npcs"] = npc_entries
    if chests:
        spec["chests"] = chests
    area_list = (areas.get("areas") if isinstance(areas, dict) else areas) or base.get("areas")
    if area_list:
        spec["areas"] = area_list
    place = list(base.get("placement") or []) + list(placements or [])
    if place:
        spec["placement"] = place
    return spec


def make_macro(spec):
    """Return the Foundry Script Macro text for a quest spec (dict)."""
    norm = _normalize(spec)
    return (_TEMPLATE
            .replace("__SPEC__", json.dumps(norm, ensure_ascii=False, indent=2))
            .replace("__ACTOR_PRIORITY__", json.dumps(ACTOR_PRIORITY))
            .replace("__ITEM_PRIORITY__", json.dumps(ITEM_PRIORITY)))


_ASSIGN_TEMPLATE = r"""/* ============================================================================
   Assign portraits/tokens - generated by gm-notes/tools/foundryExport
   Sets each named actor's portrait + circle-masked token (Dynamic Token Ring)
   from an uploaded image, and re-skins that actor's already-placed tokens.
   Run as GM after uploading the images. Verified on Foundry VTT 14 / pf2e 8.2.0.
   ========================================================================== */
(async () => {
  if (!game.user.isGM) return ui.notifications.error("Run this macro as the GM.");
  const FOLDER = __FOLDER__, BASE = __BASE__, MAP = __MAP__;
  const root = game.folders.find(f => f.type === "Actor" && f.name === FOLDER);
  if (!root) return ui.notifications.error(`No Actor folder "${FOLDER}". Import the quest first.`);
  const ids = new Set([root.id, ...game.folders.filter(f => f.folder?.id === root.id).map(f => f.id)]);
  const done = [], missing = [];
  for (const [name, file] of Object.entries(MAP)) {
    const a = game.actors.find(x => ids.has(x.folder?.id) && x.name === name);
    if (!a) { missing.push(name); continue; }
    const src = String(file).includes("/") ? file : (BASE + file);
    const upd = { "prototypeToken.texture.src": src, "prototypeToken.ring.enabled": __RING__ };
    if (__SETIMG__) upd.img = src;   // baked-frame tokens keep the un-framed portrait as img
    await a.update(upd);
    // pf2e reverts a direct texture.src update on an existing token, so re-skin
    // already-placed tokens by recreating them from the updated prototype,
    // preserving position/disposition.
    for (const sc of game.scenes) {
      const toks = sc.tokens.filter(t => t.actorId === a.id);
      if (!toks.length) continue;
      const geos = toks.map(t => ({ x: t.x, y: t.y, elevation: t.elevation, rotation: t.rotation, hidden: t.hidden, disposition: t.disposition }));
      await sc.deleteEmbeddedDocuments("Token", toks.map(t => t.id));
      const docs = [];
      for (const g of geos) docs.push((await a.getTokenDocument(g)).toObject());
      await sc.createEmbeddedDocuments("Token", docs);
    }
    done.push(name);
  }
  await ChatMessage.create({ content: `<h3>Portraits assigned in ${FOLDER}</h3><ul>${done.map(x => "<li>" + x + "</li>").join("")}</ul>` +
    (missing.length ? `<p style="color:#b33"><b>Not found:</b> ${missing.join(", ")}</p>` : ""), whisper: [game.user.id] });
  ui.notifications.info(`Assigned ${done.length} portrait(s)` + (missing.length ? `, ${missing.length} not found` : "") + ".");
})();
"""


def make_assign_macro(folder, base, mapping, set_img=True, ring=True):
    """Macro that assigns uploaded images to existing actors in `folder` by name.

    mapping: {actor name -> image filename (joined to base) or full path}.
    set_img : also set the actor portrait (img). False = token texture only
              (for baked-frame tokens, keeping the un-framed portrait as img).
    ring    : enable the Dynamic Token Ring. False for baked frames (border is
              already in the image; the ring would double it).
    """
    return (_ASSIGN_TEMPLATE
            .replace("__FOLDER__", json.dumps(folder, ensure_ascii=False))
            .replace("__BASE__", json.dumps(base or "", ensure_ascii=False))
            .replace("__MAP__", json.dumps(mapping, ensure_ascii=False, indent=2))
            .replace("__SETIMG__", "true" if set_img else "false")
            .replace("__RING__", "true" if ring else "false"))


def main():
    ap = argparse.ArgumentParser(description="Generate a Foundry import macro from a quest spec.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="Build a macro from a spec JSON.")
    b.add_argument("--spec", help="Path to the spec JSON (default: stdin).")
    b.add_argument("--out", help="Write the macro here (default: stdout).")

    s = sub.add_parser("spec", help="Assemble a spec from encounter/loot --json output.")
    s.add_argument("--folder", required=True, help="The Actor folder name for the quest.")
    s.add_argument("--encounter", nargs="*", default=[], help="encounter.py build --json file(s).")
    s.add_argument("--loot", nargs="*", default=[], help="loot.py build --json file(s); one chest each.")
    s.add_argument("--chest-name", nargs="*", default=[], help="Chest names, positional with --loot.")
    s.add_argument("--npc", action="append", default=[],
                   help='"Name" (blank npc) or "Name=Base" (import Base, rename to Name). Repeatable.')
    s.add_argument("--areas", help="map-area-editor export JSON (area rects) for token placement.")
    s.add_argument("--place", action="append", default=[], metavar="AREA=Name[*N][:disp]",
                   help="Place N tokens of an imported actor in an area. Repeatable. "
                        "disp = hostile (default) / neutral / friendly / secret.")
    s.add_argument("--merge", help="Existing spec JSON to extend (accumulate while building).")
    s.add_argument("--out", help="Write the spec here (default: stdout).")

    ai = sub.add_parser("assign-images", help="Macro to assign portraits to existing actors by name.")
    ai.add_argument("--folder", required=True, help="The quest's Actor folder name.")
    ai.add_argument("--base", default="", help="Path prefix joined to bare image filenames (the upload folder).")
    ai.add_argument("--map", action="append", default=[], metavar='Name=file',
                    help='"Actor Name=file.webp" (or a full path). Repeatable.')
    ai.add_argument("--token-only", action="store_true",
                    help="Set the token texture only, not the actor portrait (for baked-frame tokens).")
    ai.add_argument("--no-ring", action="store_true",
                    help="Do not enable the Dynamic Token Ring (use for baked-frame tokens).")
    ai.add_argument("--out", help="Write the macro here (default: stdout).")

    a = ap.parse_args()

    if a.cmd == "assign-images":
        mapping = {}
        for raw in a.map:
            name, sep, file = raw.partition("=")
            if not sep:
                sys.exit(f"--map needs Name=file: {raw!r}")
            mapping[name.strip()] = file.strip()
        macro = make_assign_macro(a.folder, a.base, mapping,
                                  set_img=not a.token_only, ring=not a.no_ring)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(macro)
            print(f"Wrote {a.out} ({len(macro)} chars).", file=sys.stderr)
        else:
            sys.stdout.write(macro)
        return

    if a.cmd == "spec":
        load = lambda p: json.load(open(p, encoding="utf-8-sig"))
        spec = spec_from_tools(
            a.folder,
            encounters=[load(p) for p in a.encounter],
            loots=[load(p) for p in a.loot],
            npcs=a.npc,
            chest_names=a.chest_name,
            merge=load(a.merge) if a.merge else None,
            areas=load(a.areas) if a.areas else None,
            placements=[_parse_place(p) for p in a.place],
        )
        out = json.dumps(spec, ensure_ascii=False, indent=2)
        if a.out:
            with open(a.out, "w", encoding="utf-8") as fh:
                fh.write(out + "\n")
            print(f"Wrote {a.out}.", file=sys.stderr)
        else:
            sys.stdout.write(out + "\n")
        return

    raw = open(a.spec, encoding="utf-8-sig").read() if a.spec else sys.stdin.read()
    spec = json.loads(raw)
    macro = make_macro(spec)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(macro)
        print(f"Wrote {a.out} ({len(macro)} chars).", file=sys.stderr)
    else:
        sys.stdout.write(macro)


if __name__ == "__main__":
    main()
