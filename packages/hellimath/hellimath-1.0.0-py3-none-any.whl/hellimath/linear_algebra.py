import numpy as np

def dot_product(vec1, vec2):
    """ Computes dot product of two vectors """
    return np.dot(vec1, vec2)

def determinant(matrix):
    """ Computes determinant of a matrix """
    return np.linalg.det(matrix)