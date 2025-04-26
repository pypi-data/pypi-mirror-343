import unittest
import numpy as np
from pixelgen.core import PixelGenerator

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.pixel_gen = PixelGenerator(32, 32)

    def test_initialization(self):
        self.assertEqual(self.pixel_gen.width, 32)
        self.assertEqual(self.pixel_gen.height, 32)
        self.assertEqual(self.pixel_gen.canvas.shape, (32, 32, 3))

    def test_set_pixel(self):
        self.pixel_gen.set_pixel(0, 0, (255, 0, 0))
        self.assertTrue(np.array_equal(self.pixel_gen.canvas[0, 0], [255, 0, 0]))

    def test_fill_area(self):
        self.pixel_gen.fill_area(0, 0, 10, 10, (0, 255, 0))
        area = self.pixel_gen.canvas[0:10, 0:10]
        self.assertTrue(np.all(area == [0, 255, 0]))