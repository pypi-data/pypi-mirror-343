import numpy as np
from typing import List, Tuple

def create_gradient(color1: Tuple[int, int, int], 
                   color2: Tuple[int, int, int], 
                   steps: int) -> List[Tuple[int, int, int]]:
    """Create a gradient between two colors"""
    gradient = []
    for i in range(steps):
        r = int(color1[0] + (color2[0] - color1[0]) * i / steps)
        g = int(color1[1] + (color2[1] - color1[1]) * i / steps)
        b = int(color1[2] + (color2[2] - color1[2]) * i / steps)
        gradient.append((r, g, b))
    return gradient

def create_pattern(pattern_size: int, color1: Tuple[int, int, int], 
                  color2: Tuple[int, int, int]) -> np.ndarray:
    """Create a checkered pattern"""
    pattern = np.zeros((pattern_size, pattern_size, 3), dtype=np.uint8)
    for i in range(pattern_size):
        for j in range(pattern_size):
            if (i + j) % 2 == 0:
                pattern[i, j] = color1
            else:
                pattern[i, j] = color2
    return pattern

def create_circle(radius : int, color : Tuple[int, int, int]) -> np.ndarray:
    """Create a circular pattern"""
    size = radius * 2 + 1
    pattern = np.zeros((size, size, 3), dtype=np.uint8)
    center = radius

    for y in range(size):
        for x in range(size):
            if (x - center) ** 2 + (y - center) ** 2 <= radius ** 2:
                pattern[y, x] = color
    return pattern

def create_dithering(width : int, height : int, color1 : Tuple[int, int, int], color2 : Tuple[int, int, int], pattern_type : str = "bayer") -> np.ndarray:
    """Create a dithering pattern"""
    if pattern_type == "bayer":
        bayer_matrix = np.array([[0, 2], [3, 1]])
        dithered_image = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                if bayer_matrix[y % 2, x % 2] == 0:
                    dithered_image[y, x] = color1
                else:
                    dithered_image[y, x] = color2
    else:
        raise ValueError("Unsupported dithering pattern type")
    return dithered_image

def create_noise(width : int, height : int, density : float) -> np.ndarray:
    """Create noise pattern"""
    pattern = np.zeros((height, width, 3), dtype=np.uint8)
    mask = np.random.random((height, width)) < density
    patter[mask] = 255
    return pattern