#!/usr/bin/env python3
"""
foundry_run.py - run JavaScript inside a Foundry world through the runner on the Foundry server.

The runner (runner/ next to this file, deployed in the Pi's compose stack) is a headless GM client that
joins the running world as the GM user Wellspring, with a password only the launcher knows. This script
reaches it over ssh, so it works from any machine that can ssh to the server: no browser, no extension.

    foundry_run.py --campaign short-notice script.js         run a file (`return` hands back a value)
    foundry_run.py --world heavens-dragons -e 'return game.actors.size'
    foundry_run.py --campaign furrious-five --switch ...     let the launcher start that world first
                                                             (it refuses while people are connected)
    foundry_run.py ... --live                                run although players are connected
    foundry_run.py --status                                  which world runs, who is in, is Wellspring in
    foundry_run.py --leave                                   make Wellspring leave the world now
    foundry_run.py --campaign short-notice apply-spec <spec.json> [--dry]
                                                             apply a quest_journal.py --spec file: update
                                                             every page whose HTML differs, report missing ones;
                                                             --dry only lists what would change

The script is the body of an async function run in the page; return plain JSON-able data (names, ids,
counts), not Foundry documents. Output is the runner's JSON; the exit code is 1 when the script threw
or could not run. Wellspring leaves the world after ten idle minutes.
"""
import argparse
import json
import os
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from upload_foundry import CAMPAIGNS, foundry_remote  # noqa: E402

APPLY_SPEC = r"""
const spec = __SPEC__, dry = __DRY__;
const out = { dry, updated: {}, missing: {}, customLayoutChanged: {}, unchanged: 0 };
for (const sj of spec.journals) {
  const j = game.journal.getName(sj.name);
  if (!j) { out.missing[sj.name] = "(whole journal)"; continue; }
  const ups = [];
  for (const sp of sj.pages) {
    if (sp.type !== "text") continue;
    const p = j.pages.getName(sp.name);
    if (!p) { (out.missing[sj.name] ??= []).push(sp.name); continue; }
    // A page laid out by hand in Foundry (the Cast: images, player line, GM block) keeps the converter's
    // HTML in flags.world.originalHtml. Never overwrite it; report when its source changed.
    const orig = p.flags?.world?.originalHtml;
    if (orig !== undefined) {
      if (orig === sp.html) out.unchanged++;
      else (out.customLayoutChanged[sj.name] ??= []).push(sp.name);
      continue;
    }
    if (p.text.content === sp.html) { out.unchanged++; continue; }
    ups.push({ _id: p.id, "text.content": sp.html });
  }
  if (ups.length) {
    if (!dry) await j.updateEmbeddedDocuments("JournalEntryPage", ups);
    out.updated[sj.name] = ups.map((u) => j.pages.get(u._id).name);
  }
}
// what Foundry stored may differ from what was sent (it normalises some HTML); report it
out.stillDiffer = {};
if (!dry) for (const sj of spec.journals) {
  const j = game.journal.getName(sj.name);
  const d = j ? sj.pages.filter((sp) => { const p = sp.type === "text" && j.pages.getName(sp.name); return p && p.flags?.world?.originalHtml === undefined && p.text.content !== sp.html; }).map((sp) => sp.name) : [];
  if (d.length) out.stillDiffer[sj.name] = d;
}
return out;
"""


def world_for(args):
    if args.world:
        return args.world
    if args.campaign:
        campaigns = json.load(open(CAMPAIGNS, encoding="utf-8"))
        world = campaigns.get(args.campaign)
        if not world:
            sys.exit(f"Campaign {args.campaign!r} has no Foundry world in {CAMPAIGNS}")
        return world
    sys.exit("Give --world <id> or --campaign <slug>.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--world", help="Foundry world id.")
    ap.add_argument("--campaign", help="Repo campaign slug (campaigns.json gives the world).")
    ap.add_argument("--switch", action="store_true", help="Have the launcher start the world if another runs.")
    ap.add_argument("--live", action="store_true", help="Run although players are connected.")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--leave", action="store_true")
    ap.add_argument("--dry", action="store_true", help="apply-spec: list the changes, write nothing.")
    ap.add_argument("-e", dest="code", help="The script as a string.")
    ap.add_argument("rest", nargs="*", help="A script file, or: apply-spec <spec.json>.")
    args = ap.parse_args()

    host, root = foundry_remote()
    remote = f"{root}/tools/foundry-run"
    if args.status or args.leave:
        cmd = [remote, "--status" if args.status else "--leave"]
        code = ""
    else:
        if args.code is not None:
            code = args.code
        elif args.rest[:1] == ["apply-spec"]:
            if len(args.rest) != 2:
                sys.exit("usage: apply-spec <spec.json>")
            spec = json.load(open(args.rest[1], encoding="utf-8"))
            code = APPLY_SPEC.replace("__DRY__", "true" if args.dry else "false").replace("__SPEC__", json.dumps(spec, ensure_ascii=False))
        elif args.rest:
            code = open(args.rest[0], encoding="utf-8").read()
        else:
            code = sys.stdin.read()
        cmd = [remote, "--world", world_for(args)] + (["--switch"] if args.switch else []) + (["--live"] if args.live else [])

    res = subprocess.run(["ssh", "-o", "BatchMode=yes", host, " ".join(shlex.quote(c) for c in cmd)],
                         input=code, text=True, capture_output=True)
    sys.stdout.write(res.stdout)
    if res.returncode and not res.stdout:
        sys.stderr.write(res.stderr)
    sys.exit(res.returncode)


if __name__ == "__main__":
    main()
