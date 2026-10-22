"""The Haraour Eliza page, generated from lore/geography/sumendar/haraour-eliza.md
(Natsume's letter lives in the deep file itself). Run from the repository root."""
import re, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagegen import *
LORE = 'lore/geography/sumendar/haraour-eliza.md'
L, T = use(LORE, LORE)

# The gate: Natsume's letter whole, then the gate
d1 = section('The gate'); p1 = body(d1)
assert [lead_name(p) for p in p1[1:5]] == ['The walk in', 'The float out', 'The huki', 'The toll']
letter = [l.strip().strip('*') for l in quote(d1, 'Rinza,') if l.strip()]
attrib = quote(d1, 'Natsume, a cook')[0]
letter_html = '  <div class="voice-quote letter">%s</div>\n  <div class="voice-attrib">%s</div>\n' % (
    ''.join('<p>%s</p>' % inline(l) for l in letter), inline(attrib))
gate_html = letter_html + prose(p1[0:1]) + lead_cards(p1[1:4]) + panel('The Toll', strip_lead(p1[4]))

# The Garden
d2 = section('The Garden'); p2 = body(d2)
assert [lead_name(p) for p in p2[1:5]] == ['Bright means careful', 'What is known', 'The preserve', 'The Eliza']
garden_html = prose(p2[0:1]) + panel('Bright Means Careful', strip_lead(p2[1])) + lead_cards(p2[2:4]) + \
    panel('The Eliza', strip_lead(p2[4])) + \
    belief('The Garden Knows Its Own', 'What Folk Say', box(d2, '#### ◈ Popular Belief: the Garden knows its own')) + \
    secret('The Gardener', 'What the Eliza was', box(d2, '#### ⚿ GM Secret: the gardener'))

# The keepers and the record
d3 = section('The keepers and the record'); p3 = body(d3)
assert [lead_name(p) for p in p3[1:5]] == ['The trying', 'Clearings', 'Certificates', 'Who keeps']
keepers_html = vq(quote(d3, 'Scholars come up')) + prose(p3[0:1]) + lead_cards(p3[1:3]) + \
    panel('Certificates', strip_lead(p3[3])) + prose(p3[4:5]) + \
    secret('The Unwritten List', 'What the keepers know', box(d3, '#### ⚿ GM Secret: the unwritten list'))

# The refuge and the crown
d4 = section('The refuge and the crown'); p4 = body(d4)
assert [lead_name(p) for p in p4[1:4]] == ['The refuge', 'The Paapuka', 'The gate shut']
crown_html = vq(quote(d4, 'Everything that leaves')) + prose(p4[0:3]) + panel('The Gate Shut', strip_lead(p4[3]))

# What leaves the gate
d5 = section('What leaves the gate'); p5 = body(d5)
assert [lead_name(p) for p in p5[1:5]] == ['Goods', 'Seeds', 'Poison', 'The proposal']
trade_html = prose(p5[0:1]) + lead_cards(p5[1:4]) + panel('Live Tension · The Proposal', strip_lead(p5[4]))

# Daily life
d6 = section('Daily life'); p6 = body(d6)
assert lead_name(p6[1]) == "The cook's bite"
daily_html = prose(p6[0:1]) + panel("The Cook's Bite", strip_lead(p6[1])) + lead_cards(p6[2:])

outer_html = prose(body(section('The outer country and the neighbours')))
tongue_html = prose(body(section('The tongue')))

nm = section('What a Haraour is called'); nmp = body(nm); samp = nmp[-1]
def pills(label, s_, first=False):
    items = [x.strip().strip('.') for x in s_.split(',')]
    return '    <p style="margin:%s 0 6px;"><b>%s</b></p>\n    <div class="pill-row">%s</div>\n' % ('0' if first else '14px', label, ''.join('<span class="pill">%s</span>' % html.escape(x) for x in items))
