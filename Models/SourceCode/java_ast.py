from dataclasses import dataclass, field

import javalang
from javalang.tree import CompilationUnit

from Utils.ast_to_file import ast_to_file
from Utils.pretty_object import pretty_object
from Utils.time_util import get_time
from Models.SourceCode.ast_base import ASTBase


@dataclass
class JavaAST(ASTBase):

    __tree: CompilationUnit = field(init=False, default=None)

    def __post_init__(self):
        self.generate_ast()

    def generate_ast(self) -> CompilationUnit:
        """Prints java_ast to the console"""
        self.__tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return self.__tree

    def get_list_of_function_names(self) -> CompilationUnit:
        """
        Returns the list of function names found in java ast tree

        # method.children => method.children[1] => {public, static}
        # method.children => method.children[5] => getRandomNumber (Function name)
        """
        return [method.children[5] for method in self.__tree.types[0].body]


    def get_return_value(self):
        if_stack = []
        method = self.__tree.types[0].body[1]
        print(f'\n{method.body[0]}')
        condition = method.body[0].condition
        comparison = f'Compares {condition.qualifier} to {condition.arguments[0].value}'
        print(f'\n\n\n{comparison}')
        if_return = method.body[0].then_statement.statements[0].expression.member
        return_statement = f'Returns {if_return}'
        print(f'{return_statement}')


    # def get_super_method_invocation(self):
    #
    #     try:
    #         super_method_check = self.__tree



    @ast_to_file
    @pretty_object
    @get_time
    def write_ast_to_file(self):
        """Prints java_ast to the console"""
        self.__tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return self.__tree
