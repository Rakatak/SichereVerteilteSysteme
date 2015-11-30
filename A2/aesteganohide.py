import hashlib
from PIL import Image
import numpy as np
from xtea import *
import hmac
import os
import argparse
__author__ = 'Rakatak'

parser = argparse.ArgumentParser(description='Hiding a text in an image.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', action='store_true') # decrypt
group.add_argument('-e', action='store_true') # encrypt

parser.add_argument('-m', nargs='?', metavar='macpassword', type=str)
parser.add_argument('-k', nargs='?', metavar='keypassword', type=str)

parser.add_argument('image', metavar='Image', type=str, help='image in .bmp format')
parser.add_argument('text', metavar='Text', nargs='?', type=str, help='text to be hid')

#parser.add_argument('text',  help='text to be hid in the image',  action='store_true')
args = parser.parse_args()

macpassword = args.m
plainpassword = args.k

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
    #print i
    return newColorChannel


def createMAC(macpassword, text):
    print "Creating Mac..."
    return hmac.new(macpassword, text, hashlib.sha256).digest()

def hashPassword(password):
    print "Hashing Password..."
    hashPW =  hashlib.sha256(password).digest()
    print "Hashing done. Result: " + str(hashPW) + " Length: " + str(len(hashPW))
    return hashPW


def readoutBitsFromChannel(colorChannel):
    bitStream = ''
    for row in colorChannel:
        for colorValue in row:
            binaryColor = list(str('{0:08b}'.format(colorValue)))
            essentialBit = binaryColor[7]
            bitStream += str(essentialBit)
    return bitStream

def convertfromBits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def authMac(mac, decryptedText):
    textMac = decryptedText[:32]
    textWithoutMac = decryptedText[32:]
    a = hmac.new(mac, textWithoutMac, hashlib.sha256).digest()
    print "Mac from Text: " + textMac
    print "Mac from User: " + a
    return hmac.compare_digest(a, textMac)

def main():

    if args.e:
        plaintext = open(args.text, "rb").read()
        im = Image.open(args.image)

        mac = createMAC(macpassword, plaintext)
        print "Mac created: " + str(mac) + " Length: " + str(len(mac))

        print "Adding Mac to Plaintext... \n"
        macAndPlaintext = str(mac) + plaintext
        hashedPassword = hashPassword(plainpassword)
        hashedPassword = hashedPassword[:len(hashedPassword)/2]

        print "Start encrypting mac and plaintext..."
        print str(len(macAndPlaintext))
        x = new(hashedPassword, mode=MODE_CFB, IV="12345678")
        encryptedMacAndPlaintext = x.encrypt(macAndPlaintext)
        print "Encrypting done. Result:\n" + encryptedMacAndPlaintext + "\n"

        textBits = converWholeTextToBits(encryptedMacAndPlaintext)

        print "Getting Image Data..."
        r, g, b = np.array(im).T
        print "Image Dimensions are " + str(len(r)) + "x" + str(len(r[0])) + ".\n"

        print "Replacing Bits..."
        r = replaceLowestBit(r, textBits)
        g = replaceLowestBit(g, textBits)
        b = replaceLowestBit(b, textBits)
        print "Bits replaced.\n"

        print "Processing and saving Image..."
        finalImage = Image.fromarray(np.dstack([item.T for item in (r,g,b)]))
        finalImage.save("encBild.bmp")
        imageFile = "C:/Users/Robin/Uni/Master/SichereVerteilteSysteme/A2/encBild.bmp"
        os.rename(imageFile, "C:/Users/Robin/Uni/Master/SichereVerteilteSysteme/A2/bild.bmp.sae")
        print "Image saved.\n"



    if args.d:
        print "Getting encrypted Image."
        im_ = Image.open(args.image)
        r_, g_, b_ = np.array(im_).T
        print "Encrypted Image Dimensions are " + str(len(r_)) + "x" + str(len(r_[0])) + ".\n"

        print "Reading out Bitstream from image"
        bitStream = readoutBitsFromChannel(g_)[:16384]
        bitList = list(bitStream)
        bitList = map(int, bitList)

        print "Converting Bits from Image"
        cryptText = convertfromBits(bitList)

        hashedPassword = hashPassword(plainpassword)
        hashedPassword = hashedPassword[:len(hashedPassword)/2]

        x = new(hashedPassword, mode=MODE_CFB, IV="12345678")
        print "Decrypting Text from Bitstream"
        decryptedText = x.decrypt(cryptText)

        print "Tecryption done! Result: \n"
        print decryptedText + "\n"
        print "Authentificating decrypted Message..."
        if authMac(macpassword, decryptedText):
            print "Authentificating was successful"
        else:
            print "Authentificating failed! Do not believe content of message!"

main()
