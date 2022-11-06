from functools import wraps
import astpretty
import pprintpp


def pretty_object(func):
    """Pretty prints the returned object from the function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        pprintpp.pprint(vars(func(*args, **kwargs)), indent=4)

    return wrapper


def python_ast_prettier(func):
    """Pretty prints Python AST returned from function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        astpretty.pprint(func(*args, **kwargs))

    return wrapper
