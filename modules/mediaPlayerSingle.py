# PiQRAP Copyright (C) 2021 Andy Jones - teardrop@zen.co.uk
#!/usr/bin/env python3
import os
import os.path
import logging

from omxplayer.player import OMXPlayer
from time import sleep

from modules.media import MediaFile, PlayList

logger = logging.getLogger('__name__')

class Player:

    def __init__(self, outputDevice = 'alsa:dmixer'):

        logger.info("Creating player. Output device : " + outputDevice)

        self.outputDevice = outputDevice

        self.player = None
        self.playList = None
        self.currentMediaFile = 0

    def initPlayer(self, mediaFile):

        logger.info("Creating main omxplayer with file : " + mediaFile.path)

        dbusName = 'org.mpris.MediaPlayer2.omxplayer1'

        player = OMXPlayer(mediaFile.path, dbus_name=dbusName, args=['--no-osd', '-o', self.outputDevice])

        player.pause()

        self.paused = True

        return player

    def play(self):

        logger.debug("Playing player")

        # Show active player
        self.player.play()

        self.paused = False

    def playFile(self, mediaFile):

        logger.debug("Playing auxillary file : " + mediaFile.path)

        if os.path.exists(mediaFile.path):

            dbusName = 'org.mpris.MediaPlayer2.omxplayer2'

            player = OMXPlayer(mediaFile.path, dbus_name=dbusName, args=['--no-osd', '--no-keys', '-o', self.outputDevice])

    def switchMedia(self, playList):

        logger.debug("Switching playlist")

        if not self.player is None:
            self.player.quit()

        self.playList = playList.asList()

        logger.debug("Playlist has " + str(len(self.playList)) + " files")

        self.currentMediaFile = 0

        # Create the player
        self.player = self.initPlayer(self.playList[0])

        # Start playing
        self.player.play()

        self.paused = False

    def playPrevious(self):

        logger.debug("Playing previous track : ")

        if self.player.position() < 2:

            self.currentMediaFile = self.getPreviousMediaFileIndex()

            # Quit the player 
            self.player.quit()

            # Create a new player using the next media file
            self.player = self.initPlayer(self.playList[self.currentMediaFile])

            # Show player
            self.player.play()

            self.paused = False

        else:

            self.player.set_position(0)

    def playNext(self):

        logger.debug("Playing next track : ")

        self.currentMediaFile = self.getNextMediaFileIndex()

        # Quit the player 
        self.player.quit()

        # Create a new player using the next media file
        self.player = self.initPlayer(self.playList[self.currentMediaFile])

        # Show player
        self.player.play()

        self.paused = False

    def togglePlayPause(self):

        if self.paused:
            logger.debug("Playing player")
            self.player.play()
        else:
            logger.debug("Pausing player")
            self.player.pause()

        self.paused = not self.paused

    def getPreviousMediaFileIndex(self):

        return len(self.playList) - 1 if self.currentMediaFile == 0 else self.currentMediaFile - 1

    def getNextMediaFileIndex(self):

        return 0 if self.currentMediaFile == len(self.playList) - 1 else self.currentMediaFile + 1

    def position(self):

        return self.player.position()

    def duration(self):

        return self.player.duration()

    def restart(self):

        self.player.set_position(self.playList[self.currentMediaFile].start)

    def action(self, key):

        self.player.action(key)

    def volume(self, volChange):

        newVol = self.player.volume() + volChange

        if newVol < 0:
            newVol = 0
        elif newVol > 10:
            newVol = 10

        return self.player.set_volume(newVol)

    def quit(self):

        self.player.quit()
