## Making Raspberry Pi OS Lite Readonly

These instructions are taken almost verbatim from - [How to make your Raspberry Pi file system read-only (Raspbian Stretch)](https://medium.com/swlh/make-your-raspberry-pi-file-system-read-only-raspbian-buster-c558694de79) by andreas.schallwig

Strictly speaking you don't HAVE to do any of this.

PiQRAP doesn't require this to run but having the Pi OS set read only has the following advantages...
<br>
* It means that you can turn the Pi off without shuting it down without risk of file corruption Useful if your running PiQRAP headless (no monitor or keyboard).
* It increases the reliability of the OS SD-Card as when in operation the Pi will no longer be writting to it.

### 1\. Remove Unneccessary Packages\.\.\.
<br>
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get remove --purge triggerhappy logrotate dphys-swapfile
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get autoremove --purge

### 2\. Disable swap and filesystem check and set it to read\-only

Edit the file /boot/cmdline.txt

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /boot/cmdline.txt

Add the following three words at the end of the line:

`fastboot noswap ro`

### 3\. Replace the Log Manager
<br>
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get install busybox-syslogd
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo apt-get remove --purge rsyslog

Make the file-systems read-only and add the temporary storage

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /etc/fstab

Add the ,ro flag to all block devices.

The updated file should look like this:

`proc                  /proc     proc    defaults             0     0`
`PARTUUID=fb0d460e-01  /boot     vfat    defaults,ro          0     2`
`PARTUUID=fb0d460e-02  /         ext4    defaults,noatime,ro  0     1`

Also add the entries for the temporary file system at the end of the file:

`tmpfs        /tmp            tmpfs   nosuid,nodev         0       0`
`tmpfs        /var/log        tmpfs   nosuid,nodev         0       0`
`tmpfs        /var/tmp        tmpfs   nosuid,nodev         0       0`

### 4\. Move Various System Files to the Temp Filesystem
<br>
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/spool /etc/resolv.conf
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo ln -s /tmp /var/lib/dhcp
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo ln -s /tmp /var/lib/dhcpcd5
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo ln -s /tmp /var/spool
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo touch /tmp/dhcpcd.resolv.conf
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf

### 5\. Update the systemd Random Seed

Link the random-seed file to the tmpfs location:

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo rm /var/lib/systemd/random-seed
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo ln -s /tmp/random-seed /var/lib/systemd/random-seed

### 6\. Make Sure the random\-seed File is Created on Boot\.

Edit the service configuration file...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /lib/systemd/system/systemd-random-seed.service

Under the [Service] section add the following line...

`ExecStartPre=/bin/echo "" >/tmp/random-seed`

The modified [Service] section should look like this...

`[Service]`
`Type=oneshot`
`RemainAfterExit=yes`
`ExecStartPre=/bin/echo "" >/tmp/random-seed`
`ExecStart=/lib/systemd/systemd-random-seed load`
`ExecStop=/lib/systemd/systemd-random-seed save`
`TimeoutSec=30s`

### 7\. Add Shell Commands

Here we create two shell commands ro (read-only) and rw (read-write) which can be used at any time to switch between the modes. In addition it will add an indicator to your command prompt to show the current mode.

Edit the file /etc/bash.bashrc and add the following lines at the end...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /etc/bash.bashrc

`set_bash_prompt() {`
`    fs_mode=$(mount | sed -n -e "s/^\/dev\/.* on \/ .*(\(r[w|o]\).*/\1/p")`
`    PS1='\[\033[01;32m\]\u@\h${fs_mode:+($fs_mode)}\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '`
`}`
`alias ro='sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'`
`alias rw='sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'`
`PROMPT_COMMAND=set_bash_prompt`

### Ensure File System is Returned to read-only on Log Out

We need to ensure the file system goes back to read-only when you log out (if it was changed).

Edit the file /etc/bash.bash\_logout...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /etc/bash.bash\_logout

Add the following lines at the end...

`mount -o remount,ro /`
`mount -o remount,ro /boot`

### 8\. Make Sure /tmp Folder is Writable by Anyone
<br>
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo chmod uga+rwx /tmp

### 9\. Reboot

All done now so we can reboot and the Pi should boot up as normal.

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo reboot

Remember it will boot up in read-only mode so if you need to make any changes you will need enter the following command

$ rw