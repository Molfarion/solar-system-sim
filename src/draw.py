import numpy as np
import pygame
import info
from celestial_object import CelestialObject

SEC_IN_HOUR = 3600
SEC_IN_DAY = 86400
SEC_IN_YEAR = 31557600

def generate_stars(num_stars=400):
    """Generates a list of random star coordinates and sizes."""
    stars = []
    for _ in range(num_stars):
        x = np.random.randint(info.WIDTH)
        y = np.random.randint(info.HEIGHT)
        radius = 1
        stars.append((x, y, radius))
    return stars

def indicator_for_planet(win, selected_body):
    pygame.draw.circle(win, (255, 255, 255), 
                             selected_body.screen_pos.astype(int), 
                             int(selected_body.radius + 5), 1)
def draw_stars(stars, win):
    for x, y, radius in stars:
        pygame.draw.circle(win, info.COLOR_WHITE, (int(x), int(y)), int(radius))

def draw_scale_indicator(win, font):
    """Calculates and draws a dynamic scale bar."""
    
    MAX_BAR_LENGTH_PX = 150  
    MARGIN = 20
    
    current_scale = CelestialObject.scale
    distance_at_max_px = MAX_BAR_LENGTH_PX / current_scale
    AU_value = distance_at_max_px / info.AU
    
    # Determine the label and distance
    if AU_value >= 1:
        nice_label_AU = 10**np.floor(np.log10(AU_value))
        label = f"{nice_label_AU:.0f} AU"
        nice_distance_m = nice_label_AU * info.AU
    elif AU_value >= 0.001:
        nice_label_AU = 10**np.floor(np.log10(AU_value))
        label = f"{nice_label_AU:.3f} AU"
        nice_distance_m = nice_label_AU * info.AU
    else:
        distance_km = distance_at_max_px / 1000 
        nice_label_km = 10**np.floor(np.log10(distance_km))
        label = f"{nice_label_km:.0f} thousand km" 
        nice_distance_m = nice_label_km * 1000

    bar_length_px = int(nice_distance_m * current_scale)
    
    start_x = info.WIDTH - MARGIN - bar_length_px
    end_x = info.WIDTH - MARGIN
    y_pos = info.HEIGHT - MARGIN
    
    pygame.draw.line(win, info.COLOR_WHITE, (start_x, y_pos), (end_x, y_pos), 2)
    pygame.draw.line(win, info.COLOR_WHITE, (start_x, y_pos - 5), (start_x, y_pos + 5), 2)
    pygame.draw.line(win, info.COLOR_WHITE, (end_x, y_pos - 5), (end_x, y_pos + 5), 2)
    
    text_surface = font.render(label, True, info.COLOR_WHITE)
    text_x = start_x + bar_length_px / 2 - text_surface.get_width() / 2
    text_y = y_pos - 25
    win.blit(text_surface, (text_x, text_y))


def display_simulation_status(win, font, deltatime, total_time_elapsed, current_fps):
    """Draws the current time speed, total elapsed time, and controls prompt.""" 
    x_start = 10
    y_start = 10
    line_spacing = 20
    
    sim_seconds_per_real_second = deltatime * current_fps
    
    # Determine the most readable unit for speed
    if sim_seconds_per_real_second >= SEC_IN_YEAR:
        speed_val = sim_seconds_per_real_second / SEC_IN_YEAR
        unit = "years/s"
    elif sim_seconds_per_real_second >= SEC_IN_DAY:
        speed_val = sim_seconds_per_real_second / SEC_IN_DAY
        unit = "days/s"
    elif sim_seconds_per_real_second >= SEC_IN_HOUR:
        speed_val = sim_seconds_per_real_second / SEC_IN_HOUR
        unit = "hours/s"
    else:
        speed_val = sim_seconds_per_real_second
        unit = "sec/s"

    speed_text = font.render(
        f"Sim Speed: {speed_val:.2f} {unit}",
        True, 
        info.COLOR_WHITE
    )
    win.blit(speed_text, (x_start, y_start))

    time_elapsed_years = total_time_elapsed / SEC_IN_YEAR
    time_elapsed_text = font.render(
        f"Time from start: {time_elapsed_years:.3f} years", 
        True, 
        info.COLOR_WHITE
    )
    win.blit(time_elapsed_text, (x_start, y_start + line_spacing))

    controls_text = "Hold X to see the controls"
    controls_surface = font.render(controls_text, True, info.COLOR_WHITE)
    
    controls_x = info.WIDTH - 10 - controls_surface.get_width()
    
    win.blit(controls_surface, (controls_x, y_start))