import pytest
from src.task4 import calculate_discount

def test_calculate_discount_int():

    assert calculate_discount(50, 10) == 45

def test_calculate_discount_float():

    assert calculate_discount(67.67, 32.5) == pytest.approx(45.67725) # Approx used to make sure small deviations on floats don't make test cases fail

def test_calculate_discount_mixed():

    assert calculate_discount(55.45, 15) == pytest.approx(47.1325)
    assert calculate_discount(80, 80.20) == pytest.approx(15.84)