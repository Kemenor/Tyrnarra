// git-commit-reminder.mjs
// ---------------------------------------------------------------------------
// PostToolUse (Write|Edit) reminder hook for the Tyrnarra project.
//
// When a file under lore/ or any .html page is edited, this injects a
// NON-BLOCKING reminder into the model's context that completed lore-writes
// and HTML publishes should be committed (with a descriptive message) and
// pushed, per CLAUDE.md's "commit + push per completed phase" workflow.
//
// It ONLY reminds. It never runs `git add`/`commit`/`push` itself; the commit
// decision, the message, and the push stay with Claude (and respect the
// surface-before-publish pause: no committing mid-phase or un-reviewed drafts).
//
// Cross-platform (Node.js): runs identically on Windows and Linux/Bazzite.
// ---------------------------------------------------------------------------

import { readFileSync } from "node:fs";

// The hook payload arrives as JSON on stdin (fd 0). Reading fd 0 synchronously
// works on both Windows and POSIX. Any failure is treated as "nothing to do".
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

const isLore = /\/lore\//.test(p);
const isHtml = /\.html$/.test(p);
if (!isLore && !isHtml) process.exit(0);

const kind = isLore ? "lore file" : "HTML page";

const msg =
  `Tyrnarra workflow reminder: you edited a ${kind}. Per CLAUDE.md, once this ` +
  "lore-write or HTML-publish phase is complete and surfaced, commit it with a " +
  "descriptive message and push. Do not commit mid-phase or un-reviewed drafts. " +
  "(This hook only reminds; it never runs git.)";

process.stdout.write(
  JSON.stringify({
    hookSpecificOutput: {
      hookEventName: "PostToolUse",
      additionalContext: msg,
    },
  })
);
process.exit(0);
