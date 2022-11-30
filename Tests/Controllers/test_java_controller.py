import pytest

from Controller.java_controller import JavaController


@pytest.fixture
def java_controller():
    return JavaController('Main.java')


def test_get_single_line_comments(java_controller):
    assert java_controller.get_single_line_comments() is not None


def test_get_multi_line_comments(java_controller):
    assert java_controller.get_multi_line_comments() is not None


def test_get_doc_comments(java_controller):
    assert java_controller.get_doc_comments() is not None
