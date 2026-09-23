import math

import pytest

from src.task7 import log_ten, remainder, round_number

# ---------- round_number ----------

@pytest.mark.parametrize(
    "value, digits, expected",
    [
        (3.14159, 2, 3.14),
        (2.71828, 3, 2.718),
        (1.41421, 4, 1.4142),
        (0.57721, 5, 0.57721),
        (-1.23456, 2, -1.23),
        (0, 3, 0),
        (100.0, 0, 100.0),     
        (1.005, 2, 1.0),           
        (2.675, 2, 2.67),          
    ],
)
def test_round_number(value, digits, expected):
    assert math.isclose(round_number(value, digits), expected)


def test_round_number_negative_digits():
    # Rounding left of the decimal point
    assert round_number(1234.5, -2) == 1200.0


def test_round_number_returns_float():
    assert isinstance(round_number(3.14159, 2), float)


# ---------- log_ten ----------

@pytest.mark.parametrize(
    "value, expected",
    [
        (100, 2.0),
        (1000, 3.0),
        (1, 0.0),        # log10(1) == 0
        (10, 1.0),
        (0.1, -1.0),     # works for fractions < 1
        (1e6, 6.0),
    ],
)
def test_log_ten(value, expected):
    assert math.isclose(log_ten(value), expected)


@pytest.mark.parametrize("bad_value", [0, -10])
def test_log_ten_invalid_input_raises(bad_value):
    
    with pytest.raises(Exception):
        log_ten(bad_value)

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 3, 1),
        (15, 4, 3),
        (20, 6, 2),
        (25, 7, 4),
        (30, 8, 6),
        (12, 4, 0), 
        (0, 5, 0),     
        (-10, 3, 2),     
        (10.5, 2, 0.5),  
    ],
)
def test_remainder(a, b, expected):
    assert math.isclose(remainder(a, b), expected)

def test_remainder_divide_by_zero_raises():
    with pytest.raises(Exception):
        remainder(10, 0)
