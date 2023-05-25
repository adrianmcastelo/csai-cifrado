##Based on https://github.com/ichantzaras/creamcrackerz
# -*- coding: utf-8 -*-
import attack
import processing
import argparse
import unicodedata2 as ud

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", help="Input file", required=True)
    parser.add_argument("-hash", help="Input file with the hash", required=True)
    return parser.parse_args()

def main():
    args = parseArgs()
    ciphered=processing.getFileContent(args.i)
    hash=processing.getFileContent(args.hash)

    ciphered = ciphered.upper()
    key, text = attack.crackText(ciphered, hash)

    if hash == processing.getHashFromText(text):
        print(key)
