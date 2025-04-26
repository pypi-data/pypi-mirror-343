import numpy as np
from typing import List, Tuple

def create_gradient(color1 : Tuple[int, int ,int], color2 : Tuple[int, int, int], steps : int) -> List[Tuple[int, int, int]]:
    """Create a gradient between two colors."""
    gradient = []
    for i in range(steps):
        r = int(color1[0] + (color2[0] - color1[0]) * i / steps)
        g = int(color1[1] + (color2[1] - color1[1]) * i / steps)
        b = int(color1[2] + (color2[2] - color1[2]) * i / steps )
        gradient.append((r, g, b))
    return gradient

def create_patterns(pattern_size : int, color1 : Tuple[int, int, int], color2 : Tuple[int, int, int]) -> np.ndarray:
    """Create a checkered pattern."""
    pattern = np.zeros((pattern_size, pattern_size, 3), dtype=np.uint8)
    for i in range(pattern_size):
        for j in range(pattern_size):
            if (i + j) % 2 == 0:
                pattern[i, j] = color1
            else:
                pattern[i, j] = color2
    return pattern
    