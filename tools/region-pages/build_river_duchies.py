"""The River Duchies page, generated from lore/geography/lioaru/river-duchies.md
and the column in river-duchies-chronicle.md. Run from the repository root."""
import re, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagegen import *
L, T = use('lore/geography/lioaru/river-duchies.md', 'lore/geography/lioaru/river-duchies-chronicle.md')

# The quick valley
d1 = section('The quick valley'); p1 = body(d1)
assert lead_name(p1[2]) == 'The turning' and lead_name(p1[3]) == 'Water'
quick_html = vq(quote(d1, 'At dawn the market')) + prose(p1[0:2]) + panel('The Turning', strip_lead(p1[2])) + prose([p1[3]]) + \
    belief('Sleep in a Field at Noon', 'What Mothers Say', box(d1, '#### ◈ Popular Belief: sleep in a field at noon'))

# The river and the Hemmal
d2 = section('The river and the Hemmal'); p2 = body(d2)
assert [lead_name(p) for p in p2[1:3]] == ['The flood feast', 'The flood-warden']
river_html = vq(quote(d2, 'Once a year it comes')) + prose(p2[0:1]) + lead_cards(p2[1:3])

# The cut law and the Mida
d3 = section('The cut law and the Mida'); p3 = body(d3)
assert [lead_name(p) for p in p3[2:6]] == ['The cut law', 'The dukes', 'The Mida', 'The Westfold fields']
cut_html = vq(quote(d3, 'Thicket is what')) + prose(p3[0:2]) + panel('The Cut Law', strip_lead(p3[2])) + prose(p3[3:5]) + \
    panel('Live Tension · The Westfold Fields', strip_lead(p3[5]))

isles_html = prose(body(section('The slow isles and Agu')))

d5 = section('Daily life'); p5 = body(d5)
assert lead_name(p5[2]) == 'Sloth'
daily_html = prose(p5[0:2]) + lead_cards(p5[2:])

folk_html = prose(body(section('The Duchy folk')))
tongue_html = prose(body(section('The tongue')))

nm = section('What the Duchy folk are called'); nmp = body(nm); samp = nmp[-1]
def pills(label, s_, first=False):
    items = [x.strip().strip('.') for x in s_.split(',')]
    return '    <p style="margin:%s 0 6px;"><b>%s</b></p>\n    <div class="pill-row">%s</div>\n' % ('0' if first else '14px', label, ''.join('<span class="pill">%s</span>' % html.escape(x) for x in items))
g = re.search(r'Given: (.+?)\. Birth-floods:', samp).group(1); bf = re.search(r'Birth-floods: (.+?)\. Houses:', samp).group(1); hh = re.search(r'Houses: (.+?)\. Whole:', samp).group(1)
wholes = [x.strip() for x in re.search(r'Whole: (.+)$', samp).group(1).split('·')]
names_html = prose(nmp[:-1]) + '  <div class="feature-panel">\n    <div class="panel-label">Sample Names</div>\n' + pills('Given', g, True) + pills('Birth-floods', bf) + pills('Houses', hh) + \
    '    <p style="margin:14px 0 6px;"><b>Whole names</b></p>\n    <div class="pill-row">%s</div>\n  </div>\n' % ''.join('<span class="pill">%s</span>' % inline(x) for x in wholes)

fig = L[L.index('## Named figures'):L.index('## Voices')]
figs = [l[2:] for l in fig.split('\n') if l.startswith('- ')]
def figcard(x):
    m = re.match(r'\*\*(.+?)\*\*,? ?:? ?(.*)$', x)
    rest = re.sub(r' \((?:her|his|their) register in [^)]*\)', ', in <i>The Travelling Chronicle</i>', m.group(2))
    r_ = inline(rest).replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>'); r_ = r_[0].upper() + r_[1:]
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_)
fig_html = '  <div class="card-grid figure-grid">\n' + ''.join(figcard(x) for x in figs) + '  </div>\n'

