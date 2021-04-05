# PiQRAP - Headless Build Instructions

## Introducton

This file describes how to build a version of PiQRAP that does not have any monitor/graphical desktop connected while in use. It also shows how to configure PiQRAP so that the OS SD-Card is set as read only so you can just turn PiQRAP off when you are done without risking corruption of the file system. This also should extend the life of the OS SD-Card greatly.

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

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt-get update -y
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> sudo apt full-upgrade -y

### 5\. Test the Camera

If you have a monitor attached to your Pi then from the command prompt enter the following commands...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get -y install fbi -y
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ raspistill -o image.jpg
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ fbi -a image.jpg

If you dont have a monitor attached then then you can still do the 'raspistill' to grab an image but you will need to copy the image.jpg file from the Raspberry Pi to another machine to view it (beyond scope of this document).

### 6\. Install USBMount

Unlike the Raspberry Pi OS Desktop OS version the 'Lite' version of Raspberry Pi OS does not include any software to automatically mount (make available) USB sticks/hard drives. As PiQRAP expects the music it is playing to be on a USB hard drive we need to install software to make this happen.

To do this we use a package called USBMount.

Please refer to the file usbmount-config.md in the documentation directory for instructions on how to do this.

### 7\. Download the Latest PiQRAP Software

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

### 8\. Setup PiQRAP Components and Dependancies

Now we need to add all the support files and components that PiQRAP needs to function.

Simply enter the following command and all should be done for you...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ ./PiQRAP/build.sh

### 9\. Make Raspberry Pi OS Lite Readonly
<br>
From - [https://medium.com/swlh/make-your-raspberry-pi-file-system-read-only-raspbian-buster-](https://medium.com/swlh/make-your-raspberry-pi-file-system-read-only-raspbian-buster-c558694de79) by andreas.schallwig

sudo apt-get remove --purge triggerhappy logrotate dphys-swapfile
sudo apt-get autoremove --purge

Edit the file /boot/cmdline.txt and add the following three words at the end of the line:
    fastboot noswap ro

Replace your log manager
sudo apt-get install busybox-syslogd
sudo apt-get remove --purge rsyslog

Update the file /etc/fstab and add the ,ro flag to all block devices. The updated file should look like this:
proc                  /proc     proc    defaults             0     0
PARTUUID=fb0d460e-01  /boot     vfat    defaults,ro          0     2
PARTUUID=fb0d460e-02  /         ext4    defaults,noatime,ro  0     1
Also add the entries for the temporary file system at the end of the file:
tmpfs        /tmp            tmpfs   nosuid,nodev         0       0
tmpfs        /var/log        tmpfs   nosuid,nodev         0       0
tmpfs        /var/tmp        tmpfs   nosuid,nodev         0       0

Move some system files to temp filesystem
sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/spool /etc/resolv.conf
sudo ln -s /tmp /var/lib/dhcp
sudo ln -s /tmp /var/lib/dhcpcd5
sudo ln -s /tmp /var/spool
sudo touch /tmp/dhcpcd.resolv.conf
sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf

Update the systemd random seed
Link the random-seed file to the tmpfs location:
$ sudo rm /var/lib/systemd/random-seed
$ sudo ln -s /tmp/random-seed /var/lib/systemd/random-seed

Edit the service configuration file /lib/systemd/system/systemd-random-seed.service to have the file created on boot.
Add the line ExecStartPre=/bin/echo "" >/tmp/random-seed under the [Service] section.

The modified [Service] section should look like this:
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/echo "" >/tmp/random-seed
ExecStart=/lib/systemd/systemd-random-seed load
ExecStop=/lib/systemd/systemd-random-seed save
TimeoutSec=30s

Adding some useful commands to switch between RO and RW modes
Here we create two shell commands ro (read-only) and rw (read-write) which can be used at any time to switch between the modes. In addition it will add an indicator to your command prompt to show the current mode.
Edit the file /etc/bash.bashrc and add the following lines at the end:
set\_bash\_prompt() {
    fs\_mode=$\(mount \| sed \-n \-e "s/^\\/dev\\/\.\* on \\/ \.\*\(\\\(r\[w\|o\]\\\)\.\*/\1/p"\)
    PS1='\\[\033[01;32m\\]\u@\h${fs\_mode:+($fs\_mode)}\\[\033[00m\\]:\\[\033[01;34m\\]\w\\[\033[00m\\]\\$ '
}
alias ro='sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
alias rw='sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
PROMPT\_COMMAND=set\_bash\_prompt

<br>
Finally ensure the file system goes back to read-only once you log out.
Edit (or create) the file /etc/bash.bash\_logout and add the following lines at the end:
mount -o remount,ro /
mount -o remount,ro /boot

\# Make sure /tmp folder is writable by anyone
sudo chmod uga+rwx /tmp

<br>
<br>
