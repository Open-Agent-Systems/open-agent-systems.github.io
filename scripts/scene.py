"""Shared semantic artwork for the website and downloadable capability map."""
MAP_POSITIONS = [(16,43),(48,43),(78,43),(32,77),(60,77),(52,12),(87,77),(15,12)]
HERO_POSITIONS = [(15,32),(48,32),(81,32),(22,76),(51,76),(81,76)]

def symbol(kind, x, y):
    artwork = {
        'model': '<path d="M-54-24H-30Q-16-24-16-10V0H28M-54 0H28M-54 24H-30Q-16 24-16 10V0"/><circle cx="-54" cy="-24" r="5"/><circle cx="-54" cy="0" r="5"/><circle cx="-54" cy="24" r="5"/><path d="M12-17L34 0 12 17"/>',
        'agent': '<circle class="symbol-halo" r="49"/><circle class="symbol-core" r="23"/><path d="M-18-16L-35-31M18-16L35-31M0 23V42"/><circle cx="-39" cy="-35" r="9"/><circle cx="39" cy="-35" r="9"/><circle cy="49" r="9"/><path d="M-7 0H7M0-7V7"/>',
        'sandbox': '<path class="symbol-volume" d="M0-40L48-16V30L0 53-48 30V-16Z"/><path d="M-48-16L0 8 48-16M0 8V53"/><path d="M-16-7L-4 0-16 7M6 10H22"/>',
        'knowledge': '<ellipse class="symbol-volume" rx="43" ry="13" cy="-21"/><path d="M-43-21V18C-43 36 43 36 43 18V-21M-43-2C-43 16 43 16 43-2M-43 16C-43 34 43 34 43 16"/>',
        'assets': '<path class="symbol-volume" d="M-36-12L0-33 40-12 4 9Z"/><path d="M-36 0L4 22 40 0M-36 14L4 36 40 14"/><circle cx="49" cy="-29" r="10"/><path d="M45-29H53M49-33V-25"/>',
        'governance': '<path class="symbol-volume" d="M0-29L24-20V0Q24 19 0 30Q-24 19-24 0V-20Z"/><path d="M-10 0L-2 8 12-9"/>',
        'evaluation': '<path d="M-40 23H42M-40 23V-26M-31 11L-12-9 5 0 27-24"/><circle cx="27" cy="-24" r="5"/>',
        'developer': '<path d="M-22-18L-44 0-22 18M22-18L44 0 22 18M9-25L-9 25"/>',
        'tools': '<circle cx="-24" r="15"/><circle cx="24" r="15"/><path d="M-9 0H9M-39 0H-55M39 0H55M-24-15V-29M24 15V29"/>',
    }
    return f'<g class="scene-symbol" transform="translate({x} {y})"><g class="scene-glyph"><g transform="scale(.30)" stroke-width="4">{artwork[kind]}</g></g></g>'

def scene_art(hero=False):
    positions = HERO_POSITIONS if hero else MAP_POSITIONS
    height = 440 if hero else 620
    width = 600 if hero else 1000
    kinds = ['model','agent','tools','knowledge','sandbox','assets'] if hero else ['model','agent','sandbox','knowledge','assets','governance','evaluation','developer']
    coords = [(x*width/100, y*height/100-22) for x,y in positions]
    edges = [(0,1),(1,2),(3,1),(1,4),(4,5)] if hero else [(7,0),(0,1),(1,2),(3,1),(1,4),(2,6),(6,1),(4,3),(5,2)]
    parts = []
    if hero:
        parts.append('<defs><radialGradient id="pearl" cx="30%" cy="20%" r="85%"><stop stop-color="#ffffff"/><stop offset=".7" stop-color="#dce8f0"/><stop offset="1" stop-color="#9db6c6"/></radialGradient><radialGradient id="core" cx="30%" cy="20%" r="90%"><stop stop-color="#7c9baa"/><stop offset=".5" stop-color="#365664"/><stop offset="1" stop-color="#172f3b"/></radialGradient><filter id="soft"><feGaussianBlur stdDeviation="8"/></filter></defs><ellipse cx="300" cy="270" rx="180" ry="45" fill="#8aa4b1" opacity=".12" filter="url(#soft)"/><g fill="none" stroke="#a6becb" stroke-width=".8"><ellipse cx="300" cy="220" rx="235" ry="90" transform="rotate(-16 300 220)"/><ellipse cx="300" cy="220" rx="202" ry="100" transform="rotate(22 300 220)"/></g><circle cx="300" cy="222" r="45" fill="url(#core)"/><circle cx="300" cy="222" r="50" fill="none" stroke="#ccdbe3"/><text x="300" y="226" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif" font-size="20" letter-spacing="2">OAS</text>')
    if hero:
        pass
    else:
        parts.append('<path class="scene-field" d="M80 175Q480 70 920 170V390Q500 570 80 390Z"/><path class="scene-boundary" d="M170 145Q520-65 900 145M910 170Q1050 350 900 510M135 500Q410 605 760 540"/>')
    for a,b in edges:
        x1,y1=coords[a];x2,y2=coords[b];mid=(x1+x2)/2
        parts.append(f'<path class="scene-edge" data-from="{a}" data-to="{b}" d="M{x1} {y1}C{mid} {y1},{mid} {y2},{x2} {y2}"/>')
    for i,((x,y),kind) in enumerate(zip(coords,kinds)):
        lens = f'<ellipse cx="{x}" cy="{y+9}" rx="25" ry="19" fill="#728e9f" opacity=".2"/><circle cx="{x}" cy="{y}" r="24" fill="url(#pearl)" stroke="#c3d5df"/>' if hero else ''
        parts.append(f'<g class="scene-object" data-object="{i}">{lens}{symbol(kind,x,y)}</g>')
    return ''.join(parts)
