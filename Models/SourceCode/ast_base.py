import dataclasses
from dataclasses import dataclass


@dataclass
class ASTBase:
    source_code_string: str

    def as_dict(self) -> dict:
        """Returns dict of the class"""
        return dataclasses.asdict(self)

    def get_ast(self):
        """ Implement generate ast for source code base """

    def get_list_of_function_names(self):
        """ Returns list of function names """

    def write_ast_to_file(self):
        """ Implement write_ast_to_file for source code base for debugging """
