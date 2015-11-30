import argparse
__author__ = 'Rakatak'

parser = argparse.ArgumentParser(description='Hiding a text in an image.')

parser.add_argument('-d', action='store_true') # decrypt
parser.add_argument('-e', action='store_true') # encrypt
args = parser.parse_args()

if args.d:
    print "ahahaha"


def main():
    print args
    print "hahaha"
main()