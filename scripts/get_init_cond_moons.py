from astroquery.jplhorizons import Horizons
import pandas as pd
import numpy as np
import os

# Output to project data directory regardless of cwd
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_PROJECT_ROOT, "data")

MOON_DATA = {
    'Moon':    {'id': '301', 'parent_id': '399', 'parent_name': 'Earth',   'mass': 7.342e22,  'color': (128, 128, 128), 'radius': 2},
    'Deimos':  {'id': '402', 'parent_id': '499', 'parent_name': 'Mars',    'mass': 1.4762e15, 'color': (140, 140, 130), 'radius': 1},
    'Io':      {'id': '501', 'parent_id': '599', 'parent_name': 'Jupiter', 'mass': 8.9319e22, 'color': (255, 230, 100), 'radius': 3},
    'Titan':   {'id': '606', 'parent_id': '699', 'parent_name': 'Saturn',  'mass': 1.3452e23, 'color': (255, 200, 120), 'radius': 4},
    'Titania': {'id': '703', 'parent_id': '799', 'parent_name': 'Uranus',  'mass': 3.527e21,  'color': (200, 190, 180), 'radius': 2},
    'Triton':  {'id': '801', 'parent_id': '899', 'parent_name': 'Neptune', 'mass': 2.139e22,  'color': (200, 200, 220), 'radius': 3},
}

AU = 149597870700  
DAY = 86400
target_date = '2025-01-01'
rows = []

for name, props in MOON_DATA.items():
    # Set location to '@parent_id' to get relative coordinates
    obj = Horizons(id=props['id'], 
                   location=f"@{props['parent_id']}", 
                   epochs={'start': target_date, 'stop': '2025-01-02', 'step': '1d'})
    
    vec = obj.vectors(refplane='ecliptic')

    rows.append({
        'parent_planet': props['parent_name'],
        'name': name,
        'rel_pos_x_m': vec['x'][0] * AU,
        'rel_pos_y_m': vec['y'][0] * AU,
        'rel_vel_x_ms': vec['vx'][0] * AU / DAY,
        'rel_vel_y_ms': vec['vy'][0] * AU / DAY,
        'mass_kg': props['mass'],
        'radius_px': props['radius'],
        'color_r': props['color'][0],
        'color_g': props['color'][1],
        'color_b': props['color'][2]
    })

df = pd.DataFrame(rows)
os.makedirs(_DATA_DIR, exist_ok=True)
df.to_csv(os.path.join(_DATA_DIR, "moons_vectors.csv"), index=False)