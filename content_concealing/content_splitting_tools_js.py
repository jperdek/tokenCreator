import random


class SplitPartsTree:
    def __init__(self):
        self.right = None
        self.left = None
        self.text = None

    def add_to_right(self, split_part) -> None:
        self.right = split_part

    def add_to_left(self, split_part) -> None:
        self.left = split_part

    def get_right(self) -> any:
        return self.right

    def get_left(self) -> any:
        return self.left

    def set_text(self, split_text: str) -> None:
        self.text = split_text

    def get_text(self) -> str:
        return self.text


class ContentSplitter:
    @staticmethod
    def recursive_random_content_splitter(file_content: str,
                                          split_parts_tree: SplitPartsTree,
                                          actual_depth: int = 0,
                                          max_depth: int = 5,
                                          min_part_length: int = 6):
        if actual_depth < max_depth:
            file_content_length = len(file_content)

            if len(file_content) > min_part_length * 2 + 1:
                divide_index = random.randrange(min_part_length, file_content_length - min_part_length)
                content_part1 = file_content[:divide_index]
                content_part2 = file_content[divide_index + 1:]
                new_split_part_left = SplitPartsTree()
                new_split_part_right = SplitPartsTree()
                split_parts_tree.add_to_left(new_split_part_left)
                split_parts_tree.add_to_right(new_split_part_right)
                ContentSplitter.recursive_random_content_splitter(
                    content_part1, new_split_part_left, actual_depth + 1, max_depth, min_part_length)
                ContentSplitter.recursive_random_content_splitter(
                    content_part2, new_split_part_right, actual_depth + 1, max_depth, min_part_length)
            else:
                split_parts_tree.set_text(file_content)
        else:
            split_parts_tree.set_text(file_content)

    @staticmethod
    def recursive_random_content_splitter_array(file_content: str,
                                                split_parts_array: list,
                                                actual_depth: int = 0,
                                                max_depth: int = 5,
                                                min_part_length: int = 6):
        if actual_depth < max_depth:
            file_content_length = len(file_content)

            if len(file_content) > min_part_length * 2 + 1:
                divide_index = random.randrange(min_part_length, file_content_length - min_part_length)
                content_part1 = file_content[:divide_index]
                content_part2 = file_content[divide_index:]
                ContentSplitter.recursive_random_content_splitter_array(
                    content_part1, split_parts_array, actual_depth + 1, max_depth, min_part_length)
                ContentSplitter.recursive_random_content_splitter_array(
                    content_part2, split_parts_array, actual_depth + 1, max_depth, min_part_length)
            else:
                split_parts_array.append(file_content)
        else:
            split_parts_array.append(file_content)

    @staticmethod
    def traverse_tree(split_parts_tree: SplitPartsTree):
        if split_parts_tree:
            left_part_tree = split_parts_tree.get_left()
            ContentSplitter.traverse_tree(left_part_tree)
            right_part_tree = split_parts_tree.get_right()
            ContentSplitter.traverse_tree(right_part_tree)

            content = split_parts_tree.get_text()
            if content:
                print(content)


