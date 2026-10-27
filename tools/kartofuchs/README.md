# kartofuchs/

The bridge to [Kartofuchs](https://github.com/Kemenor/kartofuchs), the map editor that is replacing Wonderdraft. The editor and its tools live in their own repository; this folder only makes them reachable from a Tyrnarra session.

- `mcp-server.sh` starts the Kartofuchs MCP server (`mcp/server.ts` in the Kartofuchs checkout), registered as `kartofuchs` in the repo's `.mcp.json`. It finds the checkout through `$KARTOFUCHS`, else `~/Documents/fuchs/kartofuchs`, and needs Node 26.

The server talks to the running Kartofuchs app, never to the map files, so its tools see a map only while the app has it open (the main map is `~/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs`). `KARTOFUCHS_PORT` picks the app's port (default 7717). Its tools read, query and edit the open map, generate towns and terrain, place stamps and take screenshots; Kartofuchs' own `CLAUDE.md` and `mcp/` describe them.

Never serve one map on two machines at once: the map syncs between them, and both would save over it.

The `kartofuchs-map` skill (`.claude/skills/kartofuchs-map/`) is how a session opens and edits the Tyrnarra map through these tools.
