"""Edits on selections of a WDMap: symbols, labels, regions.

Each function takes the map and a selection ([(index, item)] from wdmap.select)
and returns a list of human-readable change lines. Nothing is saved here.
"""
import math
import os
import re

from gdvar import Color, Vector2
from wdmap import USER_DIR, family

BORDER_STYLE = {"domain": "res://textures/borders/border_dash",
                "region": "res://textures/borders/border_gradient"}
# Per-art fields copied from a template symbol when swapping art: they belong to
# the sprite (anchor offset, footprint, kind, colour setup), not to the placement.
ART_FIELDS = ("texture", "offset", "radius", "type", "custom_colors", "custom_color_mode",
              "outline_width", "outline_color")
_VARIANT = re.compile(r"(\d+)$")


def parse_color(spec, alpha=None):
    """'#rrggbb', '#rrggbbaa' or 'r,g,b[,a]' (0-1 floats) to a Color."""
    s = spec.strip()
    if s.startswith("#"):
        h = s[1:]
        vals = [int(h[i:i + 2], 16) / 255 for i in range(0, len(h), 2)]
    else:
        vals = [float(v) for v in s.split(",")]
    if len(vals) == 3:
        vals.append(1.0 if alpha is None else alpha)
    if len(vals) != 4:
        raise ValueError("bad colour %r" % spec)
    return Color(*vals)


def _variants_on_disk(fam):
    """user:// textures of a family that exist as files, e.g. .../Kapok_Tree_1..14."""
    if not fam.startswith("user://"):
        return []
    base = os.path.join(USER_DIR, fam[len("user://"):])
    d, stem = os.path.split(base)
    out = []
    if os.path.isdir(d):
        for f in os.listdir(d):
            name, ext = os.path.splitext(f)
            if ext.lower() in (".png", ".webp", ".jpg") and family(name) == stem:
                out.append(fam[:len(fam) - len(stem)] + name)
    return out


def art_targets(m, spec):
    """Resolve an art spec (exact texture or family) to ({texture: template symbol}, [unused variants]).

    Only art already used somewhere in the map can be targeted: the template
    supplies the sprite's offset/radius/type, which Wonderdraft computes on
    placement and which can't be derived here reliably.
    """
    templates = {}
    for s in m.symbols:
        templates.setdefault(s.get("texture"), s)
    spec_l = spec.lower()
    exact = [t for t in templates if t and t.lower() == spec_l]
    if exact:
        return {exact[0]: templates[exact[0]]}, []
    fam = [t for t in templates if t and family(t).lower() == spec_l]
    if not fam:
        raise ValueError("no art %r in this map; place one of it in Wonderdraft once so it can be copied" % spec)
    missing = sorted(set(_variants_on_disk(family(fam[0]))) - set(fam))
    return {t: templates[t] for t in sorted(fam)}, missing


def _variant_no(tex):
    mm = _VARIANT.search(tex or "")
    return int(mm.group(1)) if mm else 0


def _resample(m, s):
    """Refresh a symbol's ground-colour sample after it moved or changed art, like Wonderdraft
    does on placement. Art that isn't ground-tinted (sample None) stays None."""
    if s.get("sample") is not None:
        s["sample"] = m.ground_sample(*s["position"])


