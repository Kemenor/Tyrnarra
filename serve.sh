#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# serve.sh — local dev server for Tyrnarra (live-reload)
# macOS / Linux / WSL.
#
# Uses live-server via npx: auto-opens the browser and refreshes
# it whenever an HTML/CSS/JS file in the repo changes.
# Requires Node.js (https://nodejs.org).
#
# On first run, npx downloads live-server (~25MB, one time).
# Subsequent runs start immediately.
#
# Press Ctrl+C to stop.
# ─────────────────────────────────────────────────────────────

set -e
cd "$(dirname "$0")"

cat <<'EOF'

 ╭─────────────────────────────────────────────╮
 │   TYRNARRA  ·  LOCAL DEV SERVER             │
 │   live-reload enabled                       │
 │   http://localhost:8000                     │
 │   Ctrl+C to stop                            │
 ╰─────────────────────────────────────────────╯

EOF

# --yes:    skip the "OK to install?" prompt on first run
# --port:   match the GitHub Pages local convention
# --ignore: skip lore/ markdown and git internals to avoid
#           reloads on notes/commits
exec npx --yes live-server --port=8000 --ignore="lore/**,.git/**,outputs/**"
