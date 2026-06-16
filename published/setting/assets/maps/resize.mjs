// resize.mjs - Resize the Talan maps for web display. Cross-platform (Node).
//
// Generates two reduced variants of each map in /assets/maps/:
//   display/  (2400px max width, quality 85) - for inline page display
//   thumbs/   (800px max width, quality 80)  - for previews / index thumbnails
//
// The originals stay untouched. Requires ImageMagick's `magick` CLI on PATH
// (cross-platform: dnf/brew install imagemagick on Linux; the Windows Binary
// Release installer, with "Add to system path" ticked).
//
// Run, from this directory:        node resize.mjs
// Or from the repo root:           node published/setting/assets/maps/resize.mjs

import { existsSync, mkdirSync, statSync } from "node:fs";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join, parse } from "node:path";

const mapsDir = dirname(fileURLToPath(import.meta.url));
const displayDir = join(mapsDir, "display");
const thumbsDir = join(mapsDir, "thumbs");

// magick is an .exe on Windows and a plain binary on Linux, so spawn finds it
// without a shell. (No shell: avoids the '>' in "-resize 2400x>" being read as
// a redirection.)
const probe = spawnSync("magick", ["-version"], { stdio: "ignore" });
if (probe.error || probe.status !== 0) {
  console.error("ERROR: ImageMagick is required but `magick` was not found on PATH.");
  console.error("Install from: https://imagemagick.org/script/download.php");
  console.error("  Linux/Bazzite:  sudo dnf install ImageMagick   (or: brew install imagemagick)");
  console.error("  Windows:        the 'Windows Binary Release' installer; tick 'Add to system path'.");
  process.exit(1);
}

mkdirSync(displayDir, { recursive: true });
mkdirSync(thumbsDir, { recursive: true });

const maps = ["terrain.webp", "kingdoms.webp", "domains.webp"];
const MB = 1024 * 1024;
const KB = 1024;
let totalOrig = 0;
let totalDisplay = 0;
let totalThumb = 0;

console.log("Resizing Talan maps...\n");

for (const map of maps) {
  const inputPath = join(mapsDir, map);
  if (!existsSync(inputPath)) {
    console.log(`  SKIP ${map} (not found)`);
    continue;
  }

  const base = parse(map).name;
  const displayOut = join(displayDir, `${base}.webp`);
  const thumbOut = join(thumbsDir, `${base}.webp`);

  const origSize = statSync(inputPath).size;
  totalOrig += origSize;
  console.log(`  ${map} (${(origSize / MB).toFixed(1)} MB)`);

  // Display version: 2400px max width, quality 85
  let r = spawnSync(
    "magick",
    [inputPath, "-resize", "2400x>", "-quality", "85", "-define", "webp:method=6", displayOut],
    { stdio: "inherit" }
  );
  if (r.status !== 0) {
    console.error(`magick failed on ${map} (display variant)`);
    process.exit(1);
  }
  const displaySize = statSync(displayOut).size;
  totalDisplay += displaySize;
  console.log(`    -> display/${base}.webp (${(displaySize / MB).toFixed(2)} MB)`);

  // Thumb version: 800px max width, quality 80
  r = spawnSync(
    "magick",
    [inputPath, "-resize", "800x>", "-quality", "80", "-define", "webp:method=6", thumbOut],
    { stdio: "inherit" }
  );
  if (r.status !== 0) {
    console.error(`magick failed on ${map} (thumb variant)`);
    process.exit(1);
  }
  const thumbSize = statSync(thumbOut).size;
  totalThumb += thumbSize;
  console.log(`    -> thumbs/${base}.webp (${Math.round(thumbSize / KB)} KB)`);
}

console.log("\nDone. Totals:");
console.log(`  Originals: ${(totalOrig / MB).toFixed(1)} MB`);
console.log(`  Display:   ${(totalDisplay / MB).toFixed(1)} MB`);
console.log(`  Thumbs:    ${(totalThumb / MB).toFixed(2)} MB`);
