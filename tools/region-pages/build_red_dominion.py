"""The Red Dominion page, generated from lore/geography/sumendar/red-dominion.md
and Roshanak's sketchbook (red-dominion-sketchbook.md). Run from the repository root."""
import re, html, os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pagegen import *
LORE = 'lore/geography/sumendar/red-dominion.md'
DOC = 'lore/geography/sumendar/red-dominion-sketchbook.md'
L, T = use(LORE, DOC)
OUT = 'published/setting/talan/domains/sumendar/red-dominion'
ART = 'tools/imageGen/scenes/red-dominion'

def heads(ps, names):
    assert [lead_name(p) for p in ps] == names, [p[:30] for p in ps]

# The ship-towns
d1 = section('The ship-towns'); p1 = body(d1)
ships_html = vq(quote(d1, '**2. The first ship-town')) + prose(p1) + vq(quote(d1, '**4. A figurehead'))

# The fleet that came home
d2 = section('The fleet that came home'); p2 = body(d2)
fleet_html = prose(p2) + secret('The Fleet Killed the Emperor', 'How the Golden Emperor died',
                                box(d2, '#### ⚿ GM Secret: the fleet killed the Emperor'))

# The muster and the Admiralty
d3 = section('The muster and the Admiralty'); p3 = body(d3)
heads(p3[3:6], ['The muster call', 'In action', 'The asking'])
muster_html = prose(p3[0:3]) + lead_cards(p3[3:5]) + panel('The Asking', strip_lead(p3[5])) + prose(p3[6:])

# What a Red is called
nm = section('What a Red is called'); nmp = body(nm); samp = nmp[-1]
def pills(label, s_, first=False):
    items = [x.strip().strip('.') for x in s_.split(',')]
    return '    <p style="margin:%s 0 6px;"><b>%s</b></p>\n    <div class="pill-row">%s</div>\n' % ('0' if first else '14px', label, ''.join('<span class="pill">%s</span>' % html.escape(x) for x in items))
g = re.search(r'Given \(Folau sound\): (.+?)\. Sea names:', samp).group(1)
sn = re.search(r'Sea names: (.+?)\. Ships:', samp).group(1)
sh = re.search(r'Ships: (.+?)\. Whole:', samp).group(1)
wholes = [x.strip() for x in re.search(r'Whole: (.+)$', samp).group(1).split('·')]
names_html = prose(nmp[:-1]) + '  <div class="feature-panel">\n    <div class="panel-label">Sample Names</div>\n' + \
    pills('Given (Folau)', g, True) + pills('Sea names', sn) + pills('Ships', sh) + \
    '    <p style="margin:14px 0 6px;"><b>Whole names</b></p>\n    <div class="pill-row">%s</div>\n  </div>\n' % ''.join('<span class="pill">%s</span>' % inline(x) for x in wholes)

# Saegate and the fleet
d5 = section('Saegate and the fleet'); p5 = body(d5)
heads([p5[1], p5[3], p5[4]], ['The imperial ships', 'The refit', 'The guns'])
saegate_html = vq(quote(d5, '**1. The point')) + prose(p5[0:1]) + panel('The Imperial Ships', strip_lead(p5[1])) + \
    prose(p5[2:3]) + lead_cards(p5[3:5]) + \
    belief("The Embrace's Gun", 'What every port says', box(d5, "#### ◈ Popular Belief: the Embrace's gun")) + \
    secret('A Gun for a God', 'What the Embrace carries', box(d5, '#### ⚿ GM Secret: a gun for a god'))

# The frontier
d6 = section('The frontier'); p6 = body(d6)
heads(p6[1:5], ['Anokula', 'The nests', 'Tuta and the scar road', 'Hyseat'])
frontier_html = vq(quote(d6, '**7. The mountains')) + prose(p6[0:1]) + lead_cards(p6[1:5]) + \
    belief('Sealed With Him Inside', 'What Dominion folk say', box(d6, '#### ◈ Popular Belief: sealed with him inside'))

