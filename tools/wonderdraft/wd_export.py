"""Export map views to images by driving Wonderdraft's own export (it has no command line).

For each view map ("<stem> - Terrain.wonderdraft_map" etc.): launch Wonderdraft with
it (on the NVIDIA GPU when there is one, so the 8192px textures sit in video memory
instead of the integrated GPU's page pool, which does not give system RAM back), wait
a fixed LOAD_WAIT seconds after its window appears (Main loads in ~10 s; Wonderdraft
keeps redrawing while idle, so CPU use can't tell "loaded" apart), then send Ctrl+E, Enter (Export Options: PNG), the file name,
Enter (save dialog). Wait for the PNG to finish, close Wonderdraft, convert the PNG
to WebP at Wonderdraft's quality 92 and delete the PNG before Proton Drive syncs it.

xdotool types as if the keyboard were US while KWin applies the user's German layout,
so "-" arrives as "ß" (and y/z swap). The file name is therefore typed as TYPED_NAME,
which uses only keys that are the same on both layouts, and renamed afterwards.

Keystrokes go to whatever window has focus, so before every one the Wonderdraft
window must be the active window; if it isn't (the user clicked elsewhere), focus is
requested once and otherwise the run stops instead of typing into another window.
Needs xdotool (Wonderdraft runs under XWayland) and a free desktop for a few minutes.
"""
import os
import signal
import subprocess
import sys
import time

WD_DIR = os.path.expanduser("~/.local/opt/Wonderdraft")
WD_BIN = os.path.join(WD_DIR, "Wonderdraft.x86_64")
WEBP_QUALITY = 92
LOAD_WAIT = 15
TYPED_NAME = "wdexport"  # layout-safe: letters without y/z only


class ExportError(RuntimeError):
    pass


