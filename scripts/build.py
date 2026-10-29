from pathlib import Path
from html import escape as esc
import json
import runpy
import hashlib
from scene import scene_art, MAP_POSITIONS, HERO_POSITIONS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
ASSET_VERSIONS = {name: hashlib.sha256((OUT / 'assets' / name).read_bytes()).hexdigest()[:12] for name in ['site.css', 'site.js']}
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
    eco = d['ecosystemView']
    coords = HERO_POSITIONS
    mode_buttons = ''.join(f'<button type="button" class="eco-mode" data-mode="{i}" aria-pressed="{str(i==0).lower()}" aria-controls="eco-stage eco-summary">{esc(m[0])}</button>' for i,m in enumerate(eco['modes']))
    eco_nodes = ''.join(f'<button type="button" class="eco-node" data-eco-node="{i}" style="--nx:{coords[i][0]}%;--ny:{coords[i][1]}%" aria-pressed="{str(i==0).lower()}" aria-controls="eco-detail"><span class="eco-number">0{i+1}</span><strong>{esc(n[0])}</strong><span class="eco-dot" aria-hidden="true"></span></button>' for i,n in enumerate(eco['nodes']))
    eco_data = esc(json.dumps(eco,ensure_ascii=False))
    fallback = ''.join(f'<p>{esc(n[0])}: {esc(n[1])}</p>' for n in eco['nodes'])
    hero_decks = scene_art(hero=True)
    ecosystem = f'''<div class="ecosystem eco-panel" data-eco="{eco_data}"><div class="ecosystem-heading"><span>{esc(eco['title'])}</span><span class="diagram-code">OAS / OPEN SYSTEMS</span></div><div class="eco-modes" aria-label="{esc(eco['title'])}">{mode_buttons}</div><h2 class="scene-title">{esc(eco["sceneTitles"][0])}</h2><p class="eco-apps">{esc(eco['apps'])}</p><div id="eco-stage" class="eco-stage"><svg class="iso-hero" viewBox="0 0 600 440" preserveAspectRatio="none" aria-hidden="true">{hero_decks}</svg><svg class="eco-wires" viewBox="0 0 600 440" preserveAspectRatio="none" aria-hidden="true"><g class="eco-links"></g></svg><div class="eco-core"><strong>OAS</strong><span>{esc(eco['modes'][0][1])}</span><small class="eco-progress">01 / 06</small></div>{eco_nodes}</div><div class="iso-level-key">{''.join(f'<span>0{i+1} / {esc(label)}</span>' for i,label in enumerate(d['iso']['heroLayers']))}</div><div class="eco-governance"><strong>{esc(eco['governance'])}</strong><span>{esc(eco['guards'])}</span></div><p id="eco-summary">{esc(eco['modes'][0][2])}</p><div class="eco-toolbar"><span>{esc(eco['note'])}</span><button class="eco-toggle" type="button" hidden>{esc(eco['play'])}</button></div><p id="eco-detail">{esc(eco['nodes'][0][1])}</p><noscript>{fallback}</noscript></div>'''

    labels = d['explorerLabels']
    insights = []
    module_positions = MAP_POSITIONS
    def capability(i):
        layer = d['layers'][i]
        info = d['capabilityInsights'][i]
        chips = ''.join(f'<span>{esc(label)}</span>' for label in layer[1])
        related = ''.join(f'<button type="button" class="related-capability" data-target="{j}">{esc(d["layers"][j][0])} <span aria-hidden="true">↗</span></button>' for j in info[2])
        insights.append(f'''<div class="node-insight" id="insight-{i}" hidden><p class="insight-code">CAPABILITY / 0{i+1}</p><h3>{esc(layer[0])}</h3><p>{esc(layer[2])}</p><dl><dt>{esc(labels['input'])}</dt><dd>{esc(info[0])}</dd><dt>{esc(labels['output'])}</dt><dd>{esc(info[1])}</dd></dl><p class="insight-label">{esc(labels['related'])}</p><div class="related-capabilities">{related}</div><button type="button" class="insight-close" data-close="{i}">{esc(labels['close'])} ↑</button></div>''')
        x,y = module_positions[i]
        return f'<div class="architecture-layer" data-domain="{i}" data-related="{",".join(map(str,info[2]))}" style="--mx:{x}%;--my:{y}%"><button type="button" class="layer-select" aria-expanded="false" data-layer="{i}" aria-controls="insight-{i}"><span class="layer-code">0{i+1}</span><strong>{esc(layer[0])}</strong><span class="layer-plus" aria-hidden="true">↗</span></button><noscript><p>{esc(layer[2])}</p></noscript></div>'
    st = d['strategic']
    apps = ''.join(f'<span>{esc(x)}</span>' for x in st['apps'])
    base_items = ''.join(f'<span>{esc(x)}</span>' for x in st['baseItems'])
    environments = ''.join(f'<span>{esc(x)}</span>' for x in st['environments'])
    modules = ''.join(capability(i) for i in range(8))
    decks = scene_art()
    group_labels = ''
    layers = f'''<div class="system-outcome"><span class="system-eyebrow">{esc(st['outcome'])}</span><div>{apps}</div></div><div class="iso-explorer"><div class="iso-landscape"><svg class="iso-map-svg" viewBox="0 0 1000 620" preserveAspectRatio="none" aria-hidden="true">{decks}</svg>{group_labels}{modules}<p class="iso-map-legend">{esc(d['iso']['legend'])}</p></div><aside class="capability-inspector" aria-label="{esc(d['iso']['detailTitle'])}"><div class="inspector-welcome"><span class="inspector-symbol" aria-hidden="true">↗</span><h3>{esc(d['iso']['detailTitle'])}</h3><p>{esc(d['iso']['detailText'])}</p></div>{''.join(insights)}</aside></div><div class="system-base"><strong>{esc(st['base'])}</strong><div>{base_items}</div></div><div class="system-environments"><span>{esc(st['deployment'])}</span><div>{environments}</div></div>'''
    journeys = ''.join(f'<button type="button" class="journey-choice" aria-pressed="false" aria-controls="journey-description" data-domains="{",".join(map(str,j[1]))}" data-steps="{esc(json.dumps(d["journeySteps"][i],ensure_ascii=False))}" data-description="{esc(j[2])}"><span>0{i+1}</span>{esc(j[0])}<span aria-hidden="true">↗</span></button>' for i,j in enumerate(d['journeys']))
    community = ''.join(f'<span>{esc(label)}</span>' for label in d['architectureCommunityItems'])
    architecture = f'<section id="architecture" class="architecture"><div class="architecture-head"><div><p class="label">{d["architectureLabel"]}</p><h2>{d["architectureTitle"]}</h2></div><p>{d["architectureIntro"]}</p></div><div class="journey-bar"><div class="journey-choices"><button type="button" class="overview-choice" aria-pressed="true">{esc(labels["overview"])}</button>{journeys}</div><p id="journey-description" aria-live="polite"></p></div><div class="journey-stepper" aria-label="{esc(d["journeyLabel"])}"></div><div class="explorer-toolbar"><span>{esc(labels["hint"])}</span><button type="button" class="explorer-reset">{esc(labels["reset"])}</button></div><div class="architecture-map">{layers}</div><p class="system-principle">{esc(st["relation"])}</p><div class="architecture-caption"><p>{d["architectureNote"]}</p><a href="/assets/architecture.{d["lang"]}.svg" download>{d["architectureDownload"]} ↓</a></div><noscript>{"".join("<p>"+esc(j[0])+": "+esc(j[2])+"</p>" for j in d["journeys"])}</noscript></section>'
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
<script src="/assets/site.js?v={ASSET_VERSIONS["site.js"]}" defer></script>
<link rel="icon" href="/assets/oas-avatar.jpg" type="image/jpeg"><link rel="stylesheet" href="/assets/site.css?v={ASSET_VERSIONS["site.css"]}">
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
