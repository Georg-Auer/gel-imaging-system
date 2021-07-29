# https://picamera.readthedocs.io/en/release-1.13/recipes2.html#raw-bayer-data-captures

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )


import io
import time
import picamera
import numpy as np
from numpy.lib.stride_tricks import as_strided

stream = io.BytesIO()
with picamera.PiCamera() as camera:

    # optional: set camera parameters
    # camera.resolution = (2592,1944)
    # camera.iso = 100
    # time.sleep(2)
    # # camera.framerate = 5
    # # camera.start_preview()
    # print(camera.exposure_speed)
    # print(camera.shutter_speed)

    # # camera.shutter_speed = camera.exposure_speed
    # camera.shutter_speed = 100000

    # print(camera.shutter_speed)
    # camera.exposure_mode = 'off'
    # g = camera.awb_gains
    # camera.awb_mode = 'off'
    # camera.awb_gains = g

    # Let the camera warm up for a couple of seconds
    time.sleep(2)
    # Capture the image, including the Bayer data
    camera.capture(stream, format='jpeg', bayer=True)
    ver = {
        'RP_ov5647': 1,
        'RP_imx219': 2,
        'RP_testc': 3,
        'RP_imx477': 3,
        "imx477": 3,
        }[camera.exif_tags['IFD0.Model']]

# Extract the raw Bayer data from the end of the stream, check the
# header and strip if off before converting the data into a numpy array

offset = {
    1: 6404096,
    2: 10270208,
    3: 18711040,
    4: 4751360, #not sure for which camera this is
    }[ver]
# data = stream.getvalue()[-offset:]
# print(data)


data = stream.getvalue()[-offset:]
assert data[:4] == 'BRCM'.encode("ascii")

import ctypes
class BroadcomRawHeader(ctypes.Structure):
    _fields_ = [
        ('name',          ctypes.c_char * 32),
        ('width',         ctypes.c_uint16),
        ('height',        ctypes.c_uint16),
        ('padding_right', ctypes.c_uint16),
        ('padding_down',  ctypes.c_uint16),
        ('dummy',         ctypes.c_uint32 * 6),
        ('transform',     ctypes.c_uint16),
        ('format',        ctypes.c_uint16),
        ('bayer_order',   ctypes.c_uint8),
        ('bayer_format',  ctypes.c_uint8),
    ]

header = BroadcomRawHeader.from_buffer_copy(
    data[176:176 + ctypes.sizeof(BroadcomRawHeader)])


# assert data[:4] == 'BRCM' # not sure what BRCM is?
# maybe this has to do something with it:
# https://github.com/waveform80/picamera/issues/133
data = data[32768:]
# data = np.fromstring(data, dtype=np.uint8) # deprecated
data = np.frombuffer(data, dtype=np.uint8)

# For the V1 module, the data consists of 1952 rows of 3264 bytes of data.
# The last 8 rows of data are unused (they only exist because the maximum
# resolution of 1944 rows is rounded up to the nearest 16).
#
# For the V2 module, the data consists of 2480 rows of 4128 bytes of data.
# There's actually 2464 rows of data, but the sensor's raw size is 2466
# rows, rounded up to the nearest multiple of 16: 2480.
#
# Likewise, the last few bytes of each row are unused (why?). Here we
# reshape the data and strip off the unused bytes.

reshape, crop = {
    1: ((1952, 3264), (1944, 3240)),
    2: ((2480, 4128), (2464, 4100)),
    3: ((3056, 6112), (3040, 6084)),
    4: ((1536, 3072), (1520, 3042)),
    }[ver]
data = data.reshape(reshape)[:crop[0], :crop[1]]

# Horizontally, each row consists of 10-bit values. Every four bytes are
# the high 8-bits of four values, and the 5th byte contains the packed low
# 2-bits of the preceding four values. In other words, the bits of the
# values A, B, C, D and arranged like so:
#
#  byte 1   byte 2   byte 3   byte 4   byte 5
# AAAAAAAA BBBBBBBB CCCCCCCC DDDDDDDD AABBCCDD
#
# Here, we convert our data into a 16-bit array, shift all values left by
# 2-bits and unpack the low-order bits from every 5th byte in each row,
# then remove the columns containing the packed bits