# The column: the intro, then a card per correspondent and one for the last evening
col = T[T.index('My column on the River Duchies'):]
chunks = [c.strip() for c in col.split('\n\n') if c.strip()]
intro = chunks[0]
cards = []; i = 1
heads = ['To a keeper of Tamalut', 'To a reader in Namur', 'To a factor of Valreka']
sums = ['They water the road.', 'A slothful people.', 'The waste of it.']
for n in range(3):
    q = chunks[i]; r = chunks[i + 1]; i += 2
    ql = [l[2:] if l.startswith('> ') else l[1:] for l in q.split('\n')]
    b = '<div class="voice-quote" style="margin:4px 0 14px;"><p>%s</p></div><div class="voice-attrib" style="margin:-8px 0 14px;">%s</div><p>%s</p>' % (inline(ql[0]), inline(ql[1]), inline(r))
    cards.append((heads[n], sums[n], b))
rest = chunks[i:]
cards.append(('The last evening', 'The meal, the seed-boats, and the salt.', ''.join('<p>%s</p>' % inline(c) for c in rest)))
column_html = '  <div class="prose"><p>%s</p></div>\n  <div class="log-letters">\n' % inline(intro)
for k, s_, b in cards:
    column_html += ('    <div class="log-letter"><button class="log-letter-head" aria-expanded="false" onclick="var c=this.parentNode;c.classList.toggle(\'open\');this.setAttribute(\'aria-expanded\',c.classList.contains(\'open\'))">'
                    '<span class="ld-date">%s</span><span class="ld-text">%s</span><span class="expand-hint">Tap ▾</span></button><div class="log-letter-body">%s</div></div>\n') % (html.escape(k), html.escape(s_), b)
column_html += '  </div>\n'

