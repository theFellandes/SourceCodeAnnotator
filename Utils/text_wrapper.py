import subprocess
import textwrap
from dataclasses import dataclass

import black


@dataclass
class TextWrapper:
    line_length: int = 80
    indent_level: int = 0
    indent_string: str = '    '

    def wrap(self, source_code: str) -> str:
        lines = source_code.splitlines()
        wrapped_lines = [self.indent_string * self.indent_level + line
                         for line in textwrap.wrap(lines[0], width=self.line_length)]
        for line in lines[1:]:
            wrapped_lines.extend(textwrap.wrap(line,
                                               width=self.line_length - len(self.indent_string) * self.indent_level,
                                               initial_indent=self.indent_string * self.indent_level,
                                               subsequent_indent=self.indent_string * (self.indent_level + 1)))
        return '\n'.join(wrapped_lines)

    @staticmethod
    def format_java_source_code(disarranged_source_output: str) -> str:
        """
        Uses google-java-format to format java source code

        https://github.com/google/google-java-format
        """
        cmd = ['java', '-jar', 'Utils\\google-java-format-1.16.0-all-deps.jar', '-']
        result = subprocess.run(cmd, input=disarranged_source_output.encode(), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        return result.stdout.decode()

    @staticmethod
    def format_python_source_code(disarranged_source_output: str) -> str:
        return black.format_str(disarranged_source_output, mode=black.Mode())
