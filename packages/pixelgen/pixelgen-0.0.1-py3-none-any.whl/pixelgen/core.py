import numpy as np
from PIL import image

class PixelGenerator:
    def __init__(self, width : int, height : int):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

    def set_pixel(self, x : int, y : int, color : tuple):
        """Set color for specific pixel."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas[y, x] = color

    def fill_area(self, x1 : int,  y1: int, x2 : int, y1 : int, color : tuple):
        """Fill a rectangular area with a color."""
        self.canvas[y1:y2, x1:x2] = color

    def save_image(self, filename : str):
        """Save the pixel art as image"""
        img = Image.fromarray(self.canvas)
        img.save(filename)