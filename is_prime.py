def is_prime(n):
    """Return 'True' is n is prime, return 'False' otherwise"""
    if n == 1:
        return False
    for d in range(2,n):
        if n % d == 0:
            return False
    return True
