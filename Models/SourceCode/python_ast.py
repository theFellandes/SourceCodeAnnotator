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

    @staticmethod
    def handle_operators(operator):
        if type(operator).__name__ == 'Add':
            return '+'
        if type(operator).__name__ == 'Sub':
            return '-'
        if type(operator).__name__ == 'Mult':
            return '*'
        if type(operator).__name__ == 'Div':
            return '/'
        if type(operator).__name__ == 'Mod':
            return '%'
        if type(operator).__name__ == 'Pow':
            return '**'
        if type(operator).__name__ == 'LShift':
            return '<<'
        if type(operator).__name__ == 'RShift':
            return '>>'
        if type(operator).__name__ == 'BitOr':
            return '|'
        if type(operator).__name__ == 'BitXor':
            return '^'
        if type(operator).__name__ == 'BitAnd':
            return '&'
        if type(operator).__name__ == 'FloorDiv':
            return '//'
        if type(operator).__name__ == 'MatMult':
            return '@'
        if type(operator).__name__ == 'Eq':
            return '=='
        if type(operator).__name__ == 'NotEq':
            return '!='
        if type(operator).__name__ == 'Lt':
            return '<'
        if type(operator).__name__ == 'LtE':
            return '<='
        if type(operator).__name__ == 'Gt':
            return '>'
        if type(operator).__name__ == 'GtE':
            return '>='
        if type(operator).__name__ == 'Is':
            return 'is'
        if type(operator).__name__ == 'IsNot':
            return 'is not'
        if type(operator).__name__ == 'In':
            return 'in'
        if type(operator).__name__ == 'NotIn':
            return 'not in'
        if type(operator).__name__ == 'And':
            return 'and'
        if type(operator).__name__ == 'Or':
            return 'or'
        if type(operator).__name__ == 'Not':
            return 'not'
        return ''

