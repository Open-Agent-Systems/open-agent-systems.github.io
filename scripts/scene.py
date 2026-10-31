"""Shared semantic artwork for the website and downloadable capability map."""
MAP_POSITIONS = [(16,43),(48,43),(78,43),(32,77),(60,77),(52,12),(87,77),(15,12)]
HERO_POSITIONS = [(15,24),(48,24),(81,24),(22,80),(51,80),(81,80)]

# A consistent 24-unit optical grid, shared by both interactive diagrams.
ICONS = {
    'vision': '<circle cx="12" cy="12" r="9"/><path d="m16 8-2 6-6 2 2-6z"/>',
    'direction': '<path d="M5 20v-8a4 4 0 0 1 4-4h10m-4-4 4 4-4 4"/><circle cx="5" cy="20" r="2"/>',
    'community': '<circle cx="9" cy="8" r="3"/><path d="M3 21v-3a6 6 0 0 1 12 0v3M16 5a3 3 0 0 1 0 6m2 4a5 5 0 0 1 3 5"/>',
    'model': '<rect x="7" y="7" width="10" height="10" rx="3"/><path d="M9 2v3m6-3v3M9 19v3m6-3v3M2 9h3m-3 6h3m14-6h3m-3 6h3M10 10h4v4h-4z"/>',
    'agent': '<circle cx="12" cy="12" r="4"/><circle cx="4" cy="4" r="2"/><circle cx="20" cy="4" r="2"/><circle cx="12" cy="21" r="2"/><path d="m6 6 3 3m9-3-3 3m-3 7v3"/>',
    'tools': '<path d="m10 8 2-2a5 5 0 0 1 7 7l-3 3a5 5 0 0 1-7 0m5 0-2 2a5 5 0 0 1-7-7l3-3a5 5 0 0 1 7 0m-6 6 6-6"/>',
    'knowledge': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
    'sandbox': '<path d="m12 2 9 5v10l-9 5-9-5V7zM3 7l9 5 9-5m-9 5v10m-5-6 2 1m6-2 3-2"/>',
    'assets': '<path d="m12 2 10 6-10 6L2 8zM2 12l10 6 10-6M2 16l10 6 10-6"/>',
    'governance': '<path d="M12 2 3 6v6c0 5 5 8 9 10 4-2 9-5 9-10V6zM8 12l3 3 5-6"/>',
    'evaluation': '<path d="M3 3v18h18M7 15l4-5 4 3 6-8M17 5h4v4"/>',
    'developer': '<path d="m7 6-5 6 5 6m10-12 5 6-5 6M14 3l-4 18"/>',
}

def icon(kind, css='capability-icon'):
    return f'<svg class="{css}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[kind]}</svg>'

def symbol(kind, x, y):
    return f'<g class="scene-symbol" transform="translate({x} {y})"><g class="scene-glyph" transform="translate(-12 -12)">{ICONS[kind]}</g></g>'

def scene_art(hero=False):
    positions = HERO_POSITIONS if hero else MAP_POSITIONS
    height, width = (440, 600) if hero else (620, 1000)
    kinds = ['model','agent','tools','knowledge','sandbox','assets'] if hero else ['model','agent','sandbox','knowledge','assets','governance','evaluation','developer']
    coords = [(x*width/100, y*height/100-22) for x,y in positions]
    edges = [(0,1),(1,2),(3,1),(1,4),(4,5)] if hero else [(7,0),(0,1),(1,2),(3,1),(1,4),(2,6),(6,1),(4,3),(5,2)]
    parts = ['''<defs>
      <linearGradient id="node-face" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#526f99"/><stop offset=".5" stop-color="#243e62"/><stop offset="1" stop-color="#14243e"/></linearGradient>
      <linearGradient id="node-depth" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#293f62"/><stop offset="1" stop-color="#091326"/></linearGradient>
      <radialGradient id="core"><stop stop-color="#385883"/><stop offset=".65" stop-color="#1c3557"/><stop offset="1" stop-color="#0b1b32"/></radialGradient>
      <radialGradient id="core-light"><stop stop-color="#70c9ff" stop-opacity=".18"/><stop offset="1" stop-color="#70c9ff" stop-opacity="0"/></radialGradient>
    </defs>''']
    if hero:
        parts.append('''<circle cx="300" cy="222" r="128" fill="url(#core-light)"/>
        <g fill="none" stroke="#5d8ac0" stroke-width=".8" opacity=".4">
          <ellipse cx="300" cy="222" rx="240" ry="95" transform="rotate(-18 300 222)"/>
          <ellipse cx="300" cy="222" rx="210" ry="100" transform="rotate(24 300 222)"/>
          <circle cx="300" cy="222" r="72" stroke-dasharray="2 9"/>
        </g>''')
    for a,b in edges:
        x1,y1=coords[a];x2,y2=coords[b];mid=(x1+x2)/2
        parts.append(f'<path class="scene-edge" data-from="{a}" data-to="{b}" d="M{x1} {y1}C{mid} {y1},{mid} {y2},{x2} {y2}"/>')
    if hero:
        parts.append('''<rect x="251" y="182" width="98" height="98" rx="32" fill="#050d1c" stroke="#385575"/>
          <rect x="251" y="173" width="98" height="98" rx="32" fill="url(#core)" stroke="#86b6df"/>
          <path d="M266 194Q267 184 280 184H319" fill="none" stroke="#c2e8ff" stroke-opacity=".55"/>
          <text x="300" y="224" text-anchor="middle" fill="#edf8ff" font-family="Arial,sans-serif" font-size="24" font-weight="600" letter-spacing="3">OAS</text>
          <text x="300" y="245" text-anchor="middle" fill="#8cdff5" font-family="monospace" font-size="7" letter-spacing="2">CONNECTED</text>''')
    for i,((x,y),kind) in enumerate(zip(coords,kinds)):
        lens = f'''<ellipse cx="{x}" cy="{y+34}" rx="30" ry="9" fill="#020916" opacity=".55"/>
          <rect x="{x-28}" y="{y-20}" width="56" height="56" rx="18" fill="url(#node-depth)" stroke="#30496b"/>
          <rect class="node-face" x="{x-28}" y="{y-28}" width="56" height="56" rx="18" fill="url(#node-face)" stroke="#7198bf"/>
          <path d="M{x-20} {y-12}Q{x-20} {y-21} {x-10} {y-21}H{x+10}" fill="none" stroke="#ceeaff" stroke-opacity=".45"/>''' if hero else ''
        parts.append(f'<g class="scene-object" data-object="{i}">{lens}{symbol(kind,x,y)}</g>')
    return ''.join(parts)
