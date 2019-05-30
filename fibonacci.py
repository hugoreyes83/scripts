def fibonacci(n):
    '''function returns fibonacci sequence up to provided number'''
    fibonacci_list = [0,1,1]
    for i in range(3,n+1):
        fibonacci_list.insert(i,fibonacci_list[i-1]+fibonacci_list[i-2])
    return fibonacci_list[n-1]

print(fibonacci(10))
