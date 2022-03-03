import sys
import re

path_string = "../../../"
file_content = ""
with open(sys.argv[1], "r", encoding="utf-8") as read_file:
    for line in read_file:
        line = re.sub(r'href\s*=\s*"/', 'href="' + path_string, line)
        line = re.sub(r"href\s*=\s*'/", "href='" + path_string, line)
        line = re.sub(r'src\s*=\s*"/', 'src="' + path_string, line)
        line = re.sub(r"src\s*=\s*'/", "src='" + path_string, line)
        file_content = file_content + line
with open(sys.argv[1], "w", encoding="utf-8") as write_file:
    write_file.write(file_content)