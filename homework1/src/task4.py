def calculate_discount(price, discount):
    """
    Calculates the final price of a product after applying a given discount
    percentage.

    Uses duck typing: any type is accepted as long as the value *behaves*
    like a number — i.e. it supports the numeric operations used here
    (int, float, decimal.Decimal, fractions.Fraction, ...). If a value
    does not behave like a number, the arithmetic itself raises TypeError,
    which is re-raised with a clearer message.

    Args:
        price: The original price of the product (any numeric type).
        discount: The discount percentage to apply, between 0 and 100.

    Returns:
        The final price after the discount is applied. The return type
        follows Python's numeric type promotion rules (e.g. a Decimal
        price with a Decimal discount returns a Decimal).

    Raises:
        TypeError: If price or discount does not support numeric operations.
        ValueError: If discount is outside the range [0, 100].
    """
    try:
        result = price - (price * (discount / 100))
    except TypeError as exc:
        raise TypeError(
            "price and discount must support numeric operations "
            f"(got {type(price).__name__}, {type(discount).__name__})"
        ) from exc

    if not 0 <= discount <= 100:
        raise ValueError(f"discount must be between 0 and 100, got {discount}")

    return result


if __name__ == "__main__":
    print(calculate_discount(100, 25))                                  # 75.0
    print(calculate_discount(59.99, 15))                                # 50.9915
    from decimal import Decimal
    from fractions import Fraction
    print(calculate_discount(Decimal("100"), Decimal("25")))            # Decimal('75.00')
    print(calculate_discount(Fraction(200), Fraction(25)))              # 150
