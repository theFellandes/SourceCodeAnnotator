from Controller.java_controller import JavaController
import re


def main():
    controller = JavaController("FibonacciForLoop.java")
    cu = controller.get_ast()
    print(cu)
    members = cu.types[0].body
    function_count = 0
    field_count = 0
    inherits_from = ""
    implements = []

    if cu.types[0].extends:
        inherits_from = cu.types[0].extends.name
    if cu.types[0].implements:
        for implement in cu.types[0].implements:
            implements.append(implement.name)

    for member in members:
        if type(member).__name__ == "MethodDeclaration":
            java_function = JavaFunction(member)
            comment = comment_function(java_function)
            # print(comment)
            controller.source_code_string = add_function_comments_to_source_code(controller.source_code_string, comment, java_function)
            function_count += 1
        if type(member).__name__ == "FieldDeclaration":
            field_count += len(member.declarators)

    inherit_string = f"\n* Inherits from {inherits_from}" if inherits_from else ""
    implements_string = f"\n* Implements {', '.join(map(str, implements))}" if implements else ""

    class_comment = f"/**\n* {cu.types[0].name}{inherit_string}{implements_string}\n* Has {function_count} method(s)" \
                    f"\n* Has {field_count} attribute(s)\n*/"
    controller.source_code_string = add_class_comment_to_source_code(controller.source_code_string, class_comment)
    # print(class_comment)


# function = JavaFunction(cu.types[0].body[1])
    # method = cu.types[0].body[2]
    # print(method, "\n\n")
    # comment_return(method)
    # for statement_type in method.body:
    #     if type(statement_type).__name__ == "ReturnStatement":
    #         print(type(statement_type.expression).__name__)


def comment_function(java_function):
    comment = f"/**\n\t* "
    for line in java_function.function_tree.body:
        java_function.get_variable_names_where_params_are_used(line)
        comment += comment_super(line)
        comment += comment_loop(line)
        comment += comment_switch(line)
        comment += comment_if(line)
    params_comment = "\n\t*" if java_function.params_used.items() else ""
    for param, used_variables in java_function.params_used.items():
        params_comment += f"\n\t* @param {param} is used to find {', '.join(map(str, used_variables))}"
    comment += f"{params_comment}\n\t*/"
    comment = line_break_comment(comment)
    return comment


def line_break_comment(comment):
    last_space_index = 0
    current_index = 8
    while current_index < len(comment):
        if comment[current_index] == " ":
            last_space_index = current_index
        if (current_index - 5) % 80 == 0:
            comment = comment[:last_space_index - 1] + "\n\t* " + comment[last_space_index + 1:]
            current_index = last_space_index + 3
        current_index += 1
        if comment[current_index:current_index + 5] == "\n\t* @":
            break
    return comment


def add_function_comments_to_source_code(source_code, comment, function):
    modifiers_regex = f"(({'|'.join(map(str, function.modifiers))})[ ]+){{{len(function.modifiers)}}}"
    parameters_regex = fr"\([ ]*"
    for param, param_type in zip(function.params, function.param_types):
        parameters_regex += f"{param_type}[ ]+{param}[ ]*,[ ]*"
    parameters_regex = parameters_regex[:-5] + fr"\)"
    regex = fr"{modifiers_regex}{function.return_type}[ ]+{function.function_name}[ ]*{parameters_regex}"
    match_object = re.search(regex, source_code)
    source_code = source_code[:match_object.span()[0]] + f"{comment}\n\t" \
                                                       + source_code[match_object.span()[0]:match_object.span()[1]] \
                                                       + source_code[match_object.span()[1]:]
    return source_code


def add_class_comment_to_source_code(source_code, comment):
    class_regex = f"((public|final|abstract)[ ]+){{0,2}}class"
    match_object = re.search(class_regex, source_code)
    source_code = source_code[:match_object.span()[0]] + f"{comment}\n" \
                  + source_code[match_object.span()[0]:match_object.span()[1]] \
                  + source_code[match_object.span()[1]:]
    print(source_code)
    return source_code


