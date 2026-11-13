// The Foundry runner: a headless GM client that runs JavaScript inside a world and hands back the result.
//
// It joins as its own Gamemaster user (RUNNER_USER, "Wellspring"), with the password the launcher's
// single sign-on keeps in sso-secrets.json (set by tools/sso-password.mjs ... random, so nobody knows it).
// It connects only when asked and leaves again after IDLE_MINUTES, so it does not sit in the player list
// and does not count as "someone connected" when the launcher decides whether a world may be switched.
//
// It listens on 127.0.0.1 inside its container only; the way in is `docker exec runner node /app/run.mjs`
// (the foundry-run wrapper on the host), so reaching it takes SSH access to the Pi.
//
//   POST /run     { world, code, switch?, live? }  -> { ok, world, result | error, console }
//   GET  /status                                   -> { active, world, users, version, runner }
//
// `code` is the body of an async function run in the page: use `return` to hand a value back. It must
// be JSON-serialisable; Foundry documents are not, so return plain data (names, ids, counts).
//
// Environment:
//   FOUNDRY_URL    the Foundry server (default http://foundry:30000)
//   LAUNCHER_URL   the launcher, used to switch worlds (default http://launcher:8080)
//   WORLDS         slug=worldId pairs, as for the launcher
//   SSO_SECRETS    the launcher's secrets file (default /secrets/sso-secrets.json)
//   RUNNER_USER    the GM user to join as (default Wellspring)
//   IDLE_MINUTES   leave the world after this long without a run (default 10)
//   CHROMIUM       the browser binary (default /usr/bin/chromium)
import fs from "node:fs";
import http from "node:http";
import { chromium } from "playwright-core";

const FOUNDRY = (process.env.FOUNDRY_URL ?? "http://foundry:30000").replace(/\/+$/, "");
const LAUNCHER = (process.env.LAUNCHER_URL ?? "http://launcher:8080").replace(/\/+$/, "");
const SECRETS = process.env.SSO_SECRETS ?? "/secrets/sso-secrets.json";
const USER = process.env.RUNNER_USER ?? "Wellspring";
const IDLE_MS = Number(process.env.IDLE_MINUTES ?? 10) * 60_000;
const CHROMIUM = process.env.CHROMIUM ?? "/usr/bin/chromium";
const RUN_TIMEOUT = 5 * 60_000;
const WORLDS = new Map((process.env.WORLDS ?? "").split(",").filter(Boolean).map((p) => p.trim().split("=")));
const slugFor = (world) => [...WORLDS].find(([, id]) => id === world)?.[0] ?? world;

const log = (...a) => console.log(new Date().toISOString(), ...a);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let browser = null;
let session = null; // { context, page, world, console: [] }
let idleTimer = null;

async function status() {
    const res = await fetch(`${FOUNDRY}/api/status`, { signal: AbortSignal.timeout(5000) });
    return res.json();
}

async function leave() {
    clearTimeout(idleTimer);
    if (!session) return;
    const { context, world } = session;
    session = null;
    await context.close().catch(() => {});
    log(`left ${world}`);
}

/** Join `world` as RUNNER_USER: log in like the launcher's SSO does, hand the cookie to a fresh page. */
async function join(world) {
    await leave();
    const account = JSON.parse(fs.readFileSync(SECRETS, "utf8"))[world]?.[USER];
    if (!account) throw new Error(`no stored password for ${USER} in ${world} (tools/sso-password.mjs ... random)`);
    const res = await fetch(`${FOUNDRY}/join`, {
        method: "POST",
        headers: { origin: FOUNDRY, accept: "application/json" },
        body: new URLSearchParams({ action: "join", userId: account.id, password: account.password }),
        redirect: "manual",
        signal: AbortSignal.timeout(15_000),
    });
    const result = await res.json().catch(() => ({}));
    if (result.status !== "success") throw new Error(`Foundry refused ${USER} in ${world} (${res.status} ${result.message ?? ""})`.trim());
    const cookies = res.headers.getSetCookie().map((c) => {
        const [pair] = c.split(";");
        const i = pair.indexOf("=");
        return { name: pair.slice(0, i).trim(), value: pair.slice(i + 1).trim(), url: FOUNDRY };
    });

    browser ??= await chromium.launch({
        executablePath: CHROMIUM,
        args: ["--no-sandbox", "--disable-dev-shm-usage", "--mute-audio", "--disable-gpu"],
    });
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    await context.addCookies(cookies);
    // No canvas: documents, scenes and their tokens, walls and tiles all work without it, and a Pi
    // rendering a battlemap in software would take minutes.
    await context.addInitScript(() => localStorage.setItem("core.noCanvas", "true"));
    const page = await context.newPage();
    const s = { context, page, world, console: [] };
    page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") s.console.push(`${m.type()}: ${m.text()}`.slice(0, 500)); });
    page.on("pageerror", (e) => s.console.push(`pageerror: ${e.message}`.slice(0, 500)));
    await page.goto(`${FOUNDRY}/game`, { waitUntil: "domcontentloaded", timeout: 120_000 });
    await page.waitForFunction(() => window.game?.ready === true, null, { timeout: 180_000, polling: 500 });
    const who = await page.evaluate(() => ({ name: game.user?.name, gm: game.user?.isGM, world: game.world?.id }));
    if (who.name !== USER || !who.gm || who.world !== world) {
        await context.close();
        throw new Error(`joined as ${who.name} (GM ${who.gm}) in ${who.world}, expected ${USER} in ${world}`);
    }
    session = s;
    log(`joined ${world} as ${USER}`);
}

