#!/usr/bin/env python3
from pathlib import Path
from time import sleep

import time
import logging, logging.handlers
import signal, sys, os, getopt
import os.path
import curses

from modules.config import Configuration
from modules.mediaPlayerSingle import Player
from modules.media import MediaFile, PlayList
from modules.musicFolder import MusicFolder
from modules.events import Events
from modules.camera import Camera

# Global variables
requestSwitchMediaFolder = False
requestVolumeUp = False
requestVolumeDown = False
requestPlayOrPause = False
requestPlayNext = False
requestPlayPrevious = False
requestShuffle = False

# Signal handler - Cleans up in case of control C
def signal_handler(sig, frame):

    global quit

    logger.debug("CTRL C detected")

    quit = True

def cleanUp():

    logger.debug("Performing cleanup")

    player.quit()

    # Stop the camera
    camera.stop()

    curses.nocbreak()
    curses.echo()
    curses.endwin()

    logger.info("Exiting program")

    sys.exit(0)

def qrDataReceived(qrData):

    global indexMediaFolder
    global requestSwitchMediaFolder
    global requestPlayNext
    global requestPlayPrevious
    global requestPlayOrPause
    global requestShuffle

    logger.debug("QR received: " + qrData)

    if qrData.isdigit():

        indexMediaFolder = int(qrData)

        requestSwitchMediaFolder = True

    elif qrData == 'SHUF':

        requestShuffle = True

    elif qrData == 'PREV':

        requestPlayPrevious = True

    elif qrData == 'NEXT':

        requestPlayNext = True

    elif qrData == 'PORP':

        requestPlayOrPause = True

# Load root config/s
# First load from the root directory of the program
config = Configuration().loadConfig(os.path.join(os.getcwd(), "piqrap.yml"))

# Now load from /boot so settings can be easily overridden
config.mergeConfig("/boot/piqrap.yml")

# Get config values falling back to defaults
outputDevice = config.outputDevice or "alsa:hw:0,0"
debug = config.debug
loglevel = config.logLevel or "INFO"
shuffle = config.shuffle

# Setup logging
logger = logging.getLogger('__name__')

# If debugging then use the log file handler. - Make sure partition is r/w when doing this  
if debug:

    logger.setLevel(getattr(logging, loglevel.upper()))

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s -> %(filename)s:%(funcName)s:%(lineno)s")

    fileHandler = logging.handlers.RotatingFileHandler("piqrap.log", maxBytes=(1048576 * 1), backupCount=2)
    fileHandler.setFormatter(logFormatter)

    logger.addHandler(fileHandler)

# Not debugging so direct all logging to NullHandler as in theory partition won't be writtable.
else:

    logger.addHandler(logging.NullHandler())

logger.info("PiQRAP starting....")

# Catch CTRL C
signal.signal(signal.SIGINT, signal_handler)

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.nodelay(1)

# Create the player
logger.debug("Creating player")

player = Player(outputDevice)

# Get the music folder object
musicFolder = MusicFolder(player)

# Get a list of all folders in the /pi/home/Music folder and set player to the first
playList = musicFolder.getPlayList(0)

if shuffle:
    
    playList.shuffle()

indexMediaFolder = 0

player.switchMedia(playList)

player.togglePlayPause()

# Set up camera object
camera = Camera(player, logger)

# Subcribe to state received event so that when the Arduino updates us with state we update controls
camera.events.onQRDataReceived += qrDataReceived

camera.start()

player.playFile(MediaFile(os.path.join(os.getcwd(), 'assets', 'audio', 'player-ready.ogg')))

quit = False

while quit == False:

    # Work out position and duration and loop to start if at end
    pos = player.position()
    dur = player.duration()

    if pos > (dur - 1): 
        player.playNext()

    # Process any key presses
    key = stdscr.getch()

    if key != -1:
        
        logger.debug("Keypress - Key value = " + str(key))

    # Esc or Q
    if key == 27 or key == 113:

        logger.debug("Keypress - Quit")

        quit = True

    # S
    elif key == 115:

        logger.debug("Keypress - Shuffle playlist")

        requestShuffle = True

    # B or P
    elif key == 98 or key == 112:

        logger.debug("Keypress - Play previous")

        requestPlayPrevious = True

    # N or Space
    elif key == 110 or key == 32:

        logger.debug("Keypress - Play next")

        requestPlayNext = True

    # F
    elif key == 102:

        logger.debug("Keypress - Switch mediaFolder")

        requestSwitchMediaFolder = True

    # Minus
    elif key == 45:

        logger.debug("Keypress - Volume down")

        requestVolumeDown = True

    # Equals
    elif key == 61:

        logger.debug("Keypress - Volume up")

        requestVolumeUp = True

    # Process requests from key presses or QR Event
    if requestSwitchMediaFolder:

        logger.info("Switching playlist to " + musicFolder.getPlayListRoot(indexMediaFolder))

        # Get all media files for the choosen folder
        playList = musicFolder.getPlayList(indexMediaFolder)

        if shuffle:

            playList.shuffle()

        player.switchMedia(playList)

        requestSwitchMediaFolder = False

    if requestShuffle:

        logger.info("Shuffling playlist")

        # Get all media files for the choosen folder
        playList = musicFolder.getPlayList(indexMediaFolder)

        playList.shuffle()

        player.switchMedia(playList)

        requestShuffle = False

    if requestPlayPrevious:

        logger.info("Switching mediaFile to previous")

        player.playPrevious()

        requestPlayPrevious = False

    if requestPlayNext:

        logger.info("Switching mediaFile to next")

        player.playNext()

        requestPlayNext = False

    if requestVolumeUp:

        logger.debug("Increasing volume")

        player.volume(0.1)

        requestVolumeUp = False

    if requestVolumeDown:

        logger.debug("Decreasing volume")

        player.volume(-0.1)

        requestVolumeDown = False

    if requestPlayOrPause:

        logger.debug("Play/Pause")

        player.togglePlayPause()

        requestPlayOrPause = False

    sleep(0.1)

cleanUp()
