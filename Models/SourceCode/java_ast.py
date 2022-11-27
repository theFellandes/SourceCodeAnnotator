from dataclasses import dataclass

import javalang
from javalang.tree import CompilationUnit

from Utils.ast_to_file import ast_to_file
from Utils.pretty_object import pretty_object
from Utils.time_util import get_time
from Models.SourceCode.ast_base import ASTBase


@dataclass
class JavaAST(ASTBase):

    def generate_ast(self) -> CompilationUnit:
        """Prints java_ast to the console"""
        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return tree

    @ast_to_file
    @pretty_object
    @get_time
    def write_ast_to_file(self):
        """Prints java_ast to the console"""
        tree: CompilationUnit = javalang.parse.parse(self.source_code_string)
        return tree
