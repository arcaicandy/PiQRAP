# USBMount - Automatic USB Device Detection

PiQRAP depends on the Raspberry Pi automatically detecting USB memory Drives/Sticks and mounting them under /media/pi.
When using the Desktop versions of Raspberry Pi OS software that performs this is already installed but when using the Lite versions of Raspberry Pi OS it is not.
This document describes how to install alternative software and configure it so it mimics the behavious of the desktop versions.
You DO NOT need this if you are using PiQRAP with the Desktop running.
These instructions have only been tested on the Lite versions of Raspberry Pi OS.

## Installing USBMount

### 1\. Install the USBmount package
<br>
$ sudo apt get install usbmount -y

## Configure USBMount

### 1\. Update USBMount Systemd Options
<br>
$ sudo nano /lib/systemd/system/systemd-udevd.service
PrivateMounts=no
MountFlags=shared

### 2\. Update USBMount Configuration Options
<br>
$ sudo nano /etc/usbmount/usbmount.conf
FS\_MOUNTOPTIONS="-fstype=vfat,umask=0000"

### 3\. Create Symbolic Link

We need to make sure PiQRAP can see any mounted USB drive under /media/pi so we create a symbolic link that allows this...

$ sudo mkdir /media/pi
$ sudo ln -s /media/usb /media/pi/usb