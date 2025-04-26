import numpy as np
from PIL import Image

class PixelGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.layers = []
        self.history =  []
        self.redo_stack = []
        self.active_layer = None

    def add_layer(self, name : str):
        layer = Layer(self.width, self.height, name)
        self.layers.append(layer)
        self.active_layer = layer
        return layer

    def merge_layers(self):
        pass

    def save_state(self):
        self.history.append(self.canvas.copy())
        self.redo_stack.clear()

    def undo(self):
        if self.history:
            self.redo_stack.append(np.copy(self.canvas))
            self.canvas = self.history.pop()

    def redo(self):
        if self.redo_stack:
            self.history.append(np.copy(self.canvas))
            self.canvas = self.redo_stack.pop()
    
    def set_pixel(self, x: int, y: int, color: tuple):
        """Set color for specific pixel"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.canvas[y, x] = color
    
    def fill_area(self, x1: int, y1: int, x2: int, y2: int, color: tuple):
        """Fill rectangular area with color"""
        self.canvas[y1:y2, x1:x2] = color
    
    def save_image(self, filename: str, format : str = "PNG"):
        """Save the pixel art as image"""
        img = Image.fromarray(self.canvas)
        if format.upper() == "GIF":
            frames = []

            img.save(filename, format="GIF", save_all=True, append_images = frames)
        else:
            img.save(filename, format=format.upper())

class Layer:
    def __init__(self, width : int, height : int, name : str):
        self.width = width
        self.height = height
        self.name = name
        self.visible = True
        self.opacity = 1.0
        self.canvas = np.zeros((height, width, 4), dtype=np.uint8)










        