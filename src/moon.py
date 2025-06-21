import numpy as np
import pygame
import info
from Planet import CelestialObject, planets

pygame.init()
FONT = pygame.font.SysFont("comicsans", 16)
WIN = pygame.display.set_mode((info.WIDTH, info.HEIGHT))

class Moon(CelestialObject):
    def __init__(self, name, parent_planet, radius, color, distance, mass, orbital_period=None):
        super().__init__(name, parent_planet.position, parent_planet.velocity, mass, color, radius)
        self.parent_planet = parent_planet
        self.distance = distance
        self.orbital_angle = 0  

        if orbital_period is None:
            self.orbital_period = 2 * np.pi * np.sqrt(distance**3 / (info.G * parent_planet.mass))
        else:
            self.orbital_period = orbital_period  

    def draw(self):
        """Draw the moon at its current position relative to its parent planet."""
        offset = np.array([
            np.cos(self.orbital_angle), 
            np.sin(self.orbital_angle)
        ]) * self.distance

        abs_moon_pos = self.parent_planet.position + offset
        moon_pos = self.get_screen_position(abs_moon_pos)

        pygame.draw.circle(WIN, self.color, moon_pos.astype(int), self.radius)

        name_text = FONT.render(self.name, True, info.COLOR_WHITE)
        WIN.blit(name_text, (moon_pos[0] - name_text.get_width() / 2,
                             moon_pos[1] - name_text.get_height() / 2 - 20))

    def update_position(self, deltatime):
        """Update the moon’s position using its orbital period."""
        self.orbital_angle += (2 * np.pi / self.orbital_period) * deltatime  

        self.position = self.parent_planet.position + np.array([
            np.cos(self.orbital_angle), 
            np.sin(self.orbital_angle)
        ]) * self.distance

    @classmethod
    def update_moons(cls, deltatime):
        """Update and draw all moons."""
        for moon in moons:
            moon.update_position(deltatime)
            moon.draw()

moon = Moon('Moon', planets[3], 2, info.COLOR_WHITE, 0.1 * info.AU, 7.346e22, 2.36e6)  
# europa = Moon('Europa', planets[5], 1, info.COLOR_WHITE, 0.1 * info.AU, 4.81e22, 3.06e5)  

moons = [moon]
