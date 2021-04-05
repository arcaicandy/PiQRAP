Install usbmount
sudo apt get install usbmount -y
Update usbmount configuration
sudo nano /lib/systemd/system/systemd-udevd.service
PrivateMounts=no
MountFlags=shared
Update usbmount.conf
sudo nano /etc/usbmount/usbmount.conf
FS\_MOUNTOPTIONS="-fstype=vfat,umask=0000"
Create symbolic link (media/pi/usb)
sud mkdir /media/pi
sudo ln -s /media/usb /media/pi/usb

<br>
<br>
