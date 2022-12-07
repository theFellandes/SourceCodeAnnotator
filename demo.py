from Controller.java_controller import JavaController


class JavaFunction:
    function_name = ""
    params = []

    def __init__(self, function_tree):
        self.function_tree = function_tree
        self.get_param_names()
        self.get_function_name()

    def get_param_names(self):
        for param_name in self.function_tree.parameters:
            self.params.append(param_name.name)

    def get_function_name(self):
        self.function_name = self.function_tree.name




def main():
    controller = JavaController("Main.java")
    cu = controller.get_ast()
    print(cu)
    function = JavaFunction(cu.types[0].body[1])
    # print(cu.types[0].body[1].return_type.name)
    # method = cu.types[0].body[1]
    # print(method, "\n\n")
    # comment_return(method)
    # for statement_type in method.body:
    #     if type(statement_type).__name__ == "ReturnStatement":
    #         print(type(statement_type.expression).__name__)


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


def get_name_or_value(statement):
    if type(statement.expression).__name__ == "MemberReference":
        return statement.expression.member
    if type(statement.expression).__name__ == "literal":
        return statement.value


if __name__ == "__main__":
    main()
