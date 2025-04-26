import unittest
import numpy as np
from pixelgen.core import PixelGenerator, Layer

class TestLayerSystem(unittest.TestCase):
    def setUp(self):
        self.pixel_gen = PixelGenerator(32, 32)

    def test_add_layer(self):
        layer = self.pixel_gen.add_layer("test_layer")
        self.assertIsInstance(layer, Layer)
        self.assertEqual(layer.name, "test_layer")
        self.assertEqual(len(self.pixel_gen.layers), 1)

    def test_layer_visibility(self):
        layer = self.pixel_gen.add_layer("test_layer")
        layer.visible = False
        self.assertFalse(layer.visible)

    def test_layer_opacity(self):
        layer = self.pixel_gen.add_layer("test_layer")
        layer.opacity = 0.5
        self.assertEqual(layer.opacity, 0.5)

    def test_layer_fill_area(self):
        layer = self.pixel_gen.add_layer("test_layer")
        layer.fill_area(0, 0, 10, 10, (255, 0, 0))
        area = layer.canvas[0:10, 0:10]
        self.assertTrue(np.all(area == [255, 0, 0]))