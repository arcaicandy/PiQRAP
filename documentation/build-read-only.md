# Making Raspberry Pi OS Lite Readonly

These instructions are taken almost verbatim from - [How to make your Raspberry Pi file system read-only (Raspbian Stretch)](https://medium.com/swlh/make-your-raspberry-pi-file-system-read-only-raspbian-buster-c558694de79) by andreas.schallwig

Strictly speaking you don't HAVE to do any of this.

PiQRAP doesn't require this to run but having the Pi OS set read only has the following advantages...

* It means that you can turn the Pi off without shutting it down without risk of file corruption Useful if your running PiQRAP headless (no monitor or keyboard).
* It increases the reliability of the OS SD-Card as when in operation the Pi will no longer be writing to it.

### 1\. Remove Unnecessary Packages

pi@PiQRAP:\~/PiQRAP $ sudo apt-get remove --purge triggerhappy logrotate dphys-swapfile -y

pi@PiQRAP:\~/PiQRAP $ sudo apt-get autoremove --purge -y

### 2\. Disable swap and filesystem check and set it to read\-only

Edit the file /boot/cmdline.txt

pi@PiQRAP:\~/PiQRAP $ sudo nano /boot/cmdline.txt

Add the following three words at the end of the line:

```
fastboot noswap ro
```

### 3\. Replace the Log Manager

pi@PiQRAP:\~/PiQRAP $ sudo apt-get install busybox-syslogd -y

pi@PiQRAP:\~/PiQRAP $ sudo apt-get remove --purge rsyslog -y

### 4\. Make the file-systems read-only and add temporary file system entries

pi@PiQRAP:\~/PiQRAP $ sudo nano /etc/fstab

Add the ',ro' flag to all block devices

The updated file should look like this:

```
proc                  /proc     proc    defaults             0     0
PARTUUID=fb0d460e-01  /boot     vfat    defaults,ro          0     2
PARTUUID=fb0d460e-02  /         ext4    defaults,noatime,ro  0     1
```

Also add the entries for the temporary file system at the end of the file:

```
tmpfs        /tmp            tmpfs   nosuid,nodev         0       0
tmpfs        /var/log        tmpfs   nosuid,nodev         0       0
tmpfs        /var/tmp        tmpfs   nosuid,nodev         0       0
```

### 5\. Move Various System Files to the Temp Filesystem

pi@PiQRAP:\~/PiQRAP $ sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/spool /etc/resolv.conf

pi@PiQRAP:\~/PiQRAP $ sudo ln -s /tmp /var/lib/dhcp

pi@PiQRAP:\~/PiQRAP $ sudo ln -s /tmp /var/lib/dhcpcd5

pi@PiQRAP:\~/PiQRAP $ sudo ln -s /tmp /var/spool

pi@PiQRAP:\~/PiQRAP $ sudo touch /tmp/dhcpcd.resolv.conf

pi@PiQRAP:\~/PiQRAP $ sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf

### 6\. Update the systemd Random Seed

Link the random-seed file to the tmpfs location:

pi@PiQRAP:\~/PiQRAP $ sudo rm /var/lib/systemd/random-seed

pi@PiQRAP:\~/PiQRAP $ sudo ln -s /tmp/random-seed /var/lib/systemd/random-seed

### 7\. Make Sure the random\-seed File is Created on Boot\.

Edit the service configuration file...

pi@PiQRAP:\~/PiQRAP $ sudo nano /lib/systemd/system/systemd-random-seed.service

Under the [Service] section add the following line...

```
ExecStartPre=/bin/echo "" >/tmp/random-seed
```

The modified [Service] section should look like this...

```
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/echo "" >/tmp/random-seed
ExecStart=/lib/systemd/systemd-random-seed load
ExecStop=/lib/systemd/systemd-random-seed save
TimeoutSec=30s
```

### 8\. Add Shell Commands

Here we create two shell commands ro (read-only) and rw (read-write) which can be used at any time to switch between the modes. In addition it will add an indicator to your command prompt to show the current mode.

Edit the file /etc/bash.bashrc and add the following lines at the end...

pi@PiQRAP:\~/PiQRAP $ sudo nano /etc/bash.bashrc

```
set_bash_prompt() {
  fs_mode=$(mount | sed -n -e "s/^\/dev\/.* on \/ .*(\(r[w|o]\).*/\1/p")
  PS1='\[\033[01;32m\]\u@\h${fs_mode:+($fs_mode)}\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
}
alias ro='sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
alias rw='sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
PROMPT_COMMAND=set_bash_prompt
```

### 9\. Ensure File System is Returned to read\-only on Log Out

We need to ensure the file system goes back to read-only when you log out (if it was changed).

Edit the file /etc/bash.bash\_logout...

pi@PiQRAP:\~/PiQRAP $ sudo nano /etc/bash.bash\_logout

Add the following lines at the end...

```
mount -o remount,ro /
mount -o remount,ro /boot
```

### 10\. Reboot

All done now so we can reboot and the Pi should boot up as normal.

pi@PiQRAP:\~/PiQRAP $ sudo reboot

Remember it will boot up in read-only mode so if you need to make any changes you will need enter the following command

pi@PiQRAP:\~/PiQRAP $ rw