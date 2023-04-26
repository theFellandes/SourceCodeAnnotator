from Controller.annotator_controller import AnnotatorController
from Controller.controller_factory import ControllerFactory


def main():
    # annotator_controller = AnnotatorController(get_controller('ReturnStatement.java'))
    controller = ControllerFactory('for_loop.java').get_controller()
    annotator_controller = AnnotatorController(controller)
    # print(annotator_controller.get_ast())
    annotator_controller.write_ast()
    annotator_controller.comment_source_code()

if __name__ == '__main__':
    main()
