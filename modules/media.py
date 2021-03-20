# PiQRAP Copyright (C) 2021 Andy Jones - teardrop@zen.co.uk
#!/usr/bin/env python3
import os.path
import random
import logging

from os import scandir

logger = logging.getLogger('__name__')

class MediaFile:  

    def __init__(self, path):  

        if not os.path.exists(path):
            raise SystemExit("File not found: " + path)

        self.path = path  

class PlayList:

    def __init__(self, path):

        logger.info("Creating playlist  :" + path)

        self.playList = []

        for entry in self.scanTree(path):
            self.playList.append(entry)

        for mediaFile in self.playList:
            logger.debug(mediaFile.path)

    # Recursively yield DirEntry objects for given directory.
    def scanTree(self, path, type='mp3'):

        logger.debug("Scanning path for media :" + path)

        for entry in scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from self.scanTree(entry.path, type) 
            elif entry.path.endswith("." + type):
                yield MediaFile(entry.path)

    def asList(self):

        return self.playList

    def shuffle(self):

        logger.debug("Shuffling playlist")

        random.shuffle(self.playList)

        for mediaFile in self.playList:
            logger.debug(mediaFile.path)
