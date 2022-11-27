from dataclasses import dataclass


@dataclass
class BaseController:

    def generate_comment(self, ast):
        """ Generate comment using ast """
