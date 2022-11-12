import ast
import dataclasses
import re

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
    single_line_comments_list: list = field(init=False, default_factory=list)
    multi_line_comments_list: list = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
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

    def generate_ast(self) -> None:
        """Executes the behavior selected by the file extension"""
        operation = {"java": self.__generate_java_ast, "py": self.__generate_python_ast}
        operation.get(self.source_code_extension)()

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

    def capture_multi_line_comments(self) -> None:
        """
        Finds multi-line comments

        Dark Compiler magic java:
        \/\* +\*(\s+([a-zA-Z]+\s+)+)\*\/
        /* <ANYTHING> */

        Darker Compiler magic python:
        Apparently Python doesn't require this regex to find multi-line comments
        Since Python AST covers multi-line comments
        \"\"\"[^"]*\"\"\"
        \'\'\'[^']*\'\'\'
        """
        # TODO: Discussion, This function can be static
        self.multi_line_comments_list = re.findall('(/\*(.)*\*/)|//.*', self.source_code_string)


    def capture_single_line_comments(self) -> None:
        """
        Finds single-line comments

        Java:
        \/\/[a-zA-Z]+ [a-zA-Z]+

        Python:
        \#[a-zA-Z]+ [a-zA-Z]+
        """
        # TODO: Discussion, This function can be static
        if self.source_code_extension == 'java':
            self.single_line_comments_list = re.findall('^(//)[a-zA-Z]+ [a-zA-Z]+', self.source_code_string)

        else:
            self.single_line_comments_list = re.findall('(^#)[a-zA-Z]+ [a-zA-Z]+', self.source_code_string)

    @get_time
    @pretty_object
    def __generate_java_ast(self) -> CompilationUnit:
        """Prints java_ast to the console"""
        # Clear the escape characters for Java.
        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return tree

    @get_time
    @python_ast_prettier
    def __generate_python_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast.body[5]
