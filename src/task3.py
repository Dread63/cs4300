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

def print_prime_numbers():
    """
    Uses a while loop to find and print the first 10 prime numbers.
    """
    primes = []

    currentNum = 0
    while len(primes) < 10:
        isPrime = True

        if currentNum < 2:
            isPrime = False
        else:
            for i in range (2, currentNum):
                if currentNum % i == 0:
                    isPrime = False

        if isPrime:
            primes.append(currentNum)
            print(currentNum)

        currentNum += 1
                    
def sum_one_one_hundred():
    """
    Uses a for loop to sum the numbers from 1 to 100 and prints the result.
    """
    sum = 0
    for i in range(1, 101):
        sum += i

    print(sum)