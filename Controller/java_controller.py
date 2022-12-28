import re
from dataclasses import dataclass

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

    def get_return_value(self):
        return self.java_ast.get_return_value()

    def generate_report(self):
        report_controller = ReportController(self.writer, self)
        report_controller.generate_report()

    def write_ast_to_file(self):
        self.java_ast.write_ast_to_file()

    def get_ast(self):
        return self.java_ast.generate_ast()

    def generate_comment_from_function_name(self):
        list_of_function_names = self.java_ast.get_list_of_function_names()
        list_of_generated_comments = [self.name_analyzer.get_generated_comments_list(function_name)
                                      for function_name in list_of_function_names]
        return list_of_generated_comments
