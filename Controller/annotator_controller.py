from dataclasses import dataclass, field

from Controller.base_controller import BaseController


@dataclass
class AnnotatorController:

    base_controller: BaseController = field(default_factory=BaseController)

    def get_single_line_comments(self):
        return self.base_controller.get_single_line_comments()

    def get_multi_line_comments(self):
        return self.base_controller.get_multi_line_comments()

    def get_doc_comments(self):
        return self.base_controller.get_doc_comments()

    def get_return_value(self):
        return self.base_controller.get_return_value()

    def generate_report(self):
        self.base_controller.generate_report()

    def write_ast_to_file(self):
        self.base_controller.write_ast_to_file()

    def get_ast(self):
        return self.base_controller.get_ast()

    def generate_comment_from_function_name(self):
        return self.base_controller.generate_comment_from_function_name()
