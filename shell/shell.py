#!/usr/bin/env python3

import sys
import os
import re
import subprocess

os.environ["PS1"] = "$"

def execCmd(prgm, cmd, env):
    try:
        os.execve(prgm, cmd, env)
    except FileNotFoundError:
        pass
    return

def runCmd(cmd):
    rc = os.fork()

    if rc<0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
    elif rc==0:
        execCmd(cmd[0], cmd, os.environ)
        for dir in re.split(':', os.environ["PATH"]):
            prgm = "/%s/%s" % (dir, cmd[0])
            execCmd(prgm, cmd, os.environ)
        os.write(2, ("Command not found\n").encode())
    else:
        os.wait()
    return

def checkIORed(cmd):
    if '>' in cmd:
        cmd = cmd.split('>')
        runRedir(cmd)
    elif '|' in cmd:
        cmd = cmd.split('|')
        runPipe(cmd)
    else:
        cmd = cmd.split(' ')
        runCmd(cmd)
    return

def startFork():
    r, w = os.pipe()
    pid = os.fork()
    if pid<0:
        os.write(2, ("Fork failed, returing %d\n" % pid).encode())
    return r, w, pid

def runRedir(cmd):
    r, w, pid = startFork()
    if pid==0:
        myOut = cmd[0].split(' ')
        os.close(1)
        sys.stdout = open(cmd[1], "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)
        execCmd(myOut[0], myOut, os.environ)
        for dir in re.split(":", os.environ['PATH']):
            prgm = "%s/%s" % (dir, myOut[0])
            execCmd(prgm, myOut, os.environ)
        os.write(2, ("Child error: Could not exec %s \n" % myOut[0]).encode())
        sys.exit()
    else:
        os.wait()
    return
        

#Main method that consist of taking the input of the user and tokenize the string
def main():
    while(True):
        try:
            cmd = input(os.environ['PS1'] + " ") #Wait for input
            cmd = re.sub(' +', ' ', cmd) #Delete extra spaces
            cmdSplit = cmd.split(' ')
            if(cmdSplit[0]=='exit'):
                exit()
            if(len(cmdSplit)<2 and cmdSplit[0]==''):
                continue
            checkIORed(cmd)
        #Catch EOFError
        except EOFError:
            exit()
    return


main()


