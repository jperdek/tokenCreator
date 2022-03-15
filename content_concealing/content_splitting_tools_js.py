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
                JavascriptContentSplitter.recursive_random_content_splitter(
                    content_part1, new_split_part_left, actual_depth + 1, max_depth, min_part_length)
                JavascriptContentSplitter.recursive_random_content_splitter(
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
                JavascriptContentSplitter.recursive_random_content_splitter_array(
                    content_part1, split_parts_array, actual_depth + 1, max_depth, min_part_length)
                JavascriptContentSplitter.recursive_random_content_splitter_array(
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


class JavascriptContentSplitter(ContentSplitter):

    def randomly_split_content(self, file_content: str):
        pass


if __name__ == "__main__":
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