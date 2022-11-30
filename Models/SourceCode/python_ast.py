import ast
from dataclasses import dataclass

from Utils.ast_to_file import ast_to_file
from Utils.pretty_object import python_ast_prettier
from Utils.time_util import get_time
from Models.SourceCode.ast_base import ASTBase


@dataclass
class PythonAST(ASTBase):
    def generate_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast

    @ast_to_file
    @python_ast_prettier
    @get_time
    def write_ast_to_file(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast
