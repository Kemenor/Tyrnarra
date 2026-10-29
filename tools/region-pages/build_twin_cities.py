"""The Twin Cities page, generated from lore/geography/askamira/twin-cities.md and
Vyrenna's column in twin-cities-column.md. Run from the repository root.

The lore file nests its sections (### subsections, ◈ and ⚿ at ### or ####), so
this builder walks each section's blocks in order instead of using body()."""
import re, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagegen import *
L, T = use('lore/geography/askamira/twin-cities.md', 'lore/geography/askamira/twin-cities-column.md')

def clean(t):
    """drop file references and lore-side carry-over notes, which stay off the page"""
    t = re.sub(r'\[`?([^\]`]+)`?\]\([^)]+\)', r'\1', t)
    t = re.sub(r' ?\((?:see )?[^()]*\.md[^()]*\)', '', t)
    t = re.sub(r'^Carried over unchanged from .*?: ', '', t)
    return t[0].upper() + t[1:] if t else t

def ill(t):
    return inline(clean(t))

BOX_LABELS = {
    'the islets are Elden ships': 'What Holds Skysail Up',
    'Ninehulls, the unkillable': 'What Walks as Ninehulls',
    'the Accommodation': 'The Mail That Is Never Taken',
    'the lure': 'What the Quays Say',
    'the broken-chain man drinks in Freeboard': 'What the Taverns Say',
}

def render(block):
    """quotes, prose, ### subheads, and ◈ / ⚿ boxes, in the order the lore gives them"""
    out = ''
    chunks = [c.strip() for c in block.strip().split('\n\n') if c.strip() and c.strip() != '---']
    i = 0
    while i < len(chunks):
        c = chunks[i]
        h = re.match(r'^#{3,4} (.+)$', c)
        if h:
            head = h.group(1)
            m = re.match(r'(⚿ GM Secret|◈ Popular Belief): (.+)$', head)
            if m:
                paras = []
                i += 1
                while i < len(chunks) and not chunks[i].startswith('#'):
                    paras.append(clean(chunks[i])); i += 1
                title = m.group(2)
                label = BOX_LABELS[title]
                out += (secret if m.group(1).startswith('⚿') else belief)(title[0].upper() + title[1:], label, paras)
                continue
            out += '  <h3 class="sub-heading">%s</h3>\n' % html.escape(head)
        elif c.startswith('>'):
            lines = [l[2:] if l.startswith('> ') else l[1:] for l in c.split('\n')]
            lines = [l for l in lines if l.strip()]
            out += vq(lines)
        elif c.startswith('- '):
            out += '  <ul class="prose-list">\n' + ''.join('    <li>%s</li>\n' % ill(l[2:]) for l in c.split('\n')) + '  </ul>\n'
        else:
            out += '  <div class="prose"><p>%s</p></div>\n' % ill(c)
        i += 1
    return out

freeboard_html = render(section('Freeboard'))
skysail_html = render(section('Skysail and the Mooring'))
articles_html = render(section('The articles and the Lords'))
trade_html = render(section('Colours and the trade'))
daily_html = render(section('Daily life'))
d6 = section('Whose colours')
tension_html = vq(quote(d6, 'One pennant')) + panel('Live Tension · Whose Colours', clean(body(d6)[0]))

nm = section('What a Freeboarder is called'); nmp = body(nm); samp = nmp[-1]
def pills(label, s_, first=False):
    items = [x.strip().strip('.') for x in s_.split(', *')]
    items = [x if x.startswith('*') else '*' + x for x in items]
    return '    <p style="margin:%s 0 6px;"><b>%s</b></p>\n    <div class="pill-row">%s</div>\n' % ('0' if first else '14px', label, ''.join('<span class="pill">%s</span>' % inline(x) for x in items))
un = re.search(r'Untold: (.+?)\. Told:', samp).group(1); told = re.search(r'Told: (.+?)\. Lords:', samp).group(1); lords = re.search(r'Lords: (.+?)\.$', samp).group(1)
names_html = prose(nmp[:-1]) + '  <div class="feature-panel">\n    <div class="panel-label">Sample Names</div>\n' + \
    pills('Untold', un, True) + pills('Told', told) + pills('Lords', lords) + '  </div>\n'

fig = L[L.index('## Named figures'):L.index('## Voices')]
figs = [l[2:] for l in fig.split('\n') if l.startswith('- ')]
def figcard(x):
    m = re.match(r'\*\*(.+?)\*\*: (.*)$', x)
    r_ = ill(m.group(2))
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_[0].upper() + r_[1:])
fig_html = '  <div class="card-grid figure-grid">\n' + ''.join(figcard(x) for x in figs) + '  </div>\n'

