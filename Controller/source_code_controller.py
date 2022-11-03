import javalang
import ast
import astpretty
from dataclasses import dataclass
from javalang.tree import CompilationUnit
from Utils.time_util import get_time
from Utils.reader import Reader
from conf import settings


@dataclass
class SourceCodeParserController:
    source_code_file_name: str

    def __post_init__(self):
        """
        Initializes the Source Code Parser rest of the attributes

        Initializes:
        source_code_path: string path of the source code
        reader: the Reader object for the source_code_path
        source_code_string: source code contents saved to string
        """
        self.source_code_path = settings.get_path(self.source_code_file_name)
        self.source_code_extension = settings.get_file_extension(self.source_code_file_name)
        self.reader = Reader(self.source_code_path)
        self.source_code_string = self.reader.read_in_string()

    def generate_ast(self):
        """ Executes the behavior selected by the file extension """
        operation = {
            'java': self.__generate_java_ast,
            'py': self.__generate_python_ast
        }
        operation.get(self.source_code_extension)()

    @get_time
    def __generate_java_ast(self):
        """ Prints java_ast to the console """
        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        print(tree)

    @get_time
    def __generate_python_ast(self):
        """ Prints python_ast to the console """
        python_ast = ast.parse(self.source_code_string)
        astpretty.pprint(python_ast.body[5])
