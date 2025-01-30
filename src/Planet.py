import numpy as np
import pygame
import timeit
import info
from collections import deque
import pandas as pd

RESOLUTION = np.array((info.WIDTH, info.HEIGHT))
WIN = pygame.display.set_mode((RESOLUTION))
FONT = pygame.font.SysFont("comicsans", 16)

class CelestialObject:
    scale = 150 / info.AU

    def __init__(self, name, position, velocity, mass, color, radius):
        self.name = name
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.acceleration = np.zeros_like(position)
        self.mass = mass
        self.color = color
        self.radius = radius
        self.orbit = deque(maxlen=300) 

    def calculate_distance_to_sun(self):
        planet_vec = planets[0].position - self.position
        return np.linalg.norm(planet_vec)

    def draw_name(self):
        x, y = self.calculate_my_position()
        name_text = FONT.render(self.name, 1, info.COLOR_WHITE)
        WIN.blit(name_text, (x - name_text.get_width() / 2, y - name_text.get_height() / 2 - 20))

    def show_distances(self):
        if self != planets[0]:
            x, y = self.calculate_my_position()
            distance_text = FONT.render(f"{self.calculate_distance_to_sun() / info.AU:.4f} AU", 1, info.COLOR_WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2 - 20))

    def update_position(self, deltatime):
        self.acceleration = np.zeros_like(self.position)
        for other_planet in planets:
            if other_planet != self:
                r_vec = other_planet.position - self.position
                r_mag = np.linalg.norm(r_vec)
                self.acceleration += info.G * other_planet.mass / r_mag**3 * r_vec
        self.velocity += self.acceleration * deltatime
        self.position += self.velocity * deltatime
        self.orbit.append(self.position.copy())

    def calculate_position(self, position):
        return info.mouse_motion + (position * self.scale) + RESOLUTION / 2

    def calculate_my_position(self):
        return self.calculate_position(self.position)

    def draw(self):
        object_pos = self.calculate_my_position()
        radius = max(min(self.radius, self.scale * info.AU / 20), 3)
        pygame.draw.circle(WIN, self.color, object_pos.astype(int), int(radius))

        orbit_np = np.array(self.orbit)
        orbit_np = (orbit_np * self.scale + RESOLUTION / 2 + info.mouse_motion).astype(int)
        if len(self.orbit) > 2:
            pygame.draw.lines(WIN, self.color, False, orbit_np, 1)

    @classmethod
    def update_planets(cls, deltatime):
        for planet in planets:
            planet.update_position(deltatime)
            planet.draw()


df = pd.read_csv("planets.csv")

def get_color(color_name):
    return getattr(info, color_name, (255, 255, 255))

planets = [CelestialObject(row["name"], [row["position_x"], row["position_y"]], 
                           [row["velocity_x"], row["velocity_y"]], row["mass"], 
                           get_color(row["color"]), row["radius"]) for _, row in df.iterrows()]
                           