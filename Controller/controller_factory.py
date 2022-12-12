from dataclasses import dataclass

from Controller.java_controller import JavaController
from Controller.python_controller import PythonController
from conf import settings


@dataclass
class ControllerFactory:

    source_code_file_name: str
    source_code_string: str = ''

    def get_controller(self):
        match settings.get_file_extension(self.source_code_file_name):
            case 'java':
                return JavaController(self.source_code_file_name)
            case 'py':
                return PythonController(self.source_code_file_name)
            case _:
                return NotImplementedError