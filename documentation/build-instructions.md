# PiQRAP - Build instructions

## Requirements

### Raspberry Pi 4

Standard Raspberry PI 4. Any memory size will be fine but no advantage or reason for anything more than the base level memory.

### Raspberry Pi 4 PSU

Doesnt have to be the official PSU but recommend that it is. Don't cheap out on the PSU the Pi4 can be extremely picky about power and uses a fair bit more than the Pi3.
If you are going to try to use USB speakers then be aware you might have power issues.

### Camera Module

PiQRAP uses the offical Raspberry Pi Camera. Others may/should work but are not supported.

### HDMI Monitor and cable (micro HDMI for RPI4)

Anything should be ok but often isn't. I can't really guide you on this but I have had older HDMI monitors that the Pi just will not recognise and use or have wierd display issues. It can be a nightmare.
If you have problems then try another monitor or cable or both.
If you are buying cables get official ones or from a specialist Pi store.

### USB Mouse and keyboard

Anything should be ok.

### Speakers/Headphones

To hear the music PiQRAP is playing you will need either speakers or headphones.
If you are using speakers then be aware that using USB speakers powered through the Pi add additional power requirements and could make your Pi unstable. It is highly recommended that if using speakers you use externally powered ones.

### SD-Card

The SD-Card size should be 8Mb or greater but doesnt need to be as music is not stored on the card itelf. It's best to get the fastest type of card you can. Not neccessary but the faster it is the faster the player will start up and the faster performing these instructions will be.

### USB Stick

The music that PiQRAP plays needs to be on a USB Stick inserted in one of the USB sockets of the Raspberry Pi.
Size can be whatever you need for your music upto the limits supported by the Module of Pi you are using.

## Setting up the Raspberry Pi OS

### 1\. Burn the Raspberry Pi OS \(32 bit\) image

This guide uses the version of Raspberry Pi OS with the desktop windowing/GUI system installed. It's not neccessary to use the GUI and for most applications once PiQRAP is configured you won't use it at all but it does make the setup process easier. It also helps with debugging if you have issues.

