import numpy

def round_number(value, digits):
    """
    Rounds a number to a specified number of decimal places.
    """
    return round(value, digits)

def log_ten(value):
    """
    Returns the base-10 logarithm of a number.
    """
    if value <= 0:
        raise ValueError("log10 is undefined for zero or negative values.")
    return numpy.log10(value)

def remainder(a, b):
    """
    Returns the remainder of a divided by b.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return numpy.remainder(a, b)

if __name__ == "__main__":
    # Example usage
    print(round_number(3.14159, 2))  # Output: 3.14
    print(log_ten(100))               # Output: 2.0
    print(remainder(10, 3))           # Output: 1.0