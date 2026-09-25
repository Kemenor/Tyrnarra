#!/usr/bin/env python3
"""Split a Wonderdraft map into one file per region type.

Wonderdraft has a single regions overlay, so god domains and regions can't be
toggled separately. This writes a copy of the map per variant, keeping only that
variant's region shapes and dropping labels on the layers it hides. The input
map is only read, never modified.

    wd-regions MAP.wonderdraft_map [-o OUTDIR]
"""
import argparse
import os
import shutil
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import gdvar  # noqa: E402

GCPF_SRC = os.path.join(HERE, "gcpf.c")
GCPF = os.path.join(HERE, "gcpf")


def ensure_codec():
    """Build the gcpf codec from source when missing or stale (the binary is gitignored)."""
    if os.path.exists(GCPF) and os.path.getmtime(GCPF) >= os.path.getmtime(GCPF_SRC):
        return
    cc = next((c for c in ("cc", "gcc", "clang") if shutil.which(c)), None)
    if not cc:
        sys.exit("need a C compiler to build %s (see README.md)" % GCPF_SRC)
    print("building gcpf codec with %s..." % cc)
    subprocess.run([cc, "-O2", "-o", GCPF, GCPF_SRC], check=True)

# Region shapes are told apart by border style; label layers are z_index
# (Default = 0, "+1" = 1, ...).
VARIANTS = {
    "God Domains": {"border": "border_dash", "hide_label_layers": {2}},
    "Regions": {"border": "border_gradient", "hide_label_layers": {1}},
}


def u32(n):
    return struct.pack("<I", n)


def child(node, name):
    for k, v in node.children:
        if gdvar.key_str(k) == name:
            return k, v
    raise KeyError(name)


def field(item, name):
    for k, v in item.children:
        if gdvar.key_str(k) == name:
            return v.value
    return None


def raw(b, node):
    return b[node.start:node.end]


def array_bytes(b, arr, keep):
    """Re-encode ARRAY `arr` keeping only children where keep(child) is true."""
    kept = [v for _, v in arr.children if keep(v)]
    return u32(19) + u32(len(kept)) + b"".join(raw(b, v) for v in kept), len(kept)


def dict_bytes(b, d, replace):
    """Re-encode DICTIONARY `d`, swapping values whose key is in `replace`."""
    out = [raw(b, d)[:8]]  # type header + entry count
    for k, v in d.children:
        out.append(raw(b, k))
        out.append(replace.get(gdvar.key_str(k)) or raw(b, v))
    return b"".join(out)


def build_variant(b, root, spec):
    _, terr = child(root, "territories")
    _, shapes = child(terr, "territories")
    new_shapes, n_shapes = array_bytes(
        b, shapes, lambda t: (field(t, "style") or "").endswith("/" + spec["border"]))
    new_terr = dict_bytes(b, terr, {"territories": new_shapes})

    _, labels = child(root, "labels")
    new_labels, n_labels = array_bytes(
        b, labels, lambda l: field(l, "z_index") not in spec["hide_label_layers"])

    body = dict_bytes(b, root, {"territories": new_terr, "labels": new_labels})
    return u32(len(body)) + body, n_shapes, n_labels


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("map", help="input .wonderdraft_map (read only)")
    ap.add_argument("-o", "--outdir", help="output folder (default: next to the input)")
    a = ap.parse_args()

    src = os.path.abspath(a.map)
    outdir = os.path.abspath(a.outdir) if a.outdir else os.path.dirname(src)
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(src))[0]

    ensure_codec()
    r = subprocess.run([GCPF, "d", src], stdout=subprocess.PIPE)
    if r.returncode:
        sys.exit("could not read %s" % src)
    b = r.stdout
    (length,) = struct.unpack_from("<I", b, 0)
    root = gdvar.parse(b, 4)
    if root.end != 4 + length or root.tname != "DICTIONARY":
        sys.exit("%s: unexpected map layout" % src)
    _, labels = child(root, "labels")
    _, shapes = child(child(root, "territories")[1], "territories")
    print("%s: %d region shapes, %d labels" % (os.path.basename(src), len(shapes.children), len(labels.children)))

    for name, spec in VARIANTS.items():
        data, n_shapes, n_labels = build_variant(b, root, spec)
        # sanity: the new data must parse back completely
        check = gdvar.parse(data, 4)
        assert check.end == len(data), name
        dst = os.path.join(outdir, "%s - %s.wonderdraft_map" % (stem, name))
        if os.path.abspath(dst) == src:
            sys.exit("refusing to overwrite the input")
        tmp = dst + ".tmp"
        w = subprocess.run([GCPF, "c", tmp], input=data)
        if w.returncode:
            sys.exit("failed writing %s" % dst)
        os.replace(tmp, dst)
        print("  %-12s %3d shapes, %3d labels -> %s" % (name, n_shapes, n_labels, dst))


if __name__ == "__main__":
    main()
