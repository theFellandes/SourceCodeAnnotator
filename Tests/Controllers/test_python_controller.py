import pytest

from Controller.python_controller import PythonController


@pytest.fixture
def python_controller():
    return PythonController('source_code.py')


def test_get_single_line_comments(python_controller):
    assert python_controller.get_single_line_comments() is not None


def test_get_multi_line_comments(python_controller):
    assert python_controller.get_multi_line_comments() is not None


def test_get_doc_comments(python_controller):
    assert python_controller.get_doc_comments() is not None

