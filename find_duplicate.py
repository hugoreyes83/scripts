def find_duplicate(s):
    '''function returns first duplicate in string'''
    list1 = []
    for i in s:
        if i in list1:
            return i
        else:
            list1.append(i)
    return None

if __name__ == '__main__':
    find_duplicate()
