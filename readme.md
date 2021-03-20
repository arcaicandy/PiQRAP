# PiQRAP - A Raspberry Pi QR code controlled audio player.

<img src="https://github.com/arcaicandy/PiQRAP/raw/master/documentation/assets/PiQRAP.jpg" alt="An image of the PiQRAP QR code controlled music player" width="250"> <img src="https://github.com/arcaicandy/PiQRAP/raw/master/documentation/assets/example-qr-cards.jpg" alt="An image of the QR cards producsed by PiQRAP" width="300">

## Introduction

Initiated by a [request](https://www.facebook.com/groups/RaspberryPiProjects/permalink/1810841379091256) by Dave Taylor on the Facebook group [Raspberry Pi Projects](https://www.facebook.com/groups/RaspberryPiProjects).

Dave has a sister that has special needs, loves music but has difficulties with managing CD's and despite Dave trying various streaming solutions these haven't worked out for her either.

Dave was thinking of building something along the lines of [Juuke](https://www.youtube.com/watch?v=5Y1Psf6igHE) which is a RFID card controlled player using an Arduino based player and some other hardware.

It's cool but I thought the barrier of entry for many people would be too high (soldering, 3D printing, programming etc..) and wondered whether something simpler/easier could be built usign a Raspberry Pi with a camera and QR Codes for control. It does like the author of Juuke was trying to get a commercial solution done but as far as I can tell it's died a death.

I suggested to Dave I would try to do something and eventually have come up with PiQRAP.

## See it in action

[A short demonstration video on YouTube](https://youtu.be/FiyGeKrGX2s)

## What is it?

PiQRAP is an audio/mp3 player that allows the user to control the playback of music stored on an external USB Stick using QRCards.

It is written in Python and uses the OMXPlayer to play audio.

You add your music to folders on a USB Stick (these can be individual albums or folders with multiple albums or folders with whatever collection of MP3 files you want). You then insert the stick in the Raspberry Pi and turn it on.

PiQRAP will then treat each folder as a playlist and play it in order or shuffled. You can switch playlists simple by holding up a QRCard infront of the Raspberry Pi. You can change playlist, skip tracks or pause/play all by holding up the appropriate QRCard.

QRCards (an image comprising a QRCode, Album art and text description) are automatically generated by the program so they can be easily printed out and laminated.

Functionality is deliberately limited but entirely controlled by QRCards. No buttons are on the device and once turned on no physical contact is required. Control is managed by holding up a QRCard in the correct orientation, in front of the device, anywhere between 5 to 15 cms away. It seems pretty tolorant of position so super accuracy is not required. This of course could still be an issue for some users so it's not going to be suitable for everyone.

It is most likely of use for anyone who has issue/difficulties with managing and playing CDs or using/controlling streaming services and could be of use for those with special needs, elderly, alzheimers. To be honest I don't know who it could be useful for as the only use case I know at the moment is Dave's sister and at time of writing we don't know if it will be useful for her yet. if you have other suggestions, definate use cases or need help then please let me know.

## Functionality

### Music/player functions

* Play/Pause
* Skip track forward/backward
* Change music folder
* Shuffle music folder

### Other

Automatic genration of QRCards that are used to control the player.

## What you need

### Required

You will need the following as a minimum...

* Raspberry Pi 4 - A RPi 3 will probably work fine but not tested.
* Raspberry Pi 4 power supply.
* Raspberry Pi Camera Module.
* SD-Card - Get as fast as you can, all dev work was on 16g Sandisk Ultras. 8g would be fine.
* USB Stick - Again as fast as possible. I have been using a Lexar JUMPDRIVE S47 32GB USB 3.1. Size depends on how much music you need.

### Optional

These components are optional depending on what you want to do.

* Case for the Pi and camera - Obviously you can build your own enclosure if you wish but not required.
* External speakers - I strongly suggest mains powered and not USB so as to minimise RPi power requirements. If your only using headphones then you dont need these.
* USB Sound card or Raspberry Pi Audio HAT - Not essential but the sound output from the audio out on the RPi is pretty poor.
* Credit card sized self laminataed pouches - You can just use printed cards but laminiating makes them more robust.
* HDMI Monitor, HDMI cable suitable to Raspberry Pi 4 (If using Pi4) - You'll need a display for initial setup/config but not afterwards.
* Keyboard and mouse - Again needed for setup/config but not afterwards.

## Costs

Approximate/indicative costs are below. These are in UK Pounds as of 20th March 2021 and based on prices in the UK.
<br>
* Raspberry Pi 4 - £35.00
* Power supply - £7.50
* Camera module - £24.00
* SD Card - £7.50
* USB Stick - £12.00
* Case - £10.00
* External speakers - £15.00
* USB sound card - £6.00
* Pi4 Audio hat - £20+
* Laminated pouches - £15.00 (for 50)

So a minimal required build cost is approx £85.00
My recommended build would be approx £105.00 (USB sound card, external speakers)

Of course much of these costs can be reduced if you already have parts and can reuse them or your use case doesn't require them.

## Alternatives

[Juuke](https://ananords.com/juuke-a-rfid-music-player-for-elderly-and-kids/) - Arduino RFID based audio player - Original inspiration for PiQRAP. Much higher barrier to entry.
[Phoniebox](http://phoniebox.de/index.html) - Very complete looking Raspberry PI 3 RFID based audio player. Typically only found the the day I did this readme. Ho hum.

## Work in progress

Build headless, read only image to allow faster startup and safe power off without OS shutdown.
Build instructions, dependancies etc...

## Future plans

RFID control