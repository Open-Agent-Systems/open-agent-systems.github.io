# coding: utf-8
from pathlib import Path
from html import escape as e
import json
ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT/'content').glob('*.json'):
    d=json.loads(path.read_text())
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1120" viewBox="0 0 1440 1120" role="img" aria-labelledby="title desc">',f'<title id="title">Open Agent Systems — {e(d["architectureLabel"])}</title>',f'<desc id="desc">{e(d["architectureNote"])}</desc>','<style>text{font-family:Arial,"PingFang SC",sans-serif;fill:#eff2ed}.accent{fill:#e1a18a}</style>','<rect width="1440" height="1120" fill="#141f24"/>','<text x="70" y="70" font-size="22" class="accent">OPEN AGENT SYSTEMS</text>',f'<text x="70" y="125" font-size="32">{e(d["architectureTitle"])}</text>']
    for i,layer in enumerate(d['layers']):
        x=70+(i%2)*660; y=170+(i//2)*190
        parts += [f'<rect x="{x}" y="{y}" width="640" height="170" fill="#1c2b31" stroke="#526a73"/>',f'<text x="{x+24}" y="{y+38}" font-size="14" class="accent">0{i+1}</text>',f'<text x="{x+24}" y="{y+77}" font-size="26">{e(layer[0])}</text>']
        for j,label in enumerate(layer[1]):
            parts.append(f'<text x="{x+24+j*204}" y="{y+125}" font-size="17">{e(label)}</text>')
    parts += [f'<text x="70" y="970" font-size="22" class="accent">{e(d["architectureCommunity"])}</text>']
    for i,label in enumerate(d['architectureCommunityItems']):
        parts.append(f'<text x="{360+i*320}" y="970" font-size="20">{e(label)}</text>')
    note='生态规划 · 拟建设的能力范围，不代表已全部交付。' if d['lang']=='zh-CN' else 'Ecosystem plan: intended capability areas, not a claim of completed delivery.'
    parts += [f'<text x="70" y="1050" font-size="18">{e(note)}</text>','</svg>']
    (ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported bilingual capability maps')
