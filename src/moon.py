import numpy as np
import pygame
import info
from celestial_object import CelestialObject

pygame.init()
FONT = pygame.font.SysFont("comicsans", 16)
WIN = pygame.display.set_mode((info.WIDTH, info.HEIGHT))

class Moon(CelestialObject):
    def __init__(self, name, parent, distance, mass, radius, color, relative_velocity):
        # Position relative to parent planet
        initial_pos = parent.position + np.array([distance, 0.0])

        # Velocity = parent velocity + moon orbital velocity around parent
        initial_vel = parent.velocity + relative_velocity

        super().__init__(name, initial_pos, initial_vel, mass, color, radius)
        self.parent = parent

    def draw(self):
        """Draw the moon and its orbit trail."""
        super().draw()