# RESUME: the Veldtmark cast art (paused 2026-09-13, ~23:40)

Paused because the GPU started throwing `Memory access fault by GPU node-1`
faults, not because anything is undecided. **Every creative call is locked and
approved** — the remaining work is pressing go on 10 renders.

**First thing to try: reboot, then run the batch below.** The faults grew more
frequent over the evening (a shot type that rendered fine at 22:47 was faulting
by 23:34), which is consistent with the amdgpu driver being left dirty by
repeated page faults and hard kills. A clean boot is the cheapest test.

---

## What is done

| NPC | full | portrait | scene |
|---|---|---|---|
| Caevan Veldtmark | ✅ | ⚠️ **redo** | ✅ conservatory |
| Aldous | ✅ | ✅ | ❌ door |
| Harlen Doss | ❌ | ❌ | ❌ counter |
| Sera Vance | ❌ | ❌ | ❌ cell |
| Professor Odo Mast | ❌ | ❌ | ❌ cell |

**10 shots outstanding**, plus Veldtmark's portrait which exists but is wrong.

All five `*.set.json` specs are final, approved, and carry their render seeds.
The approved variation for each of the four is `variations/<slug>-v1.png`, so
every command below uses `--draft 1`. Veldtmark's anchor is `--draft 4`.

**Veldtmark's portrait must be re-rolled.** The committed one was rendered in
the old `mode: "text"` and is a different man's face. His spec is now `ref`, so
it just needs the re-run below. It is deliberately **not committed** — the repo
has a gap rather than a wrong face.

---

## The commands

One driver at a time. **Never run two**; the machine has no headroom for it.

```bash
cd tools/imageGen
P=../../published/gm-notes/furrious-five/quest-veldtmark/art

# Veldtmark's portrait, in ref mode this time (fixes the mismatched face)
python3 npc_art.py set --spec $P/caevan-veldtmark.set.json --draft 4 --only portrait

# the rest, one shot per pass
for n in aldous harlen-doss sera-vance odo-mast; do
  for shot in full portrait scene; do
    python3 npc_art.py set --spec $P/$n.set.json --draft 1 --only $shot
  done
done
```

**One shot per pass is required, not stylistic.** A chained 3-shot `set` holds
all three latents in one prompt and hits ~52 GB RSS and swap thrash; single
shots sit at ~2.5 GB. `--only <shot>` uploads the saved anchor image as the
reference instead of chaining a live latent, so identity still holds. Completed
shots are skipped automatically (no `--force`), so the loop is safe to re-run.

Expect **~220 s per shot**. Watch `tools/imageGen/comfy-server.log` — that is
where a crash says why.

---

## If it still faults

The failure looks like this, and it is **not** an out-of-memory:

```
Requested to load Flux2          (or AutoencoderKL, or mid-render)
Memory access fault by GPU node-1 (Agent handle: 0x...) on address 0x...
Reason: Page not present or supervisor privilege.
Fatal Python error: Aborted
```

It struck at three different points with VRAM nearly empty and the junction
temperature at 60 °C, so **no ComfyUI flag reaches it.** Already ruled out:

- **`--reserve-vram`** — 1.0 starves KWin (amdgpu "Failed to pin framebuffer
  with error -12", desktop resets); 3.0 makes the Turbo LoRA OOM applying to
  the unet. Settled at **2.0**, which is correct and not the cause.
- **`--cpu-vae`** — tried; the fault simply moved elsewhere. Harmless, kept.
- **`--cache-none`** — unrelated to the faults, but **keep it always**: it is
  the fix for a +14.7 GB-per-pass memory leak (see README).
- **The fp8 text encoder** — not the cause; fp4_mixed was downloaded chasing
  it and is unnecessary.

**Then try `fal_art.py`** — the hosted sibling added by a parallel session the
same night (Seedream 4.5). The specs are format-agnostic and should feed it
directly. That sidesteps the GPU entirely.

If a fresh boot *and* a fresh ComfyUI still fault, it is a genuine ROCm bug
worth reporting upstream rather than tuning around.

---

## Locked creative decisions — do not re-litigate

- **Aldous** is the "pale and sickly" pass: adjectives only. Saying *bone* as a
  noun produced a floating skeleton; the spec now carries explicit living-flesh
  anchors. His hovering lives in the page prose, **not** in the art.
- **Doss** wears the Emarrean court fashion he saw exactly once — wine brocade,
  gold thread, rose silk waistcoat — and his face is *composed, masking worry*,
  not frightened. His Clothing & Dress block on the quest page matches.
- **Veldtmark** is variation 4. **Odo Mast** and **Sera Vance** were approved
  first time.
- **Portraits stay on `mode: "ref"`.** `"text"` renders with no reference to the
  anchor and returns a different person.
- **One variation, then change the prompt** — never reroll the same prompt.
  FLUX barely moves between seeds; if a shot is wrong, the spec is wrong.

---

## Housekeeping

`variations/` holds the approved picks (`-v1`) plus comparison keepers
(`aldous-A-statuesque`, `harlen-doss-A-plain`, `harlen-doss-B-scared`). They
are uncommitted by design. Delete them once the sets are complete.

The quest itself — [`quest-veldtmark.html`](../../published/gm-notes/furrious-five/quest-veldtmark/quest-veldtmark.html)
— is **finished and pushed**: three clickable maps, the drift-reskinned
bestiary, encounters re-tiered for five level-7 PCs, the escalating finale, the
half-share loot, and the cast's ancestries and physical blocks. **The art is
polish; the session does not need it.**
