# coding: utf-8
"""Export the same isometric capability landscape as a standalone SVG."""
from pathlib import Path
from html import escape as e
import json,re
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT/'content').glob('*.json'):
 d=json.loads(path.read_text());s=d['strategic']
 html=(ROOT/'docs'/d['path'].strip('/')/'index.html').read_text()
 landscape=re.search(r'<svg class="iso-map-svg"[^>]*>(.*?)</svg>',html).group(1)
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1250" viewBox="0 0 1600 1250" role="img" aria-labelledby="title desc">',f'<title id="title">{e(d["architectureTitle"])}</title>',f'<desc id="desc">{e(d["architectureNote"])}</desc>','<style>text{font-family:Arial,"PingFang SC",sans-serif;fill:#354b57}.iso-map-connections{fill:none;stroke:#9eb2bd;stroke-width:1.3;stroke-dasharray:4 8}</style>','<rect width="1600" height="1250" fill="#f5f8f9"/>']
 def text(x,y,label,size=18):parts.append(f'<text x="{x}" y="{y}" font-size="{size}">{e(label)}</text>')
 text(60,60,'OPEN AGENT SYSTEMS / CAPABILITY MAP',18);text(60,115,d['architectureTitle'],34)
 parts.append('<rect x="60" y="150" width="1480" height="80" fill="#f7eee7" stroke="#d9c1af"/>');text(85,197,s['outcome'],18)
 for j,label in enumerate(s['apps']):text(430+j*360,197,label,23)
 parts.append('<g transform="translate(60 250) scale(1.48 1.3)">'+landscape)
 coords=[(390,440),(500,280),(650,440),(130,245),(130,395),(870,245),(870,395),(500,125)]
 for i,(x,y) in enumerate(coords):
  parts.append(f'<rect x="{x-97}" y="{y-31}" width="194" height="80" fill="#cedbe1"/><rect x="{x-101}" y="{y-37}" width="194" height="80" fill="#ffffff" stroke="#adc1cc"/>')
  text(x-90,y-15,f'0{i+1} / {d["layers"][i][0]}',12)
  for j,label in enumerate(d['layers'][i][1]):text(x-90,y+2+j*15,label,10)
 parts.append('</g>')
 parts.append('<rect x="60" y="1040" width="1480" height="70" fill="#e8eff2" stroke="#d4dfe5"/>');text(85,1082,s['base'],20)
 for j,label in enumerate(s['baseItems']):text(430+j*270,1082,label,17)
 text(60,1158,s['deployment'],17)
 for j,label in enumerate(s['environments']):text(450+j*250,1158,label,18)
 note='生态规划 · 拟建设的能力范围，不代表已全部交付。' if d['lang']=='zh-CN' else 'Ecosystem plan: intended capabilities, not a claim of completed delivery.'
 text(60,1190,d['architectureCommunity'],14);text(60,1220,note,14);parts.append('</svg>');(ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported isometric system architecture')
