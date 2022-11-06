from Controller.source_code_controller import SourceCodeParserController
from Utils.time_util import get_time


@get_time
def main():
    java_source_code = "Main.java"
    python_source_code = "source_code.py"
    python_source_code_parser = SourceCodeParserController(python_source_code)
    python_source_code_parser.generate_ast()


if __name__ == "__main__":
    main()
