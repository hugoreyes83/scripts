def dbl_linear(n):
    list_of_items = [1]
    for i in range(0,n,1):
        sorted_list = sorted(list_of_items)
        if (2 * sorted_list[i] + 1) not in list_of_items:
            list_of_items.append(2 * sorted_list[i] + 1)
        if (3 * sorted_list[i] + 1) not in list_of_items:
            list_of_items.append(3 * sorted_list[i] + 1)
    return sorted(list_of_items)[n]

def dbl_linear1(n):
    u = [1]
    # dont get why the n*5 value worked tbh got tired of tryng
    for i in range(n*5):
        u.extend([2*u[i]+1,3*u[i]+1])
    return sorted(list(set(u)))[n]

result = dbl_linear1(10)
print(result)