class JavaFunction:
    def __init__(self, function_tree):
        self.function_tree = function_tree
        self.function_name = ""
        self.params = []
        self.param_types = []
        self.modifiers = self.function_tree.modifiers
        self.return_type = self.return_type = self.function_tree.return_type.name if self.function_tree.return_type else "void"
        self.params_used = {}
        self.get_param_names()
        self.get_function_name()

    def get_param_names(self):
        for param in self.function_tree.parameters:
            self.params.append(param.name)
            self.param_types.append(param.type.name)

    def get_function_name(self):
        self.function_name = self.function_tree.name

    def generate_comment(self):
        pass

    def get_variable_names_where_params_are_used(self, expression):
        variables_used = []
        if type(expression).__name__ == "LocalVariableDeclaration":
            initializer = expression.declarators[0].initializer

            if type(initializer).__name__ == "BinaryOperation":
                variables_used = get_variables_used_in_binary_operation(expression.declarators[0].initializer)

            for param in self.params:
                if get_name_or_value(initializer, True) == param or param in variables_used:
                    if param not in self.params_used:
                        self.params_used[param] = [expression.declarators[0].name]
                    if expression.declarators[0].name not in self.params_used[param]:
                        self.params_used[param].append(expression.declarators[0].name)
        elif type(expression).__name__ == "StatementExpression" and type(expression.expression).__name__ == "Assignment":
            assignee = expression.expression.expressionl.member
            variables_used = get_variables_used_in_assignment_expression(expression)
            for param in self.params:
                if param in variables_used:
                    if param not in self.params_used:
                        self.params_used[param] = [assignee]
                    if assignee not in self.params_used[param]:
                        self.params_used[param].append(assignee)


def comment_return(method):
    for statement_type in method.body:
        if type(statement_type).__name__ == "ReturnStatement":
            print(f"Returns {stringify_statement(statement_type.expression)}")


def get_name_or_value(variable_or_literal, only_get_if_variable=False):
    if type(variable_or_literal).__name__ == "MemberReference":
        return variable_or_literal.member
    if type(variable_or_literal).__name__ == "Literal" and not only_get_if_variable:
        return variable_or_literal.value


def get_variables_used_in_binary_operation(expression):
    variables = []
    if type(expression).__name__ == "BinaryOperation":
        variables.extend(get_variables_used_in_binary_operation(expression.operandl))
        variables.extend(get_variables_used_in_binary_operation(expression.operandr))
    elif type(expression).__name__ == "MemberReference":
        return [expression.member]
    return variables


def get_variables_used_in_assignment_expression(expression):
    variables = []
    value = expression.expression.value
    if type(value).__name__ == "BinaryOperation":
        variables.extend(get_variables_used_in_binary_operation(value))
    elif type(value).__name__ == "MemberReference":
        return [value.member]
    return variables


def comment_loop(statement):
    if type(statement).__name__ == "ForStatement":
        iter_condition = stringify_statement(statement.control.condition)
        iter_declaration = stringify_statement(statement.control.init)
        return f"Iterates from {iter_declaration} until {iter_condition} is false, "
    elif type(statement).__name__ == "WhileStatement":
        iter_condition = stringify_statement(statement.condition)
        return f"Loops while {iter_condition}, "
    return ""


def stringify_statement(statement):
    left_side = ""
    right_side = ""
    operator = ""
    if type(statement).__name__ == "VariableDeclaration":
        left_side = statement.declarators[0].name
        right_side = stringify_statement(statement.declarators[0].initializer)
        operator = "="
    if type(statement).__name__ == "BinaryOperation":
        left_side = stringify_statement(statement.operandl)
        right_side = stringify_statement(statement.operandr)
        operator = statement.operator
    elif type(statement).__name__ == "MemberReference":
        return statement.member
    elif type(statement).__name__ == "Literal":
        return statement.value
    return f"{left_side} {operator} {right_side}"


def comment_if(statement):
    if type(statement).__name__ != "IfStatement":
        return ""
    return create_if_comment(statement)


def create_if_comment(statement, first_statement=True):
    conditions = []
    else_exists = False
    if type(statement).__name__ == "IfStatement":
        conditions.append(stringify_statement(statement.condition))
        if statement.else_statement:
            condition, else_exists = create_if_comment(statement.else_statement, False)
            conditions.extend(condition)

    if type(statement).__name__ == "BlockStatement":
        return conditions, True
    if not first_statement:
        return conditions, else_exists
    or_else = " or else, " if else_exists else ", "
    return f"Checks if {', '.join(map(str, conditions)) + or_else}"


# TODO: Change the switch comment
def comment_switch(statement):
    if type(statement).__name__ == "SwitchStatement":
        expression = stringify_statement(statement.expression)
        case_comment = ""
        for switch_case in statement.cases:
            if switch_case.case:
                case_comment += f"If the value of {expression} matches {stringify_statement(switch_case.case[0])}, "
            else:
                case_comment += f"Else "
        return case_comment
    return ""


def comment_super(statement):
    if type(statement).__name__ == "StatementExpression":
        if type(statement.expression).__name__ == "SuperMethodInvocation":
            super_function = statement.expression.member
            return f"Calls parent's {super_function} function."
    return ""


if __name__ == "__main__":
    main()

# TODO: Use a different comment for switch statement (If the value of nthFibonacciNumber matches 0, or matches 0 && 1)
# TODO: Commenting statements' bodies (loop, if, switch)
# TODO: ChatGPT communication.
# TODO: Recursive function commenting (so complicated)
# TODO: Web Crawling
