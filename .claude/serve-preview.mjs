// serve-preview.mjs
// Launcher for the Claude preview MCP only. Binds live-server to the port the
// preview tool assigns via $PORT (so launch.json "autoPort" works), falling back
// to 8008. This is a throwaway verification instance the MCP owns and tears down
// with the session; the user's own persistent server stays serve.bat / serve.sh.
// Cross-platform (Windows + Linux): shell:true resolves npx vs npx.cmd.
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const port = process.env.PORT || 8008;
const root = join(dirname(fileURLToPath(import.meta.url)), "..");

const child = spawn(
  "npx",
  ["--yes", "live-server", join(root, "published"), `--port=${port}`],
  { cwd: root, stdio: "inherit", shell: true }
);
child.on("exit", (code) => process.exit(code ?? 0));
