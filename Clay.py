import kodo
import kodo_helpers
from PIL import Image
import math
import os
import random
import time
import sys

# Get directory of this file
directory = os.path.dirname(os.path.realpath(__file__))

# The name of the file to use for the test
filename = 'lena.jpg'

# Open the image convert it to RGB and get the height and width
image = Image.open(os.path.join(directory, filename)).convert("RGB")
image_width = image.size[0]
image_height = image.size[1]


canvas_width = image_width + image_height


canvas = kodo_helpers.CanvasScreenEngine(
    width=canvas_width,
    height=image_height)

# Create the image viewer
image_viewer = kodo_helpers.ImageViewer(
    width=image_width,
    height=image_height,
    canvas=canvas)

# Create the decoding coefficient viewer
state_viewer = kodo_helpers.DecodeStateViewer(
    size=image_height,
    canvas=canvas,
    canvas_position=(image_width, 0))


canvas.start()
time.sleep(1)
image_viewer.set_image(image.tobytes())
time.sleep(5)
canvas.stop()

