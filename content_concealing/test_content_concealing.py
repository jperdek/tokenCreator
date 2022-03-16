import js2py

from content_concealing import ContentConcealing
from content_splitting_tools_js import JavascriptContentConcealing


def get_execute_function_template(commands: list, variable_to_print: str) -> str:
    return """
        function my_to_execute() { """ + " ".join(commands) + """ return """ + variable_to_print + """; }
    """


def test1() -> None:
    concealed_text, conceal_methods = ContentConcealing.random_conceal_text(
        "My text is unconcealed and needs to be hidden! My text is unconcealed and needs to be hidden! "
        "My text is unconcealed and needs to be hidden! My text is unconcealed and needs to be hidden!")
    commands, last_variable = JavascriptContentConcealing.randomly_split_content(concealed_text)
    result_execute_function = js2py.eval_js(get_execute_function_template(commands, last_variable))
    concealed_text_executed_js = result_execute_function()

    unconcealed_text = ContentConcealing.unconceal_text(concealed_text_executed_js, applied_methods=conceal_methods)
    print("Text unconcealed:")
    print(unconcealed_text)


if __name__ == "__main__":
    test1()

