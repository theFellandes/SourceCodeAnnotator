import pytest

from Models.SourceCode.ast_base import ASTBase


@pytest.fixture
def ast_base():
    return ASTBase("Main.java")


def test_ast_base(ast_base):
    print(ast_base)
