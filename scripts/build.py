from pathlib import Path
from html import escape as esc
import json
import runpy

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
BASE = 'https://open-agent-systems.github.io'
ORG = 'https://github.com/Open-Agent-Systems'
ISSUES = ORG + '/.github/issues'
items = [json.loads(p.read_text()) for p in sorted((ROOT / 'content').glob('*.json'))]
assert len({d['path'] for d in items}) == len(items)
assert len({d['lang'] for d in items}) == len(items)
for d in items:
    assert d['path'].startswith('/') and '..' not in d['path']
    links = '\n'.join(f'<link rel="alternate" hreflang="{esc(x["lang"])}" href="{BASE}{x["path"]}">' for x in items)
    languages = ''
    for x in items:
        current = ' aria-current="page"' if x['lang'] == d['lang'] else ''
        languages += f'<a href="{x["path"]}" lang="{x["lang"]}" hreflang="{x["lang"]}"{current}>{esc(x["name"])}</a>'
    nav = ''.join(f'<a href="#{anchor}">{esc(label)}</a>' for anchor,label in zip(['vision','architecture','direction','participate'],d['nav']))
    areas = ''.join(f'<div><dt>{esc(a[0])}</dt><dd>{esc(a[1])}</dd></div>' for a in d['areas'])
    principles = ''.join(f'<li><strong>{esc(a[0])}</strong><span>{esc(a[1])}</span></li>' for a in d['principles'])
    steps = ''.join(f'<button type="button" class="direction-choice" aria-pressed="{str(i==0).lower()}" aria-controls="direction-description" data-description="{esc(a[1])}"><span>0{i+1}</span><strong>{esc(a[0])}</strong><span aria-hidden="true">↗</span></button>' for i,a in enumerate(d['steps']))
    positions = [(13,33),(87,33),(24,83),(76,83),(50,10)]
    nodes = ''.join(f'<button class="signal-node" type="button" style="--x:{x}%;--y:{y}%" data-node="{i}" aria-pressed="{str(i==1).lower()}" aria-controls="ecosystem-description" data-description="{esc(d["exploreItems"][i][1])}"><span class="node-indicator" aria-hidden="true"></span>{esc(d["exploreItems"][i][0])}</button>' for i,(x,y) in enumerate(positions))
    paths = ''.join(f'<path data-edge="{i}" class="signal-edge{ " active" if i==1 else ""}" d="M340 220 L{x*6.8} {y*4.4}"/>' for i,(x,y) in enumerate(positions))
    ecosystem = f'<div class="ecosystem"><div class="ecosystem-heading"><span>{d["exploreLabel"]}</span><span class="diagram-code" aria-hidden="true">OAS / 01</span></div><div class="signal-map"><svg viewBox="0 0 680 440" preserveAspectRatio="none" aria-hidden="true"><circle class="orbit" cx="340" cy="220" r="155"/><circle class="orbit inner" cx="340" cy="220" r="90"/>{paths}</svg><div class="signal-core" aria-hidden="true"><span>OAS</span><small>OPEN SYSTEMS</small></div>{nodes}</div><p class="ecosystem-hint">{d["exploreNote"]}</p><p id="ecosystem-description" aria-live="polite">{esc(d["exploreItems"][1][1])}</p></div>'

    layers = ''
    for i, layer in enumerate(d['layers']):
        chips = ''.join(f'<span>{esc(label)}</span>' for label in layer[1])
        layers += f'<div class="architecture-layer" data-domain="{i}"><button type="button" class="layer-select" aria-pressed="{str(i == 0).lower()}" data-layer="{i}" aria-controls="layer-description"><span class="layer-code">0{i+1}</span><strong>{esc(layer[0])}</strong><span class="layer-plus" aria-hidden="true">↗</span></button><div class="layer-capabilities">{chips}</div><p class="layer-copy">{esc(layer[2])}</p></div>'
    journeys = ''.join(f'<button type="button" class="journey-choice" aria-pressed="false" aria-controls="journey-description" data-domains="{",".join(map(str,j[1]))}" data-description="{esc(j[2])}"><span>0{i+1}</span>{esc(j[0])}<span aria-hidden="true">↗</span></button>' for i,j in enumerate(d['journeys']))
    community = ''.join(f'<span>{esc(label)}</span>' for label in d['architectureCommunityItems'])
    architecture = f'<section id="architecture" class="architecture"><div class="architecture-head"><div><p class="label">{d["architectureLabel"]}</p><h2>{d["architectureTitle"]}</h2></div><p>{d["architectureIntro"]}</p></div><div class="journey-bar"><p class="label">{d["journeyLabel"]}</p><div class="journey-choices">{journeys}</div><p id="journey-description" aria-live="polite"></p></div><div class="architecture-map">{layers}</div><div class="architecture-detail"><p class="label">{d["architectureHint"]}</p><p id="layer-description" aria-live="polite">{esc(d["layers"][0][2])}</p></div><div class="architecture-community"><strong>{d["architectureCommunity"]}</strong><div>{community}</div></div><div class="architecture-caption"><p>{d["architectureNote"]}</p><a href="/assets/architecture.{d["lang"]}.svg" download>{d["architectureDownload"]} ↓</a></div><noscript>{"".join("<p>"+esc(j[0])+": "+esc(j[2])+"</p>" for j in d["journeys"])}</noscript></section>'
    page = f'''<!doctype html>
<html lang="{d['lang']}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(d['title'])}</title><meta name="description" content="{esc(d['description'])}">
<meta name="theme-color" content="#f4f1ea"><link rel="canonical" href="{BASE}{d['path']}">
{links}<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta property="og:type" content="website"><meta property="og:site_name" content="Open Agent Systems">
<meta property="og:title" content="{esc(d['title'])}"><meta property="og:description" content="{esc(d['description'])}">
<meta property="og:url" content="{BASE}{d['path']}"><meta property="og:image" content="{BASE}/assets/oas-banner.jpg">
<meta name="twitter:card" content="summary_large_image">
<script src="/assets/site.js" defer></script>
<link rel="icon" href="/assets/oas-avatar.jpg" type="image/jpeg"><link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">{d['skip']}</a>
<header class="site-header wrap">
<a class="brand" href="{d['path']}" aria-label="Open Agent Systems"><img src="/assets/oas-avatar.jpg" width="60" height="60" alt=""><span>Open Agent Systems</span></a>
<nav class="header-nav" aria-label="Site">{nav}</nav>
<nav class="languages" aria-label="{esc(d['language'])}">{languages}</nav>
</header>
<main id="main" class="wrap">
<section class="intro">
<div class="intro-heading"><p class="label">{d['heroKicker']}</p><h1>{d['headline']}</h1><div class="intro-text"><p>{d['intro']}</p><p>{d['introMore']}</p><div class="links"><a href="{ORG}">{d['github']} <span aria-hidden="true">↗</span></a><a href="#vision">{d['visionLabel']} <span aria-hidden="true">↓</span></a></div></div></div>{ecosystem}
</section>
<section id="vision" class="vision"><p class="label">{d['visionLabel']}</p><h2>{d['visionTitle']}</h2><p>{d['visionText']}</p></section>
{architecture}
<section id="about" class="section"><h2>{d['aboutTitle']}</h2><div class="section-body"><p>{d['aboutText']}</p><dl class="areas">{areas}</dl></div></section>
<section id="direction" class="direction"><div class="section"><h2>{d['directionTitle']}</h2><div class="section-body"><p>{d['directionIntro']}</p></div></div>
<div class="direction-explorer"><div class="direction-choices" aria-label="{esc(d['diagramTitle'])}">{steps}</div><div class="direction-panel"><p class="label">{d['directionHint']}</p><h3 id="direction-title">{esc(d['steps'][0][0])}</h3><p id="direction-description" aria-live="polite">{esc(d['steps'][0][1])}</p><p class="direction-feedback">{d['feedbackLoop']}</p></div></div><p class="direction-disclaimer">{d['directionNote']}</p><noscript><ol>{"".join("<li><strong>"+esc(a[0])+"</strong><p>"+esc(a[1])+"</p></li>" for a in d['steps'])}</ol></noscript>
</section>
<section class="section"><h2>{d['principlesTitle']}</h2><div class="section-body"><ul class="principles">{principles}</ul></div></section>
<section id="participate" class="section"><h2>{d['joinTitle']}</h2><div class="section-body"><p>{d['joinText']}</p><p class="muted">{d['joinNote']}</p><a class="issue-link" href="{ISSUES}">{d['joinButton']} <span aria-hidden="true">↗</span></a></div></section>
</main>
<footer class="site-footer wrap"><div><strong>Open Agent Systems</strong><p>{d['footer']}</p></div><div class="footer-links"><a href="{ORG}/.github">{d['community']}</a><a href="{ORG}/open-agent-systems.github.io">{d['source']}</a></div></footer>
</body></html>'''
    dest = OUT / d['path'].strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{d["path"]}</loc></url>' for d in items)+'</urlset>\n')
(OUT / '404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found · OAS</title><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap error-page"><p class="label">404 · Open Agent Systems</p><h1>Page not found</h1><p>The page may have moved, or the address may be incorrect.</p><div class="links"><a href="/">English home</a><a href="/zh/" lang="zh-CN">返回中文首页</a></div></main></body></html>''')
print(f'[PASS] Built {len(items)} language pages, 404 and discovery files')

runpy.run_path(str(ROOT / "scripts/architecture.py"))
