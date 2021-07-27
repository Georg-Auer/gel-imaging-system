# https://picamera.readthedocs.io/en/release-1.13/recipes1.html

from picamera import PiCamera
from time import sleep
from fractions import Fraction

# Force sensor mode 3 (the long exposure mode), set
# the framerate to 1/6fps, the shutter speed to 6s,
# and ISO to 800 (for maximum gain)
# camera = PiCamera(
#     resolution=(1280, 720),
#     framerate=Fraction(1, 6),
#     sensor_mode=3)
# # 200s should be possible
# camera.shutter_speed = 6000000
# camera.iso = 800
# # Give the camera a good long time to set gains and
# # measure AWB (you may wish to use fixed AWB instead)
# sleep(30)
# camera.exposure_mode = 'off'
# # Finally, capture an image with a 6s exposure. Due
# # to mode switching on the still port, this will take
# # longer than 6 seconds
# camera.capture('dark.jpg')


# capture only luminescence
import time
import picamera
import picamera.array
import numpy as np
import matplotlib.pyplot as plt

with picamera.PiCamera() as camera:
    camera.resolution = (100, 100)

    camera.framerate = Fraction(1, 6)
    camera.shutter_speed = 1000000 # 6000000 = 6s, 200s should be maximum
    camera.sensor_mode = 3
    camera.iso = 1600
    # Give the camera a good long time to set gains and
    # measure AWB (you may wish to use fixed AWB instead)
    sleep(10)
    camera.exposure_mode = 'off'

    y_data = np.empty((112, 128), dtype=np.uint8)
    try:
        camera.capture(y_data, 'yuv')
    except IOError:
        pass
    y_data = y_data[:100, :100]
    # y_data now contains the Y-plane only

    print(f"luminance array{y_data}")
    print(f"luminance array sum {np.sum(y_data)}")
    np.savetxt('y_data-luminance.csv', y_data, delimiter=',')
    imgplot = plt.imshow(y_data)