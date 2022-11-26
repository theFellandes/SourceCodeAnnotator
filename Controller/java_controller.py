from dataclasses import dataclass, field

import javalang
from javalang.tree import CompilationUnit

from Utils.pretty_object import pretty_object
from Utils.reader import Reader
from Utils.time_util import get_time
from Utils.writer import Writer
from conf import settings


@dataclass
class JavaController:
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
        self.reader = Reader(self.source_code_path)
        self.writer = Writer(settings.REPORT_PATH)
        self.source_code_string = self.reader.read_in_string()

    @pretty_object
    @get_time
    def generate_java_ast(self) -> CompilationUnit:
        """Prints java_ast to the console"""
        # Clear the escape characters for Java.
        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return tree
