# PiQRAP Configuraton and Operation

The behaviour of PiQRAP can be altered in two ways,

1. Via the configuration (YAML) files
2. By the use of QRCards

## Configuration files

When PiQRAP starts up it first looks for a configuration file called piqrap.yml on the boot partition of the Raspberry Pi (/boot/cpiqrap.yml). It then scans the /media/pi folder and looks for the first folder it finds with a 'Music' folder in it. If that folder has a piqrap.yml file in it it is loaded and merged with the /boot/piqrap.yml thereby overwritting any settings with the same key.
This effectively allows you to set your default options (in the /boot/piqrap.yml file) and then have different options for each USB stick you use.

### Available Configuration Options

The default state of the /boot/piqrap.yml is as follows...
```
# outputDevice
# Controls the audio output device that PiQRAP uses to output audio.
# alsa:hw,0,0   - Default output device for Raspberry Pi can be either HDMI or Line out depending on Pi config
# alsa:dmixer   - Allows mixing of sound outputs for use on harware like USB sound cards - Requires additional config - See documentation/dmixer

outputDevice: 'alsa:hw,0,0'

# debug
# true/false  - If false then no logging will be perfomed. This is used when the system is setup as a read only device.

debug: false

# logLevel:
# INFO/DEBUG - Controls the amount of logging if debug is set true - If things arent working then setdebug to true and logLevel to DEBUG

logLevel: INFO

# shuffle 
# true /false - Shuffle tracks in playlist when play list changed. Otherwise tracks are played in order they were found

shuffle: false

# rebuildqrcards
# If True PiQRAP will rebuild the QRCards on any USB drive found everytime it starts. If you have made lots of changes to the playlists on the USB drive then this will rebuild everything.
# If false PiQRAP will still created QRCards for any new playlist folders found but wont touch those it has done before.
# This would normally be set false in the /boot/piqrap.yml and overridden in the piqrap.yml file in the Music folder on your USB drive if required.

rebuildqrcards: false
```

## QRCards

When PiQRAP is running it is controlled entirely by the use of QRCards that PiQRAP itself generates.

### Playlist QRCards

PiQRAP generates one QRCard for each playlist found in the 'Music' folder of the attached USB Drive. These cards are placed in the 'qrcards' folder in the root of the attached USB Drive.
Holding one of these cards up to the Pi's camera will switch playback to the playlist indicated by the QRCard and restart playback.

### Control QRCards

PiQRAP generates 4 QRCards that allow control of music playback.
* PLAY/PAUSE - Pauses the current track if it is playing or restarts playback if it is paused.
* PREVIOUS - Skip playback to the start of the track or if within two seconds of the start skips to the previous track.
* NEXT - Skips playback to the next track
* SHUFFLE - Randomly shuffles the current playlist and restarts playback