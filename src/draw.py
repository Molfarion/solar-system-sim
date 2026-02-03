from datetime import datetime, timedelta
import numpy as np
import pygame
import info
import config
from celestial_object import CelestialObject

SEC_IN_HOUR = 3600
SEC_IN_DAY = 86400
SEC_IN_YEAR = 31557600

def sim_seconds_to_date(total_seconds):
    """Convert simulation seconds since epoch to a calendar date."""
    return config.SIM_EPOCH + timedelta(seconds=total_seconds)

def generate_stars(num_stars=400):
    """Generates a list of random star coordinates and sizes."""
    stars = []
    for _ in range(num_stars):
        x = np.random.randint(config.WIDTH)
        y = np.random.randint(config.HEIGHT)
        radius = 1
        stars.append((x, y, radius))
    return stars

def indicator_for_planet(win, selected_body):
    pygame.draw.circle(win, (255, 255, 255), 
                             selected_body.get_screen_position().astype(int), 
                             int(selected_body.radius + 5), 1)
def draw_stars(stars, win):
    for x, y, radius in stars:
        pygame.draw.circle(win, info.COLOR_WHITE, (int(x), int(y)), int(radius))

def draw_scale_indicator(win, font):
    """Calculates and draws a dynamic scale bar with 'nice' intervals (1, 2, 5)."""
    MAX_BAR_LENGTH_PX = 150  
    MARGIN = 20
    
    current_scale = CelestialObject.scale  # px/meter
    max_distance_m = MAX_BAR_LENGTH_PX / current_scale
    
    if max_distance_m < info.AU * 0.1:
        unit = "km"
        val = max_distance_m / 1000
    else:
        unit = "AU"
        val = max_distance_m / info.AU

    exponent = np.floor(np.log10(val))
    fraction = val / (10**exponent)
    
    if fraction >= 5:
        nice_val = 5
    elif fraction >= 2:
        nice_val = 2
    else:
        nice_val = 1
    
    final_value = nice_val * (10**exponent)
    
    actual_dist_m = final_value * (1000 if unit == "km" else info.AU)
    bar_length_px = int(actual_dist_m * current_scale)
    
    label = f"{final_value:g} {unit}"

    start_x = config.WIDTH - MARGIN - bar_length_px
    end_x = config.WIDTH - MARGIN
    y_pos = config.HEIGHT - MARGIN
    
    pygame.draw.line(win, info.COLOR_WHITE, (start_x, y_pos), (end_x, y_pos), 2)
    pygame.draw.line(win, info.COLOR_WHITE, (start_x, y_pos - 5), (start_x, y_pos + 5), 2)
    pygame.draw.line(win, info.COLOR_WHITE, (end_x, y_pos - 5), (end_x, y_pos + 5), 2)
    
    text_surf = font.render(label, True, info.COLOR_WHITE)
    text_x = start_x + (bar_length_px // 2) - (text_surf.get_width() // 2)
    win.blit(text_surf, (text_x, y_pos - 25))

def display_controls(win, font):
    """Displays controls if 'X' is pressed."""
    if pygame.key.get_pressed()[pygame.K_x]:
        for i, text in enumerate(info.controls):
            surf = font.render(text, True, info.COLOR_WHITE)
            win.blit(surf, (10, config.HEIGHT - 170 + i * 20))

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

    sim_date = sim_seconds_to_date(total_time_elapsed)
    date_text = font.render(
        f"Date: {sim_date.strftime('%Y-%m-%d')}",
        True,
        info.COLOR_WHITE
    )
    win.blit(date_text, (x_start, y_start + 2 * line_spacing))

    controls_text = "Hold X to see the controls"
    controls_surface = font.render(controls_text, True, info.COLOR_WHITE)
    
    controls_x = config.WIDTH - 10 - controls_surface.get_width()
    
    win.blit(controls_surface, (controls_x, y_start))