import pytest

from Models.Entities.java_ast import JavaAST


@pytest.fixture
def java_ast():
    return JavaAST([])


def test_java_ast_initialized(java_ast):
    assert java_ast.imports == []
