"""Godot 3 Variant (store_var / encode_variant) parser, enough to walk Wonderdraft maps."""
import struct

NAMES = ["NIL", "BOOL", "INT", "REAL", "STRING", "VECTOR2", "RECT2", "VECTOR3", "TRANSFORM2D",
         "PLANE", "QUAT", "AABB", "BASIS", "TRANSFORM", "COLOR", "NODE_PATH", "RID", "OBJECT",
         "DICTIONARY", "ARRAY", "POOL_BYTE_ARRAY", "POOL_INT_ARRAY", "POOL_REAL_ARRAY",
         "POOL_STRING_ARRAY", "POOL_VECTOR2_ARRAY", "POOL_VECTOR3_ARRAY", "POOL_COLOR_ARRAY"]
FIXED_FLOATS = {5: 2, 6: 4, 7: 3, 8: 6, 9: 4, 10: 4, 11: 6, 12: 9, 13: 12, 14: 4}
POOL_ELEM = {20: 1, 21: 4, 22: 4, 24: 8, 25: 12, 26: 16}
FLAG_64 = 1 << 16


class Node:
    __slots__ = ("type", "start", "end", "value", "children")

    def __init__(self, type_, start):
        self.type, self.start, self.end, self.value, self.children = type_, start, None, None, None

    @property
    def tname(self):
        return NAMES[self.type]

    @property
    def size(self):
        return self.end - self.start


def pad4(n):
    return (n + 3) & ~3


def read_string(b, p):
    (n,) = struct.unpack_from("<I", b, p)
    return b[p + 4:p + 4 + n].decode("utf-8", "replace"), p + 4 + pad4(n)


def parse(b, p, keep_values=True):
    """Parse one variant at offset p. Returns Node (with .end set)."""
    (hdr,) = struct.unpack_from("<I", b, p)
    t, flags = hdr & 0xFFFF, hdr >> 16
    node = Node(t, p)
    p += 4
    if t == 0:
        pass
    elif t == 1:
        node.value = bool(struct.unpack_from("<I", b, p)[0]); p += 4
    elif t == 2:
        if flags & 1:
            node.value = struct.unpack_from("<q", b, p)[0]; p += 8
        else:
            node.value = struct.unpack_from("<i", b, p)[0]; p += 4
    elif t == 3:
        if flags & 1:
            node.value = struct.unpack_from("<d", b, p)[0]; p += 8
        else:
            node.value = struct.unpack_from("<f", b, p)[0]; p += 4
    elif t == 4:
        node.value, p = read_string(b, p)
    elif t in FIXED_FLOATS:
        k = FIXED_FLOATS[t]
        node.value = struct.unpack_from("<%df" % k, b, p); p += 4 * k
    elif t == 15:
        (n,) = struct.unpack_from("<I", b, p)
        if n & 0x80000000:
            names = n & 0x7FFFFFFF
            subs, fl = struct.unpack_from("<II", b, p + 4)
            p += 12
            parts = []
            for _ in range(names + subs + (1 if fl & 2 else 0)):
                s, p = read_string(b, p); parts.append(s)
            node.value = parts
        else:
            node.value, p = read_string(b, p)
    elif t == 16:
        pass
    elif t == 17:
        if flags & 1:
            node.value = struct.unpack_from("<Q", b, p)[0]; p += 8
        else:
            cls, p = read_string(b, p)
            node.value = cls
            node.children = []
            if cls:
                (cnt,) = struct.unpack_from("<I", b, p); p += 4
                for _ in range(cnt):
                    k, p = read_string(b, p)
                    v = parse(b, p, keep_values); p = v.end
                    node.children.append((k, v))
    elif t == 18:
        (cnt,) = struct.unpack_from("<I", b, p); p += 4
        cnt &= 0x7FFFFFFF
        node.children = []
        for _ in range(cnt):
            k = parse(b, p, keep_values); p = k.end
            v = parse(b, p, keep_values); p = v.end
            node.children.append((k, v))
    elif t == 19:
        (cnt,) = struct.unpack_from("<I", b, p); p += 4
        cnt &= 0x7FFFFFFF
        node.children = []
        for _ in range(cnt):
            v = parse(b, p, keep_values); p = v.end
            node.children.append((None, v))
    elif t in POOL_ELEM:
        (cnt,) = struct.unpack_from("<I", b, p); p += 4
        node.value = cnt
        p += pad4(cnt * POOL_ELEM[t])
    elif t == 23:
        (cnt,) = struct.unpack_from("<I", b, p); p += 4
        vals = []
        for _ in range(cnt):
            s, p = read_string(b, p); vals.append(s)
        node.value = vals
    else:
        raise ValueError("unknown variant type %d at %d" % (t, node.start))
    node.end = p
    return node


def key_str(k):
    if k is None:
        return ""
    if isinstance(k, str):  # OBJECT property names
        return k
    return repr(k.value) if k.type in (2, 3) else str(k.value)


def summary(n):
    if n.type in POOL_ELEM or n.type == 23:
        cnt = n.value if n.type != 23 else len(n.value)
        return "%s[%d]" % (n.tname, cnt)
    if n.type in (18, 19):
        return "%s{%d}" % (n.tname, len(n.children))
    if n.type == 17:
        return "OBJECT<%s>" % n.value
    v = repr(n.value)
    return "%s = %s" % (n.tname, v if len(v) < 80 else v[:77] + "...")


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.0f%s" % (n, u)
        n /= 1024
    return "%.1fTB" % n


def dump(n, depth=0, maxdepth=3, maxkids=12, label="root"):
    print("%s%s: %s  (%s)" % ("  " * depth, label, summary(n), human(n.size)))
    if n.children is None or depth >= maxdepth:
        return
    for i, (k, v) in enumerate(n.children):
        if i >= maxkids:
            print("%s... %d more" % ("  " * (depth + 1), len(n.children) - maxkids))
            break
        dump(v, depth + 1, maxdepth, maxkids, key_str(k) if k is not None else "[%d]" % i)


def load(path):
    b = open(path, "rb").read()
    (length,) = struct.unpack_from("<I", b, 0)  # store_var length prefix
    root = parse(b, 4)
    assert root.end == 4 + length, (root.end, length)
    return b, root
