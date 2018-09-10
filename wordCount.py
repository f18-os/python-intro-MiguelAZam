import sys
import re
import os
import subprocess
import collections

if len(sys.argv) is not 3:
    print("Correct usage: wordCount.py <input txt file> <output file>")
    exit()

def checkFile(fileName):
    if not os.path.exists(fileName):
        print(fileName + " doesn't exist! Existing")
        exit()

def makeDict(inputFile):
    words = {}
    with open(inputFile, "r") as inputOpen:
        for line in inputOpen:
            line = line.strip().lower()
            line = re.sub('[^A-Za-z ]+', '', line)
            line = line.split(" ")
            for word in line:
                if not words.has_key(word):
                    words[word] = 1
                else:
                    words[word] = words[word] + 1
    return collections.OrderedDict(sorted(words.items()))

def createFile(outputFile, wordsDict):
    with open(outputFile, "w") as writeFile:
        for k,v in wordsDict.items():
            writeFile.write(k + " " + str(v) + "\n")
    return
        

inputFile = sys.argv[1]
outputFile = sys.argv[2]

checkFile("wordCount.py")
checkFile(inputFile)

wordsOrd = makeDict(inputFile)
del wordsOrd['']

createFile(outputFile, wordsOrd)
