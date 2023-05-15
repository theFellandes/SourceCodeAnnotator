from Controller.java_controller import JavaController
import re


LAST_EXPR = ""
B = "\b"


def lazydoc_entry_point(controller: JavaController):
    cu = controller.get_ast()
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
            if java_function.function_name == "main_CHANGE_HERE_IF_YOU_WANT_TO_RESTORE_SKIPPING_MAIN":
                comment = comment_function(java_function, "Main function.")
            elif (java_function.function_name.startswith("get") or java_function.function_name.startswith("set")) \
                    and len(java_function.function_tree.body) == 1:
                comment = comment_get_set_functions(java_function)
            else:
                comment = comment_function(java_function)

            controller.source_code_string = add_function_comments_to_source_code(controller.source_code_string, comment,
                                                                                 java_function)
            function_count += 1
        if type(member).__name__ == "FieldDeclaration":
            field_count += len(member.declarators)

    inherit_string = f"\n* Inherits from {inherits_from}" if inherits_from else ""
    implements_string = f"\n* Implements {', '.join(map(str, implements))}" if implements else ""

    class_comment = f"/**\n* {cu.types[0].name}{inherit_string}{implements_string}\n* Has {function_count} method(s)" \
                    f"\n* Has {field_count} attribute(s)\n*/"
    controller.source_code_string = add_class_comment_to_source_code(controller.source_code_string, class_comment)
    return controller.source_code_string


def main():
    controller = JavaController("complex/reversed.java")
    cu = controller.get_ast()
    print(cu)
    lazydoc_entry_point(controller)


def comment_function(java_function, alternative_comment=""):
    comment = f"/**\n\t* "
    if alternative_comment:
        comment += alternative_comment
    else:
        for line in java_function.function_tree.body:
            java_function.get_variable_names_where_params_are_used(line)
            line_comment = run_all_comment_functions(line, java_function) + "\b. "
            comment += line_comment[0].upper() + line_comment[1:]
        params_comment = "\n\t*" if java_function.params else ""
        for param in java_function.params:
            params_comment += f"\n\t* @param {param}{' is used to find ' + ', '.join(map(str, java_function.params_used.get(param))) if java_function.params_used.get(param) else ''}"
        comment += f"{params_comment}"
    comment += f"\n\t*/"
    comment = apply_backspace(comment)
    comment = line_break_comment(comment)
    return comment


def comment_get_set_functions(java_function):
    return comment_function(java_function, f"{java_function.function_name[0:3].capitalize()}s the {java_function.function_name[3:]}")


def run_all_comment_functions(line, java_function):
    # Order of these function calls matter, for one above the if, we should put a dot after its comment.
    comment = ""
    comment += comment_loop(line, java_function)
    comment += comment_switch(line, java_function)
    comment += comment_if(line, java_function)
    # if comment:
    #     comment = comment[:-1] + ". "
    comment += comment_super(line)
    comment += comment_normal_line(line)
    if not comment:
        return "\b"
    return comment[0].lower() + comment[1:]


def line_break_comment(comment):
    current_index = 9
    line_start_index = 8
    last_space_index = 0
    while current_index < len(comment):
        if comment[current_index] == " ":
            last_space_index = current_index
        if (current_index - line_start_index) % 80 == 0:
            comment = comment[:last_space_index] + "\n\t* " + comment[last_space_index + 1:]
            current_index = last_space_index + 4
            line_start_index = current_index - 1
        current_index += 1
        if comment[current_index:current_index + 5] == "\n\t* @":
            break
    return comment


