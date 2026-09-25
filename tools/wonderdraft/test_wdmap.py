"""Tests for the Wonderdraft map tooling.

    python3 -m unittest tools/wonderdraft/test_wdmap.py

The real-map tests run against ~/ProtonDrive/Wonderdraft/Main.wonderdraft_map
(or $WD_TEST_MAP) and are skipped when that file isn't there. The map is decoded
once and shared: a decoded 8192px map takes a few GB, so each test class must
not load its own.
"""
import copy
import os
import struct
import sys
import unittest

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)
import gdvar  # noqa: E402
from gdvar import Color, GdObject, PoolIntArray, PoolRealArray, PoolStringArray, PoolVector2Array, Vector2  # noqa: E402
from wdmap import WDMap, family, point_in_poly, read_raw, select  # noqa: E402

TEST_MAP = os.environ.get("WD_TEST_MAP", os.path.expanduser("~/ProtonDrive/Wonderdraft/Main.wonderdraft_map"))


_REAL = {}


def real_map():
    """(raw bytes, WDMap) of the test map, decoded once per test run."""
    if not _REAL:
        raw = read_raw(TEST_MAP)
        _REAL["raw"] = raw
        _REAL["map"] = WDMap(gdvar.decode(raw, 4)[0], TEST_MAP)
    return _REAL["raw"], _REAL["map"]


def roundtrip(v):
    data = gdvar.encode(v)
    out, end = gdvar.decode(data)
    assert end == len(data)
    return out, data


class CodecTest(unittest.TestCase):
    def test_scalars(self):
        for v in (None, True, False, 0, -5, 2 ** 40, 0.5, 0.1, "", "Zuzental", "Legea\nEmpire", "é"):
            out, data = roundtrip(v)
            self.assertEqual(out, v)
            self.assertEqual(gdvar.encode(out), data)

    def test_int_is_always_64_bit(self):
        self.assertEqual(gdvar.encode(15), struct.pack("<Iq", 2 | gdvar.FLAG_64, 15))

    def test_real_width_follows_float32_exactness(self):
        self.assertEqual(len(gdvar.encode(0.5)), 8)   # exact in float32
        self.assertEqual(len(gdvar.encode(0.1)), 12)  # needs float64

    def test_structs_and_pools(self):
        v = {"p": Vector2(1.5, -2), "c": Color(1, 0.5, 0, 1), "b": b"\x01\x02\x03",
             "i": PoolIntArray([1, -2, 3]), "r": PoolRealArray([0.5, 2]),
             "s": PoolStringArray(["a", "bc"]), "v": PoolVector2Array([Vector2(1, 2)]),
             "l": [1, "x", [None]]}
        out, data = roundtrip(v)
        self.assertEqual(gdvar.encode(out), data)
        self.assertIsInstance(out["p"], Vector2)
        self.assertEqual(out["p"].y, -2)

    def test_object_keeps_duplicate_props(self):
        obj = GdObject("ImageTexture", [("flags", 2), ("storage", 0), ("flags", 2)])
        out, data = roundtrip(obj)
        self.assertEqual(out.props, obj.props)
        self.assertEqual(out.get("storage"), 0)
        null, _ = roundtrip(GdObject(""))
        self.assertEqual(null.cls, "")


class HelpersTest(unittest.TestCase):
    def test_family(self):
        self.assertEqual(family("res://sprites/trees/_hd_oak/tree_oak12"), "res://sprites/trees/_hd_oak/tree_oak")
        self.assertEqual(family("user://assets/Dotty/Kapok_Tree_11"), "user://assets/Dotty/Kapok_Tree")

    def test_point_in_poly(self):
        sq = [(0, 0), (10, 0), (10, 10), (0, 10)]
        self.assertTrue(point_in_poly(5, 5, sq))
        self.assertFalse(point_in_poly(15, 5, sq))


@unittest.skipUnless(os.path.exists(TEST_MAP), "no test map at %s" % TEST_MAP)
class RealMapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.m = real_map()

    def test_byte_identical_roundtrip(self):
        body = gdvar.encode(self.m.data)
        same = memoryview(self.raw)[4:] == body and struct.unpack_from("<I", self.raw)[0] == len(body)
        del body
        self.assertTrue(same, "re-encoded map differs from the original")

    def test_queries(self):
        m = self.m
        self.assertGreater(len(select(m, "symbols", type_="tree")), 0)
        on_water = select(m, "symbols", type_="tree", on="water")
        self.assertLess(len(on_water), len(select(m, "symbols", type_="tree")) / 10)
        named = [r for r in m.regions if r.name]
        self.assertGreater(len(named), len(m.regions) / 2)


@unittest.skipUnless(os.path.exists(TEST_MAP), "no test map at %s" % TEST_MAP)
class EditTest(unittest.TestCase):
    """Edits on an in-memory copy of the real map; nothing is written."""

    @classmethod
    def setUpClass(cls):
        # Edit a copy of the editable lists; the big terrain images stay shared and untouched.
        _, shared = real_map()
        data = dict(shared.data)
        for k in ("symbols", "labels", "territories"):
            data[k] = copy.deepcopy(shared.data[k])
        cls.m = WDMap(data, TEST_MAP)

    def test_label_replace(self):
        import edit
        hits = select(self.m, "labels", text="*prinicpality*")
        if not hits:
            self.skipTest("typo already fixed in the map")
        lines = edit.edit_labels(self.m, hits, replace=("Prinicpality", "Principality"))
        self.assertIn("Principality", hits[0][1]["text"])
        self.assertTrue(lines[0].startswith("text:"))

    def test_art_swap_keeps_footprint_and_resamples(self):
        import edit
        hits = select(self.m, "symbols", family_="*hatch_pine*")[:20]
        before = [s["radius"] * s["scale"][0] for _, s in hits]
        edit.edit_symbols(self.m, hits, art="user://assets/Dotty_Assets/sprites/trees/Dotty_Kapoks/Kapok_Tree")
        for (_, s), fp in zip(hits, before):
            self.assertIn("Kapok_Tree", s["texture"])
            self.assertAlmostEqual(s["radius"] * s["scale"][0], fp, places=3)
            self.assertEqual(tuple(s["sample"]), tuple(self.m.ground_sample(*s["position"])))

    def test_delete_and_reencode(self):
        import edit
        n = len(self.m.symbols)
        hits = select(self.m, "symbols", type_="tree", on="water")
        edit.edit_symbols(self.m, hits, delete=True)
        self.assertEqual(len(self.m.symbols), n - len(hits))
        data = gdvar.encode(self.m.data["symbols"])
        self.assertEqual(gdvar.decode(data)[1], len(data))


if __name__ == "__main__":
    unittest.main()
