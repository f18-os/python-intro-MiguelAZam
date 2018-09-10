import sys
import re
import os
import subprocess

if len(sys.argv) is not 3:
    print("Correct usage: wordCount.py <input txt file> <output file>")
    exit()

inputFile = sys.argv[1]
outputFile = sys.argv[2]

if not os.path.exists("wordCount.py"):
    print("wordCount.py doesn't exist! Exiting")
    exit()

if not os.path.exists(inputFile):
    print("file doesn't exist! Exiting")
    exit()

with open(inputFile, "r") as inputFileOpen:
    for line in inputFileOpen:
        line = line.strip().lower()
        line = re.sub('[^A-Za-z ]+', '', line)
        print(line)
