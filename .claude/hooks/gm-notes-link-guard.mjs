// gm-notes-link-guard.mjs
// ---------------------------------------------------------------------------
// PostToolUse (Write|Edit) guard hook for the Tyrnarra project.
//
// The published worldbuilding site (/setting/) is player-facing, and the player
// campaign companion (/player-campaigns/) ships with all GM-tier content
// stripped. Neither may link into /gm-notes/ (the GM-only, sidebar-unlinked
// table layer). This hook fires when an .html/.js/.css file under
// published/setting/ or published/player-campaigns/ is written or edited and
// warns (non-blocking) if the file now contains an actual LINK to /gm-notes/.
//
// It distinguishes a link from a prose/comment mention: only a /gm-notes path
// sitting immediately behind a quote or url( opener trips it. Both nav files
// (site-nav.js, pc-nav.js) carry deliberate comments explaining that gm-notes
// is NOT linked here; those bare mentions must not fire.
//
// It ONLY warns. It never edits the file or strips the link; the fix stays with
// Claude. Cross-platform (Node.js): runs identically on Windows and Linux.
// ---------------------------------------------------------------------------

import { readFileSync, existsSync } from "node:fs";
import { basename } from "node:path";

// Hook payload arrives as JSON on stdin (fd 0).
let raw = "";
try {
  raw = readFileSync(0, "utf8");
} catch {
  process.exit(0);
}
if (!raw || !raw.trim()) process.exit(0);

let payload;
try {
  payload = JSON.parse(raw);
} catch {
  process.exit(0);
}

const path = payload && payload.tool_input && payload.tool_input.file_path;
if (!path || !String(path).trim()) process.exit(0);

// Normalise separators so the same match works for Windows and POSIX paths.
const p = String(path).replace(/\\/g, "/");

// Guard only the two published, player-facing trees. The GM layer itself
// (/published/gm-notes/) links to itself freely and is intentionally skipped.
const inSetting = /\/published\/setting\//.test(p);
const inPlayer = /\/published\/player-campaigns\//.test(p);
if (!inSetting && !inPlayer) process.exit(0);

// Only the text page assets that can carry a link are worth scanning.
if (!/\.(html|js|css)$/.test(p)) process.exit(0);

if (!existsSync(path)) process.exit(0);
let content = "";
try {
  content = readFileSync(path, "utf8");
} catch {
  process.exit(0);
}
if (!content || !content.trim()) process.exit(0);

// A real link to the GM layer puts the /gm-notes path right behind a quote or a
// url( opener: href="/gm-notes/...", src='/gm-notes/...', url(/gm-notes/...),
// "../gm-notes/...". A bare prose/comment mention (". The GM-only /gm-notes/
// tree") has a space, not a delimiter, in front of the path, so it is skipped.
if (!/["'(]\s*[.\/\\]*gm-notes/i.test(content)) process.exit(0);

const name = basename(path);
const tree = inSetting
  ? "the player-facing worldbuilding site (/setting/)"
  : "the player campaign companion (/player-campaigns/)";

const msg =
  `GM-NOTES LINK LEAK: '${name}' belongs to ${tree}, which must never link into ` +
  "/gm-notes/ (the GM-only, sidebar-unlinked table layer; player-facing pages ship " +
  "with all GM-tier content stripped). The file you just wrote contains a link or " +
  "path reference to /gm-notes/. Search the file for 'gm-notes', then either delete " +
  "that href/src/path or repoint it at a published /setting/ or /player-campaigns/ " +
  "target before committing. (This hook only warns; it never edits the file. A bare " +
  "prose mention of the path will not trip it, so this is an actual link.)";

process.stdout.write(
  JSON.stringify({
    systemMessage:
      `GM-notes link guard: '${name}' under ${tree} links into the GM-only ` +
      "/gm-notes/ layer. Player-facing pages must not. Remove or repoint the link " +
      "before committing.",
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: msg,
    },
  })
);
process.exit(0);
