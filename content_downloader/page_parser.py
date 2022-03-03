
from pywebcopy import save_webpage
# for isntalation not use pip due to missing argument threaded: False
# - Otherwise problems are caused - unable to join threads
# still problems with absolute sources !
# "./venv/Scripts/python.exe" -m pip install -e git+https://github.com/rajatomar788/pywebcopy.git#egg=pywebcopy
import sys

url = None
download_folder = "./download"
project_name = "Scenario4"

for index in range(1, len(sys.argv), 2):
    name = sys.argv[index]
    print(name)
    if name == "--url":
        url = sys.argv[index + 1]
    elif name == "--folder":
        download_folder = sys.argv[index + 1]
    elif name == "--projName":
        project_name = sys.argv[index + 1]
    else:
        raise Exception("Unknown argument: " + name)
if not url:
    raise Exception("Url not defined!")


kwargs = {'bypass_robots': True, 'project_name': project_name, 'threaded': False,
          'open_in_browser': False, 'debug': True}
save_webpage(url, download_folder, **kwargs)