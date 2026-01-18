import numpy as np
import pandas as pd
from celestial_object import CelestialObject
from moon import Moon

def load_planets():
    df = pd.read_csv("data/initial_planets.csv")
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
    
    df = pd.read_csv("data/moons_vectors.csv")
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