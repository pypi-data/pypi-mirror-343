import pytest

from safecatch.safecatch import safecatch_handler


@safecatch_handler(ZeroDivisionError, 0)
def divide(a, b):
    return a / b


def test_divide_success():
    # When no exception occurs, the function should return the correct result.
    assert divide(10, 2) == 5


def test_divide_exception():
    # When a ZeroDivisionError occurs, the decorator should return 0.
    assert divide(10, 0) == 0


def test_unhandled_exception():
    # If the raised exception is not the one handled, it should propagate.
    @safecatch_handler(ValueError, "handled")
    def raise_type_error():
        raise TypeError("This is a TypeError")

    with pytest.raises(TypeError):
        raise_type_error()
