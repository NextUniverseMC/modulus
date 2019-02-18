from shutil import copy2, move, rmtree
import subprocess
import os

from os.path import isfile, join


subprocess.call("git add --all", shell=True)
subprocess.call("git commit -m \"Scheduled Backup\"", shell=True)
subprocess.call("git push origin master", shell=True)

newNumberFile = open('newnumber.txt')
newNumber = newNumberFile.read().replace("\n", "")
move('servers/' + newNumber + '/worlds', 'worlds/')
copy2('servers/' + newNumber + '/bukkit.yml', '.')
copy2('servers/' + newNumber + '/spigot.yml', '.')
copy2('servers/' + newNumber + '/server.properties', '.')
copy2('servers/' + newNumber + '/servernumber.txt', '.')

rmtree("plugins/PluginMetrics")
rmtree("plugins/Updater")

files = []
folders = []
for f in os.listdir('servers/' + newNumber + '/plugins/'):
    if isfile(join('servers/' + newNumber + '/plugins/', f)):
        files.append(f)
        print(f)
    else:
        folders.append(f)
        print(f)

for f in files:
    copy2(join('servers/' + newNumber + '/plugins/', f), 'plugins/')

for f in folders:
    move(join('servers/' + newNumber + '/plugins/', f), 'plugins/')

subprocess.call("java -Xms512m -Xmx2G -Dlog4j.configurationFile=log4j2.xml -Dcom.mojang.eula.agree=true -DIReallyKnowWhatIAmDoingISwear=true -jar spigot.jar", shell=True)

os.remove("banned-ips.json")
os.remove("banned-players.json")
os.remove("bukkit.yml")
os.remove("permissions.yml")
os.remove("server.properties")

serverNumberFile = open('servernumber.txt')
serverNumber = serverNumberFile.read().replace("\n", "")
for f in files:
    os.remove(join('plugins/', f))

for f in folders:
    move(join('plugins/', f), 'servers/' + newNumber + '/plugins')

move('worlds/', 'servers/' + serverNumber)

os.remove("servernumber.txt")