from pathlib import Path
from html import escape
import json
ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT/'content').glob('*.json'):
    d=json.loads(path.read_text()); e=escape
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1040" viewBox="0 0 1440 1040" role="img" aria-labelledby="title desc">',f'<title id="title">Open Agent Systems — {e(d["architectureLabel"])}</title>',f'<desc id="desc">{e(d["architectureIntro"])} {e(d["architectureNote"])}</desc>', '<style>text{font-family:Arial,"PingFang SC","Microsoft YaHei",sans-serif;fill:#f4f1ea}.muted{fill:#aab4b5}.accent{fill:#e1a18a}</style>','<rect width="1440" height="1040" fill="#141f24"/>','<text x="80" y="85" font-size="24">OPEN AGENT SYSTEMS</text>',f'<text x="80" y="140" font-size="36" font-weight="600">{e(d["architectureLabel"])}</text>']
    for i,layer in enumerate(d['layers']):
        y=190+i*200
        parts += [f'<rect x="80" y="{y}" width="1280" height="148" rx="4" fill="#1c2b31" stroke="#46565b"/>',f'<text x="110" y="{y+43}" font-size="14" class="accent">L{3-i}</text>',f'<text x="160" y="{y+45}" font-size="25" font-weight="600">{e(layer[0])}</text>']
        n=len(layer[1]); w=1210/n
        for j,label in enumerate(layer[1]):
            x=110+j*w
            parts += [f'<rect x="{x}" y="{y+72}" width="{w-16}" height="49" fill="#23373f"/>',f'<text x="{x+18}" y="{y+103}" font-size="20">{e(label)}</text>']
        if i<2:
            parts += [f'<path d="M720 {y+187}V{y+159}m-6 6 6-6 6 6" fill="none" stroke="#e1a18a" stroke-width="2"/>']
    parts += ['<path d="M100 770H1340" stroke="#738084" stroke-dasharray="5 7"/>',f'<text x="110" y="820" font-size="23" class="accent">{e(d["architectureCommunity"])}</text>']
    for i,label in enumerate(d['architectureCommunityItems']):
        parts += [f'<text x="{370+i*330}" y="820" font-size="20">{e(label)}</text>']
    if d['lang']=='zh-CN':
        notes=['规划视图 · 以下是拟建设的能力范围，不代表已经全部交付。','组织的生态能力视图，不是单一产品的部署架构。']
    else:
        notes=['Planning view: intended capability areas, not a claim of completed delivery.','An ecosystem capability map, not the deployment architecture of a single product.']
    for i,note in enumerate(notes): parts += [f'<text x="80" y="{920+i*32}" font-size="18" class="muted">{e(note)}</text>']
    parts += ['</svg>']
    (ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported bilingual SVG architecture diagrams')
