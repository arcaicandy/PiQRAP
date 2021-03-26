#!/bin/bash
# Install commands

# Install Open CV
sudo apt-get install python3-opencv -y
sudo apt-get install libqt4-test python3-sip python3-pyqt5 libqtgui4 libjasper-dev libatlas-base-dev -y
pip3 install opencv-contrib-python==4.1.0.25
sudo modprobe bcm2835-v4l2

# Install QRcode python library (allows creation of QR Codes)
pip3 install qrcode[pil] --no-warn-script-location

# Install required python modules
pip3 install PyYAML
pip3 install omxplayer-wrapper
pip3 install pyzbar --no-warn-script-location

# Copy default PiQRAP.yml file to /boot
echo "Copying PiQRAP config file to /boot"

FILE=/boot/piqrap.yml
if [ -f "$FILE" ]; then
    echo "$FILE exists so was not overwritten."
else 
    sudo cp PiQRAP/piqrap.yml "$FILE"
    echo "$FILE was created."
fi

# Copy dmixer.txt to /etc/asound.conf
echo "Copying PiQRAP asound configuraton to /etc"

FILE=/etc/asound.conf
if [ -f "$FILE" ]; then
    echo "$FILE exists so was not overwritten."
else 
    sudo cp PiQRAP/documentation/dmixer.txt "$FILE"
    echo "$FILE was created."
fi