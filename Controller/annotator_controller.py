from dataclasses import dataclass, field

from Controller.base_controller import BaseController


@dataclass
class AnnotatorController:

    base_controller: BaseController = field(default_factory=BaseController)

    def get_return_value(self):
        return self.base_controller.get_return_value()

    def write_ast_to_file(self):
        self.base_controller.write_ast_to_file()

    def get_ast(self):
        return self.base_controller.get_ast()

    def write_ast(self):
        return self.base_controller.write_ast()

    def generate_comment_from_function_name(self):
        return self.base_controller.generate_comment_from_function_name()


    def comment_source_code(self):
        return self.base_controller.comment_source_code()

    def comment_functions(self, ast_body):
        return self.base_controller.comment_functions(ast_body)