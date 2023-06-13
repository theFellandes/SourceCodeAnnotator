import demo
import random
import re

from dataclasses import dataclass, field

from Controller.base_controller import BaseController
from Controller import verbs
from Models.SourceCode.python_ast import PythonAST
from Utils.web_scraper import WebScraper


@dataclass
class PythonController(BaseController):
    _if_index: int = random.randint(0, 3)
    # _if_index: int = 2
    _conjunction_accumulator: int = random.randint(0, 3)
    # _conjunction_accumulator: int = 4
    _exceptions: str = ''
    _assignments: list = field(default_factory=list)
    _assignment_flag: str = 'None'

    def __post_init__(self):
        super().__post_init__()
        self.python_ast = PythonAST(self.source_code_string)
        self.web_scraper = WebScraper('', 'site: pypi.org OR docs.python.org OR stackoverflow.com')
        # TODO: Do body commenti kötü oluşabilir, deneme-yanılma
        self._if_comments_list = [
            'Checks if {condition}; {body}',
            'If {condition} then {body}',
            'Evaluates whether {condition} {conjunction} {body} if so',
            'Evaluates if {condition} {conjunction} {body}',
        ]
        self._exceptions = "\nRaises:"
        self._conjunctions = [
            '\b; and',
            '\b; after that',
            '\b; and then',
            '\b; then',
            '\b; afterwards',
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
                if lineno == 0:
                    indented_comment += f'{comment_line}\n'
                    break
                indented_comment += f'{leading_whitespace.group(0)}{comment_line}\n'
            source_code_list.insert(lineno, indented_comment.rstrip())

        self.source_code_string = '\n'.join(source_code_list)
        self.source_code_string = demo.apply_backspace(self.source_code_string)
        return self.source_code_string

    def comment_functions(self, ast_body, do_import_statements=False):
        comments_and_line_numbers = {}

        if do_import_statements:
            comments_and_line_numbers.update({0: self.comment_import_statements(ast_body)})
        for child in ast_body:
            if type(child).__name__ == 'FunctionDef':
                comments_and_line_numbers.update({child.lineno: self.comment_function(child)})

            if type(child).__name__ == 'ClassDef':
                comments_and_line_numbers.update(self.comment_functions(child.body, False))

        return comments_and_line_numbers

    @staticmethod
    def update_circular_index(incremented_value, the_list):
        return (incremented_value + 1) % len(the_list)

    def comment_function(self, function_def):
        # comments = []
        comment = '"""\n'
        get_set_comment = self.comment_getter_setter(function_def)
        if get_set_comment:
            print(get_set_comment)
            return f'"""\n{get_set_comment}\n"""'
        for statement in function_def.body:
            if type(statement).__name__ == 'Expr':
                if type(statement.value).__name__ == 'Constant':
                    self.check_for_assignment_flag(statement)
                    continue
            if type(statement).__name__ == 'Assign':
                if type(statement.value).__name__ in ['Constant', 'Name']:
                    self.check_for_assignment_flag(statement)
                    continue
            line_comment = self.run_all_comment_functions(statement).rstrip() + '. '
            self.check_for_assignment_flag(statement)
            comment += line_comment[0].upper() + line_comment[1:]

        if self._exceptions != "\nRaises:":
            comment += self._exceptions

        comment += '\n"""'
        comment = self.line_break_comment(self.change_end_of_sentence(self.line_break_comment(comment)))
        print(comment)
        self._exceptions = "\nRaises:"
        return comment

    def random_sentence_end(self):
        # random_value = 0
        random_value = random.randint(0, 3)
        if random_value == 0:
            rv = self._conjunctions[self._conjunction_accumulator]
            self._conjunction_accumulator = self.update_circular_index(self._conjunction_accumulator, self._conjunctions)
            return ' ' + rv + ' '
        return '. '

    def change_end_of_sentence(self, comment: str):
        sentences = comment.split('. ')
        fixed_sentences = []
        should_lower = False
        for index, sentence in enumerate(sentences):
            if '"""' in sentence:
                if index == 0:
                    if len(sentences) == 1:
                        fixed_sentences.append(sentence)
                        continue
                    randoms = ["Firstly", "First of all", "At the start", "Initially"]
                    random_value = random.randint(0, len(randoms) - 1)
                    sentence = f'{sentence[0:4]}{randoms[random_value]} {sentence[4].lower()}{sentence[5:]}. '
                else:
                    randoms = ["Finally", "Lastly", "In conclusion", "To conclude", "At the end", "At last",
                               "Conclusively"]
                    random_value = random.randint(0, len(randoms) - 1)
                    sentence = f'{randoms[random_value]} {sentence[0].lower()}{sentence[1:]} '
                fixed_sentences.append(sentence)
                continue
            sentence_end = self.random_sentence_end()
            if index == len(sentences) - 2:
                sentence_end = '. '
            sentence += sentence_end
            if should_lower:
                sentence = sentence[0].lower() + sentence[1:]
            fixed_sentences.append(sentence)
            should_lower = (sentence_end != '. ')

        return ''.join(fixed_sentences)

    @staticmethod
    def apply_backspace(s):
        while True:
            # if you find a character followed by a backspace, remove both
            t = re.sub('.\b', '', s, count=1)
            if len(s) == len(t):
                # now remove any backspaces from beginning of string
                return re.sub('\b+', '', t)
            s = t

    def line_break_comment(self, text: str):
        text = self.apply_backspace(text)
        words = text.split()  # Split the text into individual words
        lines = []
        current_line = ''

        for word in words:
            if word == '"""':
                continue
            if word == 'Raises:':
                # Bunu yaptığımız için bütün yazılım camiasından özür diliyoruz.
                break
            if len(current_line) + len(word) <= 120:
                current_line += word + " "  # Add the word to the current line
            else:
                lines.append(current_line.strip())  # Add the current line to the list of lines
                current_line = word + " "  # Start a new line with the current word

        lines.insert(0, '"""')
        lines.append(current_line.strip())  # Add the last line to the list of lines
        # Bunu yaptığımız için bütün yazılım camiasından özür diliyoruz.
        if self._exceptions != "\nRaises:":
            lines.append(self._exceptions) # Add the last line to the list of lines
        lines.append('"""')
        comment = "\n".join(lines)  # Join the lines with line breaks
        return self.apply_backspace(comment)


    def run_all_comment_functions(self, line):
        # Order of these function calls matter, for one above the if, we should put a dot after its comment.
        comment = ""
        comment += self.comment_loop(line)
        comment += self.comment_match(line)
        comment += self.comment_if(line)
        comment += self.comment_with_statement(line)
        comment += self.comment_try_except(line)
        # if comment:
        #     comment = comment[:-1] + ". "
        comment += self.comment_normal_line(line)
        if not comment:
            return "\b"
        self.check_for_assignment_flag(line)
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
                return f'{statement.attr}'

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
                        end_range = self.stringify_statement(statement.args[1])
                        if end_range.isnumeric():
                            end_range = int(end_range) - 1
                            comment = f'{self.stringify_statement(statement.args[0])} to {end_range}'
                        else:
                            comment = f'{self.stringify_statement(statement.args[0])} until {end_range}'
                        if len(statement.args) == 3:
                            comment = f'{comment} with steps of {self.stringify_statement(statement.args[2])}'
                        return comment
                # for arg in statement.args:
                #     right_side += str(self.stringify_statement(arg)) + ", "
                # right_side = right_side.rstrip(', ')
                # return f'{self.stringify_statement(statement.func)}({right_side})'
                return f'{self.stringify_statement(statement.func)}'

            case 'ListComp' | 'GeneratorExp' | 'DictComp' | 'SetComp':
                return f'values {self.stringify_statement(statement.generators[0].iter)}'

            case 'UnaryOp':
                return f'{self.python_ast.handle_operators(statement.op)} {self.stringify_statement(statement.operand)}'

        return f"{left_side} {operator} {right_side}"

    def comment_import_statements(self, statements):
        try:
            comment = '"""\n'
            for statement in statements:
                if type(statement).__name__ not in ['Import', 'ImportFrom']:
                    break
                if type(statement).__name__ == 'Import':
                    for name in statement.names:
                        self.web_scraper.query = name.name
                        comment += f'{name.name}: {self.web_scraper.search_google()[0].get("link")}\n'
                elif type(statement).__name__ == 'ImportFrom':
                    for name in statement.names:
                        self.web_scraper.query = f'{statement.module}.{name.name}'
                        print(self.web_scraper.query)
                        try:
                            comment += f'{name.name}: {self.web_scraper.search_google()[0].get("link")}\n'
                        except Exception as exc:
                            comment += f'{name.name}: []\n'
            comment = comment.rstrip('\n')
            comment += '\n"""'
            print(comment)
            if comment == '"""\n\n"""':
                return ''
            return comment

        except Exception as exc:
            print(f'Web scraping failed {exc=}')
            return ''

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
                # TODO: iterator ile içerideki ifade aynı mı değil mi bakmak lazım.
                # Iterates for each element in list and prints them
                return f'Iterates from {self.stringify_statement(statement.iter)} and prints each value '
            # comment = f'Iterates {self.stringify_statement(statement.target)} from {self.stringify_statement(statement.iter)}: {inner_statement}'
            comment = f'In a for loop: {inner_statement}'
            return comment
        if type(statement).__name__ == 'While':
            # comment = f'Loops while {self.stringify_statement(statement.test)}: {self.comment_inner_statements(statement.body)}'
            comment = f'In a while loop: {self.comment_inner_statements(statement.body)}'
            return comment
        return ''

    def comment_if(self, statement):
        comment = ''
        if type(statement).__name__ == 'If':
            comment = self._if_comments_list[self._if_index].format(condition=self.stringify_statement(statement.test), body=self.comment_inner_statements(statement.body).rstrip(), conjunction=self._conjunctions[self._conjunction_accumulator])
            self._if_index = self.update_circular_index(self._if_index, self._if_comments_list)
            self._conjunction_accumulator = self.update_circular_index(self._conjunction_accumulator, self._conjunctions)

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
                    comment += f'matches {matches_value}: {self.comment_inner_statements(match_case.body)} or '
                else:
                    comment += f'by default: {self.comment_inner_statements(match_case.body)} or '
            comment = comment.rstrip('or ')
            return comment
        return ''

    def comment_normal_line(self, statement):
        # TODO: Remove parenthesis around assignment tuples.
        if type(statement).__name__ == 'Assign':
            if type(statement.value).__name__ in ['Constant', 'Name']:
                return ''
            if self._assignment_flag == 'Assign':
                return f'\b\b, {self.stringify_statement(statement.targets[0])} '
            random_assignment_prefixes = ['Sets', 'Assigns', 'Initializes', 'Declares', 'Defines']
            random_assignment_prefix = random.choice(random_assignment_prefixes)
            return f'{random_assignment_prefix} {self.stringify_statement(statement.targets[0])} '
        if type(statement).__name__ == 'Expr':
            if type(statement.value).__name__ == 'Call':
                if hasattr(statement.value.func, 'id') and statement.value.func.id == 'print' and len(statement.value.args) < 1:
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
        elif type(statement).__name__ == 'Raise':
            self._exceptions += f'\n    {self.stringify_statement(statement.exc)}'
            # TODO: Her satırı commentlemeyi bıraktığımızda burası da kalkacak.
            return f'Raises {self.stringify_statement(statement.exc)}'
        return ''

    def comment_inner_statements(self, statement_body):
        inner_comments = []
        only_constant_assignment = True
        self._assignment_flag = 'None'

        for inner_statement in statement_body:
            if type(inner_statement).__name__ != 'Assign' or type(inner_statement.value).__name__ not in ['Constant', 'Name']:
                only_constant_assignment = False
                break

        if only_constant_assignment:
            for inner_statement in statement_body:
                if self._assignment_flag == 'BasicAssign':
                    current_comment = f'{self.stringify_statement(inner_statement.value)} to {self.stringify_statement(inner_statement.targets[0])} '
                else:
                    current_comment = f'assigns {self.stringify_statement(inner_statement.value)} to {self.stringify_statement(inner_statement.targets[0])} '
                inner_comments.append(current_comment)
                self.check_for_assignment_flag(inner_statement)
            comment = '\b, '.join(map(str, inner_comments))
            return comment.rstrip('\b, ')

        for inner_statement in statement_body:
            current_statement = self.run_all_comment_functions(inner_statement)
            self.check_for_assignment_flag(inner_statement)
            if not current_statement:
                continue
            inner_comments.append(current_statement)
        comment = '\b, '.join(map(str, inner_comments))
        return comment.rstrip('\b, ')

    @staticmethod
    def function_name_parser(function_name: str) -> tuple[list[str], bool]:
        function_name = re.sub(r'(?<!^)(?=[A-Z])', '_', function_name).lower()
        function_verbs_list = function_name.split('_')
        return function_verbs_list, function_verbs_list[0] in verbs.verbs

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
                if len(function_names) == 1:
                    if len(call_statement.args):
                        # İçerisinde parametre varsa on diyoruz
                        return f'{function_names[0]}s on {call_statement.func.value.id} '
                    # No parameter
                    return f'{function_names[0]}s the {call_statement.func.value.id} '
                prefix = '\b\b, ' if function_names[0] == self._assignment_flag else f'{function_names[0]}s '
                return f'{prefix}{" ".join(function_names[1:])} '

        elif type(call_statement.func).__name__ ==  'Name':
            function_names, is_common_name = self.function_name_parser(call_statement.func.id)

            if is_common_name:
                # print() || printLines() || print('1', '2', '3')
                if len(function_names) == 1:
                    if len(call_statement.args) >= 1:
                        args_comment = ''
                        for arg in call_statement.args:
                            args_comment += self.stringify_statement(arg) + ', '
                        if len(args_comment) <= 30:
                            return f'{function_names[0]}s {args_comment.rstrip(", ")} '
                    return f'{function_names[0]}s the argument(s) '
                return f'{function_names[0]}s {" ".join(function_names[1:])} '

        if self._assignment_flag == "Call":
            # TODO: Calls filledCircle, filledCircle, filledCircle => Calls filledCircle 3 times
            #  self._call_number += 1
            if type(call_statement.func).__name__ == 'Attribute':
                return f'\b\b, {call_statement.func.attr} '
            return f'\b\b, {call_statement.func.id} '

        if type(call_statement.func).__name__ ==  'Attribute':
            return f'Calls {call_statement.func.attr} '
        return f'Calls {call_statement.func.id} '

    def comment_with_statement(self, statement):
        comment = ''
        if type(statement).__name__ == 'With':
            for index, item in enumerate(statement.items):
                comment = comment.replace(' and ', ', ')
                if type(item.context_expr).__name__ == 'Call':
                    if item.context_expr.func.id == 'open':
                        call_statement = item.context_expr
                        comment += f'opens {call_statement.args[0].value} as {item.optional_vars.id} and '
                    else:
                        # func geldiyse: Creating an instance of {HelloContextManager}
                        comment += f'creates an instance of {item.context_expr.func.id} and '
                else:
                    #  Use the {SQL connector} as a context manager.
                    comment += f'uses the {item.context_expr.id} as a context manager and '
                if index == 0:
                    comment = comment[0].upper() + comment[1:]

            comment += self.comment_inner_statements(statement.body)
        return comment

    def comment_try_except(self, statement):
        comment = ''
        if type(statement).__name__ == 'Try':
            comment += self.comment_body(statement.body)
            if len(statement.handlers):
                errors_list = [', while checking for ', ', while looking for ', ', while catching ', ', while handling ',
                               ', checking for ', ', looking for ', ', catching ', ', handling ']
                rng = random.randint(0, len(errors_list) - 1)
                comment = f'{comment.rstrip(". ")}{errors_list[rng]}'
                for handler in statement.handlers:
                    comment += f'{handler.type.id}, '
                    self.comment_body(handler.body)
            comment = f'{comment.rstrip(", ")} error{"s" if len(statement.handlers) > 1 else ""}. '
            if len(statement.orelse):
                comment += f'If no errors were found; {self.comment_body(statement.orelse)}'
            if len(statement.finalbody):
                comment += f'Finally {self.comment_body(statement.finalbody)[0].lower()}{self.comment_body(statement.finalbody)[1:]}'
        return comment.rstrip('. ')

    def comment_body(self, body):
        comment = ''
        for statement in body:
            line_comment = self.run_all_comment_functions(statement).rstrip() + '. '
            comment += line_comment[0].upper() + line_comment[1:]
            self.check_for_assignment_flag(statement)
        return comment


    def check_for_assignment_flag(self, statement):
        if type(statement).__name__ == 'Assign' and not type(statement.value).__name__ in ['Constant', 'Name']:
            self._assignment_flag = 'Assign'
        elif type(statement).__name__ == 'Assign' and type(statement.value).__name__ in ['Constant', 'Name']:
            self._assignment_flag = 'BasicAssign'
        elif type(statement).__name__ == 'Expr':
            if type(statement.value).__name__ == 'Call':
                is_common_name = False
                if type(statement.value.func).__name__ == 'Attribute':
                    function_name, is_common_name = self.function_name_parser(statement.value.func.attr)
                elif type(statement.value.func).__name__ == 'Name':
                    function_name, is_common_name = self.function_name_parser(statement.value.func.id)
                if is_common_name:
                    self._assignment_flag = f'{function_name[0]}'
                else:
                    self._assignment_flag = 'Call'
        else:
            self._assignment_flag = 'None'

    # TODO: For-If bağlantısı (for'un içinde if varsa)
    # TODO: Pauses the parameters on StdDraw
    # TODO: Web scraping??? (BeautifulSoup) (Most common functions json oluşturup oradan arama yapılabilir son çare olarak)
    # TODO: Commenting every source code file in a directory -> 3 Method: VSCode, Command Line, Web UI (Zip)
    # TODO: Parametreler ve return value'lar handled değil
    # TODO: Abstract methodlar handled değil (Optional: Body'si boşsa case'i)
