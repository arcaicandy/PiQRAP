# Reducing Boot Time

In a standard Raspberry Pi OS installation PiQRAP takes around 35+ seconds to boot up to the point where it announces 'Scanning Music Folder'. 

In a headless system there is no real activity to let the use know what is going on and whether the system is starting up properly so it is advantageous to reduce this period as much as is possible.

This guide describes how to do that while leaving networking/ssh available so you can still log in to the Pi and make changes. You can improve start time further by removing networking but this guide gets the start time down to around 22 seconds.

This guide was compiled primarily from information on the following two links.

https://himeshp.blogspot.com/2018/08/fast-boot-with-raspberry-pi.html
https://k3a.me/how-to-make-raspberrypi-truly-read-only-reliable-and-trouble-free/

## Disable Services That Are Not Required 

sudo systemctl disable bluetooth.service
sudo systemctl disable hciuart.service
sudo systemctl disable rpi-eeprom-update.service
sudo systemctl disable raspi-config.service
sudo systemctl disable keyboard-setup.service
sudo systemctl disable apt-daily.service
sudo systemctl disable avahi-daemon.service
sudo systemctl disable systemd-timesyncd.service
sudo systemctl disable systemd-rfkill.service

## Remove IPV6 Functionality

edit /etc/dhcpcd.conf – at the end add:

noarp
ipv4only
noipv6

## Raspberry Pi Config Changes

Speed up tricks for headless installation

/boot/config.txt

### Disable bluetooth
dtoverlay=disable-bt

###################
/boot/cmdline.txt – after default line add parameters for quite boot and speed up process for KIOSK MODE
#noatime nodiratime data=writeback quiet splash logo.nologo vt.global_cursor_default=0 loglevel=0

quiet splash logo.nologo 

##############################################
/boot/config.txt
[all]
#dtoverlay=vc4-fkms-v3d
start_x=1
gpu_mem=128

### Disable the rainbow splash screen
disable_splash=1
### Set the bootloader delay to 0 seconds. The default is 1s if not specified.
boot_delay=0
### Overclock the SD Card from 50 to 100MHz
This can only be done with at least a UHS Class 1 card

dtoverlay=sdtweak,overclock_50=100

### Disable wait for network on startup

raspi-config