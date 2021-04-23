# PiQRAP - Headless Build Instructions

## Introduction

This file describes how to build a version of PiQRAP that does not have any monitor/graphical desktop connected while in use.

## Requirements

The requirements remain largly the same as for the standard build that uses the "Raspberry Pi OS with desktop" OS image. Instead it uses the "Raspberry Pi OS Lite" OS image which does not come with the windowing desktop and has a minmal additional software suite included.

For detailed hardware requirements please refer to the 'build-instructions'.

Note: You can set the Raspberry Pi up as a headless PiQRAP without ever connecting any monitor to it at all and using 'SSH' to connect to it instead. Doing this is beyond the scope of this document but there are many guides avaiable on how to do this on the internet.

## Setting up the Raspberry Pi OS

### 1\. Burn the Raspberry Pi OS Lite \(32 bit\) image

This 'headless' guide uses the version of Raspberry Pi OS with no desktop windowing/GUI system installed (Raspberry Pi OS Lite).

It is recommended you use the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) available from the [Raspberry Pi Foundation website](https://www.raspberrypi.org/).
If you use the Raspberry Pi Imager then when you run it click 'Choose OS', select 'Raspberry Pi OS (Other) then choose 'Raspberry Pi OS Lite'.

Note: The latest versions of the imager will let you you setup networking and SSH from the imager itself so no having to connect via a monitor/keyboard initially.

Follow the [Installing Operating System Images Guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) from the Raspberry Pi Foundation.

### 2\. First Boot

Put your newly imaged SD-Card in your Raspberry Pi and power it up. You should eventually get the logon prompt on your monitor if you have one connected.
If you don't have a monitor and keyboard connected then attempt to try to ssh to the Pi (Google for details on how to do this if required).

### 3\. Configuration Options and Enabling Camera Support

Use the raspi-config utility to setup remaining options/configuration choices required for PiQRAP.

From the command line prompt enter the following...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo raspi-config

Now select the options to enable the camera and, while we are here, SSH (this is optional but may be useful in the future so if you know you wont need it feel free to skip SSH).

When asked to reboot/restart say yes.

### 4\. Update the OS \(Raspberry Pi OS Lite\)

We need to make sure that all the packages we have and will install are the latest versions so enter the following commands at the command prompt...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt-get update -y

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt full-upgrade -y

Wait.... wait.... wait... Reboot.

### 5\. Test the Camera

We'll just make sure the camera is working before we go any further...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ raspistill -o image.jpg

If you have a monitor and keyboard attached to your Pi (ie not using SSH) then from the command prompt enter the following commands:

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get -y install fbi -y

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ fbi -a image.jpg

If you don't have a monitor and keyboard attached then then you can still do the 'raspistill' to grab an image but you will need to copy the image.jpg file from the Raspberry Pi to another machine to view it (beyond scope of this document).

### 6\. Install USBMount

Unlike the Raspberry Pi OS Desktop OS version the 'Lite' version of Raspberry Pi OS does not include any software to automatically mount (make available) USB sticks/hard drives. As PiQRAP expects the music it is playing to be on a USB hard drive we need to install software to make this happen.

To do this we use a package called USBMount.

Please refer to the file usbmount-config.md in the documentation directory for instructions on how to do this.

Note: Any USB Pen, Stick or drive must be formated using FAT32 and not NTFS.

## Install and Configure PiQRAP

### 1\. Download the Latest PiQRAP Software

At the command prompt enter the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt install git -y

Then enter the following...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ pwd

The output should be '/home/pi'

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ git clone [https://github.com/arcaicandy/PiQRAP.git](https://github.com/arcaicandy/PiQRAP.git)

If all is successful then you should now have a folder called PiQRAP in your home directory.

You can check this by entering the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ ls

You should see the PiQRAP folder listed among the others.

### 2\. Setup PiQRAP Components and Dependancies

Please refer to section 2 of 'Install and Configure PiQRAP' in build-instructions.md.

### 3\. Prepare Your USB Stick

Please refer to section 3 of 'Install and Configure PiQRAP' in build-instructions.md.

### 4\. Setup Sound Output

Please refer to section 4 of 'Install and Configure PiQRAP' in build-instructions.md.

### 5\. Run PiQRAP \(First run\)

Please refer to section 5 of 'Install and Configure PiQRAP' in build-instructions.md.

### 6\. QRCards

Please refer to section 6 of Install and Configure PiQRAP' in build-instructions.md.

### 7\. Notes

Please refer to section 7 of 'Install and Configure PiQRAP' in build-instructions.md.

### 8\. Automatically Running PiQRAP on Boot

If you are running PiQRAP headless then you need it to startup after boot when you turn your Rapsberry Pi on.

There are two steps to this. First making the Pi login automatically and second running PiQRAP when it logs in.

Edit the .bashRC file in the home/pi folder...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /home/pi/.bashrc

Add the following line as the last line in the file...

```
/home/pi/PiQRAP/piqrap.sh
```

This will automatically run PiQRAP when the Pi user logs in. It will only run if you log on from the Pi console (tty1) so you can still login using SSH and not automatically run PiQRAP.

Now the final step. Make the Pi login automatically.

Run raspi-config...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo raspi-config

Select 'System options' -> 'Boot / Auto Login' -> Console Autologin

Reboot and the Pi should bootup, login and run PiQRAP.

### 9\. Extra Credit

Look in the documentation folder for the following...
<br>
* build-read-only - Instructions on making the OS SD-Card readonly. Lengthens life of card and power off without shutdown
* build-fastboot - Instructions on speeding up the boot time of the Pi. Boots to 'Player read' in approx 22 seconds (Pi 4).