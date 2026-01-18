import numpy as np
import pygame
import info
from celestial_object import CelestialObject

class Moon(CelestialObject):
    def __init__(self, name, parent, rel_pos, rel_vel, mass, radius, color):
        initial_pos = parent.position + rel_pos
        initial_vel = parent.velocity + rel_vel

        super().__init__(name, initial_pos, initial_vel, mass, color, radius)
        self.parent = parent
        
        # Corrected: Defined consistent interval names used in store_orbit_point
        self.base_orbit_store_interval = 3600 
        self.detailed_orbit_interval = 1800
        self.last_orbit_store_time = 0
        self.tail_lifetime = 2629800

        self.min_scale_for_moons = (150 / info.AU) * 5

    def compute_acceleration(self, bodies):
        self.acceleration[:] = 0
        
        r_vec = self.parent.position - self.position
        r_mag = np.linalg.norm(r_vec)
        if r_mag > 0:
            self.acceleration += info.G * self.parent.mass / r_mag**3 * r_vec
        
        self.acceleration += self.parent.acceleration
        
    def store_orbit_point(self, total_time_elapsed, is_selected=False):
        """Store position relative to parent - detailed when parent is selected"""
        interval = self.detailed_orbit_interval if is_selected else self.base_orbit_store_interval
        
        if total_time_elapsed - self.last_orbit_store_time >= interval:
            relative_pos = self.position - self.parent.position
            self.orbit_data.append((relative_pos.copy(), total_time_elapsed))
            self.last_orbit_store_time = total_time_elapsed
            
            while self.orbit_data and (total_time_elapsed - self.orbit_data[0][1] > self.tail_lifetime):
                self.orbit_data.popleft()

    def draw(self, win, selected_body=None):
        self.screen_pos = self.get_screen_position().astype(int)
        radius_px = max(int(self.radius), 3)
        pygame.draw.circle(win, self.color, self.screen_pos, radius_px)

        if selected_body == self.parent and len(self.orbit_data) > 2:
            current_scale = CelestialObject.scale 
            if current_scale >= self.min_scale_for_moons:
                parent_screen_pos = self.parent.get_screen_position()
                rel_positions = np.array([item[0] for item in self.orbit_data])
                
                pts = (rel_positions * current_scale + parent_screen_pos).astype(int)
                if len(pts) > 1:
                    pygame.draw.aalines(win, self.color, False, pts)
    
    def draw_name(self, win, font):
        current_scale = CelestialObject.scale 
        if current_scale >= self.min_scale_for_moons:
            return super().draw_name(win, font)
    
    def show_distances(self, win, font):
        current_scale = CelestialObject.scale 
        if current_scale >= self.min_scale_for_moons:
            x, y = self.get_screen_position()
            
            distance_vector = self.position - self.parent.position
            distance_km = np.linalg.norm(distance_vector)/1000

            text = font.render(f"{distance_km:.2f} km", True, info.COLOR_WHITE)
            text_y = y - text.get_height() / 2 - 30
            
            win.blit(text, (x - text.get_width() / 2, text_y))