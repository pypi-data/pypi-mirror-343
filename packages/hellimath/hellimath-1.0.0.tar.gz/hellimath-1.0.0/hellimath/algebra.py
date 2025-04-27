import math

def solve_quadratic(a, b, c):
    """ Solves ax² + bx + c = 0 """
    delta = b**2 - 4*a*c
    if delta < 0:
        return "No real solutions"
    x1 = (-b + math.sqrt(delta)) / (2*a)
    x2 = (-b - math.sqrt(delta)) / (2*a)
    return x1, x2

def factorial(n):
    """ Computes factorial of n """
    return 1 if n in [0, 1] else n * factorial(n - 1)

def fibonacci(n):
    """ Returns the nth Fibonacci number """
    if n == 0: return 0
    if n == 1: return 1
    return fibonacci(n-1) + fibonacci(n-2)