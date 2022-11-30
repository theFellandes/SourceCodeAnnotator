from dataclasses import dataclass

from Controller.base_controller import BaseController
from Utils.writer import Writer


@dataclass
class ReportController:
    writer: Writer
    base_controller: BaseController

    def __post_init__(self):
        self.generate_report_header()
        self.generate_report()
        self.print_to_file()

    def print_to_file(self):
        self.writer.buffered_writer()

    def generate_report_header(self):
        self.writer.append_buffer(f"{self.base_controller.source_code_file_name} Report\n")
        self.writer.append_buffer("There are:\n\n")

    def generate_report(self) -> None:
        """ Generates the report.txt for source code """
        number_of_single_lines = self.generate_single_line_report()
        number_of_multi_lines = self.generate_multi_line_report()
        number_of_doc_comments = self.generate_doc_comments_report()
        total_lines_of_comment = number_of_single_lines + number_of_multi_lines + number_of_doc_comments
        self.writer.append_buffer(
            f"* {total_lines_of_comment} Total Lines of Comments\n"
        )

    def generate_single_line_report(self):
        single_lines = self.base_controller.get_single_line_comments()
        self.writer.append_buffer(
            f"* {len(single_lines)} Single Line Comments\n"
        )
        return len(single_lines)

    def generate_multi_line_report(self):
        multi_lines = self.base_controller.get_multi_line_comments()
        self.writer.append_buffer(
            f"* {len(multi_lines)} Multi Line Comments\n"
        )
        return len(multi_lines)

    def generate_doc_comments_report(self):
        doc_comments = self.base_controller.get_doc_comments()
        self.writer.append_buffer(
            f"* {len(doc_comments)} Multi Line Comments\n"
        )
        return len(doc_comments)