# The carrying
d7 = section('The carrying'); p7 = body(d7)
partners = [l[2:] for l in d7.split('\n') if l.startswith('- ')]
def partner(x):
    m = re.match(r'\*\*(.+?)\*\*,? ?:? ?(.*)$', x)
    r_ = inline(m.group(2)); r_ = r_[0].upper() + r_[1:]
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_)
carrying_html = prose(p7[0:1]) + '  <div class="card-grid life-grid">\n' + ''.join(partner(x) for x in partners) + '  </div>\n' + prose(p7[1:])

# The quarters abroad, and the call
d8 = section('The quarters abroad')
k = d8.index('\n### The call to the quarters\n'); q8, c8 = d8[:k], d8[k + len('\n### The call to the quarters\n'):]
quarters_html = vq(quote(q8, '**6. Two crews')) + prose(body(q8))
pc = body(c8); assert len(pc) == 2
call_html = vq(quote(c8, 'Every house that answers')) + vq(quote(c8, 'I put the Admiralty')) + prose(pc[0:1]) + \
    vq(quote(c8, 'My crews bring the iron')) + panel('Live Tension · The Call to the Quarters', pc[1])

# Daily life
d9 = section('Daily life'); p9 = body(d9)
heads(p9[4:6], ['The young', 'Faith'])
daily_html = prose(p9[0:3]) + panel('Visitor and Native', p9[3]) + lead_cards(p9[4:6])

# Named figures
fig = L[L.index('## Named figures'):L.index('## Voices')]
figs = [l[2:] for l in fig.split('\n') if l.startswith('- ')]
def figcard(x):
    m = re.match(r'\*\*(.+?)\*\*,? ?:? ?(.*)$', x)
    r_ = inline(m.group(2)); r_ = r_[0].upper() + r_[1:]
    return '    <div class="accent-card">\n      <div class="card-name">%s</div>\n      <p>%s</p>\n    </div>\n' % (html.escape(m.group(1)), r_)
fig_html = '  <div class="card-grid figure-grid">\n' + ''.join(figcard(x) for x in figs) + '  </div>\n'

# The sketchbook, whole, as sketch cards
ALT = {
    1: 'Ink sketch of a walled town on a rock at the end of a coast, the walls running down to the water around a harbour of masts, the stone town above.',
    2: 'Ink sketch from a ship\'s deck of a shore town roofed with upturned boats, small hull roofs around one great keel-up hall.',
    3: 'Ink sketch of a house made from an upturned hull, level and closed, its door cut in the stern under a square patch, a barrel and rope beside it.',
    4: 'Ink sketch of a hull-roofed bakery seen end-on, a carved figurehead of a woman holding fish hung over the window like a sign, a queue outside.',
    5: 'Ink sketch of a ship\'s bell hanging in a timber frame.',
    6: 'Ink sketch from a quay down the gap between two moored hulls, a crew at each rail turned to the other, a sailor in a long coat on the quay.',
    7: 'Ink sketch over a ship\'s rail and a coil of rope, across the water to a low dark line of mountains under the clouds.',
}
FILES = {1: 's1-point', 2: 's2-ship-town', 3: 's3-harbour-master', 4: 's4-figurehead', 5: 's5-bell-clean', 6: 's6-crews', 7: 's7-mountains'}
os.makedirs(OUT + '/sketches', exist_ok=True)
sk = re.findall(r'^\*\*(\d)\. (.+?)\.\*\* (.+)$', T, re.M)
assert [int(n) for n, _, _ in sk] == list(range(1, 8))
cards = ''
for n, title, note in sk:
    n = int(n); f = FILES[n] + '.webp'
    shutil.copyfile(os.path.join(ART, f), os.path.join(OUT, 'sketches', f))
    cards += ('    <figure class="sketch-card">\n      <img src="/setting/talan/domains/sumendar/red-dominion/sketches/%s" alt="%s" loading="lazy">\n'
              '      <figcaption><span class="sk-num">Sketch %d</span><span class="sk-title">%s</span><p>%s</p></figcaption>\n    </figure>\n') % (
        f, html.escape(ALT[n]), n, inline(title), inline(note))
colophon = re.search(r'^\*(From the sketchbook of .+)\*$', T, re.M).group(1)
sketch_html = '  <div class="sketch-cards">\n' + cards + '  </div>\n  <div class="voice-attrib" style="margin-top:14px;">%s</div>\n' % inline(colophon)

