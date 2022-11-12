import sys
from functools import wraps
from conf import settings


def ast_to_file(func):
    """Redirects sys.stdout to the ast report file"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        with open(settings.AST_REPORT_PATH, 'w') as sys.stdout:
            func(*args, **kwargs)

        sys.stdout = sys.__stdout__

    return wrapper
