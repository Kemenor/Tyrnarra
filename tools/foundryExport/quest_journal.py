#!/usr/bin/env python3
"""
quest_journal.py - a quest's GM pages -> a Foundry journal spec (+ staged art).

Reads the quest's GM HTML (scene pages and the cast page) and turns it into
JournalEntry pages Foundry can show: read-alouds as block quotes, GM notes under
headings, the numbers grids as tables, GM secrets as Foundry secret blocks, and
each NPC's portrait on their page. The page markup of the GM layer is rewritten
into plain HTML, because Foundry does not load gm.css.

Art is staged as resized .webp into --stage, ready for upload_foundry.py; an
image is only referenced when its file exists, so re-run after new renders.

    python quest_journal.py \\
        --quest ../../published/gm-notes/short-notice/quest-the-unspent \\
        --folder "The Unspent" \\
        --chapter "Chapter 1: Struck Colours=struck-colours.html" \\
        --cast cast.html --views art/twin-cities-views.set.json \\
        --campaign short-notice --sub the-unspent \\
        --stage _stage/the-unspent --spec the-unspent.journal.json \\
        --macro the-unspent.journal.js

Then: upload_foundry.py --dir _stage/the-unspent --campaign short-notice --sub the-unspent,
and paste-run the macro in Foundry as GM.
"""
import argparse
import json
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import foundry_macro  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
MAX_PX = 1600
STRIP = [".gm-banner", ".breadcrumb", ".scene-jump", ".map-wrap", ".map-toggle",
         ".map-hint", ".map-detail", ".map-detail-empty", "script", "style",
         ".expand-hint", ".npc-art", ".npc-icon", ".npc-face", ".draft-note"]


def world_for(campaign):
    return json.load(open(os.path.join(HERE, "campaigns.json")))[campaign]


class Art:
    """Stages images as .webp and hands back their Foundry path."""

    def __init__(self, quest_dir, stage, base):
        self.quest_dir, self.stage, self.base = quest_dir, stage, base
        self.staged = set()
        os.makedirs(stage, exist_ok=True)

    def src(self, web_src):
        """A page's image src (/gm-notes/.../art/x.png or relative) -> Foundry path, or None."""
        if web_src.startswith("/"):          # a site path: /gm-notes/... lives under published/
            local = os.path.join(REPO, "published", web_src.lstrip("/"))
        else:
            local = os.path.join(self.quest_dir, web_src)
        if not os.path.isfile(local):
            return None
        stem, ext = os.path.splitext(os.path.basename(local))
        if ext.lower() == ".svg":
            out_name = stem + ".svg"
            out = os.path.join(self.stage, out_name)
            if not os.path.isfile(out):
                with open(local, "rb") as a, open(out, "wb") as b:
                    b.write(a.read())
        else:
            out_name = stem + ".webp"
            out = os.path.join(self.stage, out_name)
            if not os.path.isfile(out) or os.path.getmtime(out) < os.path.getmtime(local):
                im = Image.open(local)
                im.thumbnail((MAX_PX, MAX_PX))
                im.save(out, "WEBP", quality=85)
        self.staged.add(out_name)
        return self.base + out_name


def text(el):
    return " ".join(el.get_text(" ", strip=True).split())


def grid_table(grid, soup):
    """A .stat-grid -> a two-row table: names, then values (with tier or DC note)."""
    cells = grid.select(".sg-cell")
    t = soup.new_tag("table")
    head, vals = soup.new_tag("tr"), soup.new_tag("tr")
    for c in cells:
        th = soup.new_tag("th")
        th.string = text(c.select_one(".sg-name"))
        head.append(th)
        td = soup.new_tag("td")
        val = text(c.select_one(".sg-val"))
        note = c.select_one(".sg-tag") or c.select_one(".sg-sub")
        b = soup.new_tag("strong")
        b.string = val
        td.append(b)
        if note:
            td.append(soup.new_tag("br"))
            td.append(text(note))
        vals.append(td)
    t.append(head)
    t.append(vals)
    return t


