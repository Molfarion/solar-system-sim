import os
import numpy as np
import pandas as pd
from celestial_object import CelestialObject
from moon import Moon

# Resolve data paths relative to project root (works from any cwd)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PLANETS_CSV = os.path.join(_PROJECT_ROOT, "data", "initial_planets.csv")
_MOONS_CSV = os.path.join(_PROJECT_ROOT, "data", "moons_vectors.csv")


def load_planets():
    if not os.path.isfile(_PLANETS_CSV):
        raise FileNotFoundError(
            f"Planets data not found: {_PLANETS_CSV}. "
            "Run from project root or ensure data/initial_planets.csv exists."
        )
    try:
        df = pd.read_csv(_PLANETS_CSV)
    except Exception as e:
        raise RuntimeError(f"Failed to read planets CSV {_PLANETS_CSV}: {e}") from e
    planets = []

    for _, row in df.iterrows():
        planets.append(
            CelestialObject(
                name = row["name"],
                position =[row["position_x"], row["position_y"]],
                velocity = [row["velocity_x"], row["velocity_y"]],
                mass = row["mass"],
                color=(row['color_r'], row['color_g'], row['color_b']),
                radius =row["radius"]
            )
        )
    return planets


def create_moons(planets):
    planet_dict = {planet.name: planet for planet in planets}

    if not os.path.isfile(_MOONS_CSV):
        return []
    try:
        df = pd.read_csv(_MOONS_CSV)
    except Exception as e:
        raise RuntimeError(f"Failed to read moons CSV {_MOONS_CSV}: {e}") from e
    moons = []

    for _, row in df.iterrows():
        parent_name = row['parent_planet']
        if parent_name in planet_dict:
            parent = planet_dict[parent_name]

            rel_pos = np.array([row['rel_pos_x_m'], row['rel_pos_y_m']])
            rel_vel = np.array([row['rel_vel_x_ms'], row['rel_vel_y_ms']])

            moon = Moon(
                name = row['name'],
                parent = parent,
                rel_pos = rel_pos,  
                rel_vel = rel_vel,  
                mass = float(row['mass_kg']),
                radius = row['radius_px'],
                color = (row['color_r'], row['color_g'], row['color_b'])
            )
            moons.append(moon)
    
    return moons

def restart_system():
    new_planets = load_planets()
    new_moons = create_moons(new_planets)
    
    return new_planets, new_moons