# The column, one card per part, the Guide's line first
gm = re.search(r'\*\*Golivander Tessek, \*A Traveller.s Guide to Tyrnarra\*:\*\*\n\n((?:>.*\n)+)', T)
glines = [l[2:] if l.startswith('> ') else l[1:] for l in gm.group(1).strip().split('\n')]
guide_ps = [l.strip('*') for l in glines if l.strip()]
col = T[T.index('**Finding it.**'):]
keys = ['Finding it', 'Under the hulls', 'The vote', 'The bilges', 'The sky comes home', 'Up', 'The last day']
parts = re.split(r'\n\n(?=\*\*(?:%s)\.\*\*)' % '|'.join(re.escape(k) for k in keys), col)
summaries = {'Finding it': 'Nine days of the wrong water, then an island with a storm sitting on it.',
             'Under the hulls': 'The gangway becomes a street, the tavern four hulls tall, bread at three in the morning, a barber with two touches.',
             'The vote': 'The Lower Spar votes out its captain over a leaking roof.',
             'The bilges': 'A window in a drowned hull, and a face on the other side.',
             'The sky comes home': 'Skarrenn on the fifth day; four islands in the air on the eighth, and rain out of a clear sky.',
             'Up': 'A basket, the brightest place she has stood, and a city the wind plays.',
             'The last day': 'The islands lean into the wind, and an old pirate on the quay explains Frae City.'}
column_html = ('  <div class="prose"><p>Vyrenna Tessek\'s column from the Twin Cities, in the Talan years of <i>One Line Further</i>, 2527 MR, opened by the line her grand-uncle\'s Guide gave them.</p></div>\n'
               '  <div class="voice-quote">%s</div>\n  <div class="voice-attrib">Golivander Tessek, <i>A Traveller\'s Guide to Tyrnarra</i></div>\n  <div class="log-letters">\n') % ''.join('<p>%s</p>' % inline(p) for p in guide_ps)
assert len(parts) == len(keys)
for pt in parts:
    m = re.match(r'\*\*(.+?)\.\*\* ', pt); key = m.group(1)
    body_ = ''.join('<p>%s</p>' % inline(c.strip()) for c in pt[m.end():].split('\n\n') if c.strip())
    column_html += log_card(html.escape(key), summaries[key], body_)
column_html += '  </div>\n'

etym = field('Etymology').replace(' (Derivations in the glossary.)', '')
pos = field('Position'); cities = field('The cities'); peop = field('Peoples'); tongue = field('Tongue'); faith = field('Faith'); rule = field('Rule'); founded = field('Founded'); char = field('Character')
cap1 = lambda t: t[0].upper() + t[1:]
page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Twin Cities · Askamira · Tyrnarra</title>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/setting/assets/style-b.css">
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
<script defer src="/setting/assets/site-interactions.js"></script>
<style>
  :root {
    --domain-accent: #e0915c;   /* lantern copper · 7.78:1 on Style B bg */
    --card-bg: rgba(28,20,14,0.55);
  }
  .voice-quote { max-width: 780px; margin: 20px auto; padding: 18px 24px; background: var(--card-bg); border-left: 3px solid var(--domain-accent); border-radius: 0 4px 4px 0; font-style: italic; line-height: 1.65; }
  .voice-quote p { margin: 0 0 12px; }
  .voice-quote p:last-child { margin-bottom: 0; }
  .voice-attrib { max-width: 780px; margin: -10px auto 22px; text-align: right; font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--domain-accent); }
  .sub-heading { max-width: 780px; margin: 30px auto 6px; font-family: 'Cinzel', serif; font-size: 1.02rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--domain-accent); font-weight: 600; }
  .prose-list { max-width: 780px; margin: 0 auto 16px; line-height: 1.65; }
  .figure-grid { --col-min: 230px; --grid-gap: 16px; --card-pad: 18px 20px; }
  .figure-grid .card-name { font-size: 1.05rem; letter-spacing: 0.06em; margin-bottom: 8px; color: var(--domain-accent); }
  .panel-label { font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--domain-accent); margin-bottom: 10px; }
  .two-cities { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; max-width: 780px; margin: 0 auto 10px; }
  @media (max-width: 600px) { .two-cities { grid-template-columns: 1fr; } }
</style>
</head>
<body data-page="twin-cities">

<div class="container">

  <div class="breadcrumb">
    <a href="/setting/index.html">Tyrnarra</a><span class="sep">›</span><a href="/setting/talan/talan.html">Talan</a><span class="sep">›</span><a href="/setting/talan/domains/askamira/askamira.html">Askamira</a><span class="sep">›</span><span>The Twin Cities</span>
  </div>

  <div class="header">
    <div class="header-ornament">✦ · ✦ · ✦</div>
    <div class="page-title">The Twin Cities</div>
    <div class="page-subtitle">The Midarra · Freeboard and Skysail · The Pirate Capital</div>
    <div class="page-flavor">''' + inline(cap1(char)) + '''</div>
  </div>

