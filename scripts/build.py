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
    nav = ''.join(f'<a href="#{anchor}">{esc(label)}</a>' for anchor,label in zip(['about','direction','participate'],d['nav']))
    areas = ''.join(f'<div><dt>{esc(a[0])}</dt><dd>{esc(a[1])}</dd></div>' for a in d['areas'])
    principles = ''.join(f'<li><strong>{esc(a[0])}</strong><span>{esc(a[1])}</span></li>' for a in d['principles'])
    steps = ''.join(f'<li><span class="roadmap-point" aria-hidden="true"></span><h3>{esc(a[0])}</h3><p>{esc(a[1])}</p></li>' for a in d['steps'])
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
<a class="brand" href="{d['path']}" aria-label="Open Agent Systems"><img src="/assets/oas-avatar.jpg" width="60" height="60" alt=""><span>Open Agent Systems</span></a>
<nav class="languages" aria-label="{esc(d['language'])}">{languages}</nav>
</header>
<main id="main" class="wrap">
<section class="intro">
<div class="intro-heading"><p class="label">{d['label']}</p><h1>{d['headline']}</h1><nav class="section-nav" aria-label="{esc(d['nav'][0])}">{nav}</nav></div>
<div class="intro-text"><p>{d['intro']}</p><p>{d['introMore']}</p><div class="links"><a href="{ORG}">{d['github']} <span aria-hidden="true">↗</span></a><a href="{ISSUES}">{d['feedback']} <span aria-hidden="true">↗</span></a></div></div>
</section>
<section id="about" class="section"><h2>{d['aboutTitle']}</h2><div class="section-body"><p>{d['aboutText']}</p><dl class="areas">{areas}</dl></div></section>
<section id="direction" class="direction"><div class="section"><h2>{d['directionTitle']}</h2><div class="section-body"><p>{d['directionIntro']}</p></div></div>
<figure class="roadmap" aria-label="{esc(d['diagramTitle'])}"><ol>{steps}</ol><div class="feedback-path"><span>{d['feedbackLoop']}</span></div><figcaption>{d['directionNote']}</figcaption></figure>
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
