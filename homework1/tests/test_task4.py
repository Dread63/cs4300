import pytest
from decimal import Decimal
from fractions import Fraction

from src.task4 import calculate_discount


@pytest.mark.parametrize(
    "price, discount, expected",
    [
        (50, 10, 45),                                  # int / int
        (67.67, 32.5, 45.67725),                       # float / float
        (55.45, 15, 47.1325),                          # float / int (mixed)
        (80, 80.20, 15.84),                            # int / float (mixed)
        (100, 0, 100),                                 # zero discount: no change
        (100, 100, 0),                                 # full discount boundary
        (0, 50, 0),                                    # zero price
        (-100, 50, -50),                               # negative price stays numeric
        (True, 10, 0.9),                               # bools ARE ints: True == 1
    ],
    ids=["int-int", "float-float", "float-int", "int-float",
         "zero-discount", "full-discount", "zero-price", "negative-price",
         "bool-price"],
)
def test_calculate_discount_duck_typing(price, discount, expected):
    assert calculate_discount(price, discount) == pytest.approx(expected)


def test_calculate_discount_accepts_decimal():
    """
    decimal.Decimal is not int or float, but the math works on it —
    duck typing accepts it (and gives exact decimal arithmetic).
    """
    assert calculate_discount(Decimal("100"), Decimal("25")) == Decimal("75.00")


def test_calculate_discount_accepts_fraction():
    """
    fractions.Fraction is also rejected by class-based checks but works fine.
    """
    assert calculate_discount(Fraction(200), Fraction(25)) == 150


@pytest.mark.parametrize(
    "price, discount",
    [
        ("100", 10),      # str
        (100, "10"),      # str
        (None, 10),       # None
        ([100], 10),      # list
        (100, [10]),      # list
    ],
    ids=["str-price", "str-discount", "none-price", "list-price",
         "list-discount"],
)
def test_calculate_discount_rejects_non_numeric(price, discount):
    with pytest.raises(TypeError):
        calculate_discount(price, discount)


@pytest.mark.parametrize(
    "discount",
    [150, -5, 100.01, -0.1],
    ids=["over-100", "negative", "float-over", "tiny-negative"],
)
def test_calculate_discount_rejects_out_of_range(discount):
    with pytest.raises(ValueError):
        calculate_discount(100, discount)


def test_calculate_discount_rejects_out_of_range_decimal():
    """
    The [0, 100] business rule applies to every numeric type.
    """
    with pytest.raises(ValueError):
        calculate_discount(Decimal("100"), Decimal("150"))
