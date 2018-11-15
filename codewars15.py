def countBits(n):
    return str(bin(n)[2:]).count('1')

result = countBits(1111)
print(result)