def add_function_comments_to_source_code(source_code, comment, function):
    modifiers_regex = f"(({'|'.join(map(str, function.modifiers))})[ ]+){{{len(function.modifiers)}}}"
    if function.params:
        parameters_regex = fr"\([ ]*"
        for param, param_type in zip(function.params, function.param_types):
            parameters_regex += fr"{param_type}[ ]*(\[[ ]*\])*(\<([ ]*[^\s]*[ ]*[,]*)+\>)*[ ]+{param}[ ]*,[ ]*"
        parameters_regex = parameters_regex[:-5] + fr"\)"
    else:
        parameters_regex = fr"\([ ]*\)"
    regex = fr"{modifiers_regex}{function.return_type}[ ]*(\[[ ]*\])*[ ]+{function.function_name}[ ]*{parameters_regex}"
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
        self.return_type = self.function_tree.return_type.name if self.function_tree.return_type else "void"
        self.params_used = {}
        self.get_param_names()
        self.get_function_name()

    def get_param_names(self):
        for param in self.function_tree.parameters:
            self.params.append(param.name)
            self.param_types.append(param.type.name)

    def get_function_name(self):
        self.function_name = self.function_tree.name

    def get_variable_names_where_params_are_used(self, expression):
        variables_used = []
        if type(expression).__name__ == "LocalVariableDeclaration":
            initializer = expression.declarators[0].initializer

            if type(initializer).__name__ == "BinaryOperation":
                variables_used.extend(get_variables_used_in_binary_operation(expression.declarators[0].initializer))
            elif type(initializer).__name__ == "MethodInvocation":
                variables_used.extend(get_argument_names(initializer))

            for param in self.params:
                if stringify_statement(initializer) == param or param in variables_used:
                    if param not in self.params_used:
                        self.params_used[param] = [expression.declarators[0].name]
                    if expression.declarators[0].name not in self.params_used[param]:
                        self.params_used[param].append(expression.declarators[0].name)

        elif type(expression).__name__ == "StatementExpression" and type(expression.expression).__name__ == "Assignment":
            assignee = stringify_statement(expression.expression.expressionl)
            variables_used = get_variables_used_in_assignment_expression(expression)
            for param in self.params:
                if param in variables_used:
                    if param not in self.params_used:
                        self.params_used[param] = [assignee]
                    if assignee not in self.params_used[param]:
                        self.params_used[param].append(assignee)


def get_argument_names(method_invocation):
    argument_names = []
    for argument in method_invocation.arguments:
        if type(argument).__name__ == "MethodInvocation":
            argument_names.extend(get_argument_names(argument))
        elif type(argument).__name__ == "MemberReference":
            argument_names.append(argument.member)
    return argument_names


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
    elif type(expression).__name__ == "MethodInvocation":
        return get_argument_names(expression)
    return variables


def get_variables_used_in_assignment_expression(expression):
    variables = []
    value = expression.expression.value
    if type(value).__name__ == "BinaryOperation":
        variables.extend(get_variables_used_in_binary_operation(value))
    elif type(value).__name__ == "MemberReference":
        return [value.member]
    return variables


def comment_loop(statement, java_function):
    global LAST_EXPR
    inner_comments = []
    if type(statement).__name__ == "ForStatement":
        LAST_EXPR = ""
        iter_condition = stringify_statement(statement.control.condition)
        iter_declaration = stringify_statement(statement.control.init)
        comment = f"Iterates from {iter_declaration} until {iter_condition} is false: "
        for inner_statement in statement.body.statements:
            inner_comments.append(run_all_comment_functions(inner_statement, java_function))
            java_function.get_variable_names_where_params_are_used(inner_statement)
        comment += '\b, '.join(map(str, inner_comments))
        return comment
    elif type(statement).__name__ == "WhileStatement":
        LAST_EXPR = ""
        iter_condition = stringify_statement(statement.condition)
        comment = f"Loops while {iter_condition}: "
        for inner_statement in statement.body.statements:
            inner_comments.append(run_all_comment_functions(inner_statement, java_function))
            java_function.get_variable_names_where_params_are_used(inner_statement)
        comment += '\b, '.join(map(str, inner_comments))
        return comment
    return ""


