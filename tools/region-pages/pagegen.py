"""Shared helpers for the region-page generators.

Each build_<slug>.py turns a region's lore deep file (and its in-world document)
into its published Style B page, so the page cannot drift from the lore. Run a
builder from the repository root:

    python3 tools/region-pages/build_<slug>.py

Call use(lore_path, doc_path) first; it loads both files and returns them as
(L, T) for the builder's own slicing. The helpers below read the loaded files.
"""
import re, html

L = ''
T = ''

def use(lore_path, doc_path):
    global L, T
    L = open(lore_path).read()
    T = open(doc_path).read()
    return L, T

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    t = re.sub(r'\[`?([^\]`]+)`?\]\([^)]+\)', r'\1', t)
    return t

def section(title):
    i = L.index('\n## ' + title + '\n'); j = L.find('\n## ', i + 5)
    return L[i + len(title) + 5: j if j != -1 else len(L)]

def field(name):
    m = re.search(r'^\*\*' + re.escape(name) + r':\*\* (.+)$', L, re.M); return m.group(1)

def body(block):
    """paragraphs before the first #### box; quotes and bullets skipped"""
    k = block.find('\n#### ')
    b = block if k == -1 else block[:k]
    return [c.strip() for c in b.strip().split('\n\n') if c.strip() and c.strip() != '---' and not c.strip().startswith('>') and not c.strip().startswith('- ')]

def quote(block, start):
    for chunk in block.split('\n\n'):
        if chunk.strip().startswith('>') and start in chunk:
            return [l[2:] if l.startswith('> ') else l[1:] for l in chunk.strip().split('\n')]
    raise KeyError(start)

def vq(lines):
    body_, att = lines[:-1], lines[-1]
    ps = ''.join('<p>%s</p>' % inline(l) for l in body_ if l.strip())
    return '  <div class="voice-quote">%s</div>\n  <div class="voice-attrib">%s</div>\n' % (ps, inline(att))

def prose(ps):
    return '  <div class="prose">\n' + ''.join('    <p>%s</p>\n' % inline(p) for p in ps) + '  </div>\n'

def box(block, head):
    i = block.index(head); rest = block[i + len(head):]
    ends = [x for x in (rest.find('\n## '), rest.find('\n#### ')) if x != -1]
    rest = rest[:min(ends)] if ends else rest
    return [p.strip() for p in rest.strip().split('\n\n') if p.strip()]

def belief(title, label, paras):
    return ('  <div class="legend-era">\n    <button class="legend-era-toggle" onclick="toggleEraLegend(event, this)">◈ &nbsp; Popular Belief · %s</button>\n'
            '    <div class="legend-era-content">\n      <div class="legend-era-label">◈ &nbsp; %s</div>\n%s    </div>\n  </div>\n') % (
        title, label, ''.join('      <p>%s</p>\n' % inline(p) for p in paras))

def secret(title, label, paras):
    return ('  <div class="secret-era">\n    <button class="secret-era-toggle" onclick="toggleEraSecret(event, this)">⚿ &nbsp; GM Secret · %s</button>\n'
            '    <div class="secret-era-content">\n      <div class="secret-era-label">⚿ &nbsp; %s</div>\n%s    </div>\n  </div>\n') % (
        title, label, ''.join('      <p%s>%s</p>\n' % (' style="margin-top:0;"' if n == 0 else '', inline(p)) for n, p in enumerate(paras)))

def panel(label, text):
    return '  <div class="feature-panel prose">\n    <div class="panel-label">%s</div>\n    <p style="margin-bottom:0;">%s</p>\n  </div>\n' % (label, inline(text))

def lead_cards(ps):
    out = '  <div class="card-grid life-grid">\n'
    for p in ps:
        m = re.match(r'\*\*(.+?)\.\*\* ', p)
        out += '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (m.group(1), inline(p[m.end():]))
    return out + '  </div>\n'

def strip_lead(p):
    return re.sub(r'^\*\*.+?\.\*\* ', '', p)

def lead_name(p):
    return re.match(r'\*\*(.+?)\.\*\* ', p).group(1)

def log_card(key, summary, body_html):
    return ('    <div class="log-letter"><button class="log-letter-head" aria-expanded="false" onclick="var c=this.parentNode;c.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',c.classList.contains(\'open\'))">'
            '<span class="ld-date">%s</span><span class="ld-text">%s</span><span class="expand-hint">Tap ▾</span></button><div class="log-letter-body">%s</div></div>\n') % (key, html.escape(summary), body_html)

DIV = '  <div class="divider"><div class="div-line"></div><div class="div-glyph">✦</div><div class="div-line"></div></div>\n\n'
