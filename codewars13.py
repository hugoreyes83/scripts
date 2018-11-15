def rgb(r, g, b):
    list1 = [r,g,b]
    list2 = []

    for i in list1:
        if i < 0:
            i = 0
        elif i > 255:
            i = 255
        if len(hex(i)[2:]) == 1:
            var = '0'+str(hex(i)[2:])
            list2.append(var.upper())
        else:
            list2.append(hex(i).upper()[2:])

    return ''.join(list2)

result = rgb(300,300,300)
print(result)
