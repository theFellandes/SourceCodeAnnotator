from Controller.annotator_controller import AnnotatorController
from Controller.controller_factory import ControllerFactory
from Utils.time_util import get_time
from Utils.NLP.Stanza.stanza_module import NameAnalyzer


@get_time
def main():
    # annotator_controller = AnnotatorController(get_controller('ReturnStatement.java'))
    controller = ControllerFactory('ReturnStatement.java').get_controller()
    annotator_controller = AnnotatorController(controller)
    # To extract the source code string for Open AI
    # print(repr(annotator_controller.base_controller.source_code_string))
    # print(annotator_controller.get_single_line_comments())
    # print(annotator_controller.generate_comment())

    print(annotator_controller.generate_comment_from_function_name())

    # annotator_controller.generate_report()
    # name_analyzer = NameAnalyzer()
    # name_analyzer.get_generated_comment("getFunctionName")


if __name__ == '__main__':
    main()
