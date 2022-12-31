from Controller.java_controller import JavaController


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
            comment_functions(member)
            function_count += 1
        if type(member).__name__ == "FieldDeclaration":
            field_count += len(member.declarators)

    inherit_string = f"\n* Inherits from {inherits_from}" if inherits_from else ""
    implements_string = f"\n* Implements {', '.join(map(str, implements))}" if implements else ""

    class_comment = f"/**\n* {cu.types[0].name}{inherit_string}{implements_string}\n* Has {function_count} method(s)" \
                    f"\n* Has {field_count} attribute(s)\n*/"
    print(class_comment)


# function = JavaFunction(cu.types[0].body[1])
    # method = cu.types[0].body[2]
    # print(method, "\n\n")
    # comment_return(method)
    # for statement_type in method.body:
    #     if type(statement_type).__name__ == "ReturnStatement":
    #         print(type(statement_type.expression).__name__)


def comment_functions(function):
    java_function = JavaFunction(function)
    for line in function.body:
        java_function.get_variable_names_where_params_are_used(line)
        print(comment_loop(line))
        print(comment_switch(line))
        print(comment_if(line))
    print(java_function.params_used)


class JavaFunction:
    def __init__(self, function_tree):
        self.function_tree = function_tree
        self.function_name = ""
        self.params = []
        self.params_used = {}
        self.get_param_names()
        self.get_function_name()

    def get_param_names(self):
        for param_name in self.function_tree.parameters:
            self.params.append(param_name.name)

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


def comment_switch(statement):
    if type(statement).__name__ == "SwitchStatement":
        expression = stringify_statement(statement.expression)
        case_comment = ""
        for switch_case in statement.cases:
            if switch_case.case:
                case_comment += f"If {expression} is {stringify_statement(switch_case.case[0])}, "
            else:
                case_comment += f"Else "
        return case_comment
    return ""


def comment_class(class_declaration, package=""):

    print("Bruh moment")


if __name__ == "__main__":
    main()

# TODO: Put function comments together and place it into the file.
# TODO: ChatGPT communication.
# TODO: Super function commenting
# TODO: Recursive function commenting
# TODO: Commenting statements' bodies
# TODO: Web Crawling
