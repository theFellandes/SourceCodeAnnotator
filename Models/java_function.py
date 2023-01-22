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