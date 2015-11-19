import os
from PIL import Image
import binascii
import numpy as np

im = Image.open("Bild.bmp")

file = open("text.txt", "rb")

def convertobits(file):
    bytes = (ord(b) for b in file.read())
    for b in bytes:
        for i in xrange(8):
            yield (b >> i) & 1

def replaceLowestBit(colorChannel, textBits):
    imageLength = len(colorChannel) * len(colorChannel[0])
    length = min(imageLength, len(textBits))
    newColorChannel = np.zeros_like(colorChannel)
    i = 0
    rowCount = 0
    for row in colorChannel:
        valueCount = 0
        for colorValue in row:
            if i == length:
                i = 0
            listColor = list(str('{0:08b}'.format(colorValue)))
            listColor[7] = textBits[i]
            i += 1
            finalColor = int(int(''.join(listColor), 2))
            newColorChannel[rowCount][valueCount] = finalColor
            #print "First Color  "+ str(colorValue)
            #print "Final Color  "+ str(finalColor)
            valueCount += 1
        rowCount += 1

    return newColorChannel





def main():
    textBits = ''
    print "\nConverting Textfile into simple bits..."
    for b in convertobits(file):
        textBits += str(b)
    print "Converting done. Result: " + textBits + "\n"

    print "Getting Image Data..."
    r, g, b = np.array(im).T
    print "Image Dimensions are " + str(len(r)) + "x" + str(len(r[0])) + ".\n"

    print "Replacing Bits..."
    r = replaceLowestBit(r, textBits)
    g = replaceLowestBit(g, textBits)
    b = replaceLowestBit(b, textBits)
    print "Bits replaced.\n"

    print "Processing and saving Image...\n"
    finalImage = Image.fromarray(np.dstack([item.T for item in (r,g,b)]))
    finalImage.save("bild.bmp")
    print "Image saved.\n"
main()