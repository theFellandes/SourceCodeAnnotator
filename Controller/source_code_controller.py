import ast
import dataclasses

import javalang
from dataclasses import dataclass, field
from javalang.tree import CompilationUnit

from conf import settings
from Utils.pretty_object import pretty_object, python_ast_prettier
from Utils.time_util import get_time
from Utils.reader import Reader


@dataclass
class SourceCodeParserController:
    source_code_file_name: str
    source_code_string: str = field(init=False, default="")

    def __post_init__(self):
        """
        Initializes the Source Code Parser rest of the attributes

        Initializes:
        source_code_path: string path of the source code
        reader: the Reader object for the source_code_path
        source_code_string: source code contents saved to string
        """
        self.source_code_path = settings.get_path(self.source_code_file_name)
        self.source_code_extension = settings.get_file_extension(
            self.source_code_file_name
        )
        self.reader = Reader(self.source_code_path)
        self.source_code_string = self.reader.read_in_string()

    def as_dict(self) -> dict:
        """Returns dict of the class"""
        return dataclasses.asdict(self)

    def generate_ast(self):
        """Executes the behavior selected by the file extension"""
        operation = {"java": self.__generate_java_ast, "py": self.__generate_python_ast}
        operation.get(self.source_code_extension)()

    def remove_escape_characters(self):
        """
        Removes first 32 characters of the ASCII table from source code string

        escapes: The first 32 characters of ASCII table
        translator: A translation table for the escape characters
        """
        escapes = "".join([chr(char) for char in range(1, 32)])
        translator = str.maketrans("", "", escapes)
        self.source_code_string = self.source_code_string.translate(translator)

    @get_time
    @pretty_object
    def __generate_java_ast(self):
        """Prints java_ast to the console"""
        # Clear the escape characters for Java.
        self.remove_escape_characters()

        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return tree.types[0].body[1]

    @get_time
    @python_ast_prettier
    def __generate_python_ast(self):
        """Prints python_ast to the console"""
        python_ast = ast.parse(self.source_code_string)
        return python_ast.body[5]
