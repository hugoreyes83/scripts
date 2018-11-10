def square_digits(num):
    result = [str(int(i)**2) for i in str(num)]
    return int(''.join(result))

result = square_digits(9119)
print(result)
