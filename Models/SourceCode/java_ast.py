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
        method = self.__tree.types[0].body[0]
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


    def stringify_statement(self, statement):
        left_side = ""
        right_side = ""
        operator = ""
        if type(statement).__name__ == "VariableDeclaration":
            left_side = statement.declarators[0].name
            right_side = self.stringify_statement(statement.declarators[0].initializer)
            operator = "="
        elif type(statement).__name__ == "BinaryOperation":
            left_side = self.stringify_statement(statement.operandl)
            right_side = self.stringify_statement(statement.operandr)
            operator = statement.operator
        elif type(statement).__name__ == "MemberReference":
            if statement.selectors:
                selectors_comment = ""
                for selector in statement.selectors:
                    selectors_comment += f"[{self.stringify_statement(selector.index)}]"
                return f"{statement.member}{selectors_comment}"
            return statement.member
        elif type(statement).__name__ == "Literal":
            return statement.value
        elif type(statement).__name__ == "MethodInvocation":
            arguments = []
            for argument in statement.arguments:
                arguments.append(self.stringify_statement(argument))
            return f"{statement.member}({', '.join(map(str, arguments))})"
        elif type(statement).__name__ == "ArrayCreator":
            string = f"new {statement.type.name}"
            for dimension in statement.dimensions:
                string += f"[{self.stringify_statement(dimension)}]"
            return string
        elif type(statement).__name__ == "ArrayInitializer":
            initializers = []
            for initializer in statement.initializers:
                initializers.append(self.stringify_statement(initializer))
            return f"{{{', '.join(map(str, initializers))}}}"
        elif type(statement).__name__ == "Cast":
            return f"({statement.type.name}) {self.stringify_statement(statement.expression)}"
        return f"{left_side} {operator} {right_side}"
