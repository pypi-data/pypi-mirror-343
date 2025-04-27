import sympy as sp

def differentiate(expression, variable):
    """ Returns derivative of an expression """
    x = sp.Symbol(variable)
    return sp.diff(expression, x)

import scipy.integrate as spi

def definite_integral(func, a, b):
    """ Computes definite integral of function between a and b """
    result, _ = spi.quad(func, a, b)
    return result