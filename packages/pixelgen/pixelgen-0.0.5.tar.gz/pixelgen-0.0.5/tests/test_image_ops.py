import unittest
import os
from pixelgen.core import PixelGenerator

class TestImageOperations(unittest.TestCase):
    def setUp(self):
        self.pixel_gen = PixelGenerator(32, 32)
        self.test_file = "test_output.png"

    def tearDown(self):
        # Clean up any test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_image(self):
        self.pixel_gen.fill_area(0, 0, 32, 32, (255, 0, 0))
        self.pixel_gen.save_image(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

    def test_save_animated_gif(self):
        frames = []
        for i in range(5):
            self.pixel_gen.fill_area(0, 0, 32, 32, (i*50, 0, 0))
            frames.append(self.pixel_gen.canvas.copy())
        
        gif_file = "test_animation.gif"
        self.pixel_gen.save_image(gif_file, format="GIF", frames=frames)
        self.assertTrue(os.path.exists(gif_file))
        os.remove(gif_file)