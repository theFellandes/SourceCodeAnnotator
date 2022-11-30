import dataclasses
from dataclasses import dataclass


@dataclass
class ASTBase:
    source_code_string: str

    def as_dict(self) -> dict:
        """Returns dict of the class"""
        return dataclasses.asdict(self)

    def generate_ast(self):
        """ Implement generate ast for source code base """

    def write_ast_to_file(self):
        """ Implement write_ast_to_file for source code base for debugging """
