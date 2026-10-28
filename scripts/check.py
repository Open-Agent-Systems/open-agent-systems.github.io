from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.h1=0; self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if 'id' in a: self.ids.add(a['id'])
        for key in ['href','src']:
            if key in a: self.links.append(a[key])
        if tag=='img': assert 'alt' in a, 'Missing image alt'
pages={}
for f in DOCS.rglob('*.html'):
    p=Page(); p.feed(f.read_text()); pages[f.resolve()]=p
    assert p.lang and p.h1==1, f
for f,p in pages.items():
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        target=(DOCS/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (f.parent/unquote(u.path) if u.path else f)
        if target.is_dir(): target=target/'index.html'
        target=target.resolve()
        assert target.exists(), (f,link)
        if u.fragment: assert unquote(u.fragment) in pages[target].ids,(f,link)
locales=[json.loads(f.read_text()) for f in (ROOT/'content').glob('*.json')]
assert all(set(d)==set(locales[0]) for d in locales)
assert all(len(d['areas'])==4 and len(d['principles'])==3 and len(d['steps'])==4 for d in locales)
assert not any(re.search(r'\bOMA\b', f.read_text()) for f in DOCS.rglob('*.html'))
print('[PASS] Local links, anchors, languages, page headings, image alt, and content scope')

for d in locales:
    assert len(d['layers']) == 8
    assert len(d['journeys']) == 3
    assert all(all(0 <= i < len(d['layers']) for i in j[1]) for j in d['journeys'])
    svg = DOCS / 'assets' / ('architecture.' + d['lang'] + '.svg')
    text = ''.join(ET.parse(svg).getroot().itertext())
    for layer in d['layers']:
        assert layer[0] in text
        assert all(label in text for label in layer[1])
    assert d['architectureCommunity'] in text
print('[PASS] SVG architecture exports contain every localized layer and capability')

for d in locales:
    eco = d['ecosystemView']
    assert len(eco['nodes']) == 6 and len(eco['modes']) == 3
    assert all(sorted(mode[3]) == list(range(6)) for mode in eco['modes'])
print('[PASS] Ecosystem views each traverse all six valid capabilities')
