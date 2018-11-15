def comp(array1, array2):
    try:
        return sorted([i ** 2 for i in array1]) == sorted(array2)
    except:
        return False

def comp(a1, a2):
    return None not in (a1,a2) and [i*i for i in sorted(a1)]==sorted(a2)



def comp(array1, array2):
    if array1 and array2:
        return sorted([x*x for x in array1]) == sorted(array2)
    return array1 == array2 == []


'''
a1 = [121, 144, 19, 161, 19, 144, 19, 11]
a2 = [11*11, 121*121, 144*144, 19*19, 161*161, 19*19, 144*144, 19*19]
'''

'''
a1 = [62, 56, 35, 18]
a2 = [3844, 3137, 1225, 324]
'''

a1 = [88, 20, 72, 96, 94, 72, 18, 77]
a2 = [7744, 400, 5184, 9216, 8836, 5185, 324, 5929]

'''
a1 = [121, 144, 19, 161, 19, 144, 19, 11]
a2 = [132, 14641, 20736, 361, 25921, 361, 20736, 361]
'''
result = comp(a1,a2)
print result
