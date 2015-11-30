import os
from PIL import Image
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='Hiding a text in an image.')
parser.add_argument('text', metavar='Text', type=str,
                   help='text to be hid in the image')
parser.add_argument('image', metavar='Image', type=str,
                   help='image in .bmp format')
args = parser.parse_args()
im = Image.open(args.image)
plaintext = open(args.text, "rb").read()

def converWholeTextToBits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def replaceLowestBit(colorChannel, textBits):
    imageLength = len(colorChannel) * len(colorChannel[0])
    length = min(imageLength, len(textBits))
    newColorChannel = np.zeros_like(colorChannel)
    i = 0
    rowCount = 0
    for row in colorChannel:
        valueCount = 0
        for colorValue in row:
            #print str(rowCount) + "  " + str(valueCount)
            if i > length - 1:
                newColorChannel[rowCount][valueCount] = colorValue
            else:
                binaryColor = list('{0:08b}'.format(colorValue))
                binaryColor[7] = str(textBits[i])
                i += 1
                finalColor = int(int(''.join(binaryColor), 2))
                newColorChannel[rowCount][valueCount] = finalColor
                #print "First Color  "+ str(colorValue)
                #print "Final Color  "+ str(finalColor)
            valueCount += 1
        rowCount += 1
    print i
    return newColorChannel

def main():
    print "\nConverting Textfile into simple bits..."
    textBits = converWholeTextToBits(plaintext);
    print "Converting done. Result: " + str(textBits) + "\n"

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
    finalImage.save("tempBild.bmp")
    imageFile = "C:/Users/Robin/Uni/Master/SichereVerteilteSysteme/A2/tempBild.bmp"
    os.rename(imageFile, "C:/Users/Robin/Uni/Master/SichereVerteilteSysteme/A2/bild.bmp.ste")
    print "Image saved.\n"
main()