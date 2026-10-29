"""Export the structured capability architecture, distinct from the hero ecosystem."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
for file in (ROOT/'content').glob('*.json'):
 d=json.loads(file.read_text());st=d['strategic']
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1160" viewBox="0 0 1600 1160" role="img" aria-labelledby="title desc">',f'<title id="title">{e(d["architectureTitle"])}</title>',f'<desc id="desc">{e(d["architectureNote"])}</desc>','<rect width="1600" height="1160" fill="#fafafa"/><style>text{font-family:Arial,"PingFang SC",sans-serif;fill:#252729}</style>']
 def text(x,y,t,size=18):parts.append(f'<text x="{x}" y="{y}" font-size="{size}">{e(t)}</text>')
 text(60,60,'OPEN AGENT SYSTEMS / SYSTEM ARCHITECTURE',18);text(60,120,d['architectureTitle'],34)
 text(60,195,st['outcome'],18)
 for i,t in enumerate(st['apps']):text(420+i*360,195,t,22)
 for row,ids in enumerate([[7],[0,1,2],[3,4],[5,6]]):
  y=245+row*175;parts.append(f'<path d="M60 {y}H1540" stroke="#dadddf"/>');text(60,y+47,d['matrixLabels'][row],16)
  width=1120/len(ids)
  for j,i in enumerate(ids):
   x=390+j*width;text(x,y+47,f'0{i+1} / {d["layers"][i][0]}',20)
   for k,t in enumerate(d['layers'][i][1]):text(x,y+80+k*24,t,16)
 text(60,990,st['base'],18)
 for i,t in enumerate(st['baseItems']):text(430+i*270,990,t,17)
 text(60,1045,st['deployment'],16)
 for i,t in enumerate(st['environments']):text(450+i*250,1045,t,17)
 text(60,1090,d['architectureCommunity'],14)
 text(60,1130,'生态规划 · 拟建设的能力范围，不代表已全部交付。' if d['lang']=='zh-CN' else 'Ecosystem plan: intended capabilities, not a claim of completed delivery.',14)
 parts.append('</svg>');(ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported structured capability architecture')
