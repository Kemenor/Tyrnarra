#!/usr/bin/env node
/*
 * export_modules.mjs - dump the Actor packs of your installed Foundry modules
 * (Battlezoo, Jam & Jax, ...) to plain Foundry actor JSON so build_db.py can
 * ingest them like the official packs.
 *
 *   node export_modules.mjs            # FOUNDRY_DATA defaults to ~/foundry/data/Data
 *
 * Module packs are LevelDB: an actor lives at `!actors!<id>` and its embedded
 * items at `!actors.items!<actorId>.<itemId>`; the actor's `items` array holds
 * only ids. We re-inline the items so the JSON matches the official pack shape.
 * Each pack is copied to a temp dir first, so a running Foundry's LOCK never
 * blocks us and we never touch the live pack.
 *
 * Reads with the `classic-level` that ships inside the Foundry app (no npm
 * install). Output: _sources/modules/<module-id>.<pack-name>/<slug>.json,
 * wiped and rewritten each run. _sources/ is gitignored (paid content stays local).
 *
 * Env overrides: FOUNDRY_DATA (the Data dir), FOUNDRY_APP (the app dir).
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
const OUT = path.join(HERE, "_sources", "modules");

const require = createRequire(path.join(APP, "package.json"));
const { ClassicLevel } = require("classic-level");

const slugify = (s) =>
  s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase()
    .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "actor";

async function readPack(srcDir) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "foundry-pack-"));
  try {
    fs.cpSync(srcDir, tmp, { recursive: true });
    fs.rmSync(path.join(tmp, "LOCK"), { force: true });
    const db = new ClassicLevel(tmp, { valueEncoding: "json" });
    const actors = new Map(), items = new Map();
    for await (const [k, v] of db.iterator()) {
      if (k.startsWith("!actors!")) actors.set(k.slice(8), v);
      else if (k.startsWith("!actors.items!")) items.set(k.slice(14), v);
    }
    await db.close();
    for (const [id, a] of actors) {
      a.items = (a.items || []).map((i) =>
        typeof i === "string" ? items.get(`${id}.${i}`) : i).filter(Boolean);
    }
    return [...actors.values()];
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

fs.rmSync(OUT, { recursive: true, force: true });
const modDir = path.join(DATA, "modules");
let total = 0;
for (const mod of fs.readdirSync(modDir).sort()) {
  const manifest = path.join(modDir, mod, "module.json");
  if (!fs.existsSync(manifest)) continue;
  const m = JSON.parse(fs.readFileSync(manifest, "utf8"));
  for (const p of m.packs || []) {
    if (p.type !== "Actor") continue;
    // Manifests write pack paths as "packs/x", "/packs/x" or legacy "packs/x.db";
    // the LevelDB lives in the directory without the .db suffix.
    const src = path.join(modDir, mod, p.path.replace(/^\//, "").replace(/\.db$/, ""));
    if (!fs.existsSync(path.join(src, "CURRENT"))) {
      console.warn(`skip ${mod}/${p.name}: no LevelDB at ${src}`);
      continue;
    }
    // Drop blank build templates ("Alchemist Template lvl 1", "A Monk Template").
    const actors = (await readPack(src))
      .filter((a) => a.type === "npc" && !/\btemplate\b/i.test(a.name || ""));
    const dest = path.join(OUT, `${m.id || mod}.${p.name}`);
    fs.mkdirSync(dest, { recursive: true });
    const used = new Set();
    for (const a of actors) {
      // Module actors often leave publication.title blank; fall back to the
      // module's title so `source` reads "Battlezoo Bestiary ..." in results.
      const pub = ((a.system ??= {}).details ??= {}).publication ??= {};
      if (!pub.title) pub.title = m.title || mod;
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
      let slug = slugify(a.name || a._id);
      if (used.has(slug)) slug = `${slug}-${a._id}`;
      used.add(slug);
      fs.writeFileSync(path.join(dest, `${slug}.json`), JSON.stringify(a));
    }
    console.log(`${String(actors.length).padStart(4)}  ${m.id || mod}.${p.name}`);
    total += actors.length;
  }
}
console.log(`Exported ${total} module creatures -> ${OUT}`);
