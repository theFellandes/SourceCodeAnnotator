import pytest

from Utils.character_manipulation import CharacterManipulation


@pytest.fixture
def character_manipulation():
    return CharacterManipulation()


def test_remove_escape_characters(character_manipulation):
    actual = "Te\nst\n"
    expected = "Test"
    assert character_manipulation.remove_escape_characters(actual) == expected
