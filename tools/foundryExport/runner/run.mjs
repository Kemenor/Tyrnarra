// Client for the runner, used inside its container: `docker exec -i runner node /app/run.mjs ...`.
//
//   run.mjs --world <id> [--switch] [--live] < script.js     run the script, print the JSON result
//   run.mjs --status                                         what runs, who is connected, is the runner in
//   run.mjs --leave                                          make the runner leave the world now
//
// Exit code 0 when the script ran and returned, 1 when it threw or could not run.
const args = process.argv.slice(2);
const flag = (name) => args.includes(`--${name}`);
const value = (name) => { const i = args.indexOf(`--${name}`); return i >= 0 ? args[i + 1] : undefined; };
const URL_ = "http://127.0.0.1:8090";

async function main() {
    if (flag("status")) return (await fetch(`${URL_}/status`)).json();
    if (flag("leave")) return (await fetch(`${URL_}/leave`, { method: "POST" })).json();
    const world = value("world");
    if (!world) throw new Error("usage: run.mjs --world <id> [--switch] [--live] < script.js | --status | --leave");
    let code = "";
    for await (const chunk of process.stdin) code += chunk;
    const res = await fetch(`${URL_}/run`, {
        method: "POST",
        body: JSON.stringify({ world, code, switch: flag("switch"), live: flag("live") }),
    });
    return res.json();
}

main()
    .then((out) => { console.log(JSON.stringify(out, null, 2)); process.exit(out?.ok === false || out?.error ? 1 : 0); })
    .catch((e) => { console.log(JSON.stringify({ ok: false, error: e.message }, null, 2)); process.exit(1); });
