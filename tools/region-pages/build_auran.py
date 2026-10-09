"""The Auran page, generated from lore/geography/lioaru/auran.md and Vyrenna's
column in auran-column.md. Run from the repository root."""
import re, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagegen import *
L, T = use('lore/geography/lioaru/auran.md', 'lore/geography/lioaru/auran-column.md')

# The rains
d1 = section('The rains'); p1 = body(d1)
assert lead_name(p1[2]) == 'The drawing-out' and lead_name(p1[3]) == 'Three rains'
rains_html = vq(quote(d1, 'bell rang from the rim')) + prose(p1[0:2]) + panel('The Drawing-Out', strip_lead(p1[2])) + prose([strip_lead(p1[3])]) + \
    secret("The Elden's Taps", 'What the Craters Are', box(d1, "#### ⚿ GM Secret: the Elden's taps"))

# Siyabask
d2 = section('Siyabask and the one harbour'); p2 = body(d2)
port_html = vq(quote(d2, 'The quay at Siyabask')) + prose(p2)

# The rain-share
d3 = section('The rain-share'); p3 = body(d3)
assert [lead_name(p) for p in p3[1:4]] == ['The bargain', 'The Tolwaja', 'The sundown account']
share_html = prose(p3[0:1]) + panel('The Bargain', strip_lead(p3[1])) + prose([p3[2]]) + panel('The Sundown Account', strip_lead(p3[3])) + \
    belief('Sell a Rain Before It Falls', 'What the Island Says', box(d3, '#### ◈ Popular Belief: sell a rain before it falls'))

# The silver
d4 = section('The silver'); p4 = body(d4)
assert lead_name(p4[2]) == 'The west harbour'
silver_html = vq(quote(d4, 'how many quays')) + prose(p4[0:2]) + panel('Live Tension · The West Harbour', strip_lead(p4[2]))

# Daily life
d5 = section('Daily life'); p5 = body(d5)
assert lead_name(p5[2]) == 'The share-day'
daily_html = prose(p5[0:2]) + panel('The Share-Day', strip_lead(p5[2])) + lead_cards(p5[3:])

hist_html = prose(body(section('Peoples and history')))
tongue_html = prose(body(section('The tongue')))

nm = section('What an Auran is called'); nmp = body(nm); samp = nmp[-1]
def pills(label, s_, first=False):
    items = [x.strip().strip('.') for x in s_.split(',')]
    return '    <p style="margin:%s 0 6px;"><b>%s</b></p>\n    <div class="pill-row">%s</div>\n' % ('0' if first else '14px', label, ''.join('<span class="pill">%s</span>' % html.escape(x) for x in items))
g = re.search(r'Given: (.+?)\. Bowl-names:', samp).group(1); bn = re.search(r'Bowl-names: (.+?)\. Households:', samp).group(1); hh = re.search(r'Households: (.+?)\. Whole:', samp).group(1)
wholes = [x.strip() for x in re.search(r'Whole: (.+)$', samp).group(1).split('·')]
names_html = prose(nmp[:-1]) + '  <div class="feature-panel">\n    <div class="panel-label">Sample Names</div>\n' + pills('Given', g, True) + pills('Bowl-names', bn) + pills('Households', hh) + \
    '    <p style="margin:14px 0 6px;"><b>Whole names</b></p>\n    <div class="pill-row">%s</div>\n  </div>\n' % ''.join('<span class="pill">%s</span>' % inline(x) for x in wholes)

fig = L[L.index('## Named figures'):L.index('## Voices')]
figs = [l[2:] for l in fig.split('\n') if l.startswith('- ')]
def figcard(x):
    m = re.match(r'\*\*(.+?)\*\*,? ?:? ?(.*)$', x)
    rest = re.sub(r' \((?:her|his|their) register in [^)]*\)', ', in <i>One Line Further</i>', m.group(2))
    r_ = inline(rest).replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>'); r_ = r_[0].upper() + r_[1:]
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_)
fig_html = '  <div class="card-grid figure-grid">\n' + ''.join(figcard(x) for x in figs) + '  </div>\n'

