from Controller.annotator_controller import AnnotatorController
from Controller.controller_factory import ControllerFactory


def main():
    # annotator_controller = AnnotatorController(get_controller('ReturnStatement.java'))
    controller = ControllerFactory('Demo/list_comprehension.py').get_controller()
    # controller = ControllerFactory('Demo/for_loop.py').get_controller()
    annotator_controller = AnnotatorController(controller)
    # print(annotator_controller.get_ast())
    annotator_controller.write_ast()
    annotator_controller.comment_source_code()

if __name__ == '__main__':
    main()
