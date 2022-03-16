import os
import sys


def copy(input_url: str, download_folder_path: str):
    print("copying")
    os.system(r'"C:\Program Files\WinHTTrack\httrack.exe" '
              + input_url + r' -v --depth=1 --ext-depth=0 -O ' + download_folder_path)


if __name__ == "__main__":
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
    copy(url, download_folder)
