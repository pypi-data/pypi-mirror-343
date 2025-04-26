from pixelgen.core import PixelGenerator
from pixelgen.tools import create_gradient, create_patterns

pixel_art = PixelGenerator(32, 32)

pixel_art.set_pixel(0, 0, (255, 0, 0))
pixel_art.set_pixel(1, 1, (0, 255, 0))

pixel_art.fill_area(10, 10, 20, 20, (0, 0, 255))

gradient = create_gradient((255, 0, 0), (0, 0, 255), 10)

pixel_art.save_image('my_pixel_art.png')