"""The Hareaveldi page, generated from lore/geography/lioaru/hareaveldi.md and the
order book in hareaveldi-order-book.md. Run from the repository root."""
import re, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagegen import *
L, T = use('lore/geography/lioaru/hareaveldi.md', 'lore/geography/lioaru/hareaveldi-order-book.md')

d1 = section('The desert of colours'); p1 = body(d1)
colours_html = vq(quote(d1, 'green here')) + prose(p1[0:2]) + panel('Arghavan', strip_lead(p1[2]))
d2 = section('Everyone paints'); p2 = body(d2)
paint_html = vq(quote(d2, 'The WINDOWS')) + prose(p2[0:1]) + panel('The Window Right', strip_lead(p2[1]))
d3 = section('The rangzar and the carrying-out'); p3 = body(d3)
rang_html = vq(quote(d3, 'kettle')) + prose(p3[0:1]) + lead_cards(p3[1:3]) + prose(p3[3:])
d4 = section('The elham and the great painters'); p4 = body(d4)
elham_html = prose(p4) + belief('The Elham Is the Child', 'What the Folk Say', box(d4, '#### ◈ Popular Belief: the elham is the child looking through you')) + \
    secret('The Pull', 'As Hard as the Painter Reached', box(d4, '#### ⚿ GM Secret: the pull'))
d5 = section('The shed crown'); p5 = body(d5)
crown_html = vq(quote(d5, 'I painted what was there')) + prose(p5[0:2]) + lead_cards(p5[2:6]) + panel("Live Tension · The Tajvar's Portrait", strip_lead(p5[6]))
d6 = section('Trade and the roads'); p6 = body(d6)
trade_html = prose(p6)
dl = section('Daily life'); head = '#### ◈ Popular Belief: a kept self lingers'
before = dl[:dl.index(head)]; after = dl[dl.index(head)+len(head):]
after_ps = [p.strip() for p in after.strip().split('\n\n') if p.strip()]
daily_html = prose([p for p in before.strip().split('\n\n') if p.strip()]) + belief('A Kept Self Lingers', 'What Mothers Say', after_ps[0:1]) + lead_cards(after_ps[1:])
tongue_html = prose(body(section('The tongue')))
nm = section('What a Hareaveldi is called'); nmp = body(nm); samp = nmp[-1]
def pills(label, s_, first=False):
    items = [x.strip().strip('.') for x in s_.split(',')]
    return '    <p style="margin:%s 0 6px;"><b>%s</b></p>\n    <div class="pill-row">%s</div>\n' % ('0' if first else '14px', label, ''.join('<span class="pill">%s</span>' % html.escape(x) for x in items))
g = re.search(r'Given: (.+?)\. Self-names:', samp).group(1); sn = re.search(r'Self-names: (.+?)\. Families:', samp).group(1); fa = re.search(r'Families: (.+?)\. Whole:', samp).group(1)
wholes = [x.strip() for x in re.search(r'Whole: (.+)$', samp).group(1).split('·')]
names_html = prose(nmp[:-1]) + '  <div class="feature-panel">\n    <div class="panel-label">Sample Names</div>\n' + pills('Given', g, True) + pills('Self-names', sn) + pills('Families', fa) + \
    '    <p style="margin:14px 0 6px;"><b>Whole names</b></p>\n    <div class="pill-row">%s</div>\n  </div>\n' % ''.join('<span class="pill">%s</span>' % inline(x) for x in wholes)
fig = L[L.index('## Named figures'):L.index('## Voices')]
figs = [l[2:] for l in fig.split('\n') if l.startswith('- ')]
def figcard(x):
    m = re.match(r'\*\*(.+?)\*\*,? ?:? ?(.*)$', x); r_ = inline(m.group(2)); r_ = r_[0].upper() + r_[1:]
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_)
fig_html = '  <div class="card-grid figure-grid">\n' + ''.join(figcard(x) for x in figs) + '  </div>\n'

# the order book, one card per day, tables rendered
bk = T[T.index('**First day'):]
days = re.split(r'\n(?=\*\*(?:First|Third|Fifth|Sixth|Seventh) day)', bk)
def md_table(block):
    rows = [r.strip().strip('|').split('|') for r in block.strip().split('\n') if r.strip().startswith('|')]
    head_, body_ = rows[0], [r for r in rows[2:]]
    t = '<table class="ledger"><tr>' + ''.join('<th>%s</th>' % inline(c.strip()) for c in head_) + '</tr>'
    for r in body_: t += '<tr>' + ''.join('<td>%s</td>' % inline(c.strip()) for c in r) + '</tr>'
    return t + '</table>'