def edit_symbols(m, hits, move=None, scale=None, rotate=None, layer=None, art=None, delete=False):
    """Art swaps keep each symbol's footprint (radius x scale), so a swapped tree takes the
    space of the one it replaces; add --scale to resize on top of that."""
    lines = []
    if art:
        targets, missing = art_targets(m, art)
        names = list(targets)
        swapped = {}
        for i, s in hits:
            new = names[_variant_no(s.get("texture")) % len(names)]
            if new == s.get("texture"):
                continue
            key = (family(s.get("texture")), family(new))
            swapped[key] = swapped.get(key, 0) + 1
            tpl = targets[new]
            old_radius = s.get("radius") or 0
            for f in ART_FIELDS:
                v = tpl.get(f)
                s[f] = list(v) if isinstance(v, list) else v  # no shared palette lists
            if old_radius and s.get("radius"):
                k = old_radius / s["radius"]
                s["scale"] = Vector2(s["scale"][0] * k, s["scale"][1] * k)
            s["sample"] = m.ground_sample(*s["position"]) if tpl.get("sample") is not None else None
        for (a, b), n in swapped.items():
            lines.append("art: %d x %s -> %s (%d variant%s)" % (n, a, b, len(names), "s" if len(names) > 1 else ""))
        if missing:
            lines.append("note: %d more variants exist in the pack but aren't used in the map yet, so were skipped"
                         % len(missing))
    for i, s in hits:
        if move:
            s["position"] = Vector2(s["position"][0] + move[0], s["position"][1] + move[1])
            _resample(m, s)
        if scale:
            s["scale"] = Vector2(s["scale"][0] * scale, s["scale"][1] * scale)
        if rotate:
            s["rotation"] = s.get("rotation", 0.0) + math.radians(rotate)
        if layer is not None:
            s["z_index"] = layer
    n = len(hits)
    if move:
        lines.append("moved %d symbols by (%g, %g)" % (n, move[0], move[1]))
    if scale:
        lines.append("scaled %d symbols by %g" % (n, scale))
    if rotate:
        lines.append("rotated %d symbols by %g deg" % (n, rotate))
    if layer is not None:
        lines.append("moved %d symbols to layer %s" % (n, m.layer_name(layer)))
    if delete:
        drop = {i for i, _ in hits}
        m.data["symbols"] = [s for i, s in enumerate(m.symbols) if i not in drop]
        lines.append("deleted %d symbols" % len(drop))
    return lines


def edit_labels(m, hits, move=None, scale=None, rotate=None, layer=None, text=None, replace=None,
                font=None, size=None, color=None, delete=False):
    lines = []
    for i, l in hits:
        old = l["text"]
        if text is not None:
            l["text"] = text
        if replace:
            l["text"] = l["text"].replace(replace[0], replace[1])
        if l["text"] != old:
            lines.append("text: %r -> %r" % (" ".join(old.split()), " ".join(l["text"].split())))
        if move:
            l["position"] = Vector2(l["position"][0] + move[0], l["position"][1] + move[1])
        if scale:
            l["size"] = max(1, round(l["size"] * scale))
        if size:
            l["size"] = size
        if rotate:
            l["rotation"] = l.get("rotation", 0.0) + math.radians(rotate)
        if layer is not None:
            l["z_index"] = layer
        if font:
            l["font"] = font
        if color:
            l["color"] = parse_color(color, alpha=l["color"][3])
    n = len(hits)
    for flag, msg in ((move, "moved %d labels by (%s)" % (n, move and "%g, %g" % move)),
                      (scale, "scaled %d labels by %s" % (n, scale)),
                      (size, "set size of %d labels to %s" % (n, size)),
                      (rotate, "rotated %d labels by %s deg" % (n, rotate)),
                      (layer is not None, "moved %d labels to layer %s" % (n, layer is not None and m.layer_name(layer))),
                      (font, "set font of %d labels to %s" % (n, font)),
                      (color, "recoloured %d labels" % n)):
        if flag:
            lines.append(msg)
    if replace and not any(l.startswith("text:") for l in lines):
        lines.append("replace: %r not found in the selected labels" % replace[0])
    if delete:
        drop = {i for i, _ in hits}
        lines.append("deleted %d labels: %s" % (len(drop), ", ".join(
            " ".join(l["text"].split()) for i, l in enumerate(m.labels) if i in drop)))
        m.data["labels"] = [l for i, l in enumerate(m.labels) if i not in drop]
    m.invalidate()
    return lines


def edit_regions(m, hits, move=None, color=None, style=None, width=None, delete=False):
    lines = []
    for i, r in hits:
        t = r.data
        if move:
            t["position"] = Vector2(t["position"][0] + move[0], t["position"][1] + move[1])
        if color:
            t["color"] = parse_color(color, alpha=t["color"][3])
        if style:
            t["style"] = BORDER_STYLE.get(style, style)
        if width is not None:
            t["width"] = float(width)
    names = ", ".join(r.label for _, r in hits[:12]) + (" ..." if len(hits) > 12 else "")
    for flag, msg in ((move, "moved"), (color, "recoloured"), (style, "restyled to %s:" % style),
                      (width is not None, "set border width %s:" % width)):
        if flag:
            lines.append("%s %d regions: %s" % (msg, len(hits), names))
    if delete:
        drop = {i for i, _ in hits}
        m.data["territories"]["territories"] = [t for i, t in enumerate(m.territories) if i not in drop]
        lines.append("deleted %d regions: %s" % (len(drop), names))
    m.invalidate()
    return lines
