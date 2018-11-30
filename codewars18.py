def zero(*args):
    if not args:
        return 0
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 0 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 0 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 0 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 0 // type_of_operation[0][1]

def one(*args):
    if not args:
        return 1
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 1 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 1 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 1 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 1 // type_of_operation[0][1]

def two(*args):
    if not args:
        return 2
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 2 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 2 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 2 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 2 // type_of_operation[0][1]

def three(*args):
    if not args:
        return 3
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 3 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 3 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 3 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 3 // type_of_operation[0][1]

def four(*args):
    if not args:
        return 4
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 4 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 4 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 4 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 4 // type_of_operation[0][1]

def five(*args):
    if not args:
        return 5
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 5 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 5 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 5 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 5 // type_of_operation[0][1]

def six(*args):
    if not args:
        return 6
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 6 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 6 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 6 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 6 // type_of_operation[0][1]

def seven(*args):
    if not args:
        return 7
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 7 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 7 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 7 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 7 // type_of_operation[0][1]

def eight(*args):
    if not args:
        return 8
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 8 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 8 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 8 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 8 // type_of_operation[0][1]

def nine(*args):
    if not args:
        return 9
    else:
        type_of_operation = args
        if type_of_operation[0][0] == 'multiplication':
            return 9 * type_of_operation[0][1]
        if type_of_operation[0][0] == 'sum':
            return 9 + type_of_operation[0][1]
        if type_of_operation[0][0] == 'substraction':
            return 9 - type_of_operation[0][1]
        if type_of_operation[0][0] == 'division':
            return 9 // type_of_operation[0][1]

def plus(num):
    operation = 'sum'
    return operation,num

def minus(num):
    operation = 'substraction'
    return operation,num

def times(num):
    operation = 'multiplication'
    return operation,num

def divided_by(num):
    operation = 'division'
    return operation,num


def zero(f = None): return 0 if not f else f(0)
def one(f = None): return 1 if not f else f(1)
def two(f = None): return 2 if not f else f(2)
def three(f = None): return 3 if not f else f(3)
def four(f = None): return 4 if not f else f(4)
def five(f = None): return 5 if not f else f(5)
def six(f = None): return 6 if not f else f(6)
def seven(f = None): return 7 if not f else f(7)
def eight(f = None): return 8 if not f else f(8)
def nine(f = None): return 9 if not f else f(9)

def plus(y): return lambda x: x+y
def minus(y): return lambda x: x-y
def times(y): return lambda  x: x*y
def divided_by(y): return lambda  x: x/y



result = eight(times(five()))
print(result)