# Open in the Chronicle Record, from the deep file's Still open
still = re.search(r'^\*\*Still open:\*\* (.+)$', L, re.M).group(1).rstrip('.')
open_html = ''.join('      <li>%s.</li>\n' % inline(x.strip()[0].upper() + x.strip()[1:]) for x in still.split(';'))

etym = field('Etymology').replace(' (Derivations in the glossary.)', '')
pos = field('Position'); terr = field('Terrain'); peop = field('Peoples'); tongue = field('Tongue'); faith = field('Faith'); rule = field('Rule'); cap = field('Capital'); founded = field('Founded'); char = field('Character')
cap1 = lambda t: t[0].upper() + t[1:]
page = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Red Dominion · Sumendar · Tyrnarra</title>
<link href="https://fonts.googleapis.com/css2?family=Uncial+Antiqua&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/setting/assets/style-b.css">
<link rel="stylesheet" href="/setting/assets/site-nav.css">
<script defer src="/setting/assets/site-nav.js"></script>
<script defer src="/setting/assets/site-interactions.js"></script>
<style>
  :root {
    --domain-accent: #d9574a;   /* pit-red, the iron paint of the ship-towns · 5.03:1 on Style B bg */
    --card-bg: rgba(34,14,12,0.55);
  }
  .voice-quote { max-width: 780px; margin: 20px auto; padding: 18px 24px; background: var(--card-bg); border-left: 3px solid var(--domain-accent); border-radius: 0 4px 4px 0; font-style: italic; line-height: 1.65; }
  .voice-quote p { margin: 0 0 12px; }
  .voice-quote p:last-child { margin-bottom: 0; }
  .voice-attrib { max-width: 780px; margin: -10px auto 22px; text-align: right; font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--domain-accent); }
  .life-grid, .figure-grid { --col-min: 230px; --grid-gap: 16px; --card-pad: 18px 20px; }
  .life-grid .card-name, .figure-grid .card-name { font-size: 1.05rem; letter-spacing: 0.06em; margin-bottom: 8px; color: var(--domain-accent); }
  .panel-label { font-family: 'Cinzel', serif; font-size: 0.78rem; letter-spacing: 0.22em; text-transform: uppercase; color: var(--domain-accent); margin-bottom: 10px; }
  .call-heading { font-family: 'Cinzel', serif; font-size: 1.05rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--domain-accent); text-align: center; margin: 34px 0 6px; }
</style>
</head>
<body data-page="red-dominion">

<div class="container">

  <div class="breadcrumb">
    <a href="/setting/index.html">Tyrnarra</a><span class="sep">›</span><a href="/setting/talan/talan.html">Talan</a><span class="sep">›</span><a href="/setting/talan/domains/sumendar/sumendar.html">Sumendar</a><span class="sep">›</span><span>The Red Dominion</span>
  </div>

  <div class="header">
    <div class="header-ornament">✦ · ✦ · ✦</div>
    <div class="page-title">The Red Dominion</div>
    <div class="page-subtitle">Sumendar Sub-Region · The Fleet That Came Home · The Ship-Towns and the Quarters</div>
    <div class="page-flavor">''' + inline(cap1(char)) + '''</div>
  </div>

''' + DIV + '''  <h2 id="at-a-glance" class="section-heading">At a Glance</h2>
  <dl class="facts">
    <dt>Etymology</dt><dd>''' + inline(cap1(etym)) + '''</dd>
    <dt>Position</dt><dd>''' + inline(cap1(pos)) + '''</dd>
    <dt>Terrain</dt><dd>''' + inline(cap1(terr)) + '''</dd>
    <dt>Character</dt><dd>
      <i>''' + inline(cap1(char)) + '''</i><br>
      <div class="pill-row" style="margin-top:6px"><span class="pill">The Ship-Towns</span><span class="pill">The Muster</span><span class="pill">The Asking</span><span class="pill">The Quarters</span><span class="pill">The Embrace</span><span class="pill">The Vaota</span><span class="pill">Anokula</span></div>
    </dd>
    <dt>Peoples</dt><dd>''' + inline(cap1(peop)) + '''</dd>
    <dt>Tongue</dt><dd>''' + inline(cap1(tongue)) + '''</dd>
    <dt>Faith</dt><dd>''' + inline(cap1(faith)) + '''</dd>
    <dt>Rule</dt><dd>''' + inline(cap1(rule)) + '''</dd>
    <dt>Capital</dt><dd>''' + inline(cap1(cap)) + '''</dd>
    <dt>Founded</dt><dd>''' + inline(cap1(founded)) + '''</dd>
  </dl>

  <div class="gods-city" style="border-color: rgba(217,87,74,0.5);">
    <div class="gods-city-label">The Capital</div>
    <div class="gods-city-name">Saegate</div>
    <div class="gods-city-byname">On the southern point, walled down to the water · the Admiralty · the Embrace</div>
  </div>

