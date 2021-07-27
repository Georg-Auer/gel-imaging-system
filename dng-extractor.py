# pip3 install PiDNG
# https://imagej.net/imaging/principles#why-lossy-jpegs-should-not-be-used-in-imaging
# https://github.com/schoolpost/PiDNG
# https://noise.getoto.net/tag/image-processing/

# examples
from pidng.core import RPICAM2DNG
import cv2
imagename = 'gel_exposure1000000_2021_07_27_12_40_+raw.png'
# use file string input to the jpeg+raw file. 
d = RPICAM2DNG()
# saves the file with the same name(!) as .dng
d.convert(imagename)

image = cv2.imread(imagename)

# saves the file with the same name as .png, minus the _+raw.png
# works in >=python3.9
imagename = imagename.removesuffix('_+raw.png') + '.png'
# imagename = imagename.removesuffix('_+raw.png') + '.jp2'
# imagename = imagename.removesuffix('_+raw.png') + '.jpg'

cv2.imwrite(imagename, image)