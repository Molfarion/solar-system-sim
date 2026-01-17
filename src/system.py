import numpy as np
import pandas as pd
from celestial_object import CelestialObject
from moon import Moon
import info

def load_planets():
    df = pd.read_csv("src/initial_planets.csv")
    planets = []

    for _, row in df.iterrows():
        planets.append(
            CelestialObject(
                row["name"],
                [row["position_x"], row["position_y"]],
                [row["velocity_x"], row["velocity_y"]],
                row["mass"],
                getattr(info, row["color"]),
                row["radius"]
            )
        )
    return planets

def create_moons(planets):
    earth = planets[3]

    MOON_DISTANCE = 3.844e8      # meters
    MOON_MASS = 7.346e22         # kg

    def orbital_speed(M, r):
        return np.sqrt(info.G * M / r)

    speed = orbital_speed(earth.mass, MOON_DISTANCE)

    offset = np.array([MOON_DISTANCE, 0.0])

    earth_v = earth.velocity

    perp = np.array([-earth_v[1], earth_v[0]])
    perp = perp / np.linalg.norm(perp)

    velocity_offset = perp * speed

    total_mass = earth.mass + MOON_MASS
    earth.position -= offset * (MOON_MASS / total_mass)
    earth.velocity -= velocity_offset * (MOON_MASS / total_mass)

    moon_position = earth.position + offset
    moon_velocity = earth.velocity + velocity_offset

    moon = Moon(
        name="Moon",
        parent=earth,
        distance=MOON_DISTANCE,
        mass=MOON_MASS,
        radius=2,
        color=info.COLOR_WHITE,
        relative_velocity=velocity_offset
    )

    moon.position = moon_position
    moon.velocity = moon_velocity

    return [moon]