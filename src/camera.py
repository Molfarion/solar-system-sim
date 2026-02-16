import numpy as np

class Camera:
    def __init__(self, width, height, initial_scale):
        self.offset = np.array([width / 2, height / 2], dtype=float)
        self.scale = initial_scale
        self.target_scale = initial_scale
        self.zoom_mouse_pos = self.offset.copy()
        self.target = None
        self.width = width
        self.height = height
        self.tracking_locked = False # New state for zero-lag tracking

    def world_to_screen(self, world_pos):
        return world_pos * self.scale + self.offset
    
    def screen_to_world(self, screen_pos):
        return (screen_pos - self.offset) / self.scale
    
    def handle_zoom(self, zoom_factor, mouse_pos):
        self.target_scale *= zoom_factor
        self.zoom_mouse_pos = np.array(mouse_pos, dtype=float)

    def handle_pan(self, rel: tuple):
        """Pans the camera by a relative screen-space amount."""
        self.offset += np.array(rel, dtype=float)
        self.target = None
        self.tracking_locked = False

    def center_on_origin(self):
        """Resets offset to center the origin."""
        self.offset[:] = [self.width / 2, self.height / 2]
        self.target = None
        self.tracking_locked = False

    def set_target(self, body):
        """Sets a celestial body to track."""
        self.target = body
        self.tracking_locked = False

    def update(self):
        # Update scale smoothly
        scaling_active = abs(self.target_scale - self.scale) > self.scale * 0.0001
        if scaling_active:
            old_scale = self.scale
            self.scale += (self.target_scale - self.scale) * 0.2 # Faster zoom response
            
            if not self.target:
                # Maintain zoom center relative to mouse if NOT tracking
                mouse_world = (self.zoom_mouse_pos - self.offset) / old_scale
                self.offset = self.zoom_mouse_pos - mouse_world * self.scale
            else:
                # Force lock while zooming to prevent "floating" away
                center = np.array([self.width / 2, self.height / 2])
                self.offset = center - self.target.position * self.scale
                self.tracking_locked = True

        # Update offset for target tracking
        if self.target:
            center = np.array([self.width / 2, self.height / 2])
            target_offset = center - self.target.position * self.scale
            
            if self.tracking_locked or scaling_active:
                # Absolute lock to prevent drift
                self.offset = target_offset
            else:
                # Smooth arrival from a distance
                diff = target_offset - self.offset
                dist = np.linalg.norm(diff)
                if dist < 1.0: # Snap to lock if within 1 pixel
                    self.offset = target_offset
                    self.tracking_locked = True
                else:
                    self.offset += diff * 0.15