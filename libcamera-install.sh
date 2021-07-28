# sudo apt update
# sudo apt upgrade
# sudo rpi-update
# sudo nano  /boot/config.txt
# Also make sure you have the correct dtoverlay 
# for your sensor in the /boot/config.txt file (for example,
# dtoverlay=imx477
# for the HQ cam) and then reboot your Pi.

sudo apt install libboost-dev -y
sudo apt install libgnutls28-dev openssl libtiff5-dev -y
sudo apt install qtbase5-dev libqt5core5a libqt5gui5 libqt5widgets5 -y
sudo apt install meson -y
sudo apt install cmake -y
sudo pip3 install --upgrade pyyaml ply
sudo pip3 install --upgrade meson
sudo pip3 install --upgrade ninja

# sudo apt install cmake-doc ninja-build #maybe??

sudo pip3 install 
cd ~
cd Downloads
git clone git://linuxtv.org/libcamera.git
cd libcamera
meson build
cd build
meson configure -Dpipelines=raspberrypi -Dtest=false
cd ..
ninja -C build
sudo ninja -C build install

# libepoxy
sudo apt install libegl1-mesa-dev -y
cd ~/Downloads
git clone https://github.com/anholt/libepoxy.git
cd libepoxy
mkdir _build
cd _build
meson
ninja
sudo ninja install

# libcamera-apps
sudo apt install cmake libboost-program-options-dev libdrm-dev libexif-dev -y
cd ~/Downloads
git clone https://github.com/raspberrypi/libcamera-apps.git
cd libcamera-apps
mkdir build
cd build
cmake ..
make -j4

# To check everything is working correctly, type ./libcamera-hello - you should see a preview window displayed for about 5 seconds.
# Note for Pi 3 devices

# As we saw previously, 1GB devices may need make -j2 instead of make -j4.

# Also, Pi 3s do not by default use the correct GL driver,
# so please ensure you have dtoverlay=vc4-fkms-v3d in the [all] (not in the [pi4]) section of your /boot/config.txt file.
# If errors are enountered, try running with -n or and use DISPLAY=:0 when via ssh
./libcamera-raw -o test.raw -n

./libcamera-hello -h
./libcamera-hello
./libcamera-hello --roi 0.25,0.25,0.5,0.5
./libcamera-hello --brightness 0.1 --contrast 1.1 --saturation 0.9 --sharpness 0.9

./libcamera-still -h
./libcamera-still -o test.jpg
./libcamera-still -r -o test.jpg
./libcamera-still -e png -o test.png
./libcamera-still -o test%04d.jpg -t 999999 --timelapse 10000
./libcamera-still --gain 2 -o test-gain2.jpg

./libcamera-vid -h
./libcamera-vid -t 10000 -o test.h264
./libcamera-vid -v -o test.mjpeg --codec mjpeg
./libcamera-vid -o test.h264 --inline --circular -k -t 0
./libcamera-vid -o segment%04d.h264 --inline --segment 5000 -t 100000
./libcamera-vid -o test.h264 --shutter 20000 --gain 1
./libcamera-vid -o test.h264 --framerate 15

./libcamera-raw -h
./libcamera-raw -o test.raw

./libcamera-jpeg -o test.jpg