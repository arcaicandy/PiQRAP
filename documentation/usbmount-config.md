# USBMount - Automatic USB Device Detection

PiQRAP depends on the Raspberry Pi automatically detecting USB memory Drives/Sticks and mounting them under /media/pi.

When using the Desktop versions of Raspberry Pi OS software that performs this is already installed but when using the Lite versions of Raspberry Pi OS it is not.

This document describes how to install alternative software and configure it so it mimics the behavious of the desktop versions.

You DO NOT need this if you are using PiQRAP with the Desktop running.

These instructions have only been tested on the Lite versions of Raspberry Pi OS.

## Installing USBMount

### 1\. Install the USBmount package

$ sudo apt install usbmount -y

## Configure USBMount

### 1\. Update USBMount Systemd Options

We need to change some of the options that the USBMount service is setup with...

pi@PiQRAP:\~/PiQRAP $ sudo nano /lib/systemd/system/systemd-udevd.service

Find the options below, in the [Service] section and change the values or add them if they don't exist...

```
PrivateMounts=no
MountFlags=shared
```

### 2\. Update USBMount Configuration Options

We need to add some options to the USBMount config file...

pi@PiQRAP:\~/PiQRAP $ sudo nano /etc/usbmount/usbmount.conf

Find the following option and change as below...

```
FS_MOUNTOPTIONS="-fstype=vfat,umask=0000"
```

### 3\. Create Symbolic Link

We need to make sure PiQRAP can see any mounted USB drive under /media/pi so we create a symbolic link that allows this...

pi@PiQRAP:\~/PiQRAP $ sudo mkdir /media/pi
pi@PiQRAP:\~/PiQRAP $ sudo ln -s /media/usb /media/pi/usb

Now reboot.

## Test USBMount

Once you have rebooted the Pi you can plug a USB Drive or stick into one of the USB ports of the Pi.

If you then enter the following command you should see the contents of the drive...

pi@PiQRAP:\~/PiQRAP $ ls /media/pi/usb