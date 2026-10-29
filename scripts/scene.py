"""Shared semantic artwork for the website and downloadable capability map."""
MAP_POSITIONS = [(16,43),(48,43),(78,43),(32,77),(60,77),(52,12),(87,77),(15,12)]
HERO_POSITIONS = [(15,32),(48,32),(81,32),(22,76),(51,76),(81,76)]

# A consistent 24-unit optical grid, shared by both interactive diagrams.
ICONS = {
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
    height = 440 if hero else 620
    width = 600 if hero else 1000
    kinds = ['model','agent','tools','knowledge','sandbox','assets'] if hero else ['model','agent','sandbox','knowledge','assets','governance','evaluation','developer']
    coords = [(x*width/100, y*height/100-22) for x,y in positions]
    edges = [(0,1),(1,2),(3,1),(1,4),(4,5)] if hero else [(7,0),(0,1),(1,2),(3,1),(1,4),(2,6),(6,1),(4,3),(5,2)]
    parts = []
    if hero:
        parts.append('<defs><radialGradient id="pearl" cx="30%" cy="20%" r="85%"><stop stop-color="#ffffff"/><stop offset=".7" stop-color="#dce8f0"/><stop offset="1" stop-color="#9db6c6"/></radialGradient><radialGradient id="core" cx="30%" cy="20%" r="90%"><stop stop-color="#7c9baa"/><stop offset=".5" stop-color="#365664"/><stop offset="1" stop-color="#172f3b"/></radialGradient><filter id="soft"><feGaussianBlur stdDeviation="8"/></filter></defs><ellipse cx="300" cy="270" rx="180" ry="45" fill="#8aa4b1" opacity=".12" filter="url(#soft)"/><g fill="none" stroke="#7d9cab" stroke-width=".8" opacity=".65"><ellipse cx="300" cy="220" rx="235" ry="90" transform="rotate(-16 300 220)"/><ellipse cx="300" cy="220" rx="202" ry="100" transform="rotate(22 300 220)"/></g>')
    if hero:
        pass
    else:
        parts.append('<path class="scene-field" d="M80 175Q480 70 920 170V390Q500 570 80 390Z"/><path class="scene-boundary" d="M170 145Q520-65 900 145M910 170Q1050 350 900 510M135 500Q410 605 760 540"/>')
    for a,b in edges:
        x1,y1=coords[a];x2,y2=coords[b];mid=(x1+x2)/2
        parts.append(f'<path class="scene-edge" data-from="{a}" data-to="{b}" d="M{x1} {y1}C{mid} {y1},{mid} {y2},{x2} {y2}"/>')
    if hero:
        parts.append('<circle cx="300" cy="222" r="45" fill="url(#core)"/><circle cx="300" cy="222" r="50" fill="none" stroke="#ccdbe3"/><text x="300" y="226" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="20" letter-spacing="2">OAS</text>')
    for i,((x,y),kind) in enumerate(zip(coords,kinds)):
        lens = f'<ellipse cx="{x}" cy="{y+9}" rx="25" ry="19" fill="#728e9f" opacity=".2"/><circle cx="{x}" cy="{y}" r="25" fill="url(#pearl)" stroke="#a4bdcc"/>' if hero else ''
        parts.append(f'<g class="scene-object" data-object="{i}">{lens}{symbol(kind,x,y)}</g>')
    return ''.join(parts)
