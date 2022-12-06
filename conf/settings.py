import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SOURCE_CODE_DIR = os.path.join(BASE_DIR, "SourceCodes")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
REPORT_PATH = os.path.join(OUTPUT_DIR, "report.txt")
AST_REPORT_PATH = os.path.join(OUTPUT_DIR, "ast_report.txt")
JAVA_PATH = os.path.join(SOURCE_CODE_DIR, "Java")
PYTHON_PATH = os.path.join(SOURCE_CODE_DIR, "Python")
GO_PATH = os.path.join(SOURCE_CODE_DIR, "Go")
C_PATH = os.path.join(SOURCE_CODE_DIR, "C")
STANZA_PATH = os.path.join(BASE_DIR, "Utils/NLP/Stanza")
STANZA_RESOURCES_PATH = os.path.join(STANZA_PATH, "Stanza")
PATH_DICTIONARY = {
    "py": PYTHON_PATH,
    "java": JAVA_PATH,
    "go": GO_PATH,
    "c": C_PATH,
}
# TODO: Edit this
GOOD_CODE_STATISTICS = {
    "java": {
        "single_line": 300,
        "multi_line": 250,
        "java_doc": 150,
        "total_line": 300,
        "comment_per_line": 45,
    },
    "py": {
        "single_line": 300,
        "multi_line": 250,
        "total_line": 150,
        "comment_per_line": 40,
    },
}


def get_file_extension(source_code_name_with_extension: str) -> str:
    """
    Returns the file extension from source code

    :param source_code_name_with_extension: Source code name with extension
    :return: file extension: The file extension for the source code.
    """
    _, _, file_extension = source_code_name_with_extension.rpartition(".")
    return file_extension


def get_path(source_code_name_with_extension: str) -> str:
    """
    Returns Java source code's path

    :argument source_code_name_with_extension: string version of the source code file name
    :returns source_code_path: string version of the source code path

    :exception TypeError: Entered extension is not supported.
    """
    coding_language = get_file_extension(source_code_name_with_extension)
    coding_language_path = PATH_DICTIONARY.get(coding_language)

    try:
        source_code_path = os.path.join(
            coding_language_path, source_code_name_with_extension
        )

    except TypeError:
        raise TypeError("Entered extension is not supported.")

    return source_code_path

def is_path_empty(path: str):
    """ Returns path is empty or not """
    return not os.listdir(path)
