from content_concealing.content_splitting_tools_js import JavascriptContentConcealing


class ConcealingForInjection:

    @staticmethod
    def prepare_to_execute(commands: list, variable_to_print: str) -> str:
        return " ".join(commands) + """ eval(""" + variable_to_print + """);"""

    @staticmethod
    def conceal_content_to_execute(content: str) -> str:
        #concealed_text, conceal_methods = ContentConcealing.random_conceal_text(content)
        concealed_text = content.replace("\n", "")
        commands, last_variable = JavascriptContentConcealing.randomly_split_content(concealed_text)
        return ConcealingForInjection.prepare_to_execute(commands, last_variable)
