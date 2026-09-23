def calculate_discount(price, discount):
    """
    Calculates the final price of a product after applying a given discount
    percentage. Accepts any numeric type for price and discount.
    """
    return price - (price * (discount/100))
