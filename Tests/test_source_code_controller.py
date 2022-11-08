import pytest

from Controller.source_code_controller import SourceCodeParserController


@pytest.fixture
def java_source_code_parser():
    return SourceCodeParserController("Main.java")


@pytest.fixture
def python_source_code_parser():
    return SourceCodeParserController("source_code.py")


def test_java_source_code_string(java_source_code_parser):
    java_source_code_parser.remove_escape_characters()
    actual = java_source_code_parser.source_code_string
    assert "\n" not in actual


def test_python_source_code_string(python_source_code_parser):
    actual = python_source_code_parser.source_code_string
    assert "\n" in actual


def test_java_source_code_print(java_source_code_parser):
    java_source_code_parser.generate_ast()


def test_python_source_code_print(python_source_code_parser):
    python_source_code_parser.generate_ast()

def test_as_dict(java_source_code_parser):
    assert type(java_source_code_parser.as_dict()) is type({})