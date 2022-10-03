import importlib
from os import listdir, getcwd, chdir

startDir = getcwd()
pluginsFunctions = {}
pluginsInFolder = listdir("plugins")

def load_plugins():
    # go through all folders in plugin folder
    for plugin in pluginsInFolder:
        if plugin == "__pycache__":
            continue

        pl = importlib.import_module("plugins." + plugin)
        importlib.reload(pl)
        pl = pl.main()

        # put all funcs of plugin in a list and append it to the dict of the plugin (pluginsFunctions)
        plFunctions = []
        for func in dir(pl):
            if func.startswith("__"): 
                continue

            plFunctions.append(func)

            if not func in pluginsFunctions:
                pluginsFunctions[func] = []
        
            pluginsFunctions[func].append(pl)

load_plugins()

while True:
    cmd = input("$> ")

    if "onenter" in pluginsFunctions:
            for onEnter in pluginsFunctions["onenter"]:
                onEnter.onenter(cmd)

    if cmd == "":
        continue


    cmd_no_args = cmd.split()[0]

    if cmd_no_args == "rl":
        chdir(startDir)
        pluginsFunctions = {}
        pluginsInFolder = listdir("plugins")
        load_plugins()

    # runnning the oncmd functions of the plugins
    if "oncmd" in pluginsFunctions:
        for onCmd in pluginsFunctions["oncmd"]:
            onCmd.oncmd(cmd)

    # running the command of the input from the plugins
    if cmd_no_args in pluginsFunctions:
        for func in pluginsFunctions[cmd_no_args]:
            getattr(func, cmd_no_args)(cmd)
    else:
        if cmd_no_args=="rl":
            pass
        else:
            print("x Command not found! x")

    
