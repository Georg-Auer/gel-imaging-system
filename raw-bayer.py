from picamraw import PiRawBayer, PiCameraVersion

raw_bayer = PiRawBayer(
    filepath='gel_exposure1000000_2021_07_27_12_40_+raw.png',  # A JPEG+RAW file, e.g. an image captured using raspistill with the "--raw" flag
    camera_version=PiCameraVersion.V2,
    sensor_mode=0
)
raw_bayer.bayer_array   # A 16-bit 2D numpy array of the bayer data
raw_bayer.bayer_order   # A `BayerOrder` enum that describes the arrangement of the R,G,G,B pixels in the bayer_array
raw_bayer.to_rgb()      # A 16-bit 3D numpy array of bayer data collapsed into RGB channels (see docstring for details).
raw_bayer.to_3d()       # A 16-bit 3D numpy array of bayer data split into RGB channels (see docstring for details).

# from pidng.core import RAW2DNG, DNGTags, Tag
# import numpy as np
# import struct

# # image specs
# width = 4096
# height = 3072
# bpp= 12

# # load raw data into 16-bit numpy array.
# numPixels = width*height
# rawFile = 'extras/scene_daylight_211ms_c2.raw16'
# rf = open(rawFile, mode='rb')
# rawData = struct.unpack("H"*numPixels,rf.read(2*numPixels))
# rawFlatImage = np.zeros(numPixels, dtype=np.uint16)
# rawFlatImage[:] = rawData[:] 
# rawImage = np.reshape(rawFlatImage,(height,width))
# rawImage = rawImage >> (16 - bpp)


# does not work for the IMX477 in the hq cam
#  # https://picamera.readthedocs.io/en/release-1.13/recipes2.html#raw-bayer-data-captures
# import time
# import picamera
# import picamera.array
# import numpy as np

# with picamera.PiCamera() as camera:
#     with picamera.array.PiBayerArray(camera) as stream:
#         camera.capture(stream, 'jpeg', bayer=True)
#         # Demosaic data and write to output (just use stream.array if you
#         # want to skip the demosaic step)
#         # output = (stream.demosaic() >> 2).astype(np.uint8)
#         output = (stream.array() >> 2).astype(np.uint8)
#         with open('image.data', 'wb') as f:
#             output.tofile(f)