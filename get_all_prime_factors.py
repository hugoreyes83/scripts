from is_prime import is_prime_v3

def getallprimefactors(n):
    """Returns all the prime factors of a positive integer"""
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            print(n)
            n /= d
        d += 1
    return factors

get_prime_factors = getallprimefactors(50)
print(get_prime_factors)
for i in get_prime_factors:
    if is_prime_v3(i):
        print('{} is prime'.format(i))
    else:
        print('{} is NOT prime'.format(i))
