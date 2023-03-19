import ast
from dataclasses import dataclass

from Utils.ast_to_file import ast_to_file
from Utils.pretty_object import python_ast_prettier
from Models.SourceCode.ast_base import ASTBase


@dataclass
class PythonAST(ASTBase):
    def get_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast

    def get_list_of_function_names(self) -> list[str]:
        list_of_function_names = []
        python_ast = self.get_ast()
        for children in python_ast.body:
            if type(children) == ast.FunctionDef:
                list_of_function_names.append(children.name)
        return list_of_function_names

    @ast_to_file
    @python_ast_prettier
    def write_ast_to_file(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast

    @python_ast_prettier
    def write_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.
        python_ast = ast.parse(self.source_code_string)
        return python_ast
