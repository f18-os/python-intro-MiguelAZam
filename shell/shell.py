#!/usr/bin/env python3

import sys
import os
import re

os.environ["PS1"] = "$"

def execCmd(prgm, cmd, env):
    try:
        os.execve(prgm, cmd, env)
    except FileNotFoundError:
        pass
    return

def runCmd(cmd):
    execCmd(cmd[0], cmd, os.environ)
    for dir in re.split(":", os.environ['PATH']):
        prgm = "%s/%s" % (dir, cmd[0])
        execCmd(prgm, cmd, os.environ)
    os.write(2, ("Child error: Could not exec %s \n" % cmd[0]).encode())
    sys.exit()

def checkForFork(cmd):
    char = ''
    if('>' in cmd):
        cmd = cmd.split('>')
        char = '>'
    elif('|' in cmd):
        cmd = cmd.split('|')
        char = '|'
    elif('&' in cmd):
        cmd = cmd.split('&')
        char = '&'
    else:
        cmd = [cmd]
    return cmd, char

def preprocess(command):
    command = re.sub(' +', ' ', command)
    command = command.split(' ')
    empty = []
    for i in range(len(command)):
        command[i] = command[i].strip(' ')
        if command[i] == '':
            empty.append(i)
    for i in range(len(empty)):
        del command[empty[i]]
    return command

def check(cmd):
    if(cmd[0]=='exit'):
        sys.exit()
    elif(cmd[0]=='cd'):
        try:
            os.chdir(cmd[1])
        except IndexError:
            os.write(2, ("Directory doesn't exist.\n").encode())
        return False
    return True

def startPipe(pcmd, scmd):
    r, w = os.pipe()
    scnd = False

    for cmd in (pcmd, scmd):
        pid = os.fork()

        if(pid<0):
            os.write(1, ("Fork failed. \n").encode())
            sys.exit()
        elif(pid==0):
            if(scnd):
               os.close(w)
               os.dup2(r,0)
            else:
                os.close(r)
                os.dup2(w, 1)
            runCmd(cmd)
        else:
            os.dup2(1,w)
            os.wait()
        scnd = True
    
def startFork(pcmd, scmd, char):
    if(char == '|'):
        startPipe(pcmd, scmd)
        return
    pid = os.fork()

    if(pid<0):
        os.write(1, ("Fork failed. \n").encode())
        sys.exit(1)
    elif(pid==0):
        if(char=='>'):
            os.close(1)
            sys.stdout = open(scmd[0], 'w')
            os.set_inheritable(1, True)
        runCmd(pcmd)
    else:
        if(char != '&'):
            os.wait()
            

#Main method that consist of taking the input of the user and tokenize the string
def main():
    while(True):
        try:
            os.write(1, (os.environ['PS1']).encode())
            cmd = input() #Wait for input
            cmd, char = checkForFork(cmd)
            pcmd = preprocess(cmd[0])
            scmd = ''
            if(len(cmd)==2):
                scmd = preprocess(cmd[1])
            if(check(pcmd)):
                startFork(pcmd, scmd, char)
        #Catch EOFError
        except EOFError:
            sys.exit()
    return

main()
