import pygame
import numpy as np
import info
import draw
import config
from simulation import Simulation

pygame.init()

WIN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
FONT = pygame.font.SysFont(["ubuntumono", "arial", "sans-serif"], 16)

def main():
    sim = Simulation() 
    clock = pygame.time.Clock()
    stars = draw.generate_stars(config.STAR_COUNT)
    
    running = True
    while running:
        WIN.fill(info.COLOR_BLACK)
        draw.draw_stars(stars, WIN)

        pygame.display.set_caption(f"Solar System Simulation - FPS: {clock.get_fps():.2f}")
        # 1. INPUT
        running = sim.handle_events() 
        
        # 2. UPDATE 
        sim.update_physics() 
        
        # 3. RENDER
        sim.render(WIN, FONT, clock)
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()