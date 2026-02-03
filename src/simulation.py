import pygame
import numpy as np
import system
import config
import info
import draw
from celestial_object import CelestialObject
from moon import Moon

class Simulation:
    def __init__(self):
        self.planets = system.load_planets()
        self.moons = system.create_moons(self.planets)
        self.bodies = self.planets + self.moons
        
        self.selected_body = self.planets[0] if self.planets else None
        self.show_name = True
        self.dragging = False
        self.deltatime = config.DEFAULT_DELTATIME
        self.total_time_elapsed = 0.0
        
        if self.selected_body:
            CelestialObject.sun = self.selected_body

    def handle_events(self):
        """Handles user input events. Returns False if the game should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False
            
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_z:
                        self.show_name = not self.show_name
                    case pygame.K_PLUS | pygame.K_EQUALS:
                        self.deltatime *= 1.5
                    case pygame.K_MINUS:
                        self.deltatime /= 1.5
                    case pygame.K_SPACE:
                        if self.deltatime != 0:
                            self.last_deltatime = self.deltatime
                            self.deltatime = 0
                        else:
                            self.deltatime = getattr(self, 'last_deltatime', 43200)
                    case pygame.K_c:
                        info.mouse_motion[:] = info.RESOLUTION / 2
                        self.selected_body = None
                    case pygame.K_q:
                        for body in self.bodies:
                            body.orbit_data.clear() 
                    case pygame.K_r:
                        self.restart()
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.dragging = True
                mx, my = pygame.mouse.get_pos()
                self.selected_body = None

                for body in self.bodies:
                    # body.screen_pos needs to be calculated in your draw/update logic
                    dist = np.linalg.norm(body.screen_pos - np.array([mx, my]))
                    click_radius = max(body.radius * CelestialObject.scale, 15) 
                    if dist < click_radius:
                        self.selected_body = body
                        break
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                info.mouse_motion += np.array(event.rel)
            
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.3 ** event.y
                CelestialObject.scale *= zoom_factor
                
                if self.selected_body is None:
                    old_scale = CelestialObject.scale / zoom_factor
                    mouse_screen = np.array(pygame.mouse.get_pos(), dtype=float)
                    world_pos = (mouse_screen - info.mouse_motion) / old_scale
                    info.mouse_motion = mouse_screen - world_pos * CelestialObject.scale
        
        return True
    
    def update_physics(self):
        if self.deltatime > 0:
            self.total_time_elapsed += self.deltatime
            sub_dt = self.deltatime / config.SUBSTEPS
            
            # Compute initial acceleration for all bodies
            for body in self.bodies:
                body.compute_acceleration(self.bodies)
            
            for _ in range(config.SUBSTEPS):
                for body in self.bodies:
                    body.update_position(sub_dt, self.bodies)
            
            for body in self.bodies:
                # Moons only store data if parent is selected
                if isinstance(body, Moon):
                    if body.parent == self.selected_body:
                        body.store_orbit_point(self.total_time_elapsed, is_selected=True)
                else:
                    # Planets always store data
                    is_selected = (body == self.selected_body)
                    body.store_orbit_point(self.total_time_elapsed, is_selected)
        return
    
    def render(self, WIN, FONT, clock):

        if self.selected_body is not None:
            # Keep the selected planet at the center of the screen
            info.mouse_motion[:] = info.RESOLUTION / 2 - self.selected_body.position * CelestialObject.scale
            draw.indicator_for_planet(WIN, self.selected_body)
        
        for body in self.bodies:
            body.draw(WIN, self.selected_body)
            if self.show_name:
                body.draw_name(WIN, FONT)
            else:
                body.show_distances(WIN, FONT)
        
        draw.display_controls(WIN, FONT)
        draw.display_simulation_status(WIN, FONT, self.deltatime, self.total_time_elapsed, clock.get_fps())
        draw.draw_scale_indicator(WIN, FONT)
        return 

    def restart(self):
        """Reset the simulation state to initial CSV values."""
        self.__init__()
        print("Simulation state reloaded from data files.")