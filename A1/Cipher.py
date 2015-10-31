import os
import re
import operator

__author__ = 'Rakatak'

lowerLetters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
letters = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z']
letterStats = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
cipherStats = {'E': 0, 'T': 0, 'A': 0, 'O': 0, 'I': 0, 'N': 0, 'S': 0, 'H': 0, 'R': 0, 'D': 0, 'L': 0, 'C': 0, 'U': 0, 'M': 0, 'W': 0, 'F': 0, 'G': 0, 'Y': 0, 'P': 0, 'B': 0, 'V': 0, 'K': 0, 'J': 0, 'X': 0, 'Q': 0, 'Z': 0}
twoLetterDictionary = {'he': 'he', 'of': 'of', 'it': 'it', 'is': 'is', 'th': 'th', 'no': 'no', 'es': 'es', 'if': 'if', 'go': 'go', 'do': 'do', 'is':'is'}
threeLetterDictionary = {'the': 'the', 'for': 'for', 'can': 'can', 'she': 'she', 'get': 'get', 'has': 'has', 'had': 'had', 'was': 'was', 'not': 'not','did': 'did', 'her': 'her','him': 'him', 'you':'you'}
fourLetterDictionary = {'will': 'will', 'does': 'does', 'have': 'have', 'take': 'take', 'wont': 'wont', 'make': 'make', 'some': 'some', 'talk': 'talk'}
sortedCipherStats = {}
currentDirectory = os.getcwd();
ciphertext = open(currentDirectory+"\\ciphertext.txt", 'r');
secondciphertext = open(currentDirectory+"\\ciphertext.txt", 'r');
cleartext = open(currentDirectory+"\\cleartext.txt", 'w');


def removeSpecialLetters(line):
    line = re.sub('[!@:123456\[\]7890#8$*()\'.;,\"!?\-]', '', line)
    return line;

def countStats(line):
    globalCounter =0
    for letter in letters:
        counter = line.lower().count(letter.lower())
        globalCounter = globalCounter + counter
        cipherStats[letter] += counter;
    return globalCounter;

def calcStats(globalCounter):
    print('Calculating Letterstats ...\n')
    for letter in cipherStats:
        #print("Letter: " + letter + " Count: " + str(cipherStats[letter]))
        temp = cipherStats[letter]
        cipherStats[letter] = temp/globalCounter;
        #print("Letter: " + letter+ " Stat: "+ str(cipherStats[letter]))

def firstLetterReplace(line, sortedDic):
    for c in line:
        if (c!='\n' and c!= ' ' and c!="'" and c!="," and c!= '.' and c!='-'):
            ind = lowerLetters.index(c.lower())
            print(sortedDic[ind])
            c.replace(c, sortedDic[ind])
#else for putting \n and so on back into cleartext TODO

def sortUp(dicti):
    return sorted(dicti, key=dicti.get, reverse=True)

def readout(dicti):
    for w in dicti:
        print(w + " " +str(dicti[w]))

def main():
    globalCounter=0
    print('Counting Letter ...\n')
    for line in ciphertext:
        globalCounter = countStats(line)
    calcStats(globalCounter);
    temp = sortUp(cipherStats)

    print('Replacing Letters on first Instance')
    for line in secondciphertext:

        firstLetterReplace(removeSpecialLetters(line), temp)
        print(line)

main()



