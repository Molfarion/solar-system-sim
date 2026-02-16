import numpy as np

class Camera:
    """
    Manages the viewport transformation (zoom and pan) and tracking of celestial bodies.
    """
    def __init__(self, width, height, initial_scale):
        self.width = width
        self.height = height
        self.offset = np.array([width / 2, height / 2], dtype=float)
        self.scale = initial_scale
        self.target = None

    def world_to_screen(self, world_pos: np.ndarray) -> np.ndarray:
        """Converts world coordinates to screen coordinates."""
        return world_pos * self.scale + self.offset

    def screen_to_world(self, screen_pos: np.ndarray) -> np.ndarray:
        """Converts screen coordinates to world coordinates."""
        return (screen_pos - self.offset) / self.scale

    def handle_zoom(self, zoom_factor: float, mouse_pos: np.ndarray):
        """
        Adjusts the scale and offset so that the world position under the mouse remains constant.
        """
        mouse_world_before = self.screen_to_world(mouse_pos)
        self.scale *= zoom_factor
        mouse_world_after = self.screen_to_world(mouse_pos)
        
        # Adjust offset: screen_pos = world_pos * new_scale + new_offset
        # We want screen_pos to remain the same for the world point that was under the mouse.
        # offset_diff = mouse_world_after - mouse_world_before in world units
        # In screen units, this shift is offset_diff * self.scale
        self.offset += (mouse_world_after - mouse_world_before) * self.scale

    def handle_pan(self, rel: tuple):
        """Pans the camera by a relative screen-space amount."""
        self.offset += np.array(rel, dtype=float)

    def center_on_origin(self):
        """Resets offset to center the origin."""
        self.offset[:] = [self.width / 2, self.height / 2]
        self.target = None

    def set_target(self, body):
        """Sets a celestial body to track."""
        self.target = body

    def update(self):
        """Updates the offset if a target is being tracked."""
        if self.target:
            # We want: target.position * scale + offset = center
            # So: offset = center - target.position * scale
            center = np.array([self.width / 2, self.height / 2])
            self.offset = center - self.target.position * self.scale