def stringify_statement(statement):
    left_side = ""
    right_side = ""
    operator = ""
    if type(statement).__name__ == "VariableDeclaration":
        left_side = statement.declarators[0].name
        right_side = stringify_statement(statement.declarators[0].initializer)
        operator = "="
    elif type(statement).__name__ == "BinaryOperation":
        left_side = stringify_statement(statement.operandl)
        right_side = stringify_statement(statement.operandr)
        operator = statement.operator
    elif type(statement).__name__ == "MemberReference":
        if statement.selectors:
            selectors_comment = ""
            for selector in statement.selectors:
                selectors_comment += f"[{stringify_statement(selector.index)}]"
            return f"{statement.member}{selectors_comment}"
        return statement.member
    elif type(statement).__name__ == "Literal":
        return statement.value
    elif type(statement).__name__ == "MethodInvocation":
        arguments = []
        for argument in statement.arguments:
            arguments.append(stringify_statement(argument))
        return f"{statement.member}({', '.join(map(str, arguments))})"
    elif type(statement).__name__ == "ArrayCreator":
        string = f"new {statement.type.name}"
        for dimension in statement.dimensions:
            string += f"[{stringify_statement(dimension)}]"
        return string
    elif type(statement).__name__ == "ArrayInitializer":
        initializers = []
        for initializer in statement.initializers:
            initializers.append(stringify_statement(initializer))
        return f"{{{', '.join(map(str, initializers))}}}"
    elif type(statement).__name__ == "Cast":
        return f"({statement.type.name}) {stringify_statement(statement.expression)}"
    return f"{left_side} {operator} {right_side}"


def comment_if(statement, java_function):
    if type(statement).__name__ != "IfStatement":
        return ""
    global LAST_EXPR
    LAST_EXPR = ""
    return create_if_comment(statement, java_function)


def create_if_comment(statement, java_function, first_statement=True):
    comment = ""
    comments = []
    inner_comments = []
    conditions = []
    else_exists = False
    if type(statement).__name__ == "IfStatement":
        conditions.append(stringify_statement(statement.condition))

        for inner_statement in statement.then_statement.statements:
            inner_comments.append(run_all_comment_functions(inner_statement, java_function))
            comments.append(inner_comments)
            java_function.get_variable_names_where_params_are_used(inner_statement)

        if statement.else_statement:
            condition, else_exists, inner_comment = create_if_comment(statement.else_statement, java_function, False)
            conditions.extend(condition)
            comments.extend(inner_comment)

    if type(statement).__name__ == "BlockStatement":
        for inner_statement in statement.statements:
            inner_comments.append(run_all_comment_functions(inner_statement, java_function))
            comments.append(inner_comments)
            java_function.get_variable_names_where_params_are_used(inner_statement)
        return conditions, True, comments
    if not first_statement:
        return conditions, else_exists, comments
    or_else = " or else, " if else_exists else ", "
    comment = f"Checks if "
    for index, condition in enumerate(conditions):
        comment += f"{'' if index == 0 else 'or if '}{condition}: and {f'{B}, '.join(map(str, comments[index]))}{B}; "
    if else_exists:
        comment += f"else: {f'{B}, '.join(map(str, comments[-1]))}"
    else:
        comment += f"\b\b "
    return comment


def comment_switch(statement, java_function):
    if type(statement).__name__ == "SwitchStatement":
        global LAST_EXPR
        LAST_EXPR = ""
        first_case = True
        expression = stringify_statement(statement.expression)
        case_comment = f"If the value of {expression}"
        for switch_case in statement.cases:
            if switch_case.case:
                case_comment += f"{'' if first_case else 'or'} matches {stringify_statement(switch_case.case[0])}: "
                for inner_statement in switch_case.statements:
                    case_comment += run_all_comment_functions(inner_statement, java_function)
                    java_function.get_variable_names_where_params_are_used(inner_statement)
                case_comment += "\b; "
                first_case = False
            else:
                case_comment += f"or by default, "
                for inner_statement in switch_case.statements:
                    case_comment += run_all_comment_functions(inner_statement, java_function)
                    java_function.get_variable_names_where_params_are_used(inner_statement)
        return case_comment
    return ""


