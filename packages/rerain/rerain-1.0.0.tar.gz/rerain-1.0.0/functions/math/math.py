import math

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def power(a, b):
    return a ** b

def sqrt(a):
    if a < 0:
        raise ValueError("Cannot compute the square root of a negative number")
    return math.sqrt(a)

def abs_value(a):
    return abs(a)

def log(a):
    if a <= 0:
        raise ValueError("Logarithm undefined for non-positive numbers")
    return math.log(a)

def log10(a):
    if a <= 0:
        raise ValueError("Logarithm undefined for non-positive numbers")
    return math.log10(a)

def sin(a):
    return math.sin(a)

def cos(a):
    return math.cos(a)

def tan(a):
    return math.tan(a)

def atan(a):
    return math.atan(a)

def nth_root(a, n):
    if n == 0:
        raise ValueError("Cannot compute the 0th root")
    return a ** (1/n)

def factorial(a):
    if a < 0:
        raise ValueError("Factorial is undefined for negative numbers")
    return math.factorial(a)

def exp(a):
    return math.exp(a)

def pi():
    return math.pi

def e():
    return math.e

def sin_deg(a):
    return math.sin(math.radians(a))

def cos_deg(a):
    return math.cos(math.radians(a))

def tan_deg(a):
    return math.tan(math.radians(a))

def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

def integral(f, a, b, n=1000):
    h = (b - a) / n
    return sum(f(a + i * h) * h for i in range(n))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def combination(n, r):
    return factorial(n) // (factorial(r) * factorial(n - r))

def permutation(n, r):
    return factorial(n) // factorial(n - r)
