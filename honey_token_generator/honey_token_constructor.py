from bs4 import BeautifulSoup, Tag
from content_concealing.concealing_for_injection import ConcealingForInjection
from content_downloader.website_copier_wrapper import copy
import glob


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


def inject_detection_code(inject_code_path: str, result_path: str, html_file_name: str) -> None:
    code_to_inject = get_code_to_inject(inject_code_path)
    searched_file = glob.glob(result_path + "/**/*" + html_file_name + "*", recursive=True)[0]
    script_content = ConcealingForInjection.conceal_content_to_execute(code_to_inject)
    detection_script = create_detection_script(script_content)
    insert_detection_script(searched_file, detection_script)


def create_token(web_token_location: str, inject_code_path: str, result_path: str) -> None:
    copy(web_token_location, result_path)
    html_file_name = web_token_location[web_token_location.rfind('/'):]
    inject_detection_code(inject_code_path, result_path, html_file_name)


if __name__ == "__main__":
    create_token("https://www.bestoldgames.net/battle-chess",
                 "../examples/simple/detectionCode.txt",
                 "../examples/simple/generatedResult")
