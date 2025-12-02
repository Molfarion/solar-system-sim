import numpy as np

WIDTH = 1200
HEIGHT = 800
MINIMUM_RADIUS = 10 

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100) 
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (183, 184, 185)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (201, 144, 57)
COLOR_SATURN = (234, 214, 184)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
COLOR_PLUTO = (126, 129, 115)
COLOR_BUTTON = (255, 255, 255)

AU = 149.6e9          
G = 6.67428e-11       

TOTAL_TIME_ELAPSED = 0.0  
DEFAULT_DELTATIME = 86400.0 
last_deltatime = DEFAULT_DELTATIME 
mouse_motion = np.array([0.0, 0.0]) # Camera offset vector

controls = [
    "Mousewheel Up/Down to zoom in/out",
    "'+' / '-' to speed up / slow down",
    "Space to Pause/Resume",
    "'C' to center view on origin (0,0)",
    "'Z' to toggle Names / Distances",
    "Hold 'X' to see this control list",
]