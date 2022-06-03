from random import seed, random, shuffle, randint, choice
from functools import reduce

def operation(operator):
    """
    A utility function used in order to determine the operation corresponding
    to the operator that is given in string format
    """
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b if a > b else b - a
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None