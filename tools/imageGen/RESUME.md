# RESUME: local FLUX art

**Status 2026-09-26: local rendering works again.** The GPU faults that stopped
the pipeline on 2026-09-13 came from the ROCm 7.x runtime bundled in the torch
wheel. The ComfyUI venv now runs `torch 2.9.1+rocm6.4`, and Kael Orvaine
rendered clean twice (395 s cold, 267 s warm). Details and the version table:
[README, *GPU faults*](README.md#gpu-faults-torch-is-pinned-to-rocm-64-fixed-2026-09-26).

The Veldtmark cast itself was finished in Midjourney on 2026-09-13; the batch
below is historical. The notes from that night are kept so the dead ends stay
dead.

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

### 2026-09-26 retest: still faults, and now we know where

Two OS updates later (bazzite 44.20260921, kernel 7.2.4), zero faults on the
fresh boot, six single-image Kael runs (spec copied to a scratch dir, so the
Midjourney art was never at risk). **All six faulted**, between 28 s and
2m44s. Ruled out today, each by a run that still faulted:

| run | change | died at |
|---|---|---|
| 1 | none (production flags) | 2m44s, `Requested to load Flux2` |
| 2 | `--disable-pinned-memory` | 2m24s, same step |
| 3 | `--disable-async-offload --disable-dynamic-vram` | 2m03s, sampling step 0/8 |
| 4 | `HIP_LAUNCH_BLOCKING=1 AMD_SERIALIZE_KERNEL=3` | 28 s, text-encoder load |
| 5 | same as 4, sampling `/proc/<pid>/maps` | 85 s |
| 6 | `HSA_ENABLE_SCRATCH_ASYNC_RECLAIM=0 HSA_NO_SCRATCH_RECLAIM=1` | 2m16s |

Also healthy in isolation: 20× 8192² fp16 matmul, a 16 GB allocation, and
`scaled_dot_product_attention` at FLUX.2 shapes (1×48×4608×128) on every
backend (flash / efficient / math) in bf16 and fp16. **Attention is fine.**

**What the fault actually is** (kernel log, identical on all six):
`[gfxhub] page fault … Faulty UTCL2 client ID: TCP`, `RW: 0x1` (a shader
*write*), `PERMISSION_FAULTS: 0x5`, `MAPPING_ERROR: 0x0`: the page is mapped
but the GPU is not allowed to write it. Run 5 caught the server's memory map
at the moment of the fault; the address is **byte 0 of a 2 MB buffer object
mapped from `/dev/dri/renderD128`**, sitting just below the ROCr VRAM
reservation. That is a runtime/driver-owned buffer, not model weights, not a
PyTorch allocation, not host RAM. The bug lives below ComfyUI and PyTorch: in
the ROCm 7.2 runtime bundled with torch 2.12.0+rocm7.2, or in the host
amdgpu/KFD driver. No ComfyUI flag will fix it.

The software inside the container is untouched since 2026-06-11 (ComfyUI
`fb991e2`, torch, comfy-aimdo 0.4.9); the host kernel is the part that moved.
The remaining real levers are outside this repo:
1. **Swap the torch wheel** to a different ROCm build (e.g. rocm7.1 / rocm6.4)
   in the container venv: tests the bundled runtime.
2. **Roll the host back** to a pre-September bazzite image (`rpm-ostree
   rebase` to a dated tag): tests the kernel driver. Both local deployments
   (20260916, 20260921) postdate the first fault.
3. **Report upstream** (ROCm/ROCm) with the table above.

**Resolved the same day by lever 1:** torch 2.12.0+rocm7.1 still faulted,
torch 2.9.1+rocm6.4 rendered clean twice. See the README section.

`npc_art.py` now reads `NPC_ART_EXTRA_ARGS` for one-off server flags, so
experiments no longer need edits to the launch list. Each crash writes a ~18 GB
core dump that systemd-coredump discards as `missing`; they do not pile up.

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