async function alive(world) {
    if (!session || session.world !== world || session.page.isClosed()) return false;
    return session.page.evaluate(() => window.game?.ready === true && game.socket?.connected === true).catch(() => false);
}

/** Ask the launcher to switch, then wait until the world is up. The launcher refuses while people are connected. */
async function switchTo(world) {
    await leave();
    const res = await fetch(`${LAUNCHER}/${encodeURIComponent(slugFor(world))}`, { redirect: "manual", signal: AbortSignal.timeout(15_000) });
    if (res.status === 409) throw new Error(`the launcher will not switch: people are connected to the running world`);
    if (res.status >= 400) throw new Error(`the launcher answered ${res.status} for ${world}`);
    for (const t0 = Date.now(); Date.now() - t0 < 180_000; await sleep(2000)) {
        const s = await status().catch(() => ({}));
        if (s.active && s.world === world) return log(`switched to ${world}`);
    }
    throw new Error(`${world} did not come up within 3 minutes`);
}

async function run({ world, code, switch: allowSwitch = false, live = false }) {
    if (!world || typeof code !== "string") throw new Error("need { world, code }");
    let s = await status();
    if (!s.active || s.world !== world) {
        if (!allowSwitch) throw new Error(`${world} is not running (${s.active ? `${s.world} is` : "no world is"}); pass --switch to have the launcher start it`);
        await switchTo(world);
        s = await status();
    }
    const others = (s.users ?? 0) - (session?.world === world ? 1 : 0);
    if (others > 0 && !live) throw new Error(`${others} ${others === 1 ? "person is" : "people are"} connected to ${world}; pass --live to run anyway`);
    if (!(await alive(world))) await join(world);

    clearTimeout(idleTimer);
    session.console.length = 0;
    const evaluation = session.page.evaluate(async (body) => {
        const AsyncFunction = (async () => {}).constructor;
        try {
            const value = await new AsyncFunction(body)();
            try { return { ok: true, result: JSON.parse(JSON.stringify(value ?? null)) }; }
            catch { return { ok: true, result: String(value) }; }
        } catch (e) {
            return { ok: false, error: e?.message ?? String(e), stack: String(e?.stack ?? "").split("\n").slice(0, 6).join("\n") };
        }
    }, code);
    const timeout = sleep(RUN_TIMEOUT).then(() => ({ ok: false, error: `no result after ${RUN_TIMEOUT / 60_000} minutes` }));
    const out = await Promise.race([evaluation, timeout]);
    idleTimer = setTimeout(() => leave().catch(() => {}), IDLE_MS);
    return { ...out, world, console: [...session.console] };
}

let queue = Promise.resolve(); // one run at a time
http.createServer((req, res) => {
    const reply = (code, body) => { res.writeHead(code, { "content-type": "application/json" }); res.end(JSON.stringify(body)); };
    if (req.method === "GET" && req.url === "/status") {
        return status()
            .then((s) => reply(200, { ...s, runner: session ? { world: session.world, user: USER } : null }))
            .catch((e) => reply(503, { error: `Foundry is not answering: ${e.message}` }));
    }
    if (req.method === "POST" && req.url === "/leave") return leave().then(() => reply(200, { ok: true }));
    if (req.method !== "POST" || req.url !== "/run") return reply(404, { error: "POST /run, POST /leave or GET /status" });
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", () => {
        queue = queue.then(async () => {
            try {
                const out = await run(JSON.parse(body));
                reply(out.ok ? 200 : 422, out);
            } catch (e) {
                log(`run failed: ${e.message}`);
                reply(409, { ok: false, error: e.message });
            }
        });
    });
}).listen(8090, "127.0.0.1", () => log(`runner on 127.0.0.1:8090 as ${USER}, Foundry ${FOUNDRY}`));

for (const sig of ["SIGTERM", "SIGINT"]) process.on(sig, async () => { await leave(); await browser?.close(); process.exit(0); });
