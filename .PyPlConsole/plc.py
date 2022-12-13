import importlib
from os import listdir, getcwd, chdir, path
import sys

sys.path.insert(0, '')

DEV = False
data_folder = f"{path.expanduser('~')}/.PyPlConsole/.PyPlConsole_data/" # /plugins but one dir higher to load plugins
if DEV:
    data_folder = ".PyPlConsole/.PyPlConsole_data/"

startDir = getcwd()
pluginsFunctions = {}

def load_plugins():
    dir_before_reload = getcwd()
    chdir(data_folder)

    with open("disable_plugins.txt") as disable_plugins_conf:
        disabled_plugins = set(disable_plugins_conf.read().splitlines()) # list with disabled plugins specified by the user in disabled_plugins.txt
        # slash (/) can be used as comment in disable_plugins.txt because file names can't start with a slash

    plugins_folder = getcwd()
    pluginsInFolder = listdir("plugins")
    # go through all folders in plugin folder
    for plugin in pluginsInFolder:
        if plugin in disabled_plugins:
            continue

        try:
            pl = importlib.import_module("plugins."+plugin)
            importlib.reload(pl)
            moduleDir = f"{plugins_folder}/plugins/{plugin}"
            pl = pl.main(moduleDir, startDir, plugins_folder+"\\plugins")
        except Exception as e:
            print("Couldn't load "+ plugin)
            print(e)

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

def stop_plugins():
    if "_bye" in pluginsFunctions:
        for bye in pluginsFunctions["_bye"]:
            try:
                bye._bye()
            except Exception as e:
                print(e)

while True:
    try:
        cmd = input("$> ")
    except KeyboardInterrupt:
        stop_plugins()
        exit()

    if "onenter" in pluginsFunctions:
            for onEnter in pluginsFunctions["onenter"]:
                try:
                    onEnter.onenter(cmd)
                except Exception as e:
                    print(e)

    # if no command was given, dont do following stuff, because onenter was run already and theres no command to run oncmd
    if cmd == "":
        continue


    cmd_no_args = cmd.split()[0]

    if cmd_no_args in set({"rl","reload"}):
        stop_plugins()
        pluginsFunctions = {}
        load_plugins()

    # runnning the oncmd functions of the plugins
    if "oncmd" in pluginsFunctions:
        for onCmd in pluginsFunctions["oncmd"]:
            try:
                onCmd.oncmd(cmd)
            except Exception as e:
                print(e)

    if cmd_no_args == "exit":
        stop_plugins()
        exit()

    # running the command inside the plugins functions (if the command is in the pluginsFunctions dict)
    if cmd_no_args in pluginsFunctions:
        for func in pluginsFunctions[cmd_no_args]:
            try:
                getattr(func, cmd_no_args)(cmd)
            except Exception as e:
                print(e)
    else:
        if not cmd_no_args in set({"rl","reload"}):
            print("x Command not found! x")

    
