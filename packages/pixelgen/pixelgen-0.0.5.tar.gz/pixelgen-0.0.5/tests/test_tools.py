import unittest
import numpy as np
from pixelgen.tools import create_circle, create_pattern, create_dithering, create_noise

class TestTools(unittest.TestCase):
    def test_create_circle(self):
        circle = create_circle(5, (255, 0, 0))
        self.assertEqual(circle.shape, (11, 11, 3))
        # Test center pixel is colored
        self.assertTrue(np.array_equal(circle[5, 5], [255, 0, 0]))

    def test_create_pattern(self):
        pattern = create_pattern(4, (255, 0, 0), (0, 255, 0))
        self.assertEqual(pattern.shape, (4, 4, 3))
        # Test alternating pattern
        self.assertTrue(np.array_equal(pattern[0, 0], [255, 0, 0]))
        self.assertTrue(np.array_equal(pattern[0, 1], [0, 255, 0]))

    def test_create_dithering(self):
        dither = create_dithering(8, 8, (255, 0, 0), (0, 255, 0), "bayer")
        self.assertEqual(dither.shape, (8, 8, 3))

    def test_create_noise(self):
        noise = create_noise(16, 16, 0.5)
        self.assertEqual(noise.shape, (16, 16, 3))