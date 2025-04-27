
def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: Division by zero is not allowed."
def power(a, b):
    return a ** b
def square_root(a):
    if a >= 0:
        return a ** 0.5
    else:
        return "Error: Square root of a negative number is not defined."