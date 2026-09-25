"""Godot 3 Variant (store_var / encode_variant) codec for Wonderdraft maps: a byte-range parser plus full decode/encode."""
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


# ---------------------------------------------------------------------------
# Full decode / encode to plain Python values.
#
# decode() turns a variant into Python values; encode() writes it back. For
# anything Wonderdraft writes, encode(decode(x)) reproduces x byte for byte:
# INT is always written 64-bit and REAL is 64-bit only when float32 can't hold
# the value exactly, so plain Python ints and floats carry enough information.

from array import array


class _Fixed(tuple):
    """Fixed-size float struct (Vector2, Color, ...); fields are float32 on disk."""
    TYPE = None
    SIZE = None

    def __new__(cls, *vals):
        if len(vals) == 1 and not isinstance(vals[0], (int, float)):
            vals = tuple(vals[0])
        if len(vals) != cls.SIZE:
            raise ValueError("%s needs %d values" % (cls.__name__, cls.SIZE))
        return super().__new__(cls, (float(v) for v in vals))

    def __repr__(self):
        return "%s(%s)" % (type(self).__name__, ", ".join("%g" % v for v in self))


def _fixed(name, type_, size):
    return type(name, (_Fixed,), {"TYPE": type_, "SIZE": size, "__slots__": ()})


Vector2 = _fixed("Vector2", 5, 2)
Rect2 = _fixed("Rect2", 6, 4)
Vector3 = _fixed("Vector3", 7, 3)
Transform2D = _fixed("Transform2D", 8, 6)
Plane = _fixed("Plane", 9, 4)
Quat = _fixed("Quat", 10, 4)
AABB = _fixed("AABB", 11, 6)
Basis = _fixed("Basis", 12, 9)
Transform = _fixed("Transform", 13, 12)
Color = _fixed("Color", 14, 4)
FIXED_TYPES = {c.TYPE: c for c in (Vector2, Rect2, Vector3, Transform2D, Plane, Quat, AABB, Basis, Transform, Color)}

for _c in (Vector2,):
    _c.x = property(lambda s: s[0])
    _c.y = property(lambda s: s[1])
Color.r = property(lambda s: s[0])
Color.g = property(lambda s: s[1])
Color.b = property(lambda s: s[2])
Color.a = property(lambda s: s[3])


class GdObject:
    """An encoded Object: class name plus ordered (name, value) properties.

    A list, not a dict: Godot can list a property twice (ImageTexture writes
    "flags" twice). Empty class name = null object.
    """
    __slots__ = ("cls", "props")

    def __init__(self, cls, props=None):
        self.cls, self.props = cls, props if props is not None else []

    def get(self, name, default=None):
        for k, v in self.props:
            if k == name:
                return v
        return default

    def __repr__(self):
        return "GdObject(%r, %d props)" % (self.cls, len(self.props))


class Raw:
    """A variant kept as its exact encoded bytes (NodePath, RID, object ids)."""
    __slots__ = ("data",)

    def __init__(self, data):
        self.data = bytes(data)

    @property
    def type(self):
        return struct.unpack_from("<I", self.data)[0] & 0xFFFF

    def __repr__(self):
        return "Raw(%s, %d bytes)" % (NAMES[self.type], len(self.data))


class PoolIntArray(array):
    def __new__(cls, vals=()):
        return super().__new__(cls, "i", vals)


class PoolRealArray(array):
    def __new__(cls, vals=()):
        return super().__new__(cls, "f", vals)


class PoolStringArray(list):
    pass


class PoolVector2Array(list):
    pass


class PoolVector3Array(list):
    pass


class PoolColorArray(list):
    pass


def _read_str(b, p):
    (n,) = struct.unpack_from("<I", b, p)
    return bytes(b[p + 4:p + 4 + n]).decode("utf-8"), p + 4 + pad4(n)


