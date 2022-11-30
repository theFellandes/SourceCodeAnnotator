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

    def get_single_line_comments(self) -> list:
        """ Returns single line comments """
        single_line_comments_list = re.findall(
            "(?:#[^\n]*|/\*(?:(?!\*/).)*\*/)", self.python_ast.source_code_string
        )
        return single_line_comments_list

    def get_multi_line_comments(self) -> list:
        """ Returns multi line comments """
        multi_line_comments_list = (
            re.findall(
                '([^:]"""[^(]*)"""',
                self.python_ast.source_code_string,
            )
        )
        return multi_line_comments_list

    def get_doc_comments(self) -> list:
        """
        Returns multi line comments

        This is because python doesn't have doc comments.
        """
        return self.get_multi_line_comments()

    def generate_report(self):
        report_controller = ReportController(self.writer, self)
        report_controller.generate_report()

    def generate_comment(self, python_ast: PythonAST):
        pass
