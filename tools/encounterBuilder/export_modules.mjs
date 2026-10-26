#!/usr/bin/env node
/*
 * export_modules.mjs - dump the Actor and Item packs of your installed Foundry
 * modules (Battlezoo, Jam & Jax, ...) to plain Foundry JSON so build_db.py
 * (creatures) and build_items.py (loot) can ingest them like the official packs.
 *
 *   node export_modules.mjs            # FOUNDRY_DATA defaults to ~/foundry/data/Data
 *
 * Module packs are LevelDB: an actor lives at `!actors!<id>` and its embedded
 * items at `!actors.items!<actorId>.<itemId>`; the actor's `items` array holds
 * only ids. We re-inline the items so the JSON matches the official pack shape.
 * Item packs hold plain `!items!<id>` documents. Each pack is copied to a temp
 * dir first, so a running Foundry's LOCK never blocks us and we never touch the
 * live pack.
 *
 * Reads with the `classic-level` that ships inside the Foundry app (no npm
 * install). Output, wiped and rewritten each run:
 *   _sources/modules/<module-id>.<pack-name>/<slug>.json        (npc actors)
 *   _sources/module-items/<module-id>.<pack-name>/<slug>.json   (items)
 * _sources/ is gitignored (paid content stays local).
 *
 * Env overrides: FOUNDRY_DATA (the Data dir), FOUNDRY_APP (the app dir).
 * rebuild.py points both at its rsync mirror of the Foundry server (_sources/foundry/).
 */
import { createRequire } from "module";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const HOME = os.homedir();
const DATA = process.env.FOUNDRY_DATA || path.join(HOME, "foundry", "data", "Data");
const APP = process.env.FOUNDRY_APP || path.join(HOME, "foundry", "app");
const OUT = { Actor: path.join(HERE, "_sources", "modules"),
              Item: path.join(HERE, "_sources", "module-items") };

const require = createRequire(path.join(APP, "package.json"));
const { ClassicLevel } = require("classic-level");

const slugify = (s) =>
  s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase()
    .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "doc";

async function readPack(srcDir) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "foundry-pack-"));
  try {
    fs.cpSync(srcDir, tmp, { recursive: true });
    fs.rmSync(path.join(tmp, "LOCK"), { force: true });
    const db = new ClassicLevel(tmp, { valueEncoding: "json" });
    const actors = new Map(), embedded = new Map(), items = [];
    for await (const [k, v] of db.iterator()) {
      if (k.startsWith("!actors!")) actors.set(k.slice(8), v);
      else if (k.startsWith("!actors.items!")) embedded.set(k.slice(14), v);
      else if (k.startsWith("!items!")) items.push(v);
    }
    await db.close();
    for (const [id, a] of actors) {
      a.items = (a.items || []).map((i) =>
        typeof i === "string" ? embedded.get(`${id}.${i}`) : i).filter(Boolean);
    }
    return { actors: [...actors.values()], items };
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

// Module documents often leave publication.title blank; fall back to the
// module's title so `source` reads "Battlezoo Bestiary ..." in results.
function setSource(sys, title) {
  const pub = (sys.publication ??= {});
  if (!pub.title) pub.title = title;
}

function prepActor(a, m, p, mod) {
  // Drop blank build templates ("Alchemist Template lvl 1", "A Monk Template").
  if (a.type !== "npc" || /\btemplate\b/i.test(a.name || "")) return null;
  setSource(((a.system ??= {}).details ??= {}), m.title || mod);
  // Class-NPC indexes (Jam & Jax) ship traitless, ancestry-agnostic actors
  // mixed with their animal companions. Give them a type so --type/--trait
  // work, and put the pack label ("Clerics", "Rogue") in the blurb so
  // --text finds them by class.
  const tr = (a.system.traits ??= {});
  if (!(tr.value || []).length) {
    tr.value = /^(wolf|cat|bear|bird|steed ally)\b/i.test(a.name || "")
      ? ["animal", "minion"] : ["humanoid"];
  }
  if (!a.system.details.blurb) a.system.details.blurb = p.label || p.name;
  return a;
}

function prepItem(it, m, p, mod) {
  setSource((it.system ??= {}), m.title || mod);
  return it;  // build_items.py keeps only the physical item types
}

for (const dir of Object.values(OUT)) fs.rmSync(dir, { recursive: true, force: true });
const modDir = path.join(DATA, "modules");
const total = { Actor: 0, Item: 0 };
for (const mod of fs.readdirSync(modDir).sort()) {
  const manifest = path.join(modDir, mod, "module.json");
  if (!fs.existsSync(manifest)) continue;
  const m = JSON.parse(fs.readFileSync(manifest, "utf8"));
  for (const p of m.packs || []) {
    if (!(p.type in OUT)) continue;
    // Many modules mirror every pack for Starfinder 2e ("sf-...", "sf2e-...").
    if (/^sf(2e)?-/i.test(p.name)) continue;
    // Manifests write pack paths as "packs/x", "/packs/x" or legacy "packs/x.db";
    // the LevelDB lives in the directory without the .db suffix.
    const src = path.join(modDir, mod, p.path.replace(/^\//, "").replace(/\.db$/, ""));
    if (!fs.existsSync(path.join(src, "CURRENT"))) {
      console.warn(`skip ${mod}/${p.name}: no LevelDB at ${src}`);
      continue;
    }
    const pack = await readPack(src);
    const docs = p.type === "Actor"
      ? pack.actors.map((a) => prepActor(a, m, p, mod)).filter(Boolean)
      : pack.items.map((it) => prepItem(it, m, p, mod));
    if (!docs.length) continue;
    const dest = path.join(OUT[p.type], `${m.id || mod}.${p.name}`);
    fs.mkdirSync(dest, { recursive: true });
    const used = new Set();
    for (const d of docs) {
      let slug = slugify(d.name || d._id);
      if (used.has(slug)) slug = `${slug}-${d._id}`;
      used.add(slug);
      fs.writeFileSync(path.join(dest, `${slug}.json`), JSON.stringify(d));
    }
    console.log(`${String(docs.length).padStart(5)}  ${p.type.padEnd(5)} ${m.id || mod}.${p.name}`);
    total[p.type] += docs.length;
  }
}
console.log(`Exported ${total.Actor} module creatures -> ${OUT.Actor}`);
console.log(`Exported ${total.Item} module items -> ${OUT.Item}`);
