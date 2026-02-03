import numpy as np
import config

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

RESOLUTION = np.array((config.WIDTH, config.HEIGHT))
AU = 149.6e9
G = 6.67428e-11

DEFAULT_DELTATIME = config.DEFAULT_DELTATIME
last_deltatime = DEFAULT_DELTATIME
mouse_motion = np.array([0.0, 0.0])  # Camera offset vector

controls = [
    "Mousewheel Up/Down to zoom in/out",
    "'+' / '-' to speed up / slow down",
    "Space to Pause/Resume",
    "'C' to center view on origin (0,0)",
    "'Q' to clear orbit trails",
    "'Z' to toggle Names / Distances",
    "'R' to restart simulation",
    "Hold 'X' to see this control list",
]