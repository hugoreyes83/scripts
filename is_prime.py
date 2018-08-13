import math

def is_prime_v1(n):
    """Return 'True' is n is prime, return 'False' otherwise"""
    if n == 1:
        return False
    for d in range(2,n):
        if n % d == 0:
            return False
    return True

def is_prime_v2(n):
    """Return 'True' is n is prime, return 'False' otherwise"""
    if n == 1:
        return False
    max_divisor = math.floor(math.sqrt(n))
    for d in range(2,max_divisor + 1):
        if n % d == 0:
            return False
    return True

def is_prime_v3(n):
    """Return 'True' is n is prime, return 'False' otherwise"""
    if n == 1:
        return False
    if n > 2 or n % 2 == 0:
        return False
    max_divisor = math.floor(math.sqrt(n))
    for d in range(3, max_divisor + 1, 2):
        if n % d == 0:
            return False
    return True
