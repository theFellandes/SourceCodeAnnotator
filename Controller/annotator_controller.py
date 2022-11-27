from dataclasses import dataclass, field

from Controller.base_controller import BaseController
from Controller.java_controller import JavaController
from Models.SourceCode.java_ast import JavaAST


@dataclass
class AnnotatorController:

    base_controller: BaseController = field(default_factory=BaseController)

    def generate_comment(self, ast):
        self.base_controller.generate_comment(ast)


if __name__ == '__main__':
    java_ast = JavaAST('Main.java')
    java_controller = JavaController()
    annotator_controller = AnnotatorController(java_controller)
    annotator_controller.generate_comment(java_ast)
