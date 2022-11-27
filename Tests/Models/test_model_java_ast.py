import pytest

from Models.SourceCode.java_ast import JavaAST


@pytest.fixture
def java_ast():
    return JavaAST("Main.java")


def test_java_ast(java_ast):
    java_ast.generate_ast()


def test_write_java_ast(java_ast):
    java_ast.write_ast_to_file()
