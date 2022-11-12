import ast
import dataclasses
import re

import javalang
from dataclasses import dataclass, field
from javalang.tree import CompilationUnit

from conf import settings
from Utils.ast_to_file import ast_to_file
from Utils.pretty_object import pretty_object, python_ast_prettier
from Utils.time_util import get_time
from Utils.reader import Reader
from Utils.writer import Writer


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
        self.writer = Writer(settings.REPORT_PATH)
        self.writer.append_buffer(f"{self.source_code_file_name} Report\n")
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
        """Finds multi-line comments"""
        # Python multiline
        self.multi_line_comments_list = re.findall(
            '([^:]"""[^(]*)"""', self.source_code_string
        )

        # Bütün comment'leri buluyor javada
        if self.source_code_extension == "java":
            # TODO: limit this regex
            self.multi_line_comments_list.extend(
                re.findall(
                    "(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)",
                    self.source_code_string,
                )
            )
            # TODO: javadoc finder regex
            number_of_java_docs = len(self.multi_line_comments_list)
            self.writer.append_buffer(f"* {number_of_java_docs} Javadoc Comments\n")
        number_of_multi_lines = len(self.multi_line_comments_list)
        self.writer.append_buffer(f"* {number_of_multi_lines} Multi Line Comments\n")

    def capture_single_line_comments(self) -> None:
        """Finds single-line comments"""
        self.single_line_comments_list = re.findall(
            "(?:#[^\n]*|/\*(?:(?!\*/).)*\*/)", self.source_code_string
        )

        if self.source_code_extension == "java":
            self.single_line_comments_list = re.findall(
                "(?://[^\n]*|/\*(?:(?!\*/).)*\*/)", self.source_code_string
            )
        self.writer.append_buffer(
            f"* {len(self.single_line_comments_list)} Single Line Comments\n"
        )

    @ast_to_file
    @pretty_object
    @get_time
    def __generate_java_ast(self) -> CompilationUnit:
        """Prints java_ast to the console"""
        # Clear the escape characters for Java.
        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return tree

    @ast_to_file
    @python_ast_prettier
    @get_time
    def __generate_python_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast

    def generate_report(self) -> None:
        """Generates the report.txt for source code"""
        self.writer.append_buffer("There are:\n\n")
        self.capture_single_line_comments()
        self.capture_multi_line_comments()

        number_of_single_lines = len(self.single_line_comments_list)
        number_of_multi_lines = len(self.multi_line_comments_list)
        total_lines_of_comment = number_of_single_lines + number_of_multi_lines
        self.writer.append_buffer(
            f"* {total_lines_of_comment} Total Lines of Comments\n"
        )
        _, total_lines = self.reader.read_in_lines()
        self.writer.append_buffer(f"* {total_lines} Total Lines of Code\n\n")
        self.compare_statistics_with_clean_code(
            number_of_single_lines,
            number_of_multi_lines,
            total_lines_of_comment,
            total_lines,
        )

    def compare_statistics_with_clean_code(
        self,
        number_of_single_lines: int,
        number_of_multi_lines: int,
        total_lines_of_comment: int,
        total_lines: int,
    ):
        """TODO: This class doesn't fit the SOLID Rules, fix it"""
        clean_code_statistics = settings.GOOD_CODE_STATISTICS.get(
            self.source_code_extension
        )
        comment_per_lines = round(total_lines_of_comment / total_lines * 100, 4)

        single_line_result = self.get_statistic_idiom(
            number_of_single_lines, clean_code_statistics.get("single_line"), 0
        )
        # TODO: Missing Suggestion
        self.writer.append_buffer(
            f"** Average Single Line Comment Usage is {single_line_result} project. **\n"
        )

        multi_line_result = self.get_statistic_idiom(
            number_of_multi_lines, clean_code_statistics.get("multi_line"), 0
        )
        # TODO: Missing Suggestion
        self.writer.append_buffer(
            f"** Average Multi Line Comment Usage is {multi_line_result} project. **\n"
        )

        total_lines_result = self.get_statistic_idiom(
            total_lines, clean_code_statistics.get("total_line"), 0
        )
        # TODO: Missing Suggestion
        self.writer.append_buffer(
            f"** Average Total Lines is {total_lines_result} project. **\n"
        )
        self.writer.append_buffer(f"* Comment Per Lines: {comment_per_lines} *")
        self.writer.buffered_writer()

    @staticmethod
    def get_statistic_idiom(compared_value: int, actual: int, error_margin: int) -> str:
        """
        Returns the statistic's advice idiom

        :param compared_value: the value of the source code
        :param actual: the value of the clean code
        :param error_margin: the error margin for the source code base
        :return: report content
        """
        if compared_value < actual:
            return "lower than"

        elif compared_value == actual:
            return "on par with"

        else:
            return "higher than"
