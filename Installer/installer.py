print("Loading...")

import requests, zipfile
from io import BytesIO
from os import path, system, chdir
import subprocess
from colorama import Fore, init as init_colorama
from webbrowser import open as open_browser

init_colorama()

def run_powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

print("Initializing..")
RELEASE_ZIPFILE = "https://github.com/namechangezero/PyPlConsole/releases/download/v1.0.0/PyPlConsole.zip"
HOMEDIR = path.expanduser('~')
DESTINATION = HOMEDIR+"/.PyPlConsole"


chdir(HOMEDIR)
print("Downloading...")
r = requests.get(RELEASE_ZIPFILE, stream=True)
z = zipfile.ZipFile(BytesIO(r.content))
print("Extracting....")
z.extractall()

print("Configuring Path.....")
system(f'setx path "%path%;{DESTINATION}"')

print("Configuring PowerShell......")
run_powershell("Set-ExecutionPolicy Bypass -Scope LocalMachine")

print("Installed successfully!\n")

print("Checking installed Python version.......")
result = subprocess.run(['python', '--version'], stdout=subprocess.PIPE).stdout.decode("utf-8")
result_splitted = result.split()
python_version = result_splitted[-1]
python_version = python_version.replace(".","")

if not python_version.startswith("3"):
    print(f"{Fore.RED}ATTENTION: Please install Python 3 or newer and install again!!{Fore.RESET}")
    open_browser("https://www.python.org/downloads/")
else:
    print("Installing needed pip modules")
    subprocess.run(["pip","install","colorama requests"])
