import javalang
from javalang.tree import CompilationUnit
from Utils.time_util import get_time
from Utils.reader import Reader
from conf import settings


@get_time
def main():
    source_code_path = settings.get_path('Main.java')
    reader = Reader(source_code_path)
    source_code_string = reader.read_in_string()
    tree: CompilationUnit = javalang.parse.parse(source_code_string)
    print(tree)


if __name__ == '__main__':
    main()
