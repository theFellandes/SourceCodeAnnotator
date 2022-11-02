import pytest
import os

from conf import settings


@pytest.fixture
def java_path():
    return os.path.join(settings.JAVA_PATH, 'Main.java')


@pytest.fixture
def bad_java_path():
    return os.path.join(settings.JAVA_PATH, 'Main.txt.java')


@pytest.fixture
def python_path():
    return os.path.join(settings.PYTHON_PATH, 'source_code.py')


def test_java_path(java_path):
    actual = settings.get_path('Main.java')
    assert java_path == actual


def test_python_path(python_path):
    actual = settings.get_path('source_code.py')
    assert python_path == actual


def test_exception_java_path():
    """
    Tests the Main.java.txt raises TypeError
    due to txt extension not being supported
    """
    with pytest.raises(TypeError):
        settings.get_path('Main.java.txt')


def test_bad_java_path(bad_java_path):
    """ Tests the Main.txt.java returns correctly """
    actual = settings.get_path('Main.txt.java')
    assert bad_java_path == actual
