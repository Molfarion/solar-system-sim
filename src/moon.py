import numpy as np
from celestial_object import CelestialObject

class Moon(CelestialObject):
    def __init__(self, name, parent, distance, mass, radius, color, relative_velocity):
        # Position relative to parent planet
        initial_pos = parent.position + np.array([distance, 0.0])

        # Velocity = parent velocity + moon orbital velocity around parent
        initial_vel = parent.velocity + relative_velocity

        super().__init__(name, initial_pos, initial_vel, mass, color, radius)
        self.parent = parent

    def draw(self, win, font):
        """Draw the moon and its orbit trail."""
        super().draw(win, font)