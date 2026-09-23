def calculate_discount(price, discount):
    """
    Calculates the final price of a product after applying a given discount
    percentage. Accepts any numeric type (int or float) for price and discount.

    Args:
        price: The original price of the product (int or float).
        discount: The discount percentage to apply, between 0 and 100.

    Returns:
        The final price after the discount is applied.

    Raises:
        TypeError: If price or discount is not an int or float.
        ValueError: If discount is outside the range [0, 100].
    """
    for name, value in (("price", price), ("discount", discount)):
        # bool is a subclass of int, so check for it explicitly.
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(
                f"{name} must be an int or float, got {type(value).__name__}"
            )

    if not 0 <= discount <= 100:
        raise ValueError(f"discount must be between 0 and 100, got {discount}")

    return price - (price * (discount / 100))


if __name__ == "__main__":
    print(calculate_discount(100, 25))    # 75.0
    print(calculate_discount(59.99, 15))  # 50.9915
