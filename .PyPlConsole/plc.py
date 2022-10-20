import importlib
from os import listdir, getcwd, chdir, path
import sys

sys.path.insert(0, '')

plugin_folder_path = f"{path.expanduser('~')}/.PyPlConsole/.PyPlConsole_data/" # /plugins but one dir higher to load plugins
startDir = getcwd()
pluginsFunctions = {}

def load_plugins():
    dir_before_reload = getcwd()
    chdir(plugin_folder_path)

    with open("disable_plugins.txt") as disable_plugins_conf:
        disabled_plugins = set(disable_plugins_conf.read().splitlines()) # list with disabled plugins specified by the user in disabled_plugins.txt
        # slash (/) can be used as comment in disable_plugins.txt because file names can't start with a slash

    plugins_folder = getcwd()
    pluginsInFolder = listdir("plugins")
    # go through all folders in plugin folder
    for plugin in pluginsInFolder:
        if plugin in disabled_plugins:
            continue

        pl = importlib.import_module("plugins."+plugin)
        importlib.reload(pl)
        moduleDir = f"{plugins_folder}/plugins/{plugin}"
        pl = pl.main(moduleDir, startDir)

        # put all funcs of plugin in a list and append it to the dict of the plugin (pluginsFunctions)
        plFunctions = []
        for func in dir(pl):
            if func.startswith("__"): 
                continue

            plFunctions.append(func)

            if not func in pluginsFunctions:
                pluginsFunctions[func] = []
        
            pluginsFunctions[func].append(pl)
    
    chdir(dir_before_reload)

load_plugins()

while True:
    cmd = input("$> ")

    if "onenter" in pluginsFunctions:
            for onEnter in pluginsFunctions["onenter"]:
                onEnter.onenter(cmd)

    # if no command was given, dont do following stuff, because onenter was run already and theres no command to run oncmd
    if cmd == "":
        continue


    cmd_no_args = cmd.split()[0]

    if cmd_no_args in set({"rl","reload"}):
        if "_bye" in pluginsFunctions:
            for bye in pluginsFunctions["_bye"]:
                bye._bye()
        pluginsFunctions = {}
        load_plugins()

    # runnning the oncmd functions of the plugins
    if "oncmd" in pluginsFunctions:
        for onCmd in pluginsFunctions["oncmd"]:
            onCmd.oncmd(cmd)

    if cmd_no_args == "exit":
        if "_bye" in pluginsFunctions:
            for bye in pluginsFunctions["_bye"]:
                bye._bye()
        exit()

    # running the command of the input from the plugins
    if cmd_no_args in pluginsFunctions:
        for func in pluginsFunctions[cmd_no_args]:
            getattr(func, cmd_no_args)(cmd)
    else:
        if not cmd_no_args in set({"rl","reload"}):
            print("x Command not found! x")

    