etym = field('Etymology').replace(' (Derivations in the glossary.)', '')
pos = field('Position'); terr = field('Terrain'); peop = field('Peoples'); tongue = field('Tongue'); faith = field('Faith'); rule = field('Rule'); cap = field('Capital'); founded = field('Founded'); char = field('Character')
cap1 = lambda t: t[0].upper() + t[1:]
page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>River Duchies · Lioaru · Tyrnarra</title>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/setting/assets/style-b.css">
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
<script defer src="/setting/assets/site-interactions.js"></script>
<style>
  :root {
    --domain-accent: #a8c878;   /* quick green · 10.40:1 on Style B bg */
    --card-bg: rgba(20,26,14,0.55);
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
<body data-page="river-duchies">

<div class="container">

  <div class="breadcrumb">
    <a href="/setting/index.html">Tyrnarra</a><span class="sep">›</span><a href="/setting/talan/talan.html">Talan</a><span class="sep">›</span><a href="/setting/talan/domains/lioaru/lioaru.html">Lioaru</a><span class="sep">›</span><span>River Duchies</span>
  </div>

  <div class="header">
    <div class="header-ornament">✦ · ✦ · ✦</div>
    <div class="page-title">River Duchies</div>
    <div class="page-subtitle">Lioaru Sub-Region · The Quick Valley · Eleven Duchies under the Cut Law</div>
    <div class="page-flavor">''' + inline(cap1(char)) + '''</div>
  </div>

''' + DIV + '''  <h2 id="at-a-glance" class="section-heading">At a Glance</h2>
  <dl class="facts">
    <dt>Etymology</dt><dd>''' + inline(cap1(etym)) + '''</dd>
    <dt>Position</dt><dd>''' + inline(cap1(pos)) + '''</dd>
    <dt>Terrain</dt><dd>''' + inline(cap1(terr)) + '''</dd>
    <dt>Character</dt><dd>
      <i>''' + inline(cap1(char)) + '''</i><br>
      <div class="pill-row" style="margin-top:6px"><span class="pill">The Quick Valley</span><span class="pill">The Turning</span><span class="pill">The Hemmal</span><span class="pill">The Cut Law</span><span class="pill">The Mida</span><span class="pill">The Slow Isles</span></div>
    </dd>
    <dt>Peoples</dt><dd>''' + inline(cap1(peop)) + '''</dd>
    <dt>Tongue</dt><dd>''' + inline(cap1(tongue)) + '''</dd>
    <dt>Faith</dt><dd>''' + inline(cap1(faith)) + '''</dd>
    <dt>Rule</dt><dd>''' + inline(cap1(rule)) + '''</dd>
    <dt>Capital</dt><dd>''' + inline(cap1(cap)) + '''</dd>
    <dt>Founded</dt><dd>''' + inline(cap1(founded)) + '''</dd>
  </dl>

  <div class="gods-city" style="border-color: rgba(168,200,120,0.5);">
    <div class="gods-city-label">The Capital</div>
    <div class="gods-city-name">Lemersa</div>
    <div class="gods-city-byname">At the head of the bay where the river meets the sea · no duke's · the seat of the Mida</div>
  </div>

''' + DIV + '''  <h2 id="the-quick-valley" class="section-heading">The Quick Valley</h2>

''' + quick_html + '\n' + DIV + '''  <h2 id="the-hemmal" class="section-heading">The River and the Hemmal</h2>

''' + river_html + '\n' + DIV + '''  <h2 id="the-cut-law" class="section-heading">The Cut Law and the Mida</h2>

''' + cut_html + '\n' + DIV + '''  <h2 id="the-slow-isles" class="section-heading">The Slow Isles and Agu</h2>
''' + isles_html + '\n' + DIV + '''  <h2 id="daily-life" class="section-heading">Daily Life</h2>
''' + daily_html + '\n' + DIV + '''  <h2 id="the-duchy-folk" class="section-heading">The Duchy Folk</h2>
''' + folk_html + '\n' + DIV + '''  <h2 id="the-tongue" class="section-heading">The Tongue</h2>
''' + tongue_html + '\n' + DIV + '''  <h2 id="names" class="section-heading">What the Duchy Folk Are Called</h2>
''' + names_html + '\n' + DIV + '''  <h2 id="figures" class="section-heading">Named Figures</h2>
''' + fig_html + '\n' + DIV + '''  <h2 id="the-column" class="section-heading">To My Correspondents, on the River Duchies</h2>
''' + column_html + '\n' + DIV + '''  <div class="see-also">
    <h3>Continue Reading</h3>
    <ul>
      <li><a href="/setting/talan/domains/lioaru/lioaru.html"><b>Lioaru →</b></a> · The Time domain and its three peoples.</li>
      <li><a href="/setting/talan/domains/lautara/emarrea/emarrea.html"><b>Emarrea →</b></a> · Upstream, where the river and the drift-barges come from.</li>
      <li><a href="/setting/talan/domains/lioaru/galdua-jendea/galdua-jendea.html"><b>Galdua Jendea →</b></a> · The rocks, the salt, and the pale band to the west.</li>
      <li><a href="/setting/talan/domains/lioaru/valreka/valreka.html"><b>Valreka →</b></a> · The herd that rests at the valley's edge, and house Asif.</li>
      <li><a href="/setting/talan/domains/lioaru/hareaveldi/hareaveldi.html"><b>Hareaveldi →</b></a> · Across the river line to the east.</li>
      <li><a href="/setting/talan/domains/lioaru/lost-kingdom.html"><b>The Lost Kingdom →</b></a> · Beyond the pale band, where the legions come from.</li>
    </ul>
  </div>

  <div class="open-canon">
    <h3>⌬ &nbsp; Open in the Chronicle Record</h3>
    <div class="sub">What the chronicle has not yet set down about the quick valley.</div>
    <ol>
      <li><b>The duchies.</b> The ten besides Westfold, by name, and their dukes.</li>
      <li><b>The houses.</b> Whether new houses are made, and how.</li>
      <li><b>The Hemmal.</b> Its season.</li>
      <li><b>Agu.</b> What lies in the fog.</li>
    </ol>
  </div>

  <div class="footer">TYRNARRA · TALAN · LIOARU · RIVER DUCHIES</div>

</div>

</body>
</html>
'''
os.makedirs('published/setting/talan/domains/lioaru/river-duchies', exist_ok=True)
open('published/setting/talan/domains/lioaru/river-duchies/river-duchies.html', 'w').write(page)
print('written', len(page))
