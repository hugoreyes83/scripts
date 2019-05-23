from collections import Counter
def find_unique(s):
    '''function returns first unique character in a string'''
    string_count = Counter(s.replace(' ',''))
    for i in string_count:
        if string_count[i] == 1:
            return i
        else:
            continue
    return None



if __name__ == '__main__':
    find_unique()
