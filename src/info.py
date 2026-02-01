import numpy as np

WIDTH = 1200
HEIGHT = 800

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

AU = 149.6e9          
G = 6.67428e-11       

DEFAULT_DELTATIME = 43200.0 
last_deltatime = DEFAULT_DELTATIME 
mouse_motion = np.array([0.0, 0.0]) # Camera offset vector

controls = [
    "Mousewheel Up/Down to zoom in/out",
    "'+' / '-' to speed up / slow down",
    "Space to Pause/Resume",
    "'C' to center view on origin (0,0)",
    "'Q' to clear orbit trails",
    "'Z' to toggle Names / Distances",
    "Hold 'X' to see this control list",
]