# coding: utf-8
"""Export the website's semantic system landscape as a standalone SVG."""
from pathlib import Path
from html import escape as e
import json
from scene import scene_art, MAP_POSITIONS
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT/'content').glob('*.json'):
 d=json.loads(path.read_text());s=d['strategic']
 parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1560" viewBox="0 0 1600 1560" role="img" aria-labelledby="title desc">',f'<title id="title">{e(d["architectureTitle"])}</title>',f'<desc id="desc">{e(d["architectureNote"])}</desc>','<style>text{font-family:Arial,"PingFang SC",sans-serif;fill:#354b57}.scene-field{fill:#e8eef2;opacity:.3}.scene-boundary{fill:none;stroke:#c5a48f;stroke-dasharray:3 9}.scene-symbol{fill:#f8fafb;stroke:#688393;stroke-width:1.7;stroke-linejoin:round;stroke-linecap:round}.symbol-core,.symbol-volume{fill:#e4edf1}.symbol-halo{fill:none;stroke:#c6d5de;stroke-dasharray:2 7}.scene-edge{fill:none;stroke:#bdcdd6;stroke-width:1.2}</style>','<rect width="1600" height="1560" fill="#f8fafb"/>']
 def text(x,y,label,size=18,center=False):parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{"middle" if center else "start"}">{e(label)}</text>')
 text(60,60,'OPEN AGENT SYSTEMS / CAPABILITY MAP',18);text(60,115,d['architectureTitle'],34)
 text(60,190,s['outcome'],18)
 for j,label in enumerate(s['apps']):text(430+j*360,190,label,23)
 parts.append('<g transform="translate(60 250) scale(1.48 1.3)">'+scene_art())
 for i,(x,y) in enumerate(MAP_POSITIONS):text(x*10,y*6.2+20,f'0{i+1} / {d["layers"][i][0]}',13,True)
 parts.append('</g>')
 text(60,1085,s['base'],20)
 for j,label in enumerate(s['baseItems']):text(430+j*270,1085,label,17)
 for i,layer in enumerate(d['layers']):
  x=60+(i%4)*380;y=1150+(i//4)*145
  text(x,y,f'0{i+1} / {layer[0]}',17)
  for j,label in enumerate(layer[1]):text(x,y+27+j*23,label,14)
 text(60,1455,s['deployment'],17)
 for j,label in enumerate(s['environments']):text(450+j*250,1455,label,18)
 note='生态规划 · 拟建设的能力范围，不代表已全部交付。' if d['lang']=='zh-CN' else 'Ecosystem plan: intended capabilities, not a claim of completed delivery.'
 text(60,1490,d['architectureCommunity'],14);text(60,1530,note,14);parts.append('</svg>');(ROOT/'docs/assets'/f'architecture.{d["lang"]}.svg').write_text('\n'.join(parts))
print('[PASS] Exported system landscape')
