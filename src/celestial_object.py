import numpy as np
import pygame
from collections import deque
import info

class CelestialObject:
    scale = 150 / info.AU
    sun = None   # set in main.py

    def __init__(self, name, position, velocity, mass, color, radius):
        self.name = name
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.acceleration = np.zeros(2, dtype=np.float64)
        self.mass = mass
        self.color = color
        self.radius = radius
        self.orbit = deque(maxlen=300)

    def compute_acceleration(self, bodies):
        self.acceleration[:] = 0
        for other in bodies:
            if other is self:
                continue
            r_vec = other.position - self.position
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 0:
                self.acceleration += info.G * other.mass / r_mag**3 * r_vec

    def update_position(self, dt, bodies):
        self.velocity += 0.5 * self.acceleration * dt
        self.position += self.velocity * dt
        self.compute_acceleration(bodies)
        self.velocity += 0.5 * self.acceleration * dt
        self.orbit.append(self.position.copy())

    def get_screen_position(self):
        return self.position * self.scale + info.mouse_motion

    def draw(self, win, font):
        self.screen_pos = self.get_screen_position()
        
        pos = self.screen_pos.astype(int)
        radius_px = max(int(self.radius), 3)
        pygame.draw.circle(win, self.color, pos, radius_px)

        if len(self.orbit) > 2:
            pts = (np.array(self.orbit) * self.scale + info.mouse_motion).astype(int)
            pygame.draw.lines(win, self.color, False, pts, 1)

    def draw_name(self, win, font):
        x, y = self.get_screen_position()
        label = font.render(self.name, True, info.COLOR_WHITE)
        win.blit(label, (x - label.get_width() / 2, y - 25))

    def show_distances(self, win, font):
        if CelestialObject.sun is None or self is CelestialObject.sun:
            return

        x, y = self.get_screen_position()
        
        distance_vector = self.position - CelestialObject.sun.position
        distance_au = np.linalg.norm(distance_vector) / info.AU

        text = font.render(f"{distance_au:.4f} AU", True, info.COLOR_WHITE)
        text_y = y - text.get_height() / 2 - 45
        
        win.blit(text, (x - text.get_width() / 2, text_y))
