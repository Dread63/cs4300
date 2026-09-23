import pytest

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
    ],
    ids=["int-int", "float-float", "float-int", "int-float",
         "zero-discount", "full-discount", "zero-price", "negative-price"],
)
def test_calculate_discount_duck_typing(price, discount, expected):
    assert calculate_discount(price, discount) == pytest.approx(expected)


@pytest.mark.parametrize(
    "price, discount",
    [
        ("100", 10),      # str
        (100, "10"),      # str
        (None, 10),       # None
        ([100], 10),      # list
        (100, [10]),      # list
        (True, 10),       # bool masquerading as int
        (100, False),     # bool discount
    ],
    ids=["str-price", "str-discount", "none-price", "list-price",
         "list-discount", "bool-price", "bool-discount"],
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
