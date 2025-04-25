import pytest

from safecatch.multi_safecatch import multi_safecatch_handler


@multi_safecatch_handler({ZeroDivisionError: 0, ValueError: -1})
def check_func(x, y):
    if y == 0:
        return x / y  # Raises ZeroDivisionError

    elif y < 0:
        raise ValueError("Negative value!")  # Raises ValueError
    else:
        return x + y


def test_multi_exception_success():
    # When no exception occurs, the function should return the correct result.
    assert check_func(3, 2) == 5


def test_multi_exception_zero_division():
    # When a ZeroDivisionError occurs, the decorator should return 0.
    assert check_func(3, 0) == 0


def test_multi_exception_value_error():
    # When a ValueError occurs, the decorator should return -1.
    assert check_func(3, -1) == -1


def test_unhandled_exception_in_multi():
    # If an exception that is not handled occurs, it should propagate.
    @multi_safecatch_handler({ValueError: -1})
    def raise_type_error():
        raise TypeError("Unhandled exception")

    with pytest.raises(TypeError):
        raise_type_error()
