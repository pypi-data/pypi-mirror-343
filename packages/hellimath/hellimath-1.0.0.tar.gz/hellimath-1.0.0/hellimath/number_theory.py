import math

def is_prime(n):
    """ Checks if n is a prime number """
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a, b):
    """ Computes greatest common divisor (GCD) """
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """ Computes least common multiple (LCM) """
    return abs(a * b) // gcd(a, b)