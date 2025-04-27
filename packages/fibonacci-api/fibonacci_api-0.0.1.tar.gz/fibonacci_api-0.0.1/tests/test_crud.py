import pytest
from hypothesis import given
from hypothesis.strategies import integers
from fibonacci_api import crud


@pytest.mark.parametrize(
    "test_input,expected",
    [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8), (12, 144)],
)
def test_calculate_fibonacci(test_input: int, expected: int):
    assert crud.calculate_fibonacci(test_input) == expected


@given(integers(min_value=2, max_value=30))
def test_fibonacci_rule(n: int):
    assert crud.calculate_fibonacci(n) == crud.calculate_fibonacci(
        n - 1
    ) + crud.calculate_fibonacci(n - 2)


def test_calculate_fibonacci_wrong_input():
    with pytest.raises(ValueError):
        crud.calculate_fibonacci(-1)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((1, 0, 5), (0, 1, 1)),
        ((2, 0, 5), (0, 2, 2)),
        ((5, 0, 2), (0, 2, 2)),
        ((5, 1, 2), (2, 4, 2)),
        ((5, 2, 2), (4, 5, 1)),
        ((5, 3, 2), (6, 5, 0)),
    ],
)
def test_pagination(test_input, expected):
    _range = crud.get_page(*test_input)
    assert _range.start == expected[0]
    assert _range.stop == expected[1]
    assert len(_range) == expected[2]
