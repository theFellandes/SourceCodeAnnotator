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
