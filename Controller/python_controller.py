from dataclasses import dataclass

from Controller.base_controller import BaseController
from Models.SourceCode.python_ast import PythonAST


@dataclass
class PythonController(BaseController):

    def generate_comment(self, python_ast: PythonAST):
        pass
