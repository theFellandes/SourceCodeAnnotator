import re


class CharacterManipulation:

    @staticmethod
    def remove_escape_characters(raw_string: str) -> str:
        """
        Removes first 32 characters of the ASCII table from source code string

        raw_string: Input string that has escape characters

        escapes: The first 32 characters of ASCII table
        translator: A translation table for the escape characters
        """
        escapes = "".join([chr(char) for char in range(1, 32)])
        translator = str.maketrans("", "", escapes)
        return raw_string.translate(translator)

    @staticmethod
    def apply_backspace(s):
        while True:
            # if you find a character followed by a backspace, remove both
            t = re.sub('.\b', '', s, count=1)
            if len(s) == len(t):
                # now remove any backspaces from beginning of string
                return re.sub('\b+', '', t)
            s = t

    @staticmethod
    def line_break_comment(comment):
        current_index = 9
        line_start_index = 8
        last_space_index = 0
        while current_index < len(comment):
            if comment[current_index] == " ":
                last_space_index = current_index
            if (current_index - line_start_index) % 80 == 0:
                comment = comment[:last_space_index] + "\n\t* " + comment[last_space_index + 1:]
                current_index = last_space_index + 4
                line_start_index = current_index - 1
            current_index += 1
            if comment[current_index:current_index + 5] == "\n\t* @":
                break
        return comment
