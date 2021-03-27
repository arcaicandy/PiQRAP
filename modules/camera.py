# PiQRAP Copyright (C) 2021 Andy Jones - teardrop@zen.co.uk
#!/usr/bin/env python3
import os
import os.path

import time
import threading

import cv2
import pyzbar.pyzbar as pyzbar

from pyzbar.pyzbar import ZBarSymbol

from modules.events import Events
from modules.mediaPlayerSingle import Player
from modules.media import MediaFile, PlayList

class Camera(threading.Thread):

    def __init__(self, player, logger=None):

        self.player = player

        if logger:

            self.logger = logger

            self.logger.debug("Starting")

        super(Camera, self).__init__()

        self.events = Events()

        self.camera = cv2.VideoCapture(0)

        # Set camera fps
        self.camera.set(cv2.CAP_PROP_FPS, 15)

        # Set the height and width of the image capture (bigger is not always better)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        # Log what the height and width actually are
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.logger.debug("Width/Height : " + str(width) + "/" + str(height))

        self.lastQRData = None

        # Name the thread
        self.name = "Camera"

        return

    def run(self):

        self.logger.debug("Running camera loop")

        self.running = True

        while self.running:

            # Attempt to grab an image
            _, img = self.camera.read()

            # Decode any qr codes if we can
            objects = pyzbar.decode(img, symbols=[ZBarSymbol.QRCODE])

            qrData = None

            # Find the first QRCode
            for obj in objects:
                if obj.type == "QRCODE":
                    qrData = obj.data.decode("utf-8") 
                    exit

            # If we found a QR code
            if qrData:

                self.logger.debug("QRData found : " + qrData)

                if qrData != self.lastQRData:

                    self.lastQRData = qrData

                    self.player.playFile(MediaFile(os.path.join(os.getcwd(), 'assets', 'audio', 'beep.ogg')))

                    self.logger.info("Sending QR data : " + qrData)

                    # Raise event to let listeners know we have a new QRCode
                    self.events.onQRDataReceived(qrData)

                    # Set a timer so we reset the last QR code read after x seconds
                    timer = threading.Timer(2, self.clearQRCode)
                    timer.start()

                else:

                    self.logger.debug("QRData ignored (duplicate) : " + qrData)

    def clearQRCode(self):

        self.lastQRData = None

    def stop(self):

        self.logger.debug("Shutdown request")

        self.running = False

        time.sleep(.5)

        self.camera.release()
