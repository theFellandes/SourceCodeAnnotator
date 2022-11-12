import pytest

from Controller.source_code_controller import SourceCodeParserController


@pytest.fixture
def java_source_code_parser():
    return SourceCodeParserController("Main.java")


@pytest.fixture
def python_source_code_parser():
    return SourceCodeParserController("source_code.py")


def test_java_source_code_string(java_source_code_parser):
    java_source_code_parser.remove_escape_characters(java_source_code_parser.source_code_string)
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


def test_as_dict_for_java(java_source_code_parser):
    # TODO: Remove some unnecessary tests and fix the tests
    java_source_code_parser.generate_ast()
    java_source_code_parser.capture_multi_line_comments()
    # java_source_code_parser.capture_single_line_comments()
    print(java_source_code_parser.as_dict().get('multi_line_comments_list'))
    print(len(java_source_code_parser.as_dict().get('multi_line_comments_list')))


def test_as_dict_for_python(python_source_code_parser):
    # TODO: Remove some unnecessary tests and fix the tests
    python_source_code_parser.generate_ast()
    python_source_code_parser.capture_multi_line_comments()
    # python_source_code_parser.capture_single_line_comments()
    print(python_source_code_parser.as_dict())
    print(python_source_code_parser.as_dict().get('multi_line_comments_list'))
    print(len(python_source_code_parser.as_dict().get('multi_line_comments_list')))


def test_report_generate_python(python_source_code_parser):
    python_source_code_parser.generate_report()


def test_report_generate_java(java_source_code_parser):
    java_source_code_parser.generate_report()
