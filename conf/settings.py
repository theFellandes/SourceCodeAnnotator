import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SOURCE_CODE_DIR = os.path.join(BASE_DIR, 'SourceCodes')
JAVA_PATH = os.path.join(SOURCE_CODE_DIR, 'Java')
PYTHON_PATH = os.path.join(SOURCE_CODE_DIR, 'Python')
PATH_DICTIONARY = {
    'py': PYTHON_PATH,
    'java': JAVA_PATH,
}


def __find_file_extension_from_source_code(source_code_name_with_extension: str) -> str:
    """
    Returns the file extension from source code

    :param source_code_name_with_extension: Source code name with extension
    :return: file extension
    :exception IndexError: Entered source code name missing extension.
    """
    splitted_source_code_name = source_code_name_with_extension.split('.')
    try:
        file_extension = splitted_source_code_name[1]

    except IndexError:
        raise IndexError('File Extension Missing.')

    return file_extension


def get_path(source_code_name_with_extension: str) -> str:
    """
    Returns Java source code's path

    :argument source_code_name_with_extension: string version of the source code file name
    :returns source_code_path: string version of the source code path

    :exception TypeError: Entered coding language format is wrong or does not exist.
    :exception IndexError: Entered source code name missing extension.
    """
    coding_language = __find_file_extension_from_source_code(source_code_name_with_extension)
    coding_language_path = PATH_DICTIONARY.get(coding_language)

    try:
        source_code_path = os.path.join(coding_language_path, source_code_name_with_extension)

    except TypeError:
        raise TypeError("Entered coding language does not exist.")

    return source_code_path
