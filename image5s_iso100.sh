#!/bin/bash
# https://raspberrypi.stackexchange.com/questions/32397/how-to-increase-the-camera-exposure-time

# define picture folder:
IMGDIR='/home/pi/images'

# move previously taken pics into -previous- folder
#mkdir /var/www/html/media/previous
mv /home/pi/images/*.jpg /home/pi/images/previous

# create timestamp
TIME=$(date +%Y_%m_%d_%H_%M)
# set exposure time
SETTING='4000000'
# create filename
FILENAME=$IMGDIR/imager_exposure${SETTING}_${TIME}.jpg
# write out exposure time
echo "SETTING is: $SETTING"
echo "starting to take picture"

raspistill -w 2592 -h 1944 -ISO 100 -ss $SETTING -br 80 -co 100 -o $FILENAME -set

# create timestamp
TIME=$(date +%Y_%m_%d_%H_%M)
# set exposure time
SETTING='5000000'
# create filename
FILENAME=$IMGDIR/imager_exposure${SETTING}_${TIME}.jpg
# write out exposure time
echo "SETTING is: $SETTING"
echo "starting to take picture"

raspistill -w 2592 -h 1944 -ISO 100 -ss $SETTING -br 80 -co 100 -o $FILENAME -set


# raspistill -w 2592 -h 1944 -ISO 800 -ss $SETTING -br 80 -co 100 -o $FILENAME -set