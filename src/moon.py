import numpy as np
import pygame
import info
from celestial_object import CelestialObject

class Moon(CelestialObject):
    def __init__(self, name, parent, distance, mass, radius, color, relative_velocity):
        # Position relative to parent planet
        initial_pos = parent.position + np.array([distance, 0.0])

        # Velocity = parent velocity + moon orbital velocity around parent
        initial_vel = parent.velocity + relative_velocity

        super().__init__(name, initial_pos, initial_vel, mass, color, radius)
        self.parent = parent
        self.orbit_store_interval = 3600 # Store orbit point every hour
        self.tail_lifetime = 2629800

    def store_orbit_point(self, total_time_elapsed, is_selected=False):
        """Store position relative to parent - detailed when parent is selected"""
        interval = self.detailed_orbit_interval if is_selected else self.base_orbit_store_interval
        
        if total_time_elapsed - self.last_orbit_store_time >= interval:
            relative_pos = self.position - self.parent.position
            self.orbit_data.append((relative_pos.copy(), total_time_elapsed))
            self.last_orbit_store_time = total_time_elapsed
            
            while self.orbit_data and (total_time_elapsed - self.orbit_data[0][1] > self.tail_lifetime):
                self.orbit_data.popleft()

    def draw(self, win):
        self.screen_pos = self.get_screen_position().astype(int)
        radius_px = max(int(self.radius),3)
        pygame.draw.circle(win, self.color, self.screen_pos, radius_px)

        if len(self.orbit_data) > 2:
            min_scale_for_moons = 150 / info.AU * 10

            if self.scale >= min_scale_for_moons:
                parent_screen_pos = self.parent.position * self.scale + info.mouse_motion
                positions = np.array([item[0] for item in self.orbit_data])
                pts = (positions * self.scale + parent_screen_pos).astype(int)
                pygame.draw.lines(win, self.color, False, pts, 1)
        