import pygame
import numpy as np
import system
import config
import info
import draw
from camera import Camera
from moon import Moon

class Simulation:
    def __init__(self):
        self.planets = system.load_planets()
        self.moons = system.create_moons(self.planets)
        self.bodies = self.planets + self.moons
        
        self.camera = Camera(config.WIDTH, config.HEIGHT, 150 / info.AU)
        self.sun = self.planets[0] if self.planets else None
        
        self.selected_body = self.sun
        if self.selected_body:
            self.camera.set_target(self.selected_body)

        self.show_name = True
        self.dragging = False
        self.deltatime = config.DEFAULT_DELTATIME
        self.total_time_elapsed = 0.0

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
                        self.camera.center_on_origin()
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
                self.camera.set_target(None)

                for body in self.bodies:
                    # Calculate live screen position for accurate clicking
                    screen_pos = self.camera.world_to_screen(body.position)
                    dist = np.linalg.norm(screen_pos - np.array([mx, my]))
                    click_radius = max(body.radius * self.camera.scale, 15) 
                    if dist < click_radius:
                        self.selected_body = body
                        self.camera.set_target(body)
                        break
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.camera.handle_pan(event.rel)
            
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.3 ** event.y
                self.camera.handle_zoom(zoom_factor, np.array(pygame.mouse.get_pos()))
        
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
                is_selected = (body == self.selected_body)
                if isinstance(body, Moon):
                    # Also consider parent selection for detailed orbits
                    is_selected = is_selected or (body.parent == self.selected_body)
                
                body.store_orbit_point(self.total_time_elapsed, is_selected)
        return
    
    def render(self, WIN, FONT, clock):
        self.camera.update()

        if self.selected_body is not None:
            draw.indicator_for_planet(WIN, self.selected_body, self.camera)
        
        for body in self.bodies:
            body.draw(WIN, self.camera, self.selected_body)
            if self.show_name:
                body.draw_name(WIN, FONT, self.camera)
            else:
                if isinstance(body, Moon):
                    body.show_distances(WIN, FONT, self.camera)
                else:
                    body.show_distances(WIN, FONT, self.camera, self.sun)
        
        draw.display_controls(WIN, FONT)
        draw.display_simulation_status(WIN, FONT, self.deltatime, self.total_time_elapsed, clock.get_fps())
        draw.draw_scale_indicator(WIN, FONT, self.camera)
        return 

    def restart(self):
        """Reset the simulation state to initial CSV values."""
        self.__init__()