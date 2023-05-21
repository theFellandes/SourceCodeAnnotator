import demo
import random
import re

from dataclasses import dataclass

from Controller.base_controller import BaseController
from Models.SourceCode.python_ast import PythonAST


@dataclass
class PythonController(BaseController):
    _if_index: int = random.randint(0, 3)

    def __post_init__(self):
        super().__post_init__()
        self.python_ast = PythonAST(self.source_code_string)
        # TODO: Do body commenti kötü oluşabilir, deneme-yanılma
        self._if_comments_list = [
            'Checks if {condition}: {body}',
            'If {condition} then {body}',
            '{body} if {condition}',
            'Evaluates if {condition} and {body}',
        ]

    def get_ast(self):
        return self.python_ast.get_ast()

    def write_ast(self):
        return self.python_ast.write_ast()

    def comment_source_code(self):
        """ Returns the commented source code generated by LazyDoc """
        comments_and_line_numbers = self.comment_functions(self.python_ast.get_ast().body)
        source_code_list = self.source_code_string.splitlines()

        for lineno, comment in reversed(comments_and_line_numbers.items()):
            leading_whitespace = re.match(r'^\s+', source_code_list[lineno])
            indented_comment = ''
            for comment_line in comment.splitlines():
                indented_comment += f'{leading_whitespace.group(0)}{comment_line}\n'
            source_code_list.insert(lineno, indented_comment.rstrip())

        self.source_code_string = '\n'.join(source_code_list)
        self.source_code_string = demo.apply_backspace(self.source_code_string)
        return self.source_code_string

    def comment_functions(self, ast_body):
        comments_and_line_numbers = {}
        for child in ast_body:
            if type(child).__name__ == 'FunctionDef':
                comments_and_line_numbers.update({child.lineno: self.comment_function(child)})

            if type(child).__name__ == 'ClassDef':
                comments_and_line_numbers.update(self.comment_functions(child.body))

        return comments_and_line_numbers

    @staticmethod
    def update_circular_index(incremented_value, the_list):
        return (incremented_value + 1) % len(the_list)

    def comment_function(self, function_def):
        comments = []
        comment = '"""\n'
        # TODO: Fix this documentation line so that it wouldn't corrupt the documentation.
        # TODO: Remove this.
        comment += f'Documentation of {function_def.name} function.\n'
        get_set_comment = self.comment_getter_setter(function_def)
        if get_set_comment:
            print(get_set_comment)
            return f'"""\n{get_set_comment}\n"""'
        for statement in function_def.body:
            if type(statement).__name__ == 'Expr':
                if type(statement.value).__name__ == 'Constant':
                    continue
            line_comment = self.run_all_comment_functions(statement).rstrip() + '. '
            comment += line_comment[0].upper() + line_comment[1:]
        comment += '\n"""'
        print(comment)
        return comment

    def run_all_comment_functions(self, line):
        # Order of these function calls matter, for one above the if, we should put a dot after its comment.
        comment = ""
        comment += self.comment_loop(line)
        comment += self.comment_match(line)
        comment += self.comment_if(line)
        # if comment:
        #     comment = comment[:-1] + ". "
        comment += self.comment_normal_line(line)
        if not comment:
            return "\b"
        return comment[0].lower() + comment[1:]

    @staticmethod
    def comment_getter_setter(function_def):
        if function_def.name.startswith('get_'):
            return f"Gets the {function_def.body[0].value.attr} attribute"

        if function_def.name.startswith('set_'):
            return f"Sets the {function_def.body[0].targets[0].attr} attribute"

        if hasattr(function_def, 'decorator_list'):
            for decorator in function_def.decorator_list:
                if hasattr(decorator, 'id') and decorator.id == 'property':
                    return f"Gets the {function_def.name} attribute"
                if hasattr(decorator, 'attr') and decorator.attr == 'setter':
                    return f"Sets the {function_def.name} attribute"

        return ''

    @staticmethod
    def stringify_data_types(data_type, statement):
        match data_type:
            case 'Tuple':
                return f"({statement})"
            case 'List':
                return f"[{statement}]"
            case 'Set':
                return f"{{{statement}}}"

    def stringify_statement(self, statement) -> str:
        left_side = ""
        right_side = ""
        operator = ""

        match type(statement).__name__:
            # TODO: Dictionary stringify
            case 'Assign':
                left_side = self.stringify_statement(statement.targets[0])
                right_side = self.stringify_statement(statement.value)
                operator = "="

            case 'AugAssign':
                left_side = self.stringify_statement(statement.target)
                right_side = self.stringify_statement(statement.value)
                operator = self.python_ast.handle_operators(statement.op)

            case 'Name':
                return statement.id

            case 'Attribute':
                return f'{self.stringify_statement(statement.value)}.{statement.attr}'

            case 'Tuple' | 'List' | 'Set':
                for element in statement.elts:
                    left_side += str(self.stringify_statement(element)) + ", "
                return self.stringify_data_types(type(statement).__name__, left_side.rstrip(', '))

            case 'Subscript':
                return f'{self.stringify_statement(statement.value)}[{self.stringify_statement(statement.slice)}]'

            case 'Slice':
                if statement.step:
                    return f'{self.stringify_statement(statement.lower)}:{self.stringify_statement(statement.upper)}:{self.stringify_statement(statement.step)}'
                return f'{self.stringify_statement(statement.lower)}:{self.stringify_statement(statement.upper)}'

            case 'Constant':
                if type(statement.value).__name__ == 'str':
                    return f"'{statement.value}'"
                return f'{statement.value}'

            case 'Expr':
                return self.stringify_statement(statement.value)

            case 'BinOp':
                left_side = self.stringify_statement(statement.left)
                right_side = self.stringify_statement(statement.right)
                operator = self.python_ast.handle_operators(statement.op)

            case 'Compare':
                comment = self.stringify_statement(statement.left)
                for op, comparator in zip(statement.ops, statement.comparators):
                    comment += f' {self.python_ast.handle_operators(op)} {self.stringify_statement(comparator)}'
                return comment

            case 'BoolOp':
                left_side = self.stringify_statement(statement.values[0])
                right_side = self.stringify_statement(statement.values[1])
                operator = self.python_ast.handle_operators(statement.op)

            case 'Call':
                if hasattr(statement.func, 'id') and statement.func.id == 'range':
                    if len(statement.args) == 1:
                        return f'0 to {int(self.stringify_statement(statement.args[0])) - 1}'
                    else:
                        comment = f'{self.stringify_statement(statement.args[0])} to {int(self.stringify_statement(statement.args[1])) - 1}'
                        if len(statement.args) == 3:
                            comment = f'{comment} with steps of {self.stringify_statement(statement.args[2])}'
                        return comment
                for arg in statement.args:
                    right_side += str(self.stringify_statement(arg)) + ", "
                right_side = right_side.rstrip(', ')
                return f'{self.stringify_statement(statement.func)}({right_side})'

            case 'ListComp' | 'GeneratorExp' | 'DictComp' | 'SetComp':
                return f'values {self.stringify_statement(statement.generators[0].iter)}'

            case 'UnaryOp':
                return f'{self.python_ast.handle_operators(statement.op)} {self.stringify_statement(statement.operand)}'

        return f"{left_side} {operator} {right_side}"

    def stringify_match_case(self, statement) -> str:
        match type(statement).__name__:
            case 'MatchSequence':
                comment = '['
                for pattern in statement.patterns:
                    comment += f'{self.stringify_match_case(pattern)}, '
                comment = comment.rstrip(', ')
                comment += ']'
                return comment
            case 'MatchValue':
                return f'{self.stringify_statement(statement.value)}'
            case 'MatchSingleton':
                raise NotImplementedError
            case 'MatchOr':
                comment = ''
                for pattern in statement.patterns:
                    comment += f'{self.stringify_match_case(pattern)} | '
                comment = comment.rstrip('| ')
                return comment
        return ''

    def comment_loop(self, statement):
        inner_comments = []
        if type(statement).__name__ == 'For':
            inner_statement = self.comment_inner_statements(statement.body)
            if "print" in inner_statement.lower() and len(statement.body) == 1:
                return f'Iterates from {self.stringify_statement(statement.iter)} and prints them '
            comment = f'Iterates {self.stringify_statement(statement.target)} from {self.stringify_statement(statement.iter)}: {inner_statement}'
            return comment
        if type(statement).__name__ == 'While':
            comment = f'Loops while {self.stringify_statement(statement.test)}: {self.comment_inner_statements(statement.body)}'
            return comment
        return ''

    def comment_if(self, statement):
        comment = ''
        if type(statement).__name__ == 'If':
            comment = self._if_comments_list[self._if_index].format(condition=self.stringify_statement(statement.test), body=self.comment_inner_statements(statement.body).rstrip())
            self._if_index = self.update_circular_index(self._if_index, self._if_comments_list)

            el = statement
            while el.orelse:
                else_body = el.orelse
                el = el.orelse[0]
                if not hasattr(el, 'orelse'):
                    comment += f'; else {self.comment_inner_statements(else_body).rstrip()}'
                    break
                comment += f'; or if {self.stringify_statement(el.test)}: {self.comment_inner_statements(el.body).rstrip()}'
        return comment

    def comment_match(self, statement):
        if type(statement).__name__ == 'Match':
            comment = f'If {self.stringify_statement(statement.subject)} '
            for match_case in statement.cases:
                if (matches_value := self.stringify_match_case(match_case.pattern)) != '':
                    comment += f'matches {matches_value}: {self.comment_inner_statements(match_case.body)}or '
                else:
                    comment += f'by default: {self.comment_inner_statements(match_case.body)}or '
            comment = comment.rstrip('or ')
            return comment
        return ''

    def comment_normal_line(self, statement):
        # TODO: Remove parenthesis around assignment tuples.
        if type(statement).__name__ == 'Assign':
            return f'Assigns {self.stringify_statement(statement.value)} to {self.stringify_statement(statement.targets[0])} '
        elif type(statement).__name__ == 'Expr':
            if type(statement.value).__name__ == 'Call':
                if hasattr(statement.value.func, 'id') and statement.value.func.id == 'print':
                    if len(statement.value.args) >= 1:
                        return f'Prints {self.stringify_statement(statement.value.args[0])} '
                    return f'Prints newline '
                return self.comment_function_expression(statement.value)
        elif type(statement).__name__ == 'AugAssign':
            match type(statement.op).__name__:
                case 'Add':
                    return f'Adds {self.stringify_statement(statement.value)} to {self.stringify_statement(statement.target)} '
                case 'Sub':
                    return f'Subtracts {self.stringify_statement(statement.value)} from {self.stringify_statement(statement.target)} '
                case 'Mult':
                    return f'Markiplies {self.stringify_statement(statement.target)} with {self.stringify_statement(statement.value)} '
                case 'Div' | 'FloorDiv':
                    return f'Divides {self.stringify_statement(statement.target)} by {self.stringify_statement(statement.value)} '
                case 'Mod':
                    return f'Updates the value of {self.stringify_statement(statement.target)} by taking its modulus with {self.stringify_statement(statement.value)} '
                case 'Pow':
                    return f'Raises {self.stringify_statement(statement.target)} to the power of {self.stringify_statement(statement.value)} '
        elif type(statement).__name__ == "Return":
            return f'Returns {self.stringify_statement(statement.value)} '
        return ''

    def comment_inner_statements(self, statement_body):
        comment = ''
        inner_comments = []
        for inner_statement in statement_body:
            inner_comments.append(self.run_all_comment_functions(inner_statement))
        comment += '\b, '.join(map(str, inner_comments))
        return comment

    @staticmethod
    def function_name_parser(function_name: str) -> tuple[list[str], bool]:
        common_verbs = [
            'remove', 'add', 'get',
            'set', 'update', 'delete',
            'create', 'insert', 'append',
            'pop', 'sort', 'draw', 'init',
            'pause', 'resume', 'start',
            'stop', 'clear', 'reset',
        ]

        function_name = re.sub(r'(?<!^)(?=[A-Z])', '_', function_name).lower()
        function_verbs_list = function_name.split('_')
        return function_verbs_list, function_verbs_list[0] in common_verbs

    def comment_function_expression(self, call_statement):
        """
        call_statement -> "file.remove()", "bruh.removeStudentId()", "print()"
        {func_name}
        """
        # file.remove() removes the file
        # bruh.removeStudentId() removes student id
        if type(call_statement.func).__name__ ==  'Attribute':
            # file.remove() || bruh.removeStudentId()
            function_names, is_common_name = self.function_name_parser(call_statement.func.attr)

            if is_common_name:
                # Create the comment here
                raise NotImplementedError()

        elif type(call_statement.func).__name__ ==  'Name':
            # print()
            function_names, is_common_name = self.function_name_parser(call_statement.func.id)

            if is_common_name:
                # Same shit
                raise NotImplementedError()

        return f'Calls {self.stringify_statement(call_statement)} '



    # TODO: For-If bağlantısı (for'un içinde if varsa)
    # TODO: Web scraping??? (BeautifulSoup) (Most common functions json oluşturup oradan arama yapılabilir son çare olarak)
    # TODO: Commenting every source code file in a directory -> 3 Method: VSCode, Command Line, Web UI (Zip)
    # TODO: Parametreler ve return value'lar handled değil
    # TODO: Abstract methodlar handled değil (Optional: Body'si boşsa case'i)
    # TODO: Unhandled cases: Walrus
