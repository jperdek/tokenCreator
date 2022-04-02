
def apply_customization_to_html_name(html_name: str, customization: dict):
    if "file_name" not in customization:
        return html_name
    if "upper" == customization["file_name"]:
        return html_name.upper()
    elif "lower" == customization["file_name"]:
        return html_name.lower()
    elif "capitalize" == customization["file_name"]:
        return html_name.capitalize()
    elif "casefold" == customization["file_name"]:
        return html_name.casefold()
    elif "" == customization["file_name"]:
        return html_name.swapcase()
    else:
        print("Unknown name customization: " + customization["file_name"])
    return html_name
