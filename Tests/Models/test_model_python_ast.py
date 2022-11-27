import pytest

from Models.SourceCode.python_ast import PythonAST


@pytest.fixture
def python_ast():
    return PythonAST("source_code.py")


def test_python_ast(python_ast):
    python_ast.generate_ast()


def test_write_python_ast(python_ast):
    python_ast.write_ast_to_file()
