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
FONT = pygame.font.SysFont("comicsans", 16)
RESOLUTION = np.array((info.WIDTH, info.HEIGHT))

SUBSTEPS = 10           # Number of integration steps per frame for stability
show_name = True        
moving = False          
deltatime = 86400      
info.TOTAL_TIME_ELAPSED = 0.0 

def handle_events():
    """Handles user input events (camera control, speed control, toggles)."""
    global show_name, moving, deltatime

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_z:
                    show_name = not show_name
                
                case pygame.K_PLUS | pygame.K_EQUALS:  # Speed Up
                    deltatime *= 1.5
                case pygame.K_MINUS:                   # Slow Down
                    deltatime /= 1.5
                case pygame.K_SPACE:                   # Toggle Pause
                    if deltatime != 0:
                        info.last_deltatime = deltatime
                        deltatime = 0
                    else:
                        deltatime = getattr(info, 'last_deltatime', 86400) # Default to 1 day
                case pygame.K_c:                     
                    info.mouse_motion[:] = np.array([info.WIDTH/2, info.HEIGHT/2])
        
        # Mouse Zoom
        if event.type == pygame.MOUSEWHEEL:
            mouse_screen = np.array(pygame.mouse.get_pos(), dtype=float)

            # Preserve the world point under the cursor during zoom
            world_pos = (mouse_screen - info.mouse_motion) / CelestialObject.scale

            zoom_factor = 1.3 ** event.y
            CelestialObject.scale *= zoom_factor

            # Recalculate camera offset
            info.mouse_motion = mouse_screen - world_pos * CelestialObject.scale

        if event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            moving = False
        elif event.type == pygame.MOUSEMOTION and moving:
            info.mouse_motion += np.array(event.rel)

    return True

def display_controls():
    """Displays controls if 'X' is pressed."""
    if pygame.key.get_pressed()[pygame.K_x]:
        for i, text in enumerate(info.controls):
            surf = FONT.render(text, True, info.COLOR_WHITE)
            WIN.blit(surf, (10, info.HEIGHT - 150 + i * 20))

def main():
    global deltatime

    clock = pygame.time.Clock()
    running = True
    
    sun = planets[0]
    CelestialObject.sun = sun
    info.mouse_motion[:] = RESOLUTION / 2 - sun.position * CelestialObject.scale
    
    stars = draw.generate_stars(40) 

    while running:
        WIN.fill(info.COLOR_BLACK)
        draw.draw_stars(stars, WIN)
        pygame.display.set_caption(f"Solar System Simulation - FPS: {clock.get_fps():.2f}")

        running = handle_events()
        if not running:
            break

        if deltatime > 0:
            info.TOTAL_TIME_ELAPSED += deltatime
            
            # Substep implementation for stability
            sub_dt = deltatime / SUBSTEPS
            
            # Compute initial acceleration for all bodies
            for body in bodies:
                body.compute_acceleration(bodies)
            
            for _ in range(SUBSTEPS):
                for body in bodies:
                    body.update_position(sub_dt, bodies)
        
        for body in bodies:
            body.draw(WIN, FONT)

        for planet in planets:
            if show_name:
                planet.draw_name(WIN, FONT)
            else:
                planet.show_distances(WIN, FONT) 

        for moon in moons:
            if show_name:
                pass
                # moon.draw_name(WIN, FONT)
        
        display_controls()
        draw.display_simulation_status(WIN, FONT, deltatime, info.TOTAL_TIME_ELAPSED)
        draw.draw_scale_indicator(WIN, FONT) 

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()