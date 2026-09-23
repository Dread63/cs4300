def get_integer():
    """
    Returns a sample integer, demonstrating the int data type.
    """
    return 5


def get_floating_point():
    """
    Returns a sample floating-point number, demonstrating the float data type.
    """
    return 5.75


def get_string():
    """
    Returns a sample string, demonstrating the str data type.
    """
    return "Architecture"


def get_boolean():
    """
    Returns a sample boolean, demonstrating the bool data type.
    """
    return False


def main():
    """
    Demonstrates Python's core data types: integers, floats, strings,
    and booleans by declaring, modifying, and printing each one.
    """
    integer = get_integer()
    floating_point = get_floating_point()
    string = get_string()
    boolean = get_boolean()

    for _ in range(0, 10):
        integer = integer * 2
    print(integer)

    floating_point = floating_point * (5.5765)
    print(floating_point)

    string = string + " is super important!"
    print(string)

    string = string.replace("s", "X")
    print(string)

    for _ in range(0, 10):
        if not boolean:
            print("Statement True!")
        else:
            print("Statement False!")
        boolean = not boolean


if __name__ == "__main__":
    main()
