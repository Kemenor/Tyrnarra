@echo off
REM ─────────────────────────────────────────────────────────────
REM serve.bat — local dev server for Tyrnarra (live-reload)
REM Double-click to launch, or run from a terminal.
REM
REM Uses live-server via npx: auto-opens the browser and refreshes
REM it whenever an HTML/CSS/JS file in the repo changes.
REM Requires Node.js (https://nodejs.org).
REM
REM On first run, npx downloads live-server (~25MB, one time).
REM Subsequent runs start immediately.
REM
REM Press Ctrl+C to stop.
REM ─────────────────────────────────────────────────────────────

cd /d "%~dp0"

echo.
echo  ╭─────────────────────────────────────────────╮
echo  │   TYRNARRA  ·  LOCAL DEV SERVER             │
echo  │   live-reload enabled                       │
echo  │   http://localhost:8000                     │
echo  │   Ctrl+C to stop                            │
echo  ╰─────────────────────────────────────────────╯
echo.

REM --yes:    skip the "OK to install?" prompt on first run
REM --port:   match the GitHub Pages local convention
REM --ignore: skip lore/ markdown and git internals to avoid
REM           reloads on notes/commits
npx --yes live-server --port=8000 --ignore="lore/**,.git/**,outputs/**"
