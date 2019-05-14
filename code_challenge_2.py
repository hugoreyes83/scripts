def find_limit(n):
    left,right = None,None
    sortedlist = sorted(n)
    for i in range(len(n)):
        if n[i] != sortedlist[i] and left is None:
            left = i
        elif n[i] != sortedlist[i]:
            right = i
    return left,right

list1 = [2,3,6,1,5]


print(find_limit(list1))
