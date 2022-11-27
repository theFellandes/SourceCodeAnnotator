import dataclasses
from dataclasses import dataclass, field

from Utils.reader import Reader
from Utils.writer import Writer
from conf import settings


@dataclass
class ASTBase:
    source_code_file_name: str
    source_code_string: str = field(init=False, default="")
    single_line_comments_list: list = field(init=False, default_factory=list)
    multi_line_comments_list: list = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        """
        Initializes the Source Code Parser rest of the attributes

        Initializes:
        source_code_path: string path of the source code
        reader: the Reader object for the source_code_path
        source_code_string: source code contents saved to string
        """
        self.source_code_path = settings.get_path(self.source_code_file_name)
        self.reader = Reader(self.source_code_path)
        self.writer = Writer(settings.REPORT_PATH)
        self.source_code_string = self.reader.read_in_string()

    def as_dict(self) -> dict:
        """Returns dict of the class"""
        return dataclasses.asdict(self)

    def generate_ast(self):
        """ Implement generate ast for source code base """

    def write_ast_to_file(self):
        """ Implement write_ast_to_file for source code base for debugging """
