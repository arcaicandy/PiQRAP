#!/usr/bin/env python3
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

import qrcode

class QRCard:

    def __init__(self, qrCode, artWork, title):

        self.qrCode = qrCode
        self.artWork = artWork
        self.title = title

    def generate(self):

        # Create the Card image - Actual size is 78mm x 45mm - 300dpi = 921 x 532
        cardWidth = 921 * 2
        cardHeight = 532
        borderSize = 2
        marginSize = 10

        self.imgCard = Image.new('RGB', (cardWidth, cardHeight))

        # Draw bounding rectangle
        draw = ImageDraw.Draw(self.imgCard)
        draw.rectangle((0, 0, cardWidth - 1, cardHeight - 1), fill='white', outline='grey', width=2)

        # Draw vertical center line
        draw.line((int(cardWidth / 2) - 1, 0, int(cardWidth / 2) - 1, cardHeight), fill='grey', width=2)

        # Create QR code image
        qr = qrcode.QRCode(version=1, box_size=16, border=5)

        qr.add_data(self.qrCode)

        qr.make(fit=True)

        imgQR = qr.make_image(fill='black', back_color='white')

        qrWidth, qrHeight = imgQR.size

        # Get a font
        font = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf', 30)

        # Add some useful meta to the qr card in readable (qrcard value, date)
        imgCardMeta = Image.new("RGB", (400, 100), (255, 255, 255))

        metaWidth, metaHeight = imgCardMeta.size

        writing = ImageDraw.Draw(imgCardMeta)

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        textWidth, textHeight, metaWrapped = self.textWrap([self.qrCode, date], font, writing, metaWidth, metaHeight)

        writing.text((int((metaWidth - textWidth) / 2) ,2), metaWrapped, font=font, align='center', fill=(0,0,0,255))

        imgCardMeta = imgCardMeta.transpose(Image.ROTATE_90) 

        metaWidth, metaHeight = imgCardMeta.size

        # Paste the text image on to the card image
        self.imgCard.paste(imgCardMeta, ((int(cardWidth / 2) - metaWidth - borderSize), int((cardHeight - metaHeight) / 2)))

        # Paste the QR code image onto the card image
        self.imgCard.paste(imgQR, (3, int((cardHeight - qrHeight) / 2)))

        # Load the artwork image, rotate and resize
        imgArtwork = Image.open(self.artWork).convert('RGB')

        imgArtwork = imgArtwork.transpose(Image.ROTATE_270) 

        imageHeight = cardHeight - (2 * (borderSize + marginSize))
        imageWidth = imageHeight

        imgArtwork = imgArtwork.resize((imageWidth, imageHeight))

        # Paste the artwork image on to the card image
        self.imgCard.paste(imgArtwork, (cardWidth - (imageWidth + borderSize + marginSize), borderSize + marginSize))

        # Get a font
        font = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf', 75)

        # Draw the metadata - Artist, Album
        imgMeta = Image.new("RGB", (cardHeight - ((borderSize + marginSize + 10) * 2), int(cardWidth / 2) - (imageWidth + ((borderSize + marginSize) * 2))), (255, 255, 255))

        metaWidth, metaHeight = imgMeta.size

        writing = ImageDraw.Draw(imgMeta)

        textWidth, textHeight, metaWrapped = self.textWrap(self.title, font, writing, metaWidth, metaHeight)

        writing.text((int((metaWidth - textWidth) / 2) ,2), metaWrapped, font=font, align='center', fill=(0,0,0,255))

        imgMeta = imgMeta.transpose(Image.ROTATE_270) 
        metaWidth, metaHeight = imgMeta.size

        # Paste the text image on to the card image
        self.imgCard.paste(imgMeta, (cardWidth - (imageWidth + borderSize + marginSize + metaWidth), int((cardHeight - metaHeight) / 2)))

    def save(self, fileName):

        self.imgCard.save(fileName)

    def textWrap(self, paras, font, draw, max_width, max_height):

        if not isinstance(paras, list):
            paras = [paras]

        lines = [[]]

        for text in paras:

            words = text.split()

            for word in words:

                # try putting this word in last line then measure
                lines[-1].append(word)
                (w,h) = draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)

                if w > max_width: # too wide

                    # take it back out, put it on the next line, then measure again
                    lines.append([lines[-1].pop()])
                    (w,h) = draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)

                    if h > max_height: # too high now, cannot fit this word in, so take out - add ellipses

                        lines.pop()

                        # try adding ellipses to last word fitting (i.e. without a space)
                        lines[-1][-1] += '...'

                        # keep checking that this doesn't make the textbox too wide, 
                        # if so, cycle through previous words until the ellipses can fit
                        while draw.multiline_textsize('\n'.join([' '.join(line) for line in lines]),font=font)[0] > max_width:
                            lines[-1].pop()
                            lines[-1][-1] += '...'
                        break

            if len(paras) > 1:
                lines[-1].append('\n')

        return [w, h, '\n' . join([' ' . join(line) for line in lines])]
