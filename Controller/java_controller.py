import re
from dataclasses import dataclass, field

from Controller.base_controller import BaseController
from Controller.report_controller import ReportController
from Models.SourceCode.java_ast import JavaAST
from Models.java_function import JavaFunction
from Utils.character_manipulation import CharacterManipulation


@dataclass
class JavaController(BaseController):
    last_expr: str = field(init=False, default_factory=str)
    comment: str = field(init=False, default_factory=str)
    function_count: int = field(init=False, default=0)
    field_count: int = field(init=False, default=0)
    inherits_from: str = field(init=False, default_factory=str)
    implements: list = field(init=False, default_factory=list)
    java_function = None
    backspace_char = "\b"
    def __post_init__(self):
        super().__post_init__()
        self.java_ast = JavaAST(self.source_code_string)
        self.types = self.get_ast().types[0]
        self.members = self.get_ast().types[0].body

    def comment(self):
        if self.types.extends:
            self.inherits_from = self.types.extends.name
        if self.types.implements:
            self.implements = [implement.name for implement in self.types.implements]
        for member in self.members:
            if type(member).__name__ == "MethodDeclaration":
                self.java_function = JavaFunction(member)
                self.comment_function_based_on_name()
            if type(member).__name__ == "FieldDeclaration":
                self.field_count += len(member.declarators)
        return self.generate_comment_for_class()

    def generate_comment_for_class(self):
        inherit_string = f"\n* Inherits from {self.inherits_from}" if self.inherits_from else ""
        implements_string = f"\n* Implements {', '.join(map(str, self.implements))}" if self.implements else ""

        class_comment = f"/**\n* {self.types.name}{inherit_string}{implements_string}\n* " \
                        f"Has {self.function_count} method(s)" \
                        f"\n* Has {self.field_count} attribute(s)\n*/"
        self.source_code_string = self.add_class_comment_to_source_code(class_comment)

    def comment_function(self, alternative_comment=""):
        self.comment = f"/**\n\t* "
        self.append_alternative_comment(alternative_comment)
        for line in self.java_function.function_tree.body:
            self.java_function.get_variable_names_where_params_are_used(line)
            line_comment = self.run_all_comment_functions(line, self.java_function) + "\b. "
            self.comment += line_comment[0].upper() + line_comment[1:]

        params_comment = self.generate_params_comment()
        self.comment += f"{params_comment}"
        self.comment += f"\n\t*/"
        self.comment = CharacterManipulation.apply_backspace(self.comment)
        self.comment = CharacterManipulation.line_break_comment(self.comment)
        return self.comment

    def append_alternative_comment(self, alternative_comment):
        if alternative_comment:
            self.comment += alternative_comment

    def generate_params_comment(self):
        params_comment = "\n\t*" if self.java_function.params else ""
        for param in self.java_function.params:
            params_comment += f"\n\t* @param {param}{self.get_param_comment(param)}"
        return params_comment

    def get_param_comment(self, param):
        if self.java_function.params_used.get(param):
            return f' is used to find {", ".join(map(str, self.java_function.params_used.get(param)))}'
        return f' is used to find {""}'

    def comment_function_based_on_name(self):
        if self.java_function.function_name == "main":
            self.comment = self.comment_function("Main function")
        elif (self.java_function.function_name.startswith("get")
              or self.java_function.function_name.startswith("set")) \
                and len(self.java_function.function_tree.body) == 1:
            self.comment = self.comment_get_set_functions()
        else:
            self.comment = self.comment_function()
        self.source_code_string = self.add_function_comments_to_source_code()
        self.function_count += 1

    # TODO: Remove this
    def comment_get_set_functions(self):
        return self.comment_function(alternative_comment=f"{self.java_function.function_name[0:3].capitalize()}s "
                                     f"the {self.java_function.function_name[3:]}")


    def get_single_line_comments(self) -> list:
        """ Returns single line comments """
        single_line_comments_list = re.findall(
            "(?://[^\n]*|/\*(?:(?!\*/).)*\*/)", self.java_ast.source_code_string
        )
        return single_line_comments_list

    def get_multi_line_comments(self) -> list:
        """ Returns multi line comments """
        multi_line_comments_list = (
            re.findall(
                "(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)",
                self.java_ast.source_code_string,
            )
        )
        return multi_line_comments_list

    def get_doc_comments(self) -> list:
        """ Returns doc comments """
        doc_comments_list = (
            re.findall(
                "(/\*\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)",
                self.java_ast.source_code_string,
            )
        )
        return doc_comments_list

    def get_return_value(self):
        return self.java_ast.get_return_value()

    def generate_report(self):
        report_controller = ReportController(self.writer, self)
        report_controller.generate_report()

    def write_ast_to_file(self):
        self.java_ast.write_ast_to_file()

    def get_ast(self):
        return self.java_ast.generate_ast()

    @property
    def members(self):
        return self.get_ast().types[0].body

    @members.setter
    def members(self, members):
        self.members = members

    @property
    def types(self):
        return self.get_ast().types[0]

    @types.setter
    def types(self, types):
        self.types = types

    def case_comment(self, statement):
        # Order of these function calls matter, for one above the if, we should put a dot after its comment.
        self.comment += self.comment_loop(statement)
        if type(statement).__name__ == "SwitchStatement":
            self.comment += self.comment_switch(statement)
        if type(statement).__name__ == "IfStatement":
            self.comment += self.comment_if(statement)
        self.comment += self.comment_super(statement)
        self.comment += self.comment_normal_line(statement)
        if not self.comment:
            return "\b"
        return self.comment[0].lower() + self.comment[1:]

    def generate_comment_from_function_name(self):
        list_of_function_names = self.java_ast.get_list_of_function_names()
        list_of_generated_comments = [self.name_analyzer.get_generated_comments_list(function_name)
                                      for function_name in list_of_function_names]
        return list_of_generated_comments

    def comment_if(self, statement):
        self.last_expr = ""
        return self.create_if_comment(statement)

    def create_if_comment(self, statement, first_statement=True):
        comment = ""
        comments = []
        inner_comments = []
        conditions = []
        else_exists = False
        if type(statement).__name__ == "IfStatement":
            conditions.append(self.java_ast.stringify_statement(statement.condition))

            for inner_statement in statement.then_statement.statements:
                inner_comments.append(self.case_comment(inner_statement))
                comments.append(inner_comments)
                self.java_function.get_variable_names_where_params_are_used(inner_statement)

            if statement.else_statement:
                condition, else_exists, inner_comment = self.create_if_comment(statement.else_statement, False)
                conditions.extend(condition)
                comments.extend(inner_comment)

        if type(statement).__name__ == "BlockStatement":
            for inner_statement in statement.statements:
                inner_comments.append(self.case_comment(inner_statement))
                comments.append(inner_comments)
                self.java_function.get_variable_names_where_params_are_used(inner_statement)
            return conditions, True, comments
        if not first_statement:
            return conditions, else_exists, comments
        or_else = " or else, " if else_exists else ", "
        comment = f"Checks if "
        for index, condition in enumerate(conditions):
            comment += f"{'' if index == 0 else 'or if '}{condition}: and " \
                       f"{f'{self.backspace_char}, '.join(map(str, comments[index]))}{self.backspace_char}; "
        if else_exists:
            comment += f"else: {f'{self.backspace_char}, '.join(map(str, comments[-1]))}"
        else:
            comment += f"\b\b "
        return comment

    def comment_loop(self, statement):
        inner_comments = []
        if type(statement).__name__ == "ForStatement":
            self.last_expr = ""
            iter_condition = self.java_ast.stringify_statement(statement.control.condition)
            iter_declaration = self.java_ast.stringify_statement(statement.control.init)
            comment = f"Iterates from {iter_declaration} until {iter_condition} is false: "
            for inner_statement in statement.body.statements:
                inner_comments.append(run_all_comment_functions(inner_statement))
                self.java_function.get_variable_names_where_params_are_used(inner_statement)
            comment += '\b, '.join(map(str, inner_comments))
            return comment
        elif type(statement).__name__ == "WhileStatement":
            self.last_expr = ""
            iter_condition = self.java_ast.stringify_statement(statement.condition)
            comment = f"Loops while {iter_condition}: "
            for inner_statement in statement.body.statements:
                inner_comments.append(run_all_comment_functions(inner_statement))
                self.java_function.get_variable_names_where_params_are_used(inner_statement)
            comment += '\b, '.join(map(str, inner_comments))
            return comment
        return ""

    def comment_switch(self, statement):
        self.last_expr = ""
        first_case = True
        expression = self.java_ast.stringify_statement(statement.expression)
        case_comment = f"If the value of {expression}"
        for switch_case in statement.cases:
            if switch_case.case:
                case_comment += f"{'' if first_case else 'or'} " \
                                f"matches {self.java_ast.stringify_statement(switch_case.case[0])}: "
                for inner_statement in switch_case.statements:
                    case_comment += self.case_comment(inner_statement)
                    self.java_function.get_variable_names_where_params_are_used(inner_statement)
                case_comment += "\b; "
                first_case = False
            else:
                case_comment += f"or by default, "
                for inner_statement in switch_case.statements:
                    case_comment += self.case_comment(inner_statement)
                    self.java_function.get_variable_names_where_params_are_used(inner_statement)
        return case_comment

    def comment_super(self, statement):
        if type(statement).__name__ == "StatementExpression":
            if type(statement.expression).__name__ == "SuperMethodInvocation":
                self.last_expr = ""
                super_function = statement.expression.member
                return f"Calls parent's {super_function} method "
        return ""

    def comment_normal_line(self, statement):
        if type(statement).__name__ == "StatementExpression":
            if type(statement.expression).__name__ == "MethodInvocation":
                self.comment_method_invocation(statement.expression)
            if type(statement.expression).__name__ == "Assignment":
                self.comment_assignment_operation(statement.expression)
            if type(statement.expression).__name__ == "MemberReference":
                self.last_expr = "MemberReference"
                if statement.expression.postfix_operators[0] == "++" \
                        or statement.expression.prefix_operators[0] == "++":
                    return f"Increments the {statement.expression.member} "
                if statement.expression.postfix_operators[0] == "--" \
                        or statement.expression.prefix_operators[0] == "--":
                    return f"Decrements the {statement.expression.member} "
        if type(statement).__name__ == "ReturnStatement":
            self.last_expr = "ReturnStatement"
            return f"Returns {self.java_ast.stringify_statement(statement.expression)} "
        if type(statement).__name__ == "LocalVariableDeclaration":
            self.comment_local_variable_declaration(statement)
        return ""

    def comment_assignment_operation(self, statement_expression):
        self.last_expr = "Assignment"
        expression_value = self.java_ast.stringify_statement(statement_expression.value)
        left_side = self.java_ast.stringify_statement(statement_expression.expressionl)
        match statement_expression.type:
            case "+=":
                return f"Increments {left_side} by {expression_value} "
            case "-=":
                return f"Subtracts {expression_value}from {left_side} "
            case "*=":
                return f"Multiplies {left_side} by {expression_value} "
            case "/=":
                return f"Divides {left_side} by {expression_value} "
            case "%=":
                return f"Updates the value of {left_side} by taking its modulus with {expression_value} "
            case "=":
                return f"Assigns {expression_value} to {left_side} "

    def comment_method_invocation(self, statement_expression):
        if statement_expression.member == "println" or statement_expression.member == "print":
            comment = f"Prints {self.java_ast.stringify_statement(statement_expression.arguments[0])} to the console "
            self.last_expr = "MethodInvocationPrint"
        else:
            if self.last_expr == "MethodInvocation":
                comment = f"\b\b, {statement_expression.member} method "
            else:
                comment = f"Calls the {statement_expression.member} method "
                self.last_expr = "MethodInvocation"
        return comment

    def comment_local_variable_declaration(self, statement):
        if self.last_expr == "LocalVariableDeclaration":
            comment = f"\b\b, {statement.declarators[0].name} with " \
                      f"{self.java_ast.stringify_statement(statement.declarators[0].initializer)} "
        else:
            comment = f"Initializes {statement.declarators[0].name} with " \
                      f"{self.java_ast.stringify_statement(statement.declarators[0].initializer)} "
        self.last_expr = "LocalVariableDeclaration"
        return comment
