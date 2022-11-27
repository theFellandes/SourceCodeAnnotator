from dataclasses import dataclass

from Controller.base_controller import BaseController
from Models.SourceCode.java_ast import JavaAST


@dataclass
class JavaController(BaseController):

    def generate_comment(self, java_ast: JavaAST):
        pass
