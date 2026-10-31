"""Shared semantic artwork for the website and downloadable capability map."""
MAP_POSITIONS = [(16,43),(48,43),(78,43),(32,77),(60,77),(52,12),(87,77),(15,12)]
HERO_POSITIONS = [(16,25),(50,25),(84,25),(16,78),(50,78),(84,78)]
HERO_HEIGHT = 360
HERO_NODE_OFFSET = 28

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
    if hero:
        return balanced_hero_art()
    kinds = ['model','agent','sandbox','knowledge','assets','governance','evaluation','developer']
    coords = [(x*1000/100, y*620/100-22) for x,y in MAP_POSITIONS]
    edges = [(7,0),(0,1),(1,2),(3,1),(1,4),(2,6),(6,1),(4,3),(5,2)]
    parts = ['<path class="scene-field" d="M80 175Q480 70 920 170V390Q500 570 80 390Z"/><path class="scene-boundary" d="M170 145Q520-65 900 145M910 170Q1050 350 900 510M135 500Q410 605 760 540"/>']
    for a,b in edges:
        x1,y1=coords[a];x2,y2=coords[b];mid=(x1+x2)/2
        parts.append(f'<path class="scene-edge" data-from="{a}" data-to="{b}" d="M{x1} {y1}C{mid} {y1},{mid} {y2},{x2} {y2}"/>')
    for i,((x,y),kind) in enumerate(zip(coords,kinds)):
        parts.append(f'<g class="scene-object" data-object="{i}">{symbol(kind,x,y)}</g>')
    return ''.join(parts)


def balanced_hero_art():
    """Keep nodes circular, the center light, and relationship lines in one JS layer."""
    parts = ['''<defs>
      <linearGradient id="node-surface" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset="1" stop-color="#eff1f2"/></linearGradient>
      <filter id="node-shadow" x="-50%" y="-50%" width="200%" height="220%"><feDropShadow dx="0" dy="3" stdDeviation="3" flood-color="#252729" flood-opacity=".08"/></filter>
    </defs>
    <g class="hero-center">
      <circle cx="300" cy="180" r="37" fill="#fafafa" stroke="#dadddf" stroke-width=".8"/>
      <circle cx="300" cy="180" r="31" fill="#eceeef" stroke="#d0d5d8" stroke-width=".8"/>
      <text x="300" y="185" text-anchor="middle" fill="#444b50" font-family="Arial,sans-serif" font-size="17" font-weight="500" letter-spacing="1.5">OAS</text>
    </g>''']
    for i, ((px,py),kind) in enumerate(zip(HERO_POSITIONS,['model','agent','tools','knowledge','sandbox','assets'])):
        x,y=px*6,py*HERO_HEIGHT/100-HERO_NODE_OFFSET
        parts.append(f'''<g class="scene-object" data-object="{i}"><g class="balanced-node">
          <circle class="node-face" cx="{x}" cy="{y}" r="24" fill="url(#node-surface)" stroke="#c7cdd1" stroke-width="1" filter="url(#node-shadow)"/>
          {symbol(kind,x,y)}
        </g></g>''')
    return ''.join(parts)
