from pidng.core import RAW2DNG, DNGTags, Tag
import numpy as np
import struct

# image specs
# width = 4096
# height = 3072
width = 2592
height = 1944
bpp= 12

# load raw data into 16-bit numpy array.
numPixels = width*height
rawFile = 'gel_exposure1000000_2021_07_27_12_40_+raw.png'
rf = open(rawFile, mode='rb')
rawData = struct.unpack("H"*numPixels,rf.read(2*numPixels))
rawFlatImage = np.zeros(numPixels, dtype=np.uint16)
rawFlatImage[:] = rawData[:] 
rawImage = np.reshape(rawFlatImage,(height,width))
rawImage = rawImage >> (16 - bpp)

print(rawImage)
