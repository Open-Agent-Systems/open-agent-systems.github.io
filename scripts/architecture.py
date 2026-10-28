# coding: utf-8
from pathlib import Path
from html import escape as e
import json
ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT/'content').glob('*.json'):
    d=json.loads(path.read_text())
    parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1060" viewBox="0 0 1440 1060" role="img" aria-labelledby="title desc">',f'<title id="title">Open Agent Systems — {e(d["architectureLabel"])}</title>',f'<desc id="desc">{e(d["architectureNote"])}</desc>','<style>text{font-family:Arial,"PingFang SC",sans-serif;fill:#233238}.accent{fill:#92553d}</style>','<rect width="1440" height="1060" fill="#eae7de"/>','<text x="70" y="70" font-size="20" class="accent">OPEN AGENT SYSTEMS</text>',f'<text x="70" y="130" font-size="34">{e(d["architectureTitle"])}</text>']
    for group,indices in enumerate([[0,1,2],[3,4,7],[5,6]]):
        y=205+group*225
        parts += [f'<path d="M70 {y}H1370" stroke="#bac5bf"/>',f'<text x="70" y="{y+43}" font-size="23">{e(d["architectureGroups"][group])}</text>']
        for j,i in enumerate(indices):
            layer=d['layers'][i];x=70+j*440
            parts += [f'<text x="{x}" y="{y+97}" font-size="13" class="accent">0{i+1}</text>',f'<text x="{x+32}" y="{y+97}" font-size="22">{e(layer[0])}</text>']
            for k,label in enumerate(layer[1]):
                parts.append(f'<text x="{x+32}" y="{y+128+k*23}" font-size="16">{e(label)}</text>')
    parts += ['<path d="M70 905H1370" stroke="#bac5bf"/>',f'<text x="70" y="945" font-size="20" class="accent">{e(d["architectureCommunity"])}</text>']
    for i,label in enumerate(d['architectureCommunityItems']): parts.append(f'<text x="{370+i*320}" y="945" font-size="18">{e(label)}</text>')
    note='生态规划 · 拟建设的能力范围，不代表已全部交付。' if d['lang']=='zh-CN' else 'Ecosystem plan: intended capability areas, not a claim of completed delivery.'
    parts += [f'<text x="70" y="1015" font-size="16">{e(note)}</text>','</svg>']
    (ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported bilingual capability maps')
