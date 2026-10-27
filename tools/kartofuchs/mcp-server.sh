#!/bin/bash
# Start the Kartofuchs MCP server (registered in the repo's .mcp.json) from the Kartofuchs checkout:
# $KARTOFUCHS, else ~/Documents/fuchs/kartofuchs. It talks to the running Kartofuchs app (port
# KARTOFUCHS_PORT, default 7717), so its tools see a map only while the app has it open.
# stdout is the MCP protocol channel, so messages go to stderr.
set -e
KF="${KARTOFUCHS:-$HOME/Documents/fuchs/kartofuchs}"
if [ ! -f "$KF/mcp/server.ts" ]; then
    echo "kartofuchs MCP: no Kartofuchs checkout at $KF (clone Kemenor/kartofuchs there, or set KARTOFUCHS)" >&2
    exit 1
fi
# The server's TypeScript runs on Node 26's type stripping; brew's node may be missing from a bare PATH.
command -v node >/dev/null || PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"
cd "$KF"
exec node mcp/server.ts
