from os import system, getcwd, listdir, path, chdir, remove as removeFile
from os import path, rename as renameFile
from platform import system as operating_system
from colorama import Fore, init

import importlib.util
import sys

class main:
    def __init__(self, moduleDir, startDir) -> None:
        self.os = operating_system()
        init()


    def oncmd(self,command):
        #what happens on every command (not if only enter is pressed)
        pass

    def onenter(self, command):
        #what happens when pressing enter (doesn't matter if command is empty or not)
        pass

    def clear(self, command):
        if self.os in {"Linux","Darwin"}:
            system("clear")
        elif self.os == "Windows":
            system("cls")

    def pwd(self, command):
        print(getcwd())

    def ls(self, cmd):
        items = listdir()
        for item in items:
            if path.isfile(item):
                print(Fore.BLUE, end="")
                print(item)
                print(Fore.RESET, end="")
            else:
                print(Fore.GREEN, end="")
                print(item)
                print(Fore.RESET, end="")

    def cd(self,cmd:str):
        dir = cmd.split()
        if len(dir)<2:
            print("You need to give a filename as argument!")
            return
        dir = dir[-1]
        if not path.exists(dir):
            print("Path doesn't exist!")
            return
        if path.isfile(dir):
            print("Path is a file!")
        chdir(dir)

    def touch(self, cmd:str):
        filename = cmd.split()
        if len(filename)<2:
            print("You need to give a filename as argument!")
            return
        filename = filename[-1]
        open(filename,"a").close()

    def read(self, cmd:str):
        filename = cmd.split()
        if len(filename)<2:
            print("You need to give a filename as argument!")
            return
        filename = filename[-1]
        if not path.exists(filename):
            print("File doesn't exist!")
            return
        f = open(filename,"r")
        content = f.read()
        f.close()
        print(content)

    cat = read

    def rm(self,cmd):
        filename = cmd.split()
        if len(filename)<2:
            print("You need to give a filename as argument!")
            return
        filename=filename[-1]
        if path.exists(filename):
            removeFile(filename)
        else:
            print("File doesn't exist!")
        

    remove = rm

    def mv(self, cmd):
        splitCmd = cmd.split()
        if len(splitCmd)<3:
            print("You need to give two filenames as argument!")
            return
        fromFile, toFile = splitCmd[1:]
        if path.exists(fromFile):
            renameFile(fromFile,toFile)
        else:
            print("File doesn't exist!")

    rename = mv

    def s(self,command:str):
        split_cmd = command.split()

        if len(split_cmd)<2:
            print("You need to give at least one argument!")
            return

        commands = " ".join(split_cmd[1:])
        system(command=commands)

