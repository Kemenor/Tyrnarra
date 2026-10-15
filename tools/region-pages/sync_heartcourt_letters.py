"""Sync the Letters from Biozuri on the Heartcourt and Emarrea pages from the lore file.

Both pages are hand-built; only the body of each `.golivander-letter` block
is replaced, matched by its letter-title, from lore/geography/lautara/heartcourt-letters.md.
Titles, attributions and everything else on the page are left alone. Run from the
repository root, optionally naming the column numbers to sync:

    python3 tools/region-pages/sync_heartcourt_letters.py 0 1 2
"""
import re, html, sys

LORE = 'lore/geography/lautara/heartcourt-letters.md'
PAGES = ['published/setting/talan/domains/lautara/emarrea/heartcourt.html',
         'published/setting/talan/domains/lautara/emarrea/emarrea.html']

def md_inline(t):
    t = t.strip()
    if t.startswith('*') and t.endswith('*') and not t.startswith('**'):
        t = t[1:-1]
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t

def columns():
    s = open(LORE).read()
    out = {}
    for m in re.finditer(r'^## Column (\d+) · (.+)$', s, re.M):
        n, title = int(m.group(1)), m.group(2).strip()
        start = m.end()
        end = s.index('\n– *G.', start)
        body = s[start:end].strip().split('\n\n')
        chunks = [c for c in body if c.strip() and not c.strip().startswith('*(')]
        out[n] = (title, chunks)
    return out

def render(chunks):
    out = []
    for c in chunks:
        lines = c.strip().split('\n')
        if all(l.startswith('>') for l in lines):
            verse = '<br>'.join(md_inline(l.lstrip('> ').strip()) for l in lines)
            out.append('<blockquote>%s</blockquote>' % verse)
        else:
            out.append('<p>%s</p>' % md_inline(' '.join(lines)))
    return out

def strip_tags(t):
    return re.sub(r'<[^>]+>', '', t).strip()

def main(nums):
    cols = columns()
    pages = {p: open(p).read() for p in PAGES}
    for n in nums:
        title, chunks = cols[n]
        hit = None
        for PAGE, page in pages.items():
            for b in re.finditer(r'<div class="golivander-letter">(.*?)\n(\s*)</div>', page, re.S):
                t = re.search(r'<div class="letter-title">(.*?)</div>', b.group(1), re.S)
                if t and strip_tags(t.group(1)).split('<br>')[0].startswith(title[:30]):
                    hit = b; break
            if hit: break
        if hit is None:
            raise SystemExit('no page letter for column %d: %s' % (n, title))
        inner = hit.group(1)
        head = re.search(r'\s*<div class="letter-title">.*?</div>', inner, re.S)
        attrib = re.search(r'\s*<div class="attribution">.*?</div>', inner, re.S)
        indent = re.match(r'\s*', inner[head.end():]).group(0) or '\n      '
        body = ''.join(indent + x for x in render(chunks))
        new_inner = inner[:head.end()] + body + attrib.group(0)
        pages[PAGE] = page[:hit.start(1)] + new_inner + page[hit.end(1):]
        print('synced column', n, '->', PAGE.rsplit('/', 1)[-1])
    for p, page in pages.items():
        open(p, 'w').write(page)

if __name__ == '__main__':
    main([int(x) for x in sys.argv[1:]] or sorted(columns()))
