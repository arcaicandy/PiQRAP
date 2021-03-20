# PiQRAP Copyright (C) 2021 Andy Jones - teardrop@zen.co.uk
#!/usr/bin/env python3
import os
import os.path
import yaml
import logging

from os import scandir

from modules.mediaPlayerSingle import Player
from modules.media import MediaFile, PlayList
from modules.qrCard import QRCard

from modules.config import Configuration 

config = Configuration()
logger = logging.getLogger('__name__')

class MusicFolder:

    def __init__(self, player):

        self.musicFolder = None
        self.player = player

        player.playFile(MediaFile(os.path.join(os.getcwd(), 'assets', 'audio', 'starting-scan.ogg')))

        logger.info("Looking for music folder")

        # Search the /media/pi folder for 'music' folders
        for folder in [f.path for f in os.scandir('/media/pi') if f.is_dir()]:

            if os.path.isdir(os.path.join(folder, 'music')):
                self.musicFolder = os.path.join(folder, 'music')
                break

        if self.musicFolder is not None:

            logger.info("Music folder found : " + self.musicFolder)

            # If there is a YML in the root then merge it into config
            config.mergeConfig(os.path.join(self.musicFolder, "piqrap.yml"))

            self.findFolders()

            self.indexFolders()

            self.makeQRCards(config.rebuildqrcards or False)
        else:

            logger.warning("No music folder found")

    def hasMusicFolder(self):

        return self.musicFolder is not None

    def findFolders(self):

        logger.info("Scanning music folders")

        # Get a list of all playlist folders in the music folder
        self.playlistFolders = [f.path for f in os.scandir(self.musicFolder) if f.is_dir()]

        logger.debug(str(len(self.playlistFolders)) + " music folders found")

    def getPlayListRoot(self, index):

        return self.indexMap[index]

    def getPlayList(self, index):

        return PlayList(self.indexMap[index])

    def indexFolders(self):

        logger.info("Indexing music folders")

        self.indexMap = {}
        newFolders = []

        highestIndex = -1

        # Iterate round the folders, look in the root of each one for a piqrap.yml file
        for folder in self.playlistFolders:

            # If there is a YML file then get the index that has been assigned to the folder
            if os.path.exists(folder + "/piqrap.yml"):

                with open(folder + "/piqrap.yml") as file:

                    ymlData = yaml.full_load(file)

                    self.indexMap[ymlData['index']] = folder

                    folderIndex = int(ymlData['index'])

                    if folderIndex > highestIndex:
                        highestIndex = int(ymlData['index'])

                logger.debug("Known music folder found (" + str(folderIndex) + "): " + folder)

            # No YML file so add the folder to the list of those that need initialising
            else:

                logger.debug("New music folder found : " + folder)

                newFolders.append(folder)

        # Find the highest value index from the initialised folders
        newIndex = highestIndex + 1

        # For each new folder found
        for folder in newFolders:

            # Create yaml file and save the folders index value 
            with open(folder +"/piqrap.yml", 'w') as file:

                documents = yaml.dump({'index': newIndex}, file)

            # Add the new folder to the index mapping
            self.indexMap[newIndex] = folder

            logger.debug("New music folder assigned index (" + str(newIndex) + "): " + folder)

            # Do the next one
            newIndex = newIndex + 1

    def makeQRCards(self, rebuild=False):

        logger.info("Making QR Cards. Rebuild = " + str(rebuild))

        # Make the folder for the QRCards if it doesn't exist
        qrCardPath = os.path.join(self.musicFolder, '..', 'qrcards')

        if not os.path.exists(qrCardPath):
            os.mkdir(qrCardPath)

        # Iterate round the folders and create a QRCard for each
        for index, folder in self.indexMap.items():

            indexString = str(index).zfill(4)

            fileName = os.path.join(qrCardPath, 'qrcard-' + indexString + '.png')

            if (not os.path.exists(fileName)) or rebuild:

                logger.debug("Building QRCard for " + folder)

                # Find the artwork for the folder
                artWorkPath = os.path.join(folder, "folder.jpg")

                if not os.path.exists(artWorkPath):
                    artWorkPath = os.path.join(os.getcwd(), 'assets', 'image-not-found.png')

                # Create the QRCard for the folder
                qrCard = QRCard(indexString, artWorkPath, os.path.basename(folder))

                qrCard.generate()
                qrCard.save(fileName)

            else:

                logger.debug("QRCard exists for = " + folder)

        # Now do the control cards (Play/pause - Next)
        controlCards = {
            'shuffle': ['SHUF', 'Shuffle playlist'],
            'previous': ['PREV', 'Previous track'],
            'next': ['NEXT', 'Next track'],
            'play-pause': ['PORP', 'Play / Pause']
        }

        for key, attribs in controlCards.items():

            fileName = os.path.join(qrCardPath, 'qrcard-' + key.lower() + '.png')

            if (not os.path.exists(qrCardPath)) or rebuild:

                artWorkPath = os.path.join(os.getcwd(), 'assets', key.lower() + '.png')

                # Create the QRCard for the control card
                qrCard = QRCard(attribs[0], artWorkPath, attribs[1])

                qrCard.generate()
                qrCard.save(fileName)