def day_body(txt):
    out = ''
    for c in [c.strip() for c in txt.split('\n\n') if c.strip()]:
        if c.startswith('|'): out += md_table(c)
        else: out += '<p>%s</p>' % inline(c)
    return out
summaries = {'First': 'Panjrang from the air, five oases and five colours; the street of windows.',
             'Third': 'Sabzab: the green worth weeping over, and painted bowls.',
             'Fifth': 'Lajvard and Sorkhab: the blue that lasts, the red that fades.',
             'Sixth': 'The field outside the east wall at sunrise: the faces, the kettle, the boards.',
             'Seventh': 'One jar of green and one board, not for resale.'}
book_html = '  <div class="prose"><p>The order book Odelind Ringhold Mordant kept on the road in 2531 MR, buying colour for Ringhold. The ledger column is the work; the margins are hers.</p></div>\n  <div class="log-letters">\n'
for dd in days:
    m = re.match(r'\*\*(\w+) day, (.+?)\*\*\n', dd); key = m.group(1); place = m.group(2)
    book_html += log_card(key + ' day', summaries[key], day_body(dd[m.end():]))
book_html += '  </div>\n'

etym = field('Etymology').replace(' (Derivations in the glossary.)', '')
pos = field('Position'); terr = field('Terrain'); peop = field('Peoples'); tongue = field('Tongue'); faith = field('Faith'); rule = field('Rule'); cap = field('Capital'); founded = field('Founded'); char = field('Character')
cap1 = lambda t: t[0].upper() + t[1:]
page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hareaveldi · Lioaru · Tyrnarra</title>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/setting/assets/style-b.css">
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
<script defer src="/setting/assets/site-interactions.js"></script>
<style>
  :root {
    --domain-accent: #8aa6f2;   /* lajvard blue · 8.19:1 on Style B bg */
    --card-bg: rgba(18,22,36,0.55);
  }
  .voice-quote { max-width: 780px; margin: 20px auto; padding: 18px 24px; background: var(--card-bg); border-left: 3px solid var(--domain-accent); border-radius: 0 4px 4px 0; font-style: italic; line-height: 1.65; }
  .voice-quote p { margin: 0 0 12px; }
  .voice-quote p:last-child { margin-bottom: 0; }
  .voice-quote b { font-style: normal; font-family: 'Cinzel', serif; font-size: 0.82em; letter-spacing: 0.12em; color: var(--domain-accent); }
  .voice-attrib { max-width: 780px; margin: -10px auto 22px; text-align: right; font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--domain-accent); }
  .life-grid, .figure-grid { --col-min: 230px; --grid-gap: 16px; --card-pad: 18px 20px; }
  .life-grid .card-name, .figure-grid .card-name { font-size: 1.05rem; letter-spacing: 0.06em; margin-bottom: 8px; color: var(--domain-accent); }
  .panel-label { font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--domain-accent); margin-bottom: 10px; }
  .log-letter-body .ledger { width: 100%; border-collapse: collapse; margin: 6px 0 12px; font-style: normal; font-size: 0.92em; }
  .log-letter-body .ledger th, .log-letter-body .ledger td { border-bottom: 1px solid rgba(138,166,242,0.25); padding: 4px 6px; text-align: left; vertical-align: top; }
  .log-letter-body .ledger th { font-family: 'Cinzel', serif; font-size: 0.75em; letter-spacing: 0.1em; color: var(--domain-accent); }
  .log-letter-body { overflow-x: auto; }
</style>
</head>
<body data-page="hareaveldi">

<div class="container">

  <div class="breadcrumb">
    <a href="/setting/index.html">Tyrnarra</a><span class="sep">›</span><a href="/setting/talan/talan.html">Talan</a><span class="sep">›</span><a href="/setting/talan/domains/lioaru/lioaru.html">Lioaru</a><span class="sep">›</span><span>Hareaveldi</span>
  </div>

  <div class="header">
    <div class="header-ornament">✦ · ✦ · ✦</div>
    <div class="page-title">Hareaveldi</div>
    <div class="page-subtitle">Lioaru Sub-Region · The Sand Realm · The Nagaji Heartland</div>
    <div class="page-flavor">''' + inline(cap1(char)) + '''</div>
  </div>

