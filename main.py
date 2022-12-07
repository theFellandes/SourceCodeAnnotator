from Controller.annotator_controller import AnnotatorController
from Controller.java_controller import JavaController
from Controller.python_controller import PythonController
from conf import settings
from Utils.time_util import get_time
from Utils.NLP.Stanza.stanza_module import NameAnalyzer


@get_time
def main():
    # annotator_controller = AnnotatorController(get_controller('ReturnStatement.java'))
    annotator_controller = AnnotatorController(get_controller('return_statement.py'))
    # To extract the source code string for Open AI
    # print(repr(annotator_controller.base_controller.source_code_string))
    # print(annotator_controller.get_single_line_comments())
    # print(annotator_controller.generate_comment())

    print(annotator_controller.generate_comment_from_function_name())

    # annotator_controller.generate_report()
    # name_analyzer = NameAnalyzer()
    # name_analyzer.get_generated_comment("getFunctionName")

def get_controller(source_code_file_name: str):
    match settings.get_file_extension(source_code_file_name):
        case 'java':
            return JavaController(source_code_file_name)
        case 'py':
            return PythonController(source_code_file_name)
        case _:
            return NotImplementedError


if __name__ == '__main__':
    main()
