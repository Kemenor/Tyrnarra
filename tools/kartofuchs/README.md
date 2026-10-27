# kartofuchs/

The bridge to [Kartofuchs](https://github.com/Kemenor/kartofuchs), the map editor that is replacing Wonderdraft. The editor and its tools live in their own repository; this folder only makes them reachable from a Tyrnarra session.

- `mcp-server.sh` starts the Kartofuchs MCP server (`mcp/server.ts` in the Kartofuchs checkout), registered as `kartofuchs` in the repo's `.mcp.json`. It finds the checkout through `$KARTOFUCHS`, else `~/Documents/fuchs/kartofuchs`, and needs Node 26.

The server talks to a running Kartofuchs, never to the map files, and starts one in the background when none runs, so `maps` with `open: <map folder>` works from nothing (the main map is `~/Sync/Tyrnarra/Kartofuchs/Main.kartofuchs`). `KARTOFUCHS_PORT` picks the port (default 7717). Its tools read, query and edit the open map, generate towns and terrain, place stamps and take screenshots; Kartofuchs' own `CLAUDE.md` and `mcp/` describe them.

One machine at a time: an open map keeps a `lock.json` in its folder naming the host, which syncs to the other PC and makes Kartofuchs there refuse the map until the lock is released or goes stale (3 minutes).

The `kartofuchs-map` skill (`.claude/skills/kartofuchs-map/`) is how a session opens and edits the Tyrnarra map through these tools.
