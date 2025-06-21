import pygame
import numpy as np

import draw
import info
from moon import Moon
from Planet import CelestialObject, planets

pygame.init()

WIN = pygame.display.set_mode((info.WIDTH, info.HEIGHT))
FONT = pygame.font.SysFont("comicsans", 16)
RESOLUTION = np.array((info.WIDTH, info.HEIGHT))

# State Variables
show_name = True
moving = False
deltatime = 86400    # in seconds 86400 seconds = 1 day

def handle_events():
    """Handles user input events."""
    global show_name, moving, deltatime
    
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_z:
                    show_name = not show_name
                case pygame.K_UP:
                    deltatime /= 1.5
                case pygame.K_DOWN:
                    deltatime *= 1.5
                case pygame.K_t:
                    deltatime = 0
                case pygame.K_y:
                    deltatime = 14400

        if keys[pygame.K_c]:
            info.mouse_motion = np.array([0.0, 0.0])

        if event.type == pygame.MOUSEWHEEL:
            mouse_screen = np.array(pygame.mouse.get_pos(), dtype=float)
            
            # Convert to world position before zoom
            world_pos = (mouse_screen - info.mouse_motion) / CelestialObject.scale
            
            zoom_factor = 1.3 ** event.y
            CelestialObject.scale *= zoom_factor

            # Adjust camera (info.mouse_motion) so that world_pos stays under mouse
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
        for i, control in enumerate(info.controls):
            text_surface = FONT.render(control, True, info.COLOR_WHITE)
            WIN.blit(text_surface, (10, 630 + i * 20))

def main():
    """Main simulation loop."""
    
    global show_name, moving, deltatime

    running = True
    clock = pygame.time.Clock()
    sun_pos = planets[0].position
    info.mouse_motion = RESOLUTION / 2 - sun_pos * CelestialObject.scale

    while running:
        WIN.fill(info.COLOR_BLACK)
        pygame.display.set_caption(f"Solar System Simulation - FPS: {clock.get_fps():.2f}")

        running = handle_events()

        for planet in planets:
            planet.draw_name() if show_name else planet.show_distances()

        display_controls()
        
        CelestialObject.update_planets(deltatime)
        Moon.update_moons(deltatime)
        draw.display_information(deltatime)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