def convert(el, soup, art):
    """Rewrite one GM-layer fragment in place into Foundry-friendly HTML."""
    for sel in STRIP:
        for x in el.select(sel):
            x.decompose()
    # links: keep the words, drop the link (they point at the website)
    for a in el.find_all("a"):
        a.unwrap()
    for img in el.find_all("img"):
        src = art.src(img.get("src", ""))
        if src:
            img["src"] = src
            for k in ("style", "loading", "class"):
                img.attrs.pop(k, None)
        else:
            img.decompose()
    for g in el.select(".stat-grid"):
        g.replace_with(grid_table(g, soup))
    for dl in el.select("dl.npc-sheet"):
        frag = soup.new_tag("div")
        for dt in dl.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            p = soup.new_tag("p")
            s = soup.new_tag("strong")
            s.string = text(dt) + ": "
            p.append(s)
            if dd:
                for c in list(dd.contents):
                    p.append(c)
            frag.append(p)
        dl.replace_with(frag)
    for ra in el.select(".read-aloud"):
        label = ra.select_one(".read-aloud-label")
        bq = soup.new_tag("blockquote")
        lp = soup.new_tag("p")
        em = soup.new_tag("strong")
        em.string = re.sub(r"\s*·\s*draft$", "", text(label)) if label else "Read Aloud"
        lp.append(em)
        bq.append(lp)
        body = ra.select_one(".read-aloud-text") or ra
        for c in list(body.contents):
            bq.append(c)
        ra.replace_with(bq)
    for sec in el.select(".gm-secret"):
        btn = sec.select_one(".gm-secret-toggle")
        box = soup.new_tag("section", attrs={"class": "secret"})
        h = soup.new_tag("p")
        s = soup.new_tag("strong")
        s.string = text(btn) if btn else "GM Secret"
        h.append(s)
        box.append(h)
        body = sec.select_one(".gm-secret-body") or sec
        for c in list(body.contents):
            box.append(c)
        sec.replace_with(box)
    for note in el.select(".gm-note"):
        label = note.select_one(".gm-note-label")
        frag = soup.new_tag("div")
        if label:
            h = soup.new_tag("h4")
            h.string = text(label)
            frag.append(h)
            label.decompose()
        for c in list(note.contents):
            frag.append(c)
        note.replace_with(frag)
    for cls, tag in ((".beat", "h3"), (".statblock-name", "h4"), (".place-name", "h3"),
                     (".exp-label", "h4"), (".scene-kind", "p"), (".statblock-meta", "p"),
                     (".numbers-note", "p"), (".npc-summary", "p"), (".npc-role", "p"),
                     (".check-head", "h4"), (".chapter-end", "h3")):
        for x in el.select(cls):
            new = soup.new_tag(tag)
            if tag == "p":
                i = soup.new_tag("em")
                i.string = text(x)
                new.append(i)
            else:
                new.string = text(x)
            x.replace_with(new)
    # a skill check: the DC line in italics, then one paragraph per degree
    for x in el.select(".check-dc"):
        x.name = "p"
        x.attrs = {}
        em = soup.new_tag("em")
        for c in list(x.contents):
            em.append(c)
        x.append(em)
    for x in el.select(".deg"):
        x.name = "p"
        x.attrs = {}
    for meta in el.select(".scene-meta"):
        p = soup.new_tag("p")
        s = soup.new_tag("strong")
        s.string = "Cast: "
        p.append(s)
        p.append(" · ".join(text(x) for x in meta.select(".pill")))
        meta.replace_with(p)
    # flatten the remaining layout divs and spans
    for d in el.find_all(["div", "span", "figure"]):
        d.unwrap()
    for fc in el.find_all("figcaption"):
        fc.name = "p"
    html = el.decode_contents(formatter="html5")   # <img>, <br>: no XHTML slash, as Foundry stores them
    html = re.sub(r"\n\s*\n+", "\n", html)
    return html.strip()


def chapter_pages(path, soup_page, art, title_prefix=""):
    soup = soup_page
    pages = []
    cont = soup.select_one(".gm-container") or soup
    for sec in cont.find_all("div", class_="section", recursive=False):
        title = sec.select_one(".section-title")
        if not title:
            continue
        name = text(title)
        title.decompose()
        places = sec.select(".place")
        place_pages = []
        for pl in places:
            pname = text(pl.select_one(".place-name"))
            where = pl.select_one(".place-where")
            keeper = pl.select_one(".place-keeper")
            head = soup.new_tag("p")
            em = soup.new_tag("em")
            em.string = (text(where) if where else "") + (f" · kept by {text(keeper)}" if keeper else "")
            head.append(em)
            pl.select_one(".place-head").replace_with(head)
            city = {"freeboard": "Freeboard", "mooring": "Skysail"}.get(sec.get("id"), name)
            place_pages.append({"name": f"{city} · {pname}",
                                "type": "text", "html": convert(pl, soup, art)})
            pl.decompose()
        pages.append({"name": name, "type": "text", "html": convert(sec, soup, art)})
        pages += place_pages
    return pages