# The column, one card per part, the Guide's line first
guide = re.search(r'\*\*Golivander Tessek, \*A Traveller.s Guide to Tyrnarra\*:\*\*\n\n> (.+)\n', T).group(1)
col = T[T.index('**The quay.**'):]
parts = re.split(r'\n\n(?=\*\*(?:The quay|The first gold|Gold again|Starlight|Silver, at last)\.\*\*)', col)
summaries = {'The quay': 'Siyabask, and a quay where nobody looks at the sea.',
             'The first gold': 'Gulgir on its roofs, the boy with his bowl, and a puddle at sundown.',
             'Gold again': 'The neighbour at dusk, the gold ink, a drop in the tea.',
             'Starlight': 'Storngir, six days of waiting, a cold point of light in every drop.',
             'Silver, at last': 'The Durbra, the stills through the night, a vial no longer than a finger.'}
column_html = ('  <div class="prose"><p>Vyrenna Tessek\'s column from Auran, in the Talan years of <i>One Line Further</i>, 2526 MR, opened by the line her grand-uncle\'s Guide gave the island.</p></div>\n'
               '  <div class="voice-quote"><p>%s</p></div>\n  <div class="voice-attrib">Golivander Tessek, <i>A Traveller\'s Guide to Tyrnarra</i></div>\n  <div class="log-letters">\n') % inline(guide.strip('*'))
for pt in parts:
    m = re.match(r'\*\*(.+?)\.\*\* ', pt); key = m.group(1)
    body_ = ''.join('<p>%s</p>' % inline(c.strip()) for c in pt[m.end():].split('\n\n') if c.strip())
    column_html += log_card(html.escape(key), summaries[key], body_)
column_html += '  </div>\n'

etym = field('Etymology').replace(' (Derivations in the glossary.)', '')
pos = field('Position'); terr = field('Terrain'); peop = field('Peoples'); tongue = field('Tongue'); faith = field('Faith'); rule = field('Rule'); cap = field('Capital'); founded = field('Founded'); char = field('Character')
cap1 = lambda t: t[0].upper() + t[1:]
page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auran · Lioaru · Tyrnarra</title>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/setting/assets/style-b.css">
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
<script defer src="/setting/assets/site-interactions.js"></script>
<style>
  :root {
    --domain-accent: #b8c2d4;   /* silfgir silver · 10.87:1 on Style B bg */
    --card-bg: rgba(20,22,28,0.55);
  }
  .voice-quote { max-width: 780px; margin: 20px auto; padding: 18px 24px; background: var(--card-bg); border-left: 3px solid var(--domain-accent); border-radius: 0 4px 4px 0; font-style: italic; line-height: 1.65; }
  .voice-quote p { margin: 0 0 12px; }
  .voice-quote p:last-child { margin-bottom: 0; }
  .voice-attrib { max-width: 780px; margin: -10px auto 22px; text-align: right; font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--domain-accent); }
  .life-grid, .figure-grid { --col-min: 230px; --grid-gap: 16px; --card-pad: 18px 20px; }
  .life-grid .card-name, .figure-grid .card-name { font-size: 1.05rem; letter-spacing: 0.06em; margin-bottom: 8px; color: var(--domain-accent); }
  .panel-label { font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--domain-accent); margin-bottom: 10px; }
</style>
</head>
<body data-page="auran">

<div class="container">

  <div class="breadcrumb">
    <a href="/setting/index.html">Tyrnarra</a><span class="sep">›</span><a href="/setting/talan/talan.html">Talan</a><span class="sep">›</span><a href="/setting/talan/domains/lioaru/lioaru.html">Lioaru</a><span class="sep">›</span><span>Auran</span>
  </div>

  <div class="header">
    <div class="header-ornament">✦ · ✦ · ✦</div>
    <div class="page-title">Auran</div>
    <div class="page-subtitle">Lioaru Sub-Region · The Isle of the Three Rains · The Azarketi Heartland</div>
    <div class="page-flavor">''' + inline(cap1(char)) + '''</div>
  </div>

