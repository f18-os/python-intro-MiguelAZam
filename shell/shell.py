#!/usr/bin/env python3

import sys
import os
import re
import subprocess
import collections
import tokenize

os.environ["PS1"] = "$"

def runCmd(cmd):
    rc = os.fork()

    if rc<0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
    elif rc==0:
        try:
            os.execve(cmd[0], cmd, os.environ)
        except FileNotFoundError:
            pass
        for dir in re.split(':', os.environ["PATH"]):
            prgm = "/%s/%s" % (dir, cmd[0])
            try:
                os.execve(prgm, cmd, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("Command not found").encode())
    else:
        os.wait()
    return

def main():
    while(True):
        try:
            cmd = input()
            cmd = re.sub(' +', ' ', cmd)
            cmd = cmd.split(' ')
            if(cmd[0] == 'exit'):
                exit()
            if(len(cmd)<2 and cmd[0] != ''):
                runCmd(cmd)
        except EOFError:
            exit()


main()
