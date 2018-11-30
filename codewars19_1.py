def add1(x):
    def sum(y):
        def sum1(z):
            return x + y + z
        return sum1
    return sum

def add(x):
    return x

def sum_numbers(*args):
    n = 0
    for i in args:
        n += i
    return n

result = sum_numbers(add(1),add(2),add(3),add(4),add(5))
print(result)

'''
result = add(3)(1)(3)
print(result)
'''
