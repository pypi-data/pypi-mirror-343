import numpy as np
from PIL import Image

class Layer:
    def __init__(self, width: int, height: int, name: str):
        self.width = width
        self.height = height
        self.name = name
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.visible = True
        self.opacity = 1.0

    def fill_area(self, x1: int, y1: int, x2: int, y2: int, color: tuple):
        """Fill rectangular area with color"""
        self.canvas[y1:y2, x1:x2] = color

    def clear(self):
        """Clear the layer"""
        self.canvas.fill(0)

    def paste(self, image: np.ndarray, position: tuple):
        """Paste an image onto the layer at specified position"""
        x, y = position
        h, w = image.shape[:2]
        self.canvas[y:y+h, x:x+w] = image

class PixelGenerator:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.layers = []
        self.history = []
        self.redo_stack = []
        self.active_layer = None

    def add_layer(self, name: str):
        layer = Layer(self.width, self.height, name)
        self.layers.append(layer)
        self.active_layer = layer
        return layer

    def merge_layers(self, layer_names=None):
        """Merge specified layers or all layers if none specified"""
        result = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        layers_to_merge = self.layers
        if layer_names:
            layers_to_merge = [layer for layer in self.layers if layer.name in layer_names]

        for layer in layers_to_merge:
            if layer.visible:
                alpha = layer.opacity
                result = result * (1 - alpha) + layer.canvas * alpha

        return result

    def get_merged_frame(self):
        """Get current frame with all visible layers merged"""
        return self.merge_layers()

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
    
    def save_image(self, filename: str, format: str = "PNG", frames=None):
        """Save the pixel art as image"""
        if frames:
            # Save animated GIF
            frames_pil = [Image.fromarray(frame) for frame in frames]
            frames_pil[0].save(
                filename,
                format="GIF",
                save_all=True,
                append_images=frames_pil[1:],
                duration=200,
                loop=0
            )
        else:
            # Save static image
            merged = self.get_merged_frame()
            img = Image.fromarray(merged)
            img.save(filename, format=format.upper())