def comment_super(statement):
    if type(statement).__name__ == "StatementExpression":
        if type(statement.expression).__name__ == "SuperMethodInvocation":
            global LAST_EXPR
            LAST_EXPR = ""
            super_function = statement.expression.member
            return f"Calls parent's {super_function} method "
    return ""


def comment_normal_line(statement):
    global LAST_EXPR
    if type(statement).__name__ == "StatementExpression":
        if type(statement.expression).__name__ == "MethodInvocation":
            if statement.expression.member == "println" or statement.expression.member == "print":
                comment = f"Prints {stringify_statement(statement.expression.arguments[0])} to the console "
                LAST_EXPR = "MethodInvocationPrint"
            else:
                if LAST_EXPR == "MethodInvocation":
                    comment = f"\b\b, {statement.expression.member} method "
                else:
                    comment = f"Calls the {statement.expression.member} method "
                    LAST_EXPR = "MethodInvocation"
            return comment
        if type(statement.expression).__name__ == "Assignment":
            LAST_EXPR = "Assignment"
            match statement.expression.type:
                case "+=":
                    return f"Increments {stringify_statement(statement.expression.expressionl)} by {stringify_statement(statement.expression.value)} "
                case "-=":
                    return f"Subtracts {stringify_statement(statement.expression.value)} from {stringify_statement(statement.expression.expressionl)} "
                case "*=":
                    return f"Multiplies {stringify_statement(statement.expression.expressionl)} with {stringify_statement(statement.expression.value)} "
                case "/=":
                    return f"Divides {stringify_statement(statement.expression.expressionl)} by {stringify_statement(statement.expression.value)} "
                case "%=":
                    return f"Updates the value of {stringify_statement(statement.expression.expressionl)} by taking its modulus with {stringify_statement(statement.expression.value)} "
                case "=":
                    return f"Assigns {stringify_statement(statement.expression.value)} to {stringify_statement(statement.expression.expressionl)} "
        if type(statement.expression).__name__ == "MemberReference":
            LAST_EXPR = "MemberReference"
            if statement.expression.postfix_operators[0] == "++" or statement.expression.prefix_operators[0] == "++":
                return f"Increments the {statement.expression.member} "
            if statement.expression.postfix_operators[0] == "--" or statement.expression.prefix_operators[0] == "--":
                return f"Decrements the {statement.expression.member} "
    elif type(statement).__name__ == "ReturnStatement":
        LAST_EXPR = "ReturnStatement"
        return f"Returns {stringify_statement(statement.expression)} "
    elif type(statement).__name__ == "LocalVariableDeclaration":
        if LAST_EXPR == "LocalVariableDeclaration":
            comment = f"\b\b, {statement.declarators[0].name} with {stringify_statement(statement.declarators[0].initializer)} "
        else:
            comment = f"Initializes {statement.declarators[0].name} with {stringify_statement(statement.declarators[0].initializer)} "
        LAST_EXPR = "LocalVariableDeclaration"
        return comment
    elif type(statement).__name__ == "ContinueStatement":
        return f"Continues "
    elif type(statement).__name__ == "BreakStatement":
        return f"Breaks "
    return ""


def apply_backspace(s):
    while True:
        # if you find a character followed by a backspace, remove both
        t = re.sub('.\b', '', s, count=1)
        if len(s) == len(t):
            # now remove any backspaces from beginning of string
            return re.sub('\b+', '', t)
        s = t


if __name__ == "__main__":
    main()


# TODO: Stringify parenthesis
# TODO: Noktaların top level blockları ayırdığından bahset sunumda
# TODO: Maybe add special comment to start if there is only one return. (Returns bruhMoment.)
# TODO: Sentence structure in comments, also punctuation
# TODO: When does the inner comments of a for loop end and the comment for the statement after for begin
# TODO: Recursive function commenting (so complicated)
# TODO: Web Crawling (Look at the qualifier and if it is a well known java class send that to google)
