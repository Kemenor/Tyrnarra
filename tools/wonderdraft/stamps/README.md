# Stamps

Reusable groups of Wonderdraft symbols and labels, captured with `wdmap stamp capture` or an `@stamp` marker and placed with `wdmap stamp place` or `@place`. See [`../README.md`](../README.md), *Adding things*.

Each `<name>.json` holds the captured items with positions relative to the stamp's anchor. Godot types are written as `{"$Vector2": [x, y]}` / `{"$Color": [r, g, b, a]}`, so a stamp can be read and hand-edited. Art is referenced by path (`user://…` pack art, `res://…` Wonderdraft built-ins), so a stamp works on any map whose Wonderdraft has the same packs.