class JavascriptContentConcealing(ContentSplitter):

    @staticmethod
    def add_declaration(text_part: str, variable_name: str, double_quotes: bool = False) -> (str, str):
        if "\"" not in text_part:
            return "let {variable_name} = \"{text_part}\";".format(
                variable_name=variable_name, text_part=text_part), variable_name
        elif "'" not in text_part:
            return "let {variable_name} = '{text_part}';".format(
                variable_name=variable_name, text_part=text_part), variable_name
        else:
            if double_quotes:
                return "let {variable_name} = \"{text_part}\";".format(
                    variable_name=variable_name, text_part=text_part.replace("\"", "\\\"")), variable_name
            else:
                return "let {variable_name} = '{text_part}';".format(
                    variable_name=variable_name, text_part=text_part.replace("'", "\\'")), variable_name

    @staticmethod
    def put_to_quotes(text_part: str, double_quotes: bool = False):
        if "\"" not in text_part:
            return "\"{text_part}\"".format(text_part=text_part)
        elif "'" not in text_part:
            return "'{text_part}'".format(text_part=text_part)
        else:
            if double_quotes:
                return "\"{text_part}\"".format(text_part=text_part.replace("\"", "\\\""))
            else:
                return "'{text_part}'".format(text_part=text_part.replace("'", "\\'"))

    @staticmethod
    def create_array_from_variables(text_parts: list,
                                    merge_variable_array_name: str,
                                    commands: list = None,
                                    quoted: bool = True,
                                    new_joined_variable_name: str = None):
        declaration = "let {merge_variable_array_name} = [{text_variables_array}];"
        text_variables_array = ""
        for text_part in text_parts:
            if quoted:
                text_variables_array = text_variables_array + "," + JavascriptContentConcealing.put_to_quotes(text_part)
            else:
                text_variables_array = text_variables_array + "," + text_part
        text_variables_array = text_variables_array[1:]
        command1 = declaration.format(
            merge_variable_array_name=merge_variable_array_name, text_variables_array=text_variables_array)
        if new_joined_variable_name:
            command2 = "{new_joined_variable_name} = {merge_variable_array_name}.join('');".format(
                new_joined_variable_name=new_joined_variable_name, merge_variable_array_name=merge_variable_array_name)
        else:
            command2 = "{merge_variable_array_name} = {merge_variable_array_name}.join('');".format(
                merge_variable_array_name=merge_variable_array_name)
        if commands is not None:
            commands.append(command1)
            commands.append(command2)
        else:
            raise Exception("Commands should be defined otherwise results are inconsistent!")
        return command1 + command2, commands

    @staticmethod
    def load_names(file_path: str):
        variable_names = list()
        with open(file_path, "r", encoding="utf-8") as file:
            for name in file:
                can_pass = True
                for javascript_word in ["abstract", "arguments", "await", "boolean", "break", "byte", "case", "catch",
                                        "char", "class", "const", "continue", "debugger", "default", "delete", "do",
                                        "double", "else", "enum", "eval",
                                        "export", "extends", "false", "final", "finally", "float", "for", "function",
                                        "goto", "if", "implements", "import",
                                        "in", "instanceof", "int", "interface", "let", "long", "native", "new", "null",
                                        "package", "private", "protected",
                                        "public", "return", "short", "static", "super", "switch", "synchronized",
                                        "this", "throw", "throws", "transient", "true",
                                        "try", "typeof", "var", "void", "volatile", "while", "with", "yield"]:
                    if javascript_word in name:
                        can_pass = False
                        break
                if not can_pass:
                    continue
                variable_names.append(name.replace("\n", ""))
        random.shuffle(variable_names)
        return variable_names

    @staticmethod
    def choose_and_perform_random_processing_method(text_parts: list,
                                                    commands: list,
                                                    variable_list: list,
                                                    variable_index: int):
        random_tool_index = random.randrange(0, 2)
        if random_tool_index == 0:
            temporary_variables = list()
            for index, text_part in enumerate(text_parts):
                command, variable_name = JavascriptContentConcealing.add_declaration(
                    text_part, variable_list[index + variable_index])
                commands.append(command)
                temporary_variables.append(variable_name)

            used_variables_index = len(text_parts) + variable_index
            merged_variable = variable_list[used_variables_index]
            merged, commands = JavascriptContentConcealing.create_array_from_variables(
                temporary_variables, merged_variable, commands=commands,
                quoted=False, new_joined_variable_name=None)
            return commands, used_variables_index + 1, merged_variable
        # creates array from text parts
        elif random_tool_index == 1:
            merged_variable = variable_list[variable_index]
            merged, commands = JavascriptContentConcealing.create_array_from_variables(
                text_parts, merged_variable, commands=commands, quoted=True)
            return commands, variable_index + 1, merged_variable
        else:
            print("Error unknown option! Command not processed!")

    @staticmethod
    def process_random_text(text_parts: list['str'],
                            variable_names: list,
                            name_position: int = 0,
                            trim_parts: int = 4) -> (list, int):
        if trim_parts > len(text_parts):
            raise Exception("Number splits is greater then trim parts!")

        variables_to_merge = list()
        commands = list()
        variable_index = 0
        array_potential_splits = random.sample(range(1, len(text_parts) - 1), trim_parts)
        array_potential_splits.sort()
        previous_index = 0

        array_potential_splits.append(len(text_parts))

        for index in array_potential_splits:
            commands, variable_index, merged_variable = \
                JavascriptContentConcealing.choose_and_perform_random_processing_method(
                    text_parts[previous_index:index], commands, variable_names, name_position)
            name_position = variable_index
            previous_index = index
            variables_to_merge.append(merged_variable)
        merged, commands = JavascriptContentConcealing.create_array_from_variables(
            variables_to_merge, variable_names[name_position], commands=commands, quoted=False)
        return commands, name_position + 1

    @staticmethod
    def randomly_split_content(file_content: str,
                               variable_names: list = None,
                               max_depth: int = 5,
                               min_part_length: int = 6,
                               trim_parts: int = 5,
                               variable_names_file: str = "words.txt") -> (list, str):
        if not variable_names:
            variable_names = JavascriptContentConcealing.load_names(variable_names_file)
        split_parts_array = list()
        JavascriptContentConcealing.recursive_random_content_splitter_array(
            file_content, split_parts_array, 0, max_depth, min_part_length)
        commands, variable_index = JavascriptContentConcealing.process_random_text(
            split_parts_array, variable_names, 0, trim_parts=trim_parts)
        return commands, variable_names[variable_index - 1]


def test1() -> None:
    split_part_tree_root: SplitPartsTree = SplitPartsTree()

    ContentSplitter.recursive_random_content_splitter("""President of South Korea Syngman Rhee is ousted by  1962 Cuban Missile Crisis
student protests. The Soviets secretly place medium-range missiles in 
Cuba. When the U.S. government finds out, it block-
1960 Sino-Soviet Split ades Cuba. The Soviets pull out the missiles, ending 
An  ideological  split  develops  between  Communist  the crisis.
China and the Soviet Union. Armed border conflict 
occurs between the two nations.""", split_part_tree_root, 0)
    ContentSplitter.traverse_tree(split_part_tree_root)

    print("-----------------------------------------")
    array = list()
    ContentSplitter.recursive_random_content_splitter_array("""President of South Korea Syngman Rhee is ousted by  1962 Cuban Missile Crisis
student protests. The Soviets secretly place medium-range missiles in 
Cuba. When the U.S. government finds out, it block-
1960 Sino-Soviet Split ades Cuba. The Soviets pull out the missiles, ending 
An  ideological  split  develops  between  Communist  the crisis.
China and the Soviet Union. Armed border conflict 
occurs between the two nations.""", array, 0)
    for part in array:
        print(part)


def test2() -> None:
    commands, last_variable = JavascriptContentConcealing.randomly_split_content("""President of South Korea Syngman Rhee is ousted by  1962 
    Cuban Missile Crisis student protests. The Soviets secretly place medium-range missiles in 
    Cuba. When the U.S. government finds out, it block-
    1960 Sino-Soviet Split ades Cuba. The Soviets pull out the missiles, ending 
    An  ideological  split  develops  between  Communist  the crisis.
    China and the Soviet Union. Armed border conflict 
    occurs between the two nations.""".replace("\n", ""))
    for command in commands:
        print(command)


if __name__ == "__main__":
    # test1()
    test2()