''' + DIV + '''  <h2 id="at-a-glance" class="section-heading">At a Glance</h2>
  <dl class="facts">
    <dt>Etymology</dt><dd>''' + ill(etym) + '''</dd>
    <dt>Position</dt><dd>''' + ill(pos) + '''</dd>
    <dt>The Cities</dt><dd>''' + ill(cities) + '''</dd>
    <dt>Character</dt><dd>
      <i>''' + inline(cap1(char)) + '''</i><br>
      <div class="pill-row" style="margin-top:6px"><span class="pill">Freeboard</span><span class="pill">Skysail</span><span class="pill">The Mooring</span><span class="pill">The Articles</span><span class="pill">The Pirate Lords</span><span class="pill">Colours</span></div>
    </dd>
    <dt>Peoples</dt><dd>''' + ill(peop) + '''</dd>
    <dt>Tongue</dt><dd>''' + ill(tongue) + '''</dd>
    <dt>Faith</dt><dd>''' + ill(faith) + '''</dd>
    <dt>Rule</dt><dd>''' + ill(rule) + '''</dd>
    <dt>Founded</dt><dd>''' + ill(founded) + '''</dd>
  </dl>

  <div class="two-cities">
    <div class="gods-city" style="border-color: rgba(224,145,92,0.5); margin:0;">
      <div class="gods-city-label">On the Water</div>
      <div class="gods-city-name">Freeboard</div>
      <div class="gods-city-byname">The Stack · hulls on hulls under lantern-light · the ring, the spires, the bilges</div>
    </div>
    <div class="gods-city" style="border-color: rgba(224,145,92,0.5); margin:0;">
      <div class="gods-city-label">In the Air</div>
      <div class="gods-city-name">Skysail</div>
      <div class="gods-city-byname">The Fore, the Main, the Mizzen, the Jigger · four islets on old work, airships on the lines</div>
    </div>
  </div>

''' + DIV + '''  <h2 id="freeboard" class="section-heading">Freeboard</h2>

''' + freeboard_html + '\n' + DIV + '''  <h2 id="skysail" class="section-heading">Skysail and the Mooring</h2>

''' + skysail_html + '\n' + DIV + '''  <h2 id="the-articles" class="section-heading">The Articles and the Lords</h2>

''' + articles_html + '\n' + DIV + '''  <h2 id="colours" class="section-heading">Colours and the Trade</h2>

''' + trade_html + '\n' + DIV + '''  <h2 id="daily-life" class="section-heading">Daily Life</h2>

''' + daily_html + '\n' + DIV + '''  <h2 id="whose-colours" class="section-heading">Whose Colours</h2>

''' + tension_html + '\n' + DIV + '''  <h2 id="names" class="section-heading">What a Freeboarder Is Called</h2>
''' + names_html + '\n' + DIV + '''  <h2 id="figures" class="section-heading">Named Figures</h2>
''' + fig_html + '\n' + DIV + '''  <h2 id="the-column" class="section-heading">One Line Further: the Twin Cities</h2>
''' + column_html + '\n' + DIV + '''  <div class="see-also">
    <h3>Continue Reading</h3>
    <ul>
      <li><a href="/setting/talan/domains/askamira/askamira.html"><b>Askamira →</b></a> · The Freedom domain, whose island the cities' usual waters surround.</li>
      <li><a href="/setting/talan/domains/askamira/frae-city/frae-city.html"><b>Frae City →</b></a> · The first free city, on the same crossing, free in its god's name.</li>
      <li><a href="/setting/talan/domains/floteyn/floating-isles/floating-isles.html"><b>The Floating Isles →</b></a> · The Sweetwater League, whose mail sails through pirate water.</li>
      <li><a href="/setting/talan/domains/zuzental/legea-empire.html"><b>The Legea Empire →</b></a> · The book that wrote a fleet, and then the terms for colours.</li>
      <li><a href="/setting/talan/transport.html"><b>Transport →</b></a> · The Midarra crossing, and the share the Pirate Lords take of it.</li>
    </ul>
  </div>

  <div class="open-canon">
    <h3>⌬ &nbsp; Open in the Chronicle Record</h3>
    <div class="sub">What the chronicle has not yet set down about the two cities.</div>
    <ol>
      <li><b>The sky Lords.</b> What marks a Lord on Skysail, where Freeboard's Lords have their spires.</li>
      <li><b>The decks.</b> Freeboard's decks and promenades by name, beyond the Lower Spar.</li>
      <li><b>The Lords.</b> The Pirate Lords beyond the four the chronicle names.</li>
      <li><b>The wax harbour.</b> The harbour on the Legean half of Hringseyja, by name, and its governor.</li>
      <li><b>The Legedi's lines.</b> The two lines on pirates, in full.</li>
      <li><b>The engines.</b> What drives Freeboard, kind by kind.</li>
    </ol>
  </div>

  <div class="footer">TYRNARRA · TALAN · ASKAMIRA · THE TWIN CITIES</div>

</div>

</body>
</html>
'''
os.makedirs('published/setting/talan/domains/askamira/twin-cities', exist_ok=True)
open('published/setting/talan/domains/askamira/twin-cities/twin-cities.html', 'w').write(page)
print('written', len(page))
