import re
from dataclasses import dataclass

from Controller.base_controller import BaseController
from Controller.report_controller import ReportController
from Models.SourceCode.python_ast import PythonAST


@dataclass
class PythonController(BaseController):
    def __post_init__(self):
        super().__post_init__()
        self.python_ast = PythonAST(self.source_code_string)

    def get_ast(self):
        return self.python_ast.get_ast()

    def write_ast(self):
        return self.python_ast.write_ast()

    def generate_comment_from_function_name(self):
        list_of_function_names = self.python_ast.get_list_of_function_names()
        list_of_generated_comments = [self.name_analyzer.get_generated_comment(function_name)
                                      for function_name in list_of_function_names]
        return list_of_generated_comments
