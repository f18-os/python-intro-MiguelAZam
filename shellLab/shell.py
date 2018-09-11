import sys
import os
import re
import subprocess
import collections

def isCommand(cmd):
    binPath = './shellBin'
    files = os.listdir(binPath)
    cmdPath = ''
    for file in files:
        fullName = file.split('-')[1]
        cmdName = fullName.split('.')[0]
        if cmd == cmdName:
            cmdPath = binPath + '/' + file
            return cmdPath, True
    return cmdPath, False

while(True):
    cmd = input(os.getcwd() + "# ")
    if cmd == "exit":
        break
    path, isCmd = isCommand(cmd)
    if(isCmd):
        subprocess.call(['python3', path])
    else:
        print("Command doesn't exist! Try again.")
