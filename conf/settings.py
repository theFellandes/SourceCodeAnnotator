import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SOURCE_CODE_DIR = os.path.join(BASE_DIR, 'SourceCodes')
JAVA_PATH = os.path.join(SOURCE_CODE_DIR, 'Java')
PYTHON_PATH = os.path.join(SOURCE_CODE_DIR, 'Python')
PATH_DICTIONARY = {
    'py': PYTHON_PATH,
    'java': JAVA_PATH,
}


def __get_file_extension(source_code_name_with_extension: str) -> str:
    """
    Returns the file extension from source code

    :param source_code_name_with_extension: Source code name with extension
    :return: file extension: The file extension for the source code.
    """
    _, _, file_extension = source_code_name_with_extension.rpartition('.')
    return file_extension


def get_path(source_code_name_with_extension: str) -> str:
    """
    Returns Java source code's path

    :argument source_code_name_with_extension: string version of the source code file name
    :returns source_code_path: string version of the source code path

    :exception TypeError: Entered extension is not supported.
    """
    coding_language = __get_file_extension(source_code_name_with_extension)
    coding_language_path = PATH_DICTIONARY.get(coding_language)

    try:
        source_code_path = os.path.join(coding_language_path, source_code_name_with_extension)

    except TypeError:
        raise TypeError("Entered extension is not supported.")

    return source_code_path