# modified with https://github.com/schoolpost/PiDNG/blob/master/pidng/core.py
# for imx477 compatibility
if ver < 3:
    data = data.astype(np.uint16) << 2
    for byte in range(4):
        data[:, byte::5] |= (
            (data[:, 4::5] >> ((4 - byte) * 2)) & 0b11)
    data = np.delete(data, np.s_[4::5], 1)
else:
    data = data.astype(np.uint16)
    shape = data.shape
    unpacked_data = np.zeros(
        (shape[0], int(shape[1] / 3 * 2)), dtype=np.uint16)
    unpacked_data[:, ::2] = (data[:, ::3] << 4) + \
        (data[:, 2::3] & 0x0F)
    unpacked_data[:, 1::2] = (
        data[:, 1::3] << 4) + ((data[:, 2::3] >> 4) & 0x0F)
    data = unpacked_data

# Now to split the data up into its red, green, and blue components. The
# Bayer pattern of the OV5647 sensor is BGGR. In other words the first
# row contains alternating green/blue elements, the second row contains
# alternating red/green elements, and so on as illustrated below:
#
# GBGBGBGBGBGBGB
# RGRGRGRGRGRGRG
# GBGBGBGBGBGBGB
# RGRGRGRGRGRGRG
#
# Please note that if you use vflip or hflip to change the orientation
# of the capture, you must flip the Bayer pattern accordingly

rgb = np.zeros(data.shape + (3,), dtype=data.dtype)
rgb[1::2, 0::2, 0] = data[1::2, 0::2] # Red
rgb[0::2, 0::2, 1] = data[0::2, 0::2] # Green
rgb[1::2, 1::2, 1] = data[1::2, 1::2] # Green
rgb[0::2, 1::2, 2] = data[0::2, 1::2] # Blue

red = rgb[1::2, 0::2, 0]
green1 = rgb[0::2, 0::2, 1]
green2 = rgb[1::2, 1::2, 1]
blue = rgb[0::2, 1::2, 2]

# print(f"red: {rgb[1::2, 0::2, 0]}")
# print(f"green1: {rgb[0::2, 0::2, 1]}")
# print(f"green1: {rgb[1::2, 1::2, 1]}")
# print(f"blue: {rgb[0::2, 1::2, 2]}")
print(f"red: {red}")
print(f"green1: {green1}")
print(f"green2: {green2}")
print(f"blue: {blue}")
print(header._fields_)
print(header.width)
print(header.height)
print(f"bayer order: {header.bayer_order}")

import matplotlib

# At this point we now have the raw Bayer data with the correct values
# and colors but the data still requires de-mosaicing and
# post-processing. If you wish to do this yourself, end the script here!
#
# Below we present a fairly naive de-mosaic method that simply
# calculates the weighted average of a pixel based on the pixels
# surrounding it. The weighting is provided by a byte representation of
# the Bayer filter which we construct first:

# bayer = np.zeros(rgb.shape, dtype=np.uint8)
# bayer[1::2, 0::2, 0] = 1 # Red
# bayer[0::2, 0::2, 1] = 1 # Green
# bayer[1::2, 1::2, 1] = 1 # Green
# bayer[0::2, 1::2, 2] = 1 # Blue

# print(bayer)


# output = (output >> 2).astype(np.uint8)
# with open('image.data', 'wb') as f:
#     output.tofile(f)


# import picamera
# from io import BytesIO
# from pydng.core import RPICAM2DNG



# with picamera.PiCamera() as camera:

#     stream = BytesIO()
#     camera.capture(stream, 'jpeg', bayer=True)

#     d = RPICAM2DNG()
#     output = d.convert(stream)

#     with open('image.dng', 'wb') as f:
#             f.write(output)

# from picamraw import PiRawBayer, PiCameraVersion

# raw_bayer = PiRawBayer(
#     filepath='testraw.jpg',  # A JPEG+RAW file, e.g. an image captured using raspistill with the "--raw" flag
#     camera_version=PiCameraVersion.V2,
#     sensor_mode=0
# )
# raw_bayer.bayer_array   # A 16-bit 2D numpy array of the bayer data
# raw_bayer.bayer_order   # A `BayerOrder` enum that describes the arrangement of the R,G,G,B pixels in the bayer_array
# raw_bayer.to_rgb()      # A 16-bit 3D numpy array of bayer data collapsed into RGB channels (see docstring for details).
# raw_bayer.to_3d()       # A 16-bit 3D numpy array of bayer data split into RGB channels (see docstring for details).

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