It is recommended you use the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) available from the [Raspberry Pi Foundation website](https://www.raspberrypi.org/).

Follow the [Installing Operating System Images Guide](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) from the Raspberry Pi Foundation.

### 2\. First Boot

Put your newly imaged SD-Card in your Raspberry Pi and power it up. You should get the desktop displayed on your monitor.
The desktop has a wizard that will talk you through connecting your Pi to your Wifi. Follow it all the way through, let it update software and then restart.

### 3\. Enable Camera Support

From the desktop select the Raspberry Icon in the top left corner, then preferences and then Raspberry Pi Configuration.
Now select the interfaces tab and enable the camera and, while we are here, SSH (this is optional but may be useful in the future so if you know you wont need it feel free to skip SSH).

When asked to reboot/restart say yes.

### 4\. Test the Camera

Start a terminal window by clicking on the right most icon on menu bar on the desktop. The icon looks like '>\_'

In the termninal window that opened enter the following command at the command prompt...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP $</span> $ raspistill -o Desktop/image.jpg

You should see a preview displayed on the desktop for 5 seconds and then a picture will be taken and saved to your Desktop.

Double click image.jpg on the Desktop to see your image.

### 5\. Download the Latest PiQRAP Software

In your terminal window (open another if you closed the first) enter the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP $</span> $ pwd

The output should be '/home/pi'

If it's not then close the terminal window and open another.
If it is then enter the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP $</span> $ git clone [https://github.com/arcaicandy/PiQRAP.git](https://github.com/arcaicandy/PiQRAP.git)

If all is successful then you should now have a folder called PiQRAP in your home directory.

You can check this by entering the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP $</span> $ ls

You should see the PiQRAP folder listed among the others.

### 6\. Setup PiQRAP Components and Dependancies

Now we need to add all the support files and components that PiQRAP needs to function.

Simply enter the following command and all should be done for you...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP $</span> ./PiQRAP/build.sh

### 7\. Prepare Your USB Stick

PiQRAP searches for music in the 'music' folder of any USB stick that is inserted in one of the Raspberry Pis USB sockets.

Place all your folders of music in a folder called 'music' in the root of your USB Stick. At present PiQRAP only looks for MP3 files. You can do this on the Raspberry Pi itself or on any other PC or Mac.
In each folder you added under the 'music' folder you can also place a JPG image called 'Folder.jpg'. PiQRAP will use this image when creating the QRCards used to control the play back of your music.

### 8\. Setup Sound Output

Possibly the most error prone part of the process so have patience.

PiQRAP uses the ALSA sound system in Linux to play the music. More accurately it uses OMXPlayer which can be told what hardware to use to play music on.

Devices used by the ALSA system are referenced by the order in which they are found by the Pi which has the annoying habit in that the devices can change depending on what you have plugged in and where.

You can see what audio devices your Raspberry Pi has by entering the follwing command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ aplay -l

\*\*\*\* List of PLAYBACK Hardware Devices \*\*\*\*
card 0: b1 [bcm2835 HDMI 1], device 0: bcm2835 HDMI 1 [bcm2835 HDMI 1]
  Subdevices: 4/4
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
card 1: Headphones [bcm2835 Headphones], device 0: bcm2835 Headphones [bcm2835 Headphones]
  Subdevices: 4/4
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
card 2: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

The output from 'aplay -l' (on my Raspberry Pi) shows 3 devices. HDMI (card 0), Headphones (card 1) and a USB Soundcard (card 3).

So in the above scenario the available alsa sound devices are...

alsa:hw:0,0  -  The HDMI output - If you have something connected via HDMI then this device will exist
alsa:hw:1,0  -  The Line Out of the Pi - All should have this
alsa:hw:2,0  -  The USB sound card attached to the Raspberry Pi

However if I disconnect my HDMI monitor and reboot the Pi I get the follwing output from 'aplay -l'

\*\*\*\* List of PLAYBACK Hardware Devices \*\*\*\*
card 0: Headphones [bcm2835 Headphones], device 0: bcm2835 Headphones [bcm2835 Headphones]
  Subdevices: 8/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 1: Device [USB Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

Notice that the HDMI card which was card 0 has dissapeared (not surprising as its been unplugged) but this means the other two cards have now shifted down to become card 0 and card 1.
If you had setup PiQRAP to use the USB sound card (Card 2, alsa:hw:2,0) it now no longer exists as it has moved to card 1. Doh!

The bottom line is to initaily use alsa:hw:0,0 and this should be either the Raspberry Pi line out or the HDMI out. Seeing if you are getting sound via one of these should let you confirm that PiQRAP is working.
once you have confirmed that PiQRAP is working you can then try other devices always remembering that removing and HDMI cable or USB sound card can change any remaining output device card numbers and screw up PiQRAP.

#### Setting PiQRAPs Output Device

To actually set the hardware device that PiQRAP should use to what you want edit the piqrap.yml file in the /boot directory of the Raspberry Pi. Instructions are in the file. Use the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /boot/piqrap.yml

#### Notes on USB Sound Cards

My testing has found that (cheap???) USB sound cards only allow one sound to play through them at a time. This is a problem for PiQRAP as it can sometime try to play more than one sounds at a time.
This was solved by using an asound mixer called dmixer.
When PiQRAP is installed it copies a file to /etc/asound.confg which contains the dmixer definition.
The problem is I dont know where your USB sound card will appear in the device list so you may need to edit /etc/asound.conf to make sure its using the correct hardware.

To do this edit the /etc/asound.confg file and change it to use the correct hardware device. Instructions are in the file. Use the following command...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ sudo nano /etc/asound.conf

### 9\. Run PiQRAP \(First run\)

Now you are ready to run PiQRAP. Make sure you speakers/headphones are on and your USB Stick plugged in.
Open a terminal window and enter the following commands...

<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ cd PiQRAP<br>
<span class="colour" style="color:rgb(0, 255, 0)">pi@PiQRAP</span>:<span class="colour" style="color:rgb(102, 119, 255)">\~/PiQRAP</span> $ python3 piqrap.py

PyQRAP should start and you should hear 'Scanning Music Folder' followed a shortwhile after by 'Player ready"

At this point you will be stuck. You have no way to tell PiQRAP what to do. Luckily PiQRAP when it starts up and scans the 'music' folder on the USB Stick will create another folder on the stick called 'QRCards'. Read on.

### 10\. QRCards

After starting PiQRAP at least once, in the 'QRCards' folder on the USB Stick, you will find the control cards you need to control play back and a card for each folder you added along with an image from the Folder.jpg file you added to each.

At this point you can shutdown the Pi and place the USB Stick in whatever computer you wish and open the QRCards and print them out. They are designed to be credit card size when folded over and you should aim to print them as close to this size as possible. Other sizes may work fine but have not been tested.

Once you have printed your QRCards then make sure the USB drive is back in the Pi and start it up again and test you cards.

### 11\. Notes

* Camera orientation - I have found having the camera looking horizontal is best. It is sensitive to changes in background lighting so if its seeing a bright light and you then hold a card in front the image darkens and it takes a while fo the camera to settle and see the QR Code.
* Sound hardware issues - Discussed above. Please read it.
