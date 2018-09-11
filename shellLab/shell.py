import sys
import os
import re
import subprocess
import collections

def isCommand(cmd):
    files = os.listdir('./bin')
    for file in files:
        file = file.split('.')
        if cmd == file[0]:
            return True
    return False

while(True):
    cmd = input(os.getcwd() + "# ")
    if cmd == "exit":
        break
    if(isCommand(cmd)):
        print("Hi")