''' + DIV + '''  <h2 id="the-ship-towns" class="section-heading">The Ship-Towns</h2>

''' + ships_html + '\n' + DIV + '''  <h2 id="the-fleet" class="section-heading">The Fleet That Came Home</h2>

''' + fleet_html + '\n' + DIV + '''  <h2 id="the-muster" class="section-heading">The Muster and the Admiralty</h2>

''' + muster_html + '\n' + DIV + '''  <h2 id="names" class="section-heading">What a Red Is Called</h2>

''' + names_html + '\n' + DIV + '''  <h2 id="saegate" class="section-heading">Saegate and the Fleet</h2>

''' + saegate_html + '\n' + DIV + '''  <h2 id="the-frontier" class="section-heading">The Frontier</h2>

''' + frontier_html + '\n' + DIV + '''  <h2 id="the-carrying" class="section-heading">The Carrying</h2>

''' + carrying_html + '\n' + DIV + '''  <h2 id="the-quarters" class="section-heading">The Quarters Abroad</h2>

''' + quarters_html + '''
  <h3 id="the-call" class="call-heading">The Call to the Quarters</h3>

''' + call_html + '\n' + DIV + '''  <h2 id="daily-life" class="section-heading">Daily Life</h2>

''' + daily_html + '\n' + DIV + '''  <h2 id="figures" class="section-heading">Named Figures</h2>

''' + fig_html + '\n' + DIV + '''  <h2 id="the-sketchbook" class="section-heading">The Sketchbook</h2>

''' + sketch_html + '\n' + DIV + '''  <div class="see-also">
    <h3>Continue Reading</h3>
    <ul>
      <li><a href="/setting/talan/domains/sumendar/sumendar.html"><b>Sumendar →</b></a> · The Fire domain and its peoples.</li>
      <li><a href="/setting/talan/historical/golden-empire.html"><b>The Golden Empire →</b></a> · The Empire whose crown land this was, and whose fleet sailed from Saegate.</li>
      <li><a href="/setting/talan/domains/lioaru/auran/auran.html"><b>Auran →</b></a> · The island of the craters, whose cargo goes out in Dominion hulls.</li>
      <li><a href="/setting/talan/domains/myrkono/three-pines/three-pines.html"><b>Three Pines →</b></a> · Ontzola's yards, where the long-haul hulls are ordered.</li>
      <li><a href="/setting/talan/domains/lioaru/river-duchies/river-duchies.html"><b>The River Duchies →</b></a> · Lemersa's grain, across the bay.</li>
      <li><a href="/setting/talan/domains/sumendar/haraour-eliza/haraour-eliza.html"><b>Haraour Eliza →</b></a> · The garden in the ring, east across the border.</li>
      <li><a href="/setting/talan/domains/sumendar/no-mans-land/no-mans-land.html"><b>No Man's Land →</b></a> · The ungoverned country past Hyseat.</li>
      <li><a href="/setting/talan/transport.html"><b>Transport →</b></a> · The Hafra's carriers and sea powers.</li>
    </ul>
  </div>

  <div class="open-canon">
    <h3>⌬ &nbsp; Open in the Chronicle Record</h3>
    <div class="sub">What the chronicle has not yet set down about the Dominion and its fleet.</div>
    <ol>
''' + open_html + '''    </ol>
  </div>

  <div class="footer">TYRNARRA · TALAN · SUMENDAR · THE RED DOMINION</div>

</div>

</body>
</html>
'''
open(OUT + '/red-dominion.html', 'w').write(page)
print('written', len(page))
