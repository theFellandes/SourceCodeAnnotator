from Controller.java_controller import JavaController


def main():
    controller = JavaController("Main.java")
    cu = controller.get_ast()
    print(cu)
    functions = cu.types[0].body
    for function in functions:
        java_function = JavaFunction(function)
        for line in function.body:
            java_function.get_variable_names_where_params_are_used(line)
            comment_loops(line)
        print(java_function.params_used)
    # function = JavaFunction(cu.types[0].body[1])
    # method = cu.types[0].body[1]
    # print(method, "\n\n")
    # comment_return(method)
    # for statement_type in method.body:
    #     if type(statement_type).__name__ == "ReturnStatement":
    #         print(type(statement_type.expression).__name__)


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
            if type(statement_type.expression).__name__ == "MemberReference":
                print("Returns " + statement_type.expression.member)
            if type(statement_type.expression).__name__ == "Literal":
                print("Returns " + statement_type.expression.value)
            if type(statement_type.expression).__name__ == "BinaryOperation":
                print("Returns", statement_type.expression.operandl.member,
                      statement_type.expression.operator, statement_type.expression.operandr.value)


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


def comment_loops(statement):
    if type(statement).__name__ == "ForStatement":
        iter_condition = stringify_statement(statement.control.condition)
        iter_declaration = stringify_statement(statement.control.init)
        return f"Iterates from {iter_declaration} until {iter_condition} is false, "
    elif type(statement).__name__ == "WhileStatement":
        iter_condition = stringify_statement(statement.condition)
        return f"Loops until {iter_condition} is false, "


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


if __name__ == "__main__":
    main()
