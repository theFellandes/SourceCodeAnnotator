from dataclasses import dataclass

from Utils.reader import Reader
from Utils.writer import Writer
from conf import settings


@dataclass
class BaseController:

    source_code_file_name: str = ''

    def __post_init__(self):
        self.source_code_path = settings.get_path(self.source_code_file_name)
        self.reader = Reader(self.source_code_path)
        self.writer = Writer(settings.REPORT_PATH)
        self.source_code_string = self.reader.read_in_string()

    def get_single_line_comments(self) -> list:
        """ Returns single line comments for the language """

    def get_multi_line_comments(self) -> list:
        """ Returns multi line comments for the language """

    def get_doc_comments(self) -> list:
        """ Returns multi line comments for the language """

    def generate_report(self):
        """ Generates report for comments """

    def write_ast_to_file(self):
        """ Generates file for ast """

    def generate_comment(self):
        """ Generate comment using ast """