''' + DIV + '''  <h2 id="at-a-glance" class="section-heading">At a Glance</h2>
  <dl class="facts">
    <dt>Etymology</dt><dd>''' + inline(cap1(etym)) + '''</dd>
    <dt>Position</dt><dd>''' + inline(cap1(pos)) + '''</dd>
    <dt>Terrain</dt><dd>''' + inline(cap1(terr)) + '''</dd>
    <dt>Character</dt><dd>
      <i>''' + inline(cap1(char)) + '''</i><br>
      <div class="pill-row" style="margin-top:6px"><span class="pill">The Three Rains</span><span class="pill">The Drawing-Out</span><span class="pill">The Rain-Share</span><span class="pill">The Tolwaja</span><span class="pill">Cloudship Silver</span><span class="pill">Azarketi Heartland</span></div>
    </dd>
    <dt>Peoples</dt><dd>''' + inline(cap1(peop)) + '''</dd>
    <dt>Tongue</dt><dd>''' + inline(cap1(tongue)) + '''</dd>
    <dt>Faith</dt><dd>''' + inline(cap1(faith)) + '''</dd>
    <dt>Rule</dt><dd>''' + inline(cap1(rule)) + '''</dd>
    <dt>Capital</dt><dd>''' + inline(cap1(cap)) + '''</dd>
    <dt>Founded</dt><dd>''' + inline(cap1(founded)) + '''</dd>
  </dl>

  <div class="gods-city" style="border-color: rgba(184,194,212,0.5);">
    <div class="gods-city-label">The Capital</div>
    <div class="gods-city-name">Siyabask</div>
    <div class="gods-city-byname">On the Bask, the lava arm of the east coast · the one harbour for a Hafra hull · the quay and the sundown account</div>
  </div>

''' + DIV + '''  <h2 id="the-rains" class="section-heading">The Rains</h2>

''' + rains_html + '\n' + DIV + '''  <h2 id="siyabask" class="section-heading">Siyabask and the One Harbour</h2>

''' + port_html + '\n' + DIV + '''  <h2 id="the-rain-share" class="section-heading">The Rain-Share</h2>
''' + share_html + '\n' + DIV + '''  <h2 id="the-silver" class="section-heading">The Silver</h2>

''' + silver_html + '\n' + DIV + '''  <h2 id="daily-life" class="section-heading">Daily Life</h2>
''' + daily_html + '\n' + DIV + '''  <h2 id="history" class="section-heading">Peoples and History</h2>
''' + hist_html + '\n' + DIV + '''  <h2 id="the-tongue" class="section-heading">The Tongue</h2>
''' + tongue_html + '\n' + DIV + '''  <h2 id="names" class="section-heading">What an Auran Is Called</h2>
''' + names_html + '\n' + DIV + '''  <h2 id="figures" class="section-heading">Named Figures</h2>
''' + fig_html + '\n' + DIV + '''  <h2 id="the-column" class="section-heading">One Line Further: Auran</h2>
''' + column_html + '\n' + DIV + '''  <div class="see-also">
    <h3>Continue Reading</h3>
    <ul>
      <li><a href="/setting/talan/domains/lioaru/lioaru.html"><b>Lioaru →</b></a> · The Time domain and its three peoples.</li>
      <li><a href="/setting/talan/domains/lioaru/valreka/valreka.html"><b>Valreka →</b></a> · The whale-borne city, whose Sovereign's reach covers the isle.</li>
      <li><a href="/setting/talan/domains/lioaru/hareaveldi/hareaveldi.html"><b>Hareaveldi →</b></a> · The sand realm, where Sokhan is spoken and the Azarketi dive for arghavan.</li>
      <li><a href="/setting/talan/domains/lioaru/galdua-jendea/galdua-jendea.html"><b>Galdua Jendea →</b></a> · The rocks across the water to the east.</li>
      <li><a href="/setting/talan/domains/vindul/vindul.html"><b>Vindul →</b></a> · Where the yards build the cloudships.</li>
      <li><a href="/setting/talan/ancestries.html"><b>Ancestries →</b></a> · The Azarketi: the ones who answer it now.</li>
    </ul>
  </div>

  <div class="open-canon">
    <h3>⌬ &nbsp; Open in the Chronicle Record</h3>
    <div class="sub">What the chronicle has not yet set down about the isle of the three rains.</div>
    <ol>
      <li><b>The wardens.</b> How a crater town chooses its warden, and who holds Gulgir and Storngir.</li>
      <li><b>The island.</b> Its villages and coves, by name.</li>
      <li><b>The carrying.</b> The Red Dominion's side of the trade.</li>
      <li><b>The Guild.</b> The post-house on the quay and its keeper.</li>
      <li><b>The pans.</b> How the drawing-out is done.</li>
    </ol>
  </div>

  <div class="footer">TYRNARRA · TALAN · LIOARU · AURAN</div>

</div>

</body>
</html>
'''
os.makedirs('published/setting/talan/domains/lioaru/auran', exist_ok=True)
open('published/setting/talan/domains/lioaru/auran/auran.html', 'w').write(page)
print('written', len(page))