def cast_pages(path, art):
    soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
    pages = []
    for sec in soup.select(".gm-container > .section"):
        t = sec.select_one(".section-title")
        if not t or not sec.select(".npc-card"):
            continue
        faction = text(t)
        for card in sec.select(".npc-card"):
            name = text(card.select_one(".npc-name"))
            portrait = card.select_one(".npc-face")
            parts = []
            if portrait:
                src = art.src(portrait["src"])
                if src:
                    parts.append(f'<p><img src="{src}" width="320"></p>')
            parts.append(f"<p><em>{faction}</em></p>")
            role = card.select_one(".npc-role")
            summ = card.select_one(".npc-summary")
            if role:
                parts.append(f"<p><strong>{text(role)}</strong></p>")
            if summ and text(summ):
                parts.append(f"<p><em>{text(summ)}</em></p>")
            body = card.select_one(".npc-body")
            for appears in body.select("p.todo"):
                appears.decompose()
            parts.append(convert(body, soup, art))
            pages.append({"name": name, "type": "text", "html": "\n".join(parts)})
    return pages


def view_pages(spec_path, art):
    spec = json.load(open(spec_path, encoding="utf-8"))
    d = os.path.dirname(spec_path)
    pages = []
    for key, shot in spec["shots"].items():
        for ext in (".png", ".webp", ".jpg"):
            f = os.path.join(d, shot["file"] + ext)
            if os.path.isfile(f):
                rel = os.path.relpath(f, art.quest_dir)
                pages.append({"name": key.replace("-", " ").title(), "type": "image",
                              "src": art.src(rel), "caption": ""})
                break
    return pages


def main():
    ap = argparse.ArgumentParser(description="Turn a quest's GM pages into a Foundry journal spec and macro.")
    ap.add_argument("--quest", required=True, help="The quest folder under published/gm-notes/.")
    ap.add_argument("--folder", required=True, help="The JournalEntry folder in Foundry.")
    ap.add_argument("--chapter", action="append", default=[], metavar="TITLE=page.html",
                    help="A scene page as one journal. Repeatable.")
    ap.add_argument("--cast", help="The cast page: one journal page per NPC.")
    ap.add_argument("--views", help="An art spec of place views: one image page per rendered shot.")
    ap.add_argument("--views-title", default="Views")
    ap.add_argument("--campaign", required=True, help="Repo campaign slug (campaigns.json gives the world).")
    ap.add_argument("--sub", required=True, help="Upload folder under the world's assets/.")
    ap.add_argument("--stage", required=True, help="Local folder the .webp art is staged into.")
    ap.add_argument("--replace", action="store_true",
                    help="Delete and rebuild same-named journals (loses edits made in Foundry). Default: add missing pages only.")
    ap.add_argument("--spec", help="Write the journal spec JSON here.")
    ap.add_argument("--macro", help="Write the Foundry macro here.")
    a = ap.parse_args()

    world = world_for(a.campaign)
    if not world:
        sys.exit(f"Campaign {a.campaign} has no Foundry world in campaigns.json.")
    art = Art(os.path.abspath(a.quest), a.stage, f"worlds/{world}/assets/{a.sub.strip('/')}/")
    journals = []
    for raw in a.chapter:
        title, _, page = raw.partition("=")
        p = os.path.join(a.quest, page)
        soup = BeautifulSoup(open(p, encoding="utf-8").read(), "html.parser")
        journals.append({"name": f"{a.folder} · {title}", "pages": chapter_pages(p, soup, art)})
    if a.cast:
        journals.append({"name": f"{a.folder} · Cast", "pages": cast_pages(os.path.join(a.quest, a.cast), art)})
    if a.views:
        vp = view_pages(os.path.join(a.quest, a.views), art)
        if vp:
            journals.append({"name": f"{a.folder} · {a.views_title}", "pages": vp})
    spec = {"folder": a.folder, "mode": "replace" if a.replace else "add", "journals": journals}
    for j in journals:
        print(f"{j['name']}: {len(j['pages'])} pages", file=sys.stderr)
    print(f"Staged {len(art.staged)} image(s) in {a.stage}", file=sys.stderr)
    if a.spec:
        json.dump(spec, open(a.spec, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if a.macro:
        m = foundry_macro.make_journal_macro(spec)
        open(a.macro, "w", encoding="utf-8").write(m)
        print(f"Wrote {a.macro} ({len(m)} chars).", file=sys.stderr)


if __name__ == "__main__":
    main()
