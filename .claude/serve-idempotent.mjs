// serve-idempotent.mjs
// Cross-platform local dev server launcher for the Tyrnarra site.
// If port 8008 is already serving, reuse it and idle; otherwise start
// live-server on published/. Runs identically on Windows and Linux/Bazzite.

import { spawn } from "node:child_process";
import http from "node:http";

const port = 8008;

function isServing() {
  return new Promise((resolve) => {
    const req = http.get(
      { host: "127.0.0.1", port, path: "/", timeout: 1000 },
      (res) => {
        res.resume();
        resolve(true);
      }
    );
    req.on("error", () => resolve(false));
    req.on("timeout", () => {
      req.destroy();
      resolve(false);
    });
  });
}

if (await isServing()) {
  console.log(`[serve] Port ${port} already serving; reusing existing server.`);
  // Idle forever so a launcher that expects a long-lived process stays happy.
  setInterval(() => {}, 1 << 30);
} else {
  console.log(`[serve] Starting live-server on port ${port}.`);
  // shell:true resolves npx vs npx.cmd correctly across Windows and POSIX.
  const child = spawn(
    "npx",
    ["--yes", "live-server", "published", `--port=${port}`],
    { stdio: "inherit", shell: true }
  );
  child.on("exit", (code) => process.exit(code ?? 0));
}
