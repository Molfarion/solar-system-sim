from astroquery.jplhorizons import Horizons
import pandas as pd

PLANET_DATA = {
    'Sun':     {'id': 10, 'mass': 1.98847e30, 'color': 'COLOR_SUN',     'radius': 13},
    'Mercury': {'id': 199,'mass': 3.3011e23,  'color': 'COLOR_MERCURY', 'radius': 4},
    'Venus':   {'id': 299,'mass': 4.8675e24,  'color': 'COLOR_VENUS',   'radius': 7},
    'Earth':   {'id': 399,'mass': 5.97237e24, 'color': 'COLOR_EARTH',   'radius': 8},
    'Mars':    {'id': 499,'mass': 6.4171e23,  'color': 'COLOR_MARS',    'radius': 6},
    'Jupiter': {'id': 599,'mass': 1.8982e27,  'color': 'COLOR_JUPITER', 'radius': 11},
    'Saturn':  {'id': 699,'mass': 5.6834e26,  'color': 'COLOR_SATURN',  'radius': 12},
    'Uranus':  {'id': 799,'mass': 8.6810e25,  'color': 'COLOR_URANUS',  'radius': 11},
    'Neptune': {'id': 899,'mass': 1.02413e26, 'color': 'COLOR_NEPTUNE', 'radius': 10},
    'Pluto':   {'id': 999,'mass': 1.303e22,   'color': 'COLOR_PLUTO',   'radius': 4},
}
AU = 149.6*10**9
DAY = 86400
target_date = '2025-01-01'
end_date = '2025-01-02'
rows = []

for name, props in PLANET_DATA.items():
    obj = Horizons(id=props['id'], location='@10',
                   epochs={'start': target_date, 'stop': end_date, 'step': '1d'})
    vec = obj.vectors()

    rows.append({
        'name': name,
        'position_y': int(vec['y'][0]*AU),
        'position_x': int(vec['x'][0]*AU), # AU
        'velocity_x': int(vec['vx'][0]*AU/DAY), # AU / d
        'velocity_y': int(vec['vy'][0]*AU/DAY),
        'mass': props['mass'],  
        'color': props['color'],
        'radius': props['radius'],
    })

df = pd.DataFrame(rows)
df.to_csv("inital_planets.csv", index=False)