g = re.search(r'Given: (.+?)\. Houses:', samp).group(1); hh = re.search(r'Houses: (.+?)\. Whole:', samp).group(1)
wholes = [x.strip() for x in re.search(r'Whole: (.+)$', samp).group(1).split('·')]
names_html = prose(nmp[:-1]) + '  <div class="feature-panel">\n    <div class="panel-label">Sample Names</div>\n' + pills('Given', g, True) + pills('Houses', hh) + \
    '    <p style="margin:14px 0 6px;"><b>Whole names</b></p>\n    <div class="pill-row">%s</div>\n  </div>\n' % ''.join('<span class="pill">%s</span>' % inline(x) for x in wholes)

fig = L[L.index('## Named figures'):L.index('## Voices')]
figs = [l[2:] for l in fig.split('\n') if l.startswith('- ')]
def figcard(x):
    m = re.match(r'\*\*(.+?)\*\*,? ?:? ?(.*)$', x)
    r_ = inline(m.group(2)); r_ = r_[0].upper() + r_[1:]
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_)
fig_html = '  <div class="card-grid figure-grid">\n' + ''.join(figcard(x) for x in figs) + '  </div>\n'

etym = field('Etymology').replace(' (Derivations in the glossary.)', '')
pos = field('Position'); terr = field('Terrain'); peop = field('Peoples'); tongue = field('Tongue'); faith = field('Faith'); rule = field('Rule'); cap = field('Capital'); founded = field('Founded'); char = field('Character')
cap1 = lambda t: t[0].upper() + t[1:]
page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Haraour Eliza · Sumendar · Tyrnarra</title>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/setting/assets/style-b.css">
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
<script defer src="/setting/assets/site-interactions.js"></script>
<style>
  :root {
    --domain-accent: #c77dd6;   /* garden violet, bright means careful · 6.81:1 on Style B bg */
    --card-bg: rgba(28,16,30,0.55);
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
<body data-page="haraour-eliza">

<div class="container">

  <div class="breadcrumb">
    <a href="/setting/index.html">Tyrnarra</a><span class="sep">›</span><a href="/setting/talan/talan.html">Talan</a><span class="sep">›</span><a href="/setting/talan/domains/sumendar/sumendar.html">Sumendar</a><span class="sep">›</span><span>Haraour Eliza</span>
  </div>

  <div class="header">
    <div class="header-ornament">✦ · ✦ · ✦</div>
    <div class="page-title">Haraour Eliza</div>
    <div class="page-subtitle">Sumendar Sub-Region · The Garden in the Ring · The Gate and the Keepers</div>
    <div class="page-flavor">''' + inline(cap1(char)) + '''</div>
  </div>

''' + DIV + '''  <h2 id="at-a-glance" class="section-heading">At a Glance</h2>
  <dl class="facts">
    <dt>Etymology</dt><dd>''' + inline(cap1(etym)) + '''</dd>
    <dt>Position</dt><dd>''' + inline(cap1(pos)) + '''</dd>
    <dt>Terrain</dt><dd>''' + inline(cap1(terr)) + '''</dd>
    <dt>Character</dt><dd>
      <i>''' + inline(cap1(char)) + '''</i><br>
      <div class="pill-row" style="margin-top:6px"><span class="pill">The Garden</span><span class="pill">The Alaloa</span><span class="pill">The Walk In</span><span class="pill">The Float Out</span><span class="pill">The Keepers</span><span class="pill">The Cook's Bite</span></div>
    </dd>
    <dt>Peoples</dt><dd>''' + inline(cap1(peop)) + '''</dd>
    <dt>Tongue</dt><dd>''' + inline(cap1(tongue)) + '''</dd>
    <dt>Faith</dt><dd>''' + inline(cap1(faith)) + '''</dd>
    <dt>Rule</dt><dd>''' + inline(cap1(rule)) + '''</dd>
    <dt>Capital</dt><dd>''' + inline(cap1(cap)) + '''</dd>
    <dt>Founded</dt><dd>''' + inline(cap1(founded)) + '''</dd>
  </dl>

  <div class="gods-city" style="border-color: rgba(199,125,214,0.5);">
    <div class="gods-city-label">The Capital</div>
    <div class="gods-city-name">Pukawai</div>
    <div class="gods-city-byname">At the foot of the ring, where the river comes out · the palace Jaurei · the gate</div>
  </div>

''' + DIV + '''  <h2 id="the-gate" class="section-heading">The Gate</h2>

''' + gate_html + '\n' + DIV + '''  <h2 id="the-garden" class="section-heading">The Garden</h2>

''' + garden_html + '\n' + DIV + '''  <h2 id="the-keepers" class="section-heading">The Keepers and the Record</h2>

''' + keepers_html + '\n' + DIV + '''  <h2 id="the-crown" class="section-heading">The Refuge and the Crown</h2>

''' + crown_html + '\n' + DIV + '''  <h2 id="what-leaves-the-gate" class="section-heading">What Leaves the Gate</h2>

''' + trade_html + '\n' + DIV + '''  <h2 id="daily-life" class="section-heading">Daily Life</h2>
''' + daily_html + '\n' + DIV + '''  <h2 id="the-outer-country" class="section-heading">The Outer Country and the Neighbours</h2>
''' + outer_html + '\n' + DIV + '''  <h2 id="the-tongue" class="section-heading">The Tongue</h2>
''' + tongue_html + '\n' + DIV + '''  <h2 id="names" class="section-heading">What a Haraour Is Called</h2>
''' + names_html + '\n' + DIV + '''  <h2 id="figures" class="section-heading">Named Figures</h2>
''' + fig_html + '\n' + DIV + '''  <div class="see-also">
    <h3>Continue Reading</h3>
    <ul>
      <li><a href="/setting/talan/domains/sumendar/sumendar.html"><b>Sumendar →</b></a> · The Fire domain and its four peoples.</li>
      <li><a href="/setting/talan/domains/sumendar/no-mans-land/no-mans-land.html"><b>No Man's Land →</b></a> · The ungoverned country the road crosses, north and east.</li>
      <li><a href="/setting/talan/domains/sumendar/eldara/eldara.html"><b>Eldara →</b></a> · The Forge City, whose still-rooms buy the reagents.</li>
      <li><a href="/setting/talan/domains/sumendar/tahu-tangata/tahu-tangata.html"><b>Tahu Tangata →</b></a> · The plain of the burn, and Leowai's sister tongue.</li>
      <li><a href="/setting/talan/domains/lautara/emarrea/emarrea.html"><b>Emarrea →</b></a> · Biozuri and the House of a Thousand Flavors, where Natsume cooks.</li>
      <li><a href="/setting/talan/factions/adventurers-guild.html"><b>The Adventurers' Guild →</b></a> · Its Kingshall at Pukawai, and what it buys.</li>
    </ul>
  </div>

  <div class="open-canon">
    <h3>⌬ &nbsp; Open in the Chronicle Record</h3>
    <div class="sub">What the chronicle has not yet set down about the Garden and the gate.</div>
    <ol>
      <li><b>The inner mouth.</b> Its name.</li>
      <li><b>The places.</b> The outer towns, and the inside's own places, by name.</li>
      <li><b>The road.</b> The halt on Eldara's line, and whether a line will run on to the Red Dominion.</li>
      <li><b>The keepers.</b> How many there are.</li>
      <li><b>The dishes.</b> The Garden's dishes, by name.</li>
    </ol>
  </div>

  <div class="footer">TYRNARRA · TALAN · SUMENDAR · HARAOUR ELIZA</div>

</div>

</body>
</html>
'''
os.makedirs('published/setting/talan/domains/sumendar/haraour-eliza', exist_ok=True)
open('published/setting/talan/domains/sumendar/haraour-eliza/haraour-eliza.html', 'w').write(page)
print('written', len(page))
