from dataclasses import dataclass

from Controller.base_controller import BaseController
from Models.SourceCode.python_ast import PythonAST


@dataclass
class PythonController(BaseController):
    def __post_init__(self):
        super().__post_init__()
        self.python_ast = PythonAST(self.source_code_string)

    def get_ast(self):
        return self.python_ast.get_ast()

    def write_ast(self):
        return self.python_ast.write_ast()


    def generate_comment_from_function_name(self):
        list_of_function_names = self.python_ast.get_list_of_function_names()
        list_of_generated_comments = [self.name_analyzer.get_generated_comment(function_name)
                                      for function_name in list_of_function_names]
        return list_of_generated_comments

    def comment_source_code(self):
        """ Returns the commented source code generated by LazyDoc """
        # TODO: self.source_code_string should be manipulated here
        self.source_code_string = self.comment_functions(self.python_ast.get_ast().body)
        return self.source_code_string

    def comment_functions(self, ast_body):
        for child in ast_body:
            if type(child).__name__ == 'FunctionDef':
                self.comment_function(child)

            if hasattr(child, 'body'):
                self.comment_functions(child.body)
        return self.source_code_string

    def comment_function(self, function_def):
        print(self.comment_getter_setter(function_def))

    @staticmethod
    def comment_getter_setter(function_def):
        if function_def.name.startswith('get_'):
            return f"Gets the {function_def.body[0].value.attr} attribute"

        if function_def.name.startswith('set_'):
            return f"Sets the {function_def.body[0].targets[0].attr} attribute"

        if hasattr(function_def, 'decorator_list'):
            for decorator in function_def.decorator_list:
                if hasattr(decorator, 'id') and decorator.id == 'property':
                    return f"Gets the {function_def.name} attribute"
                if hasattr(decorator, 'attr') and decorator.attr == 'setter':
                    return f"Sets the {function_def.name} attribute"

        return ''

    def recursive_test(self, ast_body):
        raise NotImplementedError
