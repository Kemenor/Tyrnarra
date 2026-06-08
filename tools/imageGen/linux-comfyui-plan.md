# Linux migration + local ComfyUI plan (handoff)

Written 2026-06-08, mid-migration. Purpose: this machine is moving from Windows to
Linux (Bazzite), and the Windows install + this session's chat will be wiped, so the
plan lives here in git to survive the switch. A fresh session can resume from this
file with no prior context.

This is **dev-environment / tooling** notes, not worldbuilding canon. It does not
touch `lore/` or `published/`.

## Why

Add a **local, free** image-generation tier on the machine's own GPU, alongside the
existing paid cloud tiers in this folder (fal.ai FLUX.2 via `gen_portraits.py` /
`gen_npc_set.py`, and Midjourney via `mj_prompts.py`). Local gen is for the
iterate-a-lot, no-per-image-cost work: LoRA training on approved Tyrnarra art, batch
portrait variations, inpainting on map tiles. The cloud tiers stay; ComfyUI is the
new third option, not a replacement.

The trigger was wanting ComfyUI on the GPU, which led to deciding to move the whole
daily driver to Linux (the machine is gaming + YouTube + Discord + Claude Code for
this project, with no kernel-anti-cheat games, so Linux is low-risk here).

## Hardware (all confirmed Linux-friendly, in-kernel, no proprietary drivers)

- **GPU:** AMD Radeon RX 7900 XTX, 24 GB (RDNA3 / gfx1100). Best-case Linux GPU:
  open-source Mesa driver, in-kernel. 24 GB VRAM handles SDXL, Flux, and local video
  models. ROCm-on-Linux is the *best-supported* path for this card (better than any
  Windows option: ZLUDA, ROCm-on-Windows, WSL2, DirectML).
- **CPU:** AMD Ryzen 9 5900X (Zen 3, 12C/24T). Fully in-kernel, mature.
- **RAM:** 64 GB. Generous headroom for model caching + distrobox containers.
- **10 GbE NIC:** TP-Link TX401 = Aquantia/Marvell **AQC107** chipset, driver
  `atlantic`, in mainline kernel since 4.16. Works out of the box on Bazzite's 6.x
  kernel. **Ignore** the TP-Link Linux FAQ `.rpm`/`.deb` driver packages: they are
  for old enterprise kernels and would conflict with the in-kernel module (and would
  not take on an immutable distro anyway).

Verdict: every component is in-kernel. Nothing in this box fights Linux.

## Decisions made

- **Distro:** Bazzite (Fedora-based, immutable, gaming-tuned). Chosen over Pop!_OS
  because Pop is on Ubuntu 22.04 LTS with older Mesa that does not backport well to
  RX 7000-series; Bazzite's rapid Mesa updates matter for this exact GPU. Image
  selected on bazzite.gg: **Desktop / AMD (RX 4xx+ | AI) / KDE / traditional desktop
  (not Gaming Mode)**. The "AI" variant bundles ROCm/compute bits.
- **Dual-boot via separate physical drives** (cleanest possible: no partition
  resize, independent bootloaders). After a few weeks, if Windows goes unused, wipe
  the primary M.2 (probably reinstall fresh rather than migrate).

## Drive layout

- **232 GB M.2** -> Bazzite OS + apps (plenty; keep games/models off it).
- **4 TB drive** -> Linux Steam library. **Format ext4 or btrfs**, NOT NTFS:
  Proton hits permission/case-sensitivity bugs on NTFS. (Was NTFS Steam games;
  re-download is trivial on the 10 GbE line.)
- **1 TB SSD** -> ComfyUI models + overflow. (Was empty.)
- **Primary M.2** -> Windows for now; wipe later.

## Install sequence (the checklist)

1. **In Windows first:** disable **BitLocker** (or save the recovery key) and
   disable **Fast Startup**. Order matters: turning off Secure Boot later triggers a
   BitLocker recovery-key prompt, so clear BitLocker before touching firmware.
   *(In progress as of this writing: stick being flashed, drives decrypting. Let
   BitLocker decryption finish fully before rebooting.)*
2. Flash the Bazzite ISO to USB (Fedora Media Writer or Ventoy).
3. Optionally test-boot the stick (one-time boot menu, ASUS often **F8**) to confirm
   it reaches the Bazzite live desktop *before* changing any BIOS settings.
4. **In BIOS/UEFI, one session:** disable **Secure Boot** (simplest path; Bazzite
   can run with it on but needs MOK enrollment) and **disable the Windows M.2**
   (insurance against installing to the wrong disk; keeps bootloaders separate).
5. Boot the stick -> run installer -> target the **232 GB** drive. Its bootloader
   lands on that drive, self-contained.
6. After install: back into BIOS, **re-enable the Windows M.2**. Switch OSes via the
   firmware boot menu. Because the bootloaders are isolated, wiping Windows later
   cannot orphan Bazzite's boot.
7. Format the 4 TB (ext4/btrfs) as the Steam library; re-download games. Enable
   **Proton Experimental** per-game for the fussy AAA titles.

### Game compatibility notes (ProtonDB, checked 2026-06)

- Library is almost all single-player / co-op indies + roguelikes + deckbuilders =
  Proton-friendly. No kernel-anti-cheat competitive games.
- **Monster Hunter Wilds** (app 2246340): runs with **Proton Experimental (bleeding
  edge)**. The 1-hour file-validation / 30 fps horror stories are Steam-Deck-specific
  and do NOT apply to a 7900 XTX desktop.
- **Crimson Desert** (app 3321460): playable on Proton Experimental; ships
  **Denuvo** (changing Proton version counts against a 5-installs/day limit, so do
  not swap Proton casually); **AMD: disable ray tracing** in settings before launch;
  runs ~20-30 fps below Windows.

## Post-install: ComfyUI + ROCm on the 7900 XTX (the payoff, TODO)

Bazzite is **immutable** (read-only base OS), so do NOT install Python/ROCm into the
base system. Put the whole stack in a **distrobox** container (Fedora or Ubuntu box),
which also keeps the ROCm/ComfyUI mess sandboxed away from the gaming OS. CLI tools
like Node for Claude Code can go via Bazzite's bundled **Homebrew** or in distrobox.

When resuming this step, the rough shape (verify current specifics with a web search
first; ROCm/ComfyUI move fast):
1. `distrobox create` a container (Fedora 40+ or Ubuntu), enter it.
2. Install ROCm runtime for **gfx1100** (the 7900 XTX target). May need
   `HSA_OVERRIDE_GFX_VERSION=11.0.0` if the runtime is fussy about the exact arch.
3. Install ROCm-build PyTorch (the ROCm wheel index), confirm `torch.cuda.is_available()`.
4. Clone ComfyUI, `pip install -r requirements.txt`, launch, point it at the model
   dir on the **1 TB** drive.
5. If native ROCm fights, fall back to a ZLUDA/`comfyui-zluda` approach (less likely
   to be needed on Linux than it was on Windows).

How it fits the existing folder: this stays a sibling option to the fal.ai scripts
and `mj_prompts.py`. Same `*.set.json` / `*.portraits.json` specs describe a
character; ComfyUI just becomes the local renderer for high-iteration work (LoRA on
approved art, batch variants, map inpainting). Nothing about the current cloud
pipeline changes.

## Open decisions (none blocking)

- Whether to LUKS-encrypt the Bazzite install during setup (Linux's own full-disk
  encryption; you are dropping *BitLocker*, not encryption forever).
- KDE vs trying GNOME later (KDE chosen for Windows familiarity).
- Eventually: wipe primary M.2 and reinstall vs migrate Bazzite onto it.
