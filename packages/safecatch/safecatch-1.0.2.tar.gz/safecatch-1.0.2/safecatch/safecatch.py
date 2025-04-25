from functools import wraps

from typing import Any, Type


def safecatch_handler(exc_type: Type[Exception], ret_val: Any):
    """
    A decorator that catches a specified exception and returns ret_val if it occurs.

    :param exc_type: Exception type to catch (e.g., ValueError, ZeroDivisionError, etc.)
    :param ret_val: Value to return if the exception is raised.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_type:
                return ret_val

        return wrapper

    return decorator
