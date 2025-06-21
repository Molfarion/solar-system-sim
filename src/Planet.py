import numpy as np
import pygame
import info
from collections import deque
import pandas as pd

RESOLUTION = np.array((info.WIDTH, info.HEIGHT))
WIN = pygame.display.set_mode(RESOLUTION)
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
        sun_pos = planets[0].position
        return np.linalg.norm(sun_pos - self.position)

    def get_screen_position(self, position=None):
        """Convert a world position to screen coordinates."""
        if position is None:
            position = self.position
        return (position * self.scale) + info.mouse_motion

    def draw_name(self):
        x, y = self.get_screen_position()
        text = FONT.render(self.name, True, info.COLOR_WHITE)
        WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2 - 20))

    def show_distances(self):
        if self != planets[0]:
            x, y = self.get_screen_position()
            au = self.calculate_distance_to_sun() / info.AU
            text = FONT.render(f"{au:.4f} AU", True, info.COLOR_WHITE)
            WIN.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2 - 20))

    def update_position(self, deltatime):
        self.acceleration = np.zeros_like(self.position)
        for other in planets:
            if other != self:
                r_vec = other.position - self.position
                r_mag = np.linalg.norm(r_vec)
                self.acceleration += info.G * other.mass / r_mag**3 * r_vec
        self.velocity += self.acceleration * deltatime
        self.position += self.velocity * deltatime
        self.orbit.append(self.position.copy())

    def draw(self):
        pos = self.get_screen_position()
        radius_px = max(min(self.radius, self.scale * info.AU / 20), 3)
        pygame.draw.circle(WIN, self.color, pos.astype(int), int(radius_px))

        if len(self.orbit) > 2:
            orbit_pts = (np.array(self.orbit) * self.scale + info.mouse_motion).astype(int)
            pygame.draw.lines(WIN, self.color, False, orbit_pts, 1)

    @classmethod
    def update_planets(cls, deltatime):
        for planet in planets:
            planet.update_position(deltatime)
            planet.draw()


def get_color(color_name):
    return getattr(info, color_name, (255, 255, 255))


df = pd.read_csv("src/initial_planets.csv")

planets = [
    CelestialObject(
        row["name"],
        [row["position_x"], row["position_y"]],
        [row["velocity_x"], row["velocity_y"]],
        row["mass"],
        get_color(row["color"]),
        row["radius"]
    )
    for _, row in df.iterrows()
]
