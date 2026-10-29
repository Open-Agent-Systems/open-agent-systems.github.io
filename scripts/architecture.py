# coding: utf-8
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT/'content').glob('*.json'):
 d=json.loads(path.read_text());s=d['strategic'];parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1150" viewBox="0 0 1600 1150" role="img" aria-labelledby="title desc">',f'<title id="title">{e(d["architectureTitle"])}</title>',f'<desc id="desc">{e(d["architectureNote"])}</desc>','<style>text{font-family:Arial,"PingFang SC",sans-serif;fill:#253445}.accent{fill:#d74600}</style>','<rect width="1600" height="1150" fill="#ffffff"/>']
 def text(x,y,label,size=18,accent=False): parts.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{"accent" if accent else ""}">{e(label)}</text>')
 def rect(x,y,w,h,fill='#f7f9fc'):parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#d8e0e8"/>')
 text(60,65,'OPEN AGENT SYSTEMS',21,True);text(60,120,d['architectureTitle'],34)
 rect(60,165,1480,95,'#fff3e8');text(85,202,s['outcome'],17,True)
 for j,label in enumerate(s['apps']):text(410+j*360,220,label,23)
 for x,w,label in [(60,330,s['left']),(415,770,s['middle']),(1210,330,s['right'])]:
  rect(x,305,w,485);text(x+20,342,label,16,True)
 def node(i,x,y,w,h):
  layer=d['layers'][i];rect(x,y,w,h,'#f7f9fc');text(x+15,y+30,layer[0],18)
  for j,label in enumerate(layer[1]):text(x+15,y+59+j*23,label,15)
 node(3,78,365,294,183);node(4,78,574,294,190)
 # Wide center nodes use horizontal capability labels.
 for i,x,y in [(7,435,365),(1,435,500)]:
  rect(x,y,730,115,'#fff7f0');text(x+18,y+32,d['layers'][i][0],21)
  for j,label in enumerate(d['layers'][i][1]):text(x+18+j*235,y+77,label,15)
 node(0,435,635,350,140);node(2,805,635,360,140)
 node(5,1228,365,294,183);node(6,1228,574,294,190)
 rect(60,825,1480,90,'#f0f3f7');text(85,860,s['base'],19,True)
 for j,label in enumerate(s['baseItems']):text(410+j*280,880,label,17)
 text(60,965,s['deployment'],17,True)
 for j,label in enumerate(s['environments']):text(440+j*250,965,label,18)
 text(60,1030,d['architectureCommunity'],17,True)
 note='生态规划 · 拟建设的能力范围，不代表已全部交付。' if d['lang']=='zh-CN' else 'Ecosystem plan: intended capabilities, not a claim of completed delivery.'
 text(60,1090,note,16);parts.append('</svg>');(ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported strategic system architecture')
