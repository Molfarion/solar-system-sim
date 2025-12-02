from celestial_object import CelestialObject
import info
import pygame 

pygame.init()
FONT = pygame.font.SysFont("comicsans", 16)
WIN = pygame.display.set_mode((info.WIDTH, info.HEIGHT))
clock = pygame.time.Clock()

time_elapsed = 0 

def calculating_time(deltatime):
    """Calculate total simulation time in years."""
    global time_elapsed
    time_elapsed += deltatime / 31_536_000  # Convert seconds to years
    return time_elapsed

def display_information(deltatime):
    """Display simulation time information on screen."""
    
    # Convert seconds to years
    time_text = FONT.render(
        f"Time from start: {calculating_time(deltatime):.3f} years", 1, info.COLOR_WHITE)
    WIN.blit(time_text, (10, 10))

    deltatime_text = FONT.render(
        f"Time Speed: {round((deltatime / 1440), 3)} days/s", 1, info.COLOR_WHITE)
    WIN.blit(deltatime_text, (10, 30))

    controls = FONT.render("Hold X to see the controls", 1, info.COLOR_WHITE)
    WIN.blit(controls, (1000, 10))

    scale = FONT.render(
        f"Scale: {1 / (1e6 * CelestialObject.scale):.3f} thousand km/px", 1, info.COLOR_WHITE)
    WIN.blit(scale, (10, 50))

