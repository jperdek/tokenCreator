from shutil import rmtree, copyfile

from bs4 import BeautifulSoup, Tag
from content_concealing.concealing_for_injection import ConcealingForInjection
from content_downloader.website_copier_wrapper import copy
import glob
import os
import re

from content_minifier.content_minifier import process_directory
from honey_token_generator.honey_token_customization import apply_customization_to_html_name
from token_derivation.nodejs.base_server import create_server


def create_detection_script(detection_script_content: str) -> Tag:
    soup = BeautifulSoup()
    new_script = soup.new_tag('script')
    new_script.string = detection_script_content
    return new_script


def insert_detection_script(searched_file: str, detection_script: Tag) -> None:
    with open(searched_file, "r", encoding="utf-8") as file:
        file_content = file.read()

    searched_page = BeautifulSoup(file_content, "html.parser")
    searched_page.select_one("body").append(detection_script)
    file_content = str(searched_page)
    with open(searched_file, "w", encoding="utf-8") as file:
        file.write(file_content)


def get_code_to_inject(inject_file):
    with open(inject_file) as index_file:
        return index_file.read()


def inject_detection_code(inject_code_path: str, result_path: str,
                          html_file_name: str, new_detection_address: str) -> None:
    code_to_inject = get_code_to_inject(inject_code_path)
    code_to_inject = code_to_inject.replace("http://localhost:5001/input", new_detection_address)
    searched_file = glob.glob(result_path + "/**/*" + html_file_name + "*", recursive=True)[0]
    script_content = ConcealingForInjection.conceal_content_to_execute(code_to_inject)
    detection_script = create_detection_script(script_content)
    insert_detection_script(searched_file, detection_script)


def create_token(web_token_location: str, inject_code_path: str, result_path: str, new_detection_address: str) -> None:
    copy(web_token_location, result_path)
    html_file_name = web_token_location[web_token_location.rfind('/'):]
    inject_detection_code(inject_code_path, result_path, html_file_name, new_detection_address)


def create_logger_honeypot_exmaple() -> None:
    listening_url = "http://localhost:5001/newone"
    listening_url_part = re.search(r"//[^/]+(/.*)$", listening_url).group(1)
    create_server(path_to_server_stub="../examples/simple/server_stub/",
                  path_to_server="../examples/simple/generatedServer",
                  controllers=[("logger", "business_domain", "business.domain",
                                "../examples/simple/serverLoggerCode.txt", listening_url_part)])
    create_token(web_token_location="https://www.bestoldgames.net/battle-chess",
                 inject_code_path="../examples/simple/detectionCode.txt",
                 result_path="../examples/simple/generatedToken",
                 new_detection_address=listening_url)


def copy_file_back(http_track_html_file: str, previous_token_path: str, customization: dict = None):
    with open(http_track_html_file, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file.read(), "html.parser")
    source_path = http_track_html_file[:http_track_html_file.rfind("/") + 1]
    for link in soup.select("a"):
        url = source_path + link["href"]
        html_name = url[url.rfind("/"):]
        if customization:
            html_name = apply_customization_to_html_name(html_name, customization)
        copyfile(url, previous_token_path + html_name)


def create_honeypots(honey_token_data: [],
                     path_to_server: str,
                     path_to_server_stub: str = "../examples/simple/server_stub/",
                     http_track_move: bool = True,
                     minify_tokens: bool = True) -> None:
    controllers_for_server = []
    for token_data in honey_token_data:
        web_token_location = token_data["web_token_location"]
        result_token_path = token_data["result_token_path"]
        inject_code_path = token_data["inject_code_path"]
        listening_url = token_data["listening_url"]
        customization = None
        if "customization" in token_data:
            customization = token_data["customization"]
        controller_for_server_temporary = token_data["controller"]

        listening_url_part = re.search(r"//[^/]+(/.*)$", listening_url).group(1)
        previous_token_path = "."
        if http_track_move:
            previous_token_path = result_token_path
            result_token_path = result_token_path + "/tmp"
            if not os.path.exists(result_token_path):
                os.makedirs(result_token_path)

        create_token(web_token_location=web_token_location,
                     inject_code_path=inject_code_path,
                     result_path=result_token_path,
                     new_detection_address=listening_url)
        if http_track_move:
            copy_file_back(result_token_path + "/index.html", previous_token_path, customization)
            rmtree(result_token_path)

        controllers_for_server.append((controller_for_server_temporary["controller_type"],
                                       controller_for_server_temporary["controller_name"],
                                       controller_for_server_temporary["controller_file_name"],
                                       controller_for_server_temporary["original_path"], listening_url_part))

    if not os.path.exists(path_to_server):
        os.makedirs(path_to_server)
    create_server(path_to_server_stub=path_to_server_stub,
                  path_to_server=path_to_server,
                  controllers=controllers_for_server)
    if minify_tokens:
        process_directory(previous_token_path)


if __name__ == "__main__":
    create_logger_honeypot_exmaple()
