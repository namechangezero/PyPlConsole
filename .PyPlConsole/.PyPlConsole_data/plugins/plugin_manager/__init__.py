from requests import get
from json import loads
from io import BytesIO
from zipfile import ZipFile
from os import getcwd, chdir
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
            archive = loads(get("https://raw.githubusercontent.com/namechangezero/PyPlConsole-extra-plugins/main/archive.json").content)
            if not cmd_split[2] in archive:
                print("Plugin doesn't exist in archive!")
                return
            plugin_zipfile_link = archive[cmd_split[2]]
            r = get(plugin_zipfile_link, stream=True)
            z = ZipFile(BytesIO(r.content))
            dir_before_chdir = getcwd()
            chdir(self.pluginsDir)
            z.extractall()
            chdir(dir_before_chdir)
            print("successfully installed plugin")
        elif cmd_split[1] == "help":
            print('"plugin add plugin_name" to install a plugin')
        else:
            print("Invalid Argument. Use 'plugin help' for help")