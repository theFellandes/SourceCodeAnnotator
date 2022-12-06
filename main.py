from Controller.annotator_controller import AnnotatorController
from Controller.java_controller import JavaController
from Controller.python_controller import PythonController
from conf import settings
from Utils.time_util import get_time
from Utils.NLP.Stanza.stanza_module import NameAnalyzer


@get_time
def main():
    annotator_controller = AnnotatorController(get_controller('Main.java'))
    print(annotator_controller.get_single_line_comments())
    annotator_controller.generate_report()
    name_analyzer = NameAnalyzer()
    name_analyzer.parse_function_name("getFunctionName")


def get_controller(source_code_file_name: str):
    match settings.get_file_extension(source_code_file_name):
        case 'java':
            return JavaController(source_code_file_name)
        case 'py':
            return PythonController(source_code_file_name)
        case other:
            return NotImplementedError


if __name__ == '__main__':
    main()
