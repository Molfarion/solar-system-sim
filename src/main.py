import pygame
import numpy as np
import info
import draw
from celestial_object import CelestialObject
from system import load_planets, create_moons

pygame.init()

planets = load_planets()
moons = create_moons(planets)
bodies = planets + moons

WIN = pygame.display.set_mode((info.WIDTH, info.HEIGHT))
FONT = pygame.font.SysFont(["ubuntumono", "arial", "sans-serif"], 16)
RESOLUTION = np.array((info.WIDTH, info.HEIGHT))
SUBSTEPS = 15  # Number of integration steps per frame for stability

selected_body = None
show_name = True
dragging = False  
deltatime = 86400 # 1 day in seconds (default 1 day = 1 tick in simulation)

def lock_camera_to_body(body):
    """Hard-lock camera so body stays at screen center."""
    info.mouse_motion[:] = RESOLUTION / 2 - body.position * CelestialObject.scale

def handle_events():
    """Handles user input events (camera control, speed control, toggles)."""
    global show_name, dragging, deltatime, selected_body  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False
        
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_z:
                    show_name = not show_name
                case pygame.K_PLUS | pygame.K_EQUALS:
                    deltatime *= 1.5
                case pygame.K_MINUS:
                    deltatime /= 1.5
                case pygame.K_SPACE:
                    if deltatime != 0:
                        info.last_deltatime = deltatime
                        deltatime = 0
                    else:
                        deltatime = getattr(info, 'last_deltatime', 86400)
                case pygame.K_c:
                    info.mouse_motion[:] = RESOLUTION / 2
                    selected_body = None  
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            mx, my = pygame.mouse.get_pos()
            selected_body = None
            for body in bodies:
                dist = np.hypot(*(body.screen_pos - np.array([mx, my])))
                if dist < body.radius * CelestialObject.scale + 20:
                    selected_body = body
                    break
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False
        
        elif event.type == pygame.MOUSEMOTION and dragging:
            selected_body = None
            info.mouse_motion += np.array(event.rel)
        
        elif event.type == pygame.MOUSEWHEEL:
            zoom_factor = 1.3 ** event.y
            CelestialObject.scale *= zoom_factor
            
            if selected_body is None:
                # Mouse-anchored zoom only when not locked to a body
                old_scale = CelestialObject.scale / zoom_factor
                mouse_screen = np.array(pygame.mouse.get_pos(), dtype=float)
                world_pos = (mouse_screen - info.mouse_motion) / old_scale
                info.mouse_motion = mouse_screen - world_pos * CelestialObject.scale
    
    return True

def display_controls():
    """Displays controls if 'X' is pressed."""
    if pygame.key.get_pressed()[pygame.K_x]:
        for i, text in enumerate(info.controls):
            surf = FONT.render(text, True, info.COLOR_WHITE)
            WIN.blit(surf, (10, info.HEIGHT - 150 + i * 20))

def main():
    global deltatime, selected_body
    
    total_time_elapsed = 0.0
    clock = pygame.time.Clock()
    running = True
    sun = planets[0]
    CelestialObject.sun = sun
    lock_camera_to_body(sun)
    stars = draw.generate_stars(40)
    
    while running:
        WIN.fill(info.COLOR_BLACK)
        draw.draw_stars(stars, WIN)
        pygame.display.set_caption(f"Solar System Simulation - FPS: {clock.get_fps():.2f}")
        
        running = handle_events()
        if not running:
            break
        
        if deltatime > 0:
            total_time_elapsed += deltatime
            sub_dt = deltatime / SUBSTEPS
            
            # Compute initial acceleration for all bodies
            for body in bodies:
                body.compute_acceleration(bodies)
            
            for _ in range(SUBSTEPS):
                for body in bodies:
                    body.update_position(sub_dt, bodies)
            
            for body in bodies:
                is_selected = (body == selected_body)
    
                if hasattr(body, 'parent') and body.parent == selected_body:
                    is_selected = True
                    
                body.store_orbit_point(total_time_elapsed, is_selected)
        
        if selected_body is not None:
            draw.indicator_for_planet(WIN, selected_body)
            # Keep the selected planet at the center of the screen
            info.mouse_motion[:] = RESOLUTION / 2 - (selected_body.position * CelestialObject.scale)
        
        for body in bodies:
            body.draw(WIN)
        
        for planet in planets:
            if show_name:
                planet.draw_name(WIN, FONT)
            else:
                planet.show_distances(WIN, FONT)
        
        display_controls()
        draw.display_simulation_status(WIN, FONT, deltatime, total_time_elapsed, clock.get_fps())
        draw.draw_scale_indicator(WIN, FONT)
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()