import re
from dataclasses import dataclass, field

from Controller.base_controller import BaseController
from Controller.report_controller import ReportController
from Models.SourceCode.java_ast import JavaAST


@dataclass
class JavaController(BaseController):
    def __post_init__(self):
        super().__post_init__()
        self.java_ast = JavaAST(self.source_code_string)

    def get_single_line_comments(self) -> list:
        """ Returns single line comments """
        single_line_comments_list = re.findall(
            "(?://[^\n]*|/\*(?:(?!\*/).)*\*/)", self.java_ast.source_code_string
        )
        return single_line_comments_list

    def get_multi_line_comments(self) -> list:
        """ Returns multi line comments """
        multi_line_comments_list = (
            re.findall(
                "(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)",
                self.java_ast.source_code_string,
            )
        )
        return multi_line_comments_list

    def get_doc_comments(self) -> list:
        """ Returns doc comments """
        doc_comments_list = (
            re.findall(
                "(/\*\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)",
                self.java_ast.source_code_string,
            )
        )
        return doc_comments_list

    def generate_report(self):
        report_controller = ReportController(self.writer, self)
        report_controller.generate_report()

    def generate_comment(self):
        pass
