from requests import get
from json import loads
from io import BytesIO
from zipfile import ZipFile
from os import getcwd, chdir, system, path
from shutil import rmtree

class main:
    def __init__(self, moduleDir:str, startDir,pluginsDir) -> None:
        self.pluginsDir = pluginsDir
    def plugin(self,cmd:str):
        cmd_split = cmd.split()
        if len(cmd_split) < 2:
            print("You need to give at least 1 Argument. Try 'plugin help'")
            return
        
        if cmd_split[1] == "add":
            if len(cmd_split) < 3:
                print("You need to give 2 Arguments: add plugin_name")
                return
            print("Loading archive...")
            archive = loads(get("https://raw.githubusercontent.com/namechangezero/PyPlConsole-extra-plugins/main/archive.json").content)
            if not cmd_split[2] in archive:
                print("Plugin doesn't exist in archive!")
                return
            
            print("Downloading plugin...")
            plugin_zipfile_link = archive[cmd_split[2]]
            r = get(plugin_zipfile_link, stream=True)
            z = ZipFile(BytesIO(r.content))
            extraced_dir_name = z.namelist()[0]
            dir_before_chdir = getcwd()
            chdir(self.pluginsDir)
            z.extractall()

            if path.exists(extraced_dir_name+"\\dependencies.txt"):
                print("installing requirements for "+extraced_dir_name)
                chdir(extraced_dir_name)
                system("pip3 install -r dependencies.txt")

            chdir(dir_before_chdir)
            print("Successfully installed plugin, please type 'reload' to reload plugins")
        
        elif cmd_split[1] == "remove":
            if len(cmd_split) < 3:
                print("You need to give 2 Arguments: remove plugin_name")
                return
            print("Removing plugin...")
            dir_before_chdir = getcwd()
            chdir(self.pluginsDir)
            rmtree(cmd_split[2])
            chdir(dir_before_chdir)
            print("Successfully removed plugin, please type 'reload' to reload plugins")
        
        elif cmd_split[1] == "help":
            print('"plugin add plugin_name" to install a plugin')
        else:
            print("Invalid Argument. Use 'plugin help' for help")