def _env():
    env = dict(os.environ, DISPLAY=os.environ.get("DISPLAY", ":0"))
    try:
        has_nvidia = subprocess.run(["nvidia-smi", "-L"], capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        has_nvidia = False
    if has_nvidia:
        env.update(__NV_PRIME_RENDER_OFFLOAD="1", __GLX_VENDOR_LIBRARY_NAME="nvidia",
                   __VK_LAYER_NV_optimus="NVIDIA_only")
    return env, has_nvidia


def _xdo(env, *args):
    r = subprocess.run(["xdotool"] + list(args), capture_output=True, text=True, env=env, timeout=15)
    return r.stdout.strip()


def _wonderdraft_running():
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                with open("/proc/%s/cmdline" % d, "rb") as f:
                    if os.path.basename(f.read().split(b"\0", 1)[0]) == b"Wonderdraft.x86_64":
                        return True
            except OSError:
                pass
    return False


def _countdown(seconds, what, proc):
    """Visible wait, so a pause never looks like a hang; stops early if Wonderdraft exits."""
    for left in range(int(seconds), 0, -5):
        if proc.poll() is not None:
            raise ExportError("Wonderdraft exited while %s" % what)
        print("\r    %s... %2ds " % (what, left), end="", flush=True)
        time.sleep(min(5, left))
    print("\r    %s... done  " % what, flush=True)


def _ensure_focus(env, win, what):
    if _xdo(env, "getactivewindow") == win:
        return
    _xdo(env, "windowactivate", "--sync", win)
    time.sleep(0.5)
    if _xdo(env, "getactivewindow") != win:
        raise ExportError("Wonderdraft lost keyboard focus before %s (another window was clicked?); "
                          "stopped instead of typing elsewhere" % what)


def _wait_file(path, since, timeout=600):
    """Wait until `path` exists and its size has held still for 6 s. If another PNG shows up in
    the folder instead (the typed name came out differently), stop and name it."""
    start, last, stable = time.time(), -1, 0
    folder = os.path.dirname(path)
    while time.time() - start < timeout:
        if not os.path.exists(path) and time.time() - start > 20:
            stray = [f for f in os.listdir(folder) if f.lower().endswith(".png")
                     and os.path.getmtime(os.path.join(folder, f)) >= since]
            if stray:
                raise ExportError("Wonderdraft saved %r instead of %r (keyboard layout?)"
                                  % (stray[0], os.path.basename(path)))
        if os.path.exists(path):
            size = os.path.getsize(path)
            stable = stable + 1 if size == last and size > 0 else 0
            last = size
            if stable >= 3:
                print("\r    writing PNG... done (%.0f MB)   " % (size / 1e6), flush=True)
                return time.time() - start
        print("\r    writing PNG... %3ds " % (time.time() - start), end="", flush=True)
        time.sleep(2)
    raise ExportError("no finished %s after %ds" % (os.path.basename(path), timeout))


def _close(proc):
    if proc.poll() is None:
        proc.send_signal(signal.SIGTERM)
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(5)


def export_view(map_path, env, log=print, load_wait=LOAD_WAIT):
    """Export one .wonderdraft_map to <same name>.webp next to it. Returns the WebP path."""
    folder, name = os.path.split(map_path)
    stem = os.path.splitext(name)[0]
    png, webp = os.path.join(folder, TYPED_NAME + ".png"), os.path.join(folder, stem + ".webp")
    if os.path.exists(png):
        os.remove(png)  # our own leftover; an existing file would make the dialog ask to overwrite
    t0 = time.time()
    with open(os.path.join("/tmp", "wd-export-%s.log" % os.getpid()), "w") as logf:
        proc = subprocess.Popen([WD_BIN, map_path], cwd=WD_DIR, env=env, stdout=logf, stderr=logf)
    try:
        title = "^%s - Wonderdraft$" % stem.replace("(", r"\(").replace(")", r"\)")
        win = ""
        for _ in range(90):
            win = _xdo(env, "search", "--name", title).split("\n")[-1]
            if win:
                break
            time.sleep(1)
        if not win:
            raise ExportError("no Wonderdraft window for %s" % name)
        log("  %s: window up after %.0fs" % (stem, time.time() - t0))
        _countdown(load_wait, "loading " + stem, proc)
        _ensure_focus(env, win, "Ctrl+E")
        _xdo(env, "key", "--clearmodifiers", "ctrl+e")
        time.sleep(2.5)
        _ensure_focus(env, win, "confirming the export options")
        _xdo(env, "key", "Return")
        time.sleep(2.5)
        _ensure_focus(env, win, "typing the file name")
        typed_at = time.time()
        _xdo(env, "type", "--delay", "25", TYPED_NAME + ".png")
        time.sleep(0.5)
        _ensure_focus(env, win, "saving")
        _xdo(env, "key", "Return")
        took = _wait_file(png, typed_at)
        log("  %s: exported %.0f MB PNG in %.0fs" % (stem, os.path.getsize(png) / 1e6, took))
    finally:
        _close(proc)
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(png) as im:
        im.save(webp + ".tmp", "WEBP", quality=WEBP_QUALITY)
    os.replace(webp + ".tmp", webp)
    os.remove(png)
    log("  %s: %s (%.1f MB), %.0fs total" % (stem, os.path.basename(webp), os.path.getsize(webp) / 1e6,
                                             time.time() - t0))
    return webp


def export_views(map_paths, log=print, load_wait=LOAD_WAIT):
    if not os.path.exists(WD_BIN):
        raise ExportError("Wonderdraft not found at %s" % WD_BIN)
    if _wonderdraft_running():
        raise ExportError("Wonderdraft is already running; close it first (its window would confuse the run)")
    env, nvidia = _env()
    log("Exporting %d views with Wonderdraft%s. Hands off keyboard and mouse until it's done."
        % (len(map_paths), " on the NVIDIA GPU" if nvidia else ""))
    return [export_view(p, env, log, load_wait) for p in map_paths]
