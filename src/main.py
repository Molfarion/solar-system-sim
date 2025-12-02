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

# Simulation state
SUBSTEPS = 10
show_name = True
moving = False
deltatime = 86400   # 1 day per frame

def handle_events():
    """Handles user input events."""
    global show_name, moving, deltatime

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        # Exit
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            if event.key == pygame.K_z:
                show_name = not show_name

            if event.key == pygame.K_UP:
                deltatime /= 1.5
            if event.key == pygame.K_DOWN:
                deltatime *= 1.5
            if event.key == pygame.K_t:
                deltatime = 0
            if event.key == pygame.K_y:
                deltatime = 14400  # 4 hours per frame

        if keys[pygame.K_c]:
            info.mouse_motion = np.array([0.0, 0.0])

        if event.type == pygame.MOUSEWHEEL:
            mouse_screen = np.array(pygame.mouse.get_pos(), dtype=float)

            # Convert to world position before zooming
            world_pos = (mouse_screen - info.mouse_motion) / CelestialObject.scale

            zoom_factor = 1.3 ** event.y
            CelestialObject.scale *= zoom_factor

            # Keep world point under cursor
            info.mouse_motion = mouse_screen - world_pos * CelestialObject.scale

        if event.type == pygame.MOUSEBUTTONDOWN:
            moving = True
        if event.type == pygame.MOUSEBUTTONUP:
            moving = False
        if event.type == pygame.MOUSEMOTION and moving:
            info.mouse_motion += np.array(event.rel)

    return True

def display_controls():
    if pygame.key.get_pressed()[pygame.K_x]:
        for i, text in enumerate(info.controls):
            surf = FONT.render(text, True, info.COLOR_WHITE)
            WIN.blit(surf, (10, 630 + i * 20))

def main():
    global deltatime

    clock = pygame.time.Clock()
    running = True
    CelestialObject.sun = planets[0]
    sun = planets[0]
    info.mouse_motion[:] = RESOLUTION / 2 - sun.position * CelestialObject.scale

    while running:
        WIN.fill(info.COLOR_BLACK)
        pygame.display.set_caption(f"Solar System Simulation - FPS: {clock.get_fps():.2f}")

        running = handle_events()
        if not running:
            break

        sub_dt = deltatime / SUBSTEPS
        # Find acceleration before leapfrog integration to avoid drift
        for body in bodies:
            body.compute_acceleration(bodies)
        for _ in range(SUBSTEPS):
            for body in bodies:
                body.update_position(sub_dt, bodies)

        for body in bodies:
            body.draw()

        for planet in planets:
            if show_name:
                planet.draw_name()
            else:
                planet.show_distances()

        for moon in moons:
            if show_name:
                moon.draw_name()

        display_controls()
        draw.display_information(deltatime)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
