from pixelgen.core import PixelGenerator

# Initialize a 32x32 canvas
pixel_art = PixelGenerator(32, 32)

# Define colors
yellow = (255, 255, 0)
black = (0, 0, 0)

# Fill the background with yellow
pixel_art.fill_area(0, 0, 32, 32, yellow)

# Create eyes
pixel_art.set_pixel(10, 10, black)
pixel_art.set_pixel(10, 11, black)
pixel_art.set_pixel(11, 10, black)
pixel_art.set_pixel(11, 11, black)

pixel_art.set_pixel(20, 10, black)
pixel_art.set_pixel(20, 11, black)
pixel_art.set_pixel(21, 10, black)
pixel_art.set_pixel(21, 11, black)

# Create a smile
for x in range(12, 20):
    pixel_art.set_pixel(x, 22, black)
pixel_art.set_pixel(11, 21, black)
pixel_art.set_pixel(20, 21, black)

# Save the result
pixel_art.save_image('smiley_character.png')