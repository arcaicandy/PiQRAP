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

Follow the [Installing Operating System Images Guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) from the Raspberry Pi Foundation.

### 2\. First Boot

Put your newly imaged SD-Card in your Raspberry Pi and power it up. You should eventually get the logon prompt on your monitor if you have one connected.

### 3\. Configuration Options and Enabling Camera Support

Use the raspi-config utility to setup any options/configuration choices you want for your Pi (Networking, SSH etc..).

From the command line prompt enter the following...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo raspi-config

Now select the options to enable the camera and, while we are here, SSH (this is optional but may be useful in the future so if you know you wont need it feel free to skip SSH).

When asked to reboot/restart say yes.

### 4\. Update the OS \(Raspberry Pi OS Lite\)

We need to make sure that all the packages we have and will istall are the latest versions so enter the following commands at the command prompt...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt-get update -y\
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt full-upgrade -y\

### 5\. Test the Camera

If you have a monitor attached to your Pi then from the command prompt enter the following commands:

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get -y install fbi -y\
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ raspistill -o image.jpg\
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ fbi -a image.jpg

If you dont have a monitor attached then then you can still do the 'raspistill' to grab an image but you will need to copy the image.jpg file from the Raspberry Pi to another machine to view it (beyond scope of this document).

### 6\. Install USBMount

Unlike the Raspberry Pi OS Desktop OS version the 'Lite' version of Raspberry Pi OS does not include any software to automatically mount (make available) USB sticks/hard drives. As PiQRAP expects the music it is playing to be on a USB hard drive we need to install software to make this happen.

To do this we use a package called USBMount.

Please refer to the file usbmount-config.md in the documentation directory for instructions on how to do this.

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