def positive_negative(number):
    """
    Checks whether a number is positive, negative, or zero and prints the result.
    """
    if number > 0:
        print("Positive")
    elif number < 0:
        print("Negative")
    else:
        print("Zero")


def is_prime(candidate):
    """
    Returns True if the given integer is a prime number, False otherwise.
    """
    if candidate < 2:
        return False
    for divisor in range(2, candidate):
        if candidate % divisor == 0:
            return False
    return True


def print_prime_numbers():
    """
    Uses a for loop to print the first 10 prime numbers.
    """
    primes = []
    for candidate in range(2, 30):
        if len(primes) == 10:
            break
        if is_prime(candidate):
            primes.append(candidate)
            print(candidate)


def sum_one_one_hundred():
    """
    Uses a while loop to sum the numbers from 1 to 100 and prints the result.
    """
    total = 0
    number = 1
    while number <= 100:
        total += number
        number += 1
    print(total)


if __name__ == "__main__":
    positive_negative(7)
    print_prime_numbers()
    sum_one_one_hundred()
