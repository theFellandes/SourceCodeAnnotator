import ast
from dataclasses import dataclass

from Utils.ast_to_file import ast_to_file
from Utils.pretty_object import python_ast_prettier
from Utils.time_util import get_time
from Models.SourceCode.ast_base import ASTBase


@dataclass
class PythonAST(ASTBase):

    def __post_init__(self):
        self.python_ast = self.get_ast()

    def get_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast

    def generate_comment_for_function(self):
        # TODO: Loop through a function, and get the comments for that function.
        function_comments = []
        for function in self.python_ast.body:
            if isinstance(function, ast.FunctionDef):
                function_comments.append(self.get_comment_for_return_statement(function))
        return function_comments

    def get_list_of_function_names(self) -> list[str]:
        list_of_function_names = []
        list_of_function_names = [function.name
                                  for function in self.python_ast.body if type(function) == ast.FunctionDef]
        return list_of_function_names

    def get_list_of_assignments(self) -> list[any, any]:
        list_of_assignments = self._get_list_of_constant_assignments() + self._get_list_of_call_assignments()
        return list_of_assignments

    def _get_list_of_constant_assignments(self) -> list[any, any]:
        """ Returns a list of assignments that are constant assignments """
        return [(assignment.targets[0].id, assignment.value.s)
                                for assignment in self.python_ast.body if (type(assignment) == ast.Assign
                                                                           and type(assignment.value) == ast.Constant)]

    def _get_list_of_call_assignments(self) -> list[any, any]:
        """ Returns a list of assignments that are calls """
        return [(assignment.targets[0].id, assignment.value.func.id)
                    for assignment in self.python_ast.body if (type(assignment) == ast.Assign
                                                               and type(assignment.value) == ast.Call)]
    @staticmethod
    def get_comment_for_return_statement(function_def) -> str:
        """ Creates comment for return statement of a function """
        for statement in function_def.body:
            if type(statement) == ast.Return:
                if type(statement.value) == ast.Constant:
                    return f'@return: {statement.value.s}'
                # TODO: Add support for context of return statement
                return f'@return: {statement.value.id}'
        return ''

    @ast_to_file
    @python_ast_prettier
    @get_time
    def write_ast_to_file(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast

    @python_ast_prettier
    @get_time
    def write_ast(self) -> ast:
        """Prints python_ast to the console"""
        # Since Python uses tabs and newlines, only comments extracted
        # requires the escape character deletion.

        python_ast = ast.parse(self.source_code_string)
        return python_ast
