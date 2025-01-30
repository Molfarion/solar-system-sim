import numpy as np
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 800
DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)
DEFAULT_IMAGE_POSITION = (500, 400)
MINIMUM_RADIUS = 10
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255, 255, 255)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (183, 184, 185)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (201,144,57)
COLOR_SATURN = (234,214,184)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
COLOR_PLUTO = (126,129,115)
COLOR_BUTTON = (255,255,255)
AU = 149.6e9
G = 6.67428e-11
ORBIT_UPDATE_INTERVAL = 0.1
show_name = True
deltatime = 86400
controls = ["Mousewheel Up/Down to zoom in/out",
            "Up arrow to speed up",
            "Down arrow to slow down",
            "'T' to pause",
            "'Y' to unpause",
            "C to center",
            "Z to change names/distances"]

mouse_motion = np.array([0, 0])