import os.path
import javalang
from javalang.tree import CompilationUnit
from Utils.time_util import get_time
from conf.settings import JAVA_PATH


@get_time
def main():
    source_code_path = get_java_path('Main.java')
    source_code_string = read_java_source_code_as_string(source_code_path)
    tree: CompilationUnit = javalang.parse.parse(source_code_string)
    print(tree)


def get_java_path(source_code_name: str) -> str:
    """
    Returns Java source code's path

    :argument source_code_name: string version of the source code file name
    :returns source_code_path: string version of the source code path
    """
    source_code_path = os.path.join(JAVA_PATH, source_code_name)
    return source_code_path


def read_java_source_code_as_string(source_code_path: str) -> str:
    """
    Returns string version of the source code contents

    :argument source_code_path: string path of source code
    :returns source_code_string: string version of the source code
    """
    with open(source_code_path, 'r', encoding='utf-8') as reader:
        source_code_string = reader.read()

    return source_code_string


if __name__ == '__main__':
    main()
