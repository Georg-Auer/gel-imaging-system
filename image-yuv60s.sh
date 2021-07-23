#!/bin/bash
# https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
# https://raspberrypi.stackexchange.com/questions/32397/how-to-increase-the-camera-exposure-time

# raspiyuv -rgb -o foo.rgb

# define picture folder:
IMGDIR='/home/pi/images'

# move previously taken pics into -previous- folder
#mkdir /var/www/html/media/previous
mv /home/pi/images/*.jpg /home/pi/images/previous

# create timestamp
TIME=$(date +%Y_%m_%d_%H_%M)
# set exposure time, 60000000 = 60s
SETTING='60000000'
# shutter time max is 200s = 200000000
# create filename
FILENAME=$IMGDIR/imager_exposure${SETTING}_${TIME}.jpg
# write out exposure time
echo "SETTING is: $SETTING"
echo "starting to take picture"
# raspistill -w 2592 -h 1944 -ISO 800 -ss $SETTING -br 80 -co 100 
#raspistill -w 2592 -h 1944 -ISO 800 -ex off -ss $SETTING -br 80 -co 100 -awb off -awbg 1.5,1.8 -dg 16.0 -ag 12.0 -a 64 -a 32 -a 16 -o $FILENAME
#raspistill -o bild.jpg -n -t 1 -ex off -ss 2000 -awb off -awbg 1.5,1.2 -ag 12.0 -dg 4.0
# this was not really working but last
# raspistill -w 2592 -h 1944 -ex off -ISO 800 -ss $SETTING -br 80 -co 100 -awb off -awbg 1.5,1.5 -dg 64.0 -ag 1.0 -a 64 -a 32 -a 16 -o $FILENAME -set
# -mm average -drc off -ex off -awb off -awbg 1.5,1.5 -ag 12.0 -dg 4.0 -a 64 -a 16
# -mm average -drc off -ex off -awb off -awbg 1.5,1.5 -ag 12.0 -dg 16.0
raspiyuv -w 2592 -h 1944 -o $FILENAME -n -t 1 -ex off -ss $SETTING -awb off -awbg 1.8,3 -ag 12.0 -dg 1.0 -y -set