''' + DIV + '''  <h2 id="at-a-glance" class="section-heading">At a Glance</h2>
  <dl class="facts">
    <dt>Etymology</dt><dd>''' + inline(cap1(etym)) + '''</dd>
    <dt>Position</dt><dd>''' + inline(cap1(pos)) + '''</dd>
    <dt>Terrain</dt><dd>''' + inline(cap1(terr)) + '''</dd>
    <dt>Character</dt><dd>
      <i>''' + inline(cap1(char)) + '''</i><br>
      <div class="pill-row" style="margin-top:6px"><span class="pill">Everyone Paints</span><span class="pill">The Rangzar</span><span class="pill">The Elham</span><span class="pill">The Shed Crown</span><span class="pill">Arghavan</span><span class="pill">Nagaji Heartland</span></div>
    </dd>
    <dt>Peoples</dt><dd>''' + inline(cap1(peop)) + '''</dd>
    <dt>Tongue</dt><dd>''' + inline(cap1(tongue)) + '''</dd>
    <dt>Faith</dt><dd>''' + inline(cap1(faith)) + '''</dd>
    <dt>Rule</dt><dd>''' + inline(cap1(rule)) + '''</dd>
    <dt>Capital</dt><dd>''' + inline(cap1(cap)) + '''</dd>
    <dt>Founded</dt><dd>''' + inline(cap1(founded)) + '''</dd>
  </dl>

  <div class="gods-city" style="border-color: rgba(138,166,242,0.5);">
    <div class="gods-city-label">The Capital</div>
    <div class="gods-city-name">Panjrang</div>
    <div class="gods-city-byname">Five oases in a ring on the south coast · green, blue, red, gold and white · the rangzar outside the east wall</div>
  </div>

''' + DIV + '''  <h2 id="the-desert-of-colours" class="section-heading">The Desert of Colours</h2>

''' + colours_html + '\n' + DIV + '''  <h2 id="everyone-paints" class="section-heading">Everyone Paints</h2>

''' + paint_html + '\n' + DIV + '''  <h2 id="the-rangzar" class="section-heading">The Rangzar and the Carrying-Out</h2>

''' + rang_html + '\n' + DIV + '''  <h2 id="the-elham" class="section-heading">The Elham and the Great Painters</h2>
''' + elham_html + '\n' + DIV + '''  <h2 id="the-shed-crown" class="section-heading">The Shed Crown</h2>

''' + crown_html + '\n' + DIV + '''  <h2 id="trade" class="section-heading">Trade and the Roads</h2>
''' + trade_html + '\n' + DIV + '''  <h2 id="daily-life" class="section-heading">Daily Life</h2>
''' + daily_html + '\n' + DIV + '''  <h2 id="the-tongue" class="section-heading">The Tongue</h2>
''' + tongue_html + '\n' + DIV + '''  <h2 id="names" class="section-heading">What a Hareaveldi Is Called</h2>
''' + names_html + '\n' + DIV + '''  <h2 id="figures" class="section-heading">Named Figures</h2>
''' + fig_html + '\n' + DIV + '''  <h2 id="the-order-book" class="section-heading">The Order Book</h2>
''' + book_html + '\n' + DIV + '''  <div class="see-also">
    <h3>Continue Reading</h3>
    <ul>
      <li><a href="/setting/talan/domains/lioaru/lioaru.html"><b>Lioaru →</b></a> · The Time domain and its three peoples.</li>
      <li><a href="/setting/talan/domains/lautara/emarrea/emarrea.html"><b>Emarrea →</b></a> · Across the northern river, whose court commissions the great painters.</li>
      <li><a href="/setting/talan/domains/lioaru/galdua-jendea/galdua-jendea.html"><b>Galdua Jendea →</b></a> · To the west, the rocks and the salt.</li>
      <li><a href="/setting/talan/domains/nashavel/kaosadaemi/kaosadaemi.html"><b>Kaosadaemi →</b></a> · Ringhold, whose walls buy the colour by the barrel.</li>
      <li><a href="/setting/talan/domains/lioaru/lost-kingdom.html"><b>The Lost Kingdom →</b></a> · Ida, where the tongue of the south-western sands is oldest.</li>
      <li><a href="/setting/talan/ancestries.html"><b>Ancestries →</b></a> · The Nagaji: shed, and whole again.</li>
    </ul>
  </div>

  <div class="open-canon">
    <h3>⌬ &nbsp; Open in the Chronicle Record</h3>
    <div class="sub">What the chronicle has not yet set down about the sand realm.</div>
    <ol>
      <li><b>The oases.</b> The forty-odd others, and the three islands, by name.</li>
      <li><b>The five houses.</b> Their heads.</li>
      <li><b>Roshanak.</b> When she laid the crown down.</li>
      <li><b>The east.</b> What comes out of the Wildreach to the eastern towns.</li>
      <li><b>A new self's debts.</b> Whether a new self answers for an old self's.</li>
    </ol>
  </div>

  <div class="footer">TYRNARRA · TALAN · LIOARU · HAREAVELDI</div>

</div>

</body>
</html>
'''
os.makedirs('published/setting/talan/domains/lioaru/hareaveldi', exist_ok=True)
open('published/setting/talan/domains/lioaru/hareaveldi/hareaveldi.html', 'w').write(page)
print('written', len(page))