def decode(b, p=0):
    """Decode the variant at offset p. Returns (value, end_offset)."""
    (hdr,) = struct.unpack_from("<I", b, p)
    t, flags = hdr & 0xFFFF, hdr >> 16
    start = p
    p += 4
    if t == 0:
        return None, p
    if t == 1:
        return bool(struct.unpack_from("<I", b, p)[0]), p + 4
    if t == 2:
        if flags & 1:
            return struct.unpack_from("<q", b, p)[0], p + 8
        return struct.unpack_from("<i", b, p)[0], p + 4
    if t == 3:
        if flags & 1:
            return struct.unpack_from("<d", b, p)[0], p + 8
        return struct.unpack_from("<f", b, p)[0], p + 4
    if t == 4:
        return _read_str(b, p)
    if t in FIXED_TYPES:
        cls = FIXED_TYPES[t]
        return cls(struct.unpack_from("<%df" % cls.SIZE, b, p)), p + 4 * cls.SIZE
    if t in (15, 16) or (t == 17 and flags & 1):
        end = parse(b, start).end
        return Raw(b[start:end]), end
    if t == 17:
        cls, p = _read_str(b, p)
        props = []
        if cls:
            (cnt,) = struct.unpack_from("<I", b, p)
            p += 4
            for _ in range(cnt):
                k, p = _read_str(b, p)
                pv, p = decode(b, p)
                props.append((k, pv))
        return GdObject(cls, props), p
    if t == 18:
        (cnt,) = struct.unpack_from("<I", b, p)
        p += 4
        if cnt & 0x80000000:
            raise ValueError("shared dictionary flag at %d" % start)
        d = {}
        for _ in range(cnt):
            k, p = decode(b, p)
            d[k], p = decode(b, p)
        if len(d) != cnt:
            raise ValueError("colliding dictionary keys at %d" % start)
        return d, p
    if t == 19:
        (cnt,) = struct.unpack_from("<I", b, p)
        p += 4
        if cnt & 0x80000000:
            raise ValueError("shared array flag at %d" % start)
        out = []
        for _ in range(cnt):
            v, p = decode(b, p)
            out.append(v)
        return out, p
    (cnt,) = struct.unpack_from("<I", b, p)
    p += 4
    if t == 20:
        return bytes(b[p:p + cnt]), p + pad4(cnt)
    if t == 21:
        a = PoolIntArray()
        a.frombytes(b[p:p + 4 * cnt])
        return a, p + 4 * cnt
    if t == 22:
        a = PoolRealArray()
        a.frombytes(b[p:p + 4 * cnt])
        return a, p + 4 * cnt
    if t == 23:
        out = PoolStringArray()
        for _ in range(cnt):
            s, p = _read_str(b, p)
            out.append(s)
        return out, p
    if t in (24, 25, 26):
        cls, arr = {24: (Vector2, PoolVector2Array), 25: (Vector3, PoolVector3Array),
                    26: (Color, PoolColorArray)}[t]
        n = cls.SIZE
        flat = struct.unpack_from("<%df" % (n * cnt), b, p)
        return arr(cls(flat[i:i + n]) for i in range(0, n * cnt, n)), p + 4 * n * cnt
    raise ValueError("unknown variant type %d at %d" % (t, start))


def _put_str(out, s):
    data = s.encode("utf-8")
    out += struct.pack("<I", len(data))
    out += data
    out += b"\0" * (pad4(len(data)) - len(data))


def _encode(v, out):
    if v is None:
        out += struct.pack("<I", 0)
    elif isinstance(v, bool):
        out += struct.pack("<II", 1, int(v))
    elif isinstance(v, int):
        # Wonderdraft's Godot build writes every INT as 64-bit, whatever its size.
        out += struct.pack("<Iq", 2 | FLAG_64, v)
    elif isinstance(v, float):
        if struct.unpack("<f", struct.pack("<f", v))[0] == v:
            out += struct.pack("<If", 3, v)
        else:
            out += struct.pack("<Id", 3 | FLAG_64, v)
    elif isinstance(v, str):
        out += struct.pack("<I", 4)
        _put_str(out, v)
    elif isinstance(v, _Fixed):
        out += struct.pack("<I%df" % v.SIZE, v.TYPE, *v)
    elif isinstance(v, Raw):
        out += v.data
    elif isinstance(v, GdObject):
        out += struct.pack("<I", 17)
        _put_str(out, v.cls)
        if v.cls:
            out += struct.pack("<I", len(v.props))
            for k, pv in v.props:
                _put_str(out, k)
                _encode(pv, out)
    elif isinstance(v, dict):
        out += struct.pack("<II", 18, len(v))
        for k, dv in v.items():
            _encode(k, out)
            _encode(dv, out)
    elif isinstance(v, (bytes, bytearray)):
        out += struct.pack("<II", 20, len(v))
        out += v
        out += b"\0" * (pad4(len(v)) - len(v))
    elif isinstance(v, PoolIntArray):
        out += struct.pack("<II", 21, len(v))
        out += v.tobytes()
    elif isinstance(v, PoolRealArray):
        out += struct.pack("<II", 22, len(v))
        out += v.tobytes()
    elif isinstance(v, PoolStringArray):
        out += struct.pack("<II", 23, len(v))
        for s in v:
            _put_str(out, s)
    elif isinstance(v, (PoolVector2Array, PoolVector3Array, PoolColorArray)):
        t = {PoolVector2Array: 24, PoolVector3Array: 25, PoolColorArray: 26}[type(v)]
        out += struct.pack("<II", t, len(v))
        for item in v:
            out += struct.pack("<%df" % len(item), *item)
    elif isinstance(v, (list, tuple)):
        out += struct.pack("<II", 19, len(v))
        for item in v:
            _encode(item, out)
    else:
        raise TypeError("cannot encode %r" % type(v))


def encode(v):
    out = bytearray()
    _encode(v, out)
    return bytes(out)
