from functools import wraps

from typing import Dict, Any, Type


def multi_safecatch_handler(exception_map: Dict[Type[Exception], Any]):
    """
    A decorator that catches multiple specified exceptions and returns the corresponding
    fallback value from exception_map if one of them occurs.

    :param exception_map: A dictionary mapping exception types to fallback return values.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                for exc, ret_val in exception_map.items():
                    if isinstance(e, exc):
                        return ret_val
                raise

        return wrapper

    return decorator
