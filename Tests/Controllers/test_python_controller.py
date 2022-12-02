import pytest

from Controller.python_controller import PythonController


@pytest.fixture
def python_controller():
    return PythonController('basic_addition.py')


def test_get_single_line_comments(python_controller):
    assert python_controller.get_single_line_comments() is not None


def test_get_multi_line_comments(python_controller):
    assert python_controller.get_multi_line_comments() is not None


def test_get_doc_comments(python_controller):
    assert python_controller.get_doc_comments() is not None


def test_generate_python_ast(python_controller):
    assert python_controller.generate_comment() is not None

def test_python_ast(python_controller):
    python_controller.generate_ast()


def test_write_python_ast(python_controller):
    python_controller.write_ast_to_file()
