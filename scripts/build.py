from pathlib import Path
from html import escape as esc
import json

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
    nav = ''.join(f'<a href="#{anchor}">{esc(label)}</a>' for anchor,label in zip(['purpose','focus','principles'],d['nav']))
    areas = ''.join(f'<article class="area"><span class="area-index">0{i+1}</span><div><h3>{esc(a[0])}</h3><p>{esc(a[1])}</p></div><span class="area-tag">{esc(a[2])}</span></article>' for i,a in enumerate(d['areas']))
    principles = ''.join(f'<article><span class="principle-index">0{i+1}</span><h3>{esc(a[0])}</h3><p>{esc(a[1])}</p></article>' for i,a in enumerate(d['principles']))
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
<link rel="icon" href="/assets/oas-avatar.jpg" type="image/jpeg"><link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">{d['skip']}</a>
<header class="site-header wrap">
<a class="brand" href="{d['path']}" aria-label="Open Agent Systems"><span class="brand-symbol" aria-hidden="true">o<span>a</span>s<span class="brand-dot">.</span></span><span class="brand-name">Open Agent<br>Systems</span></a>
<nav class="main-nav" aria-label="{esc(d['nav'][0])}">{nav}</nav>
<nav class="languages" aria-label="{esc(d['language'])}">{languages}</nav>
</header>
<main id="main">
<section class="hero wrap">
<div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span>{d['eyebrow']}</p>
<h1>{d['headline']}<br><em>{d['headlineAccent']}</em></h1>
<p class="hero-intro">{d['intro']}</p>
<div class="hero-actions"><a class="button" href="{ORG}">{d['primary']} <span aria-hidden="true">↗</span></a><a class="text-link" href="#purpose">{d['secondary']} <span aria-hidden="true">↓</span></a></div></div>
<figure class="hero-art"><div class="art-heading"><span>{d['visualLabel']}</span><span aria-hidden="true">[ OAS ]</span></div><img src="/assets/oas-avatar.jpg" width="512" height="512" alt="Open Agent Systems (OAS)" fetchpriority="high"><figcaption><span class="small-square" aria-hidden="true"></span>{d['visualCaption']}</figcaption></figure>
</section>
<section id="purpose" class="purpose wrap section"><div><p class="eyebrow">{d['purposeLabel']}</p><h2>{d['purposeTitle']}</h2></div><div class="purpose-body"><p class="lead">{d['purposeText']}</p><p>{d['purposeNote']}</p></div></section>
<section id="focus" class="focus wrap section"><div class="section-intro"><div><p class="eyebrow">{d['focusLabel']}</p><h2>{d['focusTitle']}</h2></div><p>{d['focusIntro']}</p></div><div class="areas">{areas}</div></section>
<section id="principles" class="principles"><div class="wrap section"><p class="eyebrow">{d['principlesLabel']}</p><h2>{d['principlesTitle']}</h2><div class="principle-grid">{principles}</div></div></section>
<section class="join wrap section"><p class="eyebrow">{d['joinLabel']}</p><h2>{d['joinTitle']}</h2><p>{d['joinText']}</p><div class="hero-actions"><a class="button" href="{ISSUES}">{d['joinButton']} <span aria-hidden="true">↗</span></a><a class="text-link" href="{ORG}">{d['joinSecondary']} <span aria-hidden="true">↗</span></a></div></section>
</main>
<footer class="site-footer wrap"><div><strong>Open Agent Systems</strong><p>{d['footer']}</p></div><div class="footer-right"><a href="{ORG}">GitHub ↗</a><span>{d['footerNote']}</span></div></footer>
</body></html>'''
    dest = OUT / d['path'].strip('/') / 'index.html'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page)
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{d["path"]}</loc></url>' for d in items)+'</urlset>\n')
(OUT / '404.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Page not found · OAS</title><link rel="stylesheet" href="/assets/site.css"></head><body><main class="wrap section join"><p class="eyebrow">404 / OPEN AGENT SYSTEMS</p><h1>This path is still open.</h1><p>The page you’re looking for isn’t here.</p><div class="hero-actions"><a class="button" href="/">English home ↗</a><a class="text-link" href="/zh/" lang="zh-CN">返回中文首页 ↗</a></div></main></body></html>''')
print(f'[PASS] Built {len(items)} language pages, 404 and discovery files')
