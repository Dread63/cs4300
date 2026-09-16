def positive_negative(number):
    if number > 0:
        print("Positive")
    elif number < 0:
        print("Negative")
    else:
        print("Zero")

def print_prime_numbers():
    
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
    
    sum = 0
    for i in range(1, 101):
        sum += i

    print(sum)