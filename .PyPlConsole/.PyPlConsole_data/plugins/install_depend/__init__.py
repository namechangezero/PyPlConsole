from os import path, system
class main:
    def __init__(self, pluginDir,startDir):
        self.startDir = startDir
        self.pluginDir = pluginDir
    def install_depend(self,cmd:str):
        split_cmd = cmd.split()
        if len(split_cmd)<2:
            print("Please provide an package name as argument!")
            return
        
        pkg = split_cmd[-1]

        dependencies_file = f"{self.pluginDir}/../{pkg}/dependencies.txt"
        if not path.exists(dependencies_file):
            print("This plugin doesnt have a dependencies file :/")
            return
        
        with open(dependencies_file,"r") as f:
            dependencies = f.read().splitlines()
        dependencies = " ".join(dependencies)

        system("pip3 install "+dependencies)
