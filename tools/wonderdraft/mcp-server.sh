#!/bin/bash
# Start the Wonderdraft MCP server (registered in the repo's .mcp.json).
# Creates the gitignored virtualenv with the `mcp` package on first run.
# stdout is the MCP protocol channel, so setup output goes to stderr.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -x "$DIR/.venv/bin/python" ] || ! "$DIR/.venv/bin/python" -c "import mcp.server.mcpserver, PIL" 2>/dev/null; then
    echo "wonderdraft MCP: setting up $DIR/.venv (mcp, pillow)..." >&2
    python3 -m venv "$DIR/.venv" >&2
    "$DIR/.venv/bin/pip" install -q --disable-pip-version-check "mcp>=2.2,<3" pillow >&2
fi
exec "$DIR/.venv/bin/python" "$DIR/mcp_server.py"
