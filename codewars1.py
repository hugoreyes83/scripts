def unique_in_order(iterable):
    mylist = []
    previous_element = ""
    for i in iterable:
        if i == previous_element:
            previous_element = i
        else:
            mylist.append(i)
            previous_element = i
    return mylist

result = unique_in_order('AAAABBBCCDAABBB')
print(result)
