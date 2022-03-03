import os
import sys
url = None
download_folder = "./download"

for index in range(1, len(sys.argv), 2):
    name = sys.argv[index]
    print(name)
    if name == "--url":
        url = sys.argv[index + 1]
    elif name == "--folder":
        download_folder = sys.argv[index + 1]
    else:
        raise Exception("Unknown argument: " + name)
if not url:
    raise Exception("Url not defined!")

# os.system('"C:\Program Files\WinHTTrack\httrack.exe"
# "https://www.bestoldgames.net/battle-chess" -v --depth=1 --ext-depth=0')
os.system(r'"C:\Program Files\WinHTTrack\httrack.exe" ' + url + r' -v --depth=1 --ext-depth=0 -O ' + download_folder)
