from dataclasses import dataclass, field

from Controller.base_controller import BaseController


@dataclass
class AnnotatorController:

    base_controller: BaseController = field(default_factory=BaseController)

    def generate_comment(self, ast):
        self.base_controller.generate_comment(ast)

    def get_single_line_comments(self):
        return self.base_controller.get_single_line_comments()

    def get_multi_line_comments(self):
        return self.base_controller.get_multi_line_comments()

    def get_doc_comments(self):
        return self.base_controller.get_doc_comments()

    def generate_report(self):
        self.base_controller.generate_report()

    def generate_comment(self):
        self.base_controller.generate_comment()
