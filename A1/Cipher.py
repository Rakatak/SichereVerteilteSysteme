import os
import re
__author__ = 'Rakatak'


letterStats = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
twoLetterDictionary = {'he': 'he', 'of': 'of', 'it': 'it', 'is': 'is', 'th': 'th', 'no': 'no', 'es': 'es', 'if': 'if', 'go': 'go', 'do': 'do', 'is':'is'}
threeLetterDictionary = {'the': 'the', 'for': 'for', 'can': 'can', 'she': 'she', 'get': 'get', 'has': 'has', 'had': 'had', 'was': 'was', 'not': 'not','did': 'did', 'her': 'her','him': 'him', 'you':'you'}
fourLetterDictionary = {'will': 'will', 'does': 'does', 'have': 'have', 'take': 'take', 'wont': 'wont', 'make': 'make', 'some': 'some', 'talk': 'talk'}

currentDirectory = os.getcwd();
ciphertext = open(currentDirectory+"\\ciphertext.txt", 'r');

def removeSpecialLetters(line):
    line = re.sub('[!@#$\'.,\"!?]', '', line)
    return line;

for line in ciphertext:
    line=removeSpecialLetters(line);
    print(line)
