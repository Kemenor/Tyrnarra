// gm-vetted-check.mjs
// PostToolUse hook (Write|Edit) — matches the registration in .claude/settings.json.
// When the edited file is an .html page that still carries a GM-Vetted badge,
// remind Claude to judge whether the edit just made was more than minor and,
// if so, strip the badge. Claude makes the minor-vs-major call; this hook only
// flags, never edits. A trivial fix keeps the badge; a real change drops it.
//
// Cross-platform (Node.js): runs identically on Windows and Linux/Bazzite.

import { readFileSync, existsSync } from "node:fs";
import { basename } from "node:path";

let raw = "";
try {
  raw = readFileSync(0, "utf8");
} catch {
  process.exit(0);
}
if (!raw) process.exit(0);

let payload;
try {
  payload = JSON.parse(raw);
} catch {
  process.exit(0);
}

const fp = payload && payload.tool_input && payload.tool_input.file_path;
if (!fp) process.exit(0);
if (!/\.html$/.test(fp)) process.exit(0);
if (!existsSync(fp)) process.exit(0);

let content = "";
try {
  content = readFileSync(fp, "utf8");
} catch {
  process.exit(0);
}
if (!content || !content.includes("gm-vetted")) process.exit(0);

const name = basename(fp);
const msg =
  `GM-VETTED PAGE: '${name}' carries a GM-Vetted badge (a page the GM personally ` +
  "read and corrected). You just edited it. Judge whether that edit was MORE THAN " +
  "MINOR (a real prose, structural, or canon change) or trivial (typo, single word, " +
  "whitespace, one punctuation swap). If MORE THAN MINOR, strip the badge so the page " +
  "is no longer marked vetted: delete the gm-vetted HTML comment line and the " +
  "gm-vetted div. If trivial, leave the badge in place. Do not add or re-add a badge " +
  "yourself; only the GM vets pages.";

process.stdout.write(
  JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: msg,
    },
  })
);
process.exit(0);
