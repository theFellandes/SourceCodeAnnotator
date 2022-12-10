from dataclasses import dataclass

from Utils.reader import Reader
from Utils.writer import Writer
from Utils.NLP.Stanza import stanza_module
from Utils.NLP.Stanza.stanza_module import NameAnalyzer
from conf import settings



@dataclass
class BaseController:

    source_code_file_name: str = ''
    source_code_string: str = ''
    name_analyzer: NameAnalyzer = stanza_module.NameAnalyzer()
    writer: Writer = Writer(settings.REPORT_PATH)

    def __post_init__(self):
        try:
            if self.source_code_string == '':
                self.source_code_path = settings.get_path(self.source_code_file_name)
                self.reader = Reader(self.source_code_path)
                self.source_code_string = self.reader.read_in_string()
        except FileNotFoundError as file_not_found:
            self.source_code_string = ''
            print(file_not_found.strerror)


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

    def get_ast(self):
        """ Returns the generated ast tree """

    def generate_comment_from_function_name(self):
        """ Generate comment using